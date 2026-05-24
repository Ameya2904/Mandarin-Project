"""Backend tests for iteration 3:
- Deck system (list/add/remove)
- Custom vocabulary CRUD (auto-add to deck, ownership)
- Vocabulary library with filters (source, lesson_number, q) and annotations (in_deck, is_custom)
- Flashcards /new endpoint deck-gating
- Lesson detail in_deck annotation
- Flashcard review.mode field stored in review_history
- Writing recognition endpoint shape + validation + auth gating
- Legacy deck migration on startup
"""
import os
import uuid
import base64
import pytest
import requests

BASE_URL = os.environ.get('EXPO_PUBLIC_BACKEND_URL', 'https://mandarin-speak-2.preview.emergentagent.com').rstrip('/')


@pytest.fixture(scope="module")
def fresh_user():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    email = f"TEST_{uuid.uuid4().hex[:8]}@example.com"
    r = s.post(f"{BASE_URL}/api/auth/signup",
               json={"email": email, "password": "password123", "name": "DeckTester"})
    assert r.status_code == 200, r.text
    data = r.json()
    return {
        "session": s,
        "user": data["user"],
        "token": data["access_token"],
        "headers": {"Authorization": f"Bearer {data['access_token']}",
                    "Content-Type": "application/json"},
        "email": email,
    }


# ---------- Deck ----------
class TestDeck:
    def test_fresh_user_deck_empty(self, fresh_user):
        r = fresh_user["session"].get(f"{BASE_URL}/api/deck", headers=fresh_user["headers"])
        assert r.status_code == 200
        assert r.json() == []

    def test_fresh_user_new_flashcards_empty(self, fresh_user):
        """flashcards/new should be empty when deck is empty (deck-gated)."""
        r = fresh_user["session"].get(f"{BASE_URL}/api/flashcards/new?limit=10",
                                       headers=fresh_user["headers"])
        assert r.status_code == 200
        assert r.json() == []

    def test_add_vocab_to_deck(self, fresh_user):
        s = fresh_user["session"]; h = fresh_user["headers"]
        # Pick a few NPCR vocab ids
        r = s.get(f"{BASE_URL}/api/vocabulary/library?source=npcr&limit=5", headers=h)
        assert r.status_code == 200
        lib = r.json()
        assert len(lib) >= 3
        vocab_ids = [v["id"] for v in lib[:3]]
        # All should NOT be in deck yet
        assert all(v["in_deck"] is False for v in lib[:3])

        # Add them
        r2 = s.post(f"{BASE_URL}/api/deck/add", headers=h,
                    json={"vocabulary_ids": vocab_ids})
        assert r2.status_code == 200
        assert r2.json()["added"] == 3

        # Duplicate add => added=0
        r3 = s.post(f"{BASE_URL}/api/deck/add", headers=h,
                    json={"vocabulary_ids": vocab_ids})
        assert r3.status_code == 200
        assert r3.json()["added"] == 0

        # Deck now has 3 entries with enriched vocabulary
        r4 = s.get(f"{BASE_URL}/api/deck", headers=h)
        deck = r4.json()
        assert len(deck) == 3
        assert all("vocabulary" in d and d["vocabulary"]["id"] in vocab_ids for d in deck)
        # No flashcards yet → current_stage None
        assert all(d.get("current_stage") is None for d in deck)

        # And library should now annotate in_deck=True for these
        r5 = s.get(f"{BASE_URL}/api/vocabulary/library?source=npcr&limit=5", headers=h)
        lib2 = r5.json()
        in_deck_ids = {v["id"] for v in lib2 if v["in_deck"]}
        assert set(vocab_ids).issubset(in_deck_ids)

    def test_flashcards_new_returns_deck_vocab(self, fresh_user):
        """After deck has items but no flashcards, /flashcards/new returns those vocab."""
        r = fresh_user["session"].get(f"{BASE_URL}/api/flashcards/new?limit=10",
                                       headers=fresh_user["headers"])
        assert r.status_code == 200
        cards = r.json()
        assert len(cards) == 3  # 3 added in previous test
        assert all("simplified" in c for c in cards)

    def test_review_with_mode_stores_in_history(self, fresh_user):
        s = fresh_user["session"]; h = fresh_user["headers"]
        cards = s.get(f"{BASE_URL}/api/flashcards/new?limit=1", headers=h).json()
        assert cards, "no new cards"
        vid = cards[0]["id"]
        # Review with mode=writing
        r = s.post(f"{BASE_URL}/api/flashcards/review", headers=h,
                   json={"vocabulary_id": vid, "was_correct": True, "mode": "writing"})
        assert r.status_code == 200
        assert r.json()["new_stage"] == 2
        # Once vocab has a flashcard, /flashcards/new should exclude it
        new_cards = s.get(f"{BASE_URL}/api/flashcards/new?limit=10", headers=h).json()
        assert vid not in [c["id"] for c in new_cards]

    def test_delete_from_deck_removes_flashcard(self, fresh_user):
        s = fresh_user["session"]; h = fresh_user["headers"]
        deck = s.get(f"{BASE_URL}/api/deck", headers=h).json()
        # find the one that has a flashcard (current_stage not None)
        with_card = [d for d in deck if d.get("current_stage") is not None]
        assert with_card, "expected at least one deck entry with a flashcard"
        vid = with_card[0]["vocabulary_id"]
        r = s.delete(f"{BASE_URL}/api/deck/{vid}", headers=h)
        assert r.status_code == 200
        assert r.json()["removed"] is True
        # Verify deck doesn't contain it
        deck2 = s.get(f"{BASE_URL}/api/deck", headers=h).json()
        assert vid not in [d["vocabulary_id"] for d in deck2]
        # And no flashcard remains for it
        # (indirectly: /flashcards/due cannot include it; just check via review eligibility)
        # Add back; if flashcard existed, the SRS state would still be there. We expect fresh.
        s.post(f"{BASE_URL}/api/deck/add", headers=h, json={"vocabulary_ids": [vid]})
        new = s.get(f"{BASE_URL}/api/flashcards/new?limit=10", headers=h).json()
        # Should reappear in /new since flashcard was deleted
        assert vid in [c["id"] for c in new]


# ---------- Custom Vocabulary ----------
class TestCustomVocab:
    def test_create_custom_auto_adds_to_deck(self, fresh_user):
        s = fresh_user["session"]; h = fresh_user["headers"]
        payload = {
            "simplified": "测试词",
            "pinyin": "cèshì cí",
            "english": "TEST_word",
            "example_chinese": "这是测试词",
        }
        r = s.post(f"{BASE_URL}/api/vocabulary/custom", headers=h, json=payload)
        assert r.status_code == 200, r.text
        vocab = r.json()
        assert vocab["created_by"] == fresh_user["user"]["id"]
        assert vocab["simplified"] == "测试词"
        assert vocab.get("lesson_number") is None
        vid = vocab["id"]
        # Verify auto-added to deck
        deck = s.get(f"{BASE_URL}/api/deck", headers=h).json()
        assert vid in [d["vocabulary_id"] for d in deck]

        # Library with source=custom returns it
        r2 = s.get(f"{BASE_URL}/api/vocabulary/library?source=custom", headers=h)
        items = r2.json()
        match = [v for v in items if v["id"] == vid]
        assert match and match[0]["is_custom"] is True and match[0]["in_deck"] is True

        # Library with source=npcr should NOT include it
        r3 = s.get(f"{BASE_URL}/api/vocabulary/library?source=npcr&limit=300", headers=h)
        assert vid not in [v["id"] for v in r3.json()]

    def test_search_filter(self, fresh_user):
        s = fresh_user["session"]; h = fresh_user["headers"]
        r = s.get(f"{BASE_URL}/api/vocabulary/library?q=TEST_word", headers=h)
        assert r.status_code == 200
        items = r.json()
        assert any(v["english"] == "TEST_word" for v in items)

    def test_lesson_number_filter(self, fresh_user):
        s = fresh_user["session"]; h = fresh_user["headers"]
        r = s.get(f"{BASE_URL}/api/vocabulary/library?lesson_number=1", headers=h)
        assert r.status_code == 200
        items = r.json()
        assert items, "expected lesson 1 vocab"
        assert all(v.get("lesson_number") == 1 for v in items)

    def test_delete_custom_only_by_owner(self, fresh_user):
        s = fresh_user["session"]; h = fresh_user["headers"]
        # Find the custom vocab
        items = s.get(f"{BASE_URL}/api/vocabulary/library?source=custom", headers=h).json()
        target = next((v for v in items if v["english"] == "TEST_word"), None)
        assert target is not None
        vid = target["id"]

        # Create a different user and try to delete -> 403
        other_email = f"TEST_{uuid.uuid4().hex[:8]}@example.com"
        other = requests.post(f"{BASE_URL}/api/auth/signup",
                              json={"email": other_email, "password": "password123", "name": "Other"}).json()
        other_h = {"Authorization": f"Bearer {other['access_token']}", "Content-Type": "application/json"}
        r_forbid = requests.delete(f"{BASE_URL}/api/vocabulary/custom/{vid}", headers=other_h)
        assert r_forbid.status_code == 403

        # Owner deletes successfully
        r = s.delete(f"{BASE_URL}/api/vocabulary/custom/{vid}", headers=h)
        assert r.status_code == 200
        assert r.json()["deleted"] is True

        # Cleanup verified: not in deck, not in library
        deck = s.get(f"{BASE_URL}/api/deck", headers=h).json()
        assert vid not in [d["vocabulary_id"] for d in deck]
        lib = s.get(f"{BASE_URL}/api/vocabulary/library?source=custom", headers=h).json()
        assert vid not in [v["id"] for v in lib]

    def test_delete_nonexistent_custom(self, fresh_user):
        r = fresh_user["session"].delete(f"{BASE_URL}/api/vocabulary/custom/nonexistent-id",
                                          headers=fresh_user["headers"])
        assert r.status_code == 404


# ---------- Lesson in_deck annotation ----------
class TestLessonInDeck:
    def test_lesson_vocab_has_in_deck_field(self, fresh_user):
        s = fresh_user["session"]; h = fresh_user["headers"]
        lessons = s.get(f"{BASE_URL}/api/lessons", headers=h).json()
        l1 = next(l for l in lessons if l["lesson_number"] == 1)
        detail = s.get(f"{BASE_URL}/api/lessons/{l1['id']}", headers=h).json()
        vocab = detail["vocabulary"]
        assert vocab, "lesson 1 should have vocab"
        assert all("in_deck" in v for v in vocab)
        # Pick one that isn't yet in deck and add
        not_in_deck = [v for v in vocab if not v["in_deck"]]
        assert not_in_deck
        target = not_in_deck[0]
        s.post(f"{BASE_URL}/api/deck/add", headers=h,
               json={"vocabulary_ids": [target["id"]]})
        detail2 = s.get(f"{BASE_URL}/api/lessons/{l1['id']}", headers=h).json()
        match = next(v for v in detail2["vocabulary"] if v["id"] == target["id"])
        assert match["in_deck"] is True


# ---------- Writing Recognition ----------
# A tiny 1x1 transparent PNG (valid PNG bytes, base64 over 100 chars)
TINY_PNG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGP8//8/AwAI/AL+8gKWqQAAAABJRU5ErkJggg=="
)
# Pad to >100 chars by repeating (still a valid-looking b64 string for length validation)
LARGE_FAKE_B64 = TINY_PNG_B64 + "A" * 200


class TestWritingRecognition:
    def test_requires_auth(self):
        r = requests.post(f"{BASE_URL}/api/writing/recognize",
                          json={"image_base64": LARGE_FAKE_B64, "target_chinese": "你好"})
        assert r.status_code in (401, 403)

    def test_empty_image_400(self, fresh_user):
        r = fresh_user["session"].post(f"{BASE_URL}/api/writing/recognize",
                                        headers=fresh_user["headers"],
                                        json={"image_base64": "", "target_chinese": "你好"})
        assert r.status_code == 400

    def test_tiny_image_400(self, fresh_user):
        r = fresh_user["session"].post(f"{BASE_URL}/api/writing/recognize",
                                        headers=fresh_user["headers"],
                                        json={"image_base64": "abc", "target_chinese": "你好"})
        assert r.status_code == 400

    def test_data_url_prefix_stripped_and_endpoint_shape(self, fresh_user):
        """Even with a real-looking image, GPT-4o-mini may return empty/garbage on random bytes.
        We accept 200 (proper shape) OR 502 (vision call failed gracefully)."""
        data_url = f"data:image/png;base64,{LARGE_FAKE_B64}"
        r = fresh_user["session"].post(f"{BASE_URL}/api/writing/recognize",
                                        headers=fresh_user["headers"],
                                        json={"image_base64": data_url, "target_chinese": "你好"})
        assert r.status_code in (200, 502), f"Unexpected {r.status_code}: {r.text[:200]}"
        if r.status_code == 200:
            data = r.json()
            for k in ("correct", "score", "feedback", "recognized_text", "target_text"):
                assert k in data, f"missing key {k}"
            assert data["target_text"] == "你好"
            assert isinstance(data["correct"], bool)
            assert isinstance(data["score"], int)


# ---------- Legacy migration ----------
class TestLegacyMigration:
    def test_test_user_deck_matches_flashcards(self):
        """If test@test.com has flashcards, their deck must contain matching entries."""
        s = requests.Session()
        s.headers.update({"Content-Type": "application/json"})
        login = s.post(f"{BASE_URL}/api/auth/login",
                       json={"email": "test@test.com", "password": "password123"})
        if login.status_code != 200:
            pytest.skip("test@test.com not available")
        token = login.json()["access_token"]
        h = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        deck = s.get(f"{BASE_URL}/api/deck", headers=h).json()
        # Pull current flashcards via /due (limit large) + /new — easier: check progress/dashboard
        dash = s.get(f"{BASE_URL}/api/progress/dashboard", headers=h).json()
        total_cards = dash["total_cards"]
        # Every flashcard must have a corresponding deck entry (deck size >= total_cards)
        assert len(deck) >= total_cards, (
            f"Legacy migration incomplete: deck={len(deck)} but total_cards={total_cards}"
        )
