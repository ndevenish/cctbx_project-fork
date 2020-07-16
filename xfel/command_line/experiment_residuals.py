from __future__ import absolute_import, division, print_function

# LIBTBX_SET_DISPATCHER_NAME cctbx.xfel.experiment_residuals

from libtbx.phil import parse
import numpy as np
import pylab as plt
import sys
from dials.util import show_mail_on_error

help_message = '''
Visualize prediction offsets for a single shot experiment

Example:

  cctbx.xfel.experiment_residuals refined.expt indexed.refl
'''

phil_scope = parse('''
lscale = 25
  .type = float
  .help = scale the offset vector by this amount
lcolor = #777777
  .type = str
  .help = display the offset vector with this color
scatt_cmap = bwr
  .type = str
  .help = display the scatter points with this pylab colormap
clim = None
  .type = floats(size=2)
  .help = colormap limits e.g. clim=[-0.01, 0.01]
axcol = w
  .type = str
  .help = pylab axis face color
mark_scale = 15
  .type = int
  .help = scale of scatter plot marker
edge_color = #777777
  .type = str
  .help = color of marker edge
edge_width = 0.5
  .type = float
  .help = width of marker edge
headlen = 0.5
  .type = float
  .help = length of pylab arrow head
headwid = 0.5
  .type = float
  .help = width of pylab arrow head
noarrow = False
  .type = bool
  .help = do not add arrows to plot
cbarshrink = 0.5
  .type = float
  .help = factor by which to shrink the displayed colorbar
exper_id = 0
  .type = int
  .help = experiment id (if experiment file is multi-shot)
title = None
  .type = str
  .help = title of the plot
''', process_includes=True)


class Script:

  def __init__(self):
    from dials.util.options import OptionParser

    self.parser = OptionParser(
      usage="",
      sort_options=True,
      phil=phil_scope,
      read_experiments=True,
      read_reflections=True,
      check_format=False,
      epilog=help_message)

  def run(self):
    from dials.util.options import flatten_experiments, flatten_reflections
    params, options = self.parser.parse_args(show_diff_phil=True)

    if len(params.input.experiments) > 1:
      print("Please only pass a single experiment file. Exiting...")
      sys.exit()
    if len(params.input.reflections) > 1:
      print("Please only pass a single reflection file. Exiting...")
      sys.exit()

    # do stuff
    ax = plt.gca()

    El = flatten_experiments(params.input.experiments)
    R = flatten_reflections(params.input.reflections)[0]

    nexper = len(El)
    nexper_in_refl = len(set(R["id"]))
    if not nexper == nexper_in_refl:
      print("There are %d experiments and %d possible reflection sets, experiment and reflection table out of sync"
            % (nexper, nexper_in_refl))
      sys.exit()
    if params.exper_id < 0:
      print("Exper Id must be greater than 0")
      sys.exit()
    if params.exper_id > nexper:
      print("exper_id must be less than maximum number of experiments (=%d)" % nexper)
      sys.exit()

    DET = El[params.exper_id].detector
    R = R.select(R["id"] == params.exper_id)

    nref = len(R)

    xyz = np.zeros((nref, 3))
    for i_ref in range(nref):
      x, y, _ = R[i_ref]["xyzobs.mm.value"]
      xcal, ycal, _ = R[i_ref]["xyzcal.mm"]
      pid = R[i_ref]['panel']
      panel = DET[pid]
      xyz_lab = panel.get_lab_coord((x,y))
      xyz_cal_lab = panel.get_lab_coord((xcal, ycal))
      xyz[i_ref] = xyz_lab

      diff = np.array(xyz_lab) - np.array(xyz_cal_lab)
      diff_scale = diff*params.lscale
      x, y, _ = xyz_lab
      ax.arrow(x, y, diff_scale[0], diff_scale[1], head_width=params.headwid, head_length=params.headlen, color=params.lcolor,
               length_includes_head=not params.noarrow)

    delpsi = R['delpsical.rad']
    xvals, yvals, zvals = xyz.T

    vmax = max(abs(delpsi))
    vmin = -vmax
    if params.clim is not None:
      vmin, vmax = params.clim

    scatt_arg = xvals, yvals
    scat = ax.scatter(*scatt_arg, s=params.mark_scale, c=delpsi, cmap=params.scatt_cmap, vmin=vmin, vmax=vmax, zorder=2,
                      edgecolors=params.edge_color, linewidths=params.edge_width)

    cbar = plt.colorbar(scat, shrink=params.cbarshrink)

    cbar.ax.set_title("$\Delta \psi$")
    ax.set_aspect("equal")
    ax.set_facecolor(params.axcol)
    title = "Arrow points to prediction"
    if params.title is not None:
      title = params.title
    ax.set_title(title)
    plt.show()


if __name__ == '__main__':
  with show_mail_on_error():
    script = Script()
    script.run()
