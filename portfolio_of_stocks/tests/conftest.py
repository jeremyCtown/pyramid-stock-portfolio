import os
import pytest
from pyramid import testing
from ..models.meta import Base
from ..models import Stock, Account

@pytest.fixture
def dummy_request(db_session):
    """
    Creates empty dummy request to server
    """
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture
def test_account():
    return Account(username='watdude', email='watdude@watup.com', password='password')


@pytest.fixture
def test_stock():
    """
    Creates testable dummy values
    """
    return Stock(
        companyName='JRC Enterprises',
        symbol='JRCE'
    )


@pytest.fixture
def configuration(request):
    """
    Set up database for testing
    """
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgres://localhost:5432/stock_test'
    })
    config.include('portfolio_of_stocks.models')
    config.include('portfolio_of_stocks.routes')

    config.testing_securitypolicy(
        userid='watdude',
        permissive=True,
    )

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture
def db_session(configuration, request):
    """
    Create dummy session for interacting with test database
    """
    SessionFactory = configuration.registry['dbsession_factory']
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session
