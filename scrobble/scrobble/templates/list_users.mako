<%inherit file="site.mako"/>
Users:

<ul>
% for user in users:
<li><a href="/user/${user}">${user}</a></li>
% endfor
</ul>
