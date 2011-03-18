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
Test for compartment class
"""

__version__ = "0.1"

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

import unittest
# import here the module / classes to be tested
from model.buhlmann.compartment import Compartment, ModelStateException

class Test(unittest.TestCase):
  def setUp(self):
    self.compt1 = Compartment(1.88,    5.0,    16.189, 0.4770, 11.696, 0.5578)
    self.compt2 = Compartment(1.88,    5.0,    16.189, 0.4770, 11.696, 0.5578)
    self.compt2.set_pp(1.4, 1.9)
    self.compt3 = Compartment(1.88,    5.0,    16.189, 0.4770, 11.696, 0.5578)
    self.compt3.set_pp(1.4, 1.9)
    
  def test1(self):
    #myobj = Class()
    assert self.compt1.pp_He == 0, "wrong pp_He : %s" % self.compt1.pp_He
  
  def test2(self):
    #myobj = Class()
    assert self.compt1.pp_N2 == 0, "wrong pp_N2 : %s" % self.compt1.pp_N2
  
  def test3(self):
    assert self.compt1.k_He == 0.36869530880848156, "wrong k_He : %s" % self.compt1.k_He

  def test4(self):
    assert self.compt1.k_N2 == 0.13862943611198905, "wrong k_N2 : %s" % self.compt1.k_N2

  def test5(self):
    assert self.compt1.a_He == 16.189, "wrong a_He : %s" % self.compt1.a_He

  def test6(self):
    assert self.compt1.b_He == 0.4770, "wrong b_He : %s" % self.compt1.b_He

  def test7(self):
    assert self.compt1.a_N2 == 11.696, "wrong a_N2 : %s" % self.compt1.a_N2
    
  def test8(self):
    assert self.compt1.b_N2 == 0.5578, "wrong b_N2 : %s" % self.compt1.b_N2
  
  def test9(self):
    assert self.compt2.pp_He == 1.4, "wrong pp_He : %s" % self.compt2.pp_He
    
  def test10(self):
    assert self.compt2.pp_N2 == 1.9, "wrong pp_N2 : %s" % self.compt2.pp_N2
  
  def test11(self):
    self.compt2.const_depth(1.5, 2.1, 12*60)
    assert round(self.compt2.pp_He,11) == 1.49880179275,  "wrong pp_He : %s" % self.compt2.pp_He
  
  def test12(self):
    self.compt2.const_depth(1.5, 2.1, 12*60)
    assert round(self.compt2.pp_N2,11) == 2.06210708584,  "wrong pp_N2 : %s" % self.compt2.pp_N2
  
  def test13(self):
    self.compt2.asc_desc(3.1, 5.6, 0.125, 0.125, 12*60)
    assert round(self.compt2.pp_He, 11) == 4.24465946415,  "wrong pp_He : %s" % self.compt2.pp_He

  def test14(self):
    self.compt2.asc_desc(3.1, 5.6, 0.125, 0.125, 12*60)
    assert round(self.compt2.pp_N2, 11) == 5.66813393539,  "wrong pp_N2 : %s" % self.compt2.pp_N2

  def test15(self):
    mv = self.compt3.get_m_value_at(2.2)
    assert  mv == 2, "wrong M-Value : %s" % mv
    
  def test16(self):
    max_amb = self.compt3.get_max_amb(0.8)
    assert max_amb == 2, "wrong max_amb for given gf : %s" % max_amb
    
  def test17(self):
    mv = self.compt3.get_mv(6.2)
    assert mv == 2, "wrong mv for given amb pressure : %s" % mv
if __name__ == "__main__":
  unittest.main() 