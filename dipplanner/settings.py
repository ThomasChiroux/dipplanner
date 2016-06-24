#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2011-2012 Thomas Chiroux
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
"""Global settings for dipplannerand their default values

All the settings can be changed by :ref:`dipplanner_cmdline`
and/or :ref:`dipplanner_configfile`
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]

# ======= "Internal" Settings ========
# software version, populated automatically
__VERSION__ = None

#: unless knowing what you're doing, this prefs should not be changed
#: by the user

FRESH_WATER_DENSITY = 1.0  #: water density kg/l
SEA_WATER_DENSITY = 1.03  #: water density kg/l
ABSOLUTE_MAX_PPO2 = 2.0  #: in bar
ABSOLUTE_MIN_PPO2 = 0.16  #: in bar
ABSOLUTE_MAX_TANK_PRESSURE = 300  #: in bar
ABSOLUTE_MAX_TANK_SIZE = 2 * 20  #: in liter

#: Temperature at surface.
#: Used to calculate PP_H2O_SURFACE
SURFACE_TEMP = 20

HE_NARCOTIC_VALUE = 0.23  #: helium narcotic value
N2_NARCOTIC_VALUE = 1.0  #: nitrogen narcotic value
O2_NARCOTIC_VALUE = 1.0  #: oxygen narcotic value
AR_NARCOTIC_VALUE = 2.33  #: argon narcotic value

STOP_DEPTH_INCREMENT = 3  #: in meter
LAST_STOP_DEPTH = 3  #: in meter : last stop before surfacing
STOP_TIME_INCREMENT = 1  #: in second

#: once deco stop begun, force to stop to each deco
#: depth stop
FORCE_ALL_STOPS = True

AMBIANT_PRESSURE_SEA_LEVEL = 1.01325  #: surface pressure (in bar)
METHOD_FOR_DEPTH_CALCULATION = 'complex'  #: either simple (/10) or complex

TRAVEL_SWITCH = 'late'  #: "late" or "early"

#: in meter practicly, this value can not be bigger than
#: about 2850m because breathing air at 0m will only
#: 'prepare the body' to a decompression until this
#: value. To go higher, another 'stop' is needed
#: between.
FLIGHT_ALTITUDE = 2450

# ========= User settings ========
TEMPLATE = "default-color.tpl"  #: template should be in templates/ directory

DECO_MODEL = "ZHL16c"  #: ZHL16c or ZHL16b

WATER_DENSITY = SEA_WATER_DENSITY  #: water density kg/l

#: surface pressure (in bar)
AMBIANT_PRESSURE_SURFACE = AMBIANT_PRESSURE_SEA_LEVEL

DEFAULT_MAX_PPO2 = 1.6  #: in bar
DEFAULT_MIN_PPO2 = 0.21  #: in bar
DEFAULT_MAX_END = 30  #: in meter

DIVE_CONSUMPTION_RATE = 17.0 / 60  #: liter/s
DECO_CONSUMPTION_RATE = 12.0 / 60  #: liter/s

DESCENT_RATE = float(20) / 60  #: m/s
ASCENT_RATE = float(10) / 60  #: m/s

#: Warning : if RUN-TIME is True, the segment duration must
#:           include descent time
#: if the duration is too small dipplanner will raise an error
#: if True: segments represents runtime,
#: if false, segments represents segtime
RUN_TIME = True

USE_OC_DECO = True  #: if True, use enabled gases of decomp in oc or bailout

GF_LOW = 0.30  #: % between 0.0 and 1.0
GF_HIGH = 0.80  #: % between 0.0 and 1.0

# TODO: check the usage of the MULTILEVEL_MODE setting
MULTILEVEL_MODE = False  #: TO CHECK

AUTOMATIC_TANK_REFILL = True  #: automatic refill of tanks between dives
