<%inherit file="site.mako"/>
<p>User: ${user.key}</p>


<div id="recent_tracks">
  Recently Listened Tracks:
  <ul>
    % for song in user.get_songs(limit=10):
    <li>${song["artist"]} - ${song["title"]}</li>
    % endfor
  </ul>
</div>
