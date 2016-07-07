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
# pylint: disable=too-many-public-methods, protected-access, no-self-use
# pylint: disable=too-few-public-methods, duplicate-code, invalid-name
# pylint: disable=too-many-ancestors, attribute-defined-outside-init
# pylint: disable=missing-docstring
"""Test for main: arguments in command line and config files."""
import unittest
# import here the module / classes to be tested
from dipplanner import settings
from dipplanner.main import activate_debug_for_tests
from dipplanner.parse_cli_args import DipplannerCliArguments
from dipplanner.tools import altitude_to_pressure


class TestCliArguments(unittest.TestCase):
    def setUp(self):
        # temporary hack (tests):
        activate_debug_for_tests()


class TestAllCli(TestCliArguments):

    def setUp(self):
        TestCliArguments.setUp(self)

    @classmethod
    def tearDownClass(cls):
        cli_args = ["dipplanner",
                    "-t", "airtank;0.21;0.0;12;200;50b",
                    "-s", "30;25*60;airtank;0.0",
                    "-c", "test/configs/restore_default_config.cfg",
                    "-c", "configs/restore_default_config.cfg", ]
        DipplannerCliArguments(cli_args)

    def test_surfaceinterval(self):
        cli_args = ["dipplanner",
                    "-t", "airtank;0.21;0.0;12;200;50b",
                    "-s", "30;25*60;airtank;0.0",
                    "--surfaceinterval=200", ]
        dipplanner_arguments = DipplannerCliArguments(cli_args)
        dives = dipplanner_arguments.dives
        args = dipplanner_arguments.args
        self.assertEqual(dives['diveCLI']['surface_interval'], 200,
                         "Wrong surface interval: %s" % args.surfaceinterval)

    def test_deco_model(self):
        cli_args = ["dipplanner",
                    "-t", "airtank;0.21;0.0;12;200;50b",
                    "-s", "30;25*60;airtank;0.0",
                    "--model=ZHL16b", ]
        _ = DipplannerCliArguments(cli_args)
        self.assertEqual(settings.DECO_MODEL, 'ZHL16b',
                         "Wrong model: %s" % settings.DECO_MODEL)

    def test_gflow(self):
        cli_args = ["dipplanner",
                    "-t", "airtank;0.21;0.0;12;200;50b",
                    "-s", "30;25*60;airtank;0.0",
                    "--gflow=22%", ]
        _ = DipplannerCliArguments(cli_args)
        self.assertEqual(settings.GF_LOW, 0.22,
                         "Wrong gllow: %s" % settings.GF_LOW)

    def test_gfhigh(self):
        cli_args = ["dipplanner",
                    "-t", "airtank;0.21;0.0;12;200;50b",
                    "-s", "30;25*60;airtank;0.0",
                    "--gfhigh=95", ]
        _ = DipplannerCliArguments(cli_args)
        self.assertEqual(settings.GF_HIGH, 0.95,
                         "Wrong gfhigh: %s" % settings.GF_HIGH)

    def test_water(self):
        cli_args = ["dipplanner",
                    "-t", "airtank;0.21;0.0;12;200;50b",
                    "-s", "30;25*60;airtank;0.0",
                    "--water=fresh", ]
        _ = DipplannerCliArguments(cli_args)
        self.assertEqual(settings.WATER_DENSITY,
                         settings.FRESH_WATER_DENSITY,
                         "Wrong water type: %s" % settings.WATER_DENSITY)

    def test_altitude(self):
        cli_args = ["dipplanner",
                    "-t", "airtank;0.21;0.0;12;200;50b",
                    "-s", "30;25*60;airtank;0.0",
                    "--altitude=2456", ]
        _ = DipplannerCliArguments(cli_args)
        self.assertEqual(settings.AMBIANT_PRESSURE_SURFACE,
                         altitude_to_pressure(2456),
                         "Wrong altitude pressure: %s" %
                         settings.AMBIANT_PRESSURE_SURFACE)

    def test_diveconsrate(self):
        cli_args = ["dipplanner",
                    "-t", "airtank;0.21;0.0;12;200;50b",
                    "-s", "30;25*60;airtank;0.0",
                    "--diveconsrate=23", ]
        _ = DipplannerCliArguments(cli_args)
        self.assertEqual(settings.DIVE_CONSUMPTION_RATE,
                         23.0/60,
                         "Wrong diveconsrate: %s" %
                         settings.DIVE_CONSUMPTION_RATE)

    def test_decoconsrate(self):
        cli_args = ["dipplanner",
                    "-t", "airtank;0.21;0.0;12;200;50b",
                    "-s", "30;25*60;airtank;0.0",
                    "--decoconsrate=21", ]
        _ = DipplannerCliArguments(cli_args)
        self.assertEqual(settings.DECO_CONSUMPTION_RATE,
                         21.0/60,
                         "Wrong decoconsrate: %s" %
                         settings.DECO_CONSUMPTION_RATE)

    def test_descentrate(self):
        cli_args = ["dipplanner",
                    "-t", "airtank;0.21;0.0;12;200;50b",
                    "-s", "30;25*60;airtank;0.0",
                    "--descentrate=42", ]
        _ = DipplannerCliArguments(cli_args)
        self.assertEqual(settings.DESCENT_RATE,
                         42.0/60,
                         "Wrong descentrate: %s" % settings.DESCENT_RATE)

    def test_ascentrate(self):
        cli_args = ["dipplanner",
                    "-t", "airtank;0.21;0.0;12;200;50b",
                    "-s", "30;25*60;airtank;0.0",
                    "--ascentrate=9", ]
        _ = DipplannerCliArguments(cli_args)
        self.assertEqual(settings.ASCENT_RATE,
                         9.0/60,
                         "Wrong ascentrate: %s" % settings.ASCENT_RATE)

    def test_deco_ascentrate(self):
        cli_args = ["dipplanner",
                    "-t", "airtank;0.21;0.0;12;200;50b",
                    "-s", "30;25*60;airtank;0.0",
                    "--deco-ascentrate=4", ]
        _ = DipplannerCliArguments(cli_args)
        self.assertEqual(settings.DECO_ASCENT_RATE,
                         4.0/60,
                         "Wrong deco_ascentrate: %s" %
                         settings.DECO_ASCENT_RATE)

    def test_mawppo2(self):
        cli_args = ["dipplanner",
                    "-t", "airtank;0.21;0.0;12;200;50b",
                    "-s", "30;25*60;airtank;0.0",
                    "--maxppo2=1.5", ]
        _ = DipplannerCliArguments(cli_args)
        self.assertEqual(settings.DEFAULT_MAX_PPO2,
                         1.5,
                         "Wrong mawppo2: %s" %
                         settings.DEFAULT_MAX_PPO2)

    def test_minppo2(self):
        cli_args = ["dipplanner",
                    "-t", "airtank;0.21;0.0;12;200;50b",
                    "-s", "30;25*60;airtank;0.0",
                    "--minppo2=0.17", ]
        _ = DipplannerCliArguments(cli_args)
        self.assertEqual(settings.DEFAULT_MIN_PPO2,
                         0.17,
                         "Wrong minppo2: %s" %
                         settings.DEFAULT_MIN_PPO2)

    def test_maxend(self):
        cli_args = ["dipplanner",
                    "-t", "airtank;0.21;0.0;12;200;50b",
                    "-s", "30;25*60;airtank;0.0",
                    "--maxend=33", ]
        _ = DipplannerCliArguments(cli_args)
        self.assertEqual(settings.DEFAULT_MAX_END,
                         33,
                         "Wrong maxend: %s" %
                         settings.DEFAULT_MAX_END)

    def test_samegasdeco(self):
        cli_args = ["dipplanner",
                    "-t", "airtank;0.21;0.0;12;200;50b",
                    "-s", "30;25*60;airtank;0.0",
                    "--samegasfordeco", ]
        _ = DipplannerCliArguments(cli_args)
        self.assertEqual(settings.USE_OC_DECO,
                         False,
                         "Wrong samegasfordeco: %s" %
                         settings.USE_OC_DECO)

    def test_forcesegmenttime(self):
        cli_args = ["dipplanner",
                    "-t", "airtank;0.21;0.0;12;200;50b",
                    "-s", "30;25*60;airtank;0.0",
                    "--forcesegmenttime", ]
        _ = DipplannerCliArguments(cli_args)
        self.assertEqual(settings.RUN_TIME,
                         False,
                         "Wrong forcesegmenttime: %s" %
                         settings.RUN_TIME)

    def test_depthcalcmethod(self):
        cli_args = ["dipplanner",
                    "-t", "airtank;0.21;0.0;12;200;50b",
                    "-s", "30;25*60;airtank;0.0",
                    "--depthcalcmethod=simple", ]
        _ = DipplannerCliArguments(cli_args)
        self.assertEqual(settings.METHOD_FOR_DEPTH_CALCULATION,
                         'simple',
                         "Wrong depthcalcmethod: %s" %
                         settings.METHOD_FOR_DEPTH_CALCULATION)

    def test_travelswitch(self):
        cli_args = ["dipplanner",
                    "-t", "airtank;0.21;0.0;12;200;50b",
                    "-s", "30;25*60;airtank;0.0",
                    "--travelswitch=early", ]
        _ = DipplannerCliArguments(cli_args)
        self.assertEqual(settings.TRAVEL_SWITCH,
                         'early',
                         "Wrong travelswitch: %s" %
                         settings.TRAVEL_SWITCH)

    def test_surfacetemp_1(self):
        cli_args = ["dipplanner",
                    "-t", "airtank;0.21;0.0;12;200;50b",
                    "-s", "30;25*60;airtank;0.0",
                    "--surfacetemp=24.5", ]
        _ = DipplannerCliArguments(cli_args)
        self.assertEqual(settings.SURFACE_TEMP,
                         24.5,
                         "Wrong surfacetemp: %s" %
                         settings.SURFACE_TEMP)

    def test_surfacetemp_2(self):
        cli_args = ["dipplanner",
                    "-t", "airtank;0.21;0.0;12;200;50b",
                    "-s", "30;25*60;airtank;0.0",
                    "--surfacetemp=29", ]
        _ = DipplannerCliArguments(cli_args)
        self.assertEqual(settings.SURFACE_TEMP,
                         29,
                         "Wrong surfacetemp: %s" %
                         settings.SURFACE_TEMP)

    def test_ambiantpressureatsea(self):
        cli_args = ["dipplanner",
                    "-t", "airtank;0.21;0.0;12;200;50b",
                    "-s", "30;25*60;airtank;0.0",
                    "--ambiantpressureatsea=1.01", ]
        _ = DipplannerCliArguments(cli_args)
        self.assertEqual(settings.AMBIANT_PRESSURE_SEA_LEVEL,
                         1.01,
                         "Wrong ambiantpressureatsea: %s" %
                         settings.AMBIANT_PRESSURE_SEA_LEVEL)

    def test_template(self):
        cli_args = ["dipplanner",
                    "-t", "airtank;0.21;0.0;12;200;50b",
                    "-s", "30;25*60;airtank;0.0",
                    "--template=default.html", ]
        _ = DipplannerCliArguments(cli_args)
        self.assertEqual(settings.TEMPLATE,
                         'default.html',
                         "Wrong template: %s" %
                         settings.TEMPLATE)


class TestAllConfig(TestCliArguments):

    def setUp(self):
        TestCliArguments.setUp(self)
        cli_args = ["dipplanner",
                    "-t", "airtank;0.21;0.0;12;200;50b",
                    "-s", "30;25*60;airtank;0.0",
                    "-c", "dipplanner/tests/configs/test_config.cfg",
                    "-c", "configs/test_config.cfg", ]

        dipplanner_arguments = DipplannerCliArguments(cli_args)
        self.dives = dipplanner_arguments.dives
        self.args = dipplanner_arguments.args

    @classmethod
    def tearDownClass(cls):
        cli_args = [
            "dipplanner",
            "-t", "airtank;0.21;0.0;12;200;50b",
            "-s", "30;25*60;airtank;0.0",
            "-c", "dipplanner/tests/configs/restore_default_config.cfg",
            "-c", "configs/restore_default_config.cfg", ]

        DipplannerCliArguments(cli_args)

    def test_surfaceinterval(self):
        self.assertEqual(self.dives['dive2']['surface_interval'], 98 * 60,
                         "Wrong surface interval: %s" %
                         self.dives['dive2']['surface_interval'])

    def test_deco_model(self):
        self.assertEqual(settings.DECO_MODEL, 'ZHL16b',
                         "Wrong model: %s" % settings.DECO_MODEL)

    def test_gflow(self):
        self.assertEqual(settings.GF_LOW, 0.35,
                         "Wrong gllow: %s" % settings.GF_LOW)

    def test_gfhigh(self):
        self.assertEqual(settings.GF_HIGH, 0.85,
                         "Wrong gfhigh: %s" % settings.GF_HIGH)

    def test_water(self):
        self.assertEqual(settings.WATER_DENSITY,
                         settings.FRESH_WATER_DENSITY,
                         "Wrong water type: %s" % settings.WATER_DENSITY)

    def test_altitude(self):
        self.assertEqual(settings.AMBIANT_PRESSURE_SURFACE,
                         altitude_to_pressure(1234),
                         "Wrong altitude pressure: %s" %
                         settings.AMBIANT_PRESSURE_SURFACE)

    def test_diveconsrate(self):
        self.assertEqual(settings.DIVE_CONSUMPTION_RATE,
                         27.0/60,
                         "Wrong diveconsrate: %s" %
                         settings.DIVE_CONSUMPTION_RATE)

    def test_decoconsrate(self):
        self.assertEqual(settings.DECO_CONSUMPTION_RATE,
                         22.0/60,
                         "Wrong decoconsrate: %s" %
                         settings.DECO_CONSUMPTION_RATE)

    def test_descentrate(self):
        self.assertEqual(settings.DESCENT_RATE,
                         32.0/60,
                         "Wrong descentrate: %s" % settings.DESCENT_RATE)

    def test_ascentrate(self):
        self.assertEqual(settings.ASCENT_RATE,
                         8.0/60,
                         "Wrong ascentrate: %s" % settings.ASCENT_RATE)

    def test_deco_ascentrate(self):
        self.assertEqual(settings.DECO_ASCENT_RATE,
                         4.0/60,
                         "Wrong ascentrate: %s" % settings.DECO_ASCENT_RATE)

    def test_mawppo2(self):
        self.assertEqual(settings.DEFAULT_MAX_PPO2,
                         1.5,
                         "Wrong mawppo2: %s" % settings.DEFAULT_MAX_PPO2)

    def test_minppo2(self):
        self.assertEqual(settings.DEFAULT_MIN_PPO2,
                         0.19,
                         "Wrong minppo2: %s" % settings.DEFAULT_MIN_PPO2)

    def test_maxend(self):
        self.assertEqual(settings.DEFAULT_MAX_END,
                         33,
                         "Wrong maxend: %s" % settings.DEFAULT_MAX_END)

    def test_samegasdeco(self):
        self.assertEqual(settings.USE_OC_DECO,
                         False,
                         "Wrong samegasfordeco: %s" % settings.USE_OC_DECO)

    def test_forcesegmenttime(self):
        self.assertEqual(settings.RUN_TIME,
                         False,
                         "Wrong forcesegmenttime: %s" % settings.RUN_TIME)

    def test_depthcalcmethod(self):
        self.assertEqual(settings.METHOD_FOR_DEPTH_CALCULATION,
                         'simple',
                         "Wrong depthcalcmethod: %s" %
                         settings.METHOD_FOR_DEPTH_CALCULATION)

    def test_travelswitch(self):
        self.assertEqual(settings.TRAVEL_SWITCH,
                         'early',
                         "Wrong travelswitch: %s" % settings.TRAVEL_SWITCH)

    def test_surfacetemp(self):
        self.assertEqual(settings.SURFACE_TEMP,
                         29,
                         "Wrong surfacetemp: %s" % settings.SURFACE_TEMP)

    def test_ambiantpressureatsea(self):
        self.assertEqual(settings.AMBIANT_PRESSURE_SEA_LEVEL,
                         1.099,
                         "Wrong ambiantpressureatsea: %s" %
                         settings.AMBIANT_PRESSURE_SEA_LEVEL)

    def test_template(self):
        self.assertEqual(settings.TEMPLATE,
                         'default.html',
                         "Wrong template: %s" % settings.TEMPLATE)

    def test_automatictankrefill(self):
        self.assertEqual(settings.AUTOMATIC_TANK_REFILL,
                         False,
                         "Wrong automatic tank refill: %s" %
                         settings.AUTOMATIC_TANK_REFILL)

    def test_fresh_water_density(self):
        self.assertEqual(settings.FRESH_WATER_DENSITY,
                         0.999,
                         "Wrong fresh_water_density: %s" %
                         settings.FRESH_WATER_DENSITY)

    def test_sea_water_density(self):
        self.assertEqual(settings.SEA_WATER_DENSITY,
                         1.099,
                         "Wrong sea_water_density: %s" %
                         settings.SEA_WATER_DENSITY)

    def test_absolute_max_ppo2(self):
        self.assertEqual(settings.ABSOLUTE_MAX_PPO2,
                         1.999,
                         "Wrong absolute_max_ppo2: %s" %
                         settings.ABSOLUTE_MAX_PPO2)

    def test_absolute_min_ppo2(self):
        self.assertEqual(settings.ABSOLUTE_MIN_PPO2,
                         0.1599,
                         "Wrong absolute_min_ppo2: %s" %
                         settings.ABSOLUTE_MIN_PPO2)

    def test_absolute_max_tank_pressure(self):
        self.assertEqual(settings.ABSOLUTE_MAX_TANK_PRESSURE,
                         299,
                         "Wrong absolute_max_tank_pressure: %s" %
                         settings.ABSOLUTE_MAX_TANK_PRESSURE)

    def test_absolute_max_tank_size(self):
        self.assertEqual(settings.ABSOLUTE_MAX_TANK_SIZE,
                         39,
                         "Wrong absolute_max_tank_size: %s" %
                         settings.ABSOLUTE_MAX_TANK_SIZE)

    def test_he_narcotic_value(self):
        self.assertEqual(settings.HE_NARCOTIC_VALUE,
                         0.29,
                         "Wrong he_narcotic_value: %s" %
                         settings.HE_NARCOTIC_VALUE)

    def test_n2_narcotic_value(self):
        self.assertEqual(settings.N2_NARCOTIC_VALUE,
                         0.99,
                         "Wrong n2_narcotic_value: %s" %
                         settings.N2_NARCOTIC_VALUE)

    def test_o2_narcotic_value(self):
        self.assertEqual(settings.O2_NARCOTIC_VALUE,
                         0.99,
                         "Wrong o2_narcotic_value: %s" %
                         settings.O2_NARCOTIC_VALUE)

    def test_ar_narcotic_value(self):
        self.assertEqual(settings.AR_NARCOTIC_VALUE,
                         2.299,
                         "Wrong ar_narcotic_value: %s" %
                         settings.AR_NARCOTIC_VALUE)

    def test_stop_depth_increment(self):
        self.assertEqual(settings.STOP_DEPTH_INCREMENT,
                         2,
                         "Wrong stop_depth_increment: %s" %
                         settings.STOP_DEPTH_INCREMENT)

    def test_last_stop_depth(self):
        self.assertEqual(settings.LAST_STOP_DEPTH,
                         2,
                         "Wrong last_stop_depth: %s" %
                         settings.LAST_STOP_DEPTH)

    def test_stop_time_increment(self):
        self.assertEqual(settings.STOP_TIME_INCREMENT,
                         5,
                         "Wrong stop_time_increment: %s" %
                         settings.STOP_TIME_INCREMENT)

    def test_force_all_stops(self):
        self.assertEqual(settings.FORCE_ALL_STOPS,
                         False,
                         "Wrong force_all_stops: %s" %
                         settings.FORCE_ALL_STOPS)

    def test_flight_altitude(self):
        self.assertEqual(settings.FLIGHT_ALTITUDE,
                         2699,
                         "Wrong flight_altitude: %s" %
                         settings.FLIGHT_ALTITUDE)
