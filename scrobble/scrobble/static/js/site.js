(function ($) {
    $.extend({
        postJSON: function (url, jsonData, success, options) {
            var config = {
                url: url,
                type: "POST",
                data: jsonData ? JSON.stringify(jsonData) : null,
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: success
            };
            $.ajax($.extend(options, config));
        }
    });
})(jQuery);

var ScrobbleActions = function(){
  var track_listen = function(track, callback){
    $.postJSON("/api/track_listen",track, callback);
  }
  var follow_user = function(userid, callback){
    $.postJSON("/api/follow_user", userid, callback);
  }
  var unfollow_user = function(userid, callback){
    $.postJSON("/api/unfollow_user", userid, callback);
  }
  return {
      "track_listen": track_listen,
      "follow_user": follow_user,
      "unfollow_user": unfollow_user
  }
}();

$(document).ready(function(){
        var flash_msg = $("#flash_message");
        if(flash_msg){
            $("#flash_message").fadeIn("slow").delay(2000).fadeOut("slow", function(){
                    flash_msg.remove();
                });
        }
    });
