.. _dipplanner_cmdline:

dipplanner command-line documentation
=====================================

when invoking dipplanner, you may specify any of these options:

.. code-block:: bash

    dipplanner [-h] [--help]
               [--version]
               [-c] [--config]
               [--surfaceinterval]
               [--model]
               [--gflow]
               [--gfhigh]
               [--water]
               [--altitude]
               [--diveconsrate]
               [--decoconsrate]
               [--descentrate]
               [--ascentrate]
               [--maxppo2]
               [--minppo2]
               [--maxend]
               [--samegasfordeco]
               [--forcesegmenttime]
               [--depthcalcmethod]
               [--travelswitch]
               [--surfacetemp]
               [--ambiantpressureatsea]
               [--template]
               [-t] [-tank]
               [-s] [-segment]

Either presence of tank and segment inside a config file or in command
line are needed for this program to run

help
****

.. cmdoption:: -h, --help

    show help message and exit

version
*******

.. cmdoption:: --version

    show version number and exit

config files
************


.. cmdoption:: -c <STRING>, --config <STRING>

    path for config file.

    Default : ./config.cfg

    see :ref:`dipplanner_configfile` for more informations on config files

    .. note::

        Multiple config files MAY be loaded by providing multiple -c options.

        each config file may contain different parameter, but some parameters
        may also appear in multiple config files. In that case, the last
        occurence of that parameter is used.

        except of tanks and segments: all tanks and segments provided are
        used for the dives (see config-file documentation for more infos)

tanks and segments
******************

.. cmdoption:: -t <STRING>, --tank <STRING>

    specify a tank that will be used for the dive

    Format: ::

                "tank_name;f_o2;f_he;Volume(l);Pressure(bar);Minimum gas rule"


    * tank_name: (str) (you choose the name) for the tank
    * f_02: (float) fraction of oxygen in the tank. Between 0.0 and 1.0
    * f_he: (float) fraction of helium in the tank. Between 0.0 and 1.0
    * Volume: (float) Volume of the tank in bar
    * Pressure: (float) Pressure of the tank in bar
    * Minimum gas rule: (str) quantity of gas that should remain in the
      tank after the dive

      There two format for minimum gas rule:

      * quantity of bar that should remain in the tank:

        format: "[0-9]+b"

        ex: "50b": it should remain 50 bar in the tank at the end of the dive
      * "fraction rule" (like `the rule of third in cave diving <http://en.wikipedia.org/wiki/Rule_of_thirds_%28diving%29>`_)

        format: "1/[0-9]"

        ex1: "1/3" : 1/3 of the tank to go in, 1/3 of the tank to go back and it should remain 1/3 of the tank at the end of the dive

        ex2: "1/6" : 1/6 of the tank to go in, 1/6 of the tank to go back and it should remain 2/3 of the tank at the end of the dive

    Example:

    12l tank filled with 200b or air. It should remain 50b at the end of the dive.

    ::

        "airtank;0.21;0.0;12;200,50b"

    .. note::

        Multiple tanks may be provided

        ex:

        dipplanner -t "airtank;0.21;0.0;12;200,50b" -t "nitrox;0.80;0.0;12;200;50b"

.. cmdoption:: -s <STRING>, --segment <STRING>

    Input segments used for the dive

    Format:  ::

                "depth;duration;tank;setpoint"

    * depth: (float) in meter
    * duration: (float) in seconds (operators are allowed like: '30 * 60')
    * tank: name of the tank (the 'tank_name' specified in -t option)
    * setpoint: (float) 0.0 if OC, setpoint if CCR

      .. note::

            If you specify a setpoint > 0.0, the dive will automatically switch
            in CCR mode.

    Example:

    20 min at 30 meter using tank: airtank in OC mode

    ::

        "30;20*60;airtank;0.0"

    .. note::

        You can specify multiple segments

        ex:

        dipplanner -s "30;1000;airtank;0.0" -s "20;800;airtank;0.0"

dive parameters
***************

.. cmdoption:: --surfaceinterval=<VALUE>

    Optional Surface Interval in seconds

    If provided, dipplanner will calculate a surface decompression before
    diving.

    Example:

    One hour of surface interval
    ::

        dipplanner --surfaceinterval=3600


.. cmdoption:: --model=<ZHL16b|ZHL16c>

    Set the decompression model used for the calculations:
    either buhlmann ZHL16b or buhlmann ZHL16c

    Default: ZHL16c

    Example:

    ::

        dipplanner --model=ZHL16b


.. cmdoption:: --gflow=<VALUE>

    GF low: (int) in %, between 0 and 100

    Default: 30%

    Example:

    GF low of 25%

    ::

        dipplanner --gflow=25%


    .. note::

        Internally, GFlow is a float number between 0.0 and 1.0, but for
        convenience, the argument in command line is provided in % value,
        between 0 and 100. The conversion is done automatically.


.. cmdoption:: --gfhigh=<VALUE>

    GF high: (int) in %, between 0 and 100

    Default: 80%

    Example:

    GF high of 85%

    ::

        dipplanner --gfhigh=85%


    .. note::

        Internally, GFhigh is a float number between 0.0 and 1.0, but for
        convenience, the argument in command line is provided in % value,
        between 0 and 100. The conversion is done automatically.

.. cmdoption:: --water=<sea|fresh>

    specify in which type of water you will do the dive: sea or fresh

    Default: sea

    Example:

    Do a dive in a lake

    ::

        dipplanner --water=fresh


.. cmdoption:: --altitude=<VALUE>

    altitude (int) of the dive in meter.

    .. warning::

        It's very important to specify this parameter if you do a dive in altitude

    Default: 0m (sea level)

    Example:

    Dive at 1400m

    ::

        dipplanner --altitude=1400


.. cmdoption:: --diveconsrate=<VALUE>

    gas consumption rate (float) during dive (in l/minute).

    Is it used for tank monitoring and associated with tank size, pressure and
    tank rules, it will warn you if your plannified dive ends without enough gas.

    Default: 17 l/min

    Example:

    Plan a dive with 25 l/min dive consumption rate

    ::

        dipplanner --diveconsrate=25


    .. note::

        Internally, the consumption rates are in l/second, but for
        convenience, the argument in command line is provided in l/min.
        The conversion is done automatically

.. cmdoption:: --decoconsrate=<VALUE>

    gas consumption rate (float) during deco (in l/minute).

    Default: 12 l/min

    Example:

    Plan a dive with 20 l/min deco consumption rate

    ::

        dipplanner --decoconsrate=20


    .. note::

        Internally, the consumption rates are in l/second, but for
        convenience, the argument in command line is provided in l/min.
        The conversion is done automatically

.. cmdoption:: --descentrate=<VALUE>

    descent rate (float) (in m/minute).

    Default: 20 m/min

    Example:

    Plan a dive with 17 m/min descent rate

    ::

        dipplanner --descentrate=17


    .. note::

        Internally, the ascent and descent rates are in m/second, but for
        convenience, the argument in command line is provided in m/min.
        The conversion is done automatically

.. cmdoption:: --ascentrate=<VALUE>

    ascent rate (float) (in m/minute).

    Default: 10 m/min

    Example:

    Plan a dive with 9 m/min ascent rate

    ::

        dipplanner --ascentrate=9


    .. note::

        Internally, the ascent and descent rates are in m/second, but for
        convenience, the argument in command line is provided in m/min.
        The conversion is done automatically

.. cmdoption:: --maxppo2=<VALUE>

    max allowed ppo2 (float) for this dive.

    Default: 1.6

    Example:

    Set the max allowed ppo2 at 1.4

    ::

        dipplanner --maxppo2=1.4


.. cmdoption:: --minppo2=<VALUE>

    minimum allowed ppo2 for this dive.

    Default: 0.21

    Example:

    Set the min allowed ppo2 at 0.19

    ::

        dipplanner --minppo2=0.19


.. cmdoption:: --maxend=<VALUE>

    max END (Equivalent narcosis Depth) allowed for this dive, in meter

    Default: 30 m

    Example:

    Set the max END at 35m

    ::

        dipplanner --maxend=35


    .. note::
        end calculation is based on narcotic index for all gases.

        By default, dipplanner considers that oxygen is narcotic
        (same narcotic index than nitrogen)

        All narcotic indexes can by changed in the config file,
        in the [advanced] section

.. cmdoption:: --samegasfordeco

    if set, do not use deco tanks (or bailout) for decompressions

    Default: <not set>

    By default, dipplanner will automatically switch to best mix for deco
    and if CCR, it will switch to deco bailout if it's best for decompression.

    If you set this option, dipplanner will keep the last bottom gas used in OC
    or will still use CCR setpoint of last segment for deco

    Example:

    force the use of same gas for deco

    ::

        dipplanner --samegasfordeco


.. cmdoption:: --forcesegmenttime

    if set, each input segment will be dove
    at the full time of the segment.

    By default the segment time is shortened by descent or ascent time


    Example:

    ::

        dipplanner --forcesegmenttime


Advanced Parameters
*******************

.. cmdoption:: --depthcalcmethod=<simple|complex>

    method used for pressure from depth calculation.

    * simple method uses only +10m = +1bar
    * complex methods uses real water density calculation

    Default: complex

    Example:

    switch depth calc method to simple

    ::

        dipplanner --depthcalcmethod=simple


.. cmdoption:: --travelswitch=<late|early>

    Travel switch method (late or early).

    * if late, it will keep the travel as long as possible (until either MOD or max END)
    * if early, it will switch to bottom tank as soon as is it breathable

    Default: late

    Example:

    switch travel switch to early

    ::

        dipplanner --travelswitch=early


.. cmdoption:: --surfacetemp=<VALUE>

    Temperature at surface (float) in celcius

    Default: 20 °C

    Example:

    change surface temperature to 30 °C

    ::

        dipplanner --surfacetemp=30

.. cmdoption:: --ambiantpressureatsea=<VALUE>

    Change ambiant pressure at sea level (float) (in bar)

    Default: 1.01325 b

    Example:

    change ambiant pressure at sea level to 1 bar

    ::

        dipplanner --ambiantpressureatsea=1.0

Output Parameters
*****************

.. cmdoption:: --template=<TEMPLATE>

    Name of the template to be used
    The template file should be present in templates directory

    see :ref:`dipplanner_templates` for more infos on templates

    Default: default-color.tpl

    Example:

    switch to html template and store the ouput in a html file

    ::

        dipplanner --template=default.html > dive1.html

