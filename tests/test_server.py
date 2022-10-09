from fastapi.testclient import TestClient


def test_hello_200(api_client: TestClient):
    """
    GET /hello/<name> OK
    """
    response = api_client.get("/hello/doggo")
    assert response.json() == {"message": "Hello doggo"}
