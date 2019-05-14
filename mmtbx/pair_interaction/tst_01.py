from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
import iotbx.pdb
from libtbx.test_utils import approx_equal
from mmtbx.pair_interaction import pair_interaction

pdb_str = """
REMARK PDB code: 1yjp, renumbered
CRYST1   21.937    4.866   23.477  90.00 107.08  90.00 P 1 21 1      2
ATOM      0  N   GLY A   0      -9.009   4.612   6.102  1.00 16.77           N
ATOM      1  CA  GLY A   0      -9.052   4.207   4.651  1.00 16.57           C
ATOM      2  C   GLY A   0      -8.015   3.140   4.419  1.00 16.16           C
ATOM      3  O   GLY A   0      -7.523   2.521   5.381  1.00 16.78           O
ATOM      4  N   ASN A   1      -7.656   2.923   3.155  1.00 15.02           N
ATOM      5  CA  ASN A   1      -6.522   2.038   2.831  1.00 14.10           C
ATOM      6  C   ASN A   1      -5.241   2.537   3.427  1.00 13.13           C
ATOM      7  O   ASN A   1      -4.978   3.742   3.426  1.00 11.91           O
ATOM      8  CB  ASN A   1      -6.346   1.881   1.341  1.00 15.38           C
ATOM      9  CG  ASN A   1      -7.584   1.342   0.692  1.00 14.08           C
ATOM     10  OD1 ASN A   1      -8.025   0.227   1.016  1.00 17.46           O
ATOM     11  ND2 ASN A   1      -8.204   2.155  -0.169  1.00 11.72           N
ATOM     12  N   ASN A   2      -4.438   1.590   3.905  1.00 12.26           N
ATOM     13  CA  ASN A   2      -3.193   1.904   4.589  1.00 11.74           C
ATOM     14  C   ASN A   2      -1.955   1.332   3.895  1.00 11.10           C
ATOM     15  O   ASN A   2      -1.872   0.119   3.648  1.00 10.42           O
ATOM     16  CB  ASN A   2      -3.259   1.378   6.042  1.00 12.15           C
ATOM     17  CG  ASN A   2      -2.006   1.739   6.861  1.00 12.82           C
ATOM     18  OD1 ASN A   2      -1.702   2.925   7.072  1.00 15.05           O
ATOM     19  ND2 ASN A   2      -1.271   0.715   7.306  1.00 13.48           N
ATOM     20  N   GLN A   3      -1.005   2.228   3.598  1.00 10.29           N
ATOM     21  CA  GLN A   3       0.384   1.888   3.199  1.00 10.53           C
ATOM     22  C   GLN A   3       1.435   2.606   4.088  1.00 10.24           C
ATOM     23  O   GLN A   3       1.547   3.843   4.115  1.00  8.86           O
ATOM     24  CB  GLN A   3       0.656   2.148   1.711  1.00  9.80           C
ATOM     25  CG  GLN A   3       1.944   1.458   1.213  1.00 10.25           C
ATOM     26  CD  GLN A   3       2.504   2.044  -0.089  1.00 12.43           C
ATOM     27  OE1 GLN A   3       2.744   3.268  -0.190  1.00 14.62           O
ATOM     28  NE2 GLN A   3       2.750   1.161  -1.091  1.00  9.05           N
ATOM     29  N   GLN A   4       2.154   1.821   4.871  1.00 10.38           N
ATOM     30  CA  GLN A   4       3.270   2.361   5.640  1.00 11.39           C
ATOM     31  C   GLN A   4       4.594   1.768   5.172  1.00 11.52           C
ATOM     32  O   GLN A   4       4.768   0.546   5.054  1.00 12.05           O
ATOM     33  CB  GLN A   4       3.056   2.183   7.147  1.00 11.96           C
ATOM     34  CG  GLN A   4       1.829   2.950   7.647  1.00 10.81           C
ATOM     35  CD  GLN A   4       1.344   2.414   8.954  1.00 13.10           C
ATOM     36  OE1 GLN A   4       0.774   1.325   9.002  1.00 10.65           O
ATOM     37  NE2 GLN A   4       1.549   3.187  10.039  1.00 12.30           N
ATOM     38  N   ASN A   5       5.514   2.664   4.856  1.00 11.99           N
ATOM     39  CA  ASN A   5       6.831   2.310   4.318  1.00 12.30           C
ATOM     40  C   ASN A   5       7.854   2.761   5.324  1.00 13.40           C
ATOM     41  O   ASN A   5       8.219   3.943   5.374  1.00 13.92           O
ATOM     42  CB  ASN A   5       7.065   3.016   2.993  1.00 12.13           C
ATOM     43  CG  ASN A   5       5.961   2.735   2.003  1.00 12.77           C
ATOM     44  OD1 ASN A   5       5.798   1.604   1.551  1.00 14.27           O
ATOM     45  ND2 ASN A   5       5.195   3.747   1.679  1.00 10.07           N
ATOM     46  N   TYR A   6       8.292   1.817   6.147  1.00 14.70           N
ATOM     47  CA  TYR A   6       9.159   2.144   7.299  1.00 15.18           C
ATOM     48  C   TYR A   6      10.603   2.331   6.885  1.00 15.91           C
ATOM     49  O   TYR A   6      11.041   1.811   5.855  1.00 15.76           O
ATOM     50  CB  TYR A   6       9.061   1.065   8.369  1.00 15.35           C
ATOM     51  CG  TYR A   6       7.665   0.929   8.902  1.00 14.45           C
ATOM     52  CD1 TYR A   6       6.771   0.021   8.327  1.00 15.68           C
ATOM     53  CD2 TYR A   6       7.210   1.756   9.920  1.00 14.80           C
ATOM     54  CE1 TYR A   6       5.480  -0.094   8.796  1.00 13.46           C
ATOM     55  CE2 TYR A   6       5.904   1.649  10.416  1.00 14.33           C
ATOM     56  CZ  TYR A   6       5.047   0.729   9.831  1.00 15.09           C
ATOM     57  OH  TYR A   6       3.766   0.589  10.291  1.00 14.39           O
ATOM     58  OXT TYR A   6      11.358   2.999   7.612  1.00 17.49           O
TER
HETATM   59  O   HOH A   7      -6.471   5.227   7.124  1.00 22.62           O
HETATM   60  O   HOH A   8      10.431   1.858   3.216  1.00 19.71           O
HETATM   61  O   HOH A   9     -11.286   1.756  -1.468  1.00 17.08           O
HETATM   62  O   HOH A  10      11.808   4.179   9.970  1.00 23.99           O
HETATM   63  O   HOH A  11      13.605   1.327   9.198  1.00 26.17           O
HETATM   64  O   HOH A  12      -2.749   3.429  10.024  1.00 39.15           O
HETATM   65  O   HOH A  13      -1.500   0.682  10.967  1.00 43.49           O
END
"""

def run():
  """
  Exercise interaction graph construction.
  """
  pdb_inp = iotbx.pdb.input(source_info=None, lines = pdb_str)
  ph = pdb_inp.construct_hierarchy()
  interaction_list = pair_interaction.run(ph)
  interaction_list.sort()
  print(interaction_list)
  expected_list = [[1, 2], [1, 8], [2, 3], [2, 8], [2, 10], [3, 4], [3, 5], [3, 8],
                   [3, 13], [3, 14], [4, 5], [4, 6], [5, 6], [5, 7], [5, 13], [5, 14],
                   [6, 7], [6, 9], [7, 9], [7, 11], [7, 12], [8, 13], [11, 12], [13, 14]]
  for e1, e2 in zip(expected_list, interaction_list):
    e1, e2 = list(e1), list(e2)
    e1.sort()
    e2.sort()
  expected_list.sort()
  interaction_list.sort()
  assert approx_equal(len(set([tuple(item) for item in expected_list])-set([tuple(item) for item in interaction_list])),0,3)
  assert approx_equal(len(set([tuple(item) for item in interaction_list])-set([tuple(item) for item in expected_list])),0,3)

if(__name__ == "__main__"):
  run()
