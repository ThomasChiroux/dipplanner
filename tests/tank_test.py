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
"""
Test for tank class
"""

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

import unittest
# local imports
from tank import Tank, InvalidGas, InvalidTank, InvalidMod, EmptyTank
import dipplanner

class TestTank(unittest.TestCase):
  def setUp(self):
    # temporary hack (tests):
    dipplanner.activate_debug_for_tests()

  def tearDown(self):
    pass

class TestTankisAir(TestTank):    
  def runTest(self):
    mytank = Tank()
    assert str(mytank) == 'Air'
    assert mytank.mod == 66

class TestTankNitrox32(TestTank):    
  def runTest(self):
    mytank = Tank(f_O2=0.32)
    assert str(mytank) == 'Nitrox 32'
    assert mytank.mod == 40
  
class TestTankisO2(TestTank):    
  def runTest(self):
    mytank = Tank(f_O2=1)
    assert str(mytank) == 'Oxygen'
    assert mytank.mod == 6

class TestTankisTrimix2030(TestTank):    
  def runTest(self):
    mytank = Tank(f_O2=0.2, f_He=0.3)
    assert str(mytank) == 'Trimix 20/30'
    assert mytank.mod == 70
    
class TestTankisTrimix870(TestTank):    
  def runTest(self):
    mytank = Tank(f_O2=0.1, f_He=0.7)
    assert str(mytank) == 'Trimix 10/70'
    assert mytank.mod == 150

class TestTankisHeliox2080(TestTank):    
  def runTest(self):
    mytank = Tank(f_O2=0.2, f_He=0.8)
    assert str(mytank) == 'Heliox 20/80'
    assert mytank.mod == 70

class TestTankisAir2(TestTank):    
  def runTest(self):
    mytank = Tank(max_ppo2=1.4)
    assert str(mytank) == 'Air'
    assert mytank.mod == 56

class TestTankisNitrox32_2(TestTank):    
  def runTest(self):
    mytank = Tank(f_O2=0.32, max_ppo2=1.4)
    assert str(mytank) == 'Nitrox 32'
    assert mytank.mod == 33

class TestTankisO2_2(TestTank):    
  def runTest(self):
    mytank = Tank(f_O2=1, max_ppo2=1.4)
    assert str(mytank) == 'Oxygen'
    assert mytank.mod == 4

class TestTankisTrimix2030_2(TestTank):    
  def runTest(self):
    mytank = Tank(f_O2=0.2, f_He=0.3, max_ppo2=1.4)
    assert str(mytank) == 'Trimix 20/30'
    assert mytank.mod == 59

class TestTankisTrimix870_2(TestTank):    
  def runTest(self):
    mytank = Tank(f_O2=0.08, f_He=0.7, max_ppo2=1.4)
    assert str(mytank) == 'Trimix 8/70'
    assert mytank.mod == 165
    assert mytank.get_min_od() == 10

class TestTankisHeliox2080_2(TestTank):    
  def runTest(self):
    mytank = Tank(f_O2=0.2, f_He=0.8, max_ppo2=1.4)
    assert str(mytank) == 'Heliox 20/80'
    assert mytank.mod == 59

class TestTankVolume1(TestTank):
  def runTest(self):
    mytank = Tank(tank_vol=15, tank_pressure=207)
    self.assertAlmostEqual(mytank.total_gas,3116, 0, 'Wrong Tank Volume : %s' % mytank.total_gas)

class TestTankVolume2(TestTank):
  def runTest(self):
    mytank = Tank(tank_vol=18, tank_pressure=230)
    self.assertAlmostEqual(mytank.total_gas, 4064, 0, 'Wrong Tank Volume : %s' % mytank.total_gas)

class TestTankVolume3(TestTank):    
  def runTest(self):
    mytank = Tank(tank_vol=15, tank_pressure=207)
    mytank.consume_gas(405)
    self.assertAlmostEqual(mytank.remaining_gas, 2711, 0, 'Wrong Tank Volume : %s' % mytank.remaining_gas)

class TestTankVolume4(TestTank):
  def runTest(self):
    mytank = Tank(tank_vol=15, tank_pressure=207)
    mytank.consume_gas(405)
    try:
      mytank.consume_gas(2800)
    except EmptyTank:
      pass
    else:
      self.fail("should raise EmptyTank")

class TestTankInvalidGas(TestTank):    
  def runTest(self):
    try:
      mytank = Tank(f_O2 = 0.8, f_He=0.3)
    except InvalidGas:
      pass
    else:
      self.fail("should raise Invalid Gas")

class TestTankInvalidTank1(TestTank):    
  def runTest(self):  
    try:
      mytank = Tank(f_O2 = 0.8, tank_vol=33)
    except InvalidTank:
      pass
    else:
      self.fail("should raise Invalid Tank")

class TestTankInvalidTank2(TestTank):    
  def runTest(self):  
    try:
      mytank = Tank(f_O2 = 0.3, tank_pressure=350)
    except InvalidTank:
      pass
    else:
      self.fail("should raise Invalid Tank")

class TestTankInvalidMod1(TestTank):    
  def runTest(self):  
    try:
      mytank = Tank(f_O2 = 0.8, mod=33)
    except InvalidMod:
      pass
    else:
      self.fail("should raise Invalid Mod")

class TestTankInvalidMod2(TestTank):
  def runTest(self):  
    try:
      mytank = Tank(f_O2 = 1, mod=7)
    except InvalidMod:
      pass
    else:
      self.fail("should raise Invalid Mod")
  
if __name__ == "__main__":
  if __package__ is None:
    __package__ = "dipplanner"
  import sys
  suite = unittest.findTestCases(sys.modules[__name__]) 
  #suite = unittest.TestLoader().loadTestsFromTestCase([TestTankInvalidGas, TestTankInvalidMod1])
  #suite = unittest.TestSuite()
  #suite2 = unittest.TestSuite()
  #suite.addTest(TestTankInvalidGas())
  #suite2.addTest(TestTankInvalidMod1())
  #unittest.TextTestRunner(verbosity=2).run(suite2)
  unittest.TextTestRunner(verbosity=2).run(suite)