from fastapi.testclient import TestClient

from server.src.main import app

client = TestClient(app)


def test_create_ed_forms():
    response = client.post("/educational_forms", json={'name': 'Очная'})
    assert response.status_code == 200

