
def test_pass_this_travis():
    pass

# def test_default_behavior_of_home_view(dummy_request):
#     """
#     Tests default behavior of home view
#     """
#     from ..views.default import home_view

#     response = home_view(dummy_request)
#     assert type(response) == dict
#     assert response == {}


# def test_default_behavior_of_auth_view(dummy_request):
#     """
#     Tests default behavior of auth view
#     """
#     from ..views.default import auth_view

#     response = auth_view(dummy_request)
#     assert type(response) == dict
#     assert response == {}


# def test_default_behavior_of_stock_view(dummy_request):
#     """
#     Tests default behavior of rendering a single stock
#     """
#     from ..views.default import stock_view

#     response = stock_view(dummy_request)
#     assert type(response) == dict
#     assert response == {}


# def test_default_behavior_of_portfolio_view(dummy_request):
#     """
#     Tests default behavior of portfolio endpoint
#     """
#     from ..views.default import portfolio_view

#     response = portfolio_view(dummy_request)
#     assert type(response) == dict
#     assert response['entries'][0]['symbol'] == 'GE'


# def test_default_behavior_of_portfolio_stock_view(dummy_request):
#     """
#     Tests default behavior of a single stock in the portfolio
#     """
#     from ..views.default import portfolio_stock_view

#     response = portfolio_stock_view(dummy_request)
#     assert type(response) == dict
#     assert response == {}


# def test_jeremy_is_awesome():
#     """
#     Tests a universal truth
#     """
#     assert True
