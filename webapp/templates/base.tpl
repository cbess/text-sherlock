<html class="{{ html_css_class }}">

    <head>
        <meta http-equiv="Content-type" content="text/html; charset=utf-8"/>
        <title>{% block title %}{{ title }}{% endblock %} - {{ site_title }}</title>
        <link rel="stylesheet" href="/static/css/bootstrap.min.css">
        <link rel="stylesheet" href="/static/css/main.css" type="text/css" charset="utf-8">

        {% block header %}
        {% endblock %}
    </head>

    <body>
        <nav class="navbar navbar-{{ site_banner_color }} bg-{{ site_banner_color }}">
            <a class="navbar-brand" href="/">
                <!-- Start custom banner HTML here -->
                {{ site_banner_text }}
                <!-- End custom banner HTML here -->
            </a>

            {% if doc %}
            <form action="/search" class="header-search form-inline" method="GET">
                <div>
                    <input type="search"
                           class="form-control mr-sm-2"
                           aria-label="Search"
                           name="q"
                           autocomplete="off"
                           autocorrect="off"
                           value="{{ search_text }}"
                           placeholder="Search text"
                           id="text" />
                    <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
                </div>
            </form>
            {% endif %}
        </nav>

        <div id="content">
        {% block content %}
            Content here
        {% endblock %}
        </div>
<!--
    For His glory (Hebrews 1, Colossians 1, Genesis 1).
    Copyright 2011 Christopher Bess
-->
    </body>
</html>
