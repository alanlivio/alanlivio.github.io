---
title: Social Impact
---

{{config.extra.reseacher.shortbio_social_impact}}

{% for project in config.extra.reseacher.social_impact %}
## :fontawesome-solid-handshake: **{{ project.title }}**
------------------------------------
{{ project.description }}
{% if project.read_more.text %}
  Read more: <a href="{{ project.read_more.url }}">{{ project.read_more.text }}</a> :fontawesome-solid-link:
{% endif %}
<img  style="width: 240px; hight: 240px" src="{{ project.logo}}">
{% if project.url_video%}
  <iframe width="480" height="240" src="{{ project.url_video }}"frameborder="0"></iframe>
{% endif %}
<br>
{% endfor %}