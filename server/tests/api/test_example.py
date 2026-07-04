def test_get_examples(client):
    response = client.get("/api/v1/example/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
