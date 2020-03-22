{% if page %}
<nav>
    <ul class="pagination">
        {% if page.previous > 0 %}
        <li class="page-item">
            <a class="page-link" href="/search?q={{ search_text }}&p={{ page.previous }}">&larr;</a>
        </li>
        {% else %}
        <li class="page-item disabled">
            <a class="page-link" href="javascript:">&larr;</a>
        </li>
        {% endif %}

        {% if page.next > 0 %}
        <li class="page-item">
            <a class="page-link" href="/search?q={{ search_text }}&p={{ page.next }}">&rarr;</a>
        </li>
        {% else %}
        <li class="page-item disabled">
            <a class="page-link" href="javascript:">&rarr;</a>
        </li>
        {% endif %}
    </ul>
</nav>
{% endif %}