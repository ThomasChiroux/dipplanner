.. _dipplanner_configfile:

dipplanner config file documentation
====================================

In config files, you can

* change all the dipplanner parameters (a little bit more than in command line)
* specify repetitive dives (in command-line, only one dive can be specified)

You may provide more than one config file in dipplanner command-line: it's up
to you to organise the config like as you wish.

For example, you MAY create one config file for your dive parameters
and another config file for your set of repetitive dives.

tanks
-----

At first you'll need to specify all the tanks you're planning to use in the
entire mission.

Later, for each dive, you'll only select one or several tanks previously defined

Tanks definitions are specific sections in the config file, in the form:

::

    [tank:NAME]

where NAME represent the name you've choosen for the tank.

.. warning:: NAME of tanks MUST be unique in the entire mission.

.. hint:: you can provide in the config file as many **[tank:NAME]** sections as you want.

to define each tank, you can provide one of the following options:

.. cmdoption:: f_o2 = <VALUE>

   (float) fraction of oxygen in the tank. Between 0.0 and 1.0

.. cmdoption:: f_he = <VALUE>

   (float) fraction of helium in the tank. Between 0.0 and 1.0

.. cmdoption:: f_n2 = <VALUE>

   (float) fraction of nitrogen in the tank. Between 0.0 and 1.0

.. note:: you're only needed to specify two of the 3 gases to define the tank

          dipplanner will automatically complete the fraction of the third gas.

.. note:: None of the previous fraction of gas is mandatory.

          By default, dipplanner will create an Air Tank
          (f_o2=0.21, f_he=0.0, f_n2=0.79)

.. cmdoption:: volume = <VALUE>

   (float) Volume of the tank in liter

.. cmdoption:: pressure = <VALUE>

   (float) Pressure of the tank in bar

.. cmdoption:: rule = <VALUE>

   Minimum gas rule (str) quantity of gas that should remain in the
   tank after the dive

   There two format for minimum gas rule:

   * quantity of bar that should remain in the tank:

        format: "[0-9]+b"

        ex: "50b": it should remain 50 bar in the tank at the end of the dive

   * "fraction rule" (like `the rule of third in cave diving <http://en.wikipedia.org/wiki/Rule_of_thirds_%28diving%29>`_)

        format: "1/[0-9]"

        ex1: "1/3" : 1/3 of the tank to go in, 1/3 of the tank to go back and it should remain 1/3 of the tank at the end of the dive

        ex2: "1/6" : 1/6 of the tank to go in, 1/6 of the tank to go back and it should remain 2/3 of the tank at the end of the dive

.. cmdoption:: max_ppo2 = <VALUE>

   (float) max_ppo2 allowed for this tank use.

   .. note:: if not provided, dipplanner will calculte the value automatically

.. cmdoption:: mod = <VALUE>

    (float) maximum operating depth allowed for this tank use.

   .. note:: if not provided, dipplanner will calculte the value automatically

Example:

    Mission with two tanks:

    12l tank filled with 200b or air. It should remain 50b at the end of the dive.

    and

    12l tank filled with Nitrox80. It should remain 30b at the end of the dive.

    .. code-block:: ini

        [tank:airtank]
        f_o2=0.21
        f_he=0
        volume=12
        pressure=230
        rule=50b

        [tank:decotank]
        f_o2=0.80
        f_he=0
        volume=12
        pressure=200
        rule=30b

dive profiles
-------------

Dive profiles are specific sections in the config file, in the form:

::

    [dive:NAME]

where NAME represent a name for the dive (it can be a number if you want).
The dives whill be processed in croissant order

To define a dive, you MUST specify which tank(s) this specific dive will use.
The Tank(s) must be defined before in the [tank:XXX] sections.

.. hint:: you can provide in the config file as many **[dive:NAME]** sections as you want.

the [dive:XXXX] sections use the following options:

.. cmdoption:: tanks = <VALUE>

   list of the tank name you'll be using during this dive.

   The names MUST match the name provided in the [tank:NAME] sections.

   ex: ::

        tanks = airtank, decotank

   in this example, the dive will use both airtank and decotank

.. cmdoption:: surface_interval  = <VALUE>

   surface interval (in seconds)

   for repetitive dives, you can specify the surface time between the previous
   dive and this dive

.. cmdoption:: automatic_tank_refill = <true|false>

    If 'automatic_tank_refill' is set to True, the tank will be full before the dive.
    If set to False, it'll use the remaining gas from last dive

    Default: true

    .. note:: if you use this parameter inside a [dive:NAME] section, it will
              override the global paramater for this specific Dive.

    Example:

    do not refill tank before this dive

    ::

        automatic_tank_refill = false

segments
--------

A segment belongs to a dive, so each segment section MUST refer to a dive.

The section structure must respect the following pattern:

::

    [dive:DIVENAME:segment:SEGNAME]

dive:DIVENAME refers to the previously defined [dive:NAME] section

.. hint:: you can provide in the config file as many
          **[dive:NAME:segment:SEGNAME]** sections as you want.

SEGNAME is a name you choose for a segment, it can also be numbers

segment sections uses the following options:

.. cmdoption:: depth = <VALUE>

   (float) in meter

.. cmdoption:: time = <VALUE>

   (float) in seconds (operators are allowed like: '30 * 60')

   duration of the segment (in seconds)

.. cmdoption:: tank = <VALUE>

   (str)

   name of the tank (the 'tank_name' specified in -t option or in config files)

.. cmdoption:: set_point = <VALUE>

   (float) 0.0 if OC, setpoint if CCR

   .. note::

       If you specify a setpoint > 0.0, the dive will automatically switch
       in CCR mode.

Example:

    20 min at 30 meter using tank: airtank in OC mode

    .. code-block:: ini

        [dive:1:segment:bottom]
        depth = 30
        time = 20*60
        tank = airtank
        set_point = 0.0

    20 min at 30 meter using tank: airtank in OC mode

    and then

    25 min at 20 meter using tank: airtank in OC mode

    .. code-block:: ini

        [dive:1:segment:1]
        depth = 30
        time = 20*60
        tank = airtank
        set_point = 0.0

        [dive:1:segment:2]
        depth = 20
        time = 25*60
        tank = airtank
        set_point = 0.0

Examples
^^^^^^^^

Full example with two subsequent dives, with a surface interval of 1h30 between the two

.. code-block:: ini

        [tank:airtank]
        f_o2=0.21
        f_he=0
        volume=15
        pressure=230
        rule=50b

        [tank:decotank]
        f_o2=0.80
        f_he=0
        volume=12
        pressure=230
        rule=50b

        [dive:1]
        tanks = airtank, decotank

        [dive:1:segment:bottom]
        depth = 30
        time = 20*60
        tank = airtank
        set_point = 0.0

        [dive:2]
        surface_interval = 90*60
        automatic_tank_refill = true
        tanks = airtank

        [dive:2:segment:bottom]
        depth = 20
        time = 30*60
        tank = airtank
        set_point = 0.0

Controling the output
---------------------


It's done via the section:

::

    [output]


.. cmdoption:: template = <TEMPLATE>


    Name of the template to be used
    The template file should be present in templates directory

    see :ref:`dipplanner_templates` for more infos on templates

    Default: default-color.tpl

    Example:

        switch to html template

        .. code-block:: ini

            [output]

            template = default.html


general dive parameters
-----------------------

general dive parameters are in the section:

::

    [general]

.. cmdoption:: deco_model = <ZHL16b|ZHL16c>

    Set the decompression model used for the calculations:
    either buhlmann ZHL16b or buhlmann ZHL16c

    Default: ZHL16c

    Example:

    switch to ZHL16b deco model

    .. code-block:: ini

        [general]

        deco_model = ZHL16b

.. cmdoption:: max_ppo2 = <VALUE>

    max allowed ppo2 (float) for this dive.

    Default: 1.6

    Example:

    Set the max allowed ppo2 at 1.4

    .. code-block:: ini

        [general]

        max_ppo2 = 1.4


.. cmdoption:: min_ppo2 = <VALUE>

    minimum allowed ppo2 for this dive.

    Default: 0.21

    Example:

    Set the min allowed ppo2 at 0.19

    .. code-block:: ini

        [general]

        max_ppo2 = 1.4


.. cmdoption:: max_end = <VALUE>

    max END (Equivalent narcosis Depth) allowed for this dive, in meter

    Default: 30 m

    Example:

    Set the max END at 35m

    .. code-block:: ini

        [general]

        max_end = 35


    .. note::
        end calculation is based on narcotic index for all gases.

        By default, dipplanner considers that oxygen is narcotic
        (same narcotic index than nitrogen)

        All narcotic indexes can by changed in the config file,
        in the [advanced] section

.. cmdoption:: descent_rate = <VALUE>

    descent rate (float) (in m/minute).

    Default: 20 m/min

    Example:

    Plan a dive with 17 m/min descent rate

    .. code-block:: ini

        [general]

        descent_rate = 17

    .. note::

        Internally, the ascent and descent rates are in m/second, but for
        convenience, the argument in command line is provided in m/min.
        The conversion is done automatically

.. cmdoption:: ascent_rate = <VALUE>

    ascent rate (float) (in m/minute).

    Default: 10 m/min

    Example:

    Plan a dive with 9 m/min ascent rate

    .. code-block:: ini

        [general]

        ascent_rate = 9

    .. note::

        Internally, the ascent and descent rates are in m/second, but for
        convenience, the argument in command line is provided in m/min.
        The conversion is done automatically

.. cmdoption:: gf_low = <VALUE>

    GF low: (int) in %, between 0 and 100

    Default: 30%

    Example:

    GF low of 25%

    .. code-block:: ini

        [general]

        gf_low = 25

    .. note::

        Internally, GFlow is a float number between 0.0 and 1.0, but for
        convenience, the argument in command line is provided in % value,
        between 0 and 100. The conversion is done automatically.


.. cmdoption:: gf_high = <VALUE>

    GF high: (int) in %, between 0 and 100

    Default: 80%

    Example:

    GF high of 85%

    .. code-block:: ini

        [general]

        gf_low = 85

    .. note::

        Internally, GFhigh is a float number between 0.0 and 1.0, but for
        convenience, the argument in command line is provided in % value,
        between 0 and 100. The conversion is done automatically.


.. cmdoption:: water = <sea|fresh>

    specify in which type of water you will do the dive: sea or fresh

    Default: sea

    Example:

    Do a dive in a lake

    .. code-block:: ini

        [general]

        water = fresh

.. cmdoption:: altitude = <VALUE>

    altitude (int) of the dive in meter.

    .. warning::

        It's very important to specify this parameter if you do a dive in altitude

    Default: 0m (sea level)

    Example:

    Dive at 1400m

    .. code-block:: ini

        [general]

        altitude = 1400


.. cmdoption:: dive_consumption_rate = <VALUE>

    gas consumption rate (float) during dive (in l/minute).

    Is it used for tank monitoring and associated with tank size, pressure and
    tank rules, it will warn you if your plannified dive ends without enough gas.

    Default: 17 l/min

    Example:

    Plan a dive with 25 l/min dive consumption rate

    .. code-block:: ini

        [general]

        dive_consumption_rate = 25

    .. note::

        Internally, the consumption rates are in l/second, but for
        convenience, the argument in command line is provided in l/min.
        The conversion is done automatically

.. cmdoption:: deco_consumption_rate = <VALUE>

    gas consumption rate (float) during deco (in l/minute).

    Default: 12 l/min

    Example:

    Plan a dive with 20 l/min deco consumption rate

    .. code-block:: ini

        [general]

        dive_consumption_rate = 20

    .. note::

        Internally, the consumption rates are in l/second, but for
        convenience, the argument in command line is provided in l/min.
        The conversion is done automatically


.. cmdoption:: run_time = <true|false>

    if true: segments represents runtime,

    if false, segments represents segtime (in this case, the full time of
    the segment will be done and the descent and/or ascent time will be
    in addition.

    Default: true


    Example:

    force segment time

    .. code-block:: ini

        [general]

        run_time = false


.. cmdoption:: use_oc_deco = <true|false>

    if false, do not use deco tanks (or bailout) for decompressions

    Default: true

    By default, dipplanner will automatically switch to best mix for deco
    and if CCR, it will switch to deco bailout if it's best for decompression.

    If you set this option, dipplanner will keep the last bottom gas used in OC
    or will still use CCR setpoint of last segment for deco

    Example:

    force the use of same gas for deco

    .. code-block:: ini

        [general]

        use_oc_deco = false


.. cmdoption:: multilevel_mode = <true|false>

    .. todo:: check the usage of the multilevel_mode option in config-files

    .. warning:: do not use this option for the moment

    Default: false

    Example:

    set multilevel mode to true

    .. code-block:: ini

        [general]

        multilevel_mode = true

.. cmdoption:: automatic_tank_refill = <true|false>

    If 'automatic_tank_refill' is set to True, the tank will be full before the dive.
    If set to False, it'll use the remaining gas from last dive

    Default: true

    Example:

    do not refill tank between dives

    .. code-block:: ini

        [general]

        automatic_tank_refill = false

advanced dive parameters
------------------------

avanced dive parameters are in the section:

::

    [advanced]

.. warning::

    unless knowing what you're doing, this prefs should not be changed
    by the user


.. cmdoption:: fresh_water_density = <VALUE>

    Water density for fresh water (float)

    Default: 1.0

.. cmdoption:: sea_water_density = <VALUE>

    Water density for sea water (float)

    Default: 1.03

.. cmdoption:: absolute_max_ppo2 = <VALUE>

    In addition to max_ppo2, dipplanner uses and 'absolute_max_ppo2'
    which should never

    Default: 2.0

.. cmdoption:: absolute_min_ppo2 = <VALUE>

    In addition to max_ppo2, dipplanner uses and 'absolute_max_ppo2'
    which should never

    Default: 0.16


.. cmdoption:: absolute_max_tank_pressure = <VALUE>

    maximum pressure for a tank. (float) -- in bar
    It's impossible to create a tank with higher pressure than this value

    Default: 300b

.. cmdoption:: absolute_max_tank_size = <VALUE>

    maximum size for a tank (float) -- in liter (dm³)
    It's impossible to create a tank larger than this value

    Default: 40l

    .. note::

        to handle double (connected) tanks, dipplanner considers one
        big tank, that's why 40l is the limit : 2x20l

.. cmdoption:: surface_temp = <VALUE>

    Temperature at surface (float) in celcius

    Default: 20 °C

    Example:

    change surface temperature to 30 °C

    ::

        [advanced]

        surface_temp = 30

.. cmdoption:: he_narcotic_value = <VALUE>

    narcotic value for helium (float)

    Default: 0.23

.. cmdoption:: n2_narcotic_value = <VALUE>

    narcotic value for nitrogen (float)

    Default: 1.0

.. cmdoption:: o2_narcotic_value = <VALUE>

    narcotic value for oxygen (float)

    Default: 1.0

.. cmdoption:: ar_narcotic_value = <VALUE>

    narcotic value for argon (float)

    Default: 2.33

.. cmdoption:: stop_depth_increment = <VALUE>

    increment for each depth stop (int) in meter

    When in ascent phase, do the deco stop every 'stop_depth_increment'.

    By default, dipplanner do the deco stop every 3m

    Default: 3m

.. cmdoption:: last_stop_depth = <VALUE>

    in meter : last stop before surfacing

    Default: 3m


.. cmdoption:: stop_time_increment = <VALUE>

    Set the time increment used for the calculations of the dive model.

    Default: 1s

    Dipplanner use by default a time increment of 1s, which is more accurate
    than other dive plannification tools (which usually take 1 min).

    But it has a serious performance impact. If you encounter some performance
    problem with dipplanner and do not want so much precision, you can raise
    this value

.. cmdoption:: force_all_stops = <true|false>

    one deco stop begun, force to stop to each deco depth stop

    Default: true

.. cmdoption:: ambiant_pressure_sea_level = <VALUE>

    Change ambiant pressure at sea level (float) (in bar)

    Default: 1.01325 b

    Example:

    change ambiant pressure at sea level to 1 bar

    .. code-block:: ini

        [advanced]

        ambiant_pressure_sea_level = 1.0

.. cmdoption:: method_for_depth_calculation = <simple|complex>

    method used for pressure from depth calculation.

    * simple method uses only +10m = +1bar
    * complex methods uses real water density calculation

    Default: complex

    Example:

    switch depth calc method to simple

    .. code-block:: ini

        [advanced]

        method_for_depth_calculation = simple

.. cmdoption:: travel_switch = <late|early>

    Travel switch method (late or early).

    * if late, it will keep the travel as long as possible (until either MOD or max END)
    * if early, it will switch to bottom tank as soon as is it breathable

    Default: late

    Example:

    switch travel switch to early

    .. code-block:: ini

        [advanced]

        travel_switch = early


.. cmdoption:: flight_altitude = <VALUE>

    this parameter used in no flight time calculation : it's the parameter needed
    to calculate decompression until the altitude of the flight

    Default: 2450

    .. note::

        the default value represents the maximum 'altitude equivalent' tolerated
        in flight by international regulation
        (8000 feet = 2 438.4 meters rounded to 2450m)

Examples
--------

Small Example: only set dives
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: ini

    # dipplanner config file
    # this file is used by the command line tool and
    # override the defaults parameters or input some dive profiles
    # =============================== tank profiles ================================
    # tanks are givent using [tank:NAME] section, where NAME represent a name
    # for the tank.
    # Tank names must be unique within the same Mission
    # you can add as many tank sections as you want

    [tank:airtank]
    f_o2=0.21
    f_he=0
    volume=15
    pressure=230
    rule=50b

    [tank:decotank]
    f_o2=0.80
    f_he=0
    volume=12
    pressure=230
    rule=50b


    # =============================== dive profiles ================================
    # repetitive dives are given using [dive:NAME] section, where NAME represent a
    # name (or number if you want) of a dive.
    # the dives will be done in give, order.
    # Dive names must be unique within the same Mission
    # you can add as many dive sections as you want

    [dive:1]

    # define the tanks used in this dive: coma-separated tank names:
    tanks = airtank, decotank

    # ------------------------------- dive segment -------------------------------
    # multiples segment are given using: [dive:NAME:segment:SEGNAME], where
    # NAME represent the name (or number if you want) of the dive and
    # SEGNAME represent the name (or number if you prefer) of the segment
    # at least ONT segment (for a dive) is mandatory
    [dive:1:segment:bottom]
    depth = 30
    time = 20*60
    tank = airtank
    set_point = 0.0

    [dive:2]
    # surface_interval (in seconds)
    # for repetitive dives, you can specify the surface time between the previous
    # dive and this dive
    surface_interval = 60*60

    # automatic tank refill: if set to true, used tanks for this dive will be
    # refilled before the dive
    automatic_tank_refill = true


    tanks = airtank

    # segment list for this dive. At least ONE segment is mandatory

    [dive:2:segment:bottom]

    depth = 20
    time = 30*60
    tank = airtank
    set_point = 0.0


Full Example
^^^^^^^^^^^^

Config file with all the settings set below.

.. note:: the default_config.cfg in ./configs directory set all the parameters
    to their default values (wich is not the case in the following example)

.. code-block:: ini

    # dipplanner config file
    # this file is used by the command line tool and
    # override the defaults parameters or input some dive profiles

    # =============================== tank profiles ================================
    # tanks are givent using [tank:NAME] section, where NAME represent a name
    # for the tank.
    # Tank names must be unique within the same Mission
    # you can add as many tank sections as you want

    [tank:airtank]
    f_o2=0.21
    f_he=0
    volume=15
    pressure=230
    rule=50b

    [tank:decotank]
    f_o2=0.80
    f_he=0
    volume=12
    pressure=230
    rule=50b


    # =============================== dive profiles ================================
    # repetitive dives are given using [dive:NAME] section, where NAME represent a
    # name (or number if you want) of a dive.
    # the dives will be done in give, order.
    # Dive names must be unique within the same Mission
    # you can add as many dive sections as you want

    [dive:1]

    # define the tanks used in this dive: coma-separated tank names:
    tanks = airtank, decotank

    # ------------------------------- dive segment -------------------------------
    # multiples segment are given using: [dive:NAME:segment:SEGNAME], where
    # NAME represent the name (or number if you want) of the dive and
    # SEGNAME represent the name (or number if you prefer) of the segment
    # at least ONT segment (for a dive) is mandatory
    [dive:1:segment:bottom]
    depth = 30
    time = 20*60
    tank = airtank
    set_point = 0.0

    [dive:2]
    # surface_interval (in seconds)
    # for repetitive dives, you can specify the surface time between the previous
    # dive and this dive
    surface_interval = 60*60

    # automatic tank refill: if set to true, used tanks for this dive will be
    # refilled before the dive
    automatic_tank_refill = true


    tanks = airtank

    # segment list for this dive. At least ONE segment is mandatory

    [dive:2:segment:bottom]

    depth = 20
    time = 30*60
    tank = airtank
    set_point = 0.0

    # ============================== Other parameters ==============================
    [output]
    # template used for output result
    # templating uses jinja2, see documentation for more infos
    template = default.html

    [general]
    # deco model
    # choose between buhlmann ZHL16b or ZHL16c
    # ZHL16c is the default
    deco_model = ZHL16b

    # ppo2
    # defines the max and min_ppo2
    max_ppo2 = 1.4
    min_ppo2 = 0.19

    # max end
    # defines the max END for the dives
    max_end = 35

    # decent and ascent rate, in m/minute
    descent_rate = 17
    ascent_rate = 9

    # Gradient factors in %
    gf_low = 35
    gf_high = 85

    # type of water
    # possible values :
    # sea -- sea water
    # fresh -- fresh water
    water = fresh

    # dive altitude
    # in meter
    altitude = 1400

    # consumption rates
    # in liter / minute (the program does the conversion internally)
    dive_consumption_rate = 25
    deco_consumption_rate = 20

    # run_time flag
    # if true: segments represents runtime,
    # if false, segments represents segtime
    run_time = false

    # Use Open Circuit deco flag
    # if True, use enabled gases of decomp in oc or bailout
    use_oc_deco = false

    # multilevel_mode
    multilevel_mode = false

    # automatic_tank_refill
    # if 'automatic_tank_refill' is set to True, the tank will be full before the
    # dive. If set to False, it'll use the remaining gas from last dive
    automatic_tank_refill = false

    # ========================== Advanced  parameters ==============================
    # ========================= "Internal" Settings ================================
    # !!!   unless knowing what you're doing, this prefs should not be changed   !!!
    # !!!                                by the user                             !!!
    # ==============================================================================
    [advanced]
    # water density kg/l
    fresh_water_density = 1.0
    sea_water_density = 1.03

    absolute_max_ppo2 = 2.0
    absolute_min_ppo2 = 0.16

    # in bar
    absolute_max_tank_pressure = 300

    # in liter
    absolute_max_tank_size = 40

    # temperature at surface
    surface_temp = 30

    he_narcotic_value = 0.23
    n2_narcotic_value = 1.0
    o2_narcotic_value = 1.0
    ar_narcotic_value = 2.33

    # in meter
    stop_depth_increment = 3

    # in meter : last stop before surfacing
    last_stop_depth = 3

    # in second
    stop_time_increment = 1

    # one deco stop begun, force to stop to each deco depth
    # stop
    force_all_stops = true

    # surface pressure at sea level (in bar)
    ambiant_pressure_sea_level = 1.0

    # either simple (/10) or complex
    method_for_depth_calculation = simple

    # travel switch method
    # if 'late', dipplanner will try to keep the travel as long as possible
    #   until either MOD or max END
    # if 'early', dipplanner will switch to bottom tank as soon as is it breathable
    travel_switch = early

    # flight altitude
    # parameter used in no flight time calculation
    flight_altitude = 2450

Config file with default values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: ini

    # dipplanner config file
    # this file is used by the command line tool and
    # override the defaults parameters or input some dive profiles

    # This file represent default configuration, without any dive profile nor tank.

    [output]
    # template used for output result
    # templating uses jinja2, see documentation for more infos
    template = default-color.tpl

    [general]
    # deco model
    # choose between buhlmann ZHL16b or ZHL16c
    # ZHL16c is the default
    deco_model = ZHL16c

    # ppo2
    # defines the max and min_ppo2
    # default values :
    #   max_ppo2 : 1.6
    #   min_ppo2 : 0.21
    max_ppo2 = 1.6
    min_ppo2 = 0.21

    # max end
    # defines the max END for the dives
    # default value (in meter):
    # max_end : 30
    max_end = 30

    # decent and ascent rate, in m/minute
    descent_rate = 20
    ascent_rate = 10

    # Gradient factors in %
    gf_low = 30
    gf_high = 80

    # type of water
    # possible values :
    # sea -- sea water
    # fresh -- fresh water
    water = sea

    # dive altitude
    # in meter
    altitude = 0

    # consumption rates
    # in liter / minute (the program does the conversion internally)
    dive_consumption_rate = 17
    deco_consumption_rate = 12

    # run_time flag
    # if true: segments represents runtime,
    # if false, segments represents segtime
    run_time = true

    # Use Open Circuit deco flag
    # if True, use enabled gases of decomp in oc or bailout
    use_oc_deco = true

    # multilevel_mode
    multilevel_mode = false

    # automatic_tank_refill
    # if 'automatic_tank_refill' is set to True, the tank will be full before the
    # dive. If set to False, it'll use the remaining gas from last dive
    automatic_tank_refill = true

    # ========================== Advanced  parameters ==============================
    # ========================= "Internal" Settings ================================
    # !!!   unless knowing what you're doing, this prefs should not be changed   !!!
    # !!!                                by the user                             !!!
    # ==============================================================================
    [advanced]
    # water density kg/l
    fresh_water_density = 1.0
    sea_water_density = 1.03
    absolute_max_ppo2 = 2.0
    absolute_min_ppo2 = 0.16

    # in bar
    absolute_max_tank_pressure = 300

    # in liter
    absolute_max_tank_size = 40

    # temperature at surface
    surface_temp = 20

    he_narcotic_value = 0.23
    n2_narcotic_value = 1.0
    o2_narcotic_value = 1.0
    ar_narcotic_value = 2.33

    # in meter
    stop_depth_increment = 3

    # in meter : last stop before surfacing
    last_stop_depth = 3

    # in second
    stop_time_increment = 1

    # one deco stop begun, force to stop to each deco depth
    # stop
    force_all_stops = true

    # surface pressure at sea level (in bar)
    ambiant_pressure_sea_level = 1.01325

    # either simple (/10) or complex
    method_for_depth_calculation = complex

    # travel switch method
    # if 'late', dipplanner will try to keep the travel as long as possible
    #   until either MOD or max END
    # if 'early', dipplanner will switch to bottom tank as soon as is it breathable
    travel_switch = late

    # flight altitude
    # parameter used in no flight time calculation : it's the parameter needed
    # to calculate decompression until the altitude of the flight
    # the default value represents the maximum 'altitude equivalent' tolerated
    # in flight by international regulation
    # (8000 feet = 2 438.4 meters rounded to 2450m)
    flight_altitude = 2450