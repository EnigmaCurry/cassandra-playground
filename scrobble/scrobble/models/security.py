import pycassa
from pyramid.decorator import reify
from pyramid.request import Request
from pyramid.security import unauthenticated_userid
from pyramid.security import Allow
from pyramid.security import Everyone
import bcrypt

import model

class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'view'),
                (Allow, 'group:users', 'api') ]
    def __init__(self, request):
        pass

class RequestWithUserAttribute(Request):
    @reify
    def user(self):
        userid = unauthenticated_userid(self)
        if userid is not None:
            try:
                return model.User.get(userid)
            except pycassa.NotFoundException:
                return None
        return None
    @reify
    def flash_messages(self):
        return self.session.pop_flash()            

def group_finder(userid, request):
    try:
        return request.user.get_groups()
    except AttributeError:
        return []

def check_user_password(user, password):
    try:
        user_hash = model.UserPassword.get(user).password_hash
    except pycassa.NotFoundException:
        return False
    return user_hash == bcrypt.hashpw(password, user_hash)

def save_user_password(user, password):
    model.User.get(user) #raise NotFoundException if no user
    user_pw = model.UserPassword()
    user_pw.key = user
    user_pw.password_hash = bcrypt.hashpw(password,bcrypt.gensalt())
    user_pw.persist()

