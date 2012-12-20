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
REST Api for Dive object
------------------------

"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]

# dependencies imports
from bottle import request, response

# local import
from dipplanner.gui.rest_main_api import ApiBottle
from dipplanner.mission import Mission
from dipplanner.dive import Dive


class DiveApiBottle(ApiBottle):
    """api for dives inside the mission object
    """

    def __init__(self, mission=None):
        self.mission = mission

    def get(self, resource_id=None):
        """GET method for the Dive object Api

        returns a json dumps of the dives in the current mission object.

        *Keyword Arguments:*
            :resource_id: (int) -- number of the dive,
                first dive is dive 1

        *Returns:*
            resp -- response object with the json dump of the dives

        *Raise:*
            <nothing>
        """
        if request.get_header('Content-Type') == 'application/json':
            if resource_id is None:
                return {'dives': [dive.dumps_dict() for dive in
                                  self.mission.dives]}
            else:
                try:
                    return self.mission.dives[int(resource_id)
                                              - 1].dumps_dict()
                except ValueError:
                    # TODO: try to find a dive with his name
                    return self.json_abort(404, "404: dive_id ({0}) not "
                                                "found".format(resource_id))
                except (KeyError, IndexError):
                    return self.json_abort(404, "404: dive_id ({0}) not "
                                                "found".format(resource_id))
        else:
            return self.json_abort(400, "400: Bad ContentType")

    def post(self):
        """POST method for the Dive object Api

        create a new dive for this mission

        if a json structure is POSTed with the request, dipplanner will
        try to load this structure while instanciating the new dive
        A full dive structure may be given, but a partial structure will
        also be allowed. (all non given parameters will use the default values)

        *Keyword Arguments:*
            <nothing>

        *Returns:*
            resp -- response object with the json dump of the newly
                    created object

        *Raise:*
            <nothing>
        """
        if request.get_header('Content-Type') == 'application/json':
            new_dive = Dive()
            if request.json is not None:
                new_dive.loads_json(request.json)
            self.mission.dives.append(new_dive)
            self.mission.change_status(Mission.STATUS_CHANGED)
            response.status = 201
            return new_dive.dumps_dict()
        else:
            return self.json_abort(400, "400: Bad ContentType")

    def patch(self, resource_id=None):
        """PATCH method for the Dive object Api

        update the dive object

        if no resource_id is given, returns 404
        if resource_id is given, try to patch the resource and returns
        the entive patched Dive with code 200 OK

        *Keyword Arguments:*
            :resource_id: --str : number of the dive, starting by 1

        *Returns:*
            resp -- response object - HTTP 200 + the list of remaining dives
                after the deletion

        *Raise:*
            <nothing>

        """
        if request.get_header('Content-Type') == 'application/json':
            if resource_id is None:
                return self.json_abort(404, "404: you must provide a dive ID")
            else:
                try:
                    self.mission.dives[int(resource_id)
                                       - 1].loads_json(request.json)
                    self.mission.change_status(Mission.STATUS_CHANGED)
                except ValueError:
                    # TODO: try to find a dive with his name
                    return self.json_abort(404, "404: dive_id ({0}) not "
                                                "found".format(resource_id))
                except (KeyError, IndexError):
                    return self.json_abort(404, "404: dive_id ({0}) not "
                                                "found".format(resource_id))
                else:
                    return self.mission.dives[int(resource_id) - 1].dumps_dict()  # TODO: Correct this using dive dict not list
        else:
            return self.json_abort(400, "400: Bad ContentType")

    def delete(self, resource_id=None):
        """DELETE method for the Dive object Api

        if no resource_id is given, all the dives will be deleted.
        If resource_id is given and exists, only one dive will be deleted

        *Keyword Arguments:*
            :resource_id: --str : number of the dive, starting by 1

        *Returns:*
            resp -- response object - HTTP 200 + the list of remaining dives
                after the deletion

        *Raise:*
            <nothing>
        """
        if request.get_header('Content-Type') == 'application/json':
            if resource_id is None:
                self.mission.clean('dives')
                self.mission.change_status(Mission.STATUS_CHANGED)
                return {'dives': [dive.dumps_dict() for dive in
                                  self.mission.dives]}
            else:
                try:
                    self.mission.dives.pop(int(resource_id) - 1)
                    self.mission.change_status(Mission.STATUS_CHANGED)
                except ValueError:
                    # TODO: try to find a dive with his name
                    return self.json_abort(404, "404: dive_id ({0}) not "
                                                "found".format(resource_id))
                except (KeyError, IndexError):
                    return self.json_abort(404, "404: dive_id ({0}) not "
                                                "found".format(resource_id))
                else:
                    return {'dives': [dive.dumps_dict() for dive in
                                      self.mission.dives]}
        else:
            return self.json_abort(400, "400: Bad ContentType")
