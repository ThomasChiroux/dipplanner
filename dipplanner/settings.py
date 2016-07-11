#
# Copyright 2011-2016 Thomas Chiroux
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
"""Global settings for dipplannerand their default values.

All the settings can be changed by :ref:`dipplanner_cmdline`
and/or :ref:`dipplanner_configfile`
"""

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
SURFACE_TEMP = 37

HE_NARCOTIC_VALUE = 0.23  #: helium narcotic value
N2_NARCOTIC_VALUE = 1.0  #: nitrogen narcotic value
O2_NARCOTIC_VALUE = 1.0  #: oxygen narcotic value
AR_NARCOTIC_VALUE = 2.33  #: argon narcotic value

DEFAULT_AIR_FH2 = 0.0  #: fraction of HE in standard AIR
DEFAULT_AIR_FN2 = 0.7808  #: fraction of N2 in standard AIR
DEFAULT_AIR_FO2 = 0.2095  #: fraction of O2 in standard AIR
DEFAULT_AIR_FAR = 0.00934  #: fraction of AR (argon) in standard AIR
#: fraction of innert gas in standard AIR, rounded to 2 decimals
#: (should be 0.79)
DEFAULT_AIR_F_INNERT_GAS = round(
    DEFAULT_AIR_FH2 + DEFAULT_AIR_FN2 + DEFAULT_AIR_FAR, 2)

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

DECO_MODEL = "ZHL16c"  #: ZHL16c or ZHL16b or ZHL16a
BUHLMANN_VALUES = "1b"  #: 1a (4 mins for 1st comp) or 1b (5 mins)


WATER_DENSITY = SEA_WATER_DENSITY  #: water density kg/l

#: surface pressure (in bar)
AMBIANT_PRESSURE_SURFACE = AMBIANT_PRESSURE_SEA_LEVEL

DEFAULT_MAX_PPO2 = 1.6  #: in bar
DEFAULT_MIN_PPO2 = 0.16  #: in bar
DEFAULT_MAX_END = 30  #: in meter

DIVE_CONSUMPTION_RATE = 20.0 / 60  #: liter/s
DECO_CONSUMPTION_RATE = 17.0 / 60  #: liter/s

DESCENT_RATE = 20   #: m/min
ASCENT_RATE = 10   #: m/min
DECO_ASCENT_RATE = 3   #: m/min

#: Warning : if RUN-TIME is True, the segment duration must
#:           include descent time
#: if the duration is too small dipplanner will raise an error
#: if True: segments represents runtime,
#: if false, segments represents segtime
RUN_TIME = True

USE_OC_DECO = True  #: if True, use enabled gases of decomp in oc or bailout

GF_LOW = 0.30  #: % between 0.0 and 1.0
GF_HIGH = 0.80  #: % between 0.0 and 1.0

#: On dives with multiple depth segments it is possible that
#: decompression encountered during the excursion from a deep to
#: shallower segment will initialise the gradient factors prematurely.
#: Selecting this option keeps the gradient factor set at low until the last
#: dive segment is executed.
#: (normal behaviour is to initialise the gradient factor to Low at
#: the first deco stop encountered. From then on it linearly increases the
#: gradient factor until the final stop when it is set to High)
MULTILEVEL_MODE = False

AUTOMATIC_TANK_REFILL = True  #: automatic refill of tanks between dives
