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

.. todo:: define a custom (json) 404 error
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]

# dependencies imports
import bottle

# local imports
from dipplanner.mission import Mission
from dipplanner.gui.rest_mission import MissionApiBottle


ROOT_API_URL = "/api/v1/"


def start_gui(mission=None):
    """Starts the html GUI server
    """
    if mission is None:
        mission_api = MissionApiBottle(Mission())
    else:
        mission_api = MissionApiBottle(mission)

    app = bottle.Bottle()
    app.route(ROOT_API_URL+'mission/',
              method='GET')(mission_api.get)
    app.route(ROOT_API_URL+'mission/status',
              method='GET')(mission_api.get_status)
    app.route(ROOT_API_URL+'mission/calculate',
              method='POST')(mission_api.calculate)
    app.route(ROOT_API_URL+'mission/',
              method='POST')(mission_api.post)
    app.route(ROOT_API_URL+'mission/',
              method='DELETE')(mission_api.delete)


    bottle.debug(True)
    bottle.run(app, host='localhost', port=8080)
