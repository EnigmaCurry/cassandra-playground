<%inherit file="site.mako"/>

<div id="follow_link">
% if request.user is not None and not is_personal_page:
 % if request.user.is_following(user.key):
  You are following ${user.key} ( <a href="#" id="follow_link">unfollow</a> )
 % else:
  <a href="#" id="follow_link">Follow ${user.key}</a>
 % endif
% endif
</div>

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

<script>
  var user = "${user.key}"
  var is_personal_page = false;
  var is_following = false;
  % if request.user is not None:
   % if is_personal_page:
  is_personal_page = true;
   % elif request.user.is_following(user.key):
  is_following = true;
   % endif
  % endif

  $(document).ready(function(){
    var reload_callback = function(){window.location.reload()}
    if(is_personal_page == false){
      $("#follow_link").click(function(){
        if(is_following){
         ScrobbleActions.unfollow_user(user, reload_callback);
        } else {
         ScrobbleActions.follow_user(user, reload_callback);
        }
      });
    }
  });
</script>
