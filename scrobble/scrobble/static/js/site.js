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

$(document).ready(function(){
        var flash_msg = $("#flash_message");
        if(flash_msg){
            $("#flash_message").fadeIn("slow").delay(2000).fadeOut("slow", function(){
                    flash_msg.remove();
                });
        }
    });
