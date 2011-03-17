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
"""Global settings for dipplanner
"""

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

# water density kg/l
FRESH_WATER_DENSITY = 1.0
SEA_WATER_DENSITY = 1.03
WATER_DENSITY = SEA_WATER_DENSITY 

ABSOLUTE_MAX_PPO2 = 2.0
DEFAULT_MAX_PPO2 = 1.6
ABSOLUTE_MIN_PPO2 = 0.16
DEFAULT_MIN_PPO2 = 0.16
ABSOLUTE_MAX_TANK_PRESSURE = 300 # in bar
ABSOLUTE_MAX_TANK_SIZE = 30 # in liter

AMBIANT_PRESSURE_SURFACE = 1.0 # surface pressure (in bar)
DIVE_CONSUMPTION_RATE = 17 # liter/minute
DECO_CONSUMPTION_RATE = 12 # liter/minute

HE_NARCOTIC_VALUE = 0.23
N2_NARCOTIC_VALUE = 1.0
O2_NARCOTIC_VALUE = 1.0
AR_NARCOTIC_VALUE = 2.33