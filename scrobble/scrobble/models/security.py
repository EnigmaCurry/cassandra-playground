from pyramid.decorator import reify
from pyramid.request import Request
from pyramid.security import unauthenticated_userid
from pyramid.security import Allow
from pyramid.security import Everyone

import model

class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'view'),
                (Allow, 'group:loggedin', 'loggedin') ]
    def __init__(self, request):
        pass

USERS = {'ryan':'asdf'}

GROUPS = {'ryan':['group:users']}

def group_finder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])

class RequestWithUserAttribute(Request):
    @reify
    def user(self):
        userid = unauthenticated_userid(self)
        return userid
        # if userid is not None:
        #     # this should return None if the user doesn't exist
        #     # in the database
        #     return dbconn['users'].query({'id':userid})
