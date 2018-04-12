from pyramid.view import view_config
from pyramid.response import Response
from . import DB_ERR_MSG
from sqlalchemy.exc import DBAPIError
from ..models import Stock
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPBadRequest
import requests

API_URL = 'https://api.iextrading.com/1.0'


@view_config(
    route_name='stock',
    renderer='../templates/stock-detail.jinja2')
def stock_view(request):
    """
    GET and POST routes for searching and adding an individual stock
    """
    if request.method == 'GET':
        try:
            symbol = request.GET['symbol']
        except KeyError:
            return {}
        try:
            response = requests.get(API_URL + '/stock/{}/company'.format(symbol))
            data = response.json()
            return {'company': data}
        except ValueError:
            raise HTTPNotFound()
    if request.method == 'POST':
        try:
            symbol = request.POST['symbol']
        except KeyError:
            raise HTTPBadRequest()

        try:
            response = requests.get(API_URL + '/stock/{}/company'.format(symbol))
            data = response.json()
        except ValueError:
            raise HTTPNotFound()

        isntance = Stock(**data)

        try:
            request.dbsession.add(instance)
        except DBAPIError:
            return Response(DB_ERR_MSG, content_type='text/plain', status=500)
        
        return HTTPFound(location=request.route_url('portfolio'))


@view_config(
    route_name='portfolio',
    renderer='../templates/portfolio.jinja2')
def portfolio_view(request):
    """
    Returns portfolio view with data from postgres
    """

    try:
        query = request.dbsession.query(Stock)
        user_entries = query.filter(Stock.account_id == request.authenticated_userid)
    except DBAPIError:
        return DBAPIError(DB_ERR_MSG, content_type='text/plain', status=500)

    return {'stocks': all_entries}


@view_config(
    route_name='detail',
    renderer='../templates/portfolio-detail.jinja2',)
def portfolio_stock_view(request):
    """
    Shows individual stock
    """
    try:
        entry_id = request.matchdict['symbol']
    except IndexError:
        raise HTTPNotFound()

    try:
        query = request.dbsession.query(Stock)
        stock_detail = query.filter(
            Stock.account_id == request.authenticated_userid).filter(
                Stock.symbol == entry_id).one_or_none()
    except DBAPIError:
        return Response(DB_ERR_MSG, content_type='txt/plain', status=500)

    if stock_detail is None:
        raise HTTPNotFound()
    
    return {'stock': stock_detail}



