{% extends "base.tpl" %}

{%- macro color(text, color="white") -%}
  {%- if color == "red" %}{{'\033[91m'}}{% endif -%}
  {%- if color == "green" %}{{'\033[92m'}}{% endif -%}
  {%- if color == "yellow" %}{{'\033[93m'}}{% endif -%}
  {%- if color == "blue" %}{{'\033[94m'}}{% endif -%}
  {%- if color == "pink" %}{{'\033[95m'}}{% endif -%}
  {{- text -}}
  {{- '\033[0m'-}}
{%- endmacro -%}


{%- block separator %}
{{color("-------------------------------------------------------------------------------","blue")}}
{%- endblock -%}
