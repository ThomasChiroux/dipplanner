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

TODO: beaucoup de cas de tests de profils
"""

__version__ = "0.1"

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

class Test(unittest.TestCase):
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
    
  def test_not_enough_gas(self):
    diveseg1 = SegmentDive(60, 30*60, self.air12l, 0)
    self.profile1 = Dive([diveseg1], [self.air12l])
    try:
      self.profile1.do_dive()
    except EmptyTank:
      pass
    else:
      self.fail("EmptyTank")

  def test_air_dive1_complete_profile(self):
    diveseg1 = SegmentDive(30, 30*60, self.airtank, 0)
    self.profile1 = Dive([diveseg1], [self.airtank])
    self.profile1.do_dive()
    assert str(self.profile1) == """Dive profile : GF:30.0-80.0
 DESCENT: at  30m for   1:30 [RT:  1:30], on Air,  SP:0.0, END:29m
   CONST: at  30m for  28:30 [RT: 30:00], on Air,  SP:0.0, END:29m
  ASCENT: at  15m for   1:30 [RT: 31:30], on Air,  SP:0.0, END:14m
    DECO: at  15m for   0:01 [RT: 31:31], on Air,  SP:0.0, END:14m
    DECO: at  12m for   0:19 [RT: 31:50], on Air,  SP:0.0, END:11m
    DECO: at   9m for   2:36 [RT: 34:26], on Air,  SP:0.0, END:8m
    DECO: at   6m for   4:51 [RT: 39:17], on Air,  SP:0.0, END:5m
    DECO: at   3m for   8:24 [RT: 47:41], on Air,  SP:0.0, END:2m
Gas:
  Air : used: 2386.4l (rem: 1213.6l or 67b)
Oxygen Toxicity: OTU:20, CNS:7%
""", "bad dive profile (%s)" % str(self.profile1)

  def test_air_dive1_run_time(self):
    diveseg1 = SegmentDive(30, 30*60, self.airtank, 0)
    self.profile1 = Dive([diveseg1], [self.airtank])
    self.profile1.do_dive()
    assert seconds_to_strtime(self.profile1.run_time) == " 47:41", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)

  def test_air_dive2(self):
    diveseg2 = SegmentDive(20, 30*60, self.airtank, 0)
    self.profile2 = Dive([diveseg2], [self.airtank])
    self.profile2.do_dive()
    assert str(self.profile2) == """Dive profile : GF:30.0-80.0
 DESCENT: at  20m for   1:00 [RT:  1:00], on Air,  SP:0.0, END:19m
   CONST: at  20m for  29:00 [RT: 30:00], on Air,  SP:0.0, END:19m
  ASCENT: at   9m for   1:06 [RT: 31:06], on Air,  SP:0.0, END:8m
    DECO: at   9m for   0:01 [RT: 31:07], on Air,  SP:0.0, END:8m
    DECO: at   6m for   0:01 [RT: 31:08], on Air,  SP:0.0, END:5m
    DECO: at   3m for   0:42 [RT: 31:50], on Air,  SP:0.0, END:2m
Gas:
  Air : used: 1577.4l (rem: 2022.6l or 112b)
Oxygen Toxicity: OTU:9, CNS:5%
""", "bad dive profile (%s)" % str(self.profile2)

  def test_air_dive2_runtime(self):
    diveseg2 = SegmentDive(20, 30*60, self.airtank, 0)
    self.profile2 = Dive([diveseg2], [self.airtank])
    self.profile2.do_dive()
    assert seconds_to_strtime(self.profile2.run_time) == " 31:50", "bad dive runtime (%s)" % seconds_to_strtime(self.profile2.run_time)

  def test_air_dive3(self):
    diveseg3 = SegmentDive(55, 30*60, self.airdouble, 0)
    self.profile3 = Dive([diveseg3], [self.airdouble])
    self.profile3.do_dive()
    assert str(self.profile3) == """Dive profile : GF:30.0-80.0
 DESCENT: at  55m for   2:45 [RT:  2:45], on Air,  SP:0.0, END:53m
   CONST: at  55m for  27:15 [RT: 30:00], on Air,  SP:0.0, END:53m
  ASCENT: at  30m for   2:30 [RT: 32:30], on Air,  SP:0.0, END:29m
    DECO: at  30m for   0:01 [RT: 32:31], on Air,  SP:0.0, END:29m
    DECO: at  27m for   1:12 [RT: 33:43], on Air,  SP:0.0, END:26m
    DECO: at  24m for   1:32 [RT: 35:15], on Air,  SP:0.0, END:23m
    DECO: at  21m for   2:33 [RT: 37:48], on Air,  SP:0.0, END:20m
    DECO: at  18m for   3:21 [RT: 41:09], on Air,  SP:0.0, END:17m
    DECO: at  15m for   5:18 [RT: 46:27], on Air,  SP:0.0, END:14m
    DECO: at  12m for   6:38 [RT: 53:05], on Air,  SP:0.0, END:11m
    DECO: at   9m for  10:46 [RT: 63:51], on Air,  SP:0.0, END:8m
    DECO: at   6m for  20:44 [RT: 84:35], on Air,  SP:0.0, END:5m
    DECO: at   3m for  43:46 [RT:128:21], on Air,  SP:0.0, END:2m
Gas:
  Air : used: 5416.2l (rem: 583.8l or 19b)
Oxygen Toxicity: OTU:47, CNS:20%
""", "bad dive profile (%s)" % str(self.profile3)
    
  def test_air_dive3_run_time(self):
    diveseg3 = SegmentDive(55, 30*60, self.airdouble, 0)
    self.profile3 = Dive([diveseg3], [self.airdouble])
    self.profile3.do_dive()
    assert seconds_to_strtime(self.profile3.run_time) == "128:21", "bad dive runtime (%s)" % seconds_to_strtime(self.profile3.run_time)
 
  def test_air_dive4(self):
    diveseg3 = SegmentDive(55, 30*60, self.airdouble, 0)
    self.profile3 = Dive([diveseg3], [self.airdouble,self.decoo2, self.deco2])
    self.profile3.do_dive()
    assert str(self.profile3) == """Dive profile : GF:30.0-80.0
 DESCENT: at  55m for   2:45 [RT:  2:45], on Air,  SP:0.0, END:53m
   CONST: at  55m for  27:15 [RT: 30:00], on Air,  SP:0.0, END:53m
  ASCENT: at  30m for   2:30 [RT: 32:30], on Air,  SP:0.0, END:29m
    DECO: at  30m for   0:01 [RT: 32:31], on Air,  SP:0.0, END:29m
    DECO: at  27m for   1:12 [RT: 33:43], on Air,  SP:0.0, END:26m
    DECO: at  24m for   1:32 [RT: 35:15], on Air,  SP:0.0, END:23m
    DECO: at  21m for   1:34 [RT: 36:49], on Nitrox 50,  SP:0.0, END:20m
    DECO: at  18m for   2:08 [RT: 38:57], on Nitrox 50,  SP:0.0, END:17m
    DECO: at  15m for   2:55 [RT: 41:52], on Nitrox 50,  SP:0.0, END:14m
    DECO: at  12m for   4:16 [RT: 46:08], on Nitrox 50,  SP:0.0, END:11m
    DECO: at   9m for   5:40 [RT: 51:48], on Nitrox 50,  SP:0.0, END:8m
    DECO: at   6m for   6:31 [RT: 58:19], on Oxygen,  SP:0.0, END:5m
    DECO: at   3m for  11:16 [RT: 69:35], on Oxygen,  SP:0.0, END:2m
Gas:
  Oxygen : used: 303.7l (rem: 1096.3l or 156b)
  Nitrox 50 : used: 461.9l (rem: 938.1l or 134b)
  Air : used: 3533.8l (rem: 2466.2l or 82b)
Oxygen Toxicity: OTU:94, CNS:49%
""", "bad dive profile (%s)" % str(self.profile3)

  def test_air_dive4_run_time(self):
    diveseg3 = SegmentDive(55, 30*60, self.airdouble, 0)
    self.profile3 = Dive([diveseg3], [self.airdouble, self.deco2, self.decoo2 ])
    self.profile3.do_dive()
    assert seconds_to_strtime(self.profile3.run_time) == " 69:35", "bad dive runtime (%s)" % seconds_to_strtime(self.profile3.run_time)


  def test_tx_dive1(self):
    diveseg1 = SegmentDive(30, 30*60, self.txtank1, 0)
    self.profile1 = Dive([diveseg1], [self.txtank1])
    self.profile1.do_dive()
    assert str(self.profile1) == """Dive profile : GF:30.0-80.0
 DESCENT: at  30m for   1:30 [RT:  1:30], on Trimix 21/30,  SP:0.0, END:20m
   CONST: at  30m for  28:30 [RT: 30:00], on Trimix 21/30,  SP:0.0, END:20m
  ASCENT: at  15m for   1:30 [RT: 31:30], on Trimix 21/30,  SP:0.0, END:8m
    DECO: at  15m for   0:01 [RT: 31:31], on Trimix 21/30,  SP:0.0, END:8m
    DECO: at  12m for   0:37 [RT: 32:08], on Trimix 21/30,  SP:0.0, END:6m
    DECO: at   9m for   3:03 [RT: 35:11], on Trimix 21/30,  SP:0.0, END:4m
    DECO: at   6m for   5:00 [RT: 40:11], on Trimix 21/30,  SP:0.0, END:2m
    DECO: at   3m for  13:59 [RT: 54:10], on Trimix 21/30,  SP:0.0, END:0m
Gas:
  Trimix 21/30 : used: 2495.6l (rem: 1504.4l or 75b)
Oxygen Toxicity: OTU:20, CNS:7%
""", "bad dive profile (%s)" % str(self.profile1)

  def test_tx_dive1_run_time(self):
    diveseg1 = SegmentDive(30, 30*60, self.txtank1, 0)
    self.profile1 = Dive([diveseg1], [self.txtank1])
    self.profile1.do_dive()
    assert seconds_to_strtime(self.profile1.run_time) == " 54:10", "bad dive runtime (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_ccr_dive1(self):
    diveseg1 = SegmentDive(65, 30*60, self.txtank1, 1.4)
    self.profile1 = Dive([diveseg1], [self.txtank1, self.decoo2])
    self.profile1.do_dive()
    assert str(self.profile1) == """Dive profile : GF:30.0-80.0
 DESCENT: at  30m for   1:30 [RT:  1:30], on Trimix 21/30,  SP:0.0, END:20m
   CONST: at  30m for  28:30 [RT: 30:00], on Trimix 21/30,  SP:0.0, END:20m
  ASCENT: at  15m for   1:30 [RT: 31:30], on Trimix 21/30,  SP:0.0, END:8m
    DECO: at  15m for   0:01 [RT: 31:31], on Trimix 21/30,  SP:0.0, END:8m
    DECO: at  12m for   0:37 [RT: 32:08], on Trimix 21/30,  SP:0.0, END:6m
    DECO: at   9m for   3:03 [RT: 35:11], on Trimix 21/30,  SP:0.0, END:4m
    DECO: at   6m for   5:00 [RT: 40:11], on Trimix 21/30,  SP:0.0, END:2m
    DECO: at   3m for  13:59 [RT: 54:10], on Trimix 21/30,  SP:0.0, END:0m
Gas:
  Trimix 21/30 : used: 2495.6l (rem: 1504.4l or 75b)
Oxygen Toxicity: OTU:20, CNS:7%
""", "bad dive profile (%s)" % str(self.profile1)
    
if __name__ == "__main__":
  #unittest.main() 
  suite = unittest.TestLoader().loadTestsFromTestCase(Test)
  unittest.TextTestRunner(verbosity=2).run(suite)