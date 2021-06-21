from fastapi.testclient import TestClient

from app.database.schema import User


def test_create_user(client, session):
    User.filter(phone_number='01094766301').delete(auto_commit=True)
    response = client.put("/api/v1/auth/create", json={
        "phoneNumber": "01094766301",
        "passwd": "111111",
        "loginType": "Local",
        "accessToken": "",
        "deviceName": "y2q",
        "deviceModel": "SM-G986N",
        "deviceId": "264fd0328238a887",
        "os": "Android",
        "profileImg": "https://api.hatam.kr/static/upload/profileImg/408/t_f0cbf61079f0f31e5ae96605a9f93257.jpg",
        "nickName": "생계형개발자",
        "marketingReceive": "Y",
        "marketingNightReject": "Y",
        "thirdPartyAgree": "Y",
        "email": "chozza@hatam.kr"
    })
    assert response.status_code == 201
    assert response.text.find('Bearer') != -1


def test_login(client, session, login):
    response = client.post("/api/v1/auth/login", json={
        "phoneNumber": "01094766301",
        "passwd": "111111",
        "loginType": "Local",
        "accessToken": "",
        "deviceName": "y2q",
        "deviceModel": "SM-G986N",
        "deviceId": "264fd0328238a887",
        "os": "Android"
    })
    assert response.status_code == 200
    assert response.text.find('Bearer') != -1
