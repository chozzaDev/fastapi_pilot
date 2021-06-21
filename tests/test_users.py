def test_users(client, session, login):
    response = client.get("/api/v1/users", headers=login)
    assert response.status_code == 200
