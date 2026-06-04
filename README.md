# Mandarin Learning App

A focused mobile app for serious Mandarin learners built on the **New Practical Chinese Reader (NPCR)** curriculum. Designed to move students from passive recognition to active speaking and sentence construction.

---

## Features

- **NPCR Lessons 1–14** — Full dialogues (Part 1 & Part 2), vocabulary lists, and grammar notes for each lesson
- **Spaced Repetition Flashcards** — 6-stage SRS system (1d → 2d → 1w → 1m → 3m → 1y) with correct/incorrect progression
- **Reading / Writing / Speaking review modes** — Each due card can be reviewed by recall, handwriting, or pronunciation
- **Sentence Drills** — Substitution and transformation drills tied to each lesson
- **Speaking Practice** — Browse all dialogue sentences organized by lesson folder; tap to practice pronunciation (OpenAI Whisper transcription + syllable/tone pinyin scoring)
- **Handwriting Recognition** — Draw characters on a canvas; scored on-device via EasyOCR
- **Vocabulary Library & Custom Words** — Browse NPCR vocab, search, and add your own custom words to your deck
- **Progress Tracking** — Streak, retention rate, mastered word count, weak words
- **Home Dashboard** — Daily progress, due reviews, quick action tiles
- **JWT Auth** — Signup/login with bcrypt password hashing; 30-day sessions

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Expo (React Native) + Expo Router + TypeScript |
| Backend | FastAPI + Motor (async MongoDB driver) |
| Database | MongoDB |
| Auth | JWT (PyJWT) + bcrypt |
| Speech | OpenAI Whisper API (transcription) + pypinyin (tone scoring) |
| Handwriting | EasyOCR (on-device Chinese OCR) |
| Semantic matching | NLTK WordNet (English synonym checking) |

---

## Project Structure

```
Mandarin-Project/
├── backend/
│   ├── server.py          # FastAPI app — all routes and business logic
│   ├── seed_data.py       # NPCR lesson content (dialogues, vocab, drills)
│   ├── requirements.txt
│   ├── .env.example       # Template for backend env vars
│   └── .env               # Environment variables (not committed)
├── frontend/
│   ├── app/
│   │   ├── (auth)/              # Login / signup screens
│   │   ├── (tabs)/
│   │   │   ├── index.tsx        # Home dashboard
│   │   │   ├── lessons.tsx      # Lesson list
│   │   │   ├── review.tsx       # SRS review (reading/writing/speaking modes)
│   │   │   ├── speak.tsx        # Speaking practice (lesson folders)
│   │   │   └── profile.tsx      # Profile & settings
│   │   ├── lesson/[id].tsx      # Lesson detail (dialogue, grammar, vocab)
│   │   ├── drill.tsx            # Sentence drill session
│   │   ├── speak-practice.tsx   # Single sentence practice screen
│   │   ├── library.tsx          # Vocabulary library
│   │   └── add-word.tsx         # Add custom word to deck
│   ├── src/
│   │   ├── api/client.ts        # Typed API client
│   │   ├── components/          # Shared UI components (HandwritingCanvas)
│   │   ├── contexts/            # Auth context
│   │   ├── hooks/               # Custom hooks
│   │   ├── utils/storage/       # Cross-platform secure storage
│   │   └── theme.ts             # Colors, spacing, typography
│   ├── .env.example
│   └── package.json
└── mongo_dump/                  # Local MongoDB backup (git-ignored, not committed)
```

---

## Prerequisites

- **Python 3.11+**
- **Node.js 18+** and **Yarn**
- **MongoDB** running locally on port 27017
- **Expo Go** app on your phone (or an Android/iOS simulator)

---

## Setup

### 1. Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env         # or create manually (see Environment Variables below)
```

### 2. Frontend

```bash
cd frontend
yarn install
```

---

## Environment Variables

### `backend/.env`

```env
MONGO_URL="mongodb://localhost:27017"
DB_NAME="mandarin_app"
JWT_SECRET_KEY="your-secret-key-here"
JWT_ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=43200
OPENAI_API_KEY="sk-your-openai-key-here"
```

### `frontend/.env`

```env
EXPO_PUBLIC_BACKEND_URL=http://YOUR_LOCAL_IP:8000
```

> Use your machine's local network IP (e.g. `192.168.1.x`), not `localhost`, so the phone can reach the backend over Wi-Fi.

---

## Running the App

### Start the backend

```bash
cd backend
venv\Scripts\activate
uvicorn server:app --reload
```

The API will be available at `http://localhost:8000`. The server automatically seeds all 14 NPCR lessons on first run.

### Start the frontend

```bash
cd frontend
yarn start
```

Scan the QR code with Expo Go on your phone.

---

## Database

MongoDB database name: `mandarin_app`

| Collection | Contents |
|---|---|
| `lessons` | NPCR lesson content (dialogue, grammar, vocab metadata) |
| `vocabulary` | Individual vocabulary entries per lesson |
| `drills` | Sentence drills with substitution/transformation patterns |
| `users` | User accounts (hashed passwords, settings) |
| `flashcards` | Per-user SRS card state (stage, next review date) |
| `review_history` | Log of every flashcard review |
| `user_deck` | Mapping of user → vocabulary words added to deck |
| `drill_attempts` | Log of drill session results |
| `speaking_attempts` | Log of speaking practice results |

### Re-seeding

The server skips seeding if 14 lessons already exist. To force a reseed (e.g. after updating `seed_data.py`):

```bash
mongosh mandarin_app --eval "db.lessons.deleteMany({}); db.vocabulary.deleteMany({}); db.drills.deleteMany({})"
```

Then restart the server. User data (flashcards, accounts, history) is unaffected.

### Restore from backup

```bash
mongorestore --db mandarin_app mongo_dump/mandarin_app/
```

---

## API Overview

All routes are prefixed with `/api` and require a `Bearer` token except auth endpoints.

| Method | Route | Description |
|---|---|---|
| POST | `/api/auth/signup` | Create account |
| POST | `/api/auth/login` | Login, returns JWT |
| GET / PUT | `/api/auth/me` | Get / update current user settings |
| GET | `/api/lessons` | List all lessons with progress |
| GET | `/api/lessons/{id}` | Lesson detail with full vocabulary |
| GET | `/api/flashcards/due` | Cards due for review today |
| GET | `/api/flashcards/new` | New (unreviewed) cards from the deck |
| GET | `/api/flashcards/schedule` | Upcoming review counts per day |
| POST | `/api/flashcards/review` | Submit a review result (reading/writing/speaking) |
| GET | `/api/drills` | List drills (filterable by lesson/part) |
| POST | `/api/drills/attempt` | Submit a drill answer |
| GET / POST / DELETE | `/api/deck` | List / add / remove deck words |
| GET | `/api/vocabulary/library` | Browse + search NPCR and custom vocab |
| POST / DELETE | `/api/vocabulary/custom` | Create / delete custom vocabulary |
| POST | `/api/vocabulary/semantic-match` | English synonym match (WordNet) |
| POST | `/api/speaking/transcribe` | Transcribe audio (Whisper) + pronunciation score |
| POST | `/api/writing/recognize` | Score handwritten characters (EasyOCR) |
| GET | `/api/progress/dashboard` | Daily dashboard counts |
| GET | `/api/progress/stats` | User stats (streak, retention, weak words) |

---

## Design Philosophy

Calm, focused, and educational. No gamification overload. The palette uses organic/earthy tones — primary green `#4A7C59`, off-white background `#FDFCF9` — with large, readable hanzi throughout.
