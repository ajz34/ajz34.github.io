---
layout: archive
permalink: /categories/
title: "分类目录"
author_profile: true
---

{% include toc %}

{% assign sorted_categories = site.categories | sort %}
{% for category in sorted_categories %}
  <h2 class="archive__subtitle"></h2>
# {{ category | first }}
  {% for post in category.last %}
    {% include archive-single.html %}
  {% endfor %}
{% endfor %}
