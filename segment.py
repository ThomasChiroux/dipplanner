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
"""Segment classes
A segment is a portion of a dive in the same depth (depth + duration)
"""

__version__ = "0.1"

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

# local import
import settings

class SegmentException(Exception):
  """Base exception class for this module
  """
  def __init__(self, description):
    self.description = description
  
  def __str__(self):
    return repr(self.description)


class UnauthorizedMod(SegmentException):
  """raised when the MOD is not possible according to the 
  depth(s) of the segment"""
  pass

class Segment(object):
  """Base class for all types of segments"""
  
  def __init__(self):
    """constructor for Segment base class, just defines all the parameters
    the type of segment can be:
      'const' : constant depth
      'ascent' : ascent
      'descent' : descednt
      'deco' : deco
      'waypoint' : waypoint (TODO: c'est quoi ?)
      'surf'  : surface
    """
    self.type = None # type of segment : base class has no type
    self.in_use = True # is this segment in use : default: yes
    self.depth = 0.0 # depth of this segment, in meter
    self.time = 0.0 # time of this segment, in second
    self.run_time = 0.0 # runtime in profile (TODO: voir a quoi ça sert)
    self.setpoint = 0.0 # for CCR
    self.tank = None # tank used for this segment
  
  def check_mod(self):
    """checks the mod for this segment according to the used tank.
    checks both Max Operating Depth and Min Operating Depth (hypoxic cases)
    if problem, raise UnauthorizedMod
    """
    if self.depth > self.tank.get_mod():
      raise UnauthorizedMod("depth is exceeding the maximum MOD")
    if self.depth < self.tank.get_min_od(): # checks minimum operating depth
      raise UnauthorizedMod("depth is too low for the minimum MOD")
    
  def get_p_absolute(self, method='simple'):
    """returns the absolute pression in bar
    (1atm = 1ATA = 1.01325 bar = 14.70psi)
    Simple method : 10m = +1 bar
    "complex method" : use real density of water, T°, etc...: need more parameters
    today: only simple method
    """
    return self.depth/10 + settings.AMBIANT_PRESSURE_SURFACE
    
  def get_end(self):
    """Calculates and returns E.N.D :
    Equivalent Narcosis Depth
    Instead of Mvplan, it uses a 'calculation method' based on 
    nacosys effet of all gas used, assuming there is no trace of
    other gases (like argon)
    """
    p_absolute = self.get_p_absolute()
    # calculate the reference narcotic effect of air
    # Air consists of: Nitrogen N2: 78.08%, Oxygen O2: 20.95%, Argon Ar: 0.934%
    # TODO: at 1 bar or at AMBIANT_PRESSURE_SURFACE bar ??
    #reference_narcotic = n2_narcotic * 0.7808 + \
    #                     o2_narcotic * 0.2095 + \
    #                     ar_narcotic * 0.00934
    reference_narcotic = settings.N2_NARCOTIC_VALUE * 0.79 + \
                        settings.O2_NARCOTIC_VALUE * 0.21

    if self.setpoint > 0:
      #CCR mode
      # TODO: change this to a 'real' calculation based on narcotic effet of
      #       all gases
      if (self.tank.f_He + self.tank.f_N2) > 0:
        p_inert = p_absolute - self.setpoint * 10
      else:
        p_inert = 0
      if p_inert > 0:
        ppn2_inspired = (p_inert * self.tank.f_N2) / (self.tank.f_He + self.tank.f_N2)
      else:
        narcotic_index = 0
    else:
      #OC mode
      # only N2 is narcotic
      #ppn2_inspired = self.tank.f_N2 * p_absolute
      
      narcotic_index = p_absolute * \
                       (self.tank.f_N2 * settings.N2_NARCOTIC_VALUE + \
                        self.tank.f_O2 * settings.O2_NARCOTIC_VALUE + \
                        self.tank.f_He * settings.HE_NARCOTIC_VALUE)
    end = int((narcotic_index / reference_narcotic - 1) * 10)
    return end
    
  def gas_used(self):
    """returns the quantity (in liter) of gas used for this segment"""
    pass
    
  def __repr__(self):
    """Returns a string representing the actual segment"""
    return "%s: for %ss at %sm on %s, SP:%s, END:%sm" % ( self.type.upper(),
                                                  self.time,
                                                  self.depth,
                                                  str(self.tank),
                                                  self.setpoint,
                                                  self.get_end() )
    
  def __str__(self):
    return self.__repr__()
    
  def __unicode__(self):
    return u"%s" % self.__repr__()
    
class SegmentDive(Segment):
  """Specialisation of segment class for dive segments
  """
  def __init__(self, depth, time, tank, setpoint = 0):
    """Constructor for SegmentDive class. Look at base class for
    more explanations"""
    self.type = 'const' # type of segment
    self.in_use = True # is this segment in use : default: yes
    self.depth = depth # depth of this segment, in meter
    self.time = time # time of this segment, in second
    
    self.setpoint = setpoint # for CCR
    self.tank = tank # tank used for this segment

    self.check_mod()
    
  def gas_used(self):
    """returns the quantity (in liter) of gas used for this segment"""
    if self.setpoint > 0 :
      return 0
    else:
      pressure = (self.depth/10 + settings.AMBIANT_PRESSURE_SURFACE)
      return ( pressure * self.time * float(settings.DIVE_CONSUMPTION_RATE)/60 )
    
class SegmentDeco(Segment):
  """Specialisation of segment class for deco segments
  """
  def __init__(self, depth, time, tank, setpoint = 0):
    """Constructor for SegmentDeco class. Look at base class for
    more explanations
    In deco segment, we also have to manage some new parameters :
    - gf_used
    - control_compartment
    - mv_max (max M-value for the compartment)
    """
    self.type = 'deco' # type of segment
    self.in_use = True # is this segment in use : default: yes
    self.depth = float(depth) # depth of this segment, in meter
    self.time = float(time) # time of this segment, in second
    
    self.setpoint = float(setpoint) # for CCR
    self.tank = tank # tank used for this segment

    # other parameters used in deco mode
    self.gf_used = 0 # wich gradient factor is used
    self.control_compartment = None # who is the control compartement
    self.mv_max = 0 # maximum M-Value gradient for the compartment
    
    self.check_mod()

  def gas_used(self):
    """returns the quantity (in liter) of gas used for this segment"""
    if self.setpoint > 0 :
      return 0
    else:
      pressure = (float(self.depth)/10 + settings.AMBIANT_PRESSURE_SURFACE)
      return ( pressure * self.time * float(settings.DECO_CONSUMPTION_RATE)/60 )

class SegmentAscDesc(Segment):
  """Specialisation of segment class for Ascent or Descent segments
  """
  def __init__(self, start_depth, end_depth, rate, tank, setpoint = 0):
    """Constructor for SegmentAscDesc class. Look at base class for
    more explanations
    in this segment, we do not specify time, but rate (of ascending 
    or descending) and start_depth and end_depth
    The comparaison between start and end depth determine if asc or desc
    rate is given in m/min
    """
    
    self.in_use = True # is this segment in use : default: yes
    self.depth = float(end_depth) # depth of this segment, in meter
    self.time = float(60) * (abs(float(end_depth) - float(start_depth)) / float(rate))
    self.rate = float(rate)
    self.start_depth = float(start_depth)
    self.end_depth = float(end_depth)
    self.setpoint = float(setpoint) # for CCR
    self.tank = tank # tank used for this segment
    if start_depth > end_depth:
      self.type = 'ascent' # type of segment
    else:
      self.type = 'descent'
    
    self.check_mod()
      
  def check_mod(self):
    """checks the mod for this segment according to the used tank.
    checks both Max Operating Depth and Min Operating Depth (hypoxic cases)
    if problem, raise UnauthorizedMod
    """
    if self.type == 'ascent':
      max_depth = self.start_depth
      min_depth = self.end_depth
    else:
      min_depth = self.start_depth
      max_depth = self.end_depth

    if max_depth > self.tank.get_mod():
      raise UnauthorizedMod("depth is exceeding the maximum MOD")
    if min_depth < self.tank.get_min_od(): # checks minimum operating depth
      raise UnauthorizedMod("depth is too low for the minimum MOD")

  def gas_used(self):
    """returns the quantity (in liter) of gas used for this segment
    because it's ascend or descent, the gas is not used at the same rate
    during the segment
    Because the rate is the same during all the segment, we can use the
    consumption at the average depth of the segment
    """
    if self.setpoint > 0 :
      return 0
    else:
      average_depth = (self.start_depth + self.end_depth) / 2.0
      pressure = (average_depth/10 + settings.AMBIANT_PRESSURE_SURFACE)
      return ( pressure * self.time * float(settings.DIVE_CONSUMPTION_RATE)/60 )
