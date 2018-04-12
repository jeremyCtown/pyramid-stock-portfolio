from pyramid.httpexceptions import HTTPFound, HTTPBadRequest, HTTPUnauthorized
from pyramid.security import NO_PERMISSION_REQUIRED, remember, forget
from pyramid.response import Response
from sqlalchemy.exc import DBAPIError, IntegrityError
from pyramid.view import view_config
from ..models import Account
from . import DB_ERR_MSG


@view_config(
    route_name='auth',
    renderer='../templates/auth.jinja2',
    permission=NO_PERMISSION_REQUIRED)
def auth_view(request):
    """
    Takes request from auth route and returns a response
    """
    if request.method == 'POST':
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']

        except KeyError:
            return HTTPBadRequest()

        try: 
            instance = Account(
                username=username,
                email=email,
                password=password,
            )

            headers = remember(request, userid=instance.username)

            try:
                request.dbsession.add(instance)
                request.dbsession.flush()
            except IntegrityError:
                return {'error': 'something went wrong'}

            return HTTPFound(location=request.route_url('portfolio'), headers=headers)

        except DBAPIError:
            return Response(DB_ERR_MSG, content_type='text/plain', status=500)

    if request.method == 'GET':
        try:
            uername = request.GET['username']
            password = request.GET['password']

        except KeyError:
            return{}

        is_authenticated = Account.check_credentials(request, username, password)
        if is_authenticated[0]:
            headers = remember(request, userid=username)
            return HTTPFound(location=request.route_url('portfolio'), headers=headers)
        else:
            return HTTPUnauthorized('401 - NotAuthorized')

    return HTTPFound(location=request.route_url('home'))

@view_config(route_name='logout')
def logout(request):
    """
    Logs user out and resets headers
    """
    headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)
