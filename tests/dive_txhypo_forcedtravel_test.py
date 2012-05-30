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
"""Test Dives in hypoxic trimix with forced travel
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
    self.txhypo = Tank(0.10, 0.50, tank_vol=30.0, tank_pressure=200) # 2x 15l
    self.txtravel = Tank(0.21, 0.30, tank_vol=24.0, tank_pressure=200) # 2x S80
    self.deco1 = Tank(0.8, 0.0, tank_vol=7.0, tank_pressure=200) # 1x S80

    self.divesegdesc1 = SegmentDive(40, 130, self.txtravel, 0)
    self.divesegdesc2 = SegmentDive(40, 30, self.txhypo, 0)

# TxHypo 10/50 + tavel Tx21/30 + DECO Nx80 ==========================================================
# ===================================================== 50m tests ==============
class TestDiveTxHypo50m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 10*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 27:58", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 15.0326465145, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 9.20139047151, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 1121.3468175,7, "bad used gas (%s)" % self.txhypo.used_gas)

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
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 63:38", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 40.2902572112, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 23.7043006309, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 2152.4648175,7, "bad used gas (%s)" % self.txhypo.used_gas)

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
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "105:17", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 69.6410027444, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 40.718614299, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 3183.5828175,7, "bad used gas (%s)" % self.txhypo.used_gas)

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
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "152:37", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 103.647781047, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 59.5453930514, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 4214.7008175,7, "bad used gas (%s)" % self.txhypo.used_gas)

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
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
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
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 35:47", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 22.5686007514, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 12.1797092833, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 1348.970145,7, "bad used gas (%s)" % self.txhypo.used_gas)

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
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 82:43", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 59.8083784813, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 33.3744051783, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 2551.861245,7, "bad used gas (%s)" % self.txhypo.used_gas)

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
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "137:34", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 102.507843629, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 56.4722280197, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 3754.752345,7, "bad used gas (%s)" % self.txhypo.used_gas)

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
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
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
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 43:57", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 31.1873696139, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 16.8476293459, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 1638.7945107,7, "bad used gas (%s)" % self.txhypo.used_gas)

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
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "102:59", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 79.8972700862, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 43.3741356852, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 3013.4587107,7, "bad used gas (%s)" % self.txhypo.used_gas)

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
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank2_cons(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

# ===================================================== 80m tests ==============
class TestDiveTxHypo80m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(80, 10*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 53:56", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 41.1397659391, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 22.0934219245, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 2029.6502232,7, "bad used gas (%s)" % self.txhypo.used_gas)

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
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "127:15", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 104.352474663, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 56.0310063593, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 3576.0875232,7, "bad used gas (%s)" % self.txhypo.used_gas)

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
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
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
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 64:03", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 51.0449996913, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 27.4008465832, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 2446.2719007,7, "bad used gas (%s)" % self.txhypo.used_gas)

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
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "155:17", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 130.901514995, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 69.4711018978, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 4164.4823007,7, "bad used gas (%s)" % self.txhypo.used_gas)

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
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
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
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 76:16", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 62.4790304007, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 33.3560324952, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 2888.6595432,7, "bad used gas (%s)" % self.txhypo.used_gas)

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
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "127:36", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 109.111103713, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 58.2845276628, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 3833.6512932, 7, "bad used gas (%s)" % self.txhypo.used_gas)

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
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
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
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 89:25", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 75.6607077013, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 40.4957929747, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 3356.8131507,7, "bad used gas (%s)" % self.txhypo.used_gas)

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
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "148:59", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 129.556834855, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 70.1371431178, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 4349.33686635, 7, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo110m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(110, 20*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
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
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "103:44", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 88.5951345808, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 48.3932648932, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 3812.37813885, 7, "bad used gas (%s)" % self.txhypo.used_gas)

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
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
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
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "120:22", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 104.437763541, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 59.3678943461, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 4281.66671655, 7, "bad used gas (%s)" % self.txhypo.used_gas)

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
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
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
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "138:05", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 121.019444884, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 81.879812958, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 4810.24009005, 7, "bad used gas (%s)" % self.txhypo.used_gas)

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
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank2_cons(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

# ===================================================== 150m tests ==============
class TestDiveTxHypo150m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(150, 10*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "159:33", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 139.724774818, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 152.192006899, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 5369.87633775, 7, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo150m15min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(150, 15*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
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
      self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
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
