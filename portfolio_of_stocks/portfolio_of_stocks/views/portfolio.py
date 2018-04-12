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
        if not all([field in request.POST for field in ['companyName', 'symbol', 'exchange', 'website', 'ceo', 'industry', 'sector', 'issueType', 'description']]):
            raise HTTPBadRequest
        # import pdb; pdb.set_trace()
        query = request.dbsession.query(Account)
        instance = query.filter(Account.username == request.authenticated_userid).first()

        query = request.dbsession.query(Stock)
        instance2 = query.filter(Stock.symbol == request.POST['symbol']).first()

        if instance2:
            instance2.account_id.append(instance)
        else:
            new = Stock()
            new.account_id.append(instance)
            new.companyName = request.POST['companyName']
            new.symbol = request.POST['symbol']
            new.exchange = request.POST['exchange']
            new.website = request.POST['website']
            new.CEO = request.POST['ceo']
            new.industry = request.POST['industry']
            new.sector = request.POST['sector']
            new.issueType = request.POST['issueType']
            new.description = request.POST['description']

            try:
                request.dbsession.add(new)
                request.dbsession.flush()
            except IntegrityError:
                pass

        return HTTPFound(location=request.route_url('portfolio'))

    return HTTPNotFound()


@view_config(
    route_name='portfolio',
    renderer='../templates/portfolio.jinja2',
    request_method='GET')
def portfolio_view(request):
    """
    Returns portfolio view with data from postgres
    """
    try:
        query = request.dbsession.query(Account)
        instance = query.filter(Account.username == request.authenticated_userid).first()
    except DBAPIError:
        return Response(DB_ERR_MSG, content_type='text/plain', status=500)
    if instance:
        return {'entries': instance.stock_id}
    else:
        return HTTPNotFound()


@view_config(
    route_name='detail',
    renderer='../templates/portfolio-detail.jinja2',
    request_method='GET')
def portfolio_stock_view(request):
    """
    Shows individual stock
    """
    try:
        stock_id = request.matchdict['symbol']
    except KeyError:
        return HTTPNotFound()

    try:
        query = request.dbsession.query(Stock)
        stock_detail = query.filter(Stock.symbol == stock_id).first()
        for each in stock_detail.account_id:
            if each.username == request.authenticated_userid:
                return {'data': stock_detail}
        raise HTTPNotFound()
    except DBAPIError:
        return Response(DB_ERR_MSG, content_type='txt/plain', status=500)



