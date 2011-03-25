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
# Strongly inspired by Guy Wittig's MVPlan 
"""
Test for tank class
"""

__version__ = "0.1"

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

import unittest
# local imports
from tank import Tank, InvalidGas, InvalidTank, InvalidMod, EmptyTank

class TestTank(unittest.TestCase):
  
  def testTankisAir(self):
    mytank = Tank()
    assert str(mytank) == 'Air'
    assert mytank.mod == 66

  def testTankisNitrox32(self):
    mytank = Tank(f_O2=0.32)
    assert str(mytank) == 'Nitrox 32'
    assert mytank.mod == 40
  
  def testTankisO2(self):
    mytank = Tank(f_O2=1)
    assert str(mytank) == 'Oxygen'
    assert mytank.mod == 6
    
  def testTankisTrimix2030(self):
    mytank = Tank(f_O2=0.2, f_He=0.3)
    assert str(mytank) == 'Trimix 20/30'
    assert mytank.mod == 70
  
  def testTankisTrimix870(self):
    mytank = Tank(f_O2=0.1, f_He=0.7)
    assert str(mytank) == 'Trimix 10/70'
    assert mytank.mod == 150

  def testTankisHeliox2080(self):
    mytank = Tank(f_O2=0.2, f_He=0.8)
    assert str(mytank) == 'Heliox 20/80'
    assert mytank.mod == 70

  def testTankisAir2(self):
    mytank = Tank(max_ppo2=1.4)
    assert str(mytank) == 'Air'
    assert mytank.mod == 56

  def testTankisNitrox32_2(self):
    mytank = Tank(f_O2=0.32, max_ppo2=1.4)
    assert str(mytank) == 'Nitrox 32'
    assert mytank.mod == 33

  def testTankisO2_2(self):
    mytank = Tank(f_O2=1, max_ppo2=1.4)
    assert str(mytank) == 'Oxygen'
    assert mytank.mod == 4

  def testTankisTrimix2030_2(self):
    mytank = Tank(f_O2=0.2, f_He=0.3, max_ppo2=1.4)
    assert str(mytank) == 'Trimix 20/30'
    assert mytank.mod == 59

  def testTankisTrimix870_2(self):
    mytank = Tank(f_O2=0.08, f_He=0.7, max_ppo2=1.4)
    assert str(mytank) == 'Trimix 8/70'
    assert mytank.mod == 165
    assert mytank.get_min_od() == 10
    
  def testTankisHeliox2080_2(self):
    mytank = Tank(f_O2=0.2, f_He=0.8, max_ppo2=1.4)
    assert str(mytank) == 'Heliox 20/80'
    assert mytank.mod == 59

  
  def testTankVolume1(self):
    mytank = Tank(tank_vol=15, tank_pressure=207)
    assert mytank.total_gas == 3105

  def testTankVolume2(self):
    mytank = Tank(tank_vol=18, tank_pressure=230)
    assert mytank.total_gas == 4140

  def testTankVolume3(self):
    mytank = Tank(tank_vol=15, tank_pressure=207)
    mytank.consume_gas(405)
    assert mytank.remaining_gas == 2700
  
  def testTankVolume4(self):
    mytank = Tank(tank_vol=15, tank_pressure=207)
    mytank.consume_gas(405)
    try:
      mytank.consume_gas(2800)
    except EmptyTank:
      pass
    else:
      self.fail("should raise EmptyTank")

  def testTankInvalidGas(self):
    try:
      mytank = Tank(f_O2 = 0.8, f_He=0.3)
    except InvalidGas:
      pass
    else:
      self.fail("should raise Invalid Gas")
    
  def testTankInvalidTank1(self):
    try:
      mytank = Tank(f_O2 = 0.8, tank_vol=33)
    except InvalidTank:
      pass
    else:
      self.fail("should raise Invalid Tank")
      
  def testTankInvalidTank2(self):
    try:
      mytank = Tank(f_O2 = 0.3, tank_pressure=350)
    except InvalidTank:
      pass
    else:
      self.fail("should raise Invalid Tank")
  
  def testTankInvalidMod1(self):
    try:
      mytank = Tank(f_O2 = 0.8, mod=33)
    except InvalidMod:
      pass
    else:
      self.fail("should raise Invalid Mod")

  def testTankInvalidMod2(self):
    try:
      mytank = Tank(f_O2 = 1, mod=7)
    except InvalidMod:
      pass
    else:
      self.fail("should raise Invalid Mod")
      
    
    
if __name__ == "__main__":
  if __package__ is None:
    __package__ = "dipplanner"
  unittest.main() 