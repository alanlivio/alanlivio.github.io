---
title: About Me
hide:
  - navigation
  - toc
---

<!-- profile grid -->

<div class="profile-grid" markdown>
<div markdown> <!-- left grid -->
  ![]({{ config.extra.researcher.photo }}){: .profile-photo }
  <div class="profile-name">{{ config.extra.researcher.name }}</div>
  <div class="profile-role">{{ config.extra.researcher.role }}</div>
  <p class="profile-icons" markdown>
  {%- for social in config.extra.researcher.social -%}
    {% set icon = social.icon.replace('/', '-') %}
    [:{{ icon }}:]({{ social.link }})
  {%- endfor -%}
  </p>
</div>
<div markdown> <!-- right grid -->
{{ config.extra.researcher.shortbio }}
**Interests**
<br>
{%- for item in config.extra.researcher.interests -%}
  :material-book-open-variant: {{ item }} <br>
{%- endfor -%}
</div>
</div>

<!-- Experience, Education, Awards -->

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
