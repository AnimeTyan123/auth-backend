from fastapi.testclient import TestClient
from auth import app

client = TestClient(app)

def test_registration():
    response = client.post(
        "/register",
        json={"username": "test_user", "password": "test_password"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}
    print("Register test passed")

def test_login():
    # Ensure registration first
    client.post(
        "/register",
        json={"username": "test_user", "password": "test_password"}
    )
    response = client.post(
        "/login",
        json={"username": "test_user", "password": "test_password"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Login successful"}
    print("Login test passed")

def test_login_wrong_password():
    # Ensure registration first
    client.post(
        "/register",
        json={"username": "test_user", "password": "test_password"}
    )
    response = client.post(
        "/login",
        json={"username": "test_user", "password": "wrong_password"}
    )
    assert response.status_code == 400
    assert response.json().get("detail") == "Incorrect username or password"
    print("Wrong password test passed")

test_registration()
test_login()
test_login_wrong_password()

