<%inherit file="site.mako"/>

<form action="${url}" method="post">
  <table>
    <tr>
      <td>
        <label for="login">Username:</label>
      </td>
      <td>
        <input type="text" name="login" value="${login}"/>
      </td>
    </tr>
    <tr>
      <td>
        <label for="password">Password:</label>
      </td>
      <td>
        <input type="password" name="password" value="${password}"/><br/>
      </td>
    </tr>
    <tr>
      <td>
        <label for="email">Email:</label>
      </td>
      <td>
        <input type="text" name="email" value="${email}"/>
      </td>
    </tr>
    <tr>
    <tr>
      <td>
        <label for="fname">First Name:</label>
      </td>
      <td>
        <input type="text" name="fname" value="${fname}"/>
      </td>
    </tr>
    <tr>
    <tr>
      <td>
        <label for="lname">Last Name:</label>
      </td>
      <td>
        <input type="text" name="lname" value="${lname}"/>
      </td>
    </tr>
    <tr>
      <td></td>
      <td>
        <input type="submit" name="form.submitted" value="Create Account"/>
      </td>
    </tr>
  </table>
</form>

<%def name="sidebar()">
## No sidebar when making new accounts
</%def>
