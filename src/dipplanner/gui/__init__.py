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
"""dipplanner module
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]

# dependencies imports
from flask import Flask

# local imports
from dipplanner.mission import Mission
from dipplanner.gui.rest_mission import MissionApi

WEBAPP = Flask(__name__)

def start_gui(mission=None):
    """Starts the html GUI server
    """
    if mission is None:
        mission_api = MissionApi('mission', Mission())
    else:
        mission_api = MissionApi('mission', mission)
    WEBAPP.register_blueprint(mission_api._blueprint)
    WEBAPP.run(debug=True)  # TODO: remove debug infos before release
