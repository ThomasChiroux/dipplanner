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

class OutputSegmentApiBottle(ApiBottle):
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
                    return {'output_segments':
                            [segment.dumps_dict() for segment in
                             self.mission.dives[int(dive_id)
                                                - 1].output_segments]}
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
                        segment = dive.output_segments[int(segment_id) - 1]
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
