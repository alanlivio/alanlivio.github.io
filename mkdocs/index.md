---
title: About Me
---

<center>
<img  style="width: 255px; hight: 255p; border-radius: 50%" src="{{config.extra.reseacher.github_avatar}}">
<br><br>{{config.extra.reseacher.name}}, {{config.extra.reseacher.role}}
<br><br>
<!-- %- usage: https://jinja.palletsprojects.com/en/3.0.x/templates/#whitespace-control -->
{%- for social in config.extra.social -%}
  {% set icon = social.icon.replace('/','-') %} 
  :{{icon}}: [{{ social.title }}]({{ social.link }})&nbsp;
 {%- endfor -%}  
:fontawesome-solid-file-lines: [CV pdf]({{config.extra.reseacher.cv_file}})
</span>
</center>


<!-- Short Bio -->
## :fontawesome-solid-user-tie: Short Bio
------------------------------------
{{config.extra.reseacher.shortbio}}

<!-- Interests -->
## :fontawesome-solid-flask: Research interests
------------------------------------
{% for interest in config.extra.reseacher.interests %}
* {{interest}}
{% endfor %}

<!-- Experience -->
## :fontawesome-solid-briefcase: Experience
------------------------------------
{% for xp in config.extra.reseacher.experience %}
  [{{ xp.place }}]({{ xp.url }}), {{ xp.location }}</a>. *{{ xp.role }}*
  <span style="float: right;">{{ xp.period }}</span>
{% endfor %}

<!-- Education -->
## :fontawesome-solid-graduation-cap: Education
------------------------------------
{% for edu in config.extra.reseacher.education %}
  [{{ edu.institution }}]({{ edu.url }}), *{{ edu.course }}*. 
  <span style="float: right;">{{ edu.period }}</span>
{% endfor %}

<!-- Honors & Awards -->
## :fontawesome-solid-award: Honors & Awards
------------------------------------
{% for accom in config.extra.reseacher.accomplishments %}
  [{{ accom.organization }}]({{ accom.certificate_url }})
  <span style="float: right;">{{ accom.year}}</span>
  <br>*{{accom.title}}*
{% endfor %}