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
"""Test Dives in hypoxic trimix
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
    
    self.txhypo = Tank(0.10, 0.50, tank_vol=30.0, tank_pressure=200) # 2x 15l
    self.txtravel = Tank(0.21, 0.30, tank_vol=24.0, tank_pressure=200) # 2x S80
    self.deco1 = Tank(0.8, 0.0, tank_vol=7.0, tank_pressure=200) # 1x S80

    self.divesegdesc1 = SegmentDive(40, 130, self.txtravel, 0)
    self.divesegdesc2 = SegmentDive(40, 30, self.txhypo, 0)

    settings.RUN_TIME = False
    settings.SURFACE_TEMP = 12

# TxHypo 10/50 + tavel Tx21/30 + DECO Nx80 ==========================================================
# ===================================================== 50m tests ==============
class TestDiveTxHypo50m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 10*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 26:14", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 14, 0, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 8, 0, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 1063.50427732, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo50m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 20*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 61:08", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 39, 0, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 23, 0, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 2094.62227732, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo50m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 30*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "102:53", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 68.0295132426, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 40, 0, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 3125.74027732, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo50m40min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 40*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "149:55", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 101.815314233, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 58, 0, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 4156.85827732, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo50m50min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 50*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank2_cons(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

# ===================================================== 60m tests ==============
class TestDiveTxHypo60m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(60, 10*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 33:41", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 21, 0, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 12, 0, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 1291.12760482, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo60m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(60, 20*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 80:02", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 57.8118417238, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 32, 0, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 2494.01870482, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo60m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(60, 30*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "134:23", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 100.371610949, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 56, 0, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 3696.90980482, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo60m40min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(60, 40*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank2_cons(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

# ===================================================== 70m tests ==============
class TestDiveTxHypo70m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(70, 10*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 42:32", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 30, 0, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 16, 0, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 1580.95197052, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo70m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(70, 20*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "100:20", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 78.0718874012, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 42.1878191995, 5, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 2955.61617052, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo70m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(70, 30*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank2_cons(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

# ===================================================== 80m tests ==============
class TestDiveTxHypo80m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(80, 10*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 51:32", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 39.4094522127, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 21, 0, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 1971.80768302, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo80m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(80, 20*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "124:26", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 102.280475116, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 55, 0, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 3518.24498302, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo80m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(80, 30*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank2_cons(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

# ===================================================== 90m tests ==============
class TestDiveTxHypo90m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(90, 10*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 61:09", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 49.1755177697, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 27, 0, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 2388.42936052, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo90m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(90, 20*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "152:01", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 129, 0, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 68, 0, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 4106.63976052, 5
                           , "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo90m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(90, 30*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank2_cons(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

# ===================================================== 100m tests ==============
class TestDiveTxHypo100m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(100, 10*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 73:30", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 60.4524801246, 3, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 32, 0, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 2830.81700302, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo100m15min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(100, 15*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "124:32", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 107, 0, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 57, 0, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 3775.80875302, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo100m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(100, 20*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank2_cons(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

# ===================================================== 110m tests ==============
class TestDiveTxHypo110m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(110, 10*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 86:21", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 73.241462871, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 39.1087296053, 5, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 3298.97061052, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo110m15min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(110, 15*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "145:21", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 126.87346546, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 68.251712302, 5, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 4291.49432617, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo110m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(110, 20*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank2_cons(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

# ===================================================== 120m tests ==============
class TestDiveTxHypo120m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(120, 10*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "100:31", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 86.2732515846, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 46.7889044386, 5, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 3754.53559867, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo120m15min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(120, 15*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank2_cons(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

# ===================================================== 130m tests ==============
class TestDiveTxHypo130m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(130, 10*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "116:48", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 101.656064471, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 57.5362260386, 5, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 4220.50883797, 1, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo130m15min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(130, 15*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank2_cons(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

# ===================================================== 140m tests ==============
class TestDiveTxHypo140m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(140, 10*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "133:59", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 117.916971495, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 80.3514857815, 5, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 4743.92732647, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo140m15min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(140, 15*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank2_cons(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

# ===================================================== 150m tests ==============
class TestDiveTxHypo150m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(150, 10*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "155:22", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 136.569733158, 5, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 150.180109686, 5, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 5302.77543877, 5, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo150m15min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(150, 15*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank2_cons(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

# ===================================================== 160m tests ==============
class TestDiveTxHypo160m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    
  def runTest(self):
    try:
      diveseg1 = SegmentDive(160, 10*60, self.txhypo, 0)
      self.profile1 = Dive([diveseg1], [self.txtravel, self.txhypo, self.deco1])
      self.profile1.do_dive()
    except UnauthorizedMod:
      pass
    else:
      self.fail("should raise UnauthorizedMod")

# ======================== Multilevel Dive =====================================
class TestDiveMultilevel(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(40, 10*60, self.txhypo, 0)
    diveseg2 = SegmentDive(50, 12*60, self.txhypo, 0)
    diveseg3 = SegmentDive(30, 15*60, self.txhypo, 0)
    self.profile1 = Dive([diveseg1, diveseg2, diveseg3], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()

  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 94:53", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 51.8821773186, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 31.7351499042, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))

  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 3347.1747525, 7, "bad used gas (%s)" % self.txhypo.used_gas)

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
