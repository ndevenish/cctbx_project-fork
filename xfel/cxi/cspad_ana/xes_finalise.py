from __future__ import absolute_import, division, print_function
from six.moves import range
import os
import glob

from libtbx import easy_pickle
from scitbx.array_family import flex
import scitbx.matrix
from xfel.cxi.cspad_ana import cspad_tbx
from math import sin, atan
from six.moves import zip

def cspad_unbound_pixel_mask():
  # Every 10th pixel along the diagonal from the top left hand corner are not
  # bonded, hence we ignore them in the summed spectrum
  mask = flex.int(flex.grid(370, 391), 0)
  for section_offset in ((0,0), (0, 197), (185, 197), (185, 0)):
    for i in range(19):
      mask[section_offset[0] + i * 10, section_offset[1] + i * 10] = 1
  return mask

def cspad2x2_bad_pixel_mask_cxi_run7():
  bad_pixels = set((
    (279,289), (277,254), (273,295), (268,247), (269,260), (281,383), (268,57),
    (262,184), (291,206), (275,106), (261,28), (286,189), (265,304), (284,277)))
  mask = flex.int(flex.grid(370, 391), 0)
  for bad_pixel in bad_pixels:
    mask[bad_pixel] = 1
  return mask


class xes_finalise(object):

  def __init__(self,
               runs,
               output_dirname=".",
               roi=None):
    avg_basename="avg_"
    stddev_basename="stddev"
    self.sum_img = None
    self.sumsq_img = None
    self.nmemb = 0
    self.roi = cspad_tbx.getOptROI(roi)
    self.unbound_pixel_mask = cspad_unbound_pixel_mask()
    for i_run, run in enumerate(runs):
      run_scratch_dir = run
      result = finalise_one_run(run_scratch_dir)
      if result.sum_img is None: continue
      if self.sum_img is None:
        self.sum_img = result.sum_img
        self.sumsq_img = result.sumsq_img
      else:
        self.sum_img += result.sum_img
        self.sumsq_img += result.sumsq_img
      self.nmemb += result.nmemb

    self.avg_img = self.sum_img.as_double() / self.nmemb
    self.stddev_img = flex.sqrt((self.sumsq_img.as_double() - self.sum_img.as_double() * self.avg_img) / (self.nmemb - 1))

    self.mask = flex.int(self.sum_img.accessor(), 0)
    self.mask.set_selected(self.sum_img == 0, 1)
    self.mask.set_selected(self.unbound_pixel_mask > 0, 1)

    if (output_dirname is not None and
        avg_basename is not None):
      if (not os.path.isdir(output_dirname)):
        os.makedirs(output_dirname)
      d = cspad_tbx.dpack(
        address='CxiSc1-0|Cspad2x2-0',
        data=self.avg_img,
        distance=1,
      )
      cspad_tbx.dwritef(d, output_dirname, avg_basename)
      d = cspad_tbx.dpack(
        address='CxiSc1-0|Cspad2x2-0',
        data=self.sum_img,
        distance=1,
      )
      cspad_tbx.dwritef(d, output_dirname, "sum_")
      if 1:
        output_image(self.avg_img, "%s/avg.png" %output_dirname)
        output_image(self.avg_img, "%s/avg_inv.png" %output_dirname, invert=True)

      if 1:
        output_matlab_form(self.sum_img, "%s/sum.m" %output_dirname)
        output_matlab_form(self.avg_img, "%s/avg.m" %output_dirname)
        output_matlab_form(self.stddev_img, "%s/stddev.m" %output_dirname)

    if (stddev_basename is not None):
      d = cspad_tbx.dpack(
        address='CxiSc1-0|Cspad2x2-0',
        data=self.stddev_img,
        distance=1,
      )
      cspad_tbx.dwritef(d, output_dirname, stddev_basename)

      # XXX we should really figure out automatically the area where the spectrum is
      #write an integrated spectrum from lines 186-227
      #spectrum_focus = self.sum_img.as_numpy_array()[186:228,:]
      img = self.sum_img
      if self.roi is None:
        spectrum_focus = img
        mask_focus = self.mask
      else:
        slices = (slice(self.roi[2],self.roi[3]), slice(self.roi[0],self.roi[1]))
        spectrum_focus = img[slices]
        mask_focus = self.mask[slices]
      if False:
        from matplotlib import pylab
        pylab.imshow(spectrum_focus.as_numpy_array())
        pylab.show()

    output_spectrum(spectrum_focus, mask_focus=mask_focus,
                    output_dirname=output_dirname)

    print("Total number of images used from %i runs: %i" %(i_run+1, self.nmemb))

def filter_outlying_pixels(spectrum_focus, mask_focus):
  for i in range(spectrum_focus.all()[0]):
    for j in range(spectrum_focus.all()[1]):
      neighbouring_pixels = flex.double()
      for ii in range(i-1, i+2):
        for jj in range(j-1, j+2):
          if ii == i and jj == j: continue
          try:
            if mask_focus[ii, jj] > 0: continue
            neighbouring_pixels.append(spectrum_focus[ii, jj])
          except IndexError:
            continue
      if len(neighbouring_pixels) == 0: continue
      if spectrum_focus[i, j] > 2 * flex.mean(neighbouring_pixels):
        print("Bad pixel: (%i, %i)" %(i, j))
        spectrum_focus[i, j] = 0
        mask_focus[i,j] = 1

def get_spectrum(spectrum_focus, mask_focus=None):
  spectrum = flex.sum(spectrum_focus, axis=0).as_double()
  # take care of columns where one or more pixels are inactive
  # and/or flagged as a "hot" - in this case the sum is over fewer rows and
  # will introduce artefacts into the spectrum
  if 1 and mask_focus is not None:
    # estimate values for bad pixels as the mean value of
    # neighbouring pixels
    for j in range(spectrum_focus.all()[1]):
      for i in range(spectrum_focus.all()[0]):
        if mask_focus[i,j] > 0:
          neighbouring_pixels = flex.double()
          for ii in range(i-1, i+2):
            for jj in range(j-1, j+2):
              if ii == i and jj == j: continue
              try:
                if mask_focus[ii, jj] > 0: continue
                neighbouring_pixels.append(spectrum_focus[ii, jj])
              except IndexError:
                continue
          if len(neighbouring_pixels) == 0: continue
          spectrum[j] += flex.mean(neighbouring_pixels)
          print("bad pixel at (%i,%i): estimating value from neighbouring pixels: %.0f" %(
            i,j, flex.mean(neighbouring_pixels)))

  if 0 and mask_focus is not None:
    # Upweight columns that contain bad pixels based on the
    # relative strength of the signal on the rows containing
    # bad pixels
    scales = flex.sum(spectrum_focus, axis=1).as_double()
    scales /= flex.sum(scales)
    for j in range(spectrum_focus.all()[1]):
      sum_column_weights = 0
      for i in range(spectrum_focus.all()[0]):
        if mask_focus[i,j] == 0:
          sum_column_weights += scales[i]
      if sum_column_weights < 1:
        print("pixels missing from column %i" %j)
        print(sum_column_weights)
        if sum_column_weights > 0:
          spectrum[j] *= (1/sum_column_weights)

  # Elongated pixels span the gap between a pair of ASICs.
  # These are 2.5x the width of normal pixels, consequently by excluding these
  # pixels we will have a 5 pixel gap in our spectrum.
  # For further details see:
  #   https://confluence.slac.stanford.edu/download/attachments/112107361/PixelPitch.pdf
  omit_col = True
  if omit_col is True:
    #omit_columns = [181,193,194,195,196,197,378] # run 4
    omit_columns = set([193,194,195,196,197]) # run 5
    for column_i in range(1, spectrum.size()-1):
      if (column_i in omit_columns
          or column_i+1 in omit_columns
          or column_i-1 in omit_columns): continue
    plot_x = flex.int(range(spectrum.size()))
    plot_y = spectrum.deep_copy()
    for i in reversed(sorted(omit_columns)):
      del plot_x[i]
      del plot_y[i]
    plot_x += 1
  else:
    plot_x = flex.double(range(1,len(spectrum)+1))
    plot_y = spectrum

  return plot_x, plot_y

#Written by Muhamed Amin
def plot_energy(plot_x):
    plot_E=[x * 0.1109 for x in plot_x]
    plot_E1=[(y/2)-(95*0.1109) for y in plot_E]
    E=[1.2398e+004/(2*0.9601*sin(atan(500/(z+50)))) for z in plot_E1]
    return E

def output_spectrum(spectrum_focus, mask_focus=None, output_dirname=".", run=None):
  plot_x, plot_y = get_spectrum(spectrum_focus, mask_focus=mask_focus)
  if run is not None:  runstr = "_%04d"%run
  else: runstr=""
  spec_plot(plot_x,plot_y,spectrum_focus,
            os.path.join(output_dirname, "spectrum%s"%runstr)+ ".png")
  plot_E=plot_energy(plot_x)
  spec_plot(plot_E,plot_y,spectrum_focus,
            os.path.join(output_dirname, "spectrum_E%s"%runstr)+ ".png")
  f = open(os.path.join(output_dirname, "spectrum%s.txt"%runstr), "wb")
  print("\n".join(["%i %f" %(x, y) for x, y in zip(plot_x, plot_y)]), file=f)
  f.close()

  return plot_x, plot_y

  ## first moment analysis
  ## XXX columns of interest for CXI run 5
  #numerator = 0
  #denominator = 0
  #for i in range(150, 270):
    #numerator += spectrum[i] * i
    #denominator += spectrum[i]
  #first_moment = numerator/denominator
  #print "first moment: ", first_moment

def output_matlab_form(flex_matrix, filename):
  f = open(filename, "wb")
  #print >> f, "%% number of images = %i" %(self.nmemb)
  print(scitbx.matrix.rec(
    flex_matrix, flex_matrix.focus()).matlab_form(one_row_per_line=True), file=f)
  f.close()

def output_image(flex_img, filename, invert=False, scale=False):
  try:
    import PIL.Image as Image
  except ImportError:
    import Image
  flex_img = flex_img.deep_copy()
  flex_img -= flex.min(flex_img)
  if scale:
    img_max_value = 2**16
    scale = img_max_value/flex.max(flex_img)
    flex_img = flex_img.as_double() * scale
    flex_img = flex_img
  if invert:
    img_max_value = 2**16
    flex_img = img_max_value - flex_img # invert image for display
  dim = flex_img.all()
  #easy_pickle.dump("%s/avg_img.pickle" %output_dirname, flex_img)
  byte_str = flex_img.slice_to_byte_str(0,flex_img.size())
  try:
    im = Image.fromstring(mode="I", size=(dim[1],dim[0]), data=byte_str)
  except NotImplementedError:
    im = Image.frombytes(mode="I", size=(dim[1],dim[0]), data=byte_str)
  im = im.crop((0,185,391,370))
  #im.save("avg.tiff", "TIFF") # XXX This does not work (phenix.python -Qnew option)
  im.save(filename, "PNG")

class finalise_one_run(object):

  def __init__(self, scratch_dir):
    pickle_dirname = "pickle"
    pickle_basename = "pkl_"
    self.sum_img = None
    self.sumsq_img = None
    self.nmemb = 0
    path_pattern = "%s/%s/%ss[0-9][0-9]-[0-9].pickle" %(
      scratch_dir, pickle_dirname, pickle_basename)
    g = glob.glob(path_pattern)
    if len(g) == 0:
      print("No files found matching pattern: %s" %path_pattern)
      return
    for path in g:
      try:
        d = easy_pickle.load(file_name=path)
      except EOFError:
        print("EOFError: skipping %s:" %path)
        continue
      if self.sum_img is None:
        self.sum_img = d["sum_img"]
        self.sumsq_img = d["sumsq_img"]
      else:
        self.sum_img += d["sum_img"]
        self.sumsq_img += d["sumsq_img"]
      self.nmemb += d["nmemb"]
      print("Read %d images from %s" % (d["nmemb"], path))
      #print "Si foil length: %s" %(d["sifoil"])

    print("Number of images used: %i" %self.nmemb)
    assert self.nmemb > 0

class first_moment_analysis:
  def __init__(self, x, y):
    self.x = flex.double(list(x)) # sometimes integer array must be coerced to double
    self.y = y
    self.calculate()

  def calculate(self):
    self.first_moment=self.x[0]
    pass
    return

  def as_trace(self):
    return (self.first_moment,self.first_moment), (flex.min(self.y), flex.max(self.y))

def spec_plot(x, y, img, file_name, figure_size=(10,5), transparent=False):
  import matplotlib
  import matplotlib.figure
  import matplotlib.cm
  from matplotlib.backends.backend_agg import FigureCanvasAgg
  figure_size = None

  F = first_moment_analysis(x,y)

  fig = matplotlib.figure.Figure(figure_size, 144, linewidth=0,
      facecolor="white")
  if transparent :
    self.figure.figurePatch.set_alpha(0.0)
  canvas = FigureCanvasAgg(fig)
  p = fig.add_subplot(211)
  p.set_position([0.1,0.3,0.8,0.6])
  p.plot(x, y, '-')
  fm = F.as_trace()
  p.plot(fm[0],fm[1],"r-")
  p.set_xlim(x[0],x[-1])
  p.set_xlabel("position")
  p.set_ylabel("intensity")
  p.set_title("X-ray emission spectrum, first moment=%.2f"%(F.first_moment))
  p2 = fig.add_subplot(212)
  p2.set_position([0.1, 0.05, 0.8, 0.2])
  im=p2.imshow(img.as_numpy_array(), cmap='spectral')
  im.set_interpolation("none")
  position=fig.add_axes([0.91,0.1,0.015,0.35])
#  p2.imshow(img.as_numpy_array(), cmap=matplotlib.cm.gist_yarg)
  p3=fig.colorbar(im, orientation='vertical', cax=position)
#  p2.set_position([0.1, 0.05, 0.8, 0.2])
  canvas.draw()
  fig.savefig(file_name, dpi=200, format="png")


if __name__ == '__main__':
  import sys
  args = sys.argv[1:]
  assert len(args) >= 2
  scratch_dir = args[0]
  runs = args[1:]
  mod_xes_mp_finalise(scratch_dir, runs)
