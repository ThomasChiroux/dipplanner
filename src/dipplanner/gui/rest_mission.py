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
"""REST Api for Mission object
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]

# dependencies imports
from flask import request
from flask import g as self

# local import
from dipplanner.gui.rest_base import BaseApi
from dipplanner.mission import Mission

class MissionApi(BaseApi):
    """RestFull API for Mission Class

    As is inherit from BaseApi, there is no need to redefine constructor and
    other common methods

    URIs:

    (...)/mission/ : GET, POST, DELETE
    (...)/mission/status : GET
    (...)/mission/commands/calculate : POST
    """
    def get(self, resource_id):
        """GET method for the Mission object Api

        *Keyword Arguments:*
        :resource_id: (str) -- id of the requested resource

        *Returns:*
            resp -- Flask response object

        *Raise:*
            <nothing>
        """
        if resource_id is None:
            return self.json_resp(self.mission.dumps_dict(), 200)
        else:
            if resource_id == 'status':
                return self.json_resp({ 'status': self.mission.status }, 200)
            else:
                return self.json_resp('{ "message": "404: Not found" }', 404)

    def post(self):
        """POST method for the Mission object Api

        create a new (empty) mission
        an new mission may only be created if the existing mission is
        empty (api user MUST call DELETE before calling POST)

        JSON: { "description" : "text describing the mission' }
        (OPTIONAL)



        *Keyword Arguments:*
            <nothing>

        *Returns:*
            resp -- Flask response object with the json dump of the newly
                    created object

        *Raise:*
            <nothing>
        """
        if request.headers['Content-Type'] == 'application/json':
            if self.mission is None or len(self.mission) == 0:
                self.mission = Mission()
                self.mission.loads_json(request.json)
                return self.json_resp(self.mission.dumps_json(), 201)
            else:
                return self.json_resp('{ "message": "403: Forbidden: you MUST '
                                      'delete the current mission before '
                                      'create a new one" }',
                                      403)
        else:
            return self.json_resp('{ "message": "400: Bad ContentType" }',
                                  400)

    def delete(self, resource_id=None):
        """DELETE method for the Mission object Api

        *Keyword Arguments:*
            <none>

        *Returns:*
            resp -- Flask response object (empty)

        *Raise:*
            <nothing>
        """
        print "delete mission !!!!!"
        if resource_id is None:
            print "ok: resource if is none"
            self.mission = None
            print self.mission
            return self.json_resp('{ "message": "204: resource deleted" }',
                                  204)
        else:
            return self.json_resp('{ "message": "404: Not found" }', 404)
