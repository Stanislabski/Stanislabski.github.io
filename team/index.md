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

Our team includes postdocs, graduate students, undergraduates, staff scientists, and collaborators from a range of institutions and disciplines.

{% include list.html data="members" component="portrait" filter="role == 'principal-investigator' and group != 'alum'" %}
{% include list.html data="members" component="portrait" filter="role != 'principal-investigator' and group != 'alum'" %}

{% include section.html dark=true %}

We actively collaborate with researchers across institutions and disciplines. If you're interested in joining our group or working together on shared research interests, we’d love to hear from you.

{%
  include button.html
  icon="fa-solid fa-handshake-angle"
  text="Join the Team"
  link="contact"
  style="button"
%}

{% include section.html %}

## Alumni

We are proud of our former lab members and grateful for the lasting impact they’ve made on our work and community. Whether continuing in academia, industry, or new adventures, they remain part of our extended lab family.

{% include list.html data="members" component="portrait" filter="group == 'alum'" style="small" %}

{% include section.html %}
