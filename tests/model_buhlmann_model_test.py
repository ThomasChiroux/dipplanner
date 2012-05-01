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
Test for Model class
"""

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

import unittest
# import here the module / classes to be tested
import settings
from model.buhlmann.model import Model
from model.buhlmann.model_exceptions import ModelStateException
import dipplanner
import settings

class TestModelBuhlmannModel(unittest.TestCase):
  def setUp(self):
    # temporary hack (tests):
    dipplanner.activate_debug_for_tests()
    settings.RUN_TIME = True
    # simples test
    self.model1 = Model()
    
    # OC tests
    self.model2 = Model()
    self.model2.const_depth(30, 12*60, 0.0, 0.79, 0.0)
  
class TestModelBuhlmannModelSimple1(TestModelBuhlmannModel):
  def runTest(self):
    assert self.model1.units == "metric", "Error in model unit : %s" % self.model1.units
  
class TestModelBuhlmannModelSimple2(TestModelBuhlmannModel):
  def runTest(self):
    assert self.model1.gradient.gf_low == settings.GF_LOW, "Error in model gradient gf low : %s" % self.model1.gradient.gf_low

class TestModelBuhlmannModelSimple3(TestModelBuhlmannModel):
  def runTest(self):
    assert self.model1.gradient.gf_high == settings.GF_HIGH, "Error in model gradient gf high : %s" % self.model1.gradient.gf_high

class TestModelBuhlmannModelSimple3b(TestModelBuhlmannModel):
  def runTest(self):
    assert self.model1.gradient.gf == settings.GF_LOW, "Error in model gradient gf : %s" % self.model1.gradient.gf
    
class TestModelBuhlmannModelSimple4(TestModelBuhlmannModel):
  def runTest(self):
    assert self.model1.metadata == "(none)", "Error in model metadata : %s" % self.model1.metadata

class TestModelBuhlmannModelSimple5(TestModelBuhlmannModel):
  def runTest(self):
    assert len(self.model1.tissues) == 16, "Error in tissues number : %s" % len(self.model1.tissues)

class TestModelBuhlmannModelSimple6(TestModelBuhlmannModel):
  def runTest(self):
    assert self.model1.ox_tox.otu == 0.0, "Error in model ox tox otu : %s" % self.model1.ox_tox_otu

class TestModelBuhlmannModelSimple7(TestModelBuhlmannModel):
  def runTest(self):
    assert self.model1.validate_model() == self.model1.MODEL_VALIDATION_SUCCESS, "Error in model validation : %s" % self.model1.validate_model()

class TestModelBuhlmannModelSimple8(TestModelBuhlmannModel):
  def runTest(self):
    # empty model should have the first compartement for control compartment ??
    assert self.model1.control_compartment() == 1, "Error in control compartement : %s" % self.model1.control_compartment()

class TestModelBuhlmannModelSimple9(TestModelBuhlmannModel):
  def runTest(self):
    assert self.model1.ceiling() == 0.0, "Error in model ceiling : %s" % self.model1.ceiling()

class TestModelBuhlmannModelSimple10(TestModelBuhlmannModel):
  def runTest(self):
    mv = self.model1.m_value(12)
    self.assertAlmostEqual(mv,0.0575632450001, 13, "Error in model m_value : %s" % mv)

class TestModelBuhlmannModelOutput1(TestModelBuhlmannModel):
  def runTest(self):
    assert str(self.model1) == """C:0 He:0.0 N2:0.7894075 gf:0.3 mv_at:2.98611129437 max_amb:0.35427199186 MV:0.264359704706
C:1 He:0.0 N2:0.7894075 gf:0.3 mv_at:2.55549585508 max_amb:0.421704338078 MV:0.308905803322
C:2 He:0.0 N2:0.7894075 gf:0.3 mv_at:2.26480470784 max_amb:0.47594471845 MV:0.34855433551
C:3 He:0.0 N2:0.7894075 gf:0.3 mv_at:2.05108817891 max_amb:0.519249093188 MV:0.384872531623
C:4 He:0.0 N2:0.7894075 gf:0.3 mv_at:1.91362345557 max_amb:0.551258498308 MV:0.412519765945
C:5 He:0.0 N2:0.7894075 gf:0.3 mv_at:1.76138724212 max_amb:0.588619561872 MV:0.448173735522
C:6 He:0.0 N2:0.7894075 gf:0.3 mv_at:1.66029300587 max_amb:0.613332959186 MV:0.475462763025
C:7 He:0.0 N2:0.7894075 gf:0.3 mv_at:1.58720538721 max_amb:0.631240751867 MV:0.49735686784
C:8 He:0.0 N2:0.7894075 gf:0.3 mv_at:1.53314126705 max_amb:0.644488367648 MV:0.514895474388
C:9 He:0.0 N2:0.7894075 gf:0.3 mv_at:1.47853129473 max_amb:0.658794052605 MV:0.533913284632
C:10 He:0.0 N2:0.7894075 gf:0.3 mv_at:1.43699477412 max_amb:0.66981321627 MV:0.54934611748
C:11 He:0.0 N2:0.7894075 gf:0.3 mv_at:1.39988162289 max_amb:0.679769847163 MV:0.563910181471
C:12 He:0.0 N2:0.7894075 gf:0.3 mv_at:1.35416745806 max_amb:0.692443494068 MV:0.582946736243
C:13 He:0.0 N2:0.7894075 gf:0.3 mv_at:1.33536177703 max_amb:0.69730263408 MV:0.591156279577
C:14 He:0.0 N2:0.7894075 gf:0.3 mv_at:1.30754890648 max_amb:0.704951492069 MV:0.60373076379
C:15 He:0.0 N2:0.7894075 gf:0.3 mv_at:1.28237367658 max_amb:0.711920003638 MV:0.615583050727
""", "Error in model output : %s" % str(self.model1)

class TestModelBuhlmannModelGf1(TestModelBuhlmannModel):
  def runTest(self):
    assert self.model2.gradient.gf == settings.GF_LOW, "Error in model gf : %s" % self.model2.gradient.gf
  
class TestModelBuhlmannModelOutput2(TestModelBuhlmannModel):
  def runTest(self):
    assert str(self.model2) == """C:0 He:0.0 N2:19.9990971717 gf:0.3 mv_at:2.98611129437 max_amb:15.8731505639 MV:6.69737166509
C:1 He:0.0 N2:16.1101921429 gf:0.3 mv_at:2.55549585508 max_amb:13.6230577025 MV:6.3041355011
C:2 He:0.0 N2:12.3062586541 gf:0.3 mv_at:2.26480470784 max_amb:10.8012791569 MV:5.43369528134
C:3 He:0.0 N2:9.37171017012 gf:0.3 mv_at:2.05108817891 max_amb:8.44098526466 MV:4.56914055011
C:4 He:0.0 N2:7.07305376653 gf:0.3 mv_at:1.91362345557 max_amb:6.42829972225 MV:3.6961575413
C:5 He:0.0 N2:5.41588728834 gf:0.3 mv_at:1.76138724212 max_amb:4.97098782429 MV:3.07478512325
C:6 He:0.0 N2:4.15542805915 gf:0.3 mv_at:1.66029300587 max_amb:3.83408085637 MV:2.50282814206
C:7 He:0.0 N2:3.21612142045 gf:0.3 mv_at:1.58720538721 max_amb:2.97204631983 MV:2.02627929969
C:8 He:0.0 N2:2.53066686651 gf:0.3 mv_at:1.53314126705 max_amb:2.33509643227 MV:1.65064167334
C:9 He:0.0 N2:2.10187885266 gf:0.3 mv_at:1.47853129473 max_amb:1.93886795897 MV:1.42159916408
C:10 He:0.0 N2:1.82048315137 gf:0.3 mv_at:1.43699477412 max_amb:1.67876956492 MV:1.26686831724
C:11 He:0.0 N2:1.60003592996 gf:0.3 mv_at:1.39988162289 max_amb:1.47524673917 MV:1.14297945183
C:12 He:0.0 N2:1.42700524191 gf:0.3 mv_at:1.35416745806 max_amb:1.31965716663 MV:1.05378787049
C:13 He:0.0 N2:1.28951969694 gf:0.3 mv_at:1.33536177703 max_amb:1.19034771379 MV:0.965670666274
C:14 He:0.0 N2:1.18196555303 gf:0.3 mv_at:1.30754890648 max_amb:1.09268807582 MV:0.90395513864
C:15 He:0.0 N2:1.09782574015 gf:0.3 mv_at:1.28237367658 max_amb:1.01704768217 MV:0.856088798612
""", "Error in model output : %s" % str(self.model2)

if __name__ == "__main__":
  #unittest.main() 
  import sys
  suite = unittest.findTestCases(sys.modules[__name__])
  #suite = unittest.TestLoader().loadTestsFromTestCase(Test)
  unittest.TextTestRunner(verbosity=2).run(suite)