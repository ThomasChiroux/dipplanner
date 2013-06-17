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

.. todo:: uniquely name the tanks (in addition of tank_id (int)
          AND handle Tank references (from tank list) to:
          current_tank
          and segment.tank

          Actually: each tank is separated

          *WORK IN PROGRESS*
          (reste en cours: les dumps_dict a modifier)

"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]

# dependencies imports
from bottle import debug, run, Bottle, ServerAdapter

# local imports
from dipplanner.mission import Mission
from dipplanner.gui.rest_mission import MissionApiBottle
from dipplanner.gui.rest_dive import DiveApiBottle
from dipplanner.gui.rest_tank import TankApiBottle
from dipplanner.gui.rest_input_segment import InputSegmentApiBottle
from dipplanner.gui.rest_output_segment import OutputSegmentApiBottle
from dipplanner.gui.error_api import ErrorApiBottle


ROOT_API_URL = "/api/v1/"  # TODO: put this in settings?

# class MyWSGIRefServer(ServerAdapter):
#     #server = None

#     def run(self, handler):
#         from wsgiref.simple_server import make_server, WSGIRequestHandler
#         if self.quiet:
#             class QuietHandler(WSGIRequestHandler):
#                 def log_request(*args, **kw): pass
#             self.options['handler_class'] = QuietHandler
#         self.server = make_server(self.host, self.port, handler, **self.options)
#         print("self.server: %s" % self.server)
#         self.server.serve_forever()

#     def stop(self):
#         print('shutting down wsgi server...')
#         self.server.shutdown()  # server_close()

#server = MyWSGIRefServer(host='localhost', port=8080)


def instanciates_app(mission=None):
    """defines all the routes and others parameters for the app
    """
    app = Bottle()

    error_api = ErrorApiBottle()

    if mission is None:
        mission_api = MissionApiBottle(Mission())
    else:
        mission_api = MissionApiBottle(mission)

    dive_api = DiveApiBottle(mission_api.mission)
    tank_api = TankApiBottle(mission_api.mission)
    input_segment_api = InputSegmentApiBottle(mission_api.mission)
    output_segment_api = OutputSegmentApiBottle(mission_api.mission)

    # Mission
    app.route(ROOT_API_URL + 'mission/',
              method='GET')(mission_api.get)
    app.route(ROOT_API_URL + 'mission/status',
              method='GET')(mission_api.get_status)
    app.route(ROOT_API_URL + 'mission/calculate',
              method='POST')(mission_api.calculate)
    app.route(ROOT_API_URL + 'mission/',
              method='POST')(mission_api.post)
    app.route(ROOT_API_URL + 'mission/',
              method='PATCH')(mission_api.patch)
    app.route(ROOT_API_URL + 'mission/',
              method='DELETE')(mission_api.delete)
    # dives
    app.route(ROOT_API_URL + 'mission/dives/',
              method='GET')(dive_api.get)
    app.route(ROOT_API_URL + 'mission/dives/<resource_id>',
              method='GET')(dive_api.get)
    app.route(ROOT_API_URL + 'mission/dives/',
              method='POST')(dive_api.post)
    app.route(ROOT_API_URL + 'mission/dives/<resource_id>',
              method='PATCH')(dive_api.patch)
    app.route(ROOT_API_URL + 'mission/dives/',
              method='DELETE')(dive_api.delete)
    app.route(ROOT_API_URL + 'mission/dives/<resource_id>',
              method='DELETE')(dive_api.delete)

    # tanks
    app.route(ROOT_API_URL + 'mission/dives/<dive_id>/tanks/',
              method='GET')(tank_api.get)
    app.route(ROOT_API_URL + 'mission/dives/<dive_id>/tanks/<tank_id>',
              method='GET')(tank_api.get)
    app.route(ROOT_API_URL + 'mission/dives/<dive_id>/tanks/',
              method='POST')(tank_api.post)
    app.route(ROOT_API_URL + 'mission/dives/<dive_id>/tanks/<tank_id>',
              method='PATCH')(tank_api.patch)
    app.route(ROOT_API_URL + 'mission/dives/<dive_id>/tanks/',
              method='DELETE')(tank_api.delete)
    app.route(ROOT_API_URL + 'mission/dives/<dive_id>/tanks/<tank_id>',
              method='DELETE')(tank_api.delete)

    # input_segments
    app.route(ROOT_API_URL
              + 'mission/dives/<dive_id>/input_segments/',
              method='GET')(input_segment_api.get)
    app.route(ROOT_API_URL
              + 'mission/dives/<dive_id>/input_segments/<segment_id>',
              method='GET')(input_segment_api.get)
    app.route(ROOT_API_URL
              + 'mission/dives/<dive_id>/input_segments/',
              method='POST')(input_segment_api.post)
    app.route(ROOT_API_URL
              + 'mission/dives/<dive_id>/input_segments/<segment_id>',
              method='PATCH')(input_segment_api.patch)
    app.route(ROOT_API_URL
              + 'mission/dives/<dive_id>/input_segments/',
              method='DELETE')(input_segment_api.delete)
    app.route(ROOT_API_URL
              + 'mission/dives/<dive_id>/input_segments/<segment_id>',
              method='DELETE')(input_segment_api.delete)

    # output_segments
    app.route(ROOT_API_URL
              + 'mission/dives/<dive_id>/output_segments/',
              method='GET')(output_segment_api.get)
    app.route(ROOT_API_URL
              + 'mission/dives/<dive_id>/output_segments/<segment_id>',
              method='GET')(output_segment_api.get)

    # custom error handling
    app.error(404)(error_api.error404)
    app.error(405)(error_api.error405)

    return app

def start_gui(mission=None, http_host='locahost', http_port=8080):
    """Starts the html GUI server
    """
    print("Starting Gui on %s:%s" % (http_host, http_port))
    #global server
    #server = MyWSGIRefServer(host=http_host, port=http_port)
    app = instanciates_app(mission)

    debug(True)
    run(app, server=server, host=http_host, port=http_port)
