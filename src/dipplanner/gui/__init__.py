#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2011-2012 Thomas Chiroux
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.
# If not, see <http://www.gnu.org/licenses/lgpl-3.0.html>
#
# This module is part of dipplanner, a Dive planning Tool written in python
"""dipplanner GUI module.

Starts the GUI
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]

# dependencies imports
import bottle
from bottle import error, response

# local imports
from dipplanner.mission import Mission
from dipplanner.gui.rest_mission import MissionApiBottle
from dipplanner.gui.rest_dive import DiveApiBottle
from dipplanner.gui.error_api import ErrorApiBottle


ROOT_API_URL = "/api/v1/"


def start_gui(mission=None):
    """Starts the html GUI server
    """
    error_api = ErrorApiBottle()

    if mission is None:
        mission_api = MissionApiBottle(Mission())
    else:
        mission_api = MissionApiBottle(mission)

    dive_api = DiveApiBottle(mission_api.mission)
    #tank_api = TankApiBottle(mission_api.mission)
    #segment_api = SegmentApiBottle(mission_api_mission)

    app = bottle.Bottle()
    # Mission
    app.route(ROOT_API_URL+'mission/',
              method='GET')(mission_api.get)
    app.route(ROOT_API_URL+'mission/status',
              method='GET')(mission_api.get_status)
    app.route(ROOT_API_URL+'mission/calculate',
              method='POST')(mission_api.calculate)
    app.route(ROOT_API_URL+'mission/',
              method='POST')(mission_api.post)
    app.route(ROOT_API_URL+'mission/',
              method='PATCH')(mission_api.patch)
    app.route(ROOT_API_URL+'mission/',
              method='DELETE')(mission_api.delete)
    # dives
    app.route(ROOT_API_URL+'mission/dives/',
              method='GET')(dive_api.get)
    app.route(ROOT_API_URL+'mission/dives/<resource_id>',
              method='GET')(dive_api.get)
    app.route(ROOT_API_URL+'mission/dives/',
              method='POST')(dive_api.post)
    app.route(ROOT_API_URL+'mission/dives/<resource_id>',
              method='PATCH')(dive_api.patch)
    app.route(ROOT_API_URL+'mission/dives/',
              method='DELETE')(dive_api.delete)
    app.route(ROOT_API_URL+'mission/dives/<resource_id>',
              method='DELETE')(dive_api.delete)

    app.error(404)(error_api.error404)
    app.error(405)(error_api.error405)

    bottle.debug(True)
    bottle.run(app, host='localhost', port=8080)
