import pycassa
import datetime
from pyramid.url import route_url
from pyramid.security import remember, forget, authenticated_userid
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from scrobble.models import model, security

def login(request):
    login_url = route_url('login', request)
    referrer = request.url
    if referrer == login_url:
        referrer = '/' # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        #Check the password hash:
        if security.check_user_password(login, password):
            headers = remember(request, login)
            headers.append(("Cache-Control","no-cache"))
            request.session.flash("Logged in.")
            return HTTPFound(location = came_from,
                             headers = headers)
        else:
            request.session.flash("Login failed!")
            return HTTPFound(location = came_from)
            
    
def logout(request):
    headers = forget(request)
    headers.append(("Cache-Control","no-cache"))
    request.session.flash("Logged out.")
    return HTTPFound(location = route_url('home', request),
                     headers = headers)

def new_account(request):
    new_account_url = route_url('new_account', request)
    referrer = request.url
    login = ''
    password = ''
    email=''
    fname=''
    lname=''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        email = request.params['email']
        fname = request.params['fname']
        lname = request.params['lname']
        #Make sure the user doesn't yet exist:
        try:
            model.User.get(login)
        except pycassa.NotFoundException:
            #Good, new user.
            new_user = model.User()
            new_user.key = login
            new_user.fname = fname
            new_user.lname = lname
            new_user.email = email
            new_user.set_groups(["group:users"])
            new_user.created = datetime.datetime.now()
            new_user.persist()
            security.save_user_password(login, password)
            headers = remember(request, login)
            request.session.flash("Account created.")
            return HTTPFound(location = "/user/{0}".format(login),
                             headers = headers)
        else:
            #User already exists
            request.session.flash("Account name already taken.")
        
    return dict(
        url = request.application_url + "/new_account",
        login = login,
        password = password,
        email = email,
        fname = fname,
        lname = lname
        )
