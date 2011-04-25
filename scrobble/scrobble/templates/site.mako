<!doctype html>
<!--[if lt IE 7 ]> <html class="no-js ie6" lang="en"> <![endif]-->
<!--[if IE 7 ]>    <html class="no-js ie7" lang="en"> <![endif]-->
<!--[if IE 8 ]>    <html class="no-js ie8" lang="en"> <![endif]-->
<!--[if (gte IE 9)|!(IE)]><!--> <html class="no-js" lang="en"> <!--<![endif]-->
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">

  <title>Cassandra Scrobbler</title>
  <meta name="description" content="">
  <meta name="author" content="">

  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="shortcut icon" href="/static/favicon.ico">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">

  <link rel="stylesheet" href="/static/css/style.css?v=2">
  <link rel='stylesheet' href="/static/css/site.css?v=1" type='text/css' />
  <script src="/static/js/libs/modernizr-1.7.min.js"></script>
  <script src="//ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.js"></script>
  <script src="//ajax.googleapis.com/ajax/libs/dojo/1.6/dojo/dojo.xd.js" type="text/javascript"></script>
</head>

<body>
    <div id="header">
      <span id="app_title"><a href="/">Cassandra Scrobbler</a></span>
    </div>
    ${self.sidebar()}
    <div id="center">
      % if len(request.flash_messages) > 0:
        <div id="flash_message">
         <div id="flash_message_bg">
           % for msg in request.flash_messages:
           <p>${msg}</p>
           % endfor
         </div>
        </div>
      % endif
      <div id="content">
        ${next.body()}
      </div>
    </div> 
    <div id="footer">
      <div id="footer_text">
        Copyright Ryan McGuire blah blah blah
      </div>
    </div>
    
  <!-- scripts concatenated and minified via ant build script-->
  <script src="/static/js/plugins.js"></script>
  <script src="/static/js/site.js"></script>
  <!-- end scripts-->

  <!--[if lt IE 7 ]>
    <script src="js/libs/dd_belatedpng.js"></script>
    <script>DD_belatedPNG.fix("img, .png_bg");</script>
  <![endif]-->

</body>
</html>

<%def name="sidebar()">
    <div id="right">
      <div id="login_box">
        % if request.user:
          Logged in as :
          ${request.user.key} <a href="/logout">Logout</a>
          <br/><br/>
          <h1>Users you follow:</h1>
          <ul>
          % for u in request.user.get_following():
            <li><a href="/user/${u}">${u}</a></li>
          % endfor
          </ul>
          <br/>
          <h1>Users following you:</h1>
          <ul>
          % for u in request.user.get_followers():
            <li><a href="/user/${u}">${u}</a></li>
          % endfor
          </ul>
        % else:
        <form action="/login" method="post">
          <label for="login">Username:</label><input type="text" name="login"/><br/>
          <label for="login">Password:</label><input type="password" name="password"/><br/>
          <input type="submit" name="form.submitted" value="Log In"/><a href="/new_account">New Account</a><br/>
        </form>
        % endif
      </div>
    </div> 
</%def>
