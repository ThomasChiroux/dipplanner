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
"""
REST Api for Mission object
=--------------------------

"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]

# dependencies imports
from bottle import request, response

# local import
from dipplanner.mission import Mission


class MissionApiBottle(object):
    """At this time, there is only one Mission at a time for a dipplanner session
    (if the user need to work on another mission, he MUST close the current
    Mission first).

    The API reflects this current limitation
    """

    def __init__(self, mission=None):
        self.mission = mission

    def json_abort(self, code, message):
        response.set_header("Content-Type", "application/json")
        response.status = code
        #response.body = { 'message': message}
        return { 'message': message }

    def get(self):
        """GET method for the Mission object Api

        returns a json dumps of the mission object.

        *Keyword Arguments:*
            <none>

        *Returns:*
            resp -- response object with the json dump of the mission object

        *Raise:*
            <nothing>
        """
        if request.get_header('Content-Type') == 'application/json':
            return self.mission.dumps_dict()
        else:
            return self.json_abort(400, "400: Bad ContentType")

    def get_status(self):
        """returns the actual status of the mission

        returns a json object with
        the current status of the Mission object.

        ex:

        .. code-block:: json

            { 'status': 'Calculated and Up to date' }

        *Keyword Arguments:*
            <none>

        *Returns:*
            resp -- response object with the status

        *Raise:*
            <nothing>
        """
        if request.get_header('Content-Type') == 'application/json':
            return { 'status': self.mission.status }
        else:
            return self.json_abort(400, "400: Bad ContentType")

    def post(self):
        """POST method for the Mission object Api

        create a new mission
        an new mission may only be created if the existing mission is
        empty (api user MUST call DELETE before calling POST)

        if a json structure is POSTed with the request, dipplanner will
        try to load this stucture inside the mission object.
        A full structure may be given.

        *Keyword Arguments:*
            <nothing>

        *Returns:*
            resp -- response object with the json dump of the newly
                    created object

        *Raise:*
            <nothing>
        """
        if request.get_header('Content-Type') == 'application/json':
            if self.mission is None or len(self.mission) == 0:
                self.mission = Mission()

                self.mission.loads_json(request.json)
                response.status = 201
                return self.mission.dumps_dict()  #, 201)
            else:
                return self.json_abort(403, "403: Forbidden: you MUST "
                                            "delete the current mission "
                                            "before create a new one")
        else:
            return self.json_abort(400, "400: Bad ContentType")

    def calculate(self):
        """launch the calculation of the mission

        returns a json object with
        the current status of the Mission object (after calculation).

        ex:

        .. code-block:: json

            { 'status': 'Calculated and Up to date' }

        *Keyword Arguments:*
            <none>

        *Returns:*
            resp -- response object with the status

        *Raise:*
            <nothing>
        """
        if request.get_header('Content-Type') == 'application/json':
            self.mission.calculate()
            return { 'status': self.mission.status }
        else:
            return self.json_abort(400, "400: Bad ContentType")

    def delete(self, resource_id=None):
        """DELETE method for the Mission object Api

        *Keyword Arguments:*
            <none>

        *Returns:*
            resp -- response object (empty)

        *Raise:*
            <nothing>
        """
        if request.get_header('Content-Type') == 'application/json':
            if resource_id is None:
                self.mission.clean()
                return self.mission.dumps_dict()
            else:
                return self.json_abort(404, "404: Not found")
        else:
            return self.json_abort(400, "400: Bad ContentType")
