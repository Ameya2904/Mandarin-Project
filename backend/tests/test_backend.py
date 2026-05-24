"""Backend API tests for Mandarin Learning App."""
import pytest
import requests
import uuid
import os
from datetime import datetime

BASE_URL = os.environ.get('EXPO_PUBLIC_BACKEND_URL', 'https://mandarin-speak-2.preview.emergentagent.com').rstrip('/')


# ---------- Health ----------
class TestHealth:
    def test_root(self, api):
        r = api.get(f"{BASE_URL}/api/")
        assert r.status_code == 200
        assert "Mandarin" in r.json().get("message", "")


# ---------- Auth ----------
class TestAuth:
    def test_signup_creates_user(self, api):
        email = f"TEST_{uuid.uuid4().hex[:8]}@example.com"
        r = api.post(f"{BASE_URL}/api/auth/signup",
                     json={"email": email, "password": "password123", "name": "Newby"})
        assert r.status_code == 200, r.text
        data = r.json()
        assert "access_token" in data
        assert data["user"]["email"] == email.lower()
        assert data["user"]["daily_goal"] == 20

    def test_signup_duplicate_email(self, api, auth_token):
        # auth_token uses test@test.com
        r = api.post(f"{BASE_URL}/api/auth/signup",
                     json={"email": "test@test.com", "password": "password123", "name": "Dup"})
        assert r.status_code == 400

    def test_login_valid(self, api):
        r = api.post(f"{BASE_URL}/api/auth/login",
                     json={"email": "test@test.com", "password": "password123"})
        assert r.status_code == 200
        assert "access_token" in r.json()

    def test_login_invalid_password(self, api):
        r = api.post(f"{BASE_URL}/api/auth/login",
                     json={"email": "test@test.com", "password": "wrongpass"})
        assert r.status_code == 401

    def test_me_requires_auth(self, api):
        r = api.get(f"{BASE_URL}/api/auth/me")
        assert r.status_code in (401, 403)

    def test_me_with_token(self, api, auth_headers):
        r = api.get(f"{BASE_URL}/api/auth/me", headers=auth_headers)
        assert r.status_code == 200
        assert "email" in r.json()

    def test_update_daily_goal(self, api, auth_headers):
        r = api.put(f"{BASE_URL}/api/auth/me", headers=auth_headers, json={"daily_goal": 25})
        assert r.status_code == 200
        assert r.json()["daily_goal"] == 25
        # verify via GET
        r2 = api.get(f"{BASE_URL}/api/auth/me", headers=auth_headers)
        assert r2.json()["daily_goal"] == 25


# ---------- Lessons ----------
class TestLessons:
    def test_list_lessons(self, api, auth_headers):
        r = api.get(f"{BASE_URL}/api/lessons", headers=auth_headers)
        assert r.status_code == 200
        lessons = r.json()
        assert len(lessons) == 20, f"Expected 20 lessons, got {len(lessons)}"
        assert all("progress" in lesson for lesson in lessons)
        assert all("vocabulary_count" in lesson for lesson in lessons)
        assert all(lesson["vocabulary_count"] > 0 for lesson in lessons)
        assert all("dialogue" in lesson and len(lesson["dialogue"]) > 0 for lesson in lessons)
        assert all("grammar_notes" in lesson and len(lesson["grammar_notes"]) > 0 for lesson in lessons)
        numbers = [l["lesson_number"] for l in lessons]
        assert numbers == list(range(1, 21))
        titles = [l["title"] for l in lessons]
        assert len(set(titles)) == 20  # unique titles
        # Verify lesson 6 and 20 by title
        l6 = next(l for l in lessons if l["lesson_number"] == 6)
        assert "游泳" in l6["title"]
        l20 = next(l for l in lessons if l["lesson_number"] == 20)
        assert "中国" in l20["title"]

    def test_get_lesson_detail(self, api, auth_headers):
        r = api.get(f"{BASE_URL}/api/lessons", headers=auth_headers)
        lesson_id = r.json()[0]["id"]
        r2 = api.get(f"{BASE_URL}/api/lessons/{lesson_id}", headers=auth_headers)
        assert r2.status_code == 200
        lesson = r2.json()
        assert "vocabulary" in lesson
        assert len(lesson["vocabulary"]) > 0
        assert "dialogue" in lesson
        assert "grammar_notes" in lesson

    def test_get_lesson_not_found(self, api, auth_headers):
        r = api.get(f"{BASE_URL}/api/lessons/nonexistent-id", headers=auth_headers)
        assert r.status_code == 404


# ---------- Flashcards / SRS ----------
def _seed_deck(api, fresh_user, n=5):
    """Helper: add the first `n` NPCR vocab to the user's deck so /flashcards/new returns items."""
    h = fresh_user["headers"]
    lib = api.get(f"{BASE_URL}/api/vocabulary/library?source=npcr&limit={n}", headers=h).json()
    vids = [v["id"] for v in lib[:n]]
    api.post(f"{BASE_URL}/api/deck/add", headers=h, json={"vocabulary_ids": vids})
    return vids


class TestFlashcardsSRS:
    def test_new_flashcards(self, api, fresh_user):
        _seed_deck(api, fresh_user, 5)
        r = api.get(f"{BASE_URL}/api/flashcards/new?limit=5", headers=fresh_user["headers"])
        assert r.status_code == 200
        cards = r.json()
        assert len(cards) > 0
        assert "simplified" in cards[0]
        assert "pinyin" in cards[0]

    def test_srs_correct_advances_stage(self, api, fresh_user):
        _seed_deck(api, fresh_user, 5)
        # get a new vocab
        r = api.get(f"{BASE_URL}/api/flashcards/new?limit=1", headers=fresh_user["headers"])
        vocab = r.json()[0]
        vocab_id = vocab["id"]

        # First correct review: stage should become 2 (new card +1 = 2)
        r1 = api.post(f"{BASE_URL}/api/flashcards/review", headers=fresh_user["headers"],
                      json={"vocabulary_id": vocab_id, "was_correct": True})
        assert r1.status_code == 200
        assert r1.json()["new_stage"] == 2

        # Second correct review: stage 2 -> 3
        r2 = api.post(f"{BASE_URL}/api/flashcards/review", headers=fresh_user["headers"],
                      json={"vocabulary_id": vocab_id, "was_correct": True})
        assert r2.json()["new_stage"] == 3

    def test_srs_incorrect_resets_to_stage_1(self, api, fresh_user):
        _seed_deck(api, fresh_user, 5)
        r = api.get(f"{BASE_URL}/api/flashcards/new?limit=2", headers=fresh_user["headers"])
        vocab = r.json()[1]  # different word
        vocab_id = vocab["id"]

        # advance to stage 3
        api.post(f"{BASE_URL}/api/flashcards/review", headers=fresh_user["headers"],
                 json={"vocabulary_id": vocab_id, "was_correct": True})
        api.post(f"{BASE_URL}/api/flashcards/review", headers=fresh_user["headers"],
                 json={"vocabulary_id": vocab_id, "was_correct": True})

        # incorrect: reset to stage 1
        r_wrong = api.post(f"{BASE_URL}/api/flashcards/review", headers=fresh_user["headers"],
                           json={"vocabulary_id": vocab_id, "was_correct": False})
        assert r_wrong.status_code == 200
        assert r_wrong.json()["new_stage"] == 1

    def test_due_flashcards(self, api, fresh_user):
        # due should be 0 right after creating cards (next_review is future)
        r = api.get(f"{BASE_URL}/api/flashcards/due", headers=fresh_user["headers"])
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_review_unknown_vocab(self, api, fresh_user):
        r = api.post(f"{BASE_URL}/api/flashcards/review", headers=fresh_user["headers"],
                     json={"vocabulary_id": "nonexistent", "was_correct": True})
        assert r.status_code == 404


# ---------- Drills ----------
class TestDrills:
    def test_list_drills(self, api, auth_headers):
        r = api.get(f"{BASE_URL}/api/drills?limit=100", headers=auth_headers)
        assert r.status_code == 200
        drills = r.json()
        assert len(drills) >= 29, f"Expected >=29 drills, got {len(drills)}"
        assert "prompt_chinese" in drills[0]
        # Coverage of lessons 1-20
        lesson_nums = {d["lesson_number"] for d in drills}
        for n in range(1, 21):
            assert n in lesson_nums, f"No drill for lesson {n}"

    def test_filter_drills_by_lesson(self, api, auth_headers):
        r = api.get(f"{BASE_URL}/api/drills?lesson_number=15", headers=auth_headers)
        assert r.status_code == 200
        drills = r.json()
        assert len(drills) > 0
        assert all(d["lesson_number"] == 15 for d in drills)

    def test_drill_attempt(self, api, auth_headers):
        r = api.get(f"{BASE_URL}/api/drills?limit=1", headers=auth_headers)
        drill = r.json()[0]
        r2 = api.post(f"{BASE_URL}/api/drills/attempt", headers=auth_headers,
                      json={"drill_id": drill["id"], "user_answer": "我不忙", "was_correct": True})
        assert r2.status_code == 200
        assert r2.json()["success"] is True


# ---------- Speaking ----------
class TestSpeaking:
    def test_perfect_match(self, api, auth_headers):
        r = api.post(f"{BASE_URL}/api/speaking/evaluate", headers=auth_headers,
                     json={"target_chinese": "你好", "spoken_text": "你好"})
        assert r.status_code == 200
        data = r.json()
        assert data["correct"] is True
        assert data["score"] == 100

    def test_partial_match(self, api, auth_headers):
        r = api.post(f"{BASE_URL}/api/speaking/evaluate", headers=auth_headers,
                     json={"target_chinese": "你好吗", "spoken_text": "你好"})
        data = r.json()
        assert data["score"] > 0 and data["score"] < 100
        assert data["correct"] is False

    def test_empty_speech(self, api, auth_headers):
        r = api.post(f"{BASE_URL}/api/speaking/evaluate", headers=auth_headers,
                     json={"target_chinese": "你好", "spoken_text": ""})
        data = r.json()
        assert data["score"] == 0


# ---------- Progress ----------
class TestProgress:
    def test_dashboard(self, api, auth_headers):
        r = api.get(f"{BASE_URL}/api/progress/dashboard", headers=auth_headers)
        assert r.status_code == 200
        d = r.json()
        for key in ["due_count", "new_count", "mastered_count", "streak_count",
                    "daily_goal", "reviews_today", "progress_percent"]:
            assert key in d

    def test_stats(self, api, auth_headers):
        r = api.get(f"{BASE_URL}/api/progress/stats", headers=auth_headers)
        assert r.status_code == 200
        s = r.json()
        for key in ["total_reviews", "retention_rate", "weak_words", "mastered_count"]:
            assert key in s
        assert isinstance(s["weak_words"], list)
