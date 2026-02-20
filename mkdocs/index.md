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

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;" markdown>
<div markdown>
**Interests**<br>
{%- for item in config.extra.researcher.interests -%}
  :material-book-open-variant: {{ item }} <br>
{%- endfor -%}
</div>
<div markdown>
**Applications**<br>
{%- for item in config.extra.researcher.applications -%}
  :material-book-open-variant: {{ item }} <br>
{%- endfor -%}
</div>
</div>

</div>

<!-- Experience, Education, Awards -->
