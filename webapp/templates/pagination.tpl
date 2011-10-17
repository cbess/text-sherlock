{% if page %}
<div class="pagination">
    <ul>
        {% if page.previous > 0 %}
        <li class='prev'>
            <a href="/search?q={{ search_text }}&p={{ page.previous }}">&larr; Previous</a>
        </li>
        {% else %}
        <li class="prev disabled">
            <a href="javascript:">&larr; Previous</a>
        </li>
        {% endif %}

        {% if page.next > 0 %}
        <li class="next">
            <a href="/search?q={{ search_text }}&p={{ page.next }}">Next &rarr;</a>
        </li>
        {% else %}
        <li class="nexxt disabled">
            <a href="javascript:">Next &rarr;</a>
        </li>
        {% endif %}
    </ul>
</div>
{% endif %}