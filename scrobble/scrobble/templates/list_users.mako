<%inherit file="site.mako"/>

% if len(users) > 0:
Users:
<ul>
 % for user in users:
 <li><a href="/user/${user}">${user}</a></li>
 % endfor
</ul>
% else:
 No Users created yet.
% endif
