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

class TestDive(unittest.TestCase):
  def setUp(self):
    # temporary hack (tests):
    dipplanner.activate_debug_for_tests()
    
    self.air12l = Tank(tank_vol=12.0, tank_pressure=200) 
    self.airtank = Tank(tank_vol=18.0, tank_pressure=200)
    self.airtank12 = Tank(tank_vol=12.0, tank_pressure=200)
    self.airdouble = Tank(tank_vol=30.0, tank_pressure=200) #bi15l 200b
    self.txtank1 = Tank(0.21, 0.30, tank_vol=20.0, tank_pressure=200)
    self.txtanknormodbl = Tank(0.21, 0.30, tank_vol=30.0, tank_pressure=200)
    self.deco1 = Tank(0.8, 0.0, tank_vol=7.0, tank_pressure=200)
    self.deco2 = Tank(0.5, 0.0, tank_vol=7.0, tank_pressure=200)
    self.decoo2 = Tank(1.0, 0.0, tank_vol=7.0, tank_pressure=200)

# TxNormo + DECO Nx80 ==========================================================
# ===================================================== 10m tests ==============
class TestDiveTxNormoDecoNx8010m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(10, 10*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 11:00", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 0.133342220445, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 0.0722537642857, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtanknormodbl.used_gas,339.7312725,7, "bad used gas (%s)" % self.txtanknormodbl.used_gas)

class TestDiveTxNormoDecoNx8010m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(10, 20*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 20:43", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 0.124917487765, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 0.0690939087302, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtanknormodbl.used_gas,683.7568725,7, "bad used gas (%s)" % self.txtanknormodbl.used_gas)
    
class TestDiveTxNormoDecoNx8010m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(10, 30*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 30:43", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 0.124917487765, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 0.0690939087302, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtanknormodbl.used_gas, 1027.7824725,7, "bad used gas (%s)" % self.txtanknormodbl.used_gas)

class TestDiveTxNormoDecoNx8010m40min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(10, 40*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 40:43", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 0.124917487765, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 0.0690939087302, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtanknormodbl.used_gas, 1371.8080725,7, "bad used gas (%s)" % self.txtanknormodbl.used_gas)

class TestDiveTxNormoDecoNx8010m50min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(10, 50*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 50:43", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 0.124917487765, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 0.0690939087302, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtanknormodbl.used_gas, 1715.8336725,7, "bad used gas (%s)" % self.txtanknormodbl.used_gas)

class TestDiveTxNormoDecoNx8010m60min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(10, 60*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 60:43", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 0.124917487765, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 0.0690939087302, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtanknormodbl.used_gas, 2059.8592725,7, "bad used gas (%s)" % self.txtanknormodbl.used_gas)

class TestDiveTxNormoDecoNx8010m180min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(10, 180*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    
  def runTest(self):
    try:
      self.profile1.do_dive()
    except EmptyTank:
      pass
    else:
      self.fail("should raise EmptyTank")

# ===================================================== 20m tests ==============
class TestDiveTxNormoDecoNx8020m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(20, 10*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 11:26", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 3.11092500521, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 1.62816731555, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtanknormodbl.used_gas, 544.96697445,7, "bad used gas (%s)" % self.txtanknormodbl.used_gas)

class TestDiveTxNormoDecoNx8020m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(20, 20*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 21:26", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 6.45324408084, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 3.38255328046, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtanknormodbl.used_gas, 1060.76567445,7, "bad used gas (%s)" % self.txtanknormodbl.used_gas)
    
class TestDiveTxNormoDecoNx8020m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(20, 30*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 32:23", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 11.0950786221, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 5.6626044213, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtanknormodbl.used_gas, 1576.56437445,7, "bad used gas (%s)" % self.txtanknormodbl.used_gas)

class TestDiveTxNormoDecoNx8020m40min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(20, 40*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 45:10", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 17.6518408278, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 8.66236075658, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtanknormodbl.used_gas, 2092.36307445,7, "bad used gas (%s)" % self.txtanknormodbl.used_gas)

class TestDiveTxNormoDecoNx8020m120min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(20, 120*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    
  def runTest(self):
    try:
      self.profile1.do_dive()
    except EmptyTank:
      pass
    else:
      self.fail("should raise EmptyTank")

# ===================================================== 30m tests ==============
class TestDiveTxNormoDecoNx8030m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(30, 10*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 12:09", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 6.41235066968, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 2.46540515712, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtanknormodbl.used_gas, 755.43696195,7, "bad used gas (%s)" % self.txtanknormodbl.used_gas)

class TestDiveTxNormoDecoNx8030m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(30, 20*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 25:34", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 18.422793213, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 7.8218866386, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtanknormodbl.used_gas, 1435.9915599,7, "bad used gas (%s)" % self.txtanknormodbl.used_gas)
    
class TestDiveTxNormoDecoNx8030m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(30, 30*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 41:21", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 32.693845554, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 14.6899421942, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtanknormodbl.used_gas, 2130.64118775,7, "bad used gas (%s)" % self.txtanknormodbl.used_gas)

class TestDiveTxNormoDecoNx8030m40min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(30, 40*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 60:05", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 47.7669540576, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 21.4862384904, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtanknormodbl.used_gas, 2893.60329135,7, "bad used gas (%s)" % self.txtanknormodbl.used_gas)

class TestDiveTxNormoDecoNx8030m90min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(30, 90*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    
  def runTest(self):
    try:
      self.profile1.do_dive()
    except EmptyTank:
      pass
    else:
      self.fail("should raise EmptyTank")

# ===================================================== 40m tests ==============
class TestDiveTxNormoDecoNx8040m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(40, 10*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 14:03", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 10.8609382055, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 4.20498808114, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtanknormodbl.used_gas, 952.74372345,7, "bad used gas (%s)" % self.txtanknormodbl.used_gas)

class TestDiveTxNormoDecoNx8040m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(40, 20*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 33:15", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 30.7979336163, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 14.0549446228, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtanknormodbl.used_gas, 1876.4761188,7, "bad used gas (%s)" % self.txtanknormodbl.used_gas)
    
class TestDiveTxNormoDecoNx8040m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(40, 30*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 56:11", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 53.5577009351, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 24.7932912875, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtanknormodbl.used_gas,2853.16205265,7, "bad used gas (%s)" % self.txtanknormodbl.used_gas)

class TestDiveTxNormoDecoNx8040m40min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(40, 40*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 82:40", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 78.123309661, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 37.0111275448, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtanknormodbl.used_gas,3921.45092145,7, "bad used gas (%s)" % self.txtanknormodbl.used_gas)

class TestDiveTxNormoDecoNx8040m50min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(40, 50*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "109:00", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 103.677805285, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 49.8728172895, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtanknormodbl.used_gas, 4933.7794242,7, "bad used gas (%s)" % self.txtanknormodbl.used_gas)

class TestDiveTxNormoDecoNx8040m60min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(40, 60*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    
  def runTest(self):
    try:
      self.profile1.do_dive()
    except EmptyTank:
      pass
    else:
      self.fail("should raise EmptyTank")

# ===================================================== 50m tests ==============
class TestDiveTxNormoDecoNx8050m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 10*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 16:39", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 14.9069609691, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 6.63108706161, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtanknormodbl.used_gas, 1183.5343281,7, "bad used gas (%s)" % self.txtanknormodbl.used_gas)

class TestDiveTxNormoDecoNx8050m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 20*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 42:41", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 43.1359081612, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 19.846157584, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtanknormodbl.used_gas, 2378.4085485,7, "bad used gas (%s)" % self.txtanknormodbl.used_gas)
    
class TestDiveTxNormoDecoNx8050m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 30*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 73:12", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 75.6645123303, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 36.6632030604, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtanknormodbl.used_gas, 3661.42772955,7, "bad used gas (%s)" % self.txtanknormodbl.used_gas)

class TestDiveTxNormoDecoNx8050m40min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 40*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "111:49", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 112.85352358, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 54.9651523782, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtanknormodbl.used_gas, 5112.52849815,7, "bad used gas (%s)" % self.txtanknormodbl.used_gas)

class TestDiveTxNormoDecoNx8050m50min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 50*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    
  def runTest(self):
    try:
      self.profile1.do_dive()
    except EmptyTank:
      pass
    else:
      self.fail("should raise EmptyTank")

# ===================================================== 60m tests ==============
class TestDiveTxNormoDecoNx8060m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(60, 10*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 19:14", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 18.3990058107, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 9.28893758666, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtanknormodbl.used_gas, 1414.3156506, 7, "bad used gas (%s)" % self.txtanknormodbl.used_gas)

class TestDiveTxNormoDecoNx8060m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(60, 20*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 52:28", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 56.0348851189, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 29.1319195382, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtanknormodbl.used_gas, 2903.7880302,7, "bad used gas (%s)" % self.txtanknormodbl.used_gas)
    
class TestDiveTxNormoDecoNx8060m25min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(60, 25*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 71:20", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 76.9880251814, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 40.755614298, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtanknormodbl.used_gas, 3686.87302545,7, "bad used gas (%s)" % self.txtanknormodbl.used_gas)

class TestDiveTxNormoDecoNx8060m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(60, 30*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 94:51", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 100.182056707, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 53.0097322317, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txtanknormodbl.used_gas, 4587.34384065,7, "bad used gas (%s)" % self.txtanknormodbl.used_gas)

class TestDiveTxNormoDecoNx8060m40min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(60, 40*60, self.txtanknormodbl, 0)
    self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
    
  def runTest(self):
    try:
      self.profile1.do_dive()
    except EmptyTank:
      pass
    else:
      self.fail("should raise EmptyTank")

# ===================================================== 70m tests ==============
class TestDiveTxNormoDecoNx8070m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    
  def runTest(self):
    try:
      diveseg1 = SegmentDive(70, 10*60, self.txtanknormodbl, 0)
      self.profile1 = Dive([diveseg1], [self.txtanknormodbl, self.deco1])
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