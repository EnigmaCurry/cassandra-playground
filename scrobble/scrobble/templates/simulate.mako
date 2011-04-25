<%inherit file="site.mako"/>

Simulate listening to a track:<br/>
<table>
  <tr><td><label for="artist">Artist:</label></td><td><input type="text" name="artist" id="artist"/></td></tr>
  <tr><td><label for="album">Album:</label></td><td><input type="text" name="album" id ="album"/></td></tr>
  <tr><td><label for="title">Title:</label></td><td><input type="text" name="title"/ id="title"></td></tr>
  <tr><td></td><td><input type="button" id="simulate_listen" value="Submit Track"/></td></tr>
</table>


<script>
  var track_listen = function(){
    var track = {"artist":$("#artist").val(),
                 "album":$("#album").val(),
                 "title":$("#title").val(),
                 }
    ScrobbleActions.track_listen(track, function(){
      alert("Track submitted.");
    });
  }
  $(document).ready(function(){
    $("#simulate_listen").click(track_listen);
  });
</script>
