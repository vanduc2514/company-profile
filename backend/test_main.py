from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data

def test_auto_search_empty_company_name():
    response = client.post("/api/search", json={"companyName": ""})
    assert response.status_code == 400

def test_auto_search_valid_company_name():
    response = client.post("/api/search", json={"companyName": "OpenAI"})
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert "companyName" in data
    assert data["companyName"] == "OpenAI"
    assert "inputs" in data
    assert data["inputs"]["google"] != ""

def test_analyze_valid_payload():
    response = client.post("/api/analyze", json={
        "inputs": {
            "google": "Stripe Inc payment software SaaS cloud tech API global enterprise $65B",
            "linkedin": "Stripe 7000 employees financial services",
            "website": "stripe.com payment processing for internet",
            "registration": "Delaware C Corp CIK 0001859665"
        }
    })
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["industry"] == "Technology / SaaS"
    assert data["scale"] == "Large Enterprise"
    assert data["confidenceScore"] > 70
