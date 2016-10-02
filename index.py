#!main.py
{% extends "base.html" %}
{% macro two_way_radio(name, label_off, label_on, default) %}
<label><input type="radio" name="{{ name }}" value="off" {% if not default %}checked{% endif %}>{{ label_off }}</label>
<label><input type="radio" name="{{ name }}" value="on" {% if default %}checked{% endif %}>{{ label_on }}</label>
{%- endmacro %}
{% macro pronouns(prs) %}
{% if prs == None %}[no pronouns]{% else %}{{ "/".join(prs[:-1]) }}  ({{ prs[0] }} {{ "are" if prs[-1] else "is" }}){% endif %}
{%- endmacro %}
{% macro pronouns_edit(prs, i) %}
{% if prs == None %}{% for j in range(5) %}<input type="text" name="pr{{ i }}_{{ j }}" value="{{ prs[j] }}">{% endfor %}{{ two_way_radio("pr%d_p" % i, "is", "are", false) }}
{% else %}{% for j in range(5) %}<input type="text" name="pr{{ i }}_{{ j }}" value="{{ prs[j] }}">{% endfor %}{{ two_way_radio("pr%d_p" % i, "is", "are", prs[5]) }}{% endif %}
{%- endmacro %}
{% macro users(block) %}
<table border="1">
<tr><td>kerberos</td><td>honorific</td><td>names</td><td>pronouns</td><td>acceptable alternatives</td></tr>
{% for user in block %}
<tr><td>{{ user.kerberos }}</td>
    <td>{% if user.prefixes %}{{ user.prefixes[0] }}{% if user.prefixes[1:] %} (or: {{ ", ".join(user.prefixes[1:]) }}){% endif %}{% else %}[no honorific]{% endif %}</td>
    <td>{% if user.names %}{{ user.names[0] }}{% for name in user.names[1:] %}<br>{{ name }}{% endfor %}{% else %}[no name; use kerberos]{% endif %}</td>
    <td>{{ pronouns(user.preferred) }}</td>
    <td>{% if user.accepted %}{{ pronouns(user.accepted[0]) }}{% for accepted in user.accepted[1:] %}<br>{{ pronouns(accepted) }}{% endfor %}{% else %}[no alternatives]{% endif %}</td></tr>
{% endfor %}
</table>
{%- endmacro %}
{% macro user_edit(user) %}
<table border="1">
<tr><td>kerberos</td><td>honorific</td><td>names</td><td>pronouns</td><td>acceptable alternatives</td></tr>
<tr id="uedit"><td>{{ user.kerberos }}</td>
    <td>{% for prefix in user.prefixes %}<input type="text" name="prefixes" value="{{ prefix }}"><br>{% endfor %}<input type="text" name="prefixes" value=""></td>
    <td>{% for name in user.names %}<input class="pname" type="text" name="names" value="{{ name }}"><br>{% endfor %}<input class="pname" type="text" name="names" value=""></td>
    <td id="uedit_pronouns">{{ pronouns_edit(user.preferred, 0) }}<br>Common pronouns: <input type="button" value="she"><input type="button" value="he"><input type="button" value="they"></td>
    <td><label><input type="checkbox" name="prthey" {% if user.accept_they %}checked{% endif %}>accept they/them (default)</label>{% if user.accept_nothey %}{% for i, accepted in enumerate(user.accept_nothey, 1) %}<br>{{ pronouns_edit(accepted, i) }}{% endfor %}{% endif %}<br>{{ pronouns_edit(["", "", "", "", "", False], len(user.accept_nothey) + 1) }}</td></tr>
</table>
{%- endmacro %}

{% block head %}{{ super() }}
<style type="text/css">
    input[type=text] { width: 70px; }
    input[type=text].pname { width: 120px; }
    input[type=button] { width: 80px; }
    table { width: 100%; }
</style>
{% endblock %}
{% block title %}home{% endblock %}
{% block content %}
NOTE: pronouns@mit is a service in early pre-alpha. do not expect anything at all. <br>
Hello, {{ kerberos }}! <br>
Here are your registered pronouns:<br>
<form action="update.py" method="post">
{{ user_edit(user) }}
<input type="submit" value="update pronouns"><br>
<br>
</form>
Here's a list of all pronouns:
{{ users(fetched) }}
<script>
    var inputs = document.getElementById("uedit_pronouns").getElementsByTagName("input");
    function set_primary(arr, is_plural) {
        var ti = 0;
        for (var i = 0; i < inputs.length; i++) {
            if (inputs[i].type == "text") {
                inputs[i].value = arr[ti++];
            } else if (inputs[i].type == "checkbox") {
                inputs[i].checked = is_plural;
            }
        }
    }
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].type == "button") {
            inputs[i].onclick = function() {
                if (inputs[this].value == "she") {
                    set_primary(["she", "her", "her", "hers", "herself"], false);
                } else if (inputs[this].value == "he") {
                    set_primary(["he", "him", "his", "his", "himself"], false);
                } else if (inputs[this].value == "they") {
                    set_primary(["they", "them", "their", "theirs", "themself"], true);
                }
            }.bind(i);
        }
    }
</script>
<br><br>
Send all complaints, suggestions, and pained grimaces to <a href="mailto://pronouns@mit.edu">pronouns@mit.edu</a>.
{% endblock %}
