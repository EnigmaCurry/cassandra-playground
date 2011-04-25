import pyramid.config
from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid_beaker import session_factory_from_settings
from scrobble.models import model, security

from scrobble import service

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    model.setup()

    session_factory = session_factory_from_settings(settings)
    
    config = Configurator(
        settings=settings,
        root_factory=security.RootFactory,
        authentication_policy=AuthTktAuthenticationPolicy(
            settings["cookie_secret"],
            callback=security.group_finder),
        authorization_policy=ACLAuthorizationPolicy())

    config.set_request_factory(security.RequestWithUserAttribute)
    config.set_session_factory(session_factory)
    config.add_static_view("static", "scrobble:static")
    config.add_route("home", "/",
                     view="scrobble.views.list_users",
                     view_renderer="list_users.mako")
    config.add_route("new_account", "/new_account",
                     view="scrobble.login.new_account",
                     view_renderer="new_account.mako")
    config.add_route("login", "/login",
                     view="scrobble.login.login")
    config.add_route("logout", "/logout",
                     view="scrobble.login.logout",
                     view_renderer="logout.mako")
    config.add_route("list_users", "/users",
                     view="scrobble.views.list_users",
                     view_renderer="list_users.mako")
    config.add_route("user_home", "/user/{user}",
                     view="scrobble.views.user_home",
                     view_renderer="user_home.mako")

    
    config.add_route("test", "/test",
                     view="scrobble.views.test",
                     view_renderer="test.mako")

    config.add_route("api_login", "api/login")
    config.add_route("api_whoami", "api/whoami")
    config.add_route("api_track_listen", "api/track_listen")
    config.scan()
    return config.make_wsgi_app()
