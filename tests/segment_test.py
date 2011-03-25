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
Test for XXXXX class
"""

__version__ = "0.1"

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

import unittest
# import here the module / classes to be tested
from tank import Tank
from segment import SegmentDive, SegmentDeco, SegmentAscDesc
from segment import UnauthorizedMod

class Test(unittest.TestCase):
  def setUp(self):
    self.airtank = Tank()
    self.trimixtank1 = Tank(f_O2=0.10, f_He=0.70)
    self.nitroxtank1 = Tank(f_O2=0.40)
    self.oxygentank1 = Tank(f_O2=1)
    self.diveseg1 = SegmentDive(30, 10*60, self.airtank, 0)
    self.diveseg2 = SegmentDive(150, 10*60, self.trimixtank1, 0)
    self.decoseg1 = SegmentDeco(12, 5*60, self.nitroxtank1, 0)
    self.decoseg2 = SegmentDeco(3, 15*60, self.oxygentank1, 0)
    self.ascseg1 = SegmentAscDesc(150,50, 20.0/60, self.trimixtank1, 0)
    self.ascseg2 = SegmentAscDesc(30, 12, 10.0/60, self.nitroxtank1, 0)
    self.descseg1 = SegmentAscDesc(0, 40, 20.0/60, self.airtank,0)
    self.descseg2 = SegmentAscDesc(40,150, 20.0/60, self.trimixtank1, 0)
    
  def test_gas_used1(self):
    assert round(self.diveseg1.gas_used(),2) == 682.21, 'Wrong gas used : %s' % self.diveseg1.gas_used()
    
  def test_gas_end1(self):
    assert self.diveseg1.get_end() == 29, 'wrong E.N.D : %s' % self.diveseg1.get_end()
    
  def test_gas_end2(self):
    assert self.diveseg2.get_end() == 62, 'wrong E.N.D : %s' % self.diveseg2.get_end()

  def test_str1(self):
    assert str(self.diveseg2) == "CONST: for 600.0s at 150.0m on Trimix 10/70, SP:0.0, END:62m", \
                                                  'wrong name : %s' % str(self.diveseg2)
  
  def test_deco1(self):
    assert self.decoseg1.gas_used() == 132.78, 'Wrong gas used : %s' % self.decoseg1.gas_used()
  
  def test_deco2(self):
    assert round(self.decoseg2.gas_used(),2) == 236.34, 'Wrong gas used : %s' % self.decoseg2.gas_used()
    
  def test_asc1(self):
    assert self.ascseg1.gas_used() == 936.105, 'Wrong gas used : %s' % self.ascseg1.gas_used()
    
  def test_asc2(self):
    assert self.ascseg2.gas_used() == 95.2578, 'Wrong gas used : %s' % self.ascseg2.gas_used()

  def test_desc1(self):
    assert self.descseg1.gas_used() == 102.442, 'Wrong gas used : %s' % self.descseg1.gas_used()

  def test_desc2(self):
    assert self.descseg2.gas_used() == 982.9655, 'Wrong gas used : %s' % self.descseg2.gas_used()

  def test_wrong_mod1(self):
    try:
      baddiveseg = SegmentDive(150, 10*60, self.airtank,0)
    except UnauthorizedMod:
      pass
    else:
      self.fail("should raise UnauthorizedMod") 
  
  def test_wrong_mod2(self):
    try:
      baddiveseg = SegmentDeco(3, 10*60, self.trimixtank1,0)
    except UnauthorizedMod:
      pass
    else:
      self.fail("should raise UnauthorizedMod") 
  
  def test_wrong_mod3(self):
    try:
      baddiveseg = SegmentAscDesc(150, 3, 10, self.nitroxtank1,0)
    except UnauthorizedMod:
      pass
    else:
      self.fail("should raise UnauthorizedMod") 

  def test_wrong_mod4(self):
    try:
      baddiveseg = SegmentAscDesc(3, 150, 10, self.trimixtank1,0)
    except UnauthorizedMod:
      pass
    else:
      self.fail("should raise UnauthorizedMod") 

  
if __name__ == "__main__":
  unittest.main() 