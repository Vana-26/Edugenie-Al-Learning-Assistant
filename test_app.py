import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get('/')
    assert response.status_code == 200
    assert 'EduGenie' in response.text

def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'

def test_empty_question():
    response = client.post('/api/qa', json={'text': ''})
    assert response.status_code == 400
