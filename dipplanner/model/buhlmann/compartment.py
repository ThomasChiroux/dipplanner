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
"""Define a Buhlmann compartment."""
import math
import logging

from dipplanner import settings
from dipplanner.model.buhlmann.model_exceptions import ModelStateException


class Compartment():
    """Buhlmann compartment class.

    *Attributes:*
        * h_he: helium halftime
        * h_n2: nitrogen halftime
        * a_he: helium : a coefficient
        * a_n2: nitrogen : a coefficient
        * b_he: helium : b coefficient
        * b_n2: nitrogen : b coefficient
        * k_he: helium : k coefficient (calculated)
        * k_n2: nitrogen : k coefficient (calculated)
        * pp_he: partial pressure of helium
        * pp_n2: partial pressure of nitrogen
    """

    def __init__(self, h_he=None, h_n2=None,
                 a_he=None, b_he=None,
                 a_n2=None, b_n2=None):
        """Init of Compartment.

        can be called without params, in this case, does not initiate anything
        can be called with time params and coef and in this case initate the
        compartment time constants

        :param float h_he: helium halftime
        :param float h_n2: nitrogen halftime
        :param float a_he: helium: a coefficient
        :param float b_he: helium: b coefficient
        :param float a_n2: nitrogen: a coefficient
        :param float b_n2: nitrogen: b coefficient
        """
        # initiate class logger
        self.logger = logging.getLogger(
            "dipplanner.model.buhlmann.compartment.Compartment")
        # self.logger.debug("creating an instance of Compartment")

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

        if (h_he is not None and h_n2 is not None and
                a_he is not None and b_he is not None and
                a_n2 is not None and b_n2 is not None):
            self.set_compartment_time_constants(h_he, h_n2,
                                                a_he, b_he,
                                                a_n2, b_n2)

    def __deepcopy__(self, memo):
        """Deepcopy method will be called by copy.deepcopy.

        Used for "cloning" the object into another new object.

        :param memo: not used here

        :returns: Compartment object copy of itself
        :rtype: :class:`Compartment`
        """
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
        """Return a string representing the compartement.

        :returns: string representation of the compartment
        :rtype: str
        """
        return "He:%s N2:%s mv_at:%s MV:%s" % (
            self.pp_he,
            self.pp_n2,
            self.get_m_value_at(settings.AMBIANT_PRESSURE_SURFACE),
            self.get_mv(settings.AMBIANT_PRESSURE_SURFACE))

    def __str__(self):
        """Return a human readable name of the compartement.

        :returns: string representation of the compartment
        :rtype: str
        """
        return self.__repr__()

    def set_compartment_time_constants(self, h_he, h_n2,
                                       a_he, b_he,
                                       a_n2, b_n2):
        """Set the compartment's time constants.

        :param float h_he: Helium Halftime
        :param float h_n2: Nitrogen Halftime
        :param float a_he: Helium : a coefficient
        :param float b_he: Helium : b coefficient
        :param float a_n2: Nitrogen : a coefficient
        :param float b_n2: Nitrogen : b coefficient
        """
        self.h_he = h_he
        self.h_n2 = h_n2
        self.k_he = math.log(2) / (float(h_he) * 60)
        self.k_n2 = math.log(2) / (float(h_n2) * 60)
        self.a_he = float(a_he)
        self.b_he = float(b_he)
        self.a_n2 = float(a_n2)
        self.b_n2 = float(b_n2)

    def set_pp(self, pp_he, pp_n2):
        """Set partial pressures of He and N2.

        :param float pp_he: partial pressure of Helium
        :param float pp_n2: partial pressure of Nitrogen
        """
        # if pp_he < 0.0 or pp_n2 < 0.0:
        #   raise ModelStateException("Error in argument:
        #  negative pp is not allowed")
        # else:
        self.pp_he = pp_he
        self.pp_n2 = pp_n2

        # calculate_p_a_b_inert
        # Calculate and returns a_he_n2 and b_he_n2
        # based on current pp_he and pp_n2 of this compartment
        #  calculate adjusted a, b coefficients based on those of He and N2
        self.a_he_n2 = (((self.a_he * pp_he) + (self.a_n2 * pp_n2)) /
                        (pp_he + pp_n2))
        self.b_he_n2 = (((self.b_he * pp_he) + (self.b_n2 * pp_n2)) /
                        (pp_he + pp_n2))

    def const_depth(self, pp_he_inspired, pp_n2_inspired, seg_time):
        """Constant depth calculations.

        Uses instananeous equation: P = Po + (Pi - Po)(1-e^-kt)
        store the new values in self.pp_he and self.pp_n2

        :param float pp_he_inspired: partial pressure of inspired helium
        :param float pp_n2_inspired: partial pressure of inspired nitrogen
        :param float seg_time: segment time in seconds

        :raises ModelStateException: if pp or time < 0
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
            # self.set_pp(new_pp_he, new_pp_n2)

            # below is an 'inline' version of set_pp for optimisation:
            self.pp_he = new_pp_he
            self.pp_n2 = new_pp_n2

            # calculate_p_a_b_inert
            # Calculate and returns a_he_n2 and b_he_n2
            # based on current pp_he and pp_n2 of this compartment
            #  calculate adjusted a, b coefficients based on those of He and N2
            self.a_he_n2 = ((self.a_he * new_pp_he) +
                            (self.a_n2 * new_pp_n2)) / (new_pp_he + new_pp_n2)
            self.b_he_n2 = ((self.b_he * new_pp_he) +
                            (self.b_n2 * new_pp_n2)) / (new_pp_he + new_pp_n2)

    def asc_desc(self, pp_he_inspired, pp_n2_inspired,
                 rate_he, rate_n2, seg_time):
        """Ascend or descent calculations.

        Uses equation : P=Pio+R(t -1/k)-[Pio-Po-(R/k)]e^-kt
        store the new values in self.pp_he and self.pp_n2

        :param float pp_he_inspired: partial pressure of inspired helium
        :param float pp_n2_inspired: partial pressure of inspired nitrogen
        :param float rate_he: rate of change of pp_he
        :param float rate_n2: rate of change of pp_n2
        :param float seg_time: segment time in seconds

        :raises ModelStateException: if pp or time < 0
        """
        if pp_he_inspired < 0 or pp_n2_inspired < 0 or seg_time < 0:
            raise ModelStateException(
                "Error in argument: negative value is not allowed")
        else:
            new_pp_he = (pp_he_inspired +
                         rate_he * (float(seg_time) - (1.0 / self.k_he)) -
                         (pp_he_inspired - self.pp_he -
                          (rate_he / self.k_he)) *
                         math.exp(-self.k_he * float(seg_time)))
            new_pp_n2 = (pp_n2_inspired +
                         rate_n2 * (float(seg_time) - (1.0 / self.k_n2)) -
                         (pp_n2_inspired - self.pp_n2 -
                          (rate_n2 / self.k_n2)) *
                         math.exp(-self.k_n2 * float(seg_time)))
            # self.set_pp(new_pp_he, new_pp_n2)
            # below is an 'inline' version of set_pp for optimisation:
            self.pp_he = new_pp_he
            self.pp_n2 = new_pp_n2

            # calculate_p_a_b_inert
            # Calculate and returns a_he_n2 and b_he_n2
            # based on current pp_he and pp_n2 of this compartment
            #  calculate adjusted a, b coefficients based on those of He and N2
            self.a_he_n2 = ((self.a_he * new_pp_he) +
                            (self.a_n2 * new_pp_n2)) / (new_pp_he + new_pp_n2)
            self.b_he_n2 = ((self.b_he * new_pp_he) +
                            (self.b_n2 * new_pp_n2)) / (new_pp_he + new_pp_n2)

    def get_m_value_at(self, pressure):
        """Get M-Value for given ambient pressure using the Buhlmann equation.

        Pm = Pa/b +a
        where:

            * Pm = M-Value pressure,
            * Pa = ambiant pressure
            * a,b co-efficients

        .. note::

            Not used for decompression but for display of M-value limit line

        .. note::

            this method does not use gradient factors.

        :param float pressure: ambient pressure (in bar)

        :returns: M_value: maximum tolerated pressure in bar
        :rtype: float
        """
        return float(pressure) / self.b_he_n2 + self.a_he_n2

    def get_max_amb(self, gf):
        """Get Tolerated Absolute Pressure for the compartment.

        for current pp of He and N2

        :param float gf: gradient factor : 0.1 to 1.0, typical 0.2 - 0.95

        :returns: maximum tolerated pressure (absolute) in bar
        :rtype: float
        """
        return (((self.pp_he + self.pp_n2) - self.a_he_n2 * gf) /
                (gf / self.b_he_n2 - gf + 1.0))

    def get_mv(self, p_amb):
        """Get M-Value for a compartment, given an ambient pressure.

        :param float p_amb: ambiant pressure

        :returns: M-value
        :rtype: float
        """
        # self.logger.debug("comp m-value for %s : %s" % (p_amb, mv))
        return (self.pp_he + self.pp_n2) / (float(p_amb) /
                                            self.b_he_n2 + self.a_he_n2)
