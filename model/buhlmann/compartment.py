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
"""Defines a Buhlmann compartment
"""

__version__ = "0.1"

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

import math

# local imports
import settings

class ModelException(Exception):
  """Base exception class for model"""
  def __init__(self, description):
    self.description = description
  
  def __str__(self):
    return repr(self.description)
  
class ModelStateException(ModelException):
  """Model State Exception"""
  pass
    
class Compartment(object):
  """Buhlmann compartment class"""
  
  def __init__(self, h_He=None, h_N2=None, 
                     a_He=None, b_He=None, 
                     a_N2=None, b_N2=None):
    """Constructor for Compartment
    can be called without params, in this case, does not initiate anything
    can be called with time params and coef and in this case initate the
    compartment time constants"""
    self.pp_He = 0
    self.pp_N2 = 0
    if h_He and h_N2 and a_He and b_He and a_N2 and b_N2:
      self.set_compartment_time_constants(h_He, h_N2, a_He, b_He, a_N2, b_N2)
  
  
  def set_compartment_time_constants(self, h_He, h_N2, a_He, b_He, a_N2, b_N2):
    """Sets the compartment's time constants :
    h_He : Helium Halftime
    h_N2 : Nitrogen Halftime
    a_He : Helium : a coefficient
    b_He : Helium : b coefficient
    a_N2 : Nitrogen : a coefficient
    b_N2 : Nitrogen : b coefficient
    """
    self.k_He = math.log(2) / h_He
    self.k_N2 = math.log(2) / h_N2
    self.a_He = a_He
    self.b_He = b_He
    self.a_N2 = a_N2
    self.b_N2 = b_N2
    
  def set_pp(self, pp_He, pp_N2):
    """Sets partial pressures of He and N2
    raise ModelStateException if pp < 0"""
    if pp_He < 0 or pp_N2 < 0:
      raise ModelStateException("Error in argument: negative pp is not allowed")
    else:
      self.pp_He = pp_He
      self.pp_N2 = pp_N2
      
  def const_depth(self, pp_He_inspired, pp_N2_inspired, seg_time):
    """Constant depth calculations. 
    Uses instananeous equation: P = Po + (Pi - Po)(1-e^-kt)
    pp_He_inspired : partial pressure of inspired helium
    pp_N2_inspired : partial pressure of inspired nitrogen
    seg_time : segment time in seconds
    store the new values in self.pp_He and self.pp_N2
    raise ModelStateException if pp or time < 0
    """
    if pp_He_inspired < 0 or pp_N2_inspired < 0 or seg_time < 0:
      raise ModelStateException("Error in argument: negative value is not allowed")
    else:
      new_pp_He = self.pp_He + ((pp_He_inspired - self.pp_He) * (1 - math.exp(-self.k_He*float(segTime)/60)))
      new_pp_N2 = self.pp_N2 + ((pp_N2_inspired - self.pp_N2) * (1 - math.exp(-self.k_N2*float(segTime)/60)))
      self.pp_He = new_pp_He
      self.pp_N2 = new_pp_N2
      
  def asc_desc(self, pp_He_inspired, pp_N2_inspired, rate_he, rate_n2, seg_time):
      """Ascend or descent calculations.
      Uses equation : P=Pio+R(t -1/k)-[Pio-Po-(R/k)]e^-kt
      pp_He_inspired : partial pressure of inspired helium
      pp_N2_inspired : partial pressure of inspired nitrogen
      rate_he : rate of change of pp_He
      rate_n2 : rate of change of pp_n2
      seg_time : segment time in seconds
      store the new values in self.pp_He and self.pp_N2
      raise ModelStateException if pp or time < 0
      """
      if pp_He_inspired < 0 or pp_N2_inspired < 0 or seg_time < 0:
        raise ModelStateException("Error in argument: negative value is not allowed")
      else:
        new_pp_He = pp_He_inspired + rate_he * (seg_time - (1.0/self.k_He)) - (pp_He_inspired - self.pp_He - (rate_he/self.k_He)) * math.exp(-self.k_He*float(seg_time)/60)
        new_pp_N2 = pp_N2_inspired + rate_n2 * (seg_time - (1.0/self.k_N2)) - (pp_N2_inspired - self.pp_N2 - (rate_n2/self.k_N2)) * math.exp(-self.k_N2*float(seg_time)/60)
        self.pp_He = new_pp_He
        self.pp_N2 = new_pp_N2
  
  