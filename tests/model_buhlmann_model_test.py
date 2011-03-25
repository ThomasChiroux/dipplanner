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
Test for Model class
"""

__version__ = "0.1"

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

import unittest
# import here the module / classes to be tested
import settings
from model.buhlmann.model import Model
from model.buhlmann.model_exceptions import ModelStateException

class Test(unittest.TestCase):
  def setUp(self):
    # simples test
    self.model1 = Model()
    
    # OC tests
    self.model2 = Model()
    self.model2.const_depth(30, 12*60, 0.0, 0.79, 0.0)
  
  def test_simple1(self):
    assert self.model1.units == "metric", "Error in model unit : %s" % self.model1.units
  
  def test_simple2(self):
    assert self.model1.gradient.gf_low == settings.GF_LOW, "Error in model gradient gf low : %s" % self.model1.gradient.gf_low

  def test_simple3(self):
    assert self.model1.gradient.gf_high == settings.GF_HIGH, "Error in model gradient gf high : %s" % self.model1.gradient.gf_high

  def test_simple3bis(self):
    assert self.model1.gradient.gf == settings.GF_LOW, "Error in model gradient gf : %s" % self.model1.gradient.gf
    
  def test_simple4(self):
    assert self.model1.metadata == "(none)", "Error in model metadata : %s" % self.model1.metadata

  def test_simple5(self):
    assert len(self.model1.tissues) == 16, "Error in tissues number : %s" % len(self.model1.tissues)

  def test_simple6(self):
    assert self.model1.ox_tox.otu == 0.0, "Error in model ox tox otu : %s" % self.model1.ox_tox_otu

  def test_simple7(self):
    assert self.model1.validate_model() == self.model1.MODEL_VALIDATION_SUCCESS, "Error in model validation : %s" % self.model1.validate_model()

  def test_simple8(self):
    # empty model should have the first compartement for control compartment ??
    assert self.model1.control_compartment() == 1, "Error in control compartement : %s" % self.model1.control_compartment()

  def test_simple9(self):
    assert self.model1.ceiling() == 0.0, "Error in model ceiling : %s" % self.model1.ceiling()

  def test_simple10(self):
    mv = self.model1.m_value(12)
    assert round(mv,12) == 0.310114218019, "Error in model m_value : %s" % mv

  def test_output1(self):
    assert str(self.model1) == "coucou", "Error in model output : %s" % str(self.model1)

  def test_cstd1(self):
    assert self.model2.gradient.gf == settings.GF_LOW, "Error in model gf : %s" % self.model2.gradient.gf
  
  def test_output2(self):
    assert str(self.model2) == "coucou2", "Error in model output : %s" % str(self.model1)

    
if __name__ == "__main__":
  unittest.main() 