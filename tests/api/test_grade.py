import pytest

def test_get_grades(client):
    response = client.get('api/v1/grades')
    assert response.status_code == 200


