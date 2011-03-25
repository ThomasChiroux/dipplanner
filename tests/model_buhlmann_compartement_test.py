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
Test for compartment class
"""

__version__ = "0.1"

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

import unittest
# import here the module / classes to be tested
from model.buhlmann.compartment import Compartment
from model.buhlmann.model_exceptions import ModelStateException

class Test(unittest.TestCase):
  def setUp(self):
    self.compt1 = Compartment(1.88,    5.0,    16.189, 0.4770, 11.696, 0.5578)
    self.compt2 = Compartment(1.88,    5.0,    16.189, 0.4770, 11.696, 0.5578)
    self.compt2.set_pp(0.3*5, (1-0.21-0.3)*5)
    self.compt3 = Compartment(1.88,    5.0,    16.189, 0.4770, 11.696, 0.5578)
    #self.compt3 = Compartment(70.69,  187.0,  5.333,  0.8997, 3.497,  0.9319)
    self.compt3.set_pp(0.0, 3.16)
    
  def test1(self):
    #myobj = Class()
    assert self.compt1.pp_He == 0, "wrong pp_He : %s" % self.compt1.pp_He
  
  def test2(self):
    #myobj = Class()
    assert self.compt1.pp_N2 == 0, "wrong pp_N2 : %s" % self.compt1.pp_N2
  
  def test3(self):
    assert round(self.compt1.k_He, 14) == 0.00614492181347, "wrong k_He : %s" % self.compt1.k_He

  def test4(self):
    assert round(self.compt1.k_N2, 14) == 0.00231049060187, "wrong k_N2 : %s" % self.compt1.k_N2

  def test5(self):
    assert self.compt1.a_He == 1.6189, "wrong a_He : %s" % self.compt1.a_He

  def test6(self):
    assert self.compt1.b_He == 0.4770, "wrong b_He : %s" % self.compt1.b_He

  def test7(self):
    assert self.compt1.a_N2 == 1.1696, "wrong a_N2 : %s" % self.compt1.a_N2
    
  def test8(self):
    assert self.compt1.b_N2 == 0.5578, "wrong b_N2 : %s" % self.compt1.b_N2
  
  def test9(self):
    assert self.compt2.pp_He == 1.5, "wrong pp_He : %s" % self.compt2.pp_He
    
  def test10(self):
    assert self.compt2.pp_N2 == 2.45, "wrong pp_N2 : %s" % self.compt2.pp_N2
  
  def test11(self):
    self.compt2.const_depth(0.3*4.5, (1-0.21-0.3)*4.5, 12*60)
    assert round(self.compt2.pp_He,11) == 1.35179731087,  "wrong pp_He : %s" % self.compt2.pp_He
  
  def test12(self):
    self.compt2.const_depth(0.3*4.5, (1-0.21-0.3)*4.5, 12*60)
    assert round(self.compt2.pp_N2,11) == 2.25141881985,  "wrong pp_N2 : %s" % self.compt2.pp_N2
  
  def test13(self):
    self.compt2.asc_desc(0.2997, 0.48951, 0.1, 0.163333333333, 9.0)
    assert round(self.compt2.pp_He, 11) == 1.45985489718,  "wrong pp_He : %s" % self.compt2.pp_He

  def test14(self):
    self.compt2.asc_desc(0.2997, 0.48951, 0.1, 0.163333333333, 9.0)
    assert round(self.compt2.pp_N2, 11) == 2.42483220311,  "wrong pp_N2 : %s" % self.compt2.pp_N2

  def test_m_value1(self):
    mv = self.compt3.get_m_value_at(0.0)
    assert mv == 1.1696, "wrong M-Value : %s" % mv
  
  def test_m_value2(self):
    mv = self.compt3.get_m_value_at(1.0)
    assert round(mv,11) == 2.96235726067, "wrong M-Value : %s" % mv
    
  def test_m_value3(self):
    mv = self.compt3.get_m_value_at(3.0)
    assert round(mv,9) == 6.547871782, "wrong M-Value : %s" % mv

  def test_max_amb1(self):
    max_amb = self.compt3.get_max_amb(0.8)
    assert round(max_amb,11) == 1.36110151389, "wrong max_amb for given gf : %s" % max_amb
    
  def test_mv1(self):
    mv = self.compt3.get_mv(1.0)
    assert round(mv,11) == 1.06671806333, "wrong mv for given amb pressure : %s" % mv
    
if __name__ == "__main__":
  unittest.main() 