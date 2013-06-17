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
        # start gui in a thread
        #self.thread_server = Thread(
        #    target=start_gui,
        #    kwargs={'mission': self.mission,
        #            'http_host': 'localhost',
        #            'http_port': 8080})
        #self.thread_server.setDaemon(True)
        #self.thread_server.start()
        #time.sleep(1)

    def tearDown(self):
        pass
        #time.sleep(1)
        #server.stop()
        #self.thread_server.join()
        #time.sleep(10)


class TestRestApiBadRessources(TestRestApi):

    def setUp(self):
        super(TestRestApiBadRessources, self).setUp()

    def test_bad_content_type(self):
        r = self.testapp.get(self.base_uri + 'mission/', expect_errors=True)
        self.assertEqual(r.status_int, 400)
        self.assertEqual(r.json['message'], u'400: Bad ContentType')


class testRestApiDefaultUris(TestRestApi):

    def setUp(self):
        super(testRestApiDefaultUris, self).setUp()

    def test_mission_api(self):
        r = self.testapp.get(self.base_uri + 'mission/',
                             headers=self.default_headers)
        self.assertEqual(r.status_int, 200)
        self.assertEqual(
            r.json,
            {u'description': None, u'dives': {}, u'tanks': {}})


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