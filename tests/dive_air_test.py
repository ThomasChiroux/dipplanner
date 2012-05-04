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

# ==============================================================================
# ======= S Y S T E M A T I C        T E S T S =================================
# ==============================================================================

# AIR ==========================================================================
# ===================================================== 10m tests ==============
class TestDiveAir10m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(10, 10*60, self.airtank12, 0)
    self.profile1 = Dive([diveseg1], [self.airtank12])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 11:00", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    assert self.profile1.model.ox_tox.otu == 0.0, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu

  def test_CNS(self):
    assert (self.profile1.model.ox_tox.cns * 100) == 0.0, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100)
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank12.used_gas,365.5451775,7, "bad used gas (%s)" % self.airtank12.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveAir10m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(10, 20*60, self.airtank12, 0)
    self.profile1 = Dive([diveseg1], [self.airtank12])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 21:00", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    assert self.profile1.model.ox_tox.otu == 0.0, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu

  def test_CNS(self):
    assert (self.profile1.model.ox_tox.cns * 100) == 0.0, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100)
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank12.used_gas,709.5707775,7, "bad used gas (%s)" % self.airtank12.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveAir10m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(10, 30*60, self.airtank12, 0)
    self.profile1 = Dive([diveseg1], [self.airtank12])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 30:43", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    assert self.profile1.model.ox_tox.otu == 0.0, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu

  def test_CNS(self):
    assert (self.profile1.model.ox_tox.cns * 100) == 0.0, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100)
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank12.used_gas,1047.91909935,7, "bad used gas (%s)" % self.airtank12.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveAir10m40min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(10, 40*60, self.airtank12, 0)
    self.profile1 = Dive([diveseg1], [self.airtank12])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 40:43", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    assert self.profile1.model.ox_tox.otu == 0.0, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu

  def test_CNS(self):
    assert (self.profile1.model.ox_tox.cns * 100) == 0.0, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100)
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank12.used_gas,1391.94469935,7, "bad used gas (%s)" % self.airtank12.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveAir10m50min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(10, 50*60, self.airtank12, 0)
    self.profile1 = Dive([diveseg1], [self.airtank12])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 50:43", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    assert self.profile1.model.ox_tox.otu == 0.0, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu

  def test_CNS(self):
    assert (self.profile1.model.ox_tox.cns * 100) == 0.0, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100)
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank12.used_gas,1735.97029935,7, "bad used gas (%s)" % self.airtank12.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveAir10m60min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(10, 60*60, self.airtank12, 0)
    self.profile1 = Dive([diveseg1], [self.airtank12])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 60:43", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    assert self.profile1.model.ox_tox.otu == 0.0, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu

  def test_CNS(self):
    assert (self.profile1.model.ox_tox.cns * 100) == 0.0, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100)
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank12.used_gas,2079.99589935,7, "bad used gas (%s)" % self.airtank12.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveAir10m70min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(10, 70*60, self.airtank12, 0)
    self.profile1 = Dive([diveseg1], [self.airtank12])
    
  def runTest(self):
    self.profile1.do_dive()
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())
    #except EmptyTank:
    #  pass
    #else:
    #  self.fail("should raise EmptyTank")

# ===================================================== 20m tests ==============
class TestDiveAir20m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(20, 10*60, self.airtank12, 0)
    self.profile1 = Dive([diveseg1], [self.airtank12])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 11:43", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 3.01929957641, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 1.58670286184, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank12.used_gas,561.74923185,7, "bad used gas (%s)" % self.airtank12.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveAir20m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(20, 20*60, self.airtank12, 0)
    self.profile1 = Dive([diveseg1], [self.airtank12])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 21:26", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 6.36182197227, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 3.34108882675, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank12.used_gas,1070.3853216,7, "bad used gas (%s)" % self.airtank12.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveAir20m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(20, 30*60, self.airtank12, 0)
    self.profile1 = Dive([diveseg1], [self.airtank12])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 32:04", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 9.70434436813, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 5.09547479167, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank12.used_gas,1592.01624825,7, "bad used gas (%s)" % self.airtank12.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveAir20m40min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(20, 40*60, self.airtank12, 0)
    self.profile1 = Dive([diveseg1], [self.airtank12])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 46:23", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 13.046866764, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 6.84986075658, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank12.used_gas,2177.57965125,7, "bad used gas (%s)" % self.airtank12.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveAir20m50min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(20, 50*60, self.airtank12, 0)
    self.profile1 = Dive([diveseg1], [self.airtank12])
    
  def runTest(self):
    self.profile1.do_dive()
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

# ===================================================== 30m tests ==============
class TestDiveAir30m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(30, 10*60, self.airtank, 0)
    self.profile1 = Dive([diveseg1], [self.airtank])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 12:09", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 6.34006508471, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 2.41216441637, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank.used_gas,756.40866675,7, "bad used gas (%s)" % self.airtank.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveAir30m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(30, 20*60, self.airtank, 0)
    self.profile1 = Dive([diveseg1], [self.airtank])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 27:25", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 13.7054851702, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 5.18994219415, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank.used_gas,1531.9456713,7, "bad used gas (%s)" % self.airtank.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveAir30m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(30, 30*60, self.airtank, 0)
    self.profile1 = Dive([diveseg1], [self.airtank])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 48:31", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 21.0724203812, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 7.97003478674, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank.used_gas,2421.12105195,7, "bad used gas (%s)" % self.airtank.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveAir30m40min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(30, 40*60, self.airtank, 0)
    self.profile1 = Dive([diveseg1], [self.airtank])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 76:57", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 28.4454160942, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 10.7593866386, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank.used_gas, 3459.83480295, 7, "bad used gas (%s)" % self.airtank.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveAir30m50min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(30, 50*60, self.airtank, 0)
    self.profile1 = Dive([diveseg1], [self.airtank])
    
  def runTest(self):
    self.profile1.do_dive()
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

# ===================================================== 40m tests ==============
class TestDiveAir40m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(40, 10*60, self.airtank, 0)
    self.profile1 = Dive([diveseg1], [self.airtank])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 14:26", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 9.0003053587, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 3.43415474781, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank.used_gas,992.3251146,7, "bad used gas (%s)" % self.airtank.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveAir40m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(40, 20*60, self.airtank, 0)
    self.profile1 = Dive([diveseg1], [self.airtank])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 38:43", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 20.0351251468, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 7.70309277096, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank.used_gas,2119.5450978,7, "bad used gas (%s)" % self.airtank.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveAir40m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(40, 30*60, self.airtank, 0)
    self.profile1 = Dive([diveseg1], [self.airtank])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 76:44", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 31.4242483674, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 12.2400505468, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airtank.used_gas, 3523.92514605, 7, "bad used gas (%s)" % self.airtank.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveAir40m40min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(40, 40*60, self.airtank, 0)
    self.profile1 = Dive([diveseg1], [self.airtank])
    
  def runTest(self):
    self.profile1.do_dive()
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

# ===================================================== 50m tests ==============
class TestDiveAir50m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 10*60, self.airdouble, 0)
    self.profile1 = Dive([diveseg1], [self.airdouble])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 18:10", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 11.1917458411, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 4.3528897792, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airdouble.used_gas,1270.31441415,7, "bad used gas (%s)" % self.airdouble.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveAir50m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 20*60, self.airdouble, 0)
    self.profile1 = Dive([diveseg1], [self.airdouble])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 55:41", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 26.2373916846, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 10.4331215217, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airdouble.used_gas,2837.7423801,7, "bad used gas (%s)" % self.airdouble.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveAir50m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 30*60, self.airdouble, 0)
    self.profile1 = Dive([diveseg1], [self.airdouble])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "111:56", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 42.2974492671, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 17.013544191, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airdouble.used_gas,4825.77776295,7, "bad used gas (%s)" % self.airdouble.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveAir50m40min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 40*60, self.airdouble, 0)
    self.profile1 = Dive([diveseg1], [self.airdouble])
    
  def runTest(self):
    self.profile1.do_dive()
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

# ===================================================== 60m tests ==============
class TestDiveAir60m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(60, 10*60, self.airdouble, 0)
    self.profile1 = Dive([diveseg1], [self.airdouble])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 22:08", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 13.1287274067, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 6.24896453013, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airdouble.used_gas, 1567.2773808, 7, "bad used gas (%s)" % self.airdouble.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveAir60m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(60, 20*60, self.airdouble, 0)
    self.profile1 = Dive([diveseg1], [self.airdouble])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 74:35", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 32.5133828231, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 15.6191271406, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airdouble.used_gas, 3620.591772,7, "bad used gas (%s)" % self.airdouble.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveAir60m25min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(60, 25*60, self.airdouble, 0)
    self.profile1 = Dive([diveseg1], [self.airdouble])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "110:47", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 42.7649344711, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 20.5657751167, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.airdouble.used_gas,4873.55826465,7, "bad used gas (%s)" % self.airdouble.used_gas)

  def test_tank_cons_rule(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

class TestDiveAir60m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(60, 30*60, self.airdouble, 0)
    self.profile1 = Dive([diveseg1], [self.airdouble])
    
  def runTest(self):
    self.profile1.do_dive()
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s)' % self.profile1.tanks[0].check_rule())

# ===================================================== 70m tests ==============
class TestDiveAir70m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    
  def runTest(self):
    try:
      diveseg1 = SegmentDive(70, 10*60, self.airdouble, 0)
      self.profile1 = Dive([diveseg1], [self.airdouble])
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