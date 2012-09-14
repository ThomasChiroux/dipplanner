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

"""Buhlmann model module

Contains:
Model -- class
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]

import logging
import copy
# local imports
from dipplanner import settings
from dipplanner.model.buhlmann.compartment import Compartment
from dipplanner.model.buhlmann.gradient import Gradient
from dipplanner.model.buhlmann.oxygen_toxicity import OxTox
from dipplanner import tools


class Model(object):
    """Represents a Buhlmann model.
    Composed of a tissue array of Compartment[]
    Has an OxTox and Gradient object

    Can throw a ModelStateException propagated from a Compartment if pressures
    or time is out of bounds.

    Models are initialised by initModel() if they are new models, or
    validated by validateModel() if they are rebuild from a saved model.

    The model is capable of ascending or descending via ascDec() using the
    ascDec() method of Compartment,
    or accounting for a constant depth using the
    constDepth() method of Compartment.

    Attributes:
        * tissues (list)-- a list of Compartments
        * gradient (Gradient) -- gradient factor object
        * ox_tox (OxTox) -- OxTox object
        * metadata (str) -- Stores infos about where the model was created
        * deco_model (str) -- name of the deco model
        * units (str) -- only 'metric' allowed
        * COMPS (int) -- static info : number of compartments
        * MODEL_VALIDATION_SUCCESS (int) -- static const for validation success
        * MODEL_VALIDATION_FAILURE (int) -- static const for validation failure
    """
    COMPS = 16

    #TODO: SUPPRIMER CES DEUX ELEMENTS ET REMPLACER PAR DES RAISE
    MODEL_VALIDATION_SUCCESS = 1
    MODEL_VALIDATION_FAILURE = 0

    def __init__(self):
        """Constructor for model class

        *Keyword arguments:*
            <none>

        *Returns:*
            <nothing>

        *Raise:*
            <nothing>
        """
        #initiate class logger
        self.logger = logging.getLogger(
            "dipplanner.model.buhlmann.model.Model")
        self.logger.debug("creating an instance of Model")
        self.deco_model = None
        self.units = 'metric'
        self.tissues = []
        self.ox_tox = OxTox()
        self.gradient = None
        self.init_gradient()

        for _ in range(0, self.COMPS):
            self.tissues.append(Compartment())

        self.set_time_constants()

        for comp in self.tissues:
            comp.set_pp(0.0, 0.79 *
                        (settings.AMBIANT_PRESSURE_SURFACE -
                         tools.calculate_pp_h2o_surf(settings.SURFACE_TEMP)))
            #TODO: Check above : 0.79 or settings.DEFAULT_AIR_PPN2 (tdb) ?

        self.metadata = "(none)"

    def __deepcopy__(self, memo):
        """deepcopy method will be called by copy.deepcopy

        Used for "cloning" the object into another new object.

        *Keyword Arguments:*
            :memo: -- not used here

        *Returns:*
            Model -- Model object copy of itself

        *Raise:*
            <nothing>
        """
        newobj = Model()
        newobj.units = self.units
        newobj.ox_tox = copy.deepcopy(self.ox_tox)
        newobj.gradient = copy.deepcopy(self.gradient)
        newobj.metadata = self.metadata
        for i in range(0, len(self.tissues)):
            newobj.tissues[i] = copy.deepcopy(self.tissues[i])
        return newobj

    def __repr__(self):
        """Returns a string representing the model

        *Keyword Arguments:*
            <none>

        *Returns:*
            str -- string representation of the model

        *Raise:*
            <nothing>
        """
        model_string = ""  # "Compartment pressures:\n"
        for comp_number in range(0, self.COMPS):
            model_string += "C:%s He:%s N2:%s gf:%s \
mv_at:%s max_amb:%s MV:%s\n" % \
                (comp_number,
                 self.tissues[comp_number].pp_he,
                 self.tissues[comp_number].pp_n2,
                 self.gradient.gf,
                 self.tissues[comp_number].get_m_value_at(
                     settings.AMBIANT_PRESSURE_SURFACE),
                 (self.tissues[comp_number].get_max_amb(
                     self.gradient.gf)) * 1,
                 self.tissues[comp_number].get_mv(
                     settings.AMBIANT_PRESSURE_SURFACE))
        #model_string += "Ceiling: %s\n" % self.ceiling()
        #model_string += "Max surface M-Value: %s\n" % self.m_value(0.0)
        #model_string += "OTUs accumulated: %s" % self.ox_tox.otu
        return model_string

    def __str__(self):
        """Return a human readable name of the segment

        *Keyword Arguments:*
            <none>

        *Returns:*
            str -- string representation of the model

        *Raise:*
            <nothing>
        """
        return self.__repr__()

    def __unicode__(self):
        """Return a human readable name of the segment in unicode

        *Keyword Arguments:*
            <none>

        *Returns:*
            ustr -- unicode string representation of the model

        *Raise:*
            <nothing>
        """
        return u"%s" % self.__repr__()

    def init_gradient(self):
        """Initialise the gradient attribute
        uses the default settings parameters for gf_low and high

        *Keyword arguments:*
            <none>

        *Returns:*
            <nothing>

        *Raise:*
            <nothing>
        """
        self.gradient = Gradient(settings.GF_LOW, settings.GF_HIGH)

    def set_time_constants(self, deco_model=settings.DECO_MODEL):
        """Initialize time constants in buhlmann tissue list
        Only for metric values

        *Keyword arguments:*
            :deco_model: (str) -- "ZHL16b" or "ZHL16c"

        *Returns:*
            <nothing>

        *Raise:*
            <nothing>
        """
        # note: comparing with buhlmann original (1990) ZH-L16 a coeficient,
        # there is here a x10 factor for a coeficient
        #h_he, h_n2, a_he, b_he, a_n2, b_n2
        if deco_model == "ZHL16c":
            self.deco_model = deco_model
            self.logger.info("model used: Buhlmann ZHL16c")
            self.tissues[0].set_compartment_time_constants(
                1.88,    5.0,    16.189, 0.4770, 11.696, 0.5578)
            self.tissues[1].set_compartment_time_constants(
                3.02,    8.0,    13.83,  0.5747, 10.0,   0.6514)
            self.tissues[2].set_compartment_time_constants(
                4.72,    12.5,   11.919, 0.6527, 8.618,  0.7222)
            self.tissues[3].set_compartment_time_constants(
                6.99,    18.5,   10.458, 0.7223, 7.562,  0.7825)
            self.tissues[4].set_compartment_time_constants(
                10.21,   27.0,   9.220,  0.7582, 6.667,  0.8126)
            self.tissues[5].set_compartment_time_constants(
                14.48,   38.3,   8.205,  0.7957, 5.60,   0.8434)
            self.tissues[6].set_compartment_time_constants(
                20.53,   54.3,   7.305,  0.8279, 4.947,  0.8693)
            self.tissues[7].set_compartment_time_constants(
                29.11,   77.0,   6.502,  0.8553, 4.5,    0.8910)
            self.tissues[8].set_compartment_time_constants(
                41.20,   109.0,  5.950,  0.8757, 4.187,  0.9092)
            self.tissues[9].set_compartment_time_constants(
                55.19,   146.0,  5.545,  0.8903, 3.798,  0.9222)
            self.tissues[10].set_compartment_time_constants(
                70.69,  187.0,  5.333,  0.8997, 3.497,  0.9319)
            self.tissues[11].set_compartment_time_constants(
                90.34,  239.0,  5.189,  0.9073, 3.223,  0.9403)
            self.tissues[12].set_compartment_time_constants(
                115.29, 305.0,  5.181,  0.9122, 2.850,  0.9477)
            self.tissues[13].set_compartment_time_constants(
                147.42, 390.0,  5.176,  0.9171, 2.737,  0.9544)
            self.tissues[14].set_compartment_time_constants(
                188.24, 498.0,  5.172,  0.9217, 2.523,  0.9602)
            self.tissues[15].set_compartment_time_constants(
                240.03, 635.0,  5.119,  0.9267, 2.327,  0.9653)
        elif deco_model == "ZHL16b":
            self.deco_model = deco_model
            self.logger.info("model used: Buhlmann ZHL16b")
            self.tissues[0].set_compartment_time_constants(
                1.88,    5.0,    16.189, 0.4770, 11.696, 0.5578)
            self.tissues[1].set_compartment_time_constants(
                3.02,    8.0,    13.83,  0.5747, 10.0,   0.6514)
            self.tissues[2].set_compartment_time_constants(
                4.72,    12.5,   11.919, 0.6527, 8.618,  0.7222)
            self.tissues[3].set_compartment_time_constants(
                6.99,    18.5,   10.458, 0.7223, 7.562,  0.7825)
            self.tissues[4].set_compartment_time_constants(
                10.21,   27.0,   9.220,  0.7582, 6.667,  0.8126)
            self.tissues[5].set_compartment_time_constants(
                14.48,   38.3,   8.205,  0.7957, 5.933,   0.8434)
            self.tissues[6].set_compartment_time_constants(
                20.53,   54.3,   7.305,  0.8279, 5.282,  0.8693)
            self.tissues[7].set_compartment_time_constants(
                29.11,   77.0,   6.502,  0.8553, 4.71,    0.8910)
            self.tissues[8].set_compartment_time_constants(
                41.20,   109.0,  5.950,  0.8757, 4.187,  0.9092)
            self.tissues[9].set_compartment_time_constants(
                55.19,   146.0,  5.545,  0.8903, 3.798,  0.9222)
            self.tissues[10].set_compartment_time_constants(
                70.69,  187.0,  5.333,  0.8997, 3.497,  0.9319)
            self.tissues[11].set_compartment_time_constants(
                90.34,  239.0,  5.189,  0.9073, 3.223,  0.9403)
            self.tissues[12].set_compartment_time_constants(
                115.29, 305.0,  5.181,  0.9122, 2.971,  0.9477)
            self.tissues[13].set_compartment_time_constants(
                147.42, 390.0,  5.176,  0.9171, 2.737,  0.9544)
            self.tissues[14].set_compartment_time_constants(
                188.24, 498.0,  5.172,  0.9217, 2.523,  0.9602)
            self.tissues[15].set_compartment_time_constants(
                240.03, 635.0,  5.119,  0.9267, 2.327,  0.9653)

    def validate_model(self):
        """Validate model - checks over the model and looks for corruption

        This is needed to check a model that has been loaded from XML
        Resets time constants

        *Keyword arguments:*
            <none>

        *Returns:*
            self.MODEL_VALIDATION_SUCCESS -- if OK
            self.MODEL_VALIDATION_FAILURE -- if not OK

        *Raise:*
            <nothing>
        """
        time_constant_zero = False  # need for resetting time constants

        for comp in self.tissues:
            if comp.pp_n2 <= 0.0:
                return self.MODEL_VALIDATION_FAILURE
            if comp.pp_he < 0.0:
                return self.MODEL_VALIDATION_FAILURE
            if comp.k_he == 0.0 or \
                    comp.k_n2 == 0.0 or \
                    comp.a_he == 0.0 or \
                    comp.b_he == 0.0 or \
                    comp.a_n2 == 0.0 or \
                    comp.b_n2 == 0.0:
                time_constant_zero = True
        if time_constant_zero:
            self.set_time_constants()
        return self.MODEL_VALIDATION_SUCCESS

    def control_compartment(self):
        """Determine the controlling compartment at ceiling (1-16)

        *Keyword arguments:*
            <none>

        *Returns:*
            integer -- reference number of the controlling
                      compartment (between 1 to 16)

        *Raise:*
            <nothing>
        """
        control_compartment_number = 0
        max_pressure = 0.0

        for comp_number in range(0, self.COMPS):
            pressure = self.tissues[comp_number].get_max_amb(
                self.gradient.gf) - settings.AMBIANT_PRESSURE_SURFACE
            #self.logger.debug("pressure:%s" % pressure)
            if pressure > max_pressure:
                control_compartment_number = comp_number
                max_pressure = pressure
        return control_compartment_number + 1

    def ceiling(self):
        """Determine the current ceiling depth

        *Keyword arguments:*
            <none>

        *Returns:*
            float -- ceiling depth in meter

        *Raise:*
            <nothing>
        """
        pressure = 0.0
        for comp in self.tissues:
            #Get compartment tolerated ambient pressure and convert from
            # absolute pressure to depth
            comp_pressure = comp.get_max_amb(
                self.gradient.gf) - settings.AMBIANT_PRESSURE_SURFACE
            if comp_pressure > pressure:
                pressure = comp_pressure
        return tools.pressure_to_depth(pressure)

    def ceiling_in_pabs(self):
        """Determine the current ceiling

        *Keyword arguments:*
            <none>

        *Returns:*
            float -- ceiling in bar (absolute pressure)

        *Raise:*
            <nothing>
        """
        pressure = 0.0
        for comp in self.tissues:
            #Get compartment tolerated ambient pressure and convert from
            #absolute pressure to depth
            comp_pressure = comp.get_max_amb(self.gradient.gf)
            if comp_pressure > pressure:
                pressure = comp_pressure
        return pressure

    def m_value(self, pressure):
        """Determine the maximum M-Value for a given depth (pressure)

        *Keyword arguments:*
            :pressure: (float) -- in bar

        *Returns*
            float -- max M-Value

        *Raise:*
            <nothing>
        """
        p_absolute = pressure + settings.AMBIANT_PRESSURE_SURFACE
        compartment_mv = 0.0
        max_mv = 0.0

        for comp in self.tissues:
            compartment_mv = comp.get_mv(p_absolute)
            if compartment_mv > max_mv:
                max_mv = compartment_mv
        #self.logger.debug("max mv : %s" % max_mv)
        return max_mv

    def const_depth(self, pressure, seg_time, f_he, f_n2, pp_o2):
        """Constant depth profile.
        Calls Compartment.constDepth for each compartment to update the model.

        *Keyword arguments:*

            :pressure: (float)-- pressure of this depth of segment in bar
            :seg_time: (float) -- Time of segment in seconds
            :f_he: (float) -- fraction of inert gas Helium in inspired gas mix
            :f_n2: (float) -- fraction of inert gas Nitrogen in
                              inspired gas mix
            :pp_o2: (float) -- For CCR mode, partial pressure of oxygen in bar.
                               If == 0.0, then open circuit

        *Returns:*
            <nothing>

        *Raise:*
            ModelStateException

        """
        ambiant_pressure = pressure + settings.AMBIANT_PRESSURE_SURFACE
        if pp_o2 > 0.0:
            # CCR mode
            #Determine pInert by subtracting absolute oxygen pressure and pH2O
            #Note that if f_he and f_n2 == 0.0 then need to force pp's to zero
            if f_he + f_n2 > 0.0:
                p_inert = ambiant_pressure - pp_o2 - \
                    tools.calculate_pp_h2o_surf(settings.SURFACE_TEMP)
            else:
                p_inert = 0.0

            #Verify that pInert is positive. If the setpoint is close to or
            # less than the depth then there is no inert gas.
            if p_inert > 0.0:
                pp_he_inspired = (p_inert * f_he) / (f_he + f_n2)
                pp_n2_inspired = (p_inert * f_n2) / (f_he + f_n2)
            else:
                pp_he_inspired = 0.0
                pp_n2_inspired = 0.0

            # update OxTox object
            pp_o2_inspired = pp_o2
            #Check that ppO2Inspired is not greater than the depth.
            #This occurs in shallow deco when the setpoint specified is > depth
            if pp_o2_inspired <= ambiant_pressure and p_inert > 0.0:
                # pp_o2 is the setpoint
                self.ox_tox.add_o2(seg_time, pp_o2)
            else:
                # pp_o2 is equal to the depth, also true is there is
                # no inert gaz
                self.ox_tox.add_o2(seg_time, ambiant_pressure -
                                   tools.calculate_pp_h2o_surf(
                                       settings.SURFACE_TEMP))
        else:
            # OC mode
            pp_he_inspired = (ambiant_pressure -
                              tools.calculate_pp_h2o_surf(
                                  settings.SURFACE_TEMP)) * f_he
            pp_n2_inspired = (ambiant_pressure -
                              tools.calculate_pp_h2o_surf(
                                  settings.SURFACE_TEMP)) * f_n2
            # update ox_tox
            if pressure == 0.0:  # surface
                self.ox_tox.remove_o2(seg_time)
            else:
                self.ox_tox.add_o2(
                    seg_time,
                    (ambiant_pressure -
                     tools.calculate_pp_h2o_surf(settings.SURFACE_TEMP))
                    * (1.0 - f_he - f_n2))
        if seg_time > 0:
            for comp in self.tissues:
                comp.const_depth(pp_he_inspired, pp_n2_inspired, seg_time)

    def asc_desc(self, start, finish, rate, f_he, f_n2, pp_o2):
        """Ascend/Descend profile.
        Calls Compartment.asc_desc to update compartments

        *Keyword arguments:*

            :start: (float) -- start pressure of this segment in bar
                               (WARNING: not meter ! it's a pressure)
            :finish: (float) -- finish pressure of this segment in bar
                                (WARNING: not meter ! it's a pressure)
            :rate: (float) -- rate of ascent or descent in m/s
            :f_he: (float) -- Fraction of inert gas Helium in inspired gas mix
            :f_n2: (float) -- Fraction of inert gas Nitrogen
                              in inspired gas mix
            :pp_o2: (float) -- For CCR mode, partial pressure of oxygen in bar.
                               If == 0.0, then open circuit

        *Returns:*
            <nothing>

        *Raise:*
            ModelStateException
        """
        # rem: here we do not bother of PP_H2O like in constant_depth : WHY ?
        start_ambiant_pressure = start + settings.AMBIANT_PRESSURE_SURFACE
        finish_ambiant_pressure = finish + settings.AMBIANT_PRESSURE_SURFACE
        seg_time = abs(float(finish) - float(start)) / rate
        if pp_o2 > 0.0:
            # CCR mode
            # Calculate inert gas partial pressure == pAmb - pO2 - pH2O
            p_inert_start = start_ambiant_pressure - pp_o2 - \
                tools.calculate_pp_h2o_surf(settings.SURFACE_TEMP)
            p_inert_finish = finish_ambiant_pressure - pp_o2 - \
                tools.calculate_pp_h2o_surf(settings.SURFACE_TEMP)
            # Check that it doesn't go less than zero.
            # Could be due to shallow deco or starting on high setpoint
            if p_inert_start < 0.0:
                p_inert_start = 0.0
            if p_inert_finish < 0.0:
                p_inert_finish = 0.0
            # Separate into He and N2 components, checking that we are not
            # on pure O2 (or we get an arithmetic error)
            if f_he + f_n2 > 0.0:
                pp_he_inspired = (p_inert_start * f_he) / (f_he + f_n2)
                pp_n2_inspired = (p_inert_start * f_n2) / (f_he + f_n2)
                # calculate rate of change of each inert gas
                rate_he = ((p_inert_finish * f_he) / (f_he + f_n2) -
                           pp_he_inspired) / (seg_time)
                rate_n2 = ((p_inert_finish * f_n2) / (f_he + f_n2) -
                           pp_n2_inspired) / (seg_time)
            else:
                pp_he_inspired = 0.0
                pp_n2_inspired = 0.0
                rate_he = 0.0
                rate_n2 = 0.0
            # update ox_tox, constant pp_o2
            # TODO - what if depth is less than pO2 in msw ?
            self.ox_tox.add_o2(seg_time, pp_o2)
        else:
            # OC mode
            # calculate He and N2 components
            pp_he_inspired = (start_ambiant_pressure -
                              tools.calculate_pp_h2o_surf(
                                  settings.SURFACE_TEMP)) * f_he
            pp_n2_inspired = (start_ambiant_pressure -
                              tools.calculate_pp_h2o_surf(
                                  settings.SURFACE_TEMP)) * f_n2
            rate_he = rate * f_he
            rate_n2 = rate * f_n2
            # update ox_tox, use average pp_o2
            pp_o2_inspired_avg = ((start_ambiant_pressure -
                                   finish_ambiant_pressure) / 2
                                  + finish_ambiant_pressure -
                                  tools.calculate_pp_h2o_surf(
                                      settings.SURFACE_TEMP)) \
                * (1.0 - f_he - f_n2)
            self.ox_tox.add_o2(seg_time, pp_o2_inspired_avg)

        for comp in self.tissues:
            comp.asc_desc(pp_he_inspired, pp_n2_inspired,
                          rate_he, rate_n2, seg_time)
