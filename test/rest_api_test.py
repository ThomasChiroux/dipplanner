#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2011 Thomas Chiroux
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
"""
Test for REST API
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]

import time
from threading import Thread
import unittest

from webtest import TestApp

# import here the module / classes to be tested
from dipplanner.main import activate_debug_for_tests
from dipplanner.mission import Mission
from dipplanner.gui import instanciates_app
#from dipplanner.gui import start_gui, app, server


class TestRestApi(unittest.TestCase):

    def setUp(self):
        # temporary hack (tests):
        activate_debug_for_tests()
        self.default_headers = {'content-type': 'application/json'}
        self.base_uri = 'http://localhost:8080/api/v1/'
        self.mission = Mission()

        self.app = instanciates_app(self.mission)
        self.testapp = TestApp(self.app)

        self.tank_json_1 = {u'automatic_name': u'Nitrox 80',
                            u'f_he': 0.0,
                            u'f_n2': 0.2,
                            u'f_o2': 0.8,
                            u'in_use': True,
                            u'max_ppo2': 1.6,
                            u'min_gas': 621.2968024772183,
                            u'mod': 10.0,
                            u'name': u'decotank',
                            u'pressure': 200.0,
                            u'remaining_gas': 2374.0258146129518,
                            u'rule': u'50b',
                            u'total_gas': 2602.167779412952,
                            u'used_gas': 228.1419648,
                            u'volume': 12.0}

    def tearDown(self):
        pass


class TestRestApiBadRessources(TestRestApi):

    def setUp(self):
        super(TestRestApiBadRessources, self).setUp()

    def test_bad_content_type(self):
        r = self.testapp.get(self.base_uri + 'mission/', expect_errors=True)
        self.assertEqual(r.status_int, 400)
        self.assertEqual(r.json['message'], u'400: Bad ContentType')


class testRestApiMission(TestRestApi):

    def setUp(self):
        super(testRestApiMission, self).setUp()

    def test_mission_api_base(self):
        r = self.testapp.get(self.base_uri + 'mission/',
                             headers=self.default_headers)
        self.assertEqual(r.status_int, 200)
        self.assertEqual(
            r.json,
            {u'description': None, u'dives': {}, u'tanks': {}})

    def test_mission_api_status(self):
        r = self.testapp.get(self.base_uri + 'mission/status',
                             headers=self.default_headers)
        self.assertEqual(r.status_int, 200)
        self.assertEqual(
            r.json,
            {u'status': u'Not Calculated'})

    def test_mission_api_get_calculate(self):
        r = self.testapp.get(self.base_uri + 'mission/calculate',
                             headers=self.default_headers,
                             expect_errors=True)
        self.assertEqual(r.status_int, 405)
        self.assertEqual(
            r.json,
            {u'message': u'405 Method not allowed'})

    def test_mission_api_post_calculate(self):
        """This test will still return 'not calculated' because we did not
        populate any dive to be calculated
        """
        r = self.testapp.post(self.base_uri + 'mission/calculate',
                              headers=self.default_headers)
        self.assertEqual(r.status_int, 200)
        self.assertEqual(
            r.json,
            {u'status': u'Not Calculated'})


class testRestApiTanks(TestRestApi):

    def setUp(self):
        super(testRestApiTanks, self).setUp()

    def test_tanks_api_base(self):
        """should return an empty tank list
        """
        r = self.testapp.get(self.base_uri + 'mission/tanks/',
                             headers=self.default_headers)
        self.assertEqual(r.status_int, 200)
        self.assertEqual(
            r.json,
            {})

    def test_tanks_api_post(self):
        r = self.testapp.post_json(self.base_uri + 'mission/tanks/',
                                   self.tank_json_1)
        self.assertEqual(r.status_int, 201)
        self.assertEqual(r.json, self.tank_json_1)


    def test_tanks_api_post2(self):
        r = self.testapp.post_json(self.base_uri + 'mission/tanks/',
                                   self.tank_json_1)
        self.assertEqual(r.status_int, 201)
        self.assertEqual(r.json, self.tank_json_1)
        r2 = self.testapp.post_json(self.base_uri + 'mission/tanks/',
                                    self.tank_json_1,
                                    expect_errors=True)
        self.assertEqual(r2.status_int, 400)
        self.assertEqual(r2.json, {'message':
                                   '400: Tank with same name already created'})

    def test_tank_api_patch1(self):
        r = self.testapp.post_json(self.base_uri + 'mission/tanks/',
                                   self.tank_json_1)
        self.assertEqual(r.status_int, 201)
        self.assertEqual(r.json, self.tank_json_1)
        patched_data = {u'f_o2': 0.5,
                        u'f_n2': 0.5,
                        u'f_he': 0.0}
        r2 = self.testapp.patch_json(self.base_uri + 'mission/tanks/decotank',
                                     patched_data)
        self.assertEqual(r2.status_int, 200)
        self.assertEqual(r2.json, {u'automatic_name': u'Nitrox 50',
                                   u'f_he': 0.0,
                                   u'f_n2': 0.5,
                                   u'f_o2': 0.5,
                                   u'in_use': True,
                                   u'max_ppo2': 1.6,
                                   u'min_gas': 621.2968024772183,
                                   u'mod': 22.0,
                                   u'name': u'decotank',
                                   u'pressure': 200.0,
                                   u'remaining_gas': 2374.0258146129518,
                                   u'rule': u'50b',
                                   u'total_gas': 2602.167779412952,
                                   u'used_gas': 228.1419648,
                                   u'volume': 12.0})

# =============================================================================
# ========================= M A I N ===========================================
# =============================================================================
def main():
    import sys
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('tests',
                        metavar='TestName',
                        type=str,
                        nargs='*',
                        help='name of the tests to run (separated by space)'
                        ' [optionnal]')
    args = parser.parse_args()
    if args.tests:
        suite = unittest.TestLoader().loadTestsFromNames(args.tests,
                                                         sys.modules[__name__])
    else:
        suite = unittest.findTestCases(sys.modules[__name__])
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    main()