from pyramid.view import (notfound_view_config, forbidden_view_config)
from pyramid.httpexceptions import HTTPFound


@notfound_view_config(renderer='../templates/404.jinja2')
def notfound_view(request):
    """
    Returns 404 response if no route
    """
    request.response.status = 404
    return {}


@forbidden_view_config(renderer='../templates/404.jinja2')
def forbidden_view(request):
    """
    Returns 404 response if route is forbidden
    """
    request.response.status = 404
    return {}

