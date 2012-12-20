{%- block dive_header -%}
Dipplanner v{{ settings.__VERSION__ }}
{% endblock -%}

{%- for dive in dives -%}

{%- block separator -%}{%- endblock %}
Configuration : GF:{{ settings.GF_LOW*100 }}-{{ settings.GF_HIGH*100 }}
{%- if dive.is_repetitive_dive -%}
{{- color(" - Repetitive dive - surface interval: %s mins" % dive.get_surface_interval(), "yellow") }}
{%- endif -%}

{{ self.separator() }}
  {%- for exc in dive.dive_exceptions %}
  {{ color("Exception: ", "red")-}}
  {{ color(exc.__repr__(), "red") -}}
  : {{ color(exc.description, "red") }}
  {%- endfor -%}

  {%- for segment in dive.output_segments %}
    {{ "%8s"|format(segment.type|upper) -}}:
    {{- " at %3d"|format(segment.depth|int) -}}m for
    {{- segment.get_time_str() }} [RT:{{ segment.get_run_time_str() -}}], on
    {{- " %12s"|format(segment.tank|string) }}, SP:{{ segment.setpoint -}},
    {%- if segment.get_end() > settings.DEFAULT_MAX_END -%}
      {{-color(" END:%im"|format(segment.get_end()), "red") -}}
    {%- else -%}
      {{- " END:%im"|format(segment.get_end()) -}}
    {%- endif -%}
  {%- endfor -%}

{{ self.separator() }}
Gas: {% for tank in dive.tanks %}
    {{ " %12s"|format(tank|string) -}}: Total: {{- "%6.1f"|format(tank.total_gas) -}}l, Used:
    {{- "%6.1fl"|format(tank.used_gas) -}}
    {{- " (rem:%6.1fl or "|format(tank.remaining_gas) -}}
    {{- "%db"|format(tank.remaining_gas / tank.volume) -}})
  {%- if not tank.check_rule() %}
{{color("       WARNING !!! Not enought remaining gas in the %s tank (min:" % tank, "red") -}}
{{- color("%6.1fl) !"|format(tank.min_gas),"red") -}}
  {%- endif -%}
  {%- endfor -%}

{{ self.separator() }}
Oxygen Toxicity: OTU:{{ dive.model.ox_tox.otu|int }}, CNS:
  {{- "%d"|format(dive.model.ox_tox.cns*100)}}%
{{- self.separator() }}

{%- if dive.no_flight_time_value %}
{{ self.separator() }}
No-flight time: {{ dive.get_no_flight_hhmmss() }}
{{- self.separator() }}
{%- endif -%}
{% endfor -%}

{%- block dive_footer %}
WARNING : This software is highly experimental and
must not be used for actual dives. Use it at your own risk.
{%- endblock -%}
