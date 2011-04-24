<%inherit file="site.mako"/>
<form action="${url}" method="post">
  <label for="login">Username:</label><input type="text" name="login" value="${login}"/><br/>
  <label for="password">Password:</label><input type="password" name="password" value="${password}"/><br/>
  <input type="submit" name="form.submitted" value="Create Account"/><br/>
</form>
