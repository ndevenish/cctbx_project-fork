import sys, os.path

import operator_functor_info

def write_copyright(f):
  try: name = __file__
  except: name = sys.argv[0]
  print >> f, \
"""/* Copyright (c) 2001-2002 The Regents of the University of California
   through E.O. Lawrence Berkeley National Laboratory, subject to
   approval by the U.S. Department of Energy.
   See files COPYRIGHT.txt and LICENSE.txt for further details.

   Revision history:
     2002 Aug: Copied from cctbx/global (Ralf W. Grosse-Kunstleve)
     2002 Feb: Created (Ralf W. Grosse-Kunstleve)

   *****************************************************
   THIS IS AN AUTOMATICALLY GENERATED FILE. DO NOT EDIT.
   *****************************************************

   Generated by:
     %s
 */""" % (name,)

def generate_unary(f, name, op):
  print >> f, """
  template <typename ResultType,
            typename ArgumentType>
  struct functor_%s {
    typedef ResultType result_type;
    ResultType operator()(ArgumentType const& x) const {
      return ResultType(%s);
    }
  };""" % (name, op)

def generate_binary(f, name, op):
  print >> f, """
  template <typename ResultType,
            typename ArgumentType1,
            typename ArgumentType2>
  struct functor_%s {
    typedef ResultType result_type;
    ResultType operator()(ArgumentType1 const& x,
                          ArgumentType2 const& y) const {
      return ResultType(%s);
    }
  };""" % (name, op)

def generate_in_place_binary(f, name, op):
  print >> f, """
  template <typename ArgumentType1,
            typename ArgumentType2>
  struct functor_%s {
    ArgumentType1& operator()(ArgumentType1& x,
                              ArgumentType2 const& y) const {
      %s;
      return x;
    }
  };""" % (name, op)

def run(target_dir):
  output_file_name = os.path.normpath(os.path.join(
    target_dir, "operator_functors.h"))
  print "Generating:", output_file_name
  f = open(output_file_name, "w")
  write_copyright(f)
  print >> f, """
#ifndef SCITBX_ARRAY_FAMILY_OPERATOR_FUNCTORS_H
#define SCITBX_ARRAY_FAMILY_OPERATOR_FUNCTORS_H

namespace scitbx { namespace fn {"""

  for op, ftor_name in operator_functor_info.unary_functors.items():
    generate_unary(f, ftor_name, op + "x")
  for op, ftor_name in operator_functor_info.binary_functors.items():
    generate_binary(f, ftor_name, "x " + op + " y")
  for op, ftor_name in operator_functor_info.in_place_binary_functors.items():
    generate_in_place_binary(f, ftor_name, "x " + op + " y")

  print >> f, """
}} // namespace scitbx::fn

#endif // SCITBX_ARRAY_FAMILY_OPERATOR_FUNCTORS_H"""
  f.close()

if (__name__ == "__main__"):
  run(".")
