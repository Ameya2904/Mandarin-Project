# SpacedChinese — MongoDB Data Export

This folder contains a snapshot of the development MongoDB database taken on 2026-05-24.

## Contents

### `mandarin_app/` — BSON dump (for `mongorestore`)
Native MongoDB binary format. Includes metadata + indexes.

### `mandarin_app_json/` — JSON exports (human readable)
Each collection exported as a JSON array via `mongoexport`.

| Collection            | Docs | Description |
| --------------------- | ---: | ----------- |
| `users`               | 19   | User accounts (bcrypt-hashed passwords) |
| `lessons`             | 20   | NPCR Book 1+2 lessons with dialogue, grammar, vocab IDs |
| `vocabulary`          | 150  | NPCR vocabulary items + any user-created custom words |
| `flashcards`          | 10   | Per-user SRS state (stage, next_review_at, counts) |
| `review_history`      | 25   | Every flashcard review event (with `mode` field) |
| `user_deck`           | 26   | Which vocabulary IDs each user has added to their deck |
| `drills`              | 29   | Substitution/transformation drills for lessons 1–20 |
| `drill_attempts`      | 5    | User drill submissions |
| `speaking_attempts`   | 11   | Whisper transcription attempts with target & score |

## Restore on a fresh machine

```bash
# BSON restore (preserves indexes)
mongorestore --uri="mongodb://localhost:27017" \
             --db=mandarin_app \
             mongo_dump/mandarin_app/

# OR — per-collection JSON import
mongoimport --uri="mongodb://localhost:27017/mandarin_app" \
            --collection=lessons --jsonArray --drop \
            --file=mongo_dump/mandarin_app_json/lessons.json
```

## Notes

- `users` collection contains real bcrypt hashes — rotate `JWT_SECRET_KEY` in your new `.env` so any existing tokens are invalidated.
- `writing_attempts` collection is not included here (empty in this snapshot — feature ships in the latest backend revision).
- If you only want NPCR seed data (no user data), the backend will auto-seed `lessons`, `vocabulary` and `drills` on first startup from `backend/seed_data.py`. You can skip the restore in that case.
