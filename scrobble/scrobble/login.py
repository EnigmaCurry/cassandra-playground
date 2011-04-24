from pyramid.url import route_url
from pyramid.security import remember, forget, authenticated_userid
from pyramid.httpexceptions import HTTPFound
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
        if security.USERS.get(login) == password:
            headers = remember(request, login)
            return HTTPFound(location = came_from,
                             headers = headers)
        message = 'Failed login'

    return dict(
        message = message,
        url = request.application_url + '/login',
        came_from = came_from,
        login = login,
        password = password,
        )
    
def logout(request):
    headers = forget(request)
    return HTTPFound(location = route_url('home', request),
                     headers = headers)

def new_account(request):
    new_account_url = route_url('new_account', request)
    referrer = request.url
    if referrer == new_account_url:
        referrer = '/' # never use the form itself as came_from
    came_from = request.params.get('came_from', referrer)

    login = ''
    password = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        #Make sure the user doesn't yet exist:
        try:
            model.User.get(login)
        except pycassa.NotFoundException:
            #Good, new user.
            pass
        else:
            #User already exists
            pass
        
    return dict(
        url = request.application_url + "/new_account",
        login = login,
        password = password
        )
