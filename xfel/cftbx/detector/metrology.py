# -*- mode: python; coding: utf-8; indent-tabs-mode: nil; python-indent: 2 -*-
#
# $Id$

"""The metrology module does conversion of this and that.  XXX Need to
describe the keys of the dictionaries here.  XXX Just like in OpenGL,
all matrices are to be pre-multiplied (with column vectors)?
"""
from __future__ import division

from scitbx import matrix


def _average_transformation(matrices, keys):
  """The _average_transformation() function determines the average
  rotation and translation from the transformation matrices in @p
  matrices with keys matching @p keys.  The function returns a
  two-tuple of the average rotation in quaternion representation and
  the average translation.
  """

  from scitbx.array_family import flex
  from tntbx import svd

  # Sum all rotation matrices and translation vectors.
  sum_R = flex.double(flex.grid(3, 3))
  sum_t = flex.double(flex.grid(3, 1))
  nmemb = 0
  for key in keys:
    T = matrices[key][1]
    sum_R += flex.double([T(0, 0), T(0, 1), T(0, 2),
                          T(1, 0), T(1, 1), T(1, 2),
                          T(2, 0), T(2, 1), T(2, 2)])
    sum_t += flex.double([T(0, 3), T(1, 3), T(2, 3)])
    nmemb += 1
  if nmemb == 0:
    # Return zero-rotation and zero-translation.
    return (matrix.col([1, 0, 0, 0]), matrix.zeros((3, 1)))

  # Calculate average rotation matrix as U * V^T where sum_R = U * S *
  # V^T and S diagonal (Curtis et al. (1993) 377-385 XXX proper
  # citation, repeat search), and convert to quaternion.
  svd = svd(sum_R)
  R_avg = matrix.sqr(list(svd.u().matrix_multiply_transpose(svd.v())))
  o_avg = R_avg.r3_rotation_matrix_as_unit_quaternion()
  t_avg = matrix.col(list(sum_t / nmemb))

  return (o_avg, t_avg)


def _transform(o, t):
  """The _transform() function returns the transformation matrices in
  homogeneous coordinates between the parent and child frames.  The
  forward transform maps coordinates in the parent frame to the child
  frame, and the backward transform provides the inverse.  The last
  row of the product of any two homogeneous transformation matrices is
  always (0, 0, 0, 1).

  @param o Orientation of child w.r.t. parent, as a unit quaternion
  @param t Translation of child w.r.t. parent
  @return  Two-tuple of the forward and backward transformation
           matrices
  """

  Rb = o.unit_quaternion_as_r3_rotation_matrix()
  tb = t
  Tb = matrix.sqr((Rb(0, 0), Rb(0, 1), Rb(0, 2), tb(0, 0),
                   Rb(1, 0), Rb(1, 1), Rb(1, 2), tb(1, 0),
                   Rb(2, 0), Rb(2, 1), Rb(2, 2), tb(2, 0),
                   0,        0,        0,        1))
  Rf = Rb.transpose()
  tf = -Rf * t
  Tf = matrix.sqr((Rf(0, 0), Rf(0, 1), Rf(0, 2), tf(0, 0),
                   Rf(1, 0), Rf(1, 1), Rf(1, 2), tf(1, 0),
                   Rf(2, 0), Rf(2, 1), Rf(2, 2), tf(2, 0),
                   0,        0,        0,        1))
  return (Tf, Tb)


def get_projection_matrix(dim_pixel, dim_readout):
  """The get_projection_matrix() function returns the projection
  matrices in homogeneous coordinates between readout frame and
  fractional row and column indices.  The forward transform maps
  coordinates in the readout frame, i.e. [x, y, z, 1], to readout
  indices, i.e. [i, j, 1], where i and j are the row and column
  indices, respectively.  The backward transform provides the inverse.
  The get_projection_matrix() function assumes that coordinates in the
  readout frame are pixel centers.  XXX Bad name!  Better
  readout2metric(), readout_projection_matrices()?

  @note If coordinates in the readout frame are the top, left corner
        of the pixel, pass dim_readout=(readout_width_in_pixels + 1,
        readout_height_in_pixels + 1).

  @param dim_pixel   Two-tuple of pixel width and height, in meters
  @param dim_readout Two-tuple of readout width and height, in pixels
  @return            Two-tuple of the forward and backward projection
                     matrices
  """

  Pb = matrix.rec(
    elems=(0, +dim_pixel[0], dim_pixel[0] * (1 - dim_readout[0]) / 2,
           -dim_pixel[1], 0, dim_pixel[1] * (dim_readout[1] - 1) / 2,
           0, 0, 0,
           0, 0, 1),
    n=(4, 3))
  Pf = matrix.rec(
    elems=(0, -1 / dim_pixel[1], 0, (dim_readout[1] - 1) / 2,
           +1 / dim_pixel[0], 0, 0, (dim_readout[0] - 1) / 2,
           0, 0, 0, 1),
    n=(3, 4))
  return (Pf, Pb)


def metrology_as_dxtbx_vectors(params):
  """The metrology_as_dxtbx_vectors() functions converts a pure Python
  object extracted from a metrology Phil object to a dictionary of
  DXTBX-style transformation vectors.  Only ASIC:s are considered,
  since DXTBX metrology is not concerned with hierarchies

  The DXTBX-style metrology description consists of three vectors for
  each ASIC.  The first vector locates the (0, 0)-pixel in the
  laboratory frame. The second and third vectors give the locations of
  the pixels immediately next to (0, 0) in the fast and slow
  directions, respectively.  All vectors are in units of mm.

  @param params Pure Python object, extracted from a metrology Phil
                object
  @return       Dictionary of DXTBX-style metrology description
  """

  d = params.detector
  Tb_d = _transform(matrix.col(d.orientation),
                    matrix.col(d.translation))[1]
  vectors = {}
  for p in d.panel:
    Tb_p = Tb_d * _transform(matrix.col(p.orientation).normalize(),
                             matrix.col(p.translation))[1]

    for s in p.sensor:
      Tb_s = Tb_p * _transform(matrix.col(s.orientation).normalize(),
                               matrix.col(s.translation))[1]

      for a in s.asic:
        Tb_a = Tb_s * _transform(matrix.col(a.orientation).normalize(),
                                 matrix.col(a.translation))[1]
        Pb = get_projection_matrix(a.pixel_size, a.dimension)[1]

        v_00 = Tb_a * Pb * matrix.col((0, 0, 1))
        v_01 = Tb_a * Pb * matrix.col((0, 1, 1))
        v_10 = Tb_a * Pb * matrix.col((1, 0, 1))

        vectors[(d.serial, p.serial, s.serial, a.serial)] = (
          matrix.col((t * 1e3).elems[0:3])
          for t in [v_00, v_01 - v_00, v_10 - v_00])

  return vectors


def metrology_as_transformation_matrices(params):
  """XXX What if the child is invisible from the parent (pointing away
  from the parent)?  XXX What if two elements are overlapping?
  Implement bounding boxes (only needed for transformation/projection
  from eye to ASIC).  XXX Projections implemented elsewhere.

  XXX Should probably be something like "phil_to_matrix_dict" and put
  the metrology2phil() function here, too!

  XXX It was not such a great idea to include the final projection
  here--it made it impossible to recover z!

  XXX Normalisation of orientation may be necessary to guarantee that
  rotation matrices are orthogonal if the serialisation truncated the
  numbers.

  @param params Pure Python object, extracted from a metrology Phil
                object
  @return       Dictionary of homogeneous transformation matrices
  """

  d = params.detector
  T_d = _transform(matrix.col(d.orientation).normalize(),
                   matrix.col(d.translation))

  matrices = {(0,): T_d}
  for p in d.panel:
    T_p = _transform(matrix.col(p.orientation).normalize(),
                     matrix.col(p.translation))
    T_p = (T_p[0] * T_d[0], T_d[1] * T_p[1])

    matrices[(d.serial, p.serial)] = T_p

    for s in p.sensor:
      T_s = _transform(matrix.col(s.orientation).normalize(),
                       matrix.col(s.translation))
      T_s = (T_s[0] * T_p[0], T_p[1] * T_s[1])

      matrices[(d.serial, p.serial, s.serial)] = T_s

      for a in s.asic:
        T_a = _transform(matrix.col(a.orientation).normalize(),
                         matrix.col(a.translation))
        T_a = (T_a[0] * T_s[0], T_s[1] * T_a[1])

        matrices[(d.serial, p.serial, s.serial, a.serial)] = (T_a[0], T_a[1])

  return matrices


def regularize_transformation_matrices(matrices, key=(0,)):
  """The _regularize_transformation_matrices() function recursively sets
  the transformation of each element to the average transformation of
  its children.  XXX Round average orientations to multiples of 90
  degrees?  XXX Should they maybe return matrices instead?.
  """

  # The length of the key tuple identifies the current recursion
  # depth.
  next_depth = len(key) + 1

  # Base case: return if at the maximum depth.
  keys = [k for k in matrices.keys()
          if (len(k) == next_depth and k[0:next_depth - 1] == key)]
  if (len(keys) == 0):
    return

  # Recursion: regularize at next depth, and get the average.
  for k in keys:
    regularize_transformation_matrices(matrices, k)
  o, t = _average_transformation(matrices, keys)
  matrices[key] = _transform(o, t)
