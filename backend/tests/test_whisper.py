"""Tests for /api/speaking/transcribe (Whisper) endpoint."""
import os
import io
import requests
import pytest

BASE_URL = os.environ.get('EXPO_PUBLIC_BACKEND_URL', 'https://mandarin-speak-2.preview.emergentagent.com').rstrip('/')


@pytest.fixture(scope="module")
def token():
    r = requests.post(f"{BASE_URL}/api/auth/login",
                      json={"email": "test@test.com", "password": "password123"})
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


@pytest.fixture(scope="module")
def auth_only_headers(token):
    # NOTE: do NOT set Content-Type — requests will set multipart boundary
    return {"Authorization": f"Bearer {token}"}


# Minimal-ish m4a header bytes (not a valid full m4a, but >100 bytes so it passes size check)
def _fake_audio_bytes(size=2048):
    # Start with an ftyp/m4a-ish atom header then random bytes
    header = b"\x00\x00\x00\x20ftypM4A \x00\x00\x00\x00M4A mp42isom"
    return header + (b"\x00\x11\x22\x33" * ((size - len(header)) // 4))


class TestWhisperEndpoint:
    def test_requires_auth(self):
        files = {"file": ("a.m4a", _fake_audio_bytes(), "audio/m4a")}
        r = requests.post(f"{BASE_URL}/api/speaking/transcribe",
                          params={"target_chinese": "你好"}, files=files)
        # No Bearer token -> 401 (auto_error=False but get_current_user raises 401)
        assert r.status_code == 401, f"Expected 401 without auth, got {r.status_code}: {r.text}"

    def test_missing_file_returns_422(self, auth_only_headers):
        r = requests.post(f"{BASE_URL}/api/speaking/transcribe",
                          headers=auth_only_headers,
                          params={"target_chinese": "你好"})
        assert r.status_code == 422, r.text

    def test_tiny_file_rejected(self, auth_only_headers):
        files = {"file": ("a.m4a", b"123", "audio/m4a")}
        r = requests.post(f"{BASE_URL}/api/speaking/transcribe",
                          headers=auth_only_headers,
                          params={"target_chinese": "你好"},
                          files=files)
        assert r.status_code == 400, r.text
        assert "too small" in r.json().get("detail", "").lower()

    def test_unsupported_extension_normalized(self, auth_only_headers):
        # send a .xyz extension; server should treat it as m4a internally.
        # The Whisper call will likely 502 on this fake audio — that's acceptable.
        files = {"file": ("a.xyz", _fake_audio_bytes(), "application/octet-stream")}
        r = requests.post(f"{BASE_URL}/api/speaking/transcribe",
                          headers=auth_only_headers,
                          params={"target_chinese": "你好"},
                          files=files)
        # Either Whisper succeeded (200) or failed gracefully (502). Must not be 5xx other than 502.
        assert r.status_code in (200, 502), f"Unexpected status {r.status_code}: {r.text}"

    def test_valid_extension_endpoint_shape(self, auth_only_headers):
        files = {"file": ("a.m4a", _fake_audio_bytes(4096), "audio/m4a")}
        r = requests.post(f"{BASE_URL}/api/speaking/transcribe",
                          headers=auth_only_headers,
                          params={"target_chinese": "你好"},
                          files=files,
                          timeout=60)
        assert r.status_code in (200, 502), f"Unexpected status {r.status_code}: {r.text}"
        if r.status_code == 200:
            data = r.json()
            assert "transcribed_text" in data
            # With target_chinese provided, response should include comparison
            for key in ("score", "correct", "feedback", "target_text"):
                assert key in data, f"Missing {key} in 200 response: {data}"
            assert data["target_text"] == "你好"
            assert isinstance(data["score"], int)
            assert 0 <= data["score"] <= 100
        else:
            assert "detail" in r.json()
            assert "Transcription failed" in r.json()["detail"]

    def test_without_target_chinese(self, auth_only_headers):
        files = {"file": ("a.m4a", _fake_audio_bytes(4096), "audio/m4a")}
        r = requests.post(f"{BASE_URL}/api/speaking/transcribe",
                          headers=auth_only_headers,
                          files=files,
                          timeout=60)
        # endpoint allows empty target (defaults to "")
        assert r.status_code in (200, 502)
        if r.status_code == 200:
            data = r.json()
            assert "transcribed_text" in data
            # No comparison fields when no target
            assert "score" not in data or data.get("target_text") in (None, "")
