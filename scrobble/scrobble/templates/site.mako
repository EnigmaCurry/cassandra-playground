<html>
  <head>
    <title>Scrobble Cassandra Test</title>
    <link rel='stylesheet' href='/static/css/site.css' type='text/css' />
  </head>
  <body>
    <div id="header">
      <span id="app_title">Scrobbler</span>
    </div>
    <div id="right">
      <div id="login_box">
        % if request.user:
        Logged in as : ${request.user}
        % else:
        <form action="/login" method="post">
          <label for="login">Username:</label><input type="text" name="login"/><br/>
          <label for="login">Password:</label><input type="password" name="password"/><br/>
          <input type="submit" name="form.submitted" value="Log In"/><a href="/new_account">New Account</a><br/>
        </form>
        % endif
      </div>
    </div> 
    <div id="center">
      <div id="content">
        ${next.body()}
      </div>
    </div> 
    <div id="footer">
      <div id="footer_text">
        Copyright blah blah blah
      </div>
    </div>     
  </body>
</html>
