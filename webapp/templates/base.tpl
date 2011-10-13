<html class='{{ html_css_class }}'>
    <head>
        <meta http-equiv="Content-type" content="text/html; charset=utf-8"/>
        <title>{% block title %}{{ title }}{% endblock %} - Text Sherlock</title>
        <link rel="stylesheet" href="/static/css/bootstrap.min.css">
        <link rel="stylesheet" href="/static/css/main.css" type="text/css" media="screen" charset="utf-8">
        <script src='/static/js/jquery.min.js'></script>
        {% block header %}

        {% endblock %}
    </head>
    <body>
        <div id="content">
        {% block content %}
            Content here
        {% endblock %}
        </div>
    </body>
</html>