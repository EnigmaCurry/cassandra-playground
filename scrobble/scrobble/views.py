import pycassa
from pyramid.response import Response
from pyramid.view import view_config
from datetime import datetime, timedelta

from scrobble.models import model, security
from scrobble.util.relative_dates import timesince

def list_users(request):
    users = list(model.User.get_all_usernames())
    return {'users':users}
    
def user_home(request):
    try:
        user = model.User.get(request.matchdict['user'])
    except pycassa.NotFoundException:
        response = Response("Unknown user : {0}".format(
                request.matchdict['user']))
        response.status_int = 404
        return response
    tracks = user.get_tracks(limit=10)
    for t in tracks:
        t["english_delta"] = timesince(datetime.utcfromtimestamp(
                long(t["listen_date"])),now=datetime.utcnow())
    is_personal_page = hasattr(request,"user") and request.user is not None \
        and (user.key == request.user.key)
    
    return {'user':user, "recent_tracks":tracks,
            "is_personal_page":is_personal_page}

def test(request):
    return {}

