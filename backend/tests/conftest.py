import pytest
import requests
import os
import uuid

BASE_URL = os.environ.get('EXPO_PUBLIC_BACKEND_URL', 'http://localhost:8000').rstrip('/')


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def api():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


@pytest.fixture(scope="session")
def auth_token(api):
    """Try login with seeded test user; otherwise signup a new test user."""
    # Try login first
    r = api.post(f"{BASE_URL}/api/auth/login", json={"email": "test@test.com", "password": "password123"})
    if r.status_code == 200:
        return r.json()["access_token"], r.json()["user"]
    # Fallback: create
    email = f"TEST_{uuid.uuid4().hex[:8]}@example.com"
    r = api.post(f"{BASE_URL}/api/auth/signup", json={"email": email, "password": "password123", "name": "Tester"})
    assert r.status_code == 200, f"Signup failed: {r.status_code} {r.text}"
    return r.json()["access_token"], r.json()["user"]


@pytest.fixture(scope="session")
def auth_headers(auth_token):
    token, _ = auth_token
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


@pytest.fixture(scope="session")
def fresh_user(api):
    """A brand new user (for SRS state isolation)."""
    email = f"TEST_{uuid.uuid4().hex[:8]}@example.com"
    r = api.post(f"{BASE_URL}/api/auth/signup", json={"email": email, "password": "password123", "name": "FreshTester"})
    assert r.status_code == 200
    data = r.json()
    headers = {"Authorization": f"Bearer {data['access_token']}", "Content-Type": "application/json"}
    return {"user": data["user"], "headers": headers, "email": email}
