---
title: Projects
---

{% for project in config.extra.reseacher.projects %}
## :fontawesome-solid-code: **{{ project.title }}**
------------------------------------
{{ project.description }}
<img  style="width: 200px; hight: 200px" src="{{ project.logo}}">
{% if project.github %}
  :fontawesome-brands-github: <a href="{{ project.github.url }}"> {{ project.github.name }}</a>
{% else %}
  :fontawesome-solid-link: <a href="{{ project.read_more.url }}">{{ project.read_more.text }}</a>
{% endif %}
<br>
{% endfor %}