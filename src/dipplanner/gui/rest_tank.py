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
REST Api for Tank object
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
from dipplanner.tank import Tank

class TankApiBottle(ApiBottle):
    """api for dives inside the mission object
    """

    def __init__(self, mission=None):
        self.mission = mission

    def get(self, dive_id, tank_id=None):
        """GET method for the Tank object Api

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
            if tank_id is None:
                try:
                    return {'tanks': [tank.dumps_dict() for tank in
                                      self.mission.dives[int(dive_id)
                                                         - 1].tanks]}
                except (ValueError, KeyError, IndexError):
                    return self.json_abort(404, "404: dive_id ({0}) not "
                                                "found".format(dive_id))
            else:
                try:
                    dive = self.mission.dives[int(dive_id) - 1]
                except ValueError:
                    # TODO: try to find a dive with his name
                    return self.json_abort(404, "404: dive_id ({0}) not "
                                                "found".format(dive_id))
                except (KeyError, IndexError):
                    return self.json_abort(404, "404: dive_id ({0}) not "
                                                "found".format(dive_id))
                else:
                    try:
                        tank = dive.tanks[int(tank_id) - 1]
                    except ValueError:
                        # TODO: try to find a tank with his name
                        return self.json_abort(404, "404: tank ({0}) not "
                                                    "found".format(tank_id))
                    except (KeyError, IndexError):
                        return self.json_abort(404, "404: tank ({0}) not "
                                                    "found".format(tank_id))
                    else:
                        return tank.dumps_dict()
        else:
            return self.json_abort(400, "400: Bad ContentType")

    def post(self, dive_id):
        """POST method for the Tank object Api

        create a new tank for this dive

        if a json structure is POSTed with the request, dipplanner will
        try to load this structure while instanciating the new tank
        A full Tank structure may be given, but a partial structure will
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
            try:
                dive = self.mission.dives[int(dive_id) - 1]
            except ValueError:
                # TODO: try to find a dive with his name
                return self.json_abort(404, "404: dive_id ({0}) not "
                                            "found".format(dive_id))
            except (KeyError, IndexError):
                return self.json_abort(404, "404: dive_id ({0}) not "
                                            "found".format(dive_id))
            except Exception as exc:  # generic unknown exception
                return self.json_abort(500, "500: {0}".format(exc))
            else:
                new_tank = Tank()
                if request.json is not None:
                    try:
                        new_tank.loads_json(request.json)
                    except Exception as exc:  # generic unknown exception
                        return self.json_abort(500, "500: {0}".format(exc))
                dive.tanks.append(new_tank)
                self.mission.change_status(Mission.STATUS_CHANGED)
                response.status = 201
                return new_tank.dumps_dict()
        else:
            return self.json_abort(400, "400: Bad ContentType")


    def patch(self, dive_id, tank_id=None):
        """PATCH method for the Tank object Api

        update the tank object

        if no tank_id is given, returns 404
        if tank_id is given, try to patch the resource and returns
        the entive patched Dive with code 200 OK
        TODO: checker if it's 200 OK or SOMETHING UPDATED

        *Keyword Arguments:*
            :dive_id: -- (str): number of the tank, starting by 1
            :tank_id: --str : number of the dive, starting by 1

        *Returns:*
            resp -- response object - HTTP 200 + the list of remaining dives
                after the deletion

        *Raise:*
            <nothing>

        """
        if request.get_header('Content-Type') == 'application/json':
            try:
                dive = self.mission.dives[int(dive_id) - 1]
            except (ValueError, KeyError, IndexError):
                return self.json_abort(404, "404: dive_id ({0}) not "
                                            "found".format(dive_id))
            else:
                if tank_id is None:
                    return self.json_abort(404, "404: you must provide "
                                                "a tank ID")
                else:
                    try:
                        dive.tanks[int(tank_id) - 1].loads_json(request.json)
                        self.mission.change_status(Mission.STATUS_CHANGED)
                    except ValueError:
                        # TODO: try to find a dive with his name
                        return self.json_abort(404, "404: tank_id ({0}) not "
                                                    "found".format(tank_id))
                    except (KeyError, IndexError):
                        return self.json_abort(404, "404: tank_id ({0}) not "
                                                    "found".format(tank_id))
                    except Exception as exc:  # generic unknown exception
                        return self.json_abort(500, "500: {0}".format(exc))
                    else:
                        return dive.tanks[int(tank_id) - 1].dumps_dict()
        else:
            return self.json_abort(400, "400: Bad ContentType")


    def delete(self, dive_id, tank_id=None):
        """DELETE method for the Tank object Api

        if no resource_id is given, all the tanks will be deleted.
        If resource_id is given and exists, only one tank will be deleted

        *Keyword Arguments:*
            :tank_id: --str : number of the tank, starting by 1

        *Returns:*
            resp -- response object - HTTP 200 + the list of remaining tanks
                after the deletion

        *Raise:*
            <nothing>
        """
        if request.get_header('Content-Type') == 'application/json':
            try:
                dive = self.mission.dives[int(dive_id) - 1]
            except (ValueError, KeyError, IndexError):
                return self.json_abort(404, "404: dive_id ({0}) not "
                                            "found".format(dive_id))
            else:
                if tank_id is None:
                    dive.tanks = []
                    self.mission.change_status(Mission.STATUS_CHANGED)
                    return { 'tanks': [tank.dumps_dict() for tank in
                                       dive.tanks]}
                else:
                    try:
                        dive.tanks.pop(int(tank_id) - 1)
                        self.mission.change_status(Mission.STATUS_CHANGED)
                    except ValueError:
                        # TODO: try to find a tank with his name
                        return self.json_abort(404, "404: tank ({0}) not "
                                                    "found".format(tank_id))
                    except (KeyError, IndexError):
                        return self.json_abort(404, "404: tank ({0}) not "
                                                    "found".format(tank_id))
                    else:
                        return { 'tanks': [tank.dumps_dict() for tank in
                                           dive.tanks]}
        else:
            return self.json_abort(400, "400: Bad ContentType")