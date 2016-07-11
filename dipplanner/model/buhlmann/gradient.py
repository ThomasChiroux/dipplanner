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
"""Gradient module."""

import logging


class Gradient():
    """Define a Gradient Factor object.

    A GF Object maintains a low and high setting and is able to determine
    a GF for any depth between its initialisation depth (see setGfAtDepth())
    and the surface.

    *Attributes (self.):*
        * gf_low (float) -- low Gradient factor, from 0.0 to 1.0
        * gf_high (float) -- high Gradient factor, from 0.0 to 1.0
        * gf (float) -- current gf
        * gf_slope (float) -- slope of the linear equation
        * gf_set (bool) -- Indicates that gf Slope has been initialised
    """

    def __init__(self, gf_low, gf_high):
        """Init of Gradient object.

        :param float gf_low: low Gradient factor, from 0.0 to 1.0
        :param float gf_high: high Gradient factor, from 0.0 to 1.0

        :raises ValueError: if either gf_low of gf_high has wrong value
        """
        # initiate class logger
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
        """Deepcopy method will be called by copy.deepcopy.

        Used for "cloning" the object into another new object.

        :param memo: not used here

        :returns: Gradient object copy of itself
        :rtype: :class:`Gradient`
        """
        newobj = Gradient(self.gf_low, self.gf_high)
        newobj.gf = self.gf
        newobj.gf_slope = self.gf_slope
        newobj.gf_set = self.gf_set
        return newobj

    def get_gradient_factor(self):
        """Return current GF with bounds checking.

        if gf < gf_low, returns gf_low

        :returns: gf
        :rtype: float
        """
        if self.gf >= self.gf_low:
            return self.gf
        else:
            return self.gf_low

    def set_gf_at_depth(self, depth):
        """Set the gf for a given depth.

        :param float depth: current depth, in meter
        """
        if (self.gf_slope < 1.0) and (depth >= 0.0):
            self.gf = (depth * self.gf_slope) + self.gf_high

    def set_gf_slope_at_depth(self, depth):
        """Set gf Slope at specified depth.

        Typically called once to initialise the GF slope.

        :param float depth: current depth, in meter
        """
        if depth > 0:
            self.gf_slope = (self.gf_high - self.gf_low) / (0.0 - depth)
            self.gf_set = True

    def set_gf_low(self, value):
        """Set gf low setting.

        :param float value: low Gf, between 0.0 and 1.0

        :raises ValueError: if either gf_low of gf_high has wrong value
        """
        if value < 0.0 or value > 1.0:
            raise ValueError("gf_low should be between 0.0 and 1.0")
        else:
            self.gf_low = float(value)

    def set_gf_high(self, value):
        """Set gf high setting.

        :param float value: high Gf, between 0.0 and 1.0

        :raises ValueError: if either gf_low of gf_high has wrong value
        """
        if value < 0.0 or value > 1.0:
            raise ValueError("gf_high should be between 0.0 and 1.0")
        else:
            self.gf_high = float(value)
