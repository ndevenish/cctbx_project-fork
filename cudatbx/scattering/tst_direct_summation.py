from __future__ import absolute_import, division, print_function
import math
from iotbx import pdb
from libtbx.test_utils import approx_equal
from scitbx.array_family import flex
from scitbx import matrix
from scitbx.math.des_3_240_21 import t_x,t_y,t_z
from six.moves import range

test_pdb = "\
CRYST1  127.692  225.403  306.106  90.00  90.00  90.00 P 21 21 21    4\n\
ATOM      1  N   SER A  10      72.910  42.823  25.407  1.00103.66           N\n\
ATOM      2  CA  SER A  10      71.864  43.176  26.422  1.00102.96           C\n\
ATOM      3  C   SER A  10      72.181  44.524  27.077  1.00102.77           C\n\
ATOM      4  O   SER A  10      73.190  44.668  27.780  1.00102.38           O\n\
ATOM      5  CB  SER A  10      71.772  42.081  27.500  1.00102.67           C\n\
ATOM      6  OG  SER A  10      70.697  42.316  28.402  1.00102.53           O\n\
ATOM      7  N   ALA A  11      71.311  45.507  26.841  1.00102.05           N\n\
ATOM      8  CA  ALA A  11      71.483  46.845  27.402  1.00100.38           C\n\
ATOM      9  C   ALA A  11      71.640  46.741  28.922  1.00 99.29           C\n\
END\n\
"

# =============================================================================
def test_direct_summation():

  # correct values
  p = pdb.input(source_info='string',lines=test_pdb)
  x = p.xray_structure_simple()
  for s in x.scatterers():
    s.set_use_u(False,False)

  fc = x.structure_factors(anomalous_flag=False,d_min=2.0,
                           algorithm='direct').f_calc()
  fcd = fc.data()
  indices = fc.indices()

  # test values
  xyz = x.sites_frac()
  h = flex.vec3_double(len(indices))
  fm = matrix.sqr(p.crystal_symmetry().unit_cell().fractionalization_matrix())
  om = matrix.sqr(p.crystal_symmetry().unit_cell().orthogonalization_matrix())
  for i in range(len(indices)):
    h[i] = fm * indices[i]
  sr = x.scattering_type_registry()
  st = x.scattering_types()

  sg = p.crystal_symmetry().space_group()
  r = flex.double()
  t = flex.vec3_double(len(sg))
  for i in range(len(sg)):
    r_i = om * matrix.sqr(sg[i].r().as_double())
    for a in r_i:
      r.append(a)
    t[i] = om * matrix.col(sg[i].t().as_double())

  bls = flex.double(len(xyz),0.0)
  amplitudes = direct_summation()
  amplitudes.add(st,xyz,bls,h,r,t,sr,False)
  amplitudes = amplitudes.get_sum()

  cpu_i = flex.norm(fcd)
  gpu_i = flex.norm(amplitudes)

  mean = 0.0
  for i in range(len(cpu_i)):
    e = math.fabs(cpu_i[i] - gpu_i[i])/cpu_i[i]
    mean += e
  mean = mean/(len(cpu_i))
  assert(mean < 1.0e-3)

# =============================================================================
def test_saxs():

  p = pdb.input(source_info='string',lines=test_pdb)
  x = p.xray_structure_simple()
  xyz = x.sites_cart()
  blsf = flex.double(len(xyz),0.0)
  sr = x.scattering_type_registry()
  st = x.scattering_types()
  q = flex.double(range(101))/200.0

  t_w = flex.double(len(t_x),1.0)

  l = flex.double()
  l.extend(t_x)
  l.extend(t_y)
  l.extend(t_z)

  intensities = direct_summation()
  intensities.prepare_saxs(st,xyz,blsf,q,t_w,l,sr,False)
  intensities.run_saxs_kernel()
  intensities.sum_over_lattice()
  intensities = intensities.get_sum()

  assert(approx_equal(intensities[10].real,3584.9828125,out=None))


# =============================================================================
if (__name__ == '__main__'):
  import libtbx.load_env
  if (libtbx.env.build_options.enable_cuda):
    from cudatbx.scattering import direct_summation
    test_direct_summation()
    test_saxs()

  print('Ok')
