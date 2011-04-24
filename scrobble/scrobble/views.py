import pycassa
from pyramid.response import Response
from pyramid.view import view_config

from scrobble.models import model, security

# def my_view(request):
#     dbsession = DBSession()
#     root = dbsession.query(MyModel).filter(MyModel.name==u'root').first()
#     return {'root':root, 'project':'scrobble'}



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
    return {'user':user}

