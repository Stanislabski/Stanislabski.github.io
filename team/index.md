---
title: Team
nav:
  order: 3
  tooltip: About our team
redirect_from:
  - /lab-members
  - /alums
  - /mascots
  - /staff
  - /trainees
---

# {% include icon.html icon="fa-solid fa-users" %}Team

Our team is united by a shared interest in understanding how molecular and microbial data can be used to improve human health. We bring together diverse backgrounds in epidemiology, statistics, computational biology, and biomedical sciences to ask interdisciplinary questions and develop meaningful solutions.

We value inclusion, curiosity, and collaboration. We believe that a supportive and respectful environment helps everyone thrive, and we are committed to fostering a lab culture where each person’s contributions and experiences are valued.

Our team includes postdocs, graduate students, staff scientists, and collaborators from a range of institutions and disciplines.

{% include list.html data="members" component="portrait" filter="role == 'principal-investigator' and group != 'alum'" %}
{% include list.html data="members" component="portrait" filter="role != 'principal-investigator' and group != 'alum'" %}

{% include section.html dark=true %}

We value collaboration and regularly work with scientists from different fields and institutions. If you’re interested in joining our team or exploring potential research partnerships, we’d be excited to connect with you.

{%
  include button.html
  icon="fa-solid fa-handshake-angle"
  text="Join the Team"
  link="contact"
  style="button"
%}

{% include section.html %}

## Alumni

Our former lab members have made meaningful contributions that continue to shape our work. Whether they’ve pursued careers in academia, industry, or other paths, they will always remain part of our broader lab community.

{% include list.html data="members" component="portrait" filter="group == 'alum'" style="small" %}

{% include gallery.html %}

{% include section.html %}
