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

**THIS PAGE IS COPIED FROM CASEY'S LABWEBSITE, NEED TO CHANGE**

Our lab is made up of a highly engaged and collaborative team of researchers.
We recognize that diverse teams do better research.
We foster an environment where team members are treated equally, and where we respect and admire our differences.
The team includes postdocs, students at all levels, staff, and our lab mascots.

{% include list.html data="members" component="portrait" filter="role == 'principal-investigator' and group != 'alum'" %}
{% include list.html data="members" component="portrait" filter="role != 'principal-investigator' and group != 'alum'" %}

{% include section.html dark=true %}

We work with a wide range of outstanding groups from around the world, and we're always on the lookout for new and unique perspectives.
We want to push the frontier of data science and train the next generation of data scientists.

{%
  include button.html
  icon="fa-solid fa-handshake-angle"
  text="Join the Team"
  link="join"
  style="button"
%}

{% include section.html %}

## Alumni

Gone but never forgotten.
These are past lab members who have moved on to the [Childhood Cancer Data Lab](https://www.alexslemonade.org/data-lab), other school programs, new jobs, or elsewhere.
They have all made lasting contributions to science and to our hearts.

{% include list.html data="members" component="portrait" filter="group == 'alum'" style="small" %}

{% include section.html %}
