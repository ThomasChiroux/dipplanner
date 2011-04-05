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
"""Buhlmann model module

Contains:
Model -- class
"""

__version__ = "0.1"

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

import logging
# local imports
import settings
from model_exceptions import ModelStateException
from compartment import Compartment
from gradient import Gradient
from oxygen_toxicity import OxTox

class Model(object):
  """Represents a Buhlmann model.
  Composed of a tissue array of Compartment[]
  Has an OxTox and Gradient object
  Can throw a ModelStateException propagated from a Compartment if pressures 
  or time is out of bounds.
   
  Models are initialised by initModel() if they are new models, or
  validated by validateModel() if they are rebuild from a saved model.
   
  The model is capable of ascending or descending via ascDec() using the 
  ascDec() method of Compartment,
  or accounting for a constant depth using the 
  constDepth() method of Compartment.
 
  Attributes:
  tissues -- a list of Compartments
  gradient -- gradient factor object
  ox_tox -- OxTox object
  metadata -- Stores information about where the model was created
  units -- only 'metric' allowed
  COMPS -- static info : number of compartments
  MODEL_VALIDATION_SUCCESS -- static const for success of validation
  MODEL_VALIDATION_FAILURE -- sattic const for failure of validation
  """
  COMPS = 16
  
  #TODO: SUPPRIMER CES DEUX ELEMENTS ET REMPLACER PAR DES RAISE
  MODEL_VALIDATION_SUCCESS = 1
  MODEL_VALIDATION_FAILURE = 0
  
  def __init__(self):
    """Constructor for model class
    
    Keyword arguments:
    <none>
    
    Returns:
    <nothing>
    
    """
    #initiate class logger
    self.logger = logging.getLogger("dipplanner.model.buhlmann.model.Model")
    self.logger.info("creating an instance of Model")
    
    self.units = 'metric'
    self.tissues = []
    self.ox_tox = OxTox()
    self.init_gradient()

    for comp_number in range(0, self.COMPS):
      comp = Compartment()
      comp.set_pp(0.0, 0.79 * (settings.AMBIANT_PRESSURE_SURFACE - \
                               settings.PP_H2O_SURFACE))
      self.tissues.append(comp)
    
    self.set_time_constants()
    self.metadata = "(none)"

  def __repr__(self):
    """Returns a string representing the model"""
    model_string = "Compartment pressures:\n"
    for comp_number in range(0, self.COMPS):
         model_string += "C:%s He:%s N2:%s gf:%s mv_at:%s max_amb:%s MV:%s\n" % (
          comp_number,
          self.tissues[comp_number].pp_He,
          self.tissues[comp_number].pp_N2,
          self.gradient.gf,
          self.tissues[comp_number].get_m_value_at(settings.AMBIANT_PRESSURE_SURFACE),
          (self.tissues[comp_number].get_max_amb(self.gradient.gf)) * 1,
          self.tissues[comp_number].get_mv(settings.AMBIANT_PRESSURE_SURFACE)
         )
    model_string += "Ceiling: %s\n" % self.ceiling()
    model_string += "Max surface M-Value: %s\n" % self.m_value(0.0)
    model_string += "OTUs accumulated: %s" % self.ox_tox.otu
    return model_string

  def __str__(self):
    """Return a human readable name of the segment"""
    return self.__repr__()

  def __unicode__(self):
    """Return a human readable name of the segment in unicode"""
    return u"%s" % self.__repr__()

  def init_gradient(self):
    """Initialise the gradient attribute
    uses the default settings parameters for gf_low and high
    
    Keyword arguments:
    <none>
    
    Returns:
    <nothing>
    
    """
    self.gradient = Gradient(settings.GF_LOW, settings.GF_HIGH)
    
  def set_time_constants(self):
    """Initialize time constants in buhmann tissue list
    Only for metric values
    
    Keyword arguments:
    <none>
    
    Returns:
    <nothing>
    """
    # note: comparing with buhlmann original (1990) ZH-L16 a coeficient,
    # there is here a x10 factor for a coeficient
    self.tissues[0].set_compartment_time_constants(1.88,    5.0,    16.189, 0.4770, 11.696, 0.5578);         
    self.tissues[1].set_compartment_time_constants(3.02,    8.0,    13.83,  0.5747, 10.0,   0.6514);
    self.tissues[2].set_compartment_time_constants(4.72,    12.5,   11.919, 0.6527, 8.618,  0.7222);
    self.tissues[3].set_compartment_time_constants(6.99,    18.5,   10.458, 0.7223, 7.562,  0.7825);
    self.tissues[4].set_compartment_time_constants(10.21,   27.0,   9.220,  0.7582, 6.667,  0.8126);
    self.tissues[5].set_compartment_time_constants(14.48,   38.3,   8.205,  0.7957, 5.60,   0.8434);
    self.tissues[6].set_compartment_time_constants(20.53,   54.3,   7.305,  0.8279, 4.947,  0.8693);
    self.tissues[7].set_compartment_time_constants(29.11,   77.0,   6.502,  0.8553, 4.5,    0.8910);
    self.tissues[8].set_compartment_time_constants(41.20,   109.0,  5.950,  0.8757, 4.187,  0.9092);
    self.tissues[9].set_compartment_time_constants(55.19,   146.0,  5.545,  0.8903, 3.798,  0.9222);
    self.tissues[10].set_compartment_time_constants(70.69,  187.0,  5.333,  0.8997, 3.497,  0.9319);
    self.tissues[11].set_compartment_time_constants(90.34,  239.0,  5.189,  0.9073, 3.223,  0.9403);
    self.tissues[12].set_compartment_time_constants(115.29, 305.0,  5.181,  0.9122, 2.850,  0.9477);
    self.tissues[13].set_compartment_time_constants(147.42, 390.0,  5.176,  0.9171, 2.737,  0.9544);
    self.tissues[14].set_compartment_time_constants(188.24, 498.0,  5.172,  0.9217, 2.523,  0.9602);
    self.tissues[15].set_compartment_time_constants(240.03, 635.0,  5.119,  0.9267, 2.327,  0.9653);
    
  def validate_model(self):
    """Validate model - checks over the model and looks for corruption
    This is needed to chack a model that has been loaded from XML
    Resets time constants
    
    Keyword arguments:
    <none>
    
    Returns:
    self.MODEL_VALIDATION_SUCCESS -- if OK
    self.MODEL_VALIDATION_FAILURE -- if not OK
    
    """
    time_constant_zero = False # need for resetting time constants
    
    for comp in self.tissues:
      if comp.pp_N2 <= 0.0:
        return self.MODEL_VALIDATION_FAILURE
      if comp.pp_He < 0.0:
        return self.MODEL_VALIDATION_FAILURE
      if comp.k_He == 0.0 or \
         comp.k_N2 == 0.0 or \
         comp.a_He == 0.0 or \
         comp.b_He == 0.0 or \
         comp.a_N2 == 0.0 or \
         comp.b_N2 == 0.0:
        time_constant_zero = True
    if time_constant_zero:
      self.set_time_constants()
    return self.MODEL_VALIDATION_SUCCESS
    
  def control_compartment(self):
    """Determine the controlling compartment at ceiling (1-16)
    
    Keyword arguments:
    <none>
    
    Returns:
    Integer : reference number of the controlling compartment (between 1 to 16)
    
    """
    control_compartment_number = 0
    max_pressure = 0.0
    
    for comp_number in range(0, self.COMPS):
      pressure = self.tissues[comp_number].get_max_amb(self.gradient.gf) - settings.AMBIANT_PRESSURE_SURFACE
      self.logger.debug("pressure:%s" % pressure)
      if pressure > max_pressure:
        control_compartment_number = comp_number
        max_pressure = pressure
    return control_compartment_number + 1
    
  def ceiling(self):
    """Determine the current ceiling depth
    
    Keyword arguments:
    <none>
    
    Returns:
    Float, ceiling depth in meter
    
    """
    pressure = 0.0
    
    for comp in self.tissues:
      #Get compartment tolerated ambient pressure and convert from absolute
      #pressure to depth
      comp_pressure = comp.get_max_amb(self.gradient.gf) - settings.AMBIANT_PRESSURE_SURFACE
      if comp_pressure > pressure:
        pressure = comp_pressure
    return pressure*10
    
  def m_value(self, pressure):
    """Determine the maximum M-Value for a given depth (pressure)
    
    Keyword arguments:
    pressure -- in bar
    
    Returns
    float, max M-Value
    
    """
    p_absolute = pressure + settings.AMBIANT_PRESSURE_SURFACE
    compartment_mv = 0.0
    max_mv = 0.0
    
    for comp in self.tissues:
      compartment_mv = comp.get_mv(p_absolute)
      if compartment_mv > max_mv:
        max_mv = compartment_mv
    self.logger.debug("max mv : %s" % max_mv)
    return max_mv
    
  def const_depth(self, pressure, seg_time, f_He, f_N2, pp_O2):
    """Constant depth profile. 
    Calls Compartment.constDepth for each compartment to update the model.
    
    Kerword arguments:
    pressure -- pressure of this depth of segment in bar
    seg_time -- Time of segment in seconds
    f_He -- Fraction of inert gas Helium in inspired gas mix
    f_N2 -- Fraction of inert gas Nitrogen in inspired gas mix
    pp_O2 -- For CCR mode, partial pressure of oxygen in bar. 
             If == 0.0, then open circuit
             
    Returns:
    <nothing>
    
    Raise:
    ModelStateException
    
    """
    ambiant_pressure = pressure + settings.AMBIANT_PRESSURE_SURFACE
    if pp_O2 > 0.0:
      # CCR mode
      #Determine pInert by subtracting absolute oxygen pressure and pH2O
      #Note that if fHe and fN2 == 0.0 then need to force pp's to zero
      if f_He + f_N2 > 0.0:
        p_inert = ambiant_pressure - pp_O2 - settings.PP_H2O_SURFACE
      else:
        p_inert = 0.0
        
      #Verify that pInert is positive. If the setpoint is close to or less 
      # than the depth then there is no inert gas.
      if p_inert > 0.0:
        pp_He_inspired = (p_inert * f_He) / (f_He + f_N2)
        pp_N2_inspired = (p_inert * f_N2) / (f_He + f_N2)
      else:
        pp_He_inspired = 0.0
        pp_N2_inspired = 0.0
      
      # update OxTox object
      pp_O2_inspired = pp_O2
      #Check that ppO2Inspired is not greater than the depth. 
      #This occurs in shallow deco when the setpoint specified is > depth
      if pp_O2_inspired <= ambiant_pressure and p_inert > 0.0:
        # pp_O2 is the setpoint
        self.ox_tox.add_O2(seg_time, pp_O2)
      else:
        # pp_O2 is equal to the depth, also true is there is no inert gaz
        self.ox_tox.add_O2(seg_time, ambiant_pressure - settings.PP_H2O_SURFACE)
    else:
      # OC mode
      pp_He_inspired = (ambiant_pressure - settings.PP_H2O_SURFACE) * f_He
      pp_N2_inspired = (ambiant_pressure - settings.PP_H2O_SURFACE) * f_N2
      # update ox_tox
      if pressure == 0.0: #surface
        self.ox_tox.remove_O2(seg_time)
      else:
        self.ox_tox.add_O2(seg_time, (ambiant_pressure \
                                      - settings.PP_H2O_SURFACE) \
                                     * (1.0 - f_He - f_N2))
    if seg_time > 0:
      for comp in self.tissues:
        comp.const_depth(pp_He_inspired, pp_N2_inspired, seg_time)
        
  def asc_desc(self, start, finish, rate, f_He, f_N2, pp_O2):
    """Ascend/Descend profile. 
    Calls Compartment.asc_desc to update compartments

    Kerword arguments:
    start -- start pressure of this segment in bar (WARNING: not meter !)
    finish -- finish pressure of this segment in bar (WARNING: not meter !) 
    rate -- rate of ascent or descent in m/s
    f_He -- Fraction of inert gas Helium in inspired gas mix
    f_N2 -- Fraction of inert gas Nitrogen in inspired gas mix
    pp_O2 -- For CCR mode, partial pressure of oxygen in bar. 
             If == 0.0, then open circuit

    Returns:
    <nothing>

    Raise:
    ModelStateException

    """
    # rem: here we do not bother of PP_H2O like in constant_depth : WHY ?
    start_ambiant_pressure = start + settings.AMBIANT_PRESSURE_SURFACE
    finish_ambiant_pressure = finish + settings.AMBIANT_PRESSURE_SURFACE
    seg_time = abs(float(finish) - float(start)) / rate
    if pp_O2 > 0.0:
      # CCR mode
      # Calculate inert gas partial pressure == pAmb - pO2 - pH2O 
      p_inert_start = start_ambiant_pressure - pp_O2 - settings.PP_H2O_SURFACE
      p_inert_finish = finish_ambiant_pressure - pp_O2 - settings.PP_H2O_SURFACE
      # Check that it doesn't go less than zero. 
      # Could be due to shallow deco or starting on high setpoint
      if p_inert_start < 0.0:
        p_inert_start = 0.0
      if p_inert_finish < 0.0:
        p_inert_finish = 0.0
      # Separate into He and N2 components, checking that we are not 
      # on pure O2 (or we get an arithmetic error)
      if f_He + f_N2 > 0.0:
        pp_He_inspired = (p_inert_start * f_He) / (f_He + f_N2)
        pp_N2_inspired = (p_inert_start * f_N2) / (f_He + f_N2)
        # calculate rate of change of each inert gas
        rate_He = ((p_inert_finish * f_He) / (f_He + f_N2) - pp_He_inspired) \
                  / (seg_time)
        rate_N2 = ((p_inert_finish * f_N2) / (f_He + f_N2) - pp_N2_inspired) \
                  / (seg_time)
      else:
        pp_He_inspired = 0.0
        pp_N2_inspired = 0.0
        rate_He = 0.0
        rate_N2 = 0.0
      # update ox_tox, constant pp_O2
      # TODO - what if depth is less than pO2 in msw ?
      self.ox_tox.add_O2(seg_time, pp_O2)
    else:
      # OC mode
      # calculate He and N2 components
      pp_He_inspired = (start_ambiant_pressure - settings.PP_H2O_SURFACE) * f_He
      pp_N2_inspired = (start_ambiant_pressure - settings.PP_H2O_SURFACE) * f_N2
      rate_He = rate * f_He
      rate_N2 = rate * f_N2
      # update ox_tox, use average pp_O2
      pp_O2_inspired_avg = ((start_ambiant_pressure - finish_ambiant_pressure) / 2 \
                           + finish_ambiant_pressure - settings.PP_H2O_SURFACE) \
                           * (1.0 - f_He - f_N2)
      self.ox_tox.add_O2(seg_time, pp_O2_inspired_avg)
    
    for comp in self.tissues:
      comp.asc_desc(pp_He_inspired, pp_N2_inspired, rate_He, rate_N2, seg_time)
    
                  