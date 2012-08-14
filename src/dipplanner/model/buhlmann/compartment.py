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
# Strongly inspired by Guy Wittig's MVPlan
"""Defines a Buhlmann compartment
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]

import math
import logging
# local imports
from dipplanner import settings
from dipplanner.model.buhlmann.model_exceptions import ModelStateException


class Compartment(object):
    """Buhlmann compartment class"""

    def __init__(self, h_he=None, h_n2=None,
                 a_he=None, b_he=None,
                 a_n2=None, b_n2=None):
        """Constructor for Compartment
        can be called without params, in this case, does not initiate anything
        can be called with time params and coef and in this case initate the
        compartment time constants

        Keyword arguments:
        Returns:
        Raise:
        see set_compartment_time_constants method
        """
        #initiate class logger
        self.logger = logging.getLogger(
            "dipplanner.model.buhlmann.compartment.Compartment")
        self.logger.debug("creating an instance of Compartment")

        self.h_he = 0.0
        self.h_n2 = 0.0
        self.k_he = 0.0
        self.k_n2 = 0.0
        self.a_he = 0.0
        self.b_he = 0.0
        self.a_n2 = 0.0
        self.b_n2 = 0.0

        self.pp_he = 0.0
        self.pp_n2 = 0.0

        self.a_he_n2 = 0.0
        self.b_he_n2 = 0.0

        self.const_exp_const_depth_he = None
        self.const_exp_const_depth_n2 = None
        self.old_k_he = None
        self.old_seg_time = None

        if h_he is not None and h_n2 is not None and \
                a_he is not None and b_he is not None and \
                a_n2 is not None and b_n2 is not None:
            self.set_compartment_time_constants(h_he, h_n2,
                                                a_he, b_he,
                                                a_n2, b_n2)

    def __deepcopy__(self, memo):
        """deepcopy method will be called by copy.deepcopy"""
        newobj = Compartment(self.h_he, self.h_n2,
                             self.a_he, self.b_he,
                             self.a_n2, self.b_n2)
        newobj.h_he = self.h_he
        newobj.h_n2 = self.h_n2
        newobj.k_he = self.k_he
        newobj.k_n2 = self.k_n2
        newobj.a_he = self.a_he
        newobj.b_he = self.b_he
        newobj.a_n2 = self.a_n2
        newobj.b_n2 = self.b_n2
        newobj.pp_he = self.pp_he
        newobj.pp_n2 = self.pp_n2
        newobj.a_he_n2 = self.a_he_n2
        newobj.b_he_n2 = self.b_he_n2
        newobj.const_exp_const_depth_he = self.const_exp_const_depth_he
        newobj.const_exp_const_depth_n2 = self.const_exp_const_depth_n2
        newobj.old_k_he = self.old_k_he
        newobj.old_seg_time = self.old_seg_time
        return newobj

    def __repr__(self):
        """Returns a string representing the comp"""
        return "He:%s N2:%s mv_at:%s MV:%s" % (
            self.pp_he,
            self.pp_n2,
            self.get_m_value_at(settings.AMBIANT_PRESSURE_SURFACE),
            self.get_mv(settings.AMBIANT_PRESSURE_SURFACE))

    def __str__(self):
        """Return a human readable name of the segment"""
        return self.__repr__()

    def __unicode__(self):
        """Return a human readable name of the segment in unicode"""
        return u"%s" % self.__repr__()

    def set_compartment_time_constants(self, h_he, h_n2,
                                       a_he, b_he,
                                       a_n2, b_n2):
        """Sets the compartment's time constants

        Keyword arguments:
        h_he -- Helium Halftime
        h_n2 -- Nitrogen Halftime
        a_he -- Helium : a coefficient
        b_he -- Helium : b coefficient
        a_n2 -- Nitrogen : a coefficient
        b_n2 -- Nitrogen : b coefficient

        Returns:
        <nothing>
        """
        self.h_he = h_he
        self.h_n2 = h_n2
        self.k_he = math.log(2) / (float(h_he) * 60)
        self.k_n2 = math.log(2) / (float(h_n2) * 60)
        self.a_he = float(a_he) / 10
        self.b_he = float(b_he)
        self.a_n2 = float(a_n2) / 10
        self.b_n2 = float(b_n2)

    def set_pp(self, pp_he, pp_n2):
        """Sets partial pressures of He and N2

        Keyword arguments:
        pp_he -- partial pressure of Helium
        pp_n2 -- partial pressure of Nitrogen

        Return:
        <nothing>

        Raise:
        ModelStateException -- if pp < 0

        """
        #if pp_he < 0.0 or pp_n2 < 0.0:
        #  raise ModelStateException("Error in argument:
        # negative pp is not allowed")
        #else:
        self.pp_he = pp_he
        self.pp_n2 = pp_n2

        #calculate_p_a_b_inert
        #Calculate and returns a_he_n2 and b_he_n2
        #based on current pp_he and pp_n2 of this compartment
        # calculate adjusted a, b coefficients based on those of He and N2
        self.a_he_n2 = ((self.a_he * pp_he) + (self.a_n2 * pp_n2)) / \
            (pp_he + pp_n2)
        self.b_he_n2 = ((self.b_he * pp_he) + (self.b_n2 * pp_n2)) / \
            (pp_he + pp_n2)

    def const_depth(self, pp_he_inspired, pp_n2_inspired, seg_time):
        """Constant depth calculations.
        Uses instananeous equation: P = Po + (Pi - Po)(1-e^-kt)
        store the new values in self.pp_he and self.pp_n2

        Keyword arguments:
        pp_he_inspired -- partial pressure of inspired helium
        pp_n2_inspired -- partial pressure of inspired nitrogen
        seg_time -- segment time in seconds

        Return:
        <nothing>

        Raise:
        ModelStateException -- if pp or time < 0
        """
        # below is an optimisation to reduce the
        # (1 - math.exp(-self.k_he*float(seg_time)))
        # calculation : only calculate when seg_time changes (k_he or k_n2 does
        # not change for a dive)
        if self.old_seg_time is None:
            self.old_seg_time = seg_time
            self.const_exp_const_depth_he = (1 - math.exp(-self.k_he *
                                                          float(seg_time)))
            self.const_exp_const_depth_n2 = (1 - math.exp(-self.k_n2 *
                                                          float(seg_time)))
        elif self.old_seg_time != seg_time:
            self.old_seg_time = seg_time
            self.const_exp_const_depth_he = (1 - math.exp(-self.k_he *
                                                          float(seg_time)))
            self.const_exp_const_depth_n2 = (1 - math.exp(-self.k_n2 *
                                                          float(seg_time)))

        if pp_he_inspired < 0 or pp_n2_inspired < 0 or seg_time < 0:
            raise ModelStateException(
                "Error in argument: negative value is not allowed")
        else:
            new_pp_he = self.pp_he + ((pp_he_inspired - self.pp_he) *
                                      self.const_exp_const_depth_he)
            new_pp_n2 = self.pp_n2 + ((pp_n2_inspired - self.pp_n2) *
                                      self.const_exp_const_depth_n2)
            #self.set_pp(new_pp_he, new_pp_n2)

            # below is an 'inline' version of set_pp for optimisation:
            self.pp_he = new_pp_he
            self.pp_n2 = new_pp_n2

            #calculate_p_a_b_inert
            #Calculate and returns a_he_n2 and b_he_n2
            #based on current pp_he and pp_n2 of this compartment
            # calculate adjusted a, b coefficients based on those of He and N2
            self.a_he_n2 = ((self.a_he * new_pp_he) +
                            (self.a_n2 * new_pp_n2)) / (new_pp_he + new_pp_n2)
            self.b_he_n2 = ((self.b_he * new_pp_he) +
                            (self.b_n2 * new_pp_n2)) / (new_pp_he + new_pp_n2)

    def asc_desc(self, pp_he_inspired, pp_n2_inspired,
                 rate_he, rate_n2, seg_time):
        """Ascend or descent calculations.
        Uses equation : P=Pio+R(t -1/k)-[Pio-Po-(R/k)]e^-kt
        store the new values in self.pp_he and self.pp_n2

        Keyword arguments:
        pp_he_inspired -- partial pressure of inspired helium
        pp_n2_inspired -- partial pressure of inspired nitrogen
        rate_he -- rate of change of pp_he
        rate_n2 -- rate of change of pp_n2
        seg_time -- segment time in seconds

        Return:
        <nothing>

        Raise:
        ModelStateException -- if pp or time < 0
        """
        if pp_he_inspired < 0 or pp_n2_inspired < 0 or seg_time < 0:
            raise ModelStateException(
                "Error in argument: negative value is not allowed")
        else:
            new_pp_he = pp_he_inspired + rate_he * \
                (float(seg_time) - (1.0 / self.k_he)) - \
                (pp_he_inspired - self.pp_he - (rate_he / self.k_he)) * \
                math.exp(-self.k_he * float(seg_time))
            new_pp_n2 = pp_n2_inspired + rate_n2 * \
                (float(seg_time) - (1.0 / self.k_n2)) - \
                (pp_n2_inspired - self.pp_n2 - (rate_n2 / self.k_n2)) * \
                math.exp(-self.k_n2 * float(seg_time))
            #self.set_pp(new_pp_he, new_pp_n2)

            # below is an 'inline' version of set_pp for optimisation:
            self.pp_he = new_pp_he
            self.pp_n2 = new_pp_n2

            #calculate_p_a_b_inert
            #Calculate and returns a_he_n2 and b_he_n2
            #based on current pp_he and pp_n2 of this compartment
            # calculate adjusted a, b coefficients based on those of He and N2
            self.a_he_n2 = ((self.a_he * new_pp_he) +
                            (self.a_n2 * new_pp_n2)) / (new_pp_he + new_pp_n2)
            self.b_he_n2 = ((self.b_he * new_pp_he) +
                            (self.b_n2 * new_pp_n2)) / (new_pp_he + new_pp_n2)

#def _calculate_p_a_b_inert(self):
#    """Calculate and returns p_he_n2, a_he_n2 and b_he_n2
#    based on current pp_he and pp_n2 of this compartment
#
#    Keyword arguments:
#    <none>
#
#    Returns:
#    3 float values : p_he_n2, a_he_n2 and b_he_n2
#    """
#    p_he_n2 = self.pp_he + self.pp_n2
#    # calculate adjusted a, b coefficients based on those of He and N2
#    a_he_n2 = ((self.a_he * self.pp_he) + (self.a_n2 * self.pp_n2)) / p_he_n2
#    b_he_n2 = ((self.b_he * self.pp_he) + (self.b_n2 * self.pp_n2)) / p_he_n2
#    return p_he_n2, a_he_n2, b_he_n2

    def get_m_value_at(self, pressure):
        """Gets M-Value for given ambient pressure using the Buhlmann equation
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
        return float(pressure) / self.b_he_n2 + self.a_he_n2

    def get_max_amb(self, gf):
        """Gets Tolerated Absolute Pressure for the compartment
        for current pp of He and N2

        Keyword arguments:
        gf -- gradient factor : 0.1 to 1.0, typical 0.2 - 0.95

        Return:
        float, maximum tolerated pressure (absolute) in bar

        """
        return ((self.pp_he + self.pp_n2) - self.a_he_n2 * gf) / \
            (gf / self.b_he_n2 - gf + 1.0)

    def get_mv(self, p_amb):
        """Gets M-Value for a compartment, given an ambient pressure

        Keyword arguments:
        p_amb -- ambiant pressure

        Return:
        float, M-value

        """
        #self.logger.debug("comp m-value for %s : %s" % (p_amb, mv))
        return (self.pp_he + self.pp_n2) / (float(p_amb) /
                                            self.b_he_n2 + self.a_he_n2)
