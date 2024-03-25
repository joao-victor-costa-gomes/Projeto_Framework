import pytest
from api import API


@pytest.fixture
def test_basic_route(api):
     @api.route("/home")
     def home(req, resp):
         resp.text = "HELLO"

     with pytest.raises(AssertionError):
             @api.route("/home")
             def home2(req, resp):
                 resp.text = "HELLO"

def test_bumbo_test_client_can_send_requests(api, client):
    RESPONSE_TEXT = "THIS IS COOL"

    @api.route("/hey")
    def cool(req, resp):
        resp.text = RESPONSE_TEXT

    assert client.get("http://testserver/hey").text == RESPONSE_TEXT

def test_default_404_response(client):
    response = client.get("http://testserver/doesnotexist")

    assert response.status_code == 404 
    assert response.text == "Not found."

def test_alternative_adding_route(api, client):
    RESPONSE_TEXT = "Alternative way to add a route."

    def home(req, resp):
        resp.text = RESPONSE_TEXT

    api.add_route("/alternative", home)
    assert client.get("http://testserver/alternative").text == RESPONSE_TEXT

