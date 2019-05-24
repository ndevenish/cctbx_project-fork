#!/usr/bin/env cctbx.python
#
#  Copyright (C) (2016) STFC Rutherford Appleton Laboratory, UK.
#
#  Author: David Waterman.
#
#  This code is distributed under the BSD license, a copy of which is
#  included in the root directory of this package.
#

from __future__ import division, print_function
from scitbx.array_family import flex
from scitbx.math.periodogram import Periodogram
from libtbx.test_utils import approx_equal

# This is the "discoveries" dataset from R, giving the number of "great"
# inventions and scientific discoveries in each year from 1860 to 1959.
dat = flex.double([5,3,0,2,0,3,2,3,6,1,2,1,2,1,3,3,3,5,2,4,4,0,2,3,7,12,3,10,9,
2,3,7,7,2,3,3,6,2,4,3,5,2,2,4,0,4,2,5,2,3,3,6,5,8,3,6,6,0,5,2,2,2,6,3,4,4,2,2,
4,7,5,3,3,0,2,2,2,1,3,4,2,2,1,1,1,2,1,4,4,3,2,1,4,1,1,1,0,0,2,0])

# The tests here were originally against calls made to R using rpy2. Here the
# values returned by those calls are written out explicitly.

def test_raw_even_and_odd_length():
  """Test raw periodogram of even and odd length sequences versus results
  obtained using R's spec.pgram function."""

  # even-length
  pgram = Periodogram(dat)
  rspec = flex.double([28.95417436723208,
                       8.804110562933733,
                       18.49821426322232,
                       4.094928274829677,
                       10.664583495648557,
                       0.9510798979384458,
                       4.818019271965207,
                       8.7890132834726,
                       0.34895472871642474,
                       4.298708963847126,
                       17.808223044747802,
                       0.43460105379492137,
                       9.846548561891545,
                       0.7189166875859443,
                       1.5700713159868809,
                       7.006058124904175,
                       0.34542255079605266,
                       3.1168239060632974,
                       1.263928801888548,
                       0.01861054239907847,
                       1.6636054250587091,
                       1.882713242160402,
                       1.1719572134942402,
                       1.5202775036250407,
                       9.849072239357147,
                       8.154656878294267,
                       3.5445494165048013,
                       1.0058616277307482,
                       4.232126563022536,
                       5.144050304879019,
                       3.5369877391028433,
                       3.096569282327231,
                       2.8433497727678416,
                       0.5666508873501074,
                       1.9719884560263852,
                       10.127938512870841,
                       1.7824474672209123,
                       4.724527776009507,
                       3.9087766384313976,
                       6.6956845513767265,
                       0.6830967285296601,
                       4.935588195925854,
                       0.5748537866060414,
                       1.6844746497921799,
                       9.263139681830246,
                       7.47129442196606,
                       4.762894221668351,
                       0.3223925047950684,
                       0.5826957996969294,
                       0.10068673474008037])

  rfreq = flex.double(0.01 * e for e in (range(1,51)))
  assert approx_equal(pgram.spec, rspec)
  assert approx_equal(pgram.freq, rfreq)

  # odd-length
  dat2 = dat[0:99]
  pgram = Periodogram(dat2)
  rspec = flex.double([27.378734487215517,
                       8.300597643964354,
                       18.601570728645616,
                       4.401309169508969,
                       9.81615913184789,
                       1.2198000269161602,
                       5.2778352616536175,
                       8.22707610023193,
                       0.8865216983472878,
                       2.8232693965537834,
                       20.1615730381271,
                       0.11712370567046958,
                       8.88090348832551,
                       0.5966571692115259,
                       1.9402032941479643,
                       7.389059053524231,
                       1.8478623100240048,
                       2.087060370495997,
                       1.4918451091166665,
                       0.29469653682276337,
                       3.3114401807871734,
                       0.34065845307496007,
                       1.2416790352786125,
                       2.162525614248078,
                       11.588418669622571,
                       7.736166858429692,
                       1.9797555750271172,
                       2.179422742788905,
                       7.124078571174135,
                       1.7626318917205566,
                       4.097247214701129,
                       3.484527330303516,
                       1.2144485874993167,
                       1.085059335676423,
                       8.41344396898852,
                       3.7261271115507744,
                       0.3362106092460046,
                       5.5128561313938516,
                       3.212041963064243,
                       5.261688734349363,
                       2.32174787318873,
                       4.50066920034715,
                       0.4679419198572981,
                       2.9281768538056987,
                       8.883073168591967,
                       8.952596303235458,
                       1.2239788162354133,
                       0.3633295633047963,
                       0.24463991145416633])
  rfreq = flex.double(1/99 * e for e in (range(1,50)))
  assert approx_equal(pgram.spec, rspec)
  assert approx_equal(pgram.freq, rfreq)

  print("OK")

def test_smoothed_even_and_odd_length():
  """Test smoothed periodogram of even and odd length sequences versus results
  obtained using R's spec.pgram function"""

  # single kernel smoother, even length
  pgram = Periodogram(dat, spans=4)
  rspec = flex.double([22.60966340315627,
                       18.195262628604752,
                       12.801658008106513,
                       9.533830316034159,
                       6.842177109002613,
                       5.718913361175838,
                       5.016220391389688,
                       4.145220428761756,
                       6.187449533598165,
                       6.766923476486281,
                       6.909821176923462,
                       7.649546371537703,
                       5.17230337090994,
                       3.9639665387034815,
                       3.5977579212052033,
                       2.709855572127937,
                       2.971326160175313,
                       2.0596273980998854,
                       1.350969309569581,
                       1.3614783358645521,
                       1.1957180543273982,
                       1.371929975931356,
                       2.582821697871905,
                       4.389998004175942,
                       5.470564984068996,
                       5.702837024958528,
                       4.936416830929916,
                       3.8579727997111832,
                       3.4807017683590322,
                       3.7410950155083493,
                       3.82883637355107,
                       3.0830643475781216,
                       2.3152645100024487,
                       2.998560753435843,
                       3.7448691190604286,
                       4.131990941949487,
                       4.893824075832538,
                       4.706890853446401,
                       4.14044026592323,
                       4.029403976076368,
                       3.639046172087742,
                       2.595904577911505,
                       3.042008709376008,
                       4.431477356793608,
                       5.271945689431424,
                       5.625190475689571,
                       4.369874722298269,
                       2.363493276128358,
                       0.9196425124786836,
                       0.39711770973225585])
  assert approx_equal(pgram.spec, rspec)

  # three kernel smoothers with differing lengths, odd length sequence
  dat2 = dat[0:99]
  pgram = Periodogram(dat2, spans=[4,6,4])
  rspec = flex.double([17.314055274775985,
                       15.746715010053997,
                       13.51918957394817,
                       11.096669833901974,
                       8.94488071864728,
                       7.357033921545414,
                       6.4291723412721415,
                       6.06483632171929,
                       6.0180027558874265,
                       6.0556124717493125,
                       6.000976488762685,
                       5.756178307862047,
                       5.315663331116168,
                       4.716140919888478,
                       4.055823092903159,
                       3.4305933136199633,
                       2.8881959432238777,
                       2.4700815936067313,
                       2.2043629196392005,
                       2.1371110039637147,
                       2.318359384971553,
                       2.737953359136525,
                       3.3119078691830612,
                       3.8971755852383345,
                       4.358224117959523,
                       4.610902643634579,
                       4.617256999182198,
                       4.404925734628821,
                       4.07304004821836,
                       3.742088947852017,
                       3.4988298970826084,
                       3.377951237167512,
                       3.3623755402288427,
                       3.4107737746104503,
                       3.493901696666407,
                       3.5886989978152486,
                       3.6571955223055133,
                       3.6669320372957337,
                       3.6399826234621893,
                       3.6368323534539106,
                       3.701389530366984,
                       3.8389251460239517,
                       3.9895437773918845,
                       4.046699282044061,
                       3.92426466711323,
                       3.5960187967975505,
                       3.122909791584781,
                       2.6492847490141163,
                       2.349620740074152])

  assert approx_equal(pgram.spec, rspec)
  print("OK")

if __name__=="__main__":

  test_raw_even_and_odd_length()
  test_smoothed_even_and_odd_length()

  print("OK")
