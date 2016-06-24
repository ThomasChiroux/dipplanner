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

"""gradient module
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]

import logging
#local imports
#import settings


class Gradient(object):
    """Defines a Gradient Factor object

    A GF Object maintains a low and high setting and is able to determine
    a GF for any depth between its initialisation depth (see setGfAtDepth())
    and the surface.

    *Attributes (self.):*
        * gf_low (float) -- low Gradient factor, from 0.0 to 1.0
        * gf_high (float) -- high Gradient factor, from 0.0 to 1.0
        * gf (float) -- current gf
        * gf_slope (float) -- slope of the linear equation
        * gf_set (float) -- Indicates that gf Slope has been initialised
    """

    def __init__(self, gf_low, gf_high):
        """Constructor for Gradient object

        *Keyword arguments:*
            :gf_low: (float) -- low Gradient factor, from 0.0 to 1.0
            :gf_high: (float) -- high Gradient factor, from 0.0 to 1.0

        *Returns:*
            <nothing>

        *Raise:*
            ValueError -- if either gf_low of gf_high has wrong value

        """
        #initiate class logger
        self.logger = logging.getLogger(
            "dipplanner.model.buhlmann.gradient.Gradient")
        self.logger.debug("creating an instance of Gradient")

        self.gf_low = None
        self.gf_high = None
        self.set_gf_low(gf_low)
        self.set_gf_high(gf_high)

        self.gf_slope = 1.0
        self.gf = gf_low
        self.gf_set = False

    def __deepcopy__(self, memo):
        """deepcopy method will be called by copy.deepcopy

        Used for "cloning" the object into another new object.

        *Keyword Arguments:*
            :memo: -- not used here

        *Returns:*
            Gradient -- Gradient object copy of itself

        *Raise:*
            <nothing>
        """
        newobj = Gradient(self.gf_low, self.gf_high)
        newobj.gf = self.gf
        newobj.gf_slope = self.gf_slope
        newobj.gf_set = self.gf_set
        return newobj

    def get_gradient_factor(self):
        """Returns current GF with bounds checking
        if gf < gf_low, returns gf_low

        *Keyword arguments:*
            <none>

        *Returns:*
            float -- gf

        *Raise:*
            <nothing>
        """
        if self.gf >= self.gf_low:
            return self.gf
        else:
            return self.gf_low

    def set_gf_at_depth(self, depth):
        """Sets the gf for a given depth.
        Must be called after setGfSlope() has initialised slope

        *Keyword arguments:*
            :depth: (float) -- current depth, in meter

        *Returns:*
            <nothing>

        *Raise:*
            <nothing>
        """
        if (self.gf_slope < 1.0) and (depth >= 0.0):
            self.gf = (depth * self.gf_slope) + self.gf_high

    def set_gf_slope_at_depth(self, depth):
        """Set gf Slope at specified depth.
        Typically called once to initialise the GF slope.

        *Keyword arguments:*
            :depth: (float) -- current depth, in meter

        *Returns:*
            <nothing>

        *Raise:*
            <nothing>
        """
        if depth > 0:
            self.gf_slope = (self.gf_high - self.gf_low) / (0.0 - depth)
            self.gf_set = True

    def set_gf_low(self, value):
        """Sets gf low setting

        *Keyword arguments:*
            :value: (float) -- low Gf, between 0.0 and 1.0

        *Returns:*
            <nothing>

        *Raise:*
            ValueError -- if either gf_low of gf_high has wrong value

        """
        if value < 0.0 or value > 1.0:
            raise ValueError("gf_low should be between 0.0 and 1.0")
        else:
            self.gf_low = float(value)

    def set_gf_high(self, value):
        """Sets gf high setting

        *Keyword arguments:*
            :value: (float) -- high Gf, between 0.0 and 1.0

        *Returns:*
            <nothing>

        *Raise:*
            ValueError -- if gf_high has wrong value

        """
        if value < 0.0 or value > 1.0:
            raise ValueError("gf_high should be between 0.0 and 1.0")
        else:
            self.gf_high = float(value)