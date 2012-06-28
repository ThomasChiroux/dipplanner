#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2011 Thomas Chiroux
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.
# If not, see <http://www.gnu.org/licenses/gpl.html>
#
# This module is part of dipplanner, a Dive planning Tool written in python
"""Test Dives with air
"""

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
  ]

import unittest
# import here the module / classes to be tested
from dive import Dive
from dive import ProcessingError, NothingToProcess, InfiniteDeco
from tank import Tank, EmptyTank
from segment import SegmentDive, SegmentDeco, SegmentAscDesc
from segment import UnauthorizedMod
import dipplanner
from tools import seconds_to_mmss
import settings

class TestDive(unittest.TestCase):
  def setUp(self):
    # temporary hack (tests):
    dipplanner.activate_debug_for_tests()

    settings.RUN_TIME = True
    settings.SURFACE_TEMP = 12
    self.air12l = Tank(tank_vol=12.0, tank_pressure=200, tank_rule="10b")
    self.airtank = Tank(tank_vol=18.0, tank_pressure=200, tank_rule="10b")
    self.airtank12 = Tank(tank_vol=12.0, tank_pressure=200, tank_rule="10b")
    self.airdouble = Tank(tank_vol=30.0, tank_pressure=200, tank_rule="10b") #bi15l 200b
    self.txtank1 = Tank(0.21, 0.30, tank_vol=30.0, tank_pressure=200, tank_rule="10b")
    self.txtanknormodbl = Tank(0.21, 0.30, tank_vol=30.0, tank_pressure=200, tank_rule="10b")
    self.deco1 = Tank(0.8, 0.0, tank_vol=7.0, tank_pressure=200, tank_rule="10b")
    self.deco2 = Tank(0.5, 0.0, tank_vol=7.0, tank_pressure=200, tank_rule="10b")
    self.decoo2 = Tank(1.0, 0.0, tank_vol=7.0, tank_pressure=200, tank_rule="10b")

# ==============================================================================
# ======= S Y S T E M A T I C        T E S T S =================================
# ==============================================================================

# Tx Normo =====================================================================
class TestRepetitiveTxDive1(TestDive):
  def setUp(self):
    TestDive.setUp(self)

    diveseg1 = SegmentDive(55, 20*60, self.txtank1, 0)
    self.profile0 = Dive([diveseg1], [self.txtank1])
    self.profile0.do_dive()

    diveseg2 = SegmentDive(50, 20*60, self.txtank1, 0)
    self.profile1 = Dive([diveseg2], [self.txtank1], self.profile0)
    self.profile1.do_surface_interval(20*60)
    #self.profile1.refill_tanks()
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_mmss(self.profile1.run_time) == "124:44", "bad dive runtime ? (%s)" % seconds_to_mmss(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 55.5549635111, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 21.1631708375, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtank1.used_gas, 4006.7619273, 7, "bad used gas (%s)" % self.txtank1.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

  def test_no_flight(self):
    no_flight_time = self.profile1.no_flight_time()
    self.assertEqual(no_flight_time, 12660, "Bad no flight time: %s" % no_flight_time)

class TestRepetitiveTxDive2(TestDive):
  def setUp(self):
    TestDive.setUp(self)

    diveseg1 = SegmentDive(55, 20*60, self.txtank1, 0)
    self.profile0 = Dive([diveseg1], [self.txtank1])
    self.profile0.do_dive()

    diveseg2 = SegmentDive(50, 20*60, self.txtank1, 0)
    self.profile1 = Dive([diveseg2], [self.txtank1], self.profile0)
    self.profile1.do_surface_interval(30*60)
    self.profile1.do_dive()

    diveseg3 = SegmentDive(35, 35*60, self.txtank1, 0)
    self.profile2 = Dive([diveseg3], [self.txtank1], self.profile1)
    self.profile2.do_surface_interval(60*60)
    #self.profile2.refill_tanks()
    self.profile2.do_dive()

  def test_RT(self):
    assert seconds_to_mmss(self.profile2.run_time) == "166:21", "bad dive runtime ? (%s)" % seconds_to_mmss(self.profile2.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile2.model.ox_tox.otu, 86.5037540773, 7, "bad dive OTU ? (%s)" % self.profile2.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile2.model.ox_tox.cns * 100, 24.2843630006, 7, "bad dive CNS ? (%s)" % (self.profile2.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtank1.used_gas, 4979.54636588, 7, "bad used gas (%s)" % self.txtank1.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile2.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile2.tanks[0].check_rule())

  def test_no_flight(self):
    no_flight_time = self.profile2.no_flight_time()
    self.assertEqual(no_flight_time, 18960, "Bad no flight time: %s" % no_flight_time)

class TestRepetitiveTxDive3(TestDive):
  def setUp(self):
    TestDive.setUp(self)

    diveseg1 = SegmentDive(55, 20*60, self.txtank1, 0)
    self.profile0 = Dive([diveseg1], [self.txtank1])
    self.profile0.do_dive()

    diveseg2 = SegmentDive(50, 20*60, self.txtank1, 0)
    self.profile1 = Dive([diveseg2], [self.txtank1], self.profile0)
    self.profile1.do_surface_interval(30*60)
    self.profile1.do_dive()

    diveseg3 = SegmentDive(35, 35*60, self.txtank1, 0)
    self.profile2 = Dive([diveseg3], [self.txtank1], self.profile1)
    self.profile2.do_surface_interval(60*60)
    #self.profile2.refill_tanks()
    self.profile2.do_dive()

    diveseg4 = SegmentDive(55, 20*60, self.txtank1, 0)
    self.profile3 = Dive([diveseg4], [self.txtank1], self.profile2)
    self.profile3.do_surface_interval(12*60*60)
    #self.profile3.refill_tanks()
    self.profile3.do_dive()

  def test_RT(self):
    assert seconds_to_mmss(self.profile3.run_time) == " 72:40", "bad dive runtime ? (%s)" % seconds_to_mmss(self.profile3.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile3.model.ox_tox.otu, 115.825853006, 7, "bad dive OTU ? (%s)" % self.profile3.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile3.model.ox_tox.cns * 100, 12.6208702934, 7, "bad dive CNS ? (%s)" % (self.profile3.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtank1.used_gas, 3350.41341833, 7, "bad used gas (%s)" % self.txtank1.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile3.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile2.tanks[0].check_rule())

  def test_no_flight(self):
    no_flight_time = self.profile3.no_flight_time()
    self.assertEqual(no_flight_time, 7380, "Bad no flight time: %s" % no_flight_time)

# ==============================================================================
# ========================== M A I N ===========================================
# ==============================================================================
if __name__ == "__main__":
  import sys
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument('tests', metavar='TestName', type=str, nargs='*',
                      help='name of the tests to run (separated by space) [optionnal]')
  args = parser.parse_args()
  if args.tests:
    suite = unittest.TestLoader().loadTestsFromNames(args.tests, sys.modules[__name__])
  else:
    suite = unittest.findTestCases(sys.modules[__name__])
  unittest.TextTestRunner(verbosity=2).run(suite)
