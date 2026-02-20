---
title: CV
hide:
- navigation
- toc
---

## :fontawesome-solid-briefcase: Experience

{% for xp in config.extra.researcher.experience %}
  *{{ xp.role }}* at [{{ xp.place }}]({{ xp.url }})</a>.
  <span style="float: right;">{{ xp.period }}</span>
{% endfor %}

## :fontawesome-solid-graduation-cap: Education

{% for edu in config.extra.researcher.education %}
  *{{ edu.course }}* at [{{ edu.institution }}]({{ edu.url }}).
  <span style="float: right;">{{ edu.period }}</span>
{% endfor %}

## :fontawesome-solid-award: Honors & Awards

{% for accom in config.extra.researcher.accomplishments %}
  [{{ accom.organization }}]({{ accom.certificate_url }})
  <span style="float: right;">{{ accom.year}}</span>
  <br>*{{accom.title}}*
{% endfor %}

<div style="text-align: center;" markdown>
:fontawesome-solid-file: [See full CV file](cv.pdf)
</div>
<div style="text-align: center;" markdown>
:fontawesome-solid-file: [See list of certificates](certificates.pdf)
</div>
