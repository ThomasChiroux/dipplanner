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
REST Api for Segment object
---------------------------

"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]

# dependencies imports
from bottle import request, response

# local import
from dipplanner.gui.rest_main_api import ApiBottle
from dipplanner.mission import Mission
from dipplanner.segment import SegmentDive

class InputSegmentApiBottle(ApiBottle):
    """api for dives inside the mission object
    """

    def __init__(self, mission=None):
        self.mission = mission

    def get(self, dive_id, segment_id=None):
        """GET method for the Segment object Api

        returns a json dumps of the segments in the current mission object.

        *Keyword Arguments:*
            :dive_id: (int) -- number of the dive, first dive is dive 1
            :segment_id: (int) -- segment number

        *Returns:*
            resp -- response object with the json dump of the dives

        *Raise:*
            <nothing>
        """
        if request.get_header('Content-Type') == 'application/json':
            if segment_id is None:
                try:
                    return {'input_segments':
                            [segment.dumps_dict() for segment in
                             self.mission.dives[int(dive_id)
                                                - 1].input_segments]}
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
                        segment = dive.input_segments[int(segment_id) - 1]
                    except ValueError:
                        # TODO: try to find a segment with his name
                        return self.json_abort(404, "404: segment ({0}) not "
                                                    "found".format(segment_id))
                    except (KeyError, IndexError):
                        return self.json_abort(404, "404: segment ({0}) not "
                                                    "found".format(segment_id))
                    else:
                        return segment.dumps_dict()
        else:
            return self.json_abort(400, "400: Bad ContentType")

    def post(self, dive_id):
        """POST method for the Segment object Api

        create a new segment for this dive

        if a json structure is POSTed with the request, dipplanner will
        try to load this structure while instanciating the new segment
        A full Segment structure may be given, but a partial structure will
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
                new_segment = SegmentDive()
                if request.json is not None:
                    try:
                        new_segment.loads_json(request.json)
                    except Exception as exc:  # generic unknown exception
                        return self.json_abort(500, "500: {0}".format(exc))
                dive.input_segments.append(new_segment)
                self.mission.change_status(Mission.STATUS_CHANGED)
                response.status = 201
                return new_segment.dumps_dict()
        else:
            return self.json_abort(400, "400: Bad ContentType")


    def patch(self, dive_id, segment_id=None):
        """PATCH method for the Segment object Api

        update the segment object

        if no segment_id is given, returns 404
        if segment_id is given, try to patch the resource and returns
        the entire patched Segment with code 200 OK

        *Keyword Arguments:*
            :dive_id: -- (str): number of the segment, starting by 1
            :segment_id: --str : number of the dive, starting by 1

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
                if segment_id is None:
                    return self.json_abort(404, "404: you must provide "
                                                "a segment ID")
                else:
                    try:
                        dive.input_segments[int(segment_id)
                                            - 1].loads_json(request.json)
                        self.mission.change_status(Mission.STATUS_CHANGED)
                    except ValueError:
                        # TODO: try to find a dive with his name
                        return self.json_abort(404, "404: segment_id ({0}) not "
                                                    "found".format(segment_id))
                    except (KeyError, IndexError):
                        return self.json_abort(404, "404: segment_id ({0}) not "
                                                    "found".format(segment_id))
                    except Exception as exc:  # generic unknown exception
                        return self.json_abort(500, "500: {0}".format(exc))
                    else:
                        return dive.input_segments[int(segment_id)
                                                   - 1].dumps_dict()
        else:
            return self.json_abort(400, "400: Bad ContentType")


    def delete(self, dive_id, segment_id=None):
        """DELETE method for the Segment object Api

        if no resource_id is given, all the segments will be deleted.
        If resource_id is given and exists, only one segment will be deleted

        *Keyword Arguments:*
            :segment_id: --str : number of the segment, starting by 1

        *Returns:*
            resp -- response object - HTTP 200 + the list of remaining segments
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
                if segment_id is None:
                    dive.input_segments = []
                    self.mission.change_status(Mission.STATUS_CHANGED)
                    return {'input_segments':
                            [segment.dumps_dict() for segment
                             in dive.input_segments]}
                else:
                    try:
                        dive.input_segments.pop(int(segment_id) - 1)
                        self.mission.change_status(Mission.STATUS_CHANGED)
                    except ValueError:
                        # TODO: try to find a segment with his name
                        return self.json_abort(404, "404: segment ({0}) not "
                                                    "found".format(segment_id))
                    except (KeyError, IndexError):
                        return self.json_abort(404, "404: segment ({0}) not "
                                                    "found".format(segment_id))
                    else:
                        return {'input_segments':
                                [segment.dumps_dict() for segment
                                 in dive.input_segments]}
        else:
            return self.json_abort(400, "400: Bad ContentType")