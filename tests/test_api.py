from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200

def test_api_root():
    response = client.get("/api")
    assert response.status_code == 200
    assert "available_endpoints" in response.json()

def test_search_title_endpoint():
    response = client.get("/api/search/title", params={
        "keywords": "cancer",
        "max_results": 5
    })
    assert response.status_code == 200
    data = response.json()
    assert "total_results" in data
    assert "articles" in data
    assert len(data["articles"]) <= 5

def test_search_date_endpoint():
    response = client.get("/api/search/date", params={
        "start_date": "2024/01/01",
        "end_date": "2024/03/01",
        "max_results": 5
    })
    assert response.status_code == 200
    data = response.json()
    assert "total_results" in data
    assert "articles" in data

def test_search_abstract_endpoint():
    response = client.get("/api/search/abstract", params={
        "keywords": "covid",
        "max_results": 5
    })
    assert response.status_code == 200
    data = response.json()
    assert "total_results" in data
    assert "articles" in data