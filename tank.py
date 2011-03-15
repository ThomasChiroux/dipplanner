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
Contains a Tank Class
in MVPlan, this class was the 'Gas' class

TODO:
 - handle double tanks, connected or not
 - minimum gas remaining in tank ? (ie/ 50 bar mini ??)
"""

__version__ = "0.1"

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

ABSOLUTE_MAX_PPO2 = 2
DEFAULT_MAX_PPO2 = 1.6
ABSOLUTE_MIN_PPO2 = 0.16
DEFAULT_MIN_PPO2 = 0.16
ABSOLUTE_MAX_TANK_PRESSURE = 300 # in bar
ABSOLUTE_MAX_TANK_SIZE = 30 # in liter

class TankException(Exception):
  """Base exception class for this module
  """
  pass
  
class InvalidGas(TankException):
  """Exception raised when the gas informations provided for the Tank
  are invalid
  """
  pass

class InvalidTank(TankException):
  """Exception raised when the tank infos provided are invalid
  """
  pass
  
class InvalidMod(TankException):
  """Exception raised when the given MOD is incompatible with the gas
  provided for the tank
  """
  pass
  
class EmptyTank(TankException):
  """Exception raised when trying to consume more gas in tank than the
  remaining gas
  """
  pass
  
class Tank(object):
  """This class implements a representation of dive tanks wich 
  contains breathing Gas
  We provide proportion of N2, O2, He, calculates MOD and volumes during the
  dives
  We can also (optionnaly) provide the type of tanks : volume and pressure
  """
  
  def __init__(self,  f_O2=0.21, f_He=0, max_ppo2=DEFAULT_MAX_PPO2, mod=None,
                      tank_vol=12, tank_pressure=200):
    """Constructor for Tank class
    If nothing is provided, create a default 'Air' with 12l/200b tank
    and max_ppo2 to 1.6 (used to calculate mod)
    if mod not provided, mod is calculed based on max tolerable ppo2
    """
    self.f_O2 = f_O2
    self.f_He = f_He
    self.f_N2 = 1 - (self.f_O2 + self.f_He)
    self.max_ppo2 = max_ppo2
    self.tank_vol = tank_vol
    self.tank_pressure = tank_pressure
    if mod:
      self.mod = mod
    else:
      self.mod = self._calculate_mod(self.max_ppo2)
    
    self.in_use = True
  
    self.used_gas = 0
    if self.tank_vol and self.tank_pressure:
      self.total_gas = self.tank_vol*self.tank_pressure
    else:
      self.total_gas = 0
    self.remaining_gas = self.total_gas

    self._validate()

  def __repr__(self):
    """Returns a string representing the actual tank"""
    return "%s - %s" % (self.name(), self.get_tank_info())
    
  def __str__(self):
    """Return a human readable name of the tank"""
    return "%s" % self.name()
    
  def __unicode__(self):
    """Return a human readable name of the tank in unicode"""
    return u"%s" % self.name()
    
  def __cmp__(self, othertank):
    """Compare a tank to another tank, based on MOD"""
    return cmp(self.mod, othertank.mod)
    
  def _calculate_mod(self, max_ppo2):
    """calculate and returns mod for a given ppo2 based on this tank info
    result in meter
    """
    return int(10*(max_ppo2/self.f_O2)-10)
    
  def _validate(self):
    """Test the validity of the tank informations
    if validity check fails raise an Exception 'InvalidTank'
    """
    if self.f_O2 + self.f_He > 1:
      raise InvalidGas
    
    if self.mod > self._calculate_mod(self.max_ppo2) or \
       self.mod > self._calculate_mod(ABSOLUTE_MAX_PPO2):
      raise InvalidMod
    
    if self.tank_pressure > ABSOLUTE_MAX_TANK_PRESSURE: #no pressure > xxxbars
      raise InvalidTank
    if self.tank_vol > ABSOLUTE_MAX_TANK_SIZE: #no tank larger than xxliter
      raise InvalidTank
    
  def name(self):
    """returns a Human readable name for the gaz and tanks
    Differnt possibilities:
    Air, Nitrox, Oxygen, Trimix, Heliox
    """
    name = 'Air'
    composition = ''
    if self.f_He == 0:
      composition = '%s' % int(self.f_O2*100)
      if self.f_O2 == 0.21:
        name = 'Air'
      elif self.f_O2 == 1:
        name = 'Oxygen'
      else:
        name = 'Nitrox ' + composition
    else:
      composition = '%s/%s' % (int(self.f_O2*100), int(self.f_He*100))
      if self.f_He + self.f_O2 == 1:
        name = 'Heliox ' + composition
      else:
        name = 'Trimix ' + composition
    return name
  
  def get_tank_info(self):
    """returns tank infos : size, remaining vol
    example of tank info: 
    15l-90% (2800/3000l)
    """
    if self.total_gas > 0:
      return "%sl-%s%% (%s/%sl)" % (self.tank_vol, 
                                 int(100*self.remaining_gas/self.total_gas),
                                 self.remaining_gas,
                                 self.total_gas)
    else:
      return "(no tank info, used:%sl)" % self.used_gas
      
  def get_mod(self, max_ppo2=None):
    """return mod in meter
    if no argument provided, return the mod based on the current tank (and 
    configured max_ppo2)
    if max_ppo2 is provied, returns the (new) mod based on the given ppo2
    """
    if not max_ppo2:
      return self.mod
    else:
      return self._calculate_mod(max_ppo2)
  
  def get_min_od(self, min_ppo2=ABSOLUTE_MIN_PPO2):
    """return in meter the minimum operating depth for the gas in the tank
    return 0 if diving from/to surface is ok with this gaz
    """
    return self._calculate_mod(min_ppo2)
    
  def consume_gas(self, gas_consumed):
    """Consume gas inside this tank
    take one argument : gas_consumed, in liter
    return EmptyTank Exception if all the gas is consumed
    return remaining gaz in tank (in liter) in other cases
    """
    if self.remaining_gas - gas_consumed < 0:
      raise EmptyTank
    else:
      self.used_gas += gas_consumed
      self.remaining_gas -= gas_consumed
      return self.remaining_gas