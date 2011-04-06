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
"""Oxygen Toxicity model
"""

__version__ = "0.1"

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

import math
import logging

class OxTox(object):
  """Defines a Oxygen Toxicity model
  
  Attributes:
  cns -- central nervous system toxicity 
         (see http://en.wikipedia.org/wiki/Oxygen_toxicity#Signs_and_symptoms)
  otu -- Oxygen toxicity Units
  max_ox -- maximum ppo2
  
  """
  
  def __init__(self):
    """Constructor for OxTox class
    
    Keyword arguments:
    <none>
    
    Returns:
    <nothing>

    """
    #initiate class logger
    self.logger = logging.getLogger("dipplanner.model.buhlmann.oxygen_toxicity.OxTox")
    self.logger.debug("creating an instance of Oxtox")
    
    self.cns = 0.0
    self.otu = 0.0
    self.max_ox = 0.0
    
  def add_O2(self, time, pp_O2):
    """Adds oxygen load into model. 
    Uses NOAA lookup table to add percentage based on time and ppO2.
    Calculate OTU using formula OTU= T * (0.5/(pO2-0.5))^-(5/6)
    this OTU formula need T (time) in minutes, so we need to convert the
    time in second to minutes while using this formula
    
    Keyword arguments:
    pp_O2 -- partial pressure of oxygen
    time -- time of segment (in seconds)
    
    Returns:
    <nothing>
    
    """
    if pp_O2 > 0.5:
      # only accumulate OTU for ppO2 > 0.5 atm
      diff_otu = (float(time)/60) * math.pow( (0.5 / ( pp_O2 - 0.5)), -0.833333)
      self.otu += diff_otu
      
    # CNS calculation
    if   pp_O2 > 1.8: exposure = 1
    elif pp_O2 > 1.7: exposure = 4
    elif pp_O2 > 1.6: exposure = 12
    elif pp_O2 > 1.5: exposure = 45
    elif pp_O2 > 1.4: exposure = 120
    elif pp_O2 > 1.3: exposure = 150
    elif pp_O2 > 1.2: exposure = 180
    elif pp_O2 > 1.1: exposure = 210
    elif pp_O2 > 1.0: exposure = 240
    elif pp_O2 > 0.9: exposure = 300
    elif pp_O2 > 0.8: exposure = 360
    elif pp_O2 > 0.7: exposure = 450
    elif pp_O2 > 0.6: exposure = 570
    elif pp_O2 > 0.5: exposure = 720
    else: exposure = 0
    
    if exposure > 0:
      self.cns += (float(time)/60) / exposure
    
    if pp_O2 > self.max_ox:
      self.max_ox = pp_O2
      
  def remove_O2(self, time):
    """Removes oxygen load from model during surface intervals
    
    Keyword arguments:
    time -- time of segment (in seconds)
    
    Returns:
    <nothing>
    
    """
    if time >= 86400:
      self.otu = 0.0
    old_cns = self.cns
    # decay cns with haltime of 90mins
    self.cns = self.cns * math.exp( -(float(time)/60) * 0.693147 / 90.0)
    