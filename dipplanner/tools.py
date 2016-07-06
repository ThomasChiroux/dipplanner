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
"""Tools module.

This modules contains some utility functions like unit conversions, etc...
"""
import math
import re

# local imports
from dipplanner import settings


def safe_eval_calculator(text_to_eval):
    """Small an safe eval function usable only for simple calculation.

    (only the basic operators)

    :param float text_to_eval: the text (formula) that should be evaluated

    :returns: the result of the calculation.
    :rtype: float

    :raises ValueError: when given expression is not constitued of only
                        numbers and operators
    :raises SyntaxError: when the given expression is incorrect

    """
    expr = r"^([0-9]|\+|\*|\/|\-|\.|\ )+$"
    re_result = re.match(expr, text_to_eval)
    if re_result is None:
        raise ValueError("Only numbers and simple operators (*+-/) "
                         "are allowed")
    else:
        return eval(re_result.group(0), {'__builtins__': None}, {})


def seconds_to_mmss(seconds):
    """Convert a value in seconds into a str representing time in min & sec.

    (like 2:06)
    It does returns only minutes and seconds, not hours, minutes and seconds

    :param float seconds: the duration in seconds

    :returns: the time in minutes and seconds.
    :rtype: str

    :raises ValueError: when bad time values

    ex::
        " 23:45"
        "112:33"
        ...
    """
    if seconds < 0:
        raise ValueError("time can not be negative")

    text = "%3d:%02d" % (int(seconds / 60), int(seconds % 60))
    return text


def seconds_to_hhmmss(seconds):
    """Convert a value in seconds into a str representing time in h, min & sec.

    like 22:34:44


    :param float seconds: the duration in seconds

    :returns: the time in hour - minutes and seconds
    :rtype: str

    :raises ValueError: when bad time values is given

    ex::
        "00:23:45"
        "01:52:33"
    """
    if seconds < 0:
        raise ValueError("time can not be negative")

    hours = seconds // (60 * 60)
    seconds %= (60 * 60)
    minutes = seconds // 60
    seconds %= 60
    return "%02i:%02i:%02i" % (hours, minutes, seconds)


def altitude_or_depth_to_absolute_pressure(altitude_or_depth):
    """Output absolute pressure for give "depth" in meter.

    * If depth is positive it's considered altitude depth
    * If depth is negative it's considered depth in water

    :param float altitude_or_depth: in meter

    :returns: resulting absolute pressure in bar
    :rtype: float

    :raises ValueError: if altitude > 10000m
    """
    if altitude_or_depth < 0:
        return (depth_to_pressure(-altitude_or_depth) +
                settings.AMBIANT_PRESSURE_SURFACE)
    else:
        return altitude_to_pressure(altitude_or_depth)


def altitude_to_pressure(altitude):
    """Convert a given altitude in pressure in bar.

    uses the formula:
    p = 101325.(1-2.25577.10^-5.h)^5.25588

    :param float altitude: current altitude in meter

    :returns: resulting pressure in bar
    :rtype: float

    :raises ValueError: when bad altitude is given (bad or <0 or > 10000 m)
    """
    if altitude < 0:
        raise ValueError("altitude can not be negative")
    if altitude > 10000:
        raise ValueError("altitude can not higher than 10000m")

    return (math.pow(1 - 2.25577 * math.pow(10, -5) * altitude, 5.25588) *
            settings.AMBIANT_PRESSURE_SEA_LEVEL)


def depth_to_pressure(depth, method=None):
    """Calculate pressure based on given depth.

    depending of choosen mehod (complex or not), the calculation is done
    either /10 or using water density and g.

    :param float depth: in meter
    :param str method: 'complex' for complex method, any other string for
                       simple method.

    :returns: depth pressure in bar
    :rtype: float
    """
    if method is None:
        method = settings.METHOD_FOR_DEPTH_CALCULATION
    if method == 'complex':
        g = 9.81
        return settings.WATER_DENSITY * 1E3 * g * float(depth) * 1E-5
    else:
        return depth / 10


def pressure_to_depth(pressure, method=None):
    """Calculate depth based on given pressure.

    depending of choosen mehod (complex or not), the calculation is done
    either * 10 or using water density and g.

    :param float pressure: pressure in bar
    :param str method: 'complex' for complex method, any other string for
                       simple method.

    :returns: depth in meter
    :rtype: float
    """
    if method is None:
        method = settings.METHOD_FOR_DEPTH_CALCULATION
    if method == 'complex':
        g = 9.81
        return pressure / (settings.WATER_DENSITY * 1E3 * g * 1E-5)
    else:
        return pressure * 10


def calculate_pp_h2o_surf(temperature=20):
    """Calculate and return vapor pressure of water at surface.

    using Antoine equation
    (http://en.wikipedia.org/wiki/Vapour_pressure_of_water)

    :param float temperature: [OPTIONNAL] in ° Celcius

    :returns: ppH2O in bar
    :rtype: float

    :raises ValueError: when temperature exceed maximum value for calculation
                        (>=374 °C)
    """
    mm_hg_to_bar = 1.0 / 750.0615

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
    """SI --> imperial pressure conversion function.

    :param float value: pressure in bar

    :returns: pressure in psi
    :rtype: float
    """
    return value * 14.5037744


def convert_psi_to_bar(value):
    """Imperial --> SI pressure conversion function.

    :param float value: pressure in psi

    :returns: pressure in bar
    :rtype: float
    """
    return value / 14.5037744


def convert_liter_to_cubicfeet(value):
    """SI -->  imperial volume conversion function.

    :param float value: volume in liter

    :returns: volume in cubicfeet
    :rtype: float
    """
    return value / (math.pow(0.3048, 3) * 1000)


def convert_cubicfeet_to_liter(value):
    """Imperial --> SI volume conversion function.

    :param float value: volume in cubicfeet

    :returns: volume in liter
    :rtype: float
    """
    return value * (math.pow(0.3048, 3) * 1000)


def convert_meter_to_feet(value):
    """SI --> imperial distance conversion function.

    :param float value: length in meter

    :returns: length in feet
    :rtype: float
    """
    return value / 0.3048


def convert_feet_to_meter(value):
    """Imperial --> SI distance conversion function.

    :param float value: length in feet

    :returns: length in meter
    :rtype: float
    """
    return value * 0.3048
