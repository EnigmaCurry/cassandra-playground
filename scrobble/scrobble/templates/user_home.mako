<%inherit file="site.mako"/>

% if len(recent_tracks) > 0:
 <div id="recent_tracks">
   <h1>${user.key.title()}'s Recent Tracks:</h1>
   <table>
     % for track in recent_tracks:
     <tr>
       <td>${track["artist"]} -
       ${track["title"]}</td><td>${track["english_delta"]} ago</td>
     </tr>
     % endfor
   </table>
 </div>
% else:
 % if is_personal_page:
  <h1>Welcome ${user.fname}!</h1>
  <br/>
  You haven't listened to anything yet.
 % else:
   ${user.key} hasn't listened to anything yet.
 % endif
% endif
