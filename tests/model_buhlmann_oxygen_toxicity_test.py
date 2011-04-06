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
Test for oxygen toxicity class
"""

__version__ = "0.1"

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

import unittest
# import here the module / classes to be tested
from model.buhlmann.oxygen_toxicity import OxTox
import dipplanner

class Test(unittest.TestCase):
  def setUp(self):
    # temporary hack (tests):
    dipplanner.activate_debug_for_tests()
    
    self.ox1 = OxTox()
    self.ox2 = OxTox()
  
  def test1(self):
    assert self.ox1.cns == 0.0, "bad cns value : %s" % self.ox1.cns

  def test2(self):
    assert self.ox1.otu == 0.0, "bad otu value : %s" % self.ox1.otu

  def test3(self):
    assert self.ox1.max_ox == 0.0, "bad max_ox value : %s" % self.ox1.max_ox
    
  def test4(self):
    self.ox1.add_O2(10*60, 1.3)
    assert round(self.ox1.cns,13) == 0.0555555555556, "bad cns value : %s" % self.ox1.cns

  def test5(self):
    self.ox1.add_O2(10*60, 1.3)
    assert round(self.ox1.otu,10) == 14.7944872366, "bad otu value : %s" % self.ox1.otu

  def test6(self):
    self.ox1.add_O2(10*60, 1.3)
    self.ox1.remove_O2(4*60*60)
    assert round(self.ox1.cns,14) == 0.00874945594818, "bad cns value : %s" % self.ox1.cns
    
  def test7(self):
    self.ox1.add_O2(10*60, 1.3)
    self.ox1.remove_O2(4*60*60)
    assert round(self.ox1.otu,10) == 14.7944872366, "bad otu value : %s" % self.ox1.otu

  def test8(self):
    self.ox1.add_O2(10*60, 1.3)
    self.ox1.remove_O2(25*60*60)
    assert round(self.ox1.cns,7) == 0.0000005, "bad cns value : %s" % round(self.ox1.cns,7)

  def test9(self):
    self.ox1.add_O2(10*60, 1.3)
    self.ox1.remove_O2(25*60*60)
    assert round(self.ox1.otu,11) == 0.0, "bad otu value : %s" % self.ox1.otu
    
if __name__ == "__main__":
  #unittest.main()
  suite = unittest.TestLoader().loadTestsFromTestCase(Test)
  unittest.TextTestRunner(verbosity=2).run(suite)