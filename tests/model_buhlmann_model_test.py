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
import dipplanner

class Test(unittest.TestCase):
  def setUp(self):
    # temporary hack (tests):
    dipplanner.activate_debug_for_tests()
    
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
    assert round(mv,13) == 0.0575499302299, "Error in model m_value : %s" % mv

  def test_output1(self):
    assert str(self.model1) == """C:0 He:0.0 N2:0.78921 gf:0.3 mv_at:2.98566310506 max_amb:0.354112438085 MV:0.264333239294
C:1 He:0.0 N2:0.78921 gf:0.3 mv_at:2.55511206632 max_amb:0.421534159634 MV:0.308874906273
C:2 He:0.0 N2:0.78921 gf:0.3 mv_at:2.26445854334 max_amb:0.475767651513 MV:0.348520401189
C:3 He:0.0 N2:0.78921 gf:0.3 mv_at:2.0507686901 max_amb:0.519066794456 MV:0.384836185481
C:4 He:0.0 N2:0.78921 gf:0.3 mv_at:1.91331580113 max_amb:0.551073778228 MV:0.412482873728
C:5 He:0.0 N2:0.78921 gf:0.3 mv_at:1.76109082286 max_amb:0.58843248276 MV:0.448137023801
C:6 He:0.0 N2:0.78921 gf:0.3 mv_at:1.66000541815 max_amb:0.613143983005 MV:0.475426159077
C:7 He:0.0 N2:0.78921 gf:0.3 mv_at:1.58692480359 max_amb:0.631050243586 MV:0.49732035079
C:8 He:0.0 N2:0.78921 gf:0.3 mv_at:1.53286630004 max_amb:0.644296612703 MV:0.514858993232
C:9 He:0.0 N2:0.78921 gf:0.3 mv_at:1.47826020386 max_amb:0.658601427756 MV:0.533877593362
C:10 He:0.0 N2:0.78921 gf:0.3 mv_at:1.43672650499 max_amb:0.669619953167 MV:0.549311227474
C:11 He:0.0 N2:0.78921 gf:0.3 mv_at:1.39961575029 max_amb:0.679576038655 MV:0.56387619233
C:12 He:0.0 N2:0.78921 gf:0.3 mv_at:1.3539036615 max_amb:0.6922492106 MV:0.582914443948
C:13 He:0.0 N2:0.78921 gf:0.3 mv_at:1.33509983236 max_amb:0.697107924965 MV:0.591124334581
C:14 He:0.0 N2:0.78921 gf:0.3 mv_at:1.30728854405 max_amb:0.7047564178 MV:0.603699928061
C:15 He:0.0 N2:0.78921 gf:0.3 mv_at:1.28211468973 max_amb:0.711724610796 MV:0.615553355967
""", "Error in model output : %s" % str(self.model1)

  def test_cstd1(self):
    assert self.model2.gradient.gf == settings.GF_LOW, "Error in model gf : %s" % self.model2.gradient.gf
  
  def test_output2(self):
    assert str(self.model2) == """C:0 He:0.0 N2:19.9988996717 gf:0.3 mv_at:2.98566310506 max_amb:15.8729910102 MV:6.69831088372
C:1 He:0.0 N2:16.1099946429 gf:0.3 mv_at:2.55511206632 max_amb:13.622887524 MV:6.3050051132
C:2 He:0.0 N2:12.3060611541 gf:0.3 mv_at:2.26445854334 max_amb:10.8011020899 MV:5.43443870515
C:3 He:0.0 N2:9.37151267012 gf:0.3 mv_at:2.0507686901 max_amb:8.44080296593 MV:4.56975607019
C:4 He:0.0 N2:7.07285626653 gf:0.3 mv_at:1.91331580113 max_amb:6.42811500217 MV:3.69664864647
C:5 He:0.0 N2:5.41568978834 gf:0.3 mv_at:1.76109082286 max_amb:4.97080074517 MV:3.0751905115
C:6 He:0.0 N2:4.15523055915 gf:0.3 mv_at:1.66000541815 max_amb:3.83389188019 MV:2.50314276912
C:7 He:0.0 N2:3.21592392045 gf:0.3 mv_at:1.58692480359 max_amb:2.97185581154 MV:2.02651311088
C:8 He:0.0 N2:2.53046936651 gf:0.3 mv_at:1.53286630004 max_amb:2.33490467732 MV:1.65080892341
C:9 He:0.0 N2:2.10168135266 gf:0.3 mv_at:1.47826020386 max_amb:1.93867533412 MV:1.42172626116
C:10 He:0.0 N2:1.82028565137 gf:0.3 mv_at:1.43672650499 max_amb:1.67857630182 MV:1.26696740475
C:11 He:0.0 N2:1.59983842996 gf:0.3 mv_at:1.39961575029 max_amb:1.47505293066 MV:1.14305546334
C:12 He:0.0 N2:1.42680774191 gf:0.3 mv_at:1.3539036615 max_amb:1.31946288316 MV:1.05384731757
C:13 He:0.0 N2:1.28932219694 gf:0.3 mv_at:1.33509983236 max_amb:1.19015300467 MV:0.965712200465
C:14 He:0.0 N2:1.18176805303 gf:0.3 mv_at:1.30728854405 max_amb:1.09249300155 MV:0.90398409625
C:15 He:0.0 N2:1.09762824015 gf:0.3 mv_at:1.28211468973 max_amb:1.01685228933 MV:0.856107685952
""", "Error in model output : %s" % str(self.model2)

if __name__ == "__main__":
  #unittest.main() 
  suite = unittest.TestLoader().loadTestsFromTestCase(Test)
  unittest.TextTestRunner(verbosity=2).run(suite)