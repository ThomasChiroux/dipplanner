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
"""Test for Dive class

TODO: more test profiles
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
    settings.RUN_TIME = True
    settings.SURFACE_TEMP = 12
    self.air12l = Tank(tank_vol=12.0, tank_pressure=200, tank_rule="10b")
    self.airtank = Tank(tank_vol=18.0, tank_pressure=200, tank_rule="10b")
    self.airtank12 = Tank(tank_vol=12.0, tank_pressure=200, tank_rule="10b")
    self.airdouble = Tank(tank_vol=30.0, tank_pressure=200, tank_rule="10b") #bi15l 200b
    self.txtank1 = Tank(0.21, 0.30, tank_vol=20.0, tank_pressure=200, tank_rule="10b")
    self.txtanknormodbl = Tank(0.21, 0.30, tank_vol=30.0, tank_pressure=200, tank_rule="10b")
    self.deco1 = Tank(0.8, 0.0, tank_vol=7.0, tank_pressure=200, tank_rule="10b")
    self.deco2 = Tank(0.5, 0.0, tank_vol=7.0, tank_pressure=200, tank_rule="10b")
    self.decoo2 = Tank(1.0, 0.0, tank_vol=7.0, tank_pressure=200, tank_rule="10b")

# AIR + DECO Nx80 ==============================================================
# ===================================================== 10m tests ==============
class TestDiveAirDecoNx8010m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(10, 10*60, self.airtank12, 0)
    self.profile1 = Dive([diveseg1], [self.airtank12, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 11:00", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 0.133348222351, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 0.0722537642857, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank12.used_gas,339.7312725,7, "bad used gas (%s)" % self.airtank12.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

class TestDiveAirDecoNx8010m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(10, 20*60, self.airtank12, 0)
    self.profile1 = Dive([diveseg1], [self.airtank12, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 21:00", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 0.133348222351, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 0.0722537642857, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank12.used_gas,683.7568725,7, "bad used gas (%s)" % self.airtank12.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

class TestDiveAirDecoNx8010m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(10, 30*60, self.airtank12, 0)
    self.profile1 = Dive([diveseg1], [self.airtank12, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 30:43", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 0.124922571826, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 0.0690939087302, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank12.used_gas, 1027.7824725,7, "bad used gas (%s)" % self.airtank12.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

class TestDiveAirDecoNx8010m40min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(10, 40*60, self.airtank12, 0)
    self.profile1 = Dive([diveseg1], [self.airtank12, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 40:43", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 0.124922571826, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 0.0690939087302, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank12.used_gas, 1371.8080725,7, "bad used gas (%s)" % self.airtank12.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

class TestDiveAirDecoNx8010m50min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(10, 50*60, self.airtank12, 0)
    self.profile1 = Dive([diveseg1], [self.airtank12, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 50:43", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 0.124922571826, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 0.0690939087302, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank12.used_gas, 1715.8336725,7, "bad used gas (%s)" % self.airtank12.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

class TestDiveAirDecoNx8010m60min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(10, 60*60, self.airtank12, 0)
    self.profile1 = Dive([diveseg1], [self.airtank12, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 60:43", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 0.124922571826, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 0.0690939087302, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank12.used_gas, 2059.8592725,7, "bad used gas (%s)" % self.airtank12.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

class TestDiveAirDecoNx8010m70min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(10, 70*60, self.airtank12, 0)
    self.profile1 = Dive([diveseg1], [self.airtank12, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

# ===================================================== 20m tests ==============
class TestDiveAirDecoNx8020m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(20, 10*60, self.airtank12, 0)
    self.profile1 = Dive([diveseg1], [self.airtank12, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 11:43", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 3.12521319129, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 1.63334277057, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank12.used_gas, 544.96697445,7, "bad used gas (%s)" % self.airtank12.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

class TestDiveAirDecoNx8020m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(20, 20*60, self.airtank12, 0)
    self.profile1 = Dive([diveseg1], [self.airtank12, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 21:26", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 6.45363520992, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 3.38255328046, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank12.used_gas, 1060.76567445,7, "bad used gas (%s)" % self.airtank12.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

class TestDiveAirDecoNx8020m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(20, 30*60, self.airtank12, 0)
    self.profile1 = Dive([diveseg1], [self.airtank12, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 31:39", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 10.3115011634, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 5.35704886574, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank12.used_gas, 1576.56437445,7, "bad used gas (%s)" % self.airtank12.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

class TestDiveAirDecoNx8020m40min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(20, 40*60, self.airtank12, 0)
    self.profile1 = Dive([diveseg1], [self.airtank12, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 43:54", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 16.1374370923, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 8.07671260843, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank12.used_gas, 2092.36307445,7, "bad used gas (%s)" % self.airtank12.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

class TestDiveAirDecoNx8020m50min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(20, 50*60, self.airtank12, 0)
    self.profile1 = Dive([diveseg1], [self.airtank12, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

# ===================================================== 30m tests ==============
class TestDiveAirDecoNx8030m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(30, 10*60, self.airtank, 0)
    self.profile1 = Dive([diveseg1], [self.airtank, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 12:09", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 6.41250813694, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 2.46540515712, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank.used_gas, 755.43696195,7, "bad used gas (%s)" % self.airtank.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

class TestDiveAirDecoNx8030m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(30, 20*60, self.airtank, 0)
    self.profile1 = Dive([diveseg1], [self.airtank, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 24:53", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 17.5896679466, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 7.1968866386, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank.used_gas, 1432.8754875,7, "bad used gas (%s)" % self.airtank.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

class TestDiveAirDecoNx8030m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(30, 30*60, self.airtank, 0)
    self.profile1 = Dive([diveseg1], [self.airtank, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 39:40", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 31.114873529, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 13.8982755275, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank.used_gas, 2122.62843015,7, "bad used gas (%s)" % self.airtank.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

class TestDiveAirDecoNx8030m40min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(30, 40*60, self.airtank, 0)
    self.profile1 = Dive([diveseg1], [self.airtank, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 58:26", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 46.1785263942, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 21.2848496016, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank.used_gas, 2883.06333075,7, "bad used gas (%s)" % self.airtank.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

class TestDiveAirDecoNx8030m50min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(30, 50*60, self.airtank, 0)
    self.profile1 = Dive([diveseg1], [self.airtank, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

# ===================================================== 40m tests ==============
class TestDiveAirDecoNx8040m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(40, 10*60, self.airtank, 0)
    self.profile1 = Dive([diveseg1], [self.airtank, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 13:51", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 10.265888536, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 3.9480436367, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank.used_gas, 964.36233,7, "bad used gas (%s)" % self.airtank.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

class TestDiveAirDecoNx8040m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(40, 20*60, self.airtank, 0)
    self.profile1 = Dive([diveseg1], [self.airtank, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 31:53", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 29.4128909675, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 13.0202224006, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank.used_gas, 1867.0897404,7, "bad used gas (%s)" % self.airtank.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

class TestDiveAirDecoNx8040m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(40, 30*60, self.airtank, 0)
    self.profile1 = Dive([diveseg1], [self.airtank, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 54:47", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 52.0788841772, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 24.7539394357, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank.used_gas,2848.32768525,7, "bad used gas (%s)" % self.airtank.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

class TestDiveAirDecoNx8040m40min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(40, 40*60, self.airtank, 0)
    self.profile1 = Dive([diveseg1], [self.airtank, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

# ===================================================== 50m tests ==============
class TestDiveAirDecoNx8050m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 10*60, self.airdouble, 0)
    self.profile1 = Dive([diveseg1], [self.airdouble, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 16:34", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 14.2928607959, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 6.23483422365, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airdouble.used_gas, 1198.56090375,7, "bad used gas (%s)" % self.airdouble.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

class TestDiveAirDecoNx8050m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 20*60, self.airdouble, 0)
    self.profile1 = Dive([diveseg1], [self.airdouble, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 40:15", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 41.2208903422, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 19.4562696698, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airdouble.used_gas, 2360.3217561,7, "bad used gas (%s)" % self.airdouble.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

class TestDiveAirDecoNx8050m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 30*60, self.airdouble, 0)
    self.profile1 = Dive([diveseg1], [self.airdouble, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 73:52", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 74.7488883394, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 35.6454886355, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airdouble.used_gas, 3701.74971735,7, "bad used gas (%s)" % self.airdouble.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

class TestDiveAirDecoNx8050m40min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 40*60, self.airdouble, 0)
    self.profile1 = Dive([diveseg1], [self.airdouble, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "108:54", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 110.710292597, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 55.2035888533, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airdouble.used_gas, 5075.4846051, 7, "bad used gas (%s)" % self.airdouble.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

class TestDiveAirDecoNx8050m50min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 50*60, self.airdouble, 0)
    self.profile1 = Dive([diveseg1], [self.airdouble, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

# ===================================================== 60m tests ==============
class TestDiveAirDecoNx8060m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(60, 10*60, self.airdouble, 0)
    self.profile1 = Dive([diveseg1], [self.airdouble, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 19:20", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 17.479532223, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 8.78831638198, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airdouble.used_gas, 1457.4404298, 7, "bad used gas (%s)" % self.airdouble.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

class TestDiveAirDecoNx8060m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(60, 20*60, self.airdouble, 0)
    self.profile1 = Dive([diveseg1], [self.airdouble, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 51:17", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 54.7215266531, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 29.188571585, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airdouble.used_gas, 2900.7949014,7, "bad used gas (%s)" % self.airdouble.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

class TestDiveAirDecoNx8060m25min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(60, 25*60, self.airdouble, 0)
    self.profile1 = Dive([diveseg1], [self.airdouble, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 71:58", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 76.0469276722, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 39.7208677093, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airdouble.used_gas, 3725.75907465,7, "bad used gas (%s)" % self.airdouble.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

class TestDiveAirDecoNx8060m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(60, 30*60, self.airdouble, 0)
    self.profile1 = Dive([diveseg1], [self.airdouble, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 95:06", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 100.121095056, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 53.6790792102, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airdouble.used_gas, 4635.07279665,7, "bad used gas (%s)" % self.airdouble.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

class TestDiveAirDecoNx8060m40min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(60, 40*60, self.airdouble, 0)
    self.profile1 = Dive([diveseg1], [self.airdouble, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

# ===================================================== 70m tests ==============
class TestDiveAirDecoNx8070m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    
  def runTest(self):
    try:
      diveseg1 = SegmentDive(70, 10*60, self.airdouble, 0)
      self.profile1 = Dive([diveseg1], [self.airdouble, self.deco1])
      self.profile1.do_dive()
    except UnauthorizedMod:
      pass
    else:
      self.fail("should raise UnauthorizedMod")

# ==============================================================================
# ========================== M A I N ===========================================
# ==============================================================================
if __name__ == "__main__":
  import sys
  suite = unittest.findTestCases(sys.modules[__name__])
  #suite = unittest.TestLoader().loadTestsFromTestCase(TestDiveTxNormoDecoNx8040m60min)
  unittest.TextTestRunner(verbosity=2).run(suite)