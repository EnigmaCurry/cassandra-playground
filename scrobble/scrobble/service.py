import pycassa
import json
from pyramid.security import remember, forget, authenticated_userid
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config

from scrobble.models import model, security

@view_config(route_name="api_whoami", request_method='GET', permission="api")
def whoami(request):
    return Response(json.dumps(request.user.key))

@view_config(route_name="api_login", request_method='POST', permission="view")
def login(request):
    args = json.loads(request.body)
    if security.check_user_password(args["username"], args["password"]):
        headers = remember(request, args["username"])
        headers.append(("Cache-Control","no-cache"))
        request.session.flash("Logged in.")
        return HTTPFound(location = "/api/whoami",
                         headers = headers)
    
@view_config(route_name="api_track_listen", request_method='POST', permission="api")
def track_listen(request):
    song = json.loads(request.body)
    request.user.record_track(song)
    return Response(json.dumps("ok"))
