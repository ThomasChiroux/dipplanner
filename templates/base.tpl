{%- block dive_header -%}
Dipplanner v{{ settings.__VERSION__ }}
{%- endblock -%}

{%- block separator -%}{%- endblock -%}

{%- block dive_profile_header %}
Configuration : GF:{{ settings.GF_LOW*100 }}-{{ settings.GF_HIGH*100 }}
{%- endblock -%}

{{ self.separator() }}

{%- block dive_profile -%}
  {%- for segment in output_segments %}
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
{%- endblock -%}

{{ self.separator() }}

{%- block dive_gas %}
Gas: {% for tank in tanks %}
    {{ " %12s"|format(tank|string) -}}: Total: {{- "%6.1f"|format(tank.total_gas) -}}l, Used:
    {{- "%6.1fl"|format(tank.used_gas) -}}
    {{- " (rem:%6.1fl or "|format(tank.remaining_gas) -}}
    {{- "%db"|format(tank.remaining_gas / tank.tank_vol) -}})
  {%- if not tank.check_rule() %}
{{color("       WARNING !!! Not enought remaining gas in the %s tank (min:" % tank, "red") -}}
{{- color("%6.1fl) !"|format(tank.min_gas),"red") -}}
  {%- endif -%}
  {%- endfor -%}
{%- endblock -%}

{{ self.separator() }}

{%- block dive_otu_cns %}
Oxygen Toxicity: OTU:{{ model.ox_tox.otu|int }}, CNS:
  {{- "%d"|format(model.ox_tox.cns*100)}}%
{%- endblock -%}

{{ self.separator() }}

{%- block dive_footer %}
WARNING : This software is highly experimental and
must not be used for actual dives. Use it at your own risk.
{%- endblock -%}
