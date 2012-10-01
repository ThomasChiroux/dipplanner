.. _dipplanner_rest_api:

REST Api
========

.. PUT si chaque field est une ressource, PATCH sinon

Dipplanner REST API is a json API.
All request and response MUST have a Content-Type: application/json


/api/v1/mission/
----------------

method: GET
^^^^^^^^^^^

returns a json object with all the content of the mission

ex:

.. code-block:: bash

    $ curl -v -X GET -H "Content-type: application/json" http://127.0.0.1:8080/api/v1/mission/
      * About to connect() to 127.0.0.1 port 8080 (#0)
      *   Trying 127.0.0.1...
      * connected
      * Connected to 127.0.0.1 (127.0.0.1) port 8080 (#0)
      > GET /api/v1/mission/ HTTP/1.1
      > User-Agent: curl/7.27.0
      > Host: 127.0.0.1:8080
      > Accept: */*
      > Content-type: application/json
      >
      * HTTP 1.0, assume close after body
      < HTTP/1.0 200 OK
      < Date: Mon, 01 Oct 2012 05:27:31 GMT
      < Server: WSGIServer/0.1 Python/2.7.3
      < Content-Length: 8389
      < Content-Type: application/json
      <

and the result contains (for example)

.. code-block:: javascript

   {"dives": [{"current_depth": 0, "pp_o2": 0.0, "current_tank": {"tank_rule": "50b", "max_ppo2": 1.6, "in_use": true, "f_n2": 0.79, "tank_vol": 15.0, "f_o2": 0.21, "mod": 66, "tank_pressure": 230.0, "name": "Air", "f_he": 0.0, "used_gas": 1595.1755578500001, "total_gas": 3387.1673441655867, "given_name": "airtank", "min_gas": 767.5548028677879, "remaining_gas": 1791.9917863155865}, "output_segments": [{"tank": {"tank_rule": "50b", "max_ppo2": 1.6, "in_use": true, "f_n2": 0.79, "tank_vol": 15.0, "f_o2": 0.21, "mod": 66, "tank_pressure": 230.0, "name": "Air", "f_he": 0.0, "used_gas": 1595.1755578500001, "total_gas": 3387.1673441655867, "given_name": "airtank", "min_gas": 767.5548028677879, "remaining_gas": 1791.9917863155865}, "in_use": true, "setpoint": 0.0, "depth": 30.0, "run_time": 90.0, "time": 90.0, "type": "descent"}, {"tank": {"tank_rule": "50b", "max_ppo2": 1.6, "in_use": true, "f_n2": 0.79, "tank_vol": 15.0, "f_o2": 0.21, "mod": 66, "tank_pressure": 230.0, "name": "Air", "f_he": 0.0, "used_gas": 1595.1755578500001, "total_gas": 3387.1673441655867, "given_name": "airtank", "min_gas": 767.5548028677879, "remaining_gas": 1791.9917863155865}, "in_use": true, "setpoint": 0.0, "depth": 30.0, "run_time": 1200.0, "time": 1110.0, "type": "const"}, {"tank": {"tank_rule": "50b", "max_ppo2": 1.6, "in_use": true, "f_n2": 0.79, "tank_vol": 15.0, "f_o2": 0.21, "mod": 66, "tank_pressure": 230.0, "name": "Air", "f_he": 0.0, "used_gas": 1595.1755578500001, "total_gas": 3387.1673441655867, "given_name": "airtank", "min_gas": 767.5548028677879, "remaining_gas": 1791.9917863155865}, "in_use": true, "setpoint": 0.0, "depth": 12.0, "run_time": 1308.0, "time": 108.0, "type": "ascent"}, {"tank": {"tank_rule": "50b", "max_ppo2": 1.6, "in_use": true, "f_n2": 0.79, "tank_vol": 15.0, "f_o2": 0.21, "mod": 66, "tank_pressure": 230.0, "name": "Air", "f_he": 0.0, "used_gas": 1595.1755578500001, "total_gas": 3387.1673441655867, "given_name": "airtank", "min_gas": 767.5548028677879, "remaining_gas": 1791.9917863155865}, "in_use": true, "setpoint": 0.0, "depth": 12.0, "run_time": 1309.0, "time": 1.0, "type": "deco"}, {"tank": {"tank_rule": "50b", "max_ppo2": 1.6, "in_use": true, "f_n2": 0.79, "tank_vol": 15.0, "f_o2": 0.21, "mod": 66, "tank_pressure": 230.0, "name": "Air", "f_he": 0.0, "used_gas": 1595.1755578500001, "total_gas": 3387.1673441655867, "given_name": "airtank", "min_gas": 767.5548028677879, "remaining_gas": 1791.9917863155865}, "in_use": true, "setpoint": 0.0, "depth": 9.0, "run_time": 1339.0, "time": 30.0, "type": "deco"}, {"tank": {"tank_rule": "50b", "max_ppo2": 1.6, "in_use": true, "f_n2": 0.79, "tank_vol": 15.0, "f_o2": 0.21, "mod": 66, "tank_pressure": 230.0, "name": "Air", "f_he": 0.0, "used_gas": 1595.1755578500001, "total_gas": 3387.1673441655867, "given_name": "airtank", "min_gas": 767.5548028677879, "remaining_gas": 1791.9917863155865}, "in_use": true, "setpoint": 0.0, "depth": 6.0, "run_time": 1435.0, "time": 96.0, "type": "deco"}, {"tank": {"tank_rule": "50b", "max_ppo2": 1.6, "in_use": true, "f_n2": 0.79, "tank_vol": 15.0, "f_o2": 0.21, "mod": 66, "tank_pressure": 230.0, "name": "Air", "f_he": 0.0, "used_gas": 1595.1755578500001, "total_gas": 3387.1673441655867, "given_name": "airtank", "min_gas": 767.5548028677879, "remaining_gas": 1791.9917863155865}, "in_use": true, "setpoint": 0.0, "depth": 3.0, "run_time": 1634.0, "time": 199.0, "type": "deco"}], "run_time": 1634.0, "tanks": [{"tank_rule": "30b", "max_ppo2": 1.6, "in_use": true, "f_n2": 0.79, "tank_vol": 15.0, "f_o2": 0.21, "mod": 66, "tank_pressure": 230.0, "name": "Air", "f_he": 0.0, "used_gas": 1527.8977473000002, "total_gas": 3387.1673441655867, "given_name": "Air", "min_gas": 767.5548028677879, "remaining_gas": 1859.2695968655864}], "is_closed_circuit": false, "no_flight_time_value": null, "in_final_ascent": true, "input_segments": [{"tank": {"tank_rule": "50b", "max_ppo2": 1.6, "in_use": true, "f_n2": 0.79, "tank_vol": 15.0, "f_o2": 0.21, "mod": 66, "tank_pressure": 230.0, "name": "Air", "f_he": 0.0, "used_gas": 1595.1755578500001, "total_gas": 3387.1673441655867, "given_name": "airtank", "min_gas": 767.5548028677879, "remaining_gas": 1791.9917863155865}, "in_use": true, "setpoint": 0.0, "depth": 30.0, "run_time": 0.0, "time": 1200.0, "type": "const"}], "metadata": "Dive to 30.0 for 1110.0s\n", "model": "ZHL16c", "surface_interval": 0, "is_repetitive_dive": false}, {"current_depth": 0, "pp_o2": 0.0, "current_tank": {"tank_rule": "50b", "max_ppo2": 1.6, "in_use": true, "f_n2": 0.79, "tank_vol": 15.0, "f_o2": 0.21, "mod": 66, "tank_pressure": 230.0, "name": "Air", "f_he": 0.0, "used_gas": 1595.1755578500001, "total_gas": 3387.1673441655867, "given_name": "airtank", "min_gas": 767.5548028677879, "remaining_gas": 1791.9917863155865}, "output_segments": [{"tank": {"tank_rule": "50b", "max_ppo2": 1.6, "in_use": true, "f_n2": 0.79, "tank_vol": 15.0, "f_o2": 0.21, "mod": 66, "tank_pressure": 230.0, "name": "Air", "f_he": 0.0, "used_gas": 1595.1755578500001, "total_gas": 3387.1673441655867, "given_name": "airtank", "min_gas": 767.5548028677879, "remaining_gas": 1791.9917863155865}, "in_use": true, "setpoint": 0.0, "depth": 20.0, "run_time": 60.0, "time": 60.0, "type": "descent"}, {"tank": {"tank_rule": "50b", "max_ppo2": 1.6, "in_use": true, "f_n2": 0.79, "tank_vol": 15.0, "f_o2": 0.21, "mod": 66, "tank_pressure": 230.0, "name": "Air", "f_he": 0.0, "used_gas": 1595.1755578500001, "total_gas": 3387.1673441655867, "given_name": "airtank", "min_gas": 767.5548028677879, "remaining_gas": 1791.9917863155865}, "in_use": true, "setpoint": 0.0, "depth": 20.0, "run_time": 1800.0, "time": 1740.0, "type": "const"}, {"tank": {"tank_rule": "50b", "max_ppo2": 1.6, "in_use": true, "f_n2": 0.79, "tank_vol": 15.0, "f_o2": 0.21, "mod": 66, "tank_pressure": 230.0, "name": "Air", "f_he": 0.0, "used_gas": 1595.1755578500001, "total_gas": 3387.1673441655867, "given_name": "airtank", "min_gas": 767.5548028677879, "remaining_gas": 1791.9917863155865}, "in_use": true, "setpoint": 0.0, "depth": 9.0, "run_time": 1866.0, "time": 66.0, "type": "ascent"}, {"tank": {"tank_rule": "50b", "max_ppo2": 1.6, "in_use": true, "f_n2": 0.79, "tank_vol": 15.0, "f_o2": 0.21, "mod": 66, "tank_pressure": 230.0, "name": "Air", "f_he": 0.0, "used_gas": 1595.1755578500001, "total_gas": 3387.1673441655867, "given_name": "airtank", "min_gas": 767.5548028677879, "remaining_gas": 1791.9917863155865}, "in_use": true, "setpoint": 0.0, "depth": 9.0, "run_time": 1867.0, "time": 1.0, "type": "deco"}, {"tank": {"tank_rule": "50b", "max_ppo2": 1.6, "in_use": true, "f_n2": 0.79, "tank_vol": 15.0, "f_o2": 0.21, "mod": 66, "tank_pressure": 230.0, "name": "Air", "f_he": 0.0, "used_gas": 1595.1755578500001, "total_gas": 3387.1673441655867, "given_name": "airtank", "min_gas": 767.5548028677879, "remaining_gas": 1791.9917863155865}, "in_use": true, "setpoint": 0.0, "depth": 6.0, "run_time": 1868.0, "time": 1.0, "type": "deco"}, {"tank": {"tank_rule": "50b", "max_ppo2": 1.6, "in_use": true, "f_n2": 0.79, "tank_vol": 15.0, "f_o2": 0.21, "mod": 66, "tank_pressure": 230.0, "name": "Air", "f_he": 0.0, "used_gas": 1595.1755578500001, "total_gas": 3387.1673441655867, "given_name": "airtank", "min_gas": 767.5548028677879, "remaining_gas": 1791.9917863155865}, "in_use": true, "setpoint": 0.0, "depth": 3.0, "run_time": 1936.0, "time": 68.0, "type": "deco"}], "run_time": 1936.0, "tanks": [{"tank_rule": "30b", "max_ppo2": 1.6, "in_use": true, "f_n2": 0.79, "tank_vol": 15.0, "f_o2": 0.21, "mod": 66, "tank_pressure": 230.0, "name": "Air", "f_he": 0.0, "used_gas": 1595.1755578500001, "total_gas": 3387.1673441655867, "given_name": "Air", "min_gas": 767.5548028677879, "remaining_gas": 1791.9917863155865}], "is_closed_circuit": false, "no_flight_time_value": 1860, "in_final_ascent": true, "input_segments": [{"tank": {"tank_rule": "50b", "max_ppo2": 1.6, "in_use": true, "f_n2": 0.79, "tank_vol": 15.0, "f_o2": 0.21, "mod": 66, "tank_pressure": 230.0, "name": "Air", "f_he": 0.0, "used_gas": 1595.1755578500001, "total_gas": 3387.1673441655867, "given_name": "airtank", "min_gas": 767.5548028677879, "remaining_gas": 1791.9917863155865}, "in_use": true, "setpoint": 0.0, "depth"* Closing connection #0
   : 20.0, "run_time": 0.0, "time": 1800.0, "type": "const"}], "metadata": "Dive to 20.0 for 1740.0s\n", "model": "ZHL16c", "surface_interval": 3600, "is_repetitive_dive": true}], "description": null}


errors
******

Bad content type
""""""""""""""""

This error is returned when the request did not use the application/json
Content-Type.

ex:

.. code-block:: bash

    $ curl -v -X GET http://127.0.0.1:8080/api/v1/mission/
      * About to connect() to 127.0.0.1 port 8080 (#0)
      *   Trying 127.0.0.1...
      * connected
      * Connected to 127.0.0.1 (127.0.0.1) port 8080 (#0)
      > GET /api/v1/mission/ HTTP/1.1
      > User-Agent: curl/7.27.0
      > Host: 127.0.0.1:8080
      > Accept: */*
      >
      * HTTP 1.0, assume close after body
      < HTTP/1.0 400 Bad Request
      < Date: Mon, 01 Oct 2012 05:26:08 GMT
      < Server: WSGIServer/0.1 Python/2.7.3
      < Content-Length: 35
      < Content-Type: application/json
      <
      * Closing connection #0
      {"message": "400: Bad ContentType"}

method: POST
^^^^^^^^^^^^

creates a new mission object and loads the given mission details posted in
the request.

.. note:: to be able to POST a mission, the current mission MUST be empty.
   you'll probably need to call DELETE first.

if the request is accepted and correctly processed, the API will return
201 CREATED and the json dumps of the created mission

ex:

.. code-block:: bash

    $ curl -v -X POST -d @/tmp/mission.json -H "Content-type: application/json" http://127.0.0.1:8080/api/v1/mission/
      * About to connect() to 127.0.0.1 port 8080 (#0)
      *   Trying 127.0.0.1...
      * connected
      * Connected to 127.0.0.1 (127.0.0.1) port 8080 (#0)
      > POST /api/v1/mission/ HTTP/1.1
      > User-Agent: curl/7.27.0
      > Host: 127.0.0.1:8080
      > Accept: */*
      > Content-type: application/json
      > Content-Length: 8389
      > Expect: 100-continue
      >
      * Done waiting for 100-continue
      * HTTP 1.0, assume close after body
      < HTTP/1.0 201 Created
      < Date: Mon, 01 Oct 2012 05:46:46 GMT
      < Server: WSGIServer/0.1 Python/2.7.3
      < Content-Length: 2814
      < Content-Type: application/json
      <

and the result contains (for example):

.. code-block:: javascript

    {"dives": [{"current_depth": 0, "pp_o2": 0.0, "current_tank": {"tank_rule": "50b", "max_ppo2": 1.6, "in_use": true, "f_n2": 0.79, "tank_vol": 15.0, "f_o2": 0.21, "mod": 66, "tank_pressure": 230.0, "name": "Air", "f_he": 0.0, "used_gas": 1595.1755578500001, "total_gas": 3387.1673441655867, "given_name": "airtank", "min_gas": 767.5548028677879, "remaining_gas": 1791.9917863155865}, "output_segments": [], "run_time": 1634.0, "tanks": [{"tank_rule": "30b", "max_ppo2": 1.6, "in_use": true, "f_n2": 0.79, "tank_vol": 15.0, "f_o2": 0.21, "mod": 66, "tank_pressure": 230.0, "name": "Air", "f_he": 0.0, "used_gas": 1527.8977473000002, "total_gas": 3387.1673441655867, "given_name": "Air", "min_gas": 454.3577760377562, "remaining_gas": 1859.2695968655864}], "is_closed_circuit": false, "no_flight_time_value": null, "in_final_ascent": false, "input_segments": [{"tank": {"tank_rule": "50b", "max_ppo2": 1.6, "in_use": true, "f_n2": 0.79, "tank_vol": 15.0, "f_o2": 0.21, "mod": 66, "tank_pressure": 230.0, "name": "Air", "f_he": 0.0, "used_gas": 1595.1755578500001, "total_gas": 3387.1673441655867, "given_name": "airtank", "min_gas": 767.5548028677879, "remaining_gas": 1791.9917863155865}, "in_use": true, "setpoint": 0.0, "depth": 30.0, "run_time": 0.0, "time": 1200.0, "type": "const"}], "metadata": "Dive to 30.0 for 1110.0s\n", "model": "ZHL16c", "surface_interval": 0, "is_repetitive_dive": false}, {"current_depth": 0, "pp_o2": 0.0, "current_tank": {"tank_rule": "50b", "max_ppo2": 1.6, "in_use": true, "f_n2": 0.79, "tank_vol": 15.0, "f_o2": 0.21, "mod": 66, "tank_pressure": 230.0, "name": "Air", "f_he": 0.0, "used_gas": 1595.1755578500001, "total_gas": 3387.1673441655867, "given_name": "airtank", "min_gas": 767.5548028677879, "remaining_gas": 1791.9917863155865}, "output_segments": [], "run_time": 1936.0, "tanks": [{"tank_rule": "30b", "max_ppo2": 1.6, "in_use": true, "f_n2": 0.79, "tank_vol": 15.0, "f_o2": 0.21, "mod": 66, "tank_pressure": 230.0, "name": "Air", "f_he": 0.0, "used_gas": 1595.1755578500001, "total_gas": 3387.167344165* Closing connection #0
    5867, "given_name": "Air", "min_gas": 454.3577760377562, "remaining_gas": 1791.9917863155865}], "is_closed_circuit": false, "no_flight_time_value": null, "in_final_ascent": false, "input_segments": [{"tank": {"tank_rule": "50b", "max_ppo2": 1.6, "in_use": true, "f_n2": 0.79, "tank_vol": 15.0, "f_o2": 0.21, "mod": 66, "tank_pressure": 230.0, "name": "Air", "f_he": 0.0, "used_gas": 1595.1755578500001, "total_gas": 3387.1673441655867, "given_name": "airtank", "min_gas": 767.5548028677879, "remaining_gas": 1791.9917863155865}, "in_use": true, "setpoint": 0.0, "depth": 20.0, "run_time": 0.0, "time": 1800.0, "type": "const"}], "metadata": "Dive to 20.0 for 1740.0s\n", "model": "ZHL16c", "surface_interval": 3600, "is_repetitive_dive": true}], "description": null}


errors
******

forbidden
"""""""""

this error is raised when you try to POST a new mission when the current
mission is not empty : before posting a new mission structure, you MUST
before call DELETE

ex:

.. code-block:: bash

    $ curl -v -X POST -d @/tmp/mission.json -H "Content-type: application/json" http://127.0.0.1:8080/api/v1/mission/
      * Could not resolve host: ; Erreur inconnue
      * Closing connection #0
      curl: (6) Could not resolve host: ; Erreur inconnue
      * About to connect() to 127.0.0.1 port 8080 (#0)
      *   Trying 127.0.0.1...
      * connected
      * Connected to 127.0.0.1 (127.0.0.1) port 8080 (#0)
      > POST /api/v1/mission/ HTTP/1.1
      > User-Agent: curl/7.27.0
      > Host: 127.0.0.1:8080
      > Accept: */*
      > Content-type: application/json
      >
      * HTTP 1.0, assume close after body
      < HTTP/1.0 403 Forbidden
      < Date: Mon, 01 Oct 2012 05:33:05 GMT
      < Server: WSGIServer/0.1 Python/2.7.3
      < Content-Length: 90
      < Content-Type: application/json
      <
      * Closing connection #0
      {"message": "403: Forbidden: you MUST delete the current mission before create a new one"}

Bad content type
""""""""""""""""

This error is returned when the request did not use the application/json
Content-Type.

ex:


.. code-block:: bash

    $ curl -v -X POST -d @/tmp/mission.json http://127.0.0.1:8080/api/v1/mission/* Could not resolve host: ; Erreur inconnue
      * Closing connection #0
      curl: (6) Could not resolve host: ; Erreur inconnue
      * About to connect() to 127.0.0.1 port 8080 (#0)
      *   Trying 127.0.0.1...
      * connected
      * Connected to 127.0.0.1 (127.0.0.1) port 8080 (#0)
      > POST /api/v1/mission/ HTTP/1.1
      > User-Agent: curl/7.27.0
      > Host: 127.0.0.1:8080
      > Accept: */*
      >
      * HTTP 1.0, assume close after body
      < HTTP/1.0 400 Bad Request
      < Date: Mon, 01 Oct 2012 05:35:07 GMT
      < Server: WSGIServer/0.1 Python/2.7.3
      < Content-Length: 35
      < Content-Type: application/json
      <
      * Closing connection #0
      {"message": "400: Bad ContentType"}

method: DELETE
^^^^^^^^^^^^^^

erase the current Mission
if the delete operation succeed, the api returns 200 OK with an empty mission
structure

ex:

.. code-block:: bash

    $ curl -v -X DELETE -H "Content-type: application/json" http://127.0.0.1:8080/api/v1/mission/* About to connect() to 127.0.0.1 port 8080 (#0)
      *   Trying 127.0.0.1...
      * connected
      * Connected to 127.0.0.1 (127.0.0.1) port 8080 (#0)
      > DELETE /api/v1/mission/ HTTP/1.1
      > User-Agent: curl/7.27.0
      > Host: 127.0.0.1:8080
      > Accept: */*
      > Content-type: application/json
      >
      * HTTP 1.0, assume close after body
      < HTTP/1.0 200 OK
      < Date: Mon, 01 Oct 2012 05:39:01 GMT
      < Server: WSGIServer/0.1 Python/2.7.3
      < Content-Length: 32
      < Content-Type: application/json
      <
      * Closing connection #0
      {"dives": [], "description": ""}


errors
******

Bad content type
""""""""""""""""

This error is returned when the request did not use the application/json
Content-Type.

ex:


.. code-block:: bash

    $ curl -v -X DELETE http://127.0.0.1:8080/api/v1/mission/
      * About to connect() to 127.0.0.1 port 8080 (#0)
      *   Trying 127.0.0.1...
      * connected
      * Connected to 127.0.0.1 (127.0.0.1) port 8080 (#0)
      > DELETE /api/v1/mission/ HTTP/1.1
      > User-Agent: curl/7.27.0
      > Host: 127.0.0.1:8080
      > Accept: */*
      >
      * HTTP 1.0, assume close after body
      < HTTP/1.0 400 Bad Request
      < Date: Mon, 01 Oct 2012 05:36:30 GMT
      < Server: WSGIServer/0.1 Python/2.7.3
      < Content-Length: 35
      < Content-Type: application/json
      <
      * Closing connection #0
      {"message": "400: Bad ContentType"}

/api/v1/mission/status
----------------------

method: GET
^^^^^^^^^^^

returns the current status of the mission

ex:

.. code-block:: bash

    $ curl -v -X GET -H "Content-type: application/json" http://127.0.0.1:8080/api/v1/mission/status
      * About to connect() to 127.0.0.1 port 8080 (#0)
      *   Trying 127.0.0.1...
      * connected
      * Connected to 127.0.0.1 (127.0.0.1) port 8080 (#0)
      > GET /api/v1/mission/status HTTP/1.1
      > User-Agent: curl/7.27.0
      > Host: 127.0.0.1:8080
      > Accept: */*
      > Content-type: application/json
      >
      * HTTP 1.0, assume close after body
      < HTTP/1.0 200 OK
      < Date: Mon, 01 Oct 2012 05:54:48 GMT
      < Server: WSGIServer/0.1 Python/2.7.3
      < Content-Length: 28
      < Content-Type: application/json
      <
      * Closing connection #0
      {"status": "Not Calculated"}


return may be one of the following results :

.. code-block:: json

   { 'status': 'Not Calculated' }

or:

.. code-block:: json

   { 'status': 'Calculated but Changed' }

or:

.. code-block:: json

   { 'status': 'Calculated and Up to date' }

/api/v1/mission/calculate
-------------------------

method: POST
^^^^^^^^^^^^

Calculate all the dives of the mission

ex:

.. code-block:: bash

    $ curl -v -X POST -H "Content-type: application/json" http://127.0.0.1:8080/api/v1/mission/calculate
      * About to connect() to 127.0.0.1 port 8080 (#0)
      *   Trying 127.0.0.1...
      * connected
      * Connected to 127.0.0.1 (127.0.0.1) port 8080 (#0)
      > POST /api/v1/mission/calculate HTTP/1.1
      > User-Agent: curl/7.27.0
      > Host: 127.0.0.1:8080
      > Accept: */*
      > Content-type: application/json
      >
      * HTTP 1.0, assume close after body
      < HTTP/1.0 200 OK
      < Date: Mon, 01 Oct 2012 06:11:50 GMT
      < Server: WSGIServer/0.1 Python/2.7.3
      < Content-Length: 39
      < Content-Type: application/json
      <
      * Closing connection #0
      {"status": "Calculated and Up to date"}


/api/v1/mission/dives/
----------------------

method: GET
^^^^^^^^^^^

method: POST
^^^^^^^^^^^^

method: DELETE
^^^^^^^^^^^^^^

/api/v1/mission/dives/<dive_id>/
--------------------------------

method: GET
^^^^^^^^^^^

method: POST
^^^^^^^^^^^^

method: PATCH
^^^^^^^^^^^^^

method: DELETE
^^^^^^^^^^^^^^

/api/v1/mission/dives/<dive_id>/tanks/
--------------------------------------

method: GET
^^^^^^^^^^^

method: POST
^^^^^^^^^^^^

method: DELETE
^^^^^^^^^^^^^^

/api/v1/mission/dives/<dive_id>/tanks/<tank_id>/
------------------------------------------------

method: GET
^^^^^^^^^^^

method: POST
^^^^^^^^^^^^

method: PATCH
^^^^^^^^^^^^^

method: DELETE
^^^^^^^^^^^^^^

/api/v1/mission/dives/<dive_id>/input_segments/
-----------------------------------------------

method: GET
^^^^^^^^^^^

method: POST
^^^^^^^^^^^^

method: DELETE
^^^^^^^^^^^^^^

/api/v1/mission/dives/<dive_id>/input_segments/<segment_id>/
------------------------------------------------------------

method: GET
^^^^^^^^^^^

method: POST
^^^^^^^^^^^^

method: PATCH
^^^^^^^^^^^^^

method: DELETE
^^^^^^^^^^^^^^

/api/v1/mission/dives/<dive_id>/output_segments/
------------------------------------------------

method: GET
^^^^^^^^^^^

/api/v1/mission/dives/<dive_id>/output_segments/<segment_id>/
-------------------------------------------------------------

method: GET
^^^^^^^^^^^

/api/v1/mission/dives/<dive_id>/OTHER DIVE ATTRIBUTES/
------------------------------------------------------

TBD

/api/v1/settings/
-----------------

method: GET
^^^^^^^^^^^

/api/v1/settings/EACHSETTINGSATTRIBUTE/
---------------------------------------

method: GET
^^^^^^^^^^^

method: PATCH
^^^^^^^^^^^^^
