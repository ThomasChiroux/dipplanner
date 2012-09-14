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
"""module generating the GUI

It uses flask micro-framework to publish a full REST/json API over the
dipplanner objects and methods
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]

# imports
import json

# dependencies imports
from flask.views import MethodView
from flask import make_response
from flask import Blueprint
from flask import g as self

class BaseApi(MethodView):
    """Base Class for the REST api

    This class should not be used directly, but serves as base class for
    all api objects
    """
    def __init__(self, name, mission):
        """Constructor for BaseApi object

        *Keyword Arguments:*
            :name: (str) -- api name
            :mission: (Mission) -- mission object

        *Returns:*
            <nothing>

        *Raise:*
            <nothing>
        """
        print "instanciation of BaseAPI"
        self.name = name
        self.mission = mission
        bp = Blueprint(name, __name__)
        bp_endpoint = '{0}_api'.format(name)
        bp_url = '/{0}/'.format(name)
        bp_pk = 'resource_id'
        self.register_api(bp, bp_endpoint, bp_url, bp_pk)
        self._blueprint = bp

    def register_api(self, blueprint, endpoint, url, p_key, pk_type=None):
        """register a REST Api for a dipplanner object

        *Keyword Arguments:*
            :app: (Flask) -- Flask application object
            :view: (MethodView) -- MethodView herited object
            :endpoint: (str) -- name for the view
            :url: (str) -- base url for the api
            :p_key: (str) -- primary key name
            :pk_type: (str) -- type of primary key

        *Returns:*
            <nothing>

        *Raise:*
            <nothing>
        """
        view_func = self.as_view(endpoint, self.name, self.mission)
        blueprint.add_url_rule(url, defaults={p_key: None},
                               view_func=view_func, methods=['GET', ])
        blueprint.add_url_rule(url, view_func=view_func, methods=['POST',
                                                                  'DELETE'])
        if pk_type is None:
            blueprint.add_url_rule('%s<%s>' % (url, p_key),
                                   view_func=view_func,
                                   methods=['GET', 'PUT', 'PATCH', 'DELETE'])
        else:
            blueprint.add_url_rule('%s<%s:%s>' % (url, pk_type, p_key),
                                   view_func=view_func,
                                   methods=['GET', 'PUT', 'PATCH', 'DELETE'])

    def json_resp(self, message, code):
        """Return a pure json Flask response with
        application/json content type and message

        *Keyword Arguments:*
            :message: (str) -- json message

            .. note :: this method does not validate the correctness of the
                       json message : this must be done before

            :code: (int) -- http response code

        *Returns:*
            resp -- Flask response objec

        *Raise:*
            <nothing>
        """
        if type(message) == dict:
            message = json.dumps(message)
        resp = make_response(message, code)
        resp.headers['Content-Type'] = 'application/json'
        return resp

    def get(self, resource_id):
        """GET method for the BaseApi

        This method always return 405 Method not allowed
        and should be redefined for each sub api

        *Keyword Arguments:*
        :resource_id: (str) -- key provided

        *Returns:*
            resp -- Flask response object

        *Raise:*
            <nothing>
        """
        return self.json_resp('{ "message": "405: Method not allowed" }',
                              405)

    def post(self):
        """POST method for the BaseApi

        This method always return 405 Method not allowed
        and should be redefined for each sub api

        *Keyword Arguments:*
            <none>

        *Returns:*
            resp -- Flask response object

        *Raise:*
            <nothing>
        """
        return self.json_resp('{ "message": "405: Method not allowed" }',
                              405)

    def put(self, resource_id):
        """PUT method for the BaseApi

        This method always return 405 Method not allowed
        and should be redefined for each sub api

        *Keyword Arguments:*
        :resource_id: (str) -- key provided

        *Returns:*
            resp -- Flask response object

        *Raise:*
            <nothing>
        """
        return self.json_resp('{ "message": "405: Method not allowed" }',
                              405)

    def patch(self, resource_id):
        """PATCH method for the BaseApi

        This method always return 405 Method not allowed
        and should be redefined for each sub api

        *Keyword Arguments:*
        :resource_id: (str) -- key provided

        *Returns:*
            resp -- Flask response object

        *Raise:*
            <nothing>
        """
        return self.json_resp('{ "message": "405: Method not allowed" }',
                              405)

    def delete(self, resource_id=None):
        """DELETE method for the BaseApi

        This method always return 405 Method not allowed
        and should be redefined for each sub api

        *Keyword Arguments:*
        :resource_id: (str) -- key provided

        *Returns:*
            resp -- Flask response object

        *Raise:*
            <nothing>
        """
        return self.json_resp('{ "message": "405: Method not allowed" }',
                              405)

