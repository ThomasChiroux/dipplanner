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
"""tools modules

Contains:
seconds_to_mmss -- function
altitude_to_pressure -- function
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]

import math

from dipplanner import settings


def seconds_to_mmss(seconds):
    """Convert a value in seconds into a string representing the time in
    minutes and seconds
    (like 2:06)
    It does returns only minutes and seconds, not hours, minutes and seconds

    Keyword Arguments:
    duration - the duration in seconds

    Returns:
    <string> : the time in minutes and seconds

    Raise:
    ValueError: when bad time values

    """
    if seconds < 0:
        raise ValueError("time can not be negative")

    text = "%3d:%02d" % (int(seconds / 60), int(seconds % 60))
    return text


def seconds_to_hhmmss(seconds):
    """Convert a value in seconds into a string representing the time
    in hour:minutes and seconds
    like 22:34:44

    Keyword Arguments:
    seconds - the duration in seconds

    Returns:
    <string> : the time in hour - minutes and seconds

    Raise:
    ValueError: when bad time values is given
    """
    if seconds < 0:
        raise ValueError("time can not be negative")

    hours = seconds // (60 * 60)
    seconds %= (60 * 60)
    minutes = seconds // 60
    seconds %= 60
    return "%02i:%02i:%02i" % (hours, minutes, seconds)


def altitude_or_depth_to_absolute_pressure(altitude_or_depth):
    """output aboslute pressure for give "depth" in meter.
    If depth is positive it's considered altitude depth
    If depth is negative it's considered depth in water

    Keyword Arguments:
    altitude_or_depth - int (signed) : in meter

    Returns:
    float - resulting absolute pressure in bar

    Raise:
    ValueError if altitude > 10000m
    """
    if altitude_or_depth < 0:
        return depth_to_pressure(-altitude_or_depth) + \
            settings.AMBIANT_PRESSURE_SURFACE
    else:
        return altitude_to_pressure(altitude_or_depth)


def altitude_to_pressure(altitude):
    """Convert a given altitude in pressure in bar
    uses the formula:
    p = 101325.(1-2.25577.10^-5.h)^5.25588

    Keyword Arguments:
    altitude - current altitude in meter

    Returns:
    float - resulting pressure in bar

    Raise:
    ValueError: when bad altitude is given (bad or <0 or > 10000 m)

    """
    if altitude < 0:
        raise ValueError("altitude can not be negative")
    if altitude > 10000:
        raise ValueError("altitude can not higher than 10000m")

    return math.pow(1 - 2.25577 * math.pow(10, -5) * altitude, 5.25588) * \
        settings.AMBIANT_PRESSURE_SEA_LEVEL


def depth_to_pressure(depth):
    """Calculates depth pressure based on depth using a more complex
    method than only /10

    Keyword Arguments:
    depth - in meter

    Returns:
    float - depth pressure in bar

    """
    if settings.METHOD_FOR_DEPTH_CALCULATION == 'complex':
        g = 9.81
        return settings.WATER_DENSITY * 1E3 * g * float(depth) * 1E-5
    else:
        return float(depth) / 10


def pressure_to_depth(pressure):
    """Calculates depth based on give pressure using a more complex
    method than only *10

    Keyword Arguments:
    pressure - float in bar

    Returns:
    int - depth in meter

    """
    if settings.METHOD_FOR_DEPTH_CALCULATION == 'complex':
        g = 9.81
        return float(pressure) / (settings.WATER_DENSITY * 1E3 * g * 1E-5)
    else:
        return float(pressure) * 10


def calculate_pp_h2o_surf(temperature=20):
    """Calculates and return vapor pressure of water at surface
    using Antoine equation
    (http://en.wikipedia.org/wiki/Vapour_pressure_of_water)

    Keyword Arguments:
      temperature - float in ° Celcius

    Returns:
      float - ppH2O in bar
    """
    mm_hg_to_bar = 1 / 750.0615

    if temperature < 1:
        temperature = 1
    if temperature >= 1 and temperature <= 100:
        const_a = 8.07131
        const_b = 1730.63
        const_c = 233.426
    elif temperature > 100 and temperature < 374:
        const_a = 8.14019
        const_b = 1810.94
        const_c = 244.485
    else:
        raise ValueError("Temperature is too High")

    pressure_mm_hg = 10 ** (const_a - (const_b / (const_c +
                                                  float(temperature))))
    return pressure_mm_hg * mm_hg_to_bar


def convert_bar_to_psi(value):
    """SI - imperial conversion function
    """
    return float(value) * 14.5037744


def convert_psi_to_bar(value):
    """SI - imperial conversion function
    """
    return float(value) / 14.5037744


def convert_liter_to_cubicfeet(value):
    """SI - imperial conversion function
    """
    return float(value) / (math.pow(0.3048, 3) * 1000)


def convert_cubicfeet_to_liter(value):
    """SI - imperial conversion function
    """
    return float(value) * (math.pow(0.3048, 3) * 1000)


def convert_meter_to_feet(value):
    """SI - imperial conversion function
    """
    return float(value) / 0.3048


def convert_feet_to_meter(value):
    """SI - imperial conversion function
    """
    return float(value) * 0.3048
