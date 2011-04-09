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
    self.airdouble = Tank(tank_vol=30.0, tank_pressure=200) #bi15l 200b
    self.txtank1 = Tank(0.21, 0.30, tank_vol=20.0, tank_pressure=200)
    self.deco1 = Tank(0.8, 0.0, tank_vol=7.0, tank_pressure=200)
    self.deco2 = Tank(0.5, 0.0, tank_vol=7.0, tank_pressure=200)
    self.decoo2 = Tank(1.0, 0.0, tank_vol=7.0, tank_pressure=200)

class TestDiveNotEnoughGas1(TestDive):
  def runTest(self):
    diveseg1 = SegmentDive(60, 30*60, self.air12l, 0)
    self.profile1 = Dive([diveseg1], [self.air12l])
    try:
      self.profile1.do_dive()
    except EmptyTank:
      pass
    else:
      self.fail("EmptyTank")

class TestDiveAirDiveOutput1(TestDive):
  def runTest(self):
    diveseg1 = SegmentDive(30, 30*60, self.airtank, 0)
    self.profile1 = Dive([diveseg1], [self.airtank])
    self.profile1.do_dive()
    assert str(self.profile1) == """Dive profile : GF:30.0-80.0
 DESCENT: at  30m for   1:30 [RT:  1:30], on Air,  SP:0.0, END:29m
   CONST: at  30m for  28:30 [RT: 30:00], on Air,  SP:0.0, END:29m
  ASCENT: at  15m for   1:30 [RT: 31:30], on Air,  SP:0.0, END:14m
    DECO: at  15m for   0:01 [RT: 31:31], on Air,  SP:0.0, END:14m
    DECO: at  12m for   0:32 [RT: 32:03], on Air,  SP:0.0, END:11m
    DECO: at   9m for   2:45 [RT: 34:48], on Air,  SP:0.0, END:8m
    DECO: at   6m for   5:03 [RT: 39:51], on Air,  SP:0.0, END:5m
    DECO: at   3m for   8:40 [RT: 48:31], on Air,  SP:0.0, END:2m
Gas:
  Air : used: 2421.1l (rem: 1178.9l or 65b)
Oxygen Toxicity: OTU:21, CNS:7%
""", "bad dive profile (%s)" % str(self.profile1)

class TestDiveAirDiveRunTime1(TestDive):
  def runTest(self):
    diveseg1 = SegmentDive(30, 30*60, self.airtank, 0)
    self.profile1 = Dive([diveseg1], [self.airtank])
    self.profile1.do_dive()
    assert seconds_to_strtime(self.profile1.run_time) == " 48:31", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

class TestDiveAirDiveOutput2(TestDive):
  def runTest(self):
    diveseg2 = SegmentDive(20, 30*60, self.airtank, 0)
    self.profile2 = Dive([diveseg2], [self.airtank])
    self.profile2.do_dive()
    assert str(self.profile2) == """Dive profile : GF:30.0-80.0
 DESCENT: at  20m for   1:00 [RT:  1:00], on Air,  SP:0.0, END:19m
   CONST: at  20m for  29:00 [RT: 30:00], on Air,  SP:0.0, END:19m
  ASCENT: at   9m for   1:06 [RT: 31:06], on Air,  SP:0.0, END:8m
    DECO: at   9m for   0:01 [RT: 31:07], on Air,  SP:0.0, END:8m
    DECO: at   6m for   0:01 [RT: 31:08], on Air,  SP:0.0, END:5m
    DECO: at   3m for   0:56 [RT: 32:04], on Air,  SP:0.0, END:2m
Gas:
  Air : used: 1592.0l (rem: 2008.0l or 111b)
Oxygen Toxicity: OTU:9, CNS:5%
""", "bad dive profile (%s)" % str(self.profile2)

class TestDiveAirDiveRunTime2(TestDive):
  def runTest(self):
    diveseg2 = SegmentDive(20, 30*60, self.airtank, 0)
    self.profile2 = Dive([diveseg2], [self.airtank])
    self.profile2.do_dive()
    assert seconds_to_strtime(self.profile2.run_time) == " 32:04", "bad dive runtime (%s)" % seconds_to_strtime(self.profile2.run_time)

class TestDiveAirDiveOutput3(TestDive):
  def runTest(self):
    diveseg3 = SegmentDive(55, 30*60, self.airdouble, 0)
    self.profile3 = Dive([diveseg3], [self.airdouble])
    self.profile3.do_dive()
    assert str(self.profile3) == """Dive profile : GF:30.0-80.0
 DESCENT: at  55m for   2:45 [RT:  2:45], on Air,  SP:0.0, END:54m
   CONST: at  55m for  27:15 [RT: 30:00], on Air,  SP:0.0, END:54m
  ASCENT: at  30m for   2:30 [RT: 32:30], on Air,  SP:0.0, END:29m
    DECO: at  30m for   0:02 [RT: 32:32], on Air,  SP:0.0, END:29m
    DECO: at  27m for   1:28 [RT: 34:00], on Air,  SP:0.0, END:26m
    DECO: at  24m for   1:33 [RT: 35:33], on Air,  SP:0.0, END:23m
    DECO: at  21m for   2:46 [RT: 38:19], on Air,  SP:0.0, END:20m
    DECO: at  18m for   3:23 [RT: 41:42], on Air,  SP:0.0, END:17m
    DECO: at  15m for   5:37 [RT: 47:19], on Air,  SP:0.0, END:14m
    DECO: at  12m for   6:41 [RT: 54:00], on Air,  SP:0.0, END:11m
    DECO: at   9m for  11:28 [RT: 65:28], on Air,  SP:0.0, END:8m
    DECO: at   6m for  21:59 [RT: 87:27], on Air,  SP:0.0, END:5m
    DECO: at   3m for  45:01 [RT:132:28], on Air,  SP:0.0, END:2m
Gas:
  Air : used: 5549.0l (rem: 451.0l or 15b)
Oxygen Toxicity: OTU:48, CNS:20%
""", "bad dive profile (%s)" % str(self.profile3)
    
class TestDiveAirDiveRunTime3(TestDive):
  def runTest(self):
    diveseg3 = SegmentDive(55, 30*60, self.airdouble, 0)
    self.profile3 = Dive([diveseg3], [self.airdouble])
    self.profile3.do_dive()
    assert seconds_to_strtime(self.profile3.run_time) == "132:28", "bad dive runtime (%s)" % seconds_to_strtime(self.profile3.run_time)
 
class TestDiveAirDiveOutput4(TestDive):
  def runTest(self):
    diveseg3 = SegmentDive(55, 30*60, self.airdouble, 0)
    self.profile3 = Dive([diveseg3], [self.airdouble,self.decoo2, self.deco2])
    self.profile3.do_dive()
    assert str(self.profile3) == """Dive profile : GF:30.0-80.0
 DESCENT: at  55m for   2:45 [RT:  2:45], on Air,  SP:0.0, END:54m
   CONST: at  55m for  27:15 [RT: 30:00], on Air,  SP:0.0, END:54m
  ASCENT: at  30m for   2:30 [RT: 32:30], on Air,  SP:0.0, END:29m
    DECO: at  30m for   0:02 [RT: 32:32], on Air,  SP:0.0, END:29m
    DECO: at  27m for   1:28 [RT: 34:00], on Air,  SP:0.0, END:26m
    DECO: at  24m for   1:33 [RT: 35:33], on Air,  SP:0.0, END:23m
    DECO: at  21m for   1:42 [RT: 37:15], on Nitrox 50,  SP:0.0, END:20m
    DECO: at  18m for   2:08 [RT: 39:23], on Nitrox 50,  SP:0.0, END:17m
    DECO: at  15m for   3:05 [RT: 42:28], on Nitrox 50,  SP:0.0, END:14m
    DECO: at  12m for   4:17 [RT: 46:45], on Nitrox 50,  SP:0.0, END:11m
    DECO: at   9m for   5:53 [RT: 52:38], on Nitrox 50,  SP:0.0, END:8m
    DECO: at   6m for   6:42 [RT: 59:20], on Oxygen,  SP:0.0, END:5m
    DECO: at   3m for  11:29 [RT: 70:49], on Oxygen,  SP:0.0, END:2m
Gas:
  Oxygen : used: 311.6l (rem: 1088.4l or 155b)
  Nitrox 50 : used: 480.2l (rem: 919.8l or 131b)
  Air : used: 3578.1l (rem: 2421.9l or 80b)
Oxygen Toxicity: OTU:97, CNS:93%
""", "bad dive profile (%s)" % str(self.profile3)

class TestDiveAirDiveRunTime4(TestDive):
  def runTest(self):
    diveseg3 = SegmentDive(55, 30*60, self.airdouble, 0)
    self.profile3 = Dive([diveseg3], [self.airdouble, self.deco2, self.decoo2 ])
    self.profile3.do_dive()
    assert seconds_to_strtime(self.profile3.run_time) == " 70:49", "bad dive runtime (%s)" % seconds_to_strtime(self.profile3.run_time)

class TestDiveTxDiveOutput1(TestDive):
  def runTest(self):
    diveseg1 = SegmentDive(30, 30*60, self.txtank1, 0)
    self.profile1 = Dive([diveseg1], [self.txtank1])
    self.profile1.do_dive()
    assert str(self.profile1) == """Dive profile : GF:30.0-80.0
 DESCENT: at  30m for   1:30 [RT:  1:30], on Trimix 21/30,  SP:0.0, END:20m
   CONST: at  30m for  28:30 [RT: 30:00], on Trimix 21/30,  SP:0.0, END:20m
  ASCENT: at  15m for   1:30 [RT: 31:30], on Trimix 21/30,  SP:0.0, END:8m
    DECO: at  15m for   0:01 [RT: 31:31], on Trimix 21/30,  SP:0.0, END:8m
    DECO: at  12m for   0:50 [RT: 32:21], on Trimix 21/30,  SP:0.0, END:6m
    DECO: at   9m for   3:10 [RT: 35:31], on Trimix 21/30,  SP:0.0, END:4m
    DECO: at   6m for   5:20 [RT: 40:51], on Trimix 21/30,  SP:0.0, END:2m
    DECO: at   3m for  14:20 [RT: 55:11], on Trimix 21/30,  SP:0.0, END:0m
Gas:
  Trimix 21/30 : used: 2533.8l (rem: 1466.2l or 73b)
Oxygen Toxicity: OTU:21, CNS:7%
""", "bad dive profile (%s)" % str(self.profile1)

class TestDiveTxDiveRunTime1(TestDive):
  def runTest(self):
    diveseg1 = SegmentDive(30, 30*60, self.txtank1, 0)
    self.profile1 = Dive([diveseg1], [self.txtank1])
    self.profile1.do_dive()
    assert seconds_to_strtime(self.profile1.run_time) == " 55:11", "bad dive runtime (%s)" % seconds_to_strtime(self.profile1.run_time)
  
class TestDiveCCRDiveOutput1(TestDive):
  def runTest(self):
    diveseg1 = SegmentDive(65, 30*60, self.txtank1, 1.4)
    self.profile1 = Dive([diveseg1], [self.txtank1, self.decoo2])
    self.profile1.do_dive()
    assert str(self.profile1) == """Dive profile : GF:30.0-80.0
 DESCENT: at  65m for   3:15 [RT:  3:15], on Trimix 21/30,  SP:1.4, END:46m
   CONST: at  65m for  26:45 [RT: 30:00], on Trimix 21/30,  SP:1.4, END:46m
  ASCENT: at  39m for   2:36 [RT: 32:36], on Trimix 21/30,  SP:1.4, END:28m
    DECO: at  39m for   0:01 [RT: 32:37], on Trimix 21/30,  SP:1.4, END:28m
    DECO: at  36m for   0:14 [RT: 32:51], on Trimix 21/30,  SP:1.4, END:26m
    DECO: at  33m for   0:55 [RT: 33:46], on Trimix 21/30,  SP:1.4, END:23m
    DECO: at  30m for   1:08 [RT: 34:54], on Trimix 21/30,  SP:1.4, END:21m
    DECO: at  27m for   1:26 [RT: 36:20], on Trimix 21/30,  SP:1.4, END:19m
    DECO: at  24m for   2:00 [RT: 38:20], on Trimix 21/30,  SP:1.4, END:17m
    DECO: at  21m for   2:06 [RT: 40:26], on Trimix 21/30,  SP:1.4, END:15m
    DECO: at  18m for   2:44 [RT: 43:10], on Trimix 21/30,  SP:1.4, END:13m
    DECO: at  15m for   3:30 [RT: 46:40], on Trimix 21/30,  SP:1.4, END:11m
    DECO: at  12m for   5:13 [RT: 51:53], on Trimix 21/30,  SP:1.4, END:9m
    DECO: at   9m for   6:53 [RT: 58:46], on Trimix 21/30,  SP:1.4, END:7m
    DECO: at   6m for   8:49 [RT: 67:35], on Oxygen,  SP:0.0, END:5m
    DECO: at   3m for  16:07 [RT: 83:42], on Oxygen,  SP:0.0, END:2m
Gas:
  Oxygen : used: 425.9l (rem: 974.1l or 139b)
  Trimix 21/30 : used: 0.0l (rem: 4000.0l or 200b)
Oxygen Toxicity: OTU:128, CNS:119%
""", "bad dive profile (%s)" % str(self.profile1)

class TestDiveCCRDiveRunTime1(TestDive):
  def runTest(self):
    diveseg1 = SegmentDive(65, 30*60, self.txtank1, 1.4)
    self.profile1 = Dive([diveseg1], [self.txtank1, self.decoo2])
    self.profile1.do_dive()
    assert seconds_to_strtime(self.profile1.run_time) == " 83:42", "bad dive runtime (%s)" % seconds_to_strtime(self.profile1.run_time)    

if __name__ == "__main__":
  import sys
  suite = unittest.findTestCases(sys.modules[__name__])
  #suite = unittest.TestLoader().loadTestsFromTestCase(Test)
  unittest.TextTestRunner(verbosity=2).run(suite)