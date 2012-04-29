Dive profile : GF:{{ settings.GF_LOW*100 }}-{{ settings.GF_HIGH*100 }}
{% for segment in output_segments %}
{{- "%8s"|format(segment.type|upper) }}: at
{{- "%3d"|format(segment.depth|int) }}m for
{{- segment.get_time_str() }} [RT:{{ segment.get_run_time_str() }}], on
{{- " "+segment.tank|string }}, SP:{{ segment.setpoint }}, END:{{segment.get_end() }}m
{% endfor %}
Gas: {% for tank in tanks %}
  {{ tank }}: Total: {{ "%.1f"|format(tank.total_gas) }}l, Used:
  {{- "%.1fl"|format(tank.used_gas) }} (rem:
  {{- "%.1fl or "|format(tank.remaining_gas) }}
  {{- "%db"|format(tank.remaining_gas / tank.tank_vol) }})
{%- if not tank.check_rule() %}
     WARNING !!! Not enought remaining gas in tank (min:
     {{- "%.1fl"|format(tank.min_gas) }}) !"
{%- endif %}
{% endfor -%}
Oxygen Toxicity: OTU:{{ model.ox_tox.otu|int }}, CNS:
{{- "%d"|format(model.ox_tox.cns*100)}}%
