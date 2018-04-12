import pytest
from pyramid import testing

@pytest.fixture
def dummy_request():
    """
    Creates empty dummy request to server
    """
    return testing.DummyRequest()
