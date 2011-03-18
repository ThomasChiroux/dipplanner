#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2011 Thomas Chiroux
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program.
# If not, see <http://www.gnu.org/licenses/lgpl-3.0.html>
# 
# This module is part of PPlan, a Dive planning Tool written in python
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

from model.buhlmann.gradient import Gradient

class Test(unittest.TestCase):
  def setUp(self):
    self.gradient1 = Gradient(0.3, 0.8)
    self.gradient2 = Gradient(0.35, 0.75)
  
  def test1(self):
    assert self.gradient1.gf_low == 0.3, "wrong gw_low : %s" % self.gradient1.gf_low

  def test2(self):
    assert self.gradient1.gf_high == 0.8, "wrong gw_high : %s" % self.gradient1.gf_high

  def test3(self):
    assert self.gradient1.gf_slope == 1.0, "wrong gw_slope : %s" % self.gradient1.gf_slope

  def test4(self):
    assert self.gradient1.gf == 0.3, "wrong gw_low : %s" % self.gradient1.gf

  def test5(self):
    self.gradient2.set_gf_slope_at_depth(12)
    assert round(self.gradient2.gf_slope, 13) == -0.0333333333333, "wrong gw_slope : %s" % self.gradient2.gf_slope
    
  def test6(self):
    self.gradient2.set_gf_slope_at_depth(6)
    self.gradient2.set_gf_at_depth(6)
    assert self.gradient2.gf == 0.35, "wrong gw_low : %s" % self.gradient2.gf

if __name__ == "__main__":
  unittest.main() 