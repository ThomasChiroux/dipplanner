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
from model_exceptions import ModelStateException

class Compartment(object):
  """Buhlmann compartment class"""
  
  def __init__(self, h_He=None, h_N2=None, 
                     a_He=None, b_He=None, 
                     a_N2=None, b_N2=None):
    """Constructor for Compartment
    can be called without params, in this case, does not initiate anything
    can be called with time params and coef and in this case initate the
    compartment time constants
    
    Keyword arguments:
    Returns:
    Raise:
    see set_compartment_time_constants method
    """
    self.pp_He = 0.0
    self.pp_N2 = 0.0
    if h_He is not None and h_N2 is not None and \
       a_He is not None and b_He is not None and \
       a_N2 is not None and b_N2 is not None:
      self.set_compartment_time_constants(h_He, h_N2, a_He, b_He, a_N2, b_N2)
  
  
  def set_compartment_time_constants(self, h_He, h_N2, a_He, b_He, a_N2, b_N2):
    """Sets the compartment's time constants
    
    Keyword arguments:
    h_He -- Helium Halftime
    h_N2 -- Nitrogen Halftime
    a_He -- Helium : a coefficient
    b_He -- Helium : b coefficient
    a_N2 -- Nitrogen : a coefficient
    b_N2 -- Nitrogen : b coefficient
    
    Returns:
    <nothing>
    
    """
    self.k_He = math.log(2) / float(h_He)
    self.k_N2 = math.log(2) / float(h_N2)
    self.a_He = float(a_He) #/ 10
    self.b_He = float(b_He)
    self.a_N2 = float(a_N2) #/ 10
    self.b_N2 = float(b_N2)
    
  def set_pp(self, pp_He, pp_N2):
    """Sets partial pressures of He and N2
    
    Keyword arguments:
    pp_He -- partial pressure of Helium
    pp_N2 -- partial pressure of Nitrogen
    
    Return:
    <nothing>
    
    Raise:
    ModelStateException -- if pp < 0
    
    """
    if pp_He < 0.0 or pp_N2 < 0.0:
      raise ModelStateException("Error in argument: negative pp is not allowed")
    else:
      self.pp_He = float(pp_He)
      self.pp_N2 = float(pp_N2)
      
  def const_depth(self, pp_He_inspired, pp_N2_inspired, seg_time):
    """Constant depth calculations. 
    Uses instananeous equation: P = Po + (Pi - Po)(1-e^-kt)
    store the new values in self.pp_He and self.pp_N2
    
    Keyword arguments:
    pp_He_inspired -- partial pressure of inspired helium
    pp_N2_inspired -- partial pressure of inspired nitrogen
    seg_time -- segment time in seconds
    
    Return:
    <nothing>
    
    Raise:
    ModelStateException -- if pp or time < 0
    """
    if pp_He_inspired < 0 or pp_N2_inspired < 0 or seg_time < 0:
      raise ModelStateException("Error in argument: negative value is not allowed")
    else:
      new_pp_He = self.pp_He + ((pp_He_inspired - self.pp_He) * (1 - math.exp(-self.k_He*float(seg_time)/60)))
      new_pp_N2 = self.pp_N2 + ((pp_N2_inspired - self.pp_N2) * (1 - math.exp(-self.k_N2*float(seg_time)/60)))
      self.pp_He = new_pp_He
      self.pp_N2 = new_pp_N2
      
  def asc_desc(self, pp_He_inspired, pp_N2_inspired, rate_he, rate_n2, seg_time):
      """Ascend or descent calculations.
      Uses equation : P=Pio+R(t -1/k)-[Pio-Po-(R/k)]e^-kt
      store the new values in self.pp_He and self.pp_N2
      
      Keyword arguments:
      pp_He_inspired -- partial pressure of inspired helium
      pp_N2_inspired -- partial pressure of inspired nitrogen
      rate_he -- rate of change of pp_He
      rate_n2 -- rate of change of pp_n2
      seg_time -- segment time in seconds
      
      Return:
      <nothing>
      
      Raise:
      ModelStateException -- if pp or time < 0
      """
      if pp_He_inspired < 0 or pp_N2_inspired < 0 or seg_time < 0:
        raise ModelStateException("Error in argument: negative value is not allowed")
      else:
        new_pp_He = pp_He_inspired + rate_he * (float(seg_time)/60 - (1.0/self.k_He)) - (pp_He_inspired - self.pp_He - (rate_he/self.k_He)) * math.exp(-self.k_He*float(seg_time)/60)
        new_pp_N2 = pp_N2_inspired + rate_n2 * (float(seg_time)/60 - (1.0/self.k_N2)) - (pp_N2_inspired - self.pp_N2 - (rate_n2/self.k_N2)) * math.exp(-self.k_N2*float(seg_time)/60)
        self.pp_He = new_pp_He
        self.pp_N2 = new_pp_N2
  
  def _calculate_p_a_b_inert(self):
    """Calculate and returns p_He_N2, a_He_N2 and b_He_N2
    
    Keyword arguments:
    <none>
    
    Returns:
    3 float values : p_He_N2, a_He_N2 and b_He_N2
    """
    p_He_N2 = self.pp_He + self.pp_N2
    # calculate adjusted a, b coefficients based on those of He and N2
    a_He_N2 = ((self.a_He * self.pp_He) + (self.a_N2 * self.pp_N2)) / p_He_N2
    b_He_N2 = ((self.b_He * self.pp_He) + (self.b_N2 * self.pp_N2)) / p_He_N2
    return p_He_N2, a_He_N2, b_He_N2
    
  def get_m_value_at(self, pressure):
    """Gets M-Value for given ambient pressure uning the Buhlmann equation
    Pm = Pa/b +a         where: Pm = M-Value pressure,
                                Pa = ambiant pressure
                                a,b co-efficients
    Not used for decompression but for display of M-value limit line
    Note that this does not factor gradient factors.
    
    Keyword arguments:
    pressure -- ambient pressure (in bar)
    
    Return:
    float, M_value : maximum tolerated pressure in bar
    
    """
    p_He_N2, a_He_N2, b_He_N2 = self._calculate_p_a_b_inert()
    return float(pressure) / b_He_N2 + a_He_N2
    
  def get_max_amb(self, gf):
    """Gets Tolerated Absolute Pressure for the compartment
    
    Keyword arguments:
    gf -- gradient factor : 0.1 to 1.0, typical 0.2 - 0.95
    
    Return:
    float, maximum tolerated pressure in bar
    
    """
    p_He_N2, a_He_N2, b_He_N2 = self._calculate_p_a_b_inert()
    #TODO: il y a un pb avec cette formule ou cette fonction : elle 
    #      retourne (selon les cas) des valeurs négatives (si p_He_N2 < a_He_N2)
    #      et cela ne me parrait pas logique ni normal
    max_amb = (p_He_N2 - a_He_N2 * gf) / (gf / b_He_N2 - gf + 1.0)
    #max_amb = (p_He_N2 - a_He_N2 ) /  b_He_N2 
    return max_amb
    
  def get_mv(self, p_amb):
    """Gets M-Value for a compartment, given an ambient pressure
    
    Keyword arguments:
    p_amb -- ambiant pressure
    
    Return:
    float, M-value
    
    """
    p_He_N2, a_He_N2, b_He_N2 = self._calculate_p_a_b_inert()
    return p_He_N2 / (float(p_amb) / b_He_N2 + a_He_N2)