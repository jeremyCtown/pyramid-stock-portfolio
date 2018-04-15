from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPBadRequest
from pyramid.security import remember


def test_pass_this_travis():
    """
    Tests Travis initial connection
    """
    pass


def test_default_behavior_of_home_view(dummy_request):
    """
    Tests default behavior of home view
    """
    from ..views.base import home_view
    from pyramid.httpexceptions import HTTPFound

    response = home_view(dummy_request)
    assert response.status_code == 302


def test_default_response_auth_view(dummy_request):
    """
    Tests default behavior of auth view
    """
    from ..views.auth import auth_view

    response = auth_view(dummy_request)
    assert response == {}


def test_account_sign_up_and_login(dummy_request):
    """
    Tests basic auth signup and signin interactivity
    """
    from ..views.auth import auth_view
    from pyramid.httpexceptions import HTTPFound

    dummy_request.POST = {'username': 'watdude', 'password': 'watup', 'email': 'watdude@wat.com'}
    dummy_request.method = 'POST'
    response = auth_view(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)
    dummy_request.GET = {'username': 'watdude', 'password': 'watup'}
    dummy_request.method = 'GET'
    response = auth_view(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


def test_bad_auth_signin_view(dummy_request):
    """
    Tests bad sign-in raise 401 response
    """
    from ..views.auth import auth_view
    from pyramid.httpexceptions import HTTPFound

    dummy_request.GET = {'username': 'watdude', 'password': 'watup'}
    response = auth_view(dummy_request)
    assert response.status_code == 401


def test_bad_auth_request(dummy_request):
    """
    Tests bad signup post method
    """
    from ..views.auth import auth_view
    from pyramid.httpexceptions import HTTPBadRequest

    dummy_request.POST = {'password': 'watup', 'email': 'watdude@wat.com'}
    dummy_request.method = 'POST'
    response = auth_view(dummy_request)
    assert response.status_code == 400
    assert isinstance(response, HTTPBadRequest)


def test_bad_request_method_auth_signup_view(dummy_request):
    """
    Tests bad signup put method 
    """
    from ..views.auth import auth_view
    from pyramid.httpexceptions import HTTPFound

    dummy_request.POST = {'password': 'watup', 'email': 'watdude@wat.com'}
    dummy_request.method = 'PUT'
    response = auth_view(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


def test_account_added_to_database(db_session, test_account):
    """
    Test adding a new account to the database and ensure unique IDs
    """
    from ..models import Account

    assert len(db_session.query(Account).all()) == 0
    account = test_account
    db_session.add(account)
    assert len(db_session.query(Account).all()) == 1
    db_session.add(account)
    assert len(db_session.query(Account).all()) == 1
    db_session.add(Account(username='jeremy', email='jeremy@watup.com', password='password'))
    assert len(db_session.query(Account).all()) == 2


def test_stock_added_to_db(db_session):
    """
    Tests stock is added to database
    """
    from ..models import Stock

    assert len(db_session.query(Stock).all()) == 0
    stock = Stock(
        companyName='JRC Enterprises',
        symbol='JRCE',
    )
    db_session.add(stock)
    assert len(db_session.query(Stock).all()) == 1


def test_stock_with_no_symbol_throws_error(db_session):
    """
    Tests that symbol is required to post stock
    """
    from ..models import Stock
    import pytest
    from sqlalchemy.exc import IntegrityError

    assert len(db_session.query(Stock).all()) == 0
    stock = Stock(
        companyName='test 1',
    )
    with pytest.raises(IntegrityError):
        db_session.add(stock)

        assert db_session.query(Stock).one_or_none() is None


def test_auth_signup_view(dummy_request):
    """
    Tests basic auth signup functionality
    """
    from ..views.auth import auth_view
    from pyramid.httpexceptions import HTTPFound

    dummy_request.POST = {'username': 'watdude', 'password': 'watup', 'email': 'watdude@wat.com'}
    dummy_request.method = 'POST'
    response = auth_view(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


def test_default_not_found(dummy_request):
    """
    Tests not found response
    """
    from ..views.notfound import notfound_view

    assert notfound_view(dummy_request) == {}


def test_default_logout(dummy_request):
    """
    Tests logout works
    """
    from ..views.auth import logout
    from pyramid.httpexceptions import HTTPFound

    response = logout(dummy_request)
    assert isinstance(response, HTTPFound)


def test_default_response_portfolio_view(dummy_request):
    """
    Tests empty portfolio returns HTTPNotFound
    """
    from ..views.portfolio import portfolio_view

    response = portfolio_view(dummy_request)
    assert isinstance(response, HTTPNotFound)


def test_default_portfolio_stock_view(dummy_request, db_session, test_stock, test_account):
    """
    Tests portfolio stock view from portfolio
    """
    from ..views.portfolio import portfolio_stock_view

    test_stock.account_id.append(test_account)
    db_session.add(test_stock)
    db_session.add(test_account)

    dummy_request.matchdict = {'symbol': 'JRCE'}
    response = portfolio_stock_view(dummy_request)
    assert type(response) == dict
    assert response['stock'].symbol == 'JRCE'


def test_detail_not_found(dummy_request):
    """
    Tests HTTPNotFound for non-existent stock in portfolio
    """
    from ..views.portfolio import portfolio_stock_view
    from pyramid.httpexceptions import HTTPNotFound

    response = portfolio_stock_view(dummy_request)
    assert isinstance(response, HTTPNotFound)


def test_default_response_stock_view(dummy_request):
    """
    Tests default response to empty request
    """
    from ..views.portfolio import stock_view

    response = stock_view(dummy_request)
    assert len(response) == 0
    assert type(response) == dict


def test_default_response_search_view(dummy_request):
    """
    Test default response on stock search
    """
    from ..views.portfolio import stock_view
    
    request = dummy_request
    request.GET = {'symbol': 'AAPL'}
    response = stock_view(dummy_request)
    assert type(response) == dict


def test_valid_stock_post_adds_record_to_db(dummy_request, test_account, db_session):
    """
    Tests adding a stock to the database
    """
    from ..views.portfolio import stock_view
    from ..models import Stock

    db_session.add(test_account)

    dummy_request.method = 'POST'
    dummy_request.POST = {
        "symbol": "TST",
        "companyName": "test",
        "exchange": "test",
        "industry": "test",
        "website": "test",
        "description": "test",
        "ceo": "test",
        "issueType": "test",
        "sector": "test",
    }

    response = stock_view(dummy_request)
    query = db_session.query(Stock)
    one = query.first()
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)
    assert one.companyName == 'test'
    assert one.symbol == 'TST'
    assert type(one.id) == int
    

def test_invalid_stock_post(dummy_request):
    """
    Tests invalid stock is not added
    """
    import pytest
    from ..views.portfolio import stock_view
    from pyramid.httpexceptions import HTTPBadRequest

    dummy_request.method = 'POST'
    dummy_request.POST = {}

    with pytest.raises(HTTPBadRequest):
        response = stock_view(dummy_request)
        assert isinstance(response, HTTPBadRequest)


def test_jeremy_is_awesome():
    """
    Tests a universal truth
    """
    assert True
