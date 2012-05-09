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
"""Test for CC mode
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
from tools import seconds_to_strtime
import settings

class TestDive(unittest.TestCase):
  def setUp(self):
    # temporary hack (tests):
    dipplanner.activate_debug_for_tests()

    self.air = Tank(tank_vol=3.0, tank_pressure=200, tank_rule="10b")
    self.txhypo = Tank(0.10, 0.50, tank_vol=3.0, tank_pressure=200, tank_rule="10b")
    self.setpoint = 1.2

    settings.RUN_TIME = False
    settings.SURFACE_TEMP = 12

# Diluant: AIR =================================================================
# ===================================================== 10m tests ==============
class TestDiveCCAir10m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(10, 10*60, self.air, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.air])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 11:30", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 13.437123003, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 4.83407833333, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.air.used_gas, 0.0 , 7, "bad used gas (%s)" % self.air.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveCCAir10m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(10, 20*60, self.air, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.air])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 21:30", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 26.673627586, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 9.59598309524, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.air.used_gas, 0.0, 7, "bad used gas (%s)" % self.air.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveCCAir10m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(10, 30*60, self.air, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.air])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 31:30", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 39.9101321691, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 14.3578878571, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.air.used_gas, 0.0, 7, "bad used gas (%s)" % self.air.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveCCAir10m40min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(10, 40*60, self.air, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.air])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 41:30", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 53.1466367522, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 19.119792619, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.air.used_gas, 0.0, 7, "bad used gas (%s)" % self.air.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveCCAir10m50min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(10, 50*60, self.air, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.air])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 51:30", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 66.3831413353, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 23.881697381, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.air.used_gas, 0.0, 7, "bad used gas (%s)" % self.air.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveCCAir10m60min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(10, 60*60, self.air, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.air])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 61:30", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 79.6196459184, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 28.6436021429, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.air.used_gas, 0.0, 7, "bad used gas (%s)" % self.air.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveCCAir10m70min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(10, 70*60, self.air, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.air])

  def runTest(self):
    self.profile1.do_dive()
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())
    #except EmptyTank:
    #  pass
    #else:
    #  self.fail("should raise EmptyTank")

# ===================================================== 20m tests ==============
class TestDiveCCAir20m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(20, 10*60, self.air, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.air])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 13:00", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 13.6377414229, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 4.90625190476, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.air.used_gas, 0.0, 7, "bad used gas (%s)" % self.air.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveCCAir20m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(20, 20*60, self.air, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.air])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 22:43", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 26.8561831629, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 9.66165846032, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.air.used_gas, 0.0, 7, "bad used gas (%s)" % self.air.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveCCAir20m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(20, 30*60, self.air, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.air])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 32:43", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 40.092687746, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 14.4235632222, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.air.used_gas, 0.0, 7, "bad used gas (%s)" % self.air.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveCCAir20m40min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(20, 40*60, self.air, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.air])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 42:43", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 53.3291923291, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 19.1854679841, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.air.used_gas, 0.0, 7, "bad used gas (%s)" % self.air.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveCCAir20m50min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(20, 50*60, self.air, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.air])

  def runTest(self):
    self.profile1.do_dive()
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

# ===================================================== 30m tests ==============
class TestDiveCCAir30m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(30, 10*60, self.air, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.air])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 13:56", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 13.8022341567, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 4.96542906349, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.air.used_gas, 0.0, 7, "bad used gas (%s)" % self.air.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveCCAir30m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(30, 20*60, self.air, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.air])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 24:56", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 28.7193606516, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 10.3319467302, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.air.used_gas, 0.0, 7, "bad used gas (%s)" % self.air.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveCCAir30m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(30, 30*60, self.air, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.air])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 38:10", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 46.5926398368, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 16.7619564603, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.air.used_gas, 0.0, 7, "bad used gas (%s)" % self.air.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveCCAir30m40min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(30, 40*60, self.air, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.air])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 52:17", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 65.2781721399, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 23.4841786825, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.air.used_gas, 0.0, 7, "bad used gas (%s)" % self.air.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveCCAir30m50min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(30, 50*60, self.air, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.air])

  def runTest(self):
    self.profile1.do_dive()
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

# ===================================================== 40m tests ==============
class TestDiveCCAir40m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(40, 10*60, self.air, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.air])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 16:32", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 16.1728109878, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 5.81825701587, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.air.used_gas, 0.0, 7, "bad used gas (%s)" % self.air.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveCCAir40m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(40, 20*60, self.air, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.air])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 33:00", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 38.682864775, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 13.9163717143, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.air.used_gas, 0.0, 7, "bad used gas (%s)" % self.air.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveCCAir40m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(40, 30*60, self.air, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.air])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 52:23", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 64.6965942787, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 23.274952873, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.air.used_gas, 0.0, 7, "bad used gas (%s)" % self.air.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveCCAir40m40min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(40, 40*60, self.air, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.air])

  def runTest(self):
    self.profile1.do_dive()
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

# ===================================================== 50m tests ==============
class TestDiveCCAir50m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)

  def runTest(self):
    try:
      diveseg1 = SegmentDive(50, 10*60, self.air, self.setpoint)
      self.profile1 = Dive([diveseg1], [self.air])
      self.profile1.do_dive()
    except UnauthorizedMod:
      pass
    else:
      self.fail("should raise UnauthorizedMod")

# Diluant: Trimix Hypo =========================================================
# TxHypo 10/50 + tavel Tx21/30 + DECO Nx80 =====================================
# ===================================================== 50m tests ==============
class TestDiveCCHypo50m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 10*60, self.txhypo, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.txhypo])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 22:55", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 23.908170173, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 8.60109469841, 5, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

class TestDiveCCHypo50m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 20*60, self.txhypo, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.txhypo])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 49:52", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 60.2944929314, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 21.6912728889, 5, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

class TestDiveCCHypo50m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 30*60, self.txhypo, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.txhypo])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 80:55", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 101.393839662, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 36.4769871746, 5, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

class TestDiveCCHypo50m40min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 40*60, self.txhypo, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.txhypo])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "113:14", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 144.52678176, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 51.9942984921, 5, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

class TestDiveCCHypo50m50min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 50*60, self.txhypo, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.txhypo])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

# ===================================================== 60m tests ==============
class TestDiveCCHypo60m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(60, 10*60, self.txhypo, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.txhypo])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 29:50", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 31.9925048157, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 11.5094782063, 5, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

class TestDiveCCHypo60m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(60, 20*60, self.txhypo, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.txhypo])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 65:57", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 80.5122901086, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 28.9647357619, 5, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

class TestDiveCCHypo60m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(60, 30*60, self.txhypo, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.txhypo])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "107:43", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 136.153729037, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 48.9820470794, 5, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

class TestDiveCCHypo60m40min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(60, 40*60, self.txhypo, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.txhypo])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

# ===================================================== 70m tests ==============
class TestDiveCCHypo70m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(70, 10*60, self.txhypo, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.txhypo])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 37:16", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 41.1176969821, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 14.7923158889, 5, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

class TestDiveCCHypo70m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(70, 20*60, self.txhypo, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.txhypo])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 84:36", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 104.484428249, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 37.5888432857, 5, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

class TestDiveCCHypo70m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(70, 30*60, self.txhypo, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.txhypo])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

# ===================================================== 80m tests ==============
class TestDiveCCHypo80m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(80, 10*60, self.txhypo, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.txhypo])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 46:24", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 52.1361234741, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 18.7562549524, 5, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

class TestDiveCCHypo80m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(80, 20*60, self.txhypo, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.txhypo])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "107:46", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 134.078082839, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 48.2353220317, 5, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

class TestDiveCCHypo80m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(80, 30*60, self.txhypo, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.txhypo])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

# ===================================================== 90m tests ==============
class TestDiveCCHypo90m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(90, 10*60, self.txhypo, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.txhypo])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 56:33", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 64.5002612654, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 23.204321, 5, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

class TestDiveCCHypo90m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(90, 20*60, self.txhypo, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.txhypo])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "132:07", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 165.595028592, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 59.5737152698, 5, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5
                           , "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

class TestDiveCCHypo90m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(90, 30*60, self.txhypo, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.txhypo])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

# ===================================================== 100m tests ==============
class TestDiveCCHypo100m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(100, 10*60, self.txhypo, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.txhypo])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 68:28", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 79.2028481997, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 28.4936568889, 5, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

class TestDiveCCHypo100m15min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(100, 15*60, self.txhypo, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.txhypo])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "112:54", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 138.730993137, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 49.9092319048, 5, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 0.0, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

class TestDiveCCHypo100m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(100, 20*60, self.txhypo, self.setpoint)
    self.profile1 = Dive([diveseg1], [self.txhypo])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

# ===================================================== 110m tests ==============
class TestDiveCCHypo110m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)

  def runTest(self):
    try:
      diveseg1 = SegmentDive(110, 10*60, self.txhypo, self.setpoint)
      self.profile1 = Dive([diveseg1], [self.txhypo])
      self.profile1.do_dive()
    except UnauthorizedMod:
      pass
    else:
      self.fail("should raise UnauthorizedMod")

# ======================== Multilevel Dive =====================================
class TestDiveMultilevel(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(40, 10*60, self.air, self.setpoint)
    diveseg2 = SegmentDive(45, 12*60, self.air, self.setpoint)
    diveseg3 = SegmentDive(30, 15*60, self.air, self.setpoint)
    self.profile1 = Dive([diveseg1, diveseg2, diveseg3], [self.air])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 61:41", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 75.4001720001, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 27.125623373, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.air.used_gas, 0.0, 7, "bad used gas (%s)" % self.air.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())


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
