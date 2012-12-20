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

"""uses config parser to parse config files
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]

import sys
import logging
from collections import OrderedDict
from ConfigParser import SafeConfigParser

# local imports
from dipplanner import settings
from dipplanner.tank import Tank
from dipplanner.dive import Dive
from dipplanner.segment import SegmentDive
from dipplanner.tools import altitude_to_pressure
from dipplanner.tools import safe_eval_calculator

#LOGGER = logging.getLogger("dipplanner")


class DipplannerConfigFiles(object):
    """This class contains all methods and elements to parse the config files
    and launch dipplanner

    Attributes:

    * config: SafeConfigParser object
    * dives: dives dict is in the following form:

        .. code-block:: python

            dives = { 'dive1': { 'tanks': {},
                                 'segments': {},
                                 'surface_interval':0 },
                      'dive2': { 'tanks': {},
                                 'segments': {},
                                 'surface_interval':60 }}
    """

    def __init__(self, mission, filenames):
        """Constructor for DipplannerCliArguments object

        *Keyword Arguments:*
            :mission: -- the current mission object
            :filenames: -- list of filenames to be parsed

        *Returns*
            <nothing>

        """
        self.logger = logging.getLogger("dipplanner")

        self.mission = mission
        self.config = None
        #self.dives = OrderedDict()
        #self.tanks = {}

        if filenames is None:
            self.logger.info("No config file found: skip config from files")
        else:
            self.config = SafeConfigParser()
            filesread = self.config.read(filenames)

            missing = set(filenames) - set(filesread)
            if len(filesread) == 0:
                self.logger.info("No config file found: skip config from files")

            if len(missing) > 0:
                if len(missing) == 1:
                    self.logger.warning("Config file : %s not found, skip it"
                                   % list(missing)[0])
                else:
                    self.logger.warning("Config files : %s not found, skip them"
                                   % ', '.join(str(n) for n in list(missing)))

        if self.config is not None:
            # note: advanced MUST be run before general because of
            # order dependencies of settings elements
            self.parse_config()

    def parse_config(self):
        """Parse the configuration file
        """
        for section in self.config.sections():
            if section == 'advanced':
                self.parse_config_advanced_section(section)
            elif section == 'general':
                self.parse_config_general_section(section)
            elif section == 'output':
                self.parse_config_output_section(section)
            elif section.startswith('tank:'):
                self.parse_config_tank_section(section)
            elif section.startswith('dive:'):
                if len(section.split(':')) > 2 and "segment" in section.lower():
                    self.parse_config_segment_section(section)
                else:
                    self.parse_config_dive_section(section)

    def parse_config_general_section(self, section):
        """check configs and change default settings values

        *Keyword Arguments:*
            :section: config parser's section

        *Returns:*
            <nothing>

        *Raise:*
            Nothing, but can exit
        """
        config = self.config
        if config.has_section('general'):
            section = 'general'
            if config.has_option(section, 'deco_model'):
                model = ''.join(config.get(section, 'deco_model')).strip()
                if model == "ZHL16b" or model == "ZHL16c":
                    settings.DECO_MODEL = model

            if config.has_option(section, 'gf_low'):
                settings.GF_LOW = float(
                    safe_eval_calculator(''.join(config.get(section,
                        'gf_low'))
                    .strip('%'))) / 100

            if config.has_option(section, 'gf_high'):
                settings.GF_HIGH = float(
                    safe_eval_calculator(''.join(config.get(section,
                        'gf_high'))
                    .strip('%'))) / 100

            if config.has_option(section, 'water'):
                if config.get(section, 'water') == 'sea':
                    settings.WATER_DENSITY = settings.SEA_WATER_DENSITY
                elif config.get(section, 'water') == 'fresh':
                    settings.WATER_DENSITY = settings.FRESH_WATER_DENSITY

            if config.has_option(section, 'altitude'):
                settings.AMBIANT_PRESSURE_SURFACE =\
                altitude_to_pressure(float(config.get(section,
                    'altitude')))

            if config.has_option(section, 'dive_consumption_rate'):
                settings.DIVE_CONSUMPTION_RATE =\
                float(config.get(section, 'dive_consumption_rate')) / 60

            if config.has_option(section, 'deco_consumption_rate'):
                settings.DECO_CONSUMPTION_RATE =\
                float(config.get(section, 'deco_consumption_rate')) / 60

            if config.has_option(section, 'descent_rate'):
                settings.DESCENT_RATE = float(
                    config.get(section, 'descent_rate')) / 60

            if config.has_option(section, 'ascent_rate'):
                settings.ASCENT_RATE = float(
                    config.get(section, 'ascent_rate')) / 60

            if config.has_option(section, 'max_ppo2'):
                settings.DEFAULT_MAX_PPO2 = float(config.get(section,
                                                             'max_ppo2'))
            if config.has_option(section, 'min_ppo2'):
                settings.DEFAULT_MIN_PPO2 = float(config.get(section,
                                                             'min_ppo2'))
            if config.has_option(section, 'max_end'):
                settings.DEFAULT_MAX_END = float(config.get(section,
                                                            'max_end'))

            if config.has_option(section, 'run_time'):
                settings.RUN_TIME = config.getboolean(section, 'run_time')

            if config.has_option(section, 'use_oc_deco'):
                settings.USE_OC_DECO = config.getboolean(section,
                                                         'use_oc_deco')

            if config.has_option(section, 'multilevel_mode'):
                settings.MULTILEVEL_MODE = config.getboolean(section,
                                                             'multilevel_mode')

            if config.has_option(section, 'automatic_tank_refill'):
                settings.AUTOMATIC_TANK_REFILL = \
                    config.getboolean(section,
                                      'automatic_tank_refill')

    def parse_config_advanced_section(self, section):
        """check configs and change default settings values

        *Keyword Arguments:*
            :section: config parser's section

        *Returns:*
            <nothing>

        *Raise:*
            Nothing, but can exit
        """
        # now try to find each parameter and set the new setting
        config = self.config
        if config.has_section('advanced'):
            section = 'advanced'
            if config.has_option(section, 'fresh_water_density'):
                settings.FRESH_WATER_DENSITY = float(
                    config.get(section, 'fresh_water_density'))
            if config.has_option(section, 'sea_water_density'):
                settings.SEA_WATER_DENSITY = float(
                    config.get(section, 'sea_water_density'))
            if config.has_option(section, 'absolute_max_ppo2'):
                settings.ABSOLUTE_MAX_PPO2 = float(
                    config.get(section, 'absolute_max_ppo2'))
            if config.has_option(section, 'absolute_min_ppo2'):
                settings.ABSOLUTE_MIN_PPO2 = float(
                    config.get(section, 'absolute_min_ppo2'))
            if config.has_option(section, 'absolute_max_pressure'):
                settings.ABSOLUTE_MAX_pressure = float(
                    config.get(section, 'absolute_max_pressure'))
            if config.has_option(section, 'absolute_max_tank_size'):
                settings.ABSOLUTE_MAX_TANK_SIZE = float(
                    config.get(section, 'absolute_max_tank_size'))

            if config.has_option(section, 'surface_temp'):
                settings.SURFACE_TEMP = float(config.get(section,
                                                         'surface_temp'))
            if config.has_option(section, 'he_narcotic_value'):
                settings.HE_NARCOTIC_VALUE = float(
                    config.get(section, 'he_narcotic_value'))
            if config.has_option(section, 'n2_narcotic_value'):
                settings.N2_NARCOTIC_VALUE = float(
                    config.get(section, 'n2_narcotic_value'))
            if config.has_option(section, 'o2_narcotic_value'):
                settings.O2_NARCOTIC_VALUE = float(
                    config.get(section, 'o2_narcotic_value'))
            if config.has_option(section, 'ar_narcotic_value'):
                settings.AR_NARCOTIC_VALUE = float(
                    config.get(section, 'ar_narcotic_value'))

            if config.has_option(section, 'stop_depth_increment'):
                settings.STOP_DEPTH_INCREMENT = float(
                    config.get(section, 'stop_depth_increment'))
            if config.has_option(section, 'last_stop_depth'):
                settings.LAST_STOP_DEPTH = float(
                    config.get(section, 'last_stop_depth'))
            if config.has_option(section, 'stop_time_increment'):
                settings.STOP_TIME_INCREMENT = float(
                    config.get(section, 'stop_time_increment'))
            if config.has_option(section, 'force_all_stops'):
                settings.FORCE_ALL_STOPS = config.getboolean(section,
                                                             'force_all_stops')
            if config.has_option(section, 'ambiant_pressure_sea_level'):
                settings.AMBIANT_PRESSURE_SEA_LEVEL = float(
                    config.get(section, 'ambiant_pressure_sea_level'))
            if config.has_option(section, 'method_for_depth_calculation'):
                method = config.get(section, 'method_for_depth_calculation')
                if method == 'simple' or method == 'complex':
                    settings.METHOD_FOR_DEPTH_CALCULATION = method
            if config.has_option(section, 'travel_switch'):
                travel = config.get(section, 'travel_switch')
                if travel == 'late' or travel == 'early':
                    settings.TRAVEL_SWITCH = travel
            if config.has_option(section, 'flight_altitude'):
                settings.FLIGHT_ALTITUDE = float(
                    config.get(section, 'flight_altitude'))

    def parse_config_output_section(self, section):
        """check configs and change default settings values

        *Keyword Arguments:*
            :section: config parser's section

        *Returns:*
            <nothing>

        *Raise:*
            Nothing, but can exit
        """
        config = self.config
        if config.has_section('output'):
            section = 'output'
            if config.has_option(section, 'template'):
                settings.TEMPLATE = config.get(section, 'template')

    def parse_config_tank_section(self, section):
        """check configs and change default settings values

        *Keyword Arguments:*
            :section: config parser's section

        *Returns:*
            <nothing>

        *Raise:*
            Nothing, but can exit
        """
        tank_dict = dict(self.config.items(section))
        tank_dict['name'] = section.split("tank:")[-1].lower()
        tank = Tank()
        tank.loads_json(tank_dict)
        if tank.name not in self.mission.tanks:
            self.mission.tanks[tank.name] = tank
        else:
            self.logger.error("Tank already exists with the same name: %s"
                              % tank.name)

    def parse_config_dive_section(self, section):
        """check configs and change default settings values

        *Keyword Arguments:*
            :section: config parser's section

        *Returns:*
            <nothing>

        *Raise:*
            Nothing, but can exit
        """
        dive_dict = dict(self.config.items(section))
        dive_dict['name'] = section.split("dive:")[-1].lower().split(':')[0]
        dive = Dive(self.mission)
        dive.loads_json(dive_dict)

        self.mission.add_dive(dive)

    def parse_config_segment_section(self, section):
        """check configs and change default settings values

        *Keyword Arguments:*
            :section: config parser's section

        *Returns:*
            <nothing>

        *Raise:*
            Nothing, but can exit
        """
        segment_dict = dict(self.config.items(section))
        segment_dict['name'] = section.split(":")[-1].lower()
        dive_name = section.split("dive:")[-1].lower().split(':')[0]
        segment = SegmentDive()
        segment.dive = self.mission.dives[dive_name]
        segment.loads_json(segment_dict)
        self.mission.dives[dive_name].add_input_segment(segment)
