# Mandarin Learning App — Complete Codebase Guide

This document is a full walkthrough of the codebase. It is organized into three parts:

1. **Architecture Overview** — what the app is, the tech stack, and a description of every script and what it does.
2. **Method-by-Method Reference** — an exhaustive, function-level breakdown of every method: its signature, what it receives, every meaningful step, the edge cases it handles, and what it returns.
3. **How Everything Connects** — the data flows and seams that wire the frontend and backend together, including end-to-end traces.

---
---

# PART 1 — ARCHITECTURE OVERVIEW

This is a full-stack mobile language-learning app for studying Mandarin from the **New Practical Chinese Reader (NPCR)** textbook (Lessons 1–14). It has two halves:

- **`backend/`** — a Python **FastAPI** server backed by **MongoDB**, with local AI for speech recognition (FunASR) and handwriting OCR (EasyOCR).
- **`frontend/`** — an **Expo / React Native** app (TypeScript) using **Expo Router** for navigation.

The pedagogical core is **spaced repetition** (SRS): you add words to a personal deck, and the app schedules them for review at growing intervals, testing you three ways — reading, handwriting, and pronunciation.

## Backend (`backend/app/`)

### `config.py` — Environment & constants
Loads `backend/.env` via `python-dotenv`, then exposes module-level constants:
- `MONGO_URL`, `DB_NAME` — database connection (required; crashes loudly if missing).
- `JWT_SECRET`, `JWT_ALGO`, `ACCESS_TOKEN_EXPIRE_MINUTES` — auth config (token lifetime defaults to 43200 min = 30 days).
- `ASR_MODEL`, `ASR_HUB`, `ASR_DEVICE`, `ASR_LANGUAGE` — speech-to-text settings for FunASR.
- `SRS_INTERVALS = {1:1, 2:2, 3:7, 4:30, 5:90, 6:365}` — the heart of the SRS: stage number → days until next review (1 day, 2 days, 1 week, 1 month, 3 months, 1 year).

### `main.py` — Application entry point
- Configures logging and creates the `FastAPI` app.
- Builds an `APIRouter` with prefix `/api`, defines a `root()` health-check at `/api/`, then loops over all nine router modules and includes each into the API router.
- Adds permissive CORS (all origins/methods/headers) so the phone app can reach it.
- **`on_startup()`** — runs `create_indexes()`, `seed_lessons_and_vocab()`, `migrate_legacy_decks()`, and `asr.warm_up()` (preloads the speech model so the first user request isn't slow).
- **`on_shutdown()`** — closes the Mongo client.

### `db.py` — Database connection, indexing, seeding
Creates the async Mongo client (`AsyncIOMotorClient`) and the `db` handle. Three functions:
- **`create_indexes()`** — unique index on user email; unique compound index on `(user_id, vocabulary_id)` for flashcards and deck entries (prevents duplicates); an index on `next_review_at` for fast "due cards" queries; and an index on `created_by` for custom vocab.
- **`seed_lessons_and_vocab()`** — populates lessons/vocab/drills from `seed_data.py`. It's idempotent: if the lesson count already matches, it skips. If the count *changed* (e.g. you edited the seed file), it deletes and reseeds only the content collections, **preserving user data**. For each lesson it inserts vocab docs (each with a UUID), then the lesson doc holding the list of vocab IDs.
- **`migrate_legacy_decks()`** — a one-time backfill. Older versions had flashcards without explicit deck entries; this aggregates each user's flashcards and creates the missing `user_deck` rows.

### `models.py` — Pydantic request/response schemas
Validation models for the API: `UserCreate` (enforces 6-char password), `UserLogin`, `UserPublic` (the safe user shape returned to clients — no password), `TokenResponse`, `CustomVocabCreate`, `DeckAddRequest`, `WritingRecognizeRequest`, `FlashcardReviewRequest` (carries `mode` and a `skip_srs` flag), `DrillAttemptRequest`, `SemanticMatchRequest`, `UserSettingsUpdate`, and the password-reset trio (`ForgotPasswordRequest/Response`, `ResetPasswordRequest`, `ChangePasswordRequest`). The forgot-password response deliberately returns the reset token in the body because there's no email service.

### `auth.py` — Authentication helpers
- **`hash_password` / `verify_password`** — bcrypt hashing and a safe verify that returns `False` on any error.
- **`create_access_token(user_id)`** — signs a JWT with `sub` = user id and an expiry.
- **`get_current_user(creds)`** — the FastAPI dependency injected into every protected route. Decodes/validates the bearer token, looks up the user (excluding `_id` and `hashed_password`), and raises 401 on any failure.
- **`user_to_public(doc)`** — maps a raw Mongo user doc into the `UserPublic` model.

### `scoring.py` — Chinese normalization & pronunciation scoring
The pinyin-based pronunciation grader used by speaking practice:
- **`normalize_chinese`** — strips whitespace/punctuation for comparison.
- **`pinyin_syllables`** — converts hanzi to tone-numbered pinyin (`你好` → `['ni3','hao3']`).
- **`_strip_tone`** — drops the trailing tone digit (`hao3` → `hao`).
- **`pinyin_display`** — pretty pinyin with tone marks for showing the learner.
- **`score_pronunciation(target, spoken)`** — the key algorithm. It's an **order-independent multiset match**: Pass 1 awards full credit for syllables matching in both sound *and* tone; Pass 2 awards half credit where the base sound matches but the tone is wrong. This means a single dropped/swapped syllable doesn't cascade into everything after it being marked wrong. Returns score %, a `correct` boolean, and counts.
- **`pronunciation_feedback(p)`** — turns the score dict into a human sentence ("All the syllables right, but check your tones", etc.).

### `semantic.py` — English synonym matching (WordNet)
Used so reading answers like "happy" can match a target of "glad". On import it ensures NLTK's WordNet corpus is downloaded.
- **`normalize_en`** — lowercases, trims trailing punctuation, strips leading articles ("to/a/an/the").
- **`_word_synonyms`** — collects all WordNet lemma synonyms for a word.
- **`words_match`** — equal, or each appears in the other's synonym set.
- **`answer_matches_target`** — splits the target on `;`, `,`, `/`, or "or" and returns true if the answer matches any part.

### `asr.py` — Local speech-to-text (FunASR)
Wraps the FunASR `Fun-ASR-Nano` model with lazy loading and thread-safety:
- **`_get_model`** — double-checked-locking singleton load (model isn't cheap; `trust_remote_code=True` because the model ships custom code).
- **`warm_up`** — eager load at startup.
- **`_to_wav_16k`** — uses **ffmpeg** to convert any uploaded audio to 16 kHz mono WAV; raises clear errors if ffmpeg is missing or fails.
- **`transcribe(audio_path)`** — the blocking inference call (must be run in a threadpool by callers). Uses an `_infer_lock` to serialize calls (model isn't thread-safe) and sets `itn=False` so single Mandarin syllables come back as hanzi rather than being rewritten into homophonous English letters.

### `seed_data.py` — The NPCR curriculum (~1500 lines of data)
Holds `NPCR_LESSONS` (Lessons 1–14, each with dialogue split into Part 1/2, grammar notes, and a vocabulary list) and `SENTENCE_DRILLS`. The **`_expand_drill(...)`** helper turns one substitution-drill template plus a list of variants into many individual drill entries. Exports `NPCR_LESSONS` and `SENTENCE_DRILLS`.

### The routers (`backend/app/routers/`)

**`auth.py`**
- **`signup`** — rejects duplicate email, hashes password, creates the user with defaults (daily_goal 20, streak 0, level "Beginner"), returns a token.
- **`login`** — verifies credentials and **updates the streak**: same-day login keeps it, consecutive-day increments it, a gap resets it to 1.
- **`forgot_password`** — generates a UUID reset token with a 30-min expiry, stores it, and returns it directly (no mail service).
- **`reset_password`** — validates token + expiry (handling tz-naive timestamps), sets the new password, clears the token, returns a fresh login token.
- **`get_me`** — returns the current user.
- **`change_password`** — re-fetches the full doc (the dependency strips the hash), verifies the current password, updates it.
- **`update_me`** — patches name/daily_goal/learner_level (only non-null fields).

**`lessons.py`**
- **`list_lessons`** — all lessons sorted by number, each annotated with per-user progress (`mastered` = cards at stage ≥4, `started` = any card, `total`).
- **`get_lesson`** — one lesson plus its full vocab list, each word flagged `in_deck` for this user.

**`flashcards.py` — the SRS engine**
- **`get_due_flashcards`** — cards whose `next_review_at` ≤ now, joined with their vocab.
- **`get_new_flashcards`** — words in the user's deck that have no flashcard yet (i.e. never reviewed).
- **`get_review_schedule`** — counts upcoming due cards per day for the next N days (for the profile chart).
- **`submit_review`** — the core SRS state machine. If `skip_srs` is set it only logs history (used by the non-final review modes). Otherwise: an existing card moves up one stage on correct (capped at 6) or **resets to stage 1** on incorrect; a brand-new card starts at stage 2 (correct) or 1 (incorrect). It recomputes `next_review_at` from `SRS_INTERVALS`, updates correct/incorrect counts, and always logs to `review_history`.

**`drills.py`**
- **`list_drills`** — fetches drills (optionally filtered by lesson/part) and **repeats each one `REPEAT_PER_DRILL` (3) times** back-to-back so the learner drills a pattern before moving on.
- **`submit_drill_attempt`** — logs a drill attempt.

**`deck.py`**
- **`list_deck`** — the user's deck words joined with vocab and current SRS stage.
- **`add_to_deck`** — bulk-adds vocab IDs, skipping invalid or already-present ones.
- **`remove_from_deck`** — removes a word from the deck **and** deletes its flashcard.

**`vocabulary.py`**
- **`check_semantic_match`** — exposes `answer_matches_target` (WordNet).
- **`create_custom_vocab`** — creates a user-owned word (simplified copied to traditional) and **auto-adds it to the deck**.
- **`delete_custom_vocab`** — ownership-checked delete that cascades to deck + flashcards.
- **`vocabulary_library`** — the searchable library: filters by source (npcr/custom), lesson, and a regex `q` across simplified/pinyin/english; annotates each row with `in_deck` and `is_custom`.

**`speaking.py`**
- **`transcribe_audio`** — accepts an audio upload (size-validated 100 bytes–25 MB), writes it to a temp file, runs `asr.transcribe` in a threadpool, then if a `target_chinese` was supplied, normalizes both sides, scores with `score_pronunciation`, logs a `speaking_attempts` record, and returns score + feedback + target/spoken pinyin.

**`writing.py`**
- **`_get_ocr_reader`** — lazy singleton EasyOCR reader (Simplified Chinese, CPU).
- **`_ocr_score`** — bag-of-characters scoring: fraction of recognized chars present in the target, plus an exact-match flag.
- **`recognize_handwriting`** — decodes the base64 PNG (handling `data:` URLs), runs OCR in an executor, scores it, logs a `writing_attempts` record, and returns the result.

**`progress.py`**
- **`get_dashboard`** — home-screen counts: due today, total/mastered cards, reviews/correct today, "new" count (deck words with no flashcard), daily goal, streak, and a clamped progress %.
- **`get_stats`** — profile stats: retention rate, mastered/learning counts, top-10 "weak words" (incorrect > correct), and speaking-attempt count.

## Frontend (`frontend/`)

### Core infrastructure (`src/`)

**`api/client.ts`** — The single typed gateway to the backend. Exports TS types (`Vocabulary`, `Flashcard`, `Lesson`, `Drill`, `Dashboard`, `UserPublic`), token helpers (`getToken`/`setAuthToken`/`clearAuthToken` backed by secure storage), and a generic **`request<T>()`** that injects the bearer token, parses JSON, and throws the server's `detail` on error. The `api` object exposes one method per endpoint. The standout is **`transcribeAudio`**, which builds multipart `FormData` (handling web `blob:`/`data:` vs native `{uri,name,type}`), and **retries up to 3 times** on transient network failures — because a just-stopped recording file can briefly be unreadable — while never retrying real 4xx/5xx errors, all under a 30s abort timeout.

**`contexts/AuthContext.tsx`** — React context holding `user` + `loading`. On mount it tries the stored token and fetches `/auth/me`. Exposes `login`, `signup`, `resetPassword` (each stores the token and sets the user), `logout`, and `refreshUser`. `useAuth()` is the guarded consumer hook.

**`theme.ts`** — Design tokens: a `colors` palette (brand green `#3E9D6B`), an `accents` map (base + soft tint pairs), `accentCycle` for cycling colors across lists, `gradients`, and scales for `spacing`, `radius`, `fontSize` (including large `hanzi` sizes), and `shadows` (including a `glow(color)` factory). **`getToneColor(pinyin)`** inspects the diacritic on a pinyin string and returns the matching tone color (tone 1–4), used to color pinyin everywhere.

**`utils/storage/`** — A cross-platform key-value wrapper with a platform-split: `index.ts` (native) and `index.web.ts` (web), Metro picks the right one.
- **`storage-base.ts`** — abstract `StorageBase` with a `retrieve()` helper that JSON-parses stored values and a `warn()` logger; declares the six abstract methods. The `AssertNoExtras` type is a compile-time guard forcing subclasses to declare nothing beyond the base.
- **`index.ts`** — native impl. General KV via `AsyncStorage`; secure values via `expo-secure-store` (Keychain/EncryptedSharedPreferences). All methods swallow errors (reads return fallback, writes return false).
- **`index.web.ts`** — web impl. Same, but secure* methods just fall through to `AsyncStorage` since browsers have no Keychain.

**`hooks/use-icon-fonts.ts`** — **`useIconFonts()`** loads `@expo/vector-icons` TTFs from a CDN, but **only under Expo Go** (where Metro returns 0-byte fonts on Android); native/web builds get an empty map and resolve instantly.

### Shared components
- **`PressableScale.tsx`** — a `Pressable` that springs down to ~0.96 scale on press via Reanimated; a tactile drop-in for `TouchableOpacity`.
- **`HandwritingCanvas.tsx`** — a dependency-light drawing surface. Uses `PanResponder` to build SVG path strings as you draw, renders them with `react-native-svg`, and exposes a ref handle (`captureBase64`, `clear`, `isEmpty`). `captureBase64` uses `react-native-view-shot` to snapshot the view as a 512×512 PNG for the OCR endpoint. Includes Undo/Clear toolbar buttons and a placeholder hint.

### Review feature components (`src/components/review/`)
- **`types.ts`** — `Mode` ('reading'|'writing'|'speaking'), the `Card` shape (vocab + mode + round + `isFinal`), the `OnAnswered` callback type, and writing-result types.
- **`reviewHelpers.ts`** — `STAGE_LABELS` and `MODE_META` (label/icon/description per mode); **`shuffleArray`** (Fisher–Yates); **`buildMultiModeQueue`** which is the clever bit: every due/new word gets all three modes, one per "round", shuffled, so a session tests each word by reading, writing, and speaking without the same card repeating back-to-back; **`formatNextReview`** (humanizes an ISO date to "in 2 weeks"); and **`englishMatches`** (local synonym-free string match, tried before the WordNet API call).
- **`ReadingCard.tsx`** — shows the hanzi, hides pinyin, takes an English answer. `handleCheck` tries the local `englishMatches` first, then falls back to the `semanticMatch` API. Then reveals pinyin/meaning and Correct/Incorrect buttons.
- **`WritingCard.tsx`** — shows English + pinyin, embeds the `HandwritingCanvas`, captures the drawing and calls `recognizeHandwriting`. Computes `passed = score≥80 && identity≥67` and renders per-character result tiles or a target-vs-recognized comparison. Lets the user "Mark correct anyway" if OCR was harsh.
- **`SpeakingCard.tsx`** — uses `expo-audio` to record. Manages mic-permission state (including the "blocked → open Settings" path), records, waits 250 ms for the file to flush, uploads via `transcribeAudio`, and renders score/feedback with target vs. "AI heard" pinyin (colored by match) and a tones-wrong note.
- **`review.styles.ts`** — shared StyleSheet for all three cards and the review screen.

### Navigation & screens (`app/` — Expo Router file-based routing)

**Layouts**
- **`_layout.tsx`** (root) — keeps the splash screen up until icon fonts load, wraps everything in `GestureHandlerRootView` → `SafeAreaProvider` → `AuthProvider`. **`ProtectedRoutes`** is the auth guard: redirects unauthenticated users to `/(auth)/login` and authenticated users away from auth/root into `/(tabs)`. Declares the navigation stack.
- **`index.tsx`** — root redirect: spinner while loading, then to tabs or login.
- **`(auth)/_layout.tsx`** and **`(tabs)/_layout.tsx`** — the auth stack (headerless) and the bottom tab bar (Home, Review, Lessons, Speak, Profile) with platform-tuned styling.
- **`+html.tsx`** — web-only HTML shell that disables body scrolling so React Native ScrollViews behave.

**Auth screens (`app/(auth)/`)**
- **`login.tsx`** — branded email/password form; `onSubmit` validates then calls `login()`. Lots of styling, focus states, animated entrance, a "间隔" watermark.
- **`signup.tsx`** — name/email/password with a 6-char check, calls `signup()`.
- **`forgot-password.tsx`** — two-phase: `requestCode` (gets the reset token, which it auto-fills since there's no email) then `submitReset` (validates matching passwords, calls `resetPassword()`).

**Tab screens (`app/(tabs)/`)**
- **`index.tsx` (Home)** — loads the dashboard on focus. Shows greeting + streak badge, an animated daily-progress bar, a "Continue Learning" CTA (disabled when nothing's due), a grid of six quick-action tiles routing to features, and a "Memory Snapshot" of stat cards. `StatCard` is a small local component.
- **`review.tsx`** — the SRS session driver. `loadQueue` fetches due cards + new vocab + deck in parallel and builds the multi-mode queue. `handleAnswered` accumulates per-card results across the three modes; on the **final** mode it aggregates (≥2/3 correct = correct) and advances the SRS **once**, while non-final modes log history only (`skip_srs`). Renders empty-deck, all-caught-up, in-progress (progress bar + mode banner + the right card via `CardBody`), and a completion summary listing each word's next review.
- **`lessons.tsx`** — fetches lessons on focus and renders a `FlatList` of cards with number badge, accent color, word/mastered counts, and a progress bar; tapping opens the lesson detail.
- **`speak.tsx`** — builds collapsible per-lesson "folders" of every dialogue sentence (via a `SectionList`); tapping a sentence routes to `speak-practice` with the sentence params.
- **`profile.tsx`** — loads stats + the review schedule. Shows user card, a 4-box stats grid, an upcoming-reviews list (`formatScheduleDate` labels Tomorrow/weekday/date), weak-words list, an editable daily-goal, an inline change-password form (`handleChangePassword`), and a platform-aware logout (`window.confirm` on web, `Alert` on native).

**Standalone screens (`app/`)**
- **`lesson/[id].tsx`** — lesson detail. Loads the lesson, renders dialogue (grouped by Part 1/2), grammar notes, and the vocab list. `handleAddAll`/`handleAddOne`/`handleRemoveOne` manage deck membership with optimistic local state updates. Buttons jump to drills for that lesson.
- **`drill.tsx`** — the drill runner. If no lesson was passed it shows a lesson **picker**; otherwise it loads that lesson's drills. Each drill asks you to *say* an English prompt in Mandarin. It offers a **tiered hint system** (none → characters → pinyin), records audio (same permission/record/upload flow as speaking), scores via `transcribeAudio`, logs the attempt, shows feedback with target-vs-heard comparison and tone notes, and advances. Tracks session stats.
- **`speak-practice.tsx`** — single-sentence pronunciation practice (reached from the Speak tab). Hides the Mandarin behind a "Show Mandarin" reveal so you produce it from the English, records and transcribes, then shows a score bar, target-vs-heard pinyin, and tone feedback, with Try-again / Next.
- **`library.tsx`** — the vocabulary library. Debounced-ish search, all/NPCR/custom filter chips, multi-select with a bulk "Add to deck" bar, single add/remove, and delete for custom words (platform-aware confirm). Optimistically updates rows.
- **`add-word.tsx`** — form to create a custom word (required: simplified/pinyin/english; optional example sentence). On save it calls `createCustomVocab` (which auto-adds to the deck) and pops back. `Section` and `Field` are small layout helpers.

## How it all fits together (the main flows)

1. **Auth** → JWT stored in secure storage; `AuthContext` + `ProtectedRoutes` gate everything.
2. **Build a deck** → browse Lessons or Library, or add custom words → words land in `user_deck`.
3. **Review** → `buildMultiModeQueue` interleaves reading/writing/speaking for each due word; only the final mode advances the SRS stage, which reschedules `next_review_at` using `SRS_INTERVALS`.
4. **AI grading** → speaking goes to FunASR + the syllable/tone `score_pronunciation`; handwriting goes to EasyOCR + bag-of-characters; reading uses local + WordNet synonym matching.
5. **Drills & Speak** → extra active-production practice keyed off the same lesson dialogues.
6. **Progress** → `review_history` and per-card counts feed the Home dashboard and Profile stats.

Two small things worth flagging, since they're intentional shortcuts rather than bugs: password reset **returns the token in the API response** (no email service), and `daily_goal` is read from the JWT-loaded user doc rather than re-fetched — both are noted in the code comments.

---
---

# PART 2 — METHOD-BY-METHOD REFERENCE

Below is an exhaustive, method-by-method breakdown. For each function it gives its signature, what it receives, every meaningful step it takes, edge cases it handles, and what it returns.

## BACKEND

### `config.py`
No functions — top-level execution only.
- `ROOT_DIR = Path(__file__).resolve().parent.parent` resolves to `backend/`. `load_dotenv(ROOT_DIR / ".env")` reads the env file there.
- `os.environ["MONGO_URL"]` / `["DB_NAME"]` / `["JWT_SECRET_KEY"]` use bracket access deliberately — if any is missing the process crashes at import (fail-fast), rather than running misconfigured.
- `os.environ.get(...)` with defaults is used for the optional values (algorithm, token expiry, ASR settings) so they're tolerant.
- `int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 43200))` — env vars are strings, so it casts; 43200 min = 30 days.
- `SRS_INTERVALS` dict maps stage→days; consumed only in `flashcards.py`.

### `main.py`

**`root()`** (`@api_router.get("/")`, async)
- No params. Returns a static dict `{"message", "version"}`. Pure liveness check; unauthenticated.

**Module-level router wiring**
- `for module in (auth, lessons, …): api_router.include_router(module.router)` — each router module exposes a `router` attribute; this mounts all of them under `/api`. Then `app.include_router(api_router)` mounts that under the app.

**`on_startup()`** (async, `@app.on_event("startup")`)
- Awaits `create_indexes()` → `seed_lessons_and_vocab()` → `migrate_legacy_decks()` in order (indexes must exist before seeding; seeding before migration). Then `asr.warm_up()` (synchronous) to preload the speech model. Order matters: migration depends on flashcards/deck collections existing.

**`on_shutdown()`** (async)
- `client.close()` — releases Mongo connections cleanly.

### `db.py`

**`create_indexes()`** (async, returns `None`)
- `db.users.create_index("email", unique=True)` — enforces unique emails at the DB layer (defense even if app logic misses a duplicate).
- `db.flashcards.create_index([("user_id",1),("vocabulary_id",1)], unique=True)` — one flashcard per user per word.
- `db.flashcards.create_index([("user_id",1),("next_review_at",1)])` — makes the "due cards" query (`user_id == X and next_review_at <= now`, sorted) index-covered and fast.
- `db.user_deck.create_index([("user_id",1),("vocabulary_id",1)], unique=True)` — one deck entry per user per word.
- `db.vocabulary.create_index("created_by")` — fast lookup of a user's custom words.
- All idempotent; creating an existing index is a no-op.

**`seed_lessons_and_vocab()`** (async, returns `None`)
- `existing = count_documents({})` on lessons.
- **Skip branch:** `if existing == len(NPCR_LESSONS): log + return`. Normal restart path — no rewrites.
- **Reseed branch:** `if existing != len and existing > 0:` deletes lessons, vocabulary, drills (only content collections — user data untouched). This triggers when you change the number of seeded lessons.
- **Seeding loop:** for each lesson dict:
  - `lesson_id = uuid4()`. For each vocab in the lesson, generate `vocab_id`, insert a vocab doc spreading the lesson fields plus `**vocab`, collect IDs in `vocab_ids`.
  - Insert the lesson doc with `vocabulary_ids` and `vocabulary_count`.
- Then insert each drill with a fresh UUID.
- Logs counts. Note: uses app-generated UUID `id` fields throughout rather than Mongo `_id`, so IDs are stable/portable.

**`migrate_legacy_decks()`** (async, returns `None`)
- Aggregation pipeline groups flashcards by `user_id`, collecting the set of `vocabulary_id`s (`$addToSet`).
- For each user, for each vocab id, checks if a `user_deck` row exists; if not, inserts one (UUID, timestamp). Increments `total`.
- Logs only if anything was migrated. Backfills decks for accounts predating the explicit-deck model.

### `models.py`
No methods — Pydantic models. Notable validation:
- `UserCreate.password = Field(min_length=6)`, `name = Field(min_length=1)`; `email: EmailStr` (format-validated).
- `UserPublic` has defaults (`daily_goal=20`, `streak_count=0`) so partial docs still serialize.
- `FlashcardReviewRequest.mode` defaults `"reading"`; `skip_srs` defaults `False`.
- `ResetPasswordRequest.new_password = Field(min_length=6)`.
- Comments on `ForgotPasswordResponse` explain returning the token is a deliberate no-mail-service choice.

### `auth.py`

**`hash_password(plain) -> str`**
- `bcrypt.hashpw(plain.encode(), bcrypt.gensalt())` → bytes → `.decode()` to store as a UTF-8 string. `gensalt()` creates a random per-password salt embedded in the hash.

**`verify_password(plain, hashed) -> bool`**
- `bcrypt.checkpw(plain.encode(), hashed.encode())`. Wrapped in `try/except` returning `False` — a malformed stored hash can't crash login, it just fails auth.

**`create_access_token(user_id) -> str`**
- `expire = now(utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)`. Payload `{"sub": user_id, "exp": expire}`. `jwt.encode(...)` signs with `JWT_SECRET`/`JWT_ALGO`. `exp` is honored automatically by PyJWT on decode.

**`get_current_user(creds) -> dict`** (async, FastAPI dependency)
- `creds` injected via `Depends(security)` where `security = HTTPBearer(auto_error=False)` — `auto_error=False` means a missing header yields `None` instead of FastAPI auto-raising, so the function controls the error.
- `if creds is None: raise 401`.
- `jwt.decode(creds.credentials, …)` — raises `PyJWTError` (caught → 401) on bad signature/expiry. Extracts `sub`; missing sub → 401.
- `db.users.find_one({"id": user_id}, {"_id":0, "hashed_password":0})` — fetches user **without** the hash or Mongo id. Not found → 401.
- Returns the sanitized user dict (this is why `change_password` must re-fetch the hash separately).

**`user_to_public(doc) -> UserPublic`**
- Constructs `UserPublic` pulling required fields and `.get(...)` with defaults for optional ones. Centralizes the "safe shape."

### `scoring.py`

**`normalize_chinese(text) -> str`**
- `re.sub(r"[\s\W_，。!?,.!?]", "", text or "")` — removes whitespace, non-word chars, underscores, and both ASCII and full-width punctuation. `text or ""` guards `None`.

**`pinyin_syllables(text) -> list[str]`**
- `lazy_pinyin(text, style=Style.TONE3)` returns tone-number pinyin; list-comprehension lowercases each. `你好` → `["ni3","hao3"]`.

**`_strip_tone(syllable) -> str`**
- `syllable.rstrip("012345")` removes trailing tone digits (5 = neutral). `"hao3"` → `"hao"`.

**`pinyin_display(text) -> str`**
- `" ".join(lazy_pinyin(text, style=Style.TONE))` — diacritic pinyin joined by spaces for display.

**`score_pronunciation(target, spoken) -> dict`** — the core algorithm
- Compute `target_syls`, `spoken_syls`. `total = len(target_syls)`.
- **Empty guard:** `total == 0` → returns zeros with `correct=False`.
- `pool = Counter(spoken_syls)` — multiset of what was said.
- **Pass 1 (exact):** loop target syllables; if present in `pool`, decrement and increment `full`; else append to `unmatched`. This consumes spoken syllables so duplicates are handled correctly.
- **Pass 2 (tone-wrong):** build `base_pool` = Counter of remaining spoken syllables stripped of tone. For each unmatched target syllable, if its base sound remains in `base_pool`, decrement and increment `tone_wrong`.
- `credit = full + 0.5*tone_wrong`; `score = round(credit/total*100)`.
- `correct = full == total and len(spoken_syls) == total` — requires every syllable exact in sound+tone AND no extra syllables spoken (no insertions).
- Returns `{score, correct, syllables_right (=full+tone_wrong), tones_wrong, total}`. Order-independence is the point: a dropped middle syllable doesn't misalign the rest.

**`pronunciation_feedback(p) -> str`**
- Cascading conditions producing a human message: perfect → all-syllables-but-tones → some-tones-wrong → ≥80 → ≥50 → else. Reads the dict from `score_pronunciation`.

### `semantic.py`

**Module import block**
- Tries `from nltk.corpus import wordnet as wn; wn.synsets("call")`. The probe call forces NLTK to actually touch the corpus; if data is absent it raises `LookupError`, caught to `nltk.download("wordnet"/"omw-1.4", quiet=True)` then re-import. So first-run auto-provisions the corpus.

**`normalize_en(s) -> str`**
- Lowercases/strips; `re.sub(r"[.;]+$","",s)` strips trailing `.`/`;`; `re.sub(r"^(to |a |an |the )","",s)` strips a leading article/infinitive marker; final `.strip()`.

**`_word_synonyms(word) -> set`**
- For each synset of the word, for each lemma, add `lemma.name().lower().replace("_"," ")` (WordNet joins multiword lemmas with `_`). Returns the synonym set.

**`words_match(w1, w2) -> bool`**
- Fast path: equal. Else compute both synonym sets and return `w2 in syns1 or w1 in syns2` (bidirectional membership).

**`answer_matches_target(answer, target) -> bool`**
- `answer_clean = normalize_en(answer)`. Split target on `;`, `,`, `/`, or word "or" (`re.split(r"[;,/]|\bor\b", target)`). Normalize each non-empty part. Return `any(words_match(answer_clean, part) …)`. So "to call / to be called" matches "call".

### `asr.py`

**`_get_model()`**
- Double-checked locking singleton: outer `if _model is None`, acquire `_model_lock`, inner `if _model is None` (guards against a race where two threads passed the outer check). Imports `funasr.AutoModel` lazily (heavy import only when needed), constructs with `trust_remote_code=True`, `device`, `hub`, `disable_update=True`. Caches in global `_model`. Returns it.

**`warm_up()`**
- Just calls `_get_model()` to force the load eagerly (used at startup).

**`_to_wav_16k(src_path) -> str`**
- Creates a temp `.wav` (`delete=False` so the path survives after closing the handle). Runs `ffmpeg -y -i src -ar 16000 -ac 1 dst` (`check=True` raises on nonzero exit; stderr captured).
- On `CalledProcessError`: removes the temp file, raises `RuntimeError` with decoded ffmpeg stderr.
- On `FileNotFoundError` (ffmpeg not installed): removes temp, raises a clear "install ffmpeg" error.
- Returns the new WAV path.

**`transcribe(audio_path, language=ASR_LANGUAGE) -> str`** (blocking)
- `model = _get_model()`; `wav_path = _to_wav_16k(audio_path)`.
- Inside `try`: acquire `_infer_lock` (serializes inference — the model isn't thread-safe), call `model.generate(input=[wav_path], cache={}, batch_size=1, language=language, itn=False)`. `itn=False` keeps raw hanzi instead of normalizing single syllables into Latin letters.
- `finally`: removes the temp WAV (`OSError` swallowed).
- `if not res: return ""`. Else `res[0].get("text") or ""` stripped. Note: it deletes `wav_path` but *not* the original `audio_path` — the caller (router) owns that temp file.

### `seed_data.py`

**`_expand_drill(lesson_number, part, group, instruction_en, instruction_zh, pattern_zh, pattern_en, variants, repeat_count=6) -> list`**
- Loops `variants` (each a dict with `chinese`/`pinyin`/`english`) and builds a uniform drill dict per variant carrying the shared template fields plus the variant's expected answer. Returns the list. This is a data-construction helper; `SENTENCE_DRILLS` is assembled by extending with these outputs. (`repeat_count` here is stored on the doc; the *runtime* repetition actually comes from `REPEAT_PER_DRILL` in the drills router.)

### `routers/auth.py`

**`signup(payload: UserCreate)`** (async)
- Lowercases email. `find_one({"email"})`; if exists → 400 "Email already registered".
- Builds `user_doc`: UUID id, lowercased email, name, `hash_password(password)`, defaults (`daily_goal=20`, `streak_count=0`, `learner_level="Beginner"`), `last_active_date = today.isoformat()`, `created_at=now`. Inserts it.
- `create_access_token(user_id)`, returns `TokenResponse(access_token, user=user_to_public(user_doc))`.

**`login(payload: UserLogin)`** (async)
- Lowercase email, fetch user. `if not user or not verify_password(...)` → 401 (same message for both to avoid leaking which exists).
- **Streak logic:** `today`, `last_active = user.get("last_active_date")`, start `new_streak` from stored value.
  - If `last_active` exists: parse to date. Same day → keep. Exactly 1 day ago (`(today-last).days==1`) → `+1`. Any larger gap → reset to 1.
  - If no `last_active` → 1.
- Persists `last_active_date=today` and `streak_count=new_streak`; mirrors into the in-memory `user` so the response is current.
- Returns token + public user.

**`forgot_password(payload)`** (async)
- Lowercase email; not found → 404. Generate UUID `token`, `expires_at = now + 30min`. Store both on the user. Return `ForgotPasswordResponse(reset_token=token, expires_in_minutes=30)` (token surfaced because no email service).

**`reset_password(payload: ResetPasswordRequest)`** (async)
- `find_one({"reset_token": payload.token})`; missing → 400.
- `expires_at = user.get("reset_token_expires_at")`; missing → 400.
- **TZ handling:** `if expires_at.tzinfo is None: expires_at = expires_at.replace(tzinfo=utc)` — Mongo may return naive datetimes; this makes the comparison safe. If `expires_at < now` → 400.
- Updates `hashed_password` and `$unset`s the token fields atomically. Returns a fresh login token (logs you straight in).

**`get_me(current_user=Depends(get_current_user))`** — returns `user_to_public(current_user)`.

**`change_password(payload, current_user)`** (async)
- `current_user` lacks the hash, so re-`find_one({"id"})` for the full doc. Verify `current_password`; wrong → 400. Update to new hash. Returns `{"success": True}`.

**`update_me(payload: UserSettingsUpdate, current_user)`** (async)
- `updates = {k:v for k,v in payload.dict().items() if v is not None}` — only patches provided fields. If any, `update_one(... $set updates)`. Re-fetch sanitized doc and return public form (so the client sees the saved state).

### `routers/lessons.py`

**`list_lessons(current_user)`** (async)
- All lessons, `{_id:0}`, sorted by `lesson_number`, capped 100.
- For each lesson: if it has `vocabulary_ids`, count `mastered` (`current_stage >= 4`) and `started` (any flashcard) among those ids for this user via `$in`. Attach `progress = {mastered, started, total}`. Empty lessons get zeros. Returns the list.

**`get_lesson(lesson_id, current_user)`** (async)
- Fetch lesson; missing → 404. Fetch its vocab (`lesson_id` match). Fetch the user's deck entries (projection `vocabulary_id` only, up to 10000) → build `deck_set`. For each vocab set `in_deck = id in deck_set`. Attach `lesson["vocabulary"]` and return.

### `routers/flashcards.py`

**`get_due_flashcards(limit=20, current_user)`** (async)
- Query flashcards where `next_review_at <= now`, sorted ascending (most overdue first), limited. For each card, fetch its vocab and append `{**card, "vocabulary": vocab}` (skips cards whose vocab vanished). Returns enriched list.

**`get_new_flashcards(lesson_id=None, limit=10, current_user)`** (async)
- Get deck `vocabulary_id`s; empty → `[]`.
- Get existing flashcards' `vocabulary_id`s → `existing_ids` set.
- `new_ids = deck_ids not in existing_ids` (deck words never reviewed). Empty → `[]`.
- Query vocab `id ∈ new_ids` (+ optional `lesson_id`), sorted by lesson number, limited. Returns vocab docs (not flashcards — these have no card yet).

**`get_review_schedule(days=14, current_user)`** (async)
- Window `now … now+days`. Fetch due-within-window cards (projection just `next_review_at`, cap 5000). `counts = defaultdict(int)` keyed by `YYYY-MM-DD`. Then for each of the next `days` days (starting tomorrow, `i+1`), if that date has a count, append `{date, count}`. Returns only days that actually have reviews.

**`submit_review(payload: FlashcardReviewRequest, current_user)`** (async) — the SRS state machine
- Fetch vocab; missing → 404. Fetch `existing` flashcard for (user, vocab).
- **`skip_srs` branch:** log history only (if a card exists, record a `review_history` row with mode/time). Returns current stage and next_review unchanged (the non-final review modes use this so only the last mode advances SRS).
- **Existing card:**
  - Correct → `new_stage = min(stage+1, 6)`, `correct_count+1`.
  - Incorrect → `new_stage = 1` (full reset), `incorrect_count+1`.
  - `next_review = now + SRS_INTERVALS[new_stage]` days. `update_one` sets stage/next_review/counts/`last_reviewed_at`. `card_id = existing["id"]`.
- **New card:** `new_stage = 2 if correct else 1`; compute next_review; insert a full flashcard doc (counts initialized from this first answer). `card_id` = new UUID.
- Always insert a `review_history` row (id, user, vocab, flashcard_id, was_correct, response_time, mode, timestamp).
- Returns `{success, new_stage, next_review_at: iso}`.

### `routers/drills.py`

**`list_drills(lesson_number=None, part=None, limit=500, current_user)`** (async)
- Build `query` from optional filters. Fetch drills (cap 2000, seed order preserved so pattern variants stay grouped).
- **Expansion:** for each drill, append it `REPEAT_PER_DRILL` (3) times to `expanded`. Return `expanded[:limit]`. This is what makes you drill each pattern 3× back-to-back.

**`submit_drill_attempt(payload: DrillAttemptRequest, current_user)`** (async)
- Insert a `drill_attempts` row (id, user, drill_id, answer, was_correct, response_time, timestamp). Returns `{success: True}`. Pure logging — no scoring here (scoring happened client-side via the speaking API).

### `routers/deck.py`

**`list_deck(current_user)`** (async)
- Deck entries sorted by `added_at` desc (cap 10000). For each, fetch vocab; if present, also fetch the flashcard to expose `current_stage` and `next_review_at` (iso or null). Append `{**entry, vocabulary, current_stage, next_review_at}`. Returns list.

**`add_to_deck(payload: DeckAddRequest, current_user)`** (async)
- For each id: verify vocab exists (skip if not); skip if already in deck; else insert a deck row and `added += 1`. Returns `{"added": added}` so the UI can say "N words added."

**`remove_from_deck(vocabulary_id, current_user)`** (async)
- `delete_one` the deck entry; **also** `delete_one` the flashcard for that word (removing from deck discards SRS progress). Returns `{"removed": deck_res.deleted_count > 0}`.

### `routers/vocabulary.py`

**`check_semantic_match(payload: SemanticMatchRequest, current_user)`** — returns `{"match": answer_matches_target(answer, target)}`.

**`create_custom_vocab(payload: CustomVocabCreate, current_user)`** (async)
- Build a vocab doc: UUID id, `lesson_id=None`, `lesson_number=None` (marks it custom), trimmed fields, `traditional` set equal to `simplified` (no conversion), `part_of_speech` default "custom", `created_by=user_id`, timestamp. Insert it.
- **Auto-add to deck:** insert a `user_deck` row for it.
- `doc.pop("_id", None)` (remove Mongo id Motor injected on insert) and return the doc.

**`delete_custom_vocab(vocab_id, current_user)`** (async)
- Fetch vocab; missing → 404. **Ownership check:** `created_by != user_id` → 403. Delete the vocab, then cascade `delete_many` on `user_deck` and `flashcards` for that vocab id. Returns `{"deleted": True}`.

**`vocabulary_library(q=None, lesson_number=None, source=None, limit=200, current_user)`** (async)
- Start `query={}`. If `source=="npcr"` → `lesson_number != None`; if `"custom"` → `created_by == user`. If `lesson_number` provided, set it.
- If `q`, add `$or` regex (case-insensitive) over simplified/pinyin/english.
- If `source is None` (the "all" tab), wrap into `$and` of the query plus `$or[ lesson_id != None, created_by==user ]` — i.e. all NPCR words **plus** this user's customs (but not other users' customs).
- Fetch sorted by `(lesson_number asc, created_at desc)`, limited. Build `deck_set`. Annotate each item with `in_deck` and `is_custom`. Return.

### `routers/speaking.py`

**`transcribe_audio(file: UploadFile, target_chinese="", vocabulary_id=None, current_user)`** (async)
- Derive `suffix` from the filename extension; if it's not in `_ALLOWED_AUDIO_SUFFIXES`, force `.m4a`.
- `contents = await file.read()`. **Size guards:** `> 25MB` → 400; `< 100 bytes` → 400 (empty/garbage).
- Write to a `NamedTemporaryFile(delete=False, suffix=…)`, close it.
- `try`: `await run_in_threadpool(asr.transcribe, tmp.name)` — runs the blocking ASR off the event loop. `except` → log + 502. `finally`: remove the temp file (`OSError` swallowed).
- Strip transcription. `result = {"transcribed_text": transcribed}`.
- **If `target_chinese`:** normalize both, `p = score_pronunciation(target_norm, spoken_norm)`. Insert a `speaking_attempts` record (score, exact_match, vocab, source="funasr", timestamp). Update `result` with `correct, score, feedback (pronunciation_feedback(p)), target_text, target_pinyin (pinyin_display), spoken_pinyin, tones_wrong, syllables_right, syllable_count`.
- Return `result`. (When no target is passed — pure transcription — only `transcribed_text` comes back.)

### `routers/writing.py`

**`_get_ocr_reader() -> easyocr.Reader`**
- Lazy global singleton: first call logs and constructs `easyocr.Reader(["ch_sim"], gpu=False)` (~100 MB model load). Returns cached reader.

**`_ocr_score(target_norm, recognized_norm) -> (int, bool)`**
- `target_chars = list(target_norm)`. `correct_chars = sum(1 for c in recognized_norm if c in target_chars)` — counts recognized chars that appear in the target (bag-of-characters; position-agnostic; `in target_chars` allows repeats to match).
- `score = round(correct_chars / max(len(target_chars),1) * 100)` if target else 0. `exact_match = (target==recognized) and len(target)>0`. Returns `(score, exact_match)`.

**`recognize_handwriting(payload: WritingRecognizeRequest, current_user)`** (async)
- `image_b64 = payload.image_base64`. If it starts with `data:`, split off the header via `partition(",")`. Guard: empty or `< 100` chars → 400.
- `target_norm = normalize_chinese(payload.target_chinese)`.
- `try`: base64-decode → `Image.open(BytesIO).convert("RGB")` → numpy array → `reader.readtext(img, detail=0, paragraph=True)` run via `loop.run_in_executor(None, …)` (off the event loop). `recognized_norm = normalize_chinese("".join(ocr_results))`. `except` → log + 502.
- `score, exact_match = _ocr_score(...)`. Insert a `writing_attempts` record (score, identity_score=score, quality_score=0, exact_match, vocab, timestamp).
- Return `{correct: exact_match, score, identity_score, quality_score:0, feedback:"", characters:[], recognized_text, target_text}`. (Per-character analysis fields exist in the contract but are stubbed — the frontend handles their absence.)

### `routers/progress.py`

**`get_dashboard(current_user)`** (async)
- `today_start` = midnight UTC today. Counts: `due_count` (`next_review_at <= now`), `total_cards`, `mastered` (`stage >= 4`).
- `reviews_today` and `correct_today` from `review_history` since `today_start`.
- **New count:** deck `vocabulary_id`s minus existing flashcards' ids → `len(deck_ids - existing_ids)` (deck words never reviewed). Comment explains why counting all vocab would be wrong.
- `daily_goal` from the user doc. `progress_percent = min(round(reviews_today/max(daily_goal,1)*100), 100)` (clamped, div-by-zero-safe). Returns the dashboard dict.

**`get_stats(current_user)`** (async)
- `total_reviews`, `correct_reviews` → `retention = round(correct/total*100)` if total else 0.
- `mastered` (`stage>=4`), `learning` (`stage<4`).
- **Weak words:** `find` with `$expr: {$gt: ["$incorrect_count","$correct_count"]}` (server-side field comparison), top 10. For each, fetch vocab and append `{simplified, pinyin, english, correct, incorrect}`.
- `speaking_attempts` count. Returns all stats plus streak.

## FRONTEND

### `src/api/client.ts`

**`getToken() -> Promise<string|null>`** — `storage.secureGet(TOKEN_KEY, '')`.
**`setAuthToken(token)`** — `storage.secureSet(...)`.
**`clearAuthToken()`** — `storage.secureRemove(...)`.

**`request<T>(path, init={}) -> Promise<T>`** — the generic fetch
- Reads token; builds headers merging caller's headers with `Content-Type: application/json`; adds `Authorization: Bearer` if a token exists.
- `fetch(${BASE_URL}/api${path}, {...init, headers})`. Reads `res.text()` then `JSON.parse` only if non-empty (tolerates empty bodies → `null`).
- On `!res.ok`, throws `Error(data.detail || data.message || "Request failed (status)")` — surfaces the backend's `detail`. Else returns `data as T`.

**The `api` object** — each method wraps `request` with the right path/verb/body. Highlights:
- `signup/login` POST credentials. `me` GET. `updateMe` PUT. `forgotPassword/resetPassword/changePassword` POST.
- `dashboard/stats/lessons/lesson(id)` GET. `semanticMatch` POST.
- `dueFlashcards(limit)`, `newFlashcards(limit, lessonId?)` (conditionally appends `lesson_id`), `drills(lessonNumber?)`, `drillAttempt(...)`.
- `deck/addToDeck/removeFromDeck`. `library(params)` — builds a `URLSearchParams` from optional `q/lesson_number/source`. `createCustomVocab/deleteCustomVocab`.
- `recognizeHandwriting(image_base64, target, vocabId?)` POST with a fully typed response.
- `reviewSchedule(days)`. `reviewFlashcardWithMode(vocabId, wasCorrect, mode, responseTime?, skipSrs?)` — wraps `/flashcards/review`.

**`transcribeAudio(audioUri, target_chinese, vocabulary_id?)`** (async) — the most complex client method
- Build `FormData`. Derive `filename`/`ext`/`mime` from a `typeMap`.
- **Web vs native upload:** if uri is `blob:`/`data:`, `fetch(uri).blob()` → `new File(...)` → append; else append `{uri, name, type}` (RN's native multipart shape).
- Build URL with `target_chinese` (URL-encoded) and optional `vocabulary_id` query params. Headers: `Accept` + bearer.
- **Retry loop** (`MAX_ATTEMPTS=3`, `RETRY_DELAY_MS=400`, `TIMEOUT_MS=30000`):
  - Per attempt: `AbortController` + `setTimeout(abort, 30s)`. `fetch` with `signal`. Parse body.
  - On `!res.ok` → throw the server error (a real 4xx/5xx — **not** retried).
  - On success → return data.
  - In `catch`: classify `isNetwork` (AbortError or /network request failed/). If not a network error, or last attempt → rethrow. Else sleep and retry. `finally` clears the timer.
- This exists because a just-stopped recording file is briefly unreadable, causing a spurious "Network request failed" before the request even reaches the server.

### `src/contexts/AuthContext.tsx`

**`AuthProvider({children})`**
- State: `user` (UserPublic|null), `loading` (true initially).
- **`useEffect` on mount:** IIFE reads stored token; if present, `api.me()` → `setUser`. On any error, `clearAuthToken()`. `finally setLoading(false)`. This is the "remember me" restore.
- **`login(email, password)`** — `api.login` → `setAuthToken(res.access_token)` → `setUser(res.user)`.
- **`signup(...)`** — same pattern via `api.signup`.
- **`resetPassword(token, newPassword)`** — `api.resetPassword` → store token + set user (logs in after reset).
- **`logout()`** — `clearAuthToken()` + `setUser(null)`.
- **`refreshUser()`** — `api.me()` → `setUser`, errors ignored (used after settings changes).
- Provides all of these via context.

**`useAuth()`** — `useContext`; throws if used outside the provider (guards misuse).

### `src/theme.ts`

**`getToneColor(pinyin) -> string`**
- Empty → `tone0`. Defines four strings of tone-marked vowels (tone 1 macron, tone 2 acute, tone 3 caron, tone 4 grave, both cases). Iterates each char of the pinyin; returns the color for the first tone diacritic found. No diacritic (neutral tone) → `tone0`. Used everywhere pinyin is shown.

**`shadows.glow(color)`** — a factory returning a colored shadow style object (used on CTAs/badges).

### `src/utils/storage/`

**`storage-base.ts` — `StorageBase` (abstract)**
- **`warn(op, key, e)`** (protected) — `console.warn` with a tagged message.
- **`retrieve<Fallback>(raw, fallback)`** (protected) — if `raw === null` return fallback; else `JSON.parse(raw)`; on parse error, `warn` and return fallback. Centralizes the "stored as JSON, never throw" contract.
- Declares six abstract methods (`getItem/setItem/removeItem/secureGet/secureSet/secureRemove`).

**`index.ts` (native) — `Storage extends StorageBase`**
- **`getItem(key, fallback)`** — `AsyncStorage.getItem` → `retrieve`; catch → warn + fallback.
- **`setItem(key, value)`** — `AsyncStorage.setItem(key, JSON.stringify(value))` → true; catch → warn + false.
- **`removeItem`** — delete → true/false.
- **`secureGet/secureSet/secureRemove`** — same shape but via `expo-secure-store` (Keychain/EncryptedSharedPreferences).
- Exports a singleton `storage`. `type _NoExtras = AssertNoExtras<...>` — compile-time check that the class adds no methods beyond the base.

**`index.web.ts` (web)** — identical general KV via AsyncStorage; the three `secure*` methods just delegate to their non-secure counterparts (no Keychain in browsers).

### `src/hooks/use-icon-fonts.ts`

**`iconFontMap()`** — builds a `{family: cdnUrl}` map for all icon families at the pinned `ICON_VECTOR_VERSION`.
**`useIconFonts() -> [boolean, Error|null]`**
- Calls `useFonts(...)` with the CDN map **only when** `Constants.executionEnvironment === StoreClient` (Expo Go), otherwise `{}` (native/web builds autolink fonts, so an empty map resolves instantly). Works around Expo Go returning 0-byte fonts on Android.

### `src/components/PressableScale.tsx`

**`PressableScale({scaleTo=0.96, style, children, ...rest})`**
- `scale = useSharedValue(1)`. `animatedStyle` maps `scale.value` to a transform.
- Renders an `AnimatedPressable`, spreading `rest`. **`onPressIn`** springs `scale` to `scaleTo` and forwards the original handler. **`onPressOut`** springs back to 1 and forwards. Style array combines caller style + animated transform. A tactile drop-in for `TouchableOpacity`.

### `src/components/HandwritingCanvas.tsx`

**`HandwritingCanvas = forwardRef(({height=260, testID}, ref) => …)`**
- Refs/state: `viewShotRef` (the captured view), `paths` (completed stroke path strings), `currentPath` (in-progress stroke).
- **`panResponder`** (created once via `useRef(...).current`):
  - `onStart/MoveShouldSetPanResponder` → true (claims touches).
  - **`onPanResponderGrant`** — start a path: `M{x},{y}` at touch start.
  - **`onPanResponderMove`** — append `L{x},{y}` segments as the finger moves.
  - **`onPanResponderRelease`** — push the finished `currentPath` into `paths`, reset `currentPath`.
- **`useImperativeHandle`** exposes:
  - **`clear()`** — empties paths + current.
  - **`isEmpty()`** — true if no paths and no current stroke.
  - **`captureBase64()`** — throws if not ready; else `captureRef(view, {format:'png', quality:0.8, result:'base64', width:512, height:512})` → returns base64 PNG. Dependency array `[paths, currentPath]` keeps the closure current.
- **Render:** a toolbar (Undo = `paths.slice(0,-1)`, disabled when empty; Clear = reset both, disabled when empty); the capture `View` (`collapsable={false}` so Android keeps it as a real view for snapshotting) wired with `panResponder.panHandlers`; an `Svg` drawing a dashed center guide, all completed `paths`, and the live `currentPath` (stroke width platform-tuned); and a placeholder shown only when empty.

### `src/components/review/`

**`reviewHelpers.ts`**
- **`shuffleArray<T>(arr)`** — in-place Fisher–Yates; returns the same array.
- **`buildMultiModeQueue(dueCards, newVocab) -> Card[]`** — the session builder:
  - Merge due cards (`current_stage` from the card) and new vocab (`current_stage: null`) into `entries`. Empty → `[]`.
  - Create three empty `rounds`. For each entry, `shuffleArray([...MODES])` and assign one mode per round (so each word is tested in all three modes, but the per-word mode order is randomized). Each `Card` records `round` and `isFinal = round===2`.
  - Shuffle within each round (so the same word doesn't recur adjacent across rounds), then concatenate rounds 0→1→2. Result: all words' first mode, then all second, then all third.
- **`formatNextReview(isoDate) -> string`** — diff in days from now; cascading buckets → "tomorrow" / "in N days" / "in 1 week" / "in N weeks" / "in 1 month" / "in N months" / "in 1 year".
- **`normalize(text)`** (private) — trim + lowercase.
- **`englishMatches(answer, target) -> boolean`** — local pre-check before hitting WordNet: normalize answer (strip trailing `.`/`;` and leading article); split target on `;,/`/"or", normalize each part; return true if the cleaned answer equals any part.

**`ReadingCard({card, onAnswered})`**
- State: `answer`, `result` (`{correct}|null`), `checking`.
- **`handleCheck()`** — first try local `englishMatches(answer, vocab.english)` → instant correct. Else `setChecking(true)`, call `api.semanticMatch`; set `result.correct = match`; on error → `correct:false`; `finally` clear checking.
- Render: hanzi shown, pinyin hidden until answered; a `TextInput` (disabled once `result` exists) styled green/red by result; feedback block revealing pinyin (tone-colored) + English; footer shows Check button (disabled when empty/checking) or, after a result, "Mark incorrect" / "Continue" calling `onAnswered(vocab.id, bool, 'reading')`.

**`WritingCard({card, onAnswered})`**
- Refs/state: `canvasRef`, `submitting`, `result: WritingResult|null`, `error`.
- **`handleSubmit()`** — if canvas empty → set error. Else `captureBase64()` → `api.recognizeHandwriting(base64, vocab.simplified, vocab.id)`. Compute `passed = score>=80 && identity_score>=67`. Build the `result` object. Errors → `setError`.
- **`qualityBarColor(q)`** — green/amber/red thresholds.
- Render: English + pinyin prompt, the canvas; on result, either per-character tiles (each with target, recognized, a quality bar, %, optional note) or a target-vs-"AI read" comparison; an "Identity %/Quality %" line; feedback. Footer: Submit, or after a result "Incorrect" / a Correct button whose label becomes "Mark correct anyway" when `!passed` (lets the user override harsh OCR). All call `onAnswered(..., 'writing')`.

**`SpeakingCard({card, onAnswered})`**
- Uses `useAudioRecorder(HIGH_QUALITY)`. State: `permission` (4-state), `recording`, `uploading`, `result: SpeakingResult|null`, `errorMsg`.
- **`useEffect` mount** — `setAudioModeAsync({playsInSilentMode, allowsRecording})`, then read current mic permission → set `granted`/`blocked`/`undetermined`.
- **`requestPermission()`** — request mic; set state to granted, or `denied`/`blocked` based on `canAskAgain`; returns bool.
- **`startRec()`** — clear error/result; ensure permission (request if needed; bail with error if denied); `prepareToRecordAsync()` + `record()`; set `recording`.
- **`stopAndUpload()`** — stop; read `recorder.uri` (null → error). **Wait 250 ms** for the file to flush. `setUploading`; `api.transcribeAudio(uri, vocab.simplified, vocab.id)`; map response into `result`. Errors → `errorMsg`; `finally` clear uploading.
- Render: prompt; a "Microphone blocked → Open Settings" panel; error panel; result panel (target hanzi/pinyin, "AI heard", spoken pinyin colored by exact match, match score, a tones-wrong note with singular/plural grammar). Footer state machine: result → Incorrect/Continue; recording → "Stop & transcribe" (with pulsing dot); uploading → spinner; idle → "Tap to record".

### App layouts & routing (`app/`)

**`_layout.tsx`**
- `SplashScreen.preventAutoHideAsync()` at module load.
- **`ProtectedRoutes()`** — reads `user`/`loading` and `useSegments()`. `useEffect`: while loading, do nothing. Compute `inAuthGroup` (`segments[0]==='(auth)'`) and `atRoot`. If no user and not in auth → `replace('/(auth)/login')`. If user and (in auth or at root) → `replace('/(tabs)')`. Renders the `Stack` (auth, tabs, and the three modal-ish card screens).
- **`RootLayout()`** — `useIconFonts()`; `useEffect` hides splash once fonts load or error; returns null until then. Wraps `GestureHandlerRootView → SafeAreaProvider → AuthProvider → (StatusBar + ProtectedRoutes)`.

**`index.tsx`** — `Index()` reads auth; spinner while loading; else `<Redirect href={user ? '/(tabs)' : '/(auth)/login'} />`.
**`(auth)/_layout.tsx`** — headerless `Stack`.
**`(tabs)/_layout.tsx`** — `TabsLayout()` configures the five tabs (icons via Ionicons, platform-tuned bar height/padding, floating shadow).
**`+html.tsx`** — `Root({children})` web HTML shell; `ScrollViewStyleReset` + fixed body so RN ScrollViews work in the browser.

### Auth screens

**`login.tsx` — `LoginScreen()`**
- State: `email`, `password`, `focused`, `submitting`, `error`.
- **`onSubmit()`** — clear error; if either field empty → set error and return; `setSubmitting`; `await login(email.trim(), password)` then `router.replace('/(tabs)')`; on error set message; `finally` clear submitting.
- Render: brand block, two inputs (focus-styled), a Forgot-password link, error box, gradient submit button (spinner while submitting), and a link to signup. `testID`s throughout for e2e.

**`signup.tsx` — `SignupScreen()`**
- State adds `name`. **`onSubmit()`** — require all three fields; require password ≥ 6; call `signup(email.trim(), password, name.trim())`; navigate; error handling identical pattern.

**`forgot-password.tsx` — `ForgotPasswordScreen()`**
- State: `phase` ('request'|'reset'), `email`, `code`, `password`, `confirm`, `focused`, `submitting`, `error`.
- **`requestCode()`** — require email; `api.forgotPassword(email.trim())`; **auto-fills `code` from `res.reset_token`** (no email service) and switches to 'reset' phase.
- **`submitReset()`** — require code + password; password ≥ 6; `password === confirm`; `await resetPassword(code.trim(), password)`; navigate to tabs.
- Render switches inputs by phase; a notice explains the code would normally be emailed.

### Tab screens

**`(tabs)/index.tsx` — `HomeScreen()`**
- State: `dashboard`, `loading`, `refreshing`.
- **`load()`** (`useCallback`) — `api.dashboard()` → set; errors ignored; `finally` clear loading + refreshing.
- **`useFocusEffect(load)`** — reloads every time the tab gains focus (so counts stay fresh after reviews).
- Derived: `reviewsToday/goal/progressPercent/dueCount/newCount`, `hasReviews`, `goalComplete`.
- **Progress animation:** `progress = useSharedValue(0)`; `useEffect` `withTiming` to the clamped percent over 800 ms; `fillStyle` maps it to width.
- Early return spinner while loading. `tiles` array defines the six quick actions (icon/title/sub/accent/route).
- Render: watermark, header (greeting + streak badge), animated daily-progress card (shows "goal complete" or "N reviews to go"), the "Continue Learning" CTA (haptic + navigate; disabled and grayed when nothing due), the tile grid (staggered `FadeInDown`), and a stats row.
- **`StatCard({testID, value, label, accent})`** — a presentational stat tile.

**`(tabs)/review.tsx` — `ReviewScreen()`** (the SRS session orchestrator)
- State: `queue`, `index`, `loading`, `sessionStats`, `done`, `hasDeck`, `cardModeResults` (per-vocab list of `{mode, correct}`), `reviewSummary`.
- **`loadQueue()`** — reset everything; `Promise.all([dueFlashcards(20), newFlashcards(10), deck().catch(()=>[])])`; `setHasDeck(deck.length>0)`; `setQueue(buildMultiModeQueue(due, fresh))`. On error → empty queue. (The `.catch` on deck means a deck failure won't sink the whole load.)
- **`useFocusEffect(loadQueue)`** — fresh session on each focus.
- **`handleAnswered(vocabId, wasCorrect, mode)`** — the per-answer brain:
  - Append `{mode, correct}` to that vocab's `cardModeResults`.
  - **If `card.isFinal`** (3rd mode): aggregate `correctCount = results.filter(correct).length`, `aggregateCorrect = correctCount >= 2`; call `reviewFlashcardWithMode(vocabId, aggregateCorrect, mode)` (no skip → **advances SRS once**); push the returned stage/next-review into `reviewSummary`.
  - **Else:** `reviewFlashcardWithMode(vocabId, wasCorrect, mode, undefined, true)` (`skip_srs=true` → history only).
  - Network errors swallowed. Update `sessionStats`. Advance `index` or set `done`.
- Conditional renders: loading spinner; empty-deck screen (links to library/add-word); all-caught-up screen; **done** screen (session summary + per-word "Next Reviews" list using `STAGE_LABELS` + `formatNextReview`, with Back-to-Home / Review-More); else the active card — progress bar, a mode banner (`MODE_META` icon/label/description + stage label), and `CardBody`.
- **`CardBody({card, onAnswered})`** — dispatches to `ReadingCard`/`WritingCard`/`SpeakingCard` by `card.mode`. Keyed by `${vocab.id}-${mode}-${index}` so React remounts a fresh card each step.

**`(tabs)/lessons.tsx` — `LessonsScreen()`**
- **`load()`** + `useFocusEffect`. Renders a `FlatList`; each row gets a cycling accent (`accentCycle[index % len]`), staggered entrance, number badge, title/subtitle, level pill, "N words · M mastered", and a started/total progress bar; tapping routes to `/lesson/{id}`.

**`(tabs)/speak.tsx` — `SpeakScreen()`**
- State: `groups`, `expanded` (Set of lesson numbers), `loading`.
- **`load()`** — fetch lessons; build a `groupMap` keyed by lesson number, pushing every dialogue line as a `Sentence`; set sorted groups.
- **`toggle(lessonNumber)`** — add/remove from the `expanded` set (accordion).
- `sections` — maps groups to `SectionList` sections whose `data` is the sentences only when expanded (collapsed → empty array → header-only).
- Render: a `SectionList`; **`renderSectionHeader`** is a tappable folder row (open/closed folder icon, lesson label/title, sentence count, chevron); **`renderItem`** is a sentence card (hanzi, tone-colored pinyin, English, a mic button) that routes to `/speak-practice` with the sentence params; **`renderSectionFooter`** adds spacing under expanded sections.

**`(tabs)/profile.tsx` — `ProfileScreen()`**
- **`formatScheduleDate(dateStr)`** (module fn) — "Tomorrow" if next day; weekday name if within 7 days; else "Mon D".
- State: `stats`, `schedule`, `loading`, goal-editing (`editing`, `draftGoal`), and password-change form (`changingPw`, `currentPw`, `newPw`, `confirmPw`, `pwSubmitting`, `pwError`, `pwSuccess`).
- **`load()`** — `Promise.all([stats(), reviewSchedule(14)])`; seed `draftGoal` from the user. `useFocusEffect`.
- **`handleLogout()`** — defines `doLogout` (logout + navigate to login). On web uses `window.confirm` (since `Alert.alert` is a no-op there); native uses `Alert.alert` with a destructive action.
- **`resetPwForm()`** — clears the password form/state.
- **`handleChangePassword()`** — validate (all fields, ≥6, match); `api.changePassword`; on success reset form + set `pwSuccess`; errors → `pwError`; toggles `pwSubmitting`.
- **`handleSaveGoal()`** — `parseInt(draftGoal)`; validate 1–200 (Alert on invalid); `api.updateMe({daily_goal})` → `refreshUser()` → exit editing.
- Render: user card (gradient avatar from first initial), 4-box stats grid, conditional upcoming-reviews list, conditional weak-words list, an editable daily-goal row (input + Save, or a pencil badge), a Security card (link → inline 3-field password form with Cancel/Update), and a logout button.
- **`StatBox({testID, icon, accent, value, label})`** — presentational stat tile.

### Standalone screens

**`lesson/[id].tsx` — `LessonDetailScreen()`**
- `id` from `useLocalSearchParams`. State: `lesson`, `loading`, `adding`.
- **`load()`** — guard on `id`; `api.lesson(id)`; `useEffect(load)`.
- **`handleAddAll()`** — collect ids of vocab not `in_deck`; if any, `addToDeck`; reload (so badges update). Toggles `adding`.
- **`handleAddOne(vocabId)`** — `addToDeck([id])`; **optimistically** flips that word's `in_deck` in local state.
- **`handleRemoveOne(vocabId)`** — `removeFromDeck`; optimistically flips back.
- `notInDeckCount` drives the "Add N to deck" / "All in deck" button. Renders loading/not-found states, then header, title/subtitle/description, the Add-all + Drills CTAs, the dialogue (filtered into Part 1/2 with a per-part card), grammar cards, and the vocab list (each row: hanzi, tone-colored pinyin, English, and an in-deck/add toggle).

**`drill.tsx` — `DrillScreen()`** (speaking drills with hints)
- `lesson` param decides whether to skip the picker. State: `selectedLesson`, `lessonOptions`, `drills`, `index`, `loading`, `done`, `sessionStats`, `hintLevel` (0/1/2), plus the full audio stack (`recorder`, `permission`, `recording`, `uploading`, `result`, `errorMsg`).
- **`useEffect` (mount)** — configure audio + read mic permission.
- **`useEffect` ([selectedLesson])** — with a `cancelled` guard: if no lesson selected, load the lesson picker list; else load that lesson's drills. The cancel flag prevents setting state after unmount/switch.
- **`startLesson(n)`** — reset session + card, set `selectedLesson`.
- **`resetCard()`** — clears hint/result/error/recording/uploading between drills.
- **`handleNext()`** — advance index or mark done; reset card.
- **`requestPermission()` / `startRec()`** — same mic flow as SpeakingCard.
- **`stopAndCheck()`** — stop; guard uri; `setUploading`; `api.transcribeAudio(uri, current.expected_answer)`; build feedback `{correct, score, feedback, transcribed, spokenPinyin, tonesWrong}`; update session stats; log `api.drillAttempt(current.id, transcribed, isCorrect)` (errors swallowed); errors → `errorMsg`.
- Render branches: loading; **lesson picker** (when `selectedLesson==null`) listing lessons; no-drills empty state; done summary; else the active drill — progress header, drill-type label, prompt card ("Say this in Mandarin" + English target + instruction), a **hint block** (tier 1 reveals characters, tier 2 reveals tone-colored pinyin; a button advances the tier), blocked-mic/error/result panels (result shows target-vs-heard, score, and which hint tier was used), and a footer state machine (record / stop / transcribing / next-or-finish).

**`speak-practice.tsx` — `SpeakPracticeScreen()`** (single sentence)
- Params `chinese/pinyin/english`. State: `revealed`, plus the audio stack.
- **`useEffect` mount** — audio mode + permission read.
- **`requestPermission()`** (`useCallback`) — request mic, set state, return bool.
- **`handleStartRecording()`** — clear error/result; ensure permission; prepare + record.
- **`handleStopAndUpload()`** — guard `recording`; stop; guard uri; upload `api.transcribeAudio(uri, target)`; set `result`; errors handled.
- **`handleReset()`** — clear result/error and re-hide the answer.
- **`renderRecordButton()`** — returns the uploading spinner, the active "stop" button (with dot), or the idle "Tap to record" button depending on state.
- Render: a target card that **hides the Mandarin** behind a "Show Mandarin" reveal (so you produce it from English), blocked-mic/error panels, and a result panel (score bar + %, tones-wrong note, target-vs-heard with tone-colored pinyin). Footer: Try-again / Next when there's a result, else the record button (+ a web-only mic hint).

**`library.tsx` — `LibraryScreen()`**
- State: `items`, `loading`, `query`, `filter` ('all'|'npcr'|'custom'), `selected` (Set), `submitting`.
- **`load()`** — `api.library({q, source})` (`'all'` → undefined source); `useFocusEffect`.
- **`toggleSelect(id)`** — add/remove from the multi-select set.
- **`handleAddSelected()`** — guard empty; `addToDeck(Array.from(selected))`; clear selection; reload; show platform-aware "N words added" (web `window.alert`, native `Alert.alert`); errors via Alert; toggles `submitting`.
- **`handleAddSingle(id)`** — `addToDeck([id])`; optimistically set that row `in_deck`.
- **`handleRemove(id)`** — `removeFromDeck`; optimistically unset.
- **`deleteCustom(id)`** — `deleteCustomVocab`; remove from `items` and from `selected`; errors via Alert.
- **`handleDelete(item)`** — confirmation wrapper: web `window.confirm`, native `Alert.alert` with destructive action → calls `deleteCustom`.
- Render: header (back, title, add-custom button), a search row (submit/clear), filter chips, the `FlatList` (rows show hanzi/pinyin/English, an L-number or "Custom" pill, a delete button for customs, and an in-deck/selected/add control; tapping a non-deck row toggles selection), an empty state, and a floating bulk-add bar shown when `selected.size > 0`.

**`add-word.tsx` — `AddWordScreen()`**
- State: the six field values, `error`, `saving`.
- **`handleSave()`** — require simplified/pinyin/english; `setSaving`; `api.createCustomVocab({...trimmed, optional examples or undefined})` (backend auto-adds to deck); `router.back()`; errors → `error`; `finally` clear saving.
- **`Section({title, children})`** and **`Field({label, required, children})`** — small layout helpers (the latter renders a red `*` for required fields).
- Render: header, intro note, Required section (3 inputs), optional Example section (3 inputs), error box, and a sticky "Save & Add to Deck" footer button.

---
---

# PART 3 — HOW EVERYTHING CONNECTS

This section traces the wiring — how a tap in the UI becomes a database write and back, how the pieces depend on each other, and how the data model threads through the whole system. Where the previous sections described parts in isolation, this one is about the seams between them.

## 1. The two halves and the contract between them

There are exactly **two processes** and **one contract**:

- The **Expo app** (frontend) runs on the phone/browser.
- The **FastAPI server** (backend) runs on your machine, talking to MongoDB.
- The contract is the **`/api` HTTP surface**, and on the client side it is funneled through a single file: `client.ts`.

Nothing in the UI ever calls `fetch` directly except `client.ts`. Every screen imports the `api` object and calls a typed method. This is the chokepoint that makes the whole system tractable: the base URL (`EXPO_PUBLIC_BACKEND_URL`), the `/api` prefix, JSON encoding, bearer-token injection, and error unwrapping all live in `request<T>()`. On the server side, the mirror chokepoint is `main.py`, which mounts every router under the same `/api` prefix. So the client's `request('/auth/login', …)` and the server's `APIRouter(prefix="/api") + router(prefix="/auth")` are two ends of the same wire.

```
Screen → api.X() → request<T>() → fetch(BASE_URL/api/...)
                                      → FastAPI APIRouter(/api)
                                      → module.router(/resource)
                                      → handler(Depends(get_current_user))
                                      → Motor → MongoDB
```

## 2. Authentication is the connective tissue

Auth is what links *every* request to *a* user, and it's woven through four layers that hand off to each other:

1. **Storage layer** — the JWT lives in secure storage under `mandarin_auth_token`, written by `setAuthToken` and read by `getToken`. On native that's the Keychain (`storage/index.ts`); on web it falls back to AsyncStorage (`storage/index.web.ts`). Metro picks the file by platform, so the rest of the app just imports `storage` and never knows the difference.

2. **Context layer** — `AuthProvider` is the in-memory mirror of that token. On mount it reads the token and calls `api.me()` to rehydrate the `user`. `login/signup/resetPassword` all follow the same shape: call the API, store the returned token, set the user. This means the token in storage and the `user` in React state are kept in lockstep by exactly these methods.

3. **Transport layer** — `request()` reads the token on *every* call and sets `Authorization: Bearer`. The screens never attach the token themselves; it's automatic because storage is the single source of truth.

4. **Server layer** — `get_current_user` is a FastAPI dependency injected into every protected handler via `Depends(...)`. It decodes the JWT, looks up the user (minus the password hash), and either returns the user dict or raises 401. Because it's a dependency, every router method that lists `current_user: dict = Depends(get_current_user)` is automatically gated — there's no per-route auth code.

The loop closes visibly in the UI through the **route guard**. `ProtectedRoutes` watches `user` + `loading` from the context and the current route `segments`. No user + not on an auth screen → redirect to login. Has user + sitting on an auth screen → redirect to tabs. So an expired token causes `api.me()` to 401 → context clears the user → the guard bounces you to login. The same `user` value drives both navigation and data access.

**One concrete trace (login):**
```
LoginScreen.onSubmit()
  → useAuth().login(email, password)
    → api.login() → POST /api/auth/login
      → routers/auth.login(): verify_password, update streak, create_access_token
    ← { access_token, user }
  → setAuthToken(token)  (storage)
  → setUser(user)        (context state)
→ router.replace('/(tabs)')   (and ProtectedRoutes now permits it)
```
Notice the streak is computed *on login* in `login()` using `last_active_date`, so the very act of authenticating is also a daily-engagement event. That streak then surfaces on the Home dashboard and Profile — connected purely through the `users` document.

## 3. Navigation wiring (how screens reach each other)

Routing is file-based via Expo Router, and the file tree *is* the navigation graph:

- `app/_layout.tsx` is the root: it installs the providers (`GestureHandlerRootView → SafeAreaProvider → AuthProvider`) and the guard, then declares the stack (`(auth)`, `(tabs)`, and the three pushed screens `lesson/[id]`, `drill`, `speak-practice`).
- `(tabs)/_layout.tsx` defines the five-tab bar. Tabs are siblings; you switch between them.
- The **standalone screens** (`library`, `add-word`, `drill`, `speak-practice`, `lesson/[id]`) are pushed *over* the tabs with `router.push(...)`, and they pass data forward two ways:
  - **By id in the path:** `lesson/[id].tsx` reads `useLocalSearchParams().id` and refetches.
  - **By params object:** `speak.tsx` pushes `{ pathname: '/speak-practice', params: { chinese, pinyin, english } }`, and the destination reads them with `useLocalSearchParams`. This is why speaking practice doesn't need a vocab id — the sentence travels in the navigation params.

The other connective trick is `useFocusEffect`. Home, Lessons, Speak, Review, Profile, and Library all reload **on focus**, not just on mount. So when you finish a review and navigate back to Home, the dashboard counts are already refreshed — the screens don't message each other; they all independently re-pull from the server, which is the shared state.

## 4. The data model is linked by UUIDs, not Mongo `_id`

Every document carries an app-generated `id` (a `uuid4()` string), and **all cross-references use that `id`**, never Mongo's `_id` (which is consistently projected out with `{_id: 0}`). This is the glue of the whole database. The relationships:

```
lessons.id ──< vocabulary.lesson_id
lessons.vocabulary_ids[] ──> vocabulary.id        (denormalized list)

users.id ──< user_deck.user_id
          ──< flashcards.user_id
          ──< review_history.user_id
          ──< drill_attempts / speaking_attempts / writing_attempts.user_id

vocabulary.id ──< user_deck.vocabulary_id
              ──< flashcards.vocabulary_id
              ──< review_history.vocabulary_id

vocabulary.created_by ──> users.id   (custom words only; null/absent for NPCR)
```

Two compound **unique indexes** (`db.create_indexes`) enforce the most important invariants in the schema rather than in app logic: one flashcard per `(user_id, vocabulary_id)` and one deck row per `(user_id, vocabulary_id)`. That's why `add_to_deck` can safely "skip if exists" and why a double-tap can't create duplicates.

The `created_by` field is the discriminator that fuses NPCR and custom vocabulary into one collection: a word is "custom" iff `created_by == current_user` (and `lesson_number == null`). The library query in `vocabulary_library` leans entirely on this — its `source is None` branch builds an `$or` of "any NPCR word OR my own customs," which is how one endpoint serves the All/NPCR/Custom filter chips on `library.tsx`.

## 5. The central spine: Deck → Flashcard → Review → SRS

This is the loop the entire app orbits. Each stage is a different collection, and the transitions between them are specific endpoints:

```
            add_to_deck                first review (submit_review)
 vocabulary ───────────► user_deck ───────────────────────► flashcards
                            │                                    │
                            │ get_new_flashcards                 │ get_due_flashcards
                            │ (deck words w/ no card yet)        │ (next_review_at <= now)
                            ▼                                    ▼
                       ┌──────────────── Review queue ──────────────┐
                       │  buildMultiModeQueue(due, new)             │
                       └────────────────────────────────────────────┘
```

The seam between "new" and "due" is subtle and important. A word in your deck with **no flashcard yet** is *new*; the first `submit_review` *creates* the flashcard (stage 1 or 2). After that it's *due* whenever `next_review_at <= now`. So `get_new_flashcards` computes `deck_ids − existing_flashcard_ids`, and the dashboard's `new_count` uses the exact same set difference — the two stay consistent because they implement the same definition.

The **review session** is where the most logic-per-tap lives, and it spans client and server in a deliberate split:

- The **client** owns *session structure*. `buildMultiModeQueue` assigns each word all three modes (reading/writing/speaking) across three rounds. `handleAnswered` accumulates per-word results in `cardModeResults`.
- The **server** owns *SRS state*. But it's told *when* to act via two flags on the same endpoint:
  - Non-final modes call `reviewFlashcardWithMode(..., skip_srs=true)` → `submit_review` only logs `review_history`, leaving the stage untouched.
  - The final (3rd) mode aggregates `≥2/3 correct` on the client, then calls with `skip_srs=false` → `submit_review` advances the stage **once** and recomputes `next_review_at` from `SRS_INTERVALS`.

So a single word answered three times produces **three `review_history` rows but exactly one SRS transition**. That division — client decides cadence, server decides scheduling — is the key architectural connection in the review feature. The `mode` field travels the whole way (client `MODE_META` → request body → `FlashcardReviewRequest.mode` → the history row), so even skipped-SRS answers are attributable per modality.

The loop's feedback surfaces back through aggregation endpoints that read the *same* collections the loop writes: `get_dashboard` and `get_stats` count `flashcards` (by `current_stage`) and `review_history` (by `was_correct`/`timestamp`), and `get_review_schedule` buckets `flashcards.next_review_at`. The Profile's "weak words" come from `flashcards` where `incorrect_count > correct_count` — fields that `submit_review` maintains. Nothing computes progress separately; it's all derived from the spine's own writes.

## 6. The three AI graders, and how they plug into the same UI shape

Speaking, writing, and reading each have a grader, and they connect to the UI through a **common result shape** so the review cards can stay uniform:

- **Speaking** → `transcribe_audio` → `asr.transcribe` (FunASR, run in a threadpool so it doesn't block the event loop) → `score_pronunciation` → returns `{correct, score, feedback, target_pinyin, spoken_pinyin, tones_wrong, …}`. Used by `SpeakingCard`, `drill.tsx`, and `speak-practice.tsx` — three different screens, one endpoint, because `transcribeAudio` is generic over "what's the target text."
- **Writing** → `recognize_handwriting` → EasyOCR → bag-of-characters `_ocr_score` → `{correct, score, identity_score, …}`. The image originates in `HandwritingCanvas.captureBase64` (a 512×512 PNG snapshot of SVG strokes) and is consumed by `WritingCard`.
- **Reading** → tried *locally first* via `englishMatches`, then escalated to the server's `answer_matches_target` (WordNet).

That reading path is the clearest example of **deliberate logic duplication for latency**: `englishMatches` (client) and `answer_matches_target` (server) implement the *same* normalization rules (strip articles, split on `;,/`/"or"). The client version catches the easy exact/variant matches instantly with no round-trip; only genuine synonym questions ("glad" vs "happy") fall through to the WordNet call. The two must stay in sync semantically, and they do because they were written as mirrors.

All three graders **log to their own attempt collections** (`speaking_attempts`, `writing_attempts`, `drill_attempts`) in addition to (for review) the SRS write. Those attempt logs are write-mostly today — `get_stats` reads `speaking_attempts` count — but they're the audit trail that connects raw practice to the spine.

The audio flow has its own resilience seam worth calling out: `expo-audio`'s `stop()` can resolve before the file is flushed, so the cards wait ~250ms *and* `transcribeAudio` retries transient network failures up to 3× while never retrying real 4xx/5xx. The client-side delay and the client-side retry are two cooperating guards around the same OS-level race.

## 7. How seed data becomes user-specific state

The curriculum and the user's progress are connected by a one-way fan-out at the `id` level:

```
seed_data.NPCR_LESSONS  (static Python)
   │  seed_lessons_and_vocab()  (startup, idempotent)
   ▼
lessons + vocabulary  (shared, read-only to users)
   │  user taps "Add" in lesson/[id].tsx or library.tsx → addToDeck
   ▼
user_deck  (per user)
   │  first review → submit_review
   ▼
flashcards + review_history  (per user, the SRS state)
```

`seed_lessons_and_vocab` is the bridge from static content to live documents, and its idempotency is what makes the connection safe across restarts: it skips if the count matches, and reseeds *only content collections* if you change the lesson count — user data (`user_deck`, `flashcards`, `users`) is never touched. `migrate_legacy_decks` patches an older break in this chain (flashcards that predate explicit deck rows) by reconstructing `user_deck` from `flashcards`.

The Speak tab shows the *other* use of the same seed content: it reads `lesson.dialogue` (not vocabulary) and reshapes it into practice sentences entirely client-side in `load()`. So one `lessons` document feeds two unrelated features — vocabulary drilling and sentence pronunciation — through different fields.

## 8. Startup ordering: why the sequence matters

The connections have a required boot order, encoded in `on_startup`:

```
create_indexes()          # unique constraints must exist before…
→ seed_lessons_and_vocab() # …content is inserted (so dupes can't sneak in), and before…
→ migrate_legacy_decks()   # …migration, which reads flashcards/deck that seeding assumes exist
→ asr.warm_up()            # load FunASR now so the first /speaking call isn't a cold-start
```

Each step depends on the previous. If indexes came after seeding, a re-seed could create duplicate vocab; if migration ran before the collections were guaranteed, it would no-op. `warm_up` is the connection between *server start* and *acceptable first-request latency* — without it, the first learner to hit Speak would pay the multi-second model load.

## 9. Cross-cutting glue (the small connectors)

A few utilities quietly tie distant parts together:

- **`getToneColor`** (`theme.ts`) is called by *every* screen that renders pinyin (lessons, review cards, speak, drills, library), turning the server's `pinyin` strings into consistent tone coloring. The backend's `pinyin_display` produces those strings; the frontend colors them. Pronunciation "meaning" thus flows from `pypinyin` (server) to a color (client) without either side knowing the other's internals.
- **Platform splits** (`storage/index.ts` vs `.web.ts`, `useIconFonts` Expo-Go-vs-build branch) are connectors between "one codebase" and "three runtimes." They let every other file stay platform-agnostic.
- **`testID` props** thread through nearly every interactive element, connecting the UI to an external e2e test harness — a parallel "API" for automation that mirrors the user-facing one.
- **`PressableScale`** is imported by the high-traffic screens (Home tiles, auth buttons, lesson cards) to give a uniform press feel — a shared interaction connector rather than a data one.

## 10. One end-to-end trace through the whole stack

To see all the seams at once, here is "add a word from a lesson, then review it correctly three times":

```
1. lesson/[id].tsx: handleAddOne(vid)
   → api.addToDeck([vid]) → POST /api/deck/add
     → deck.add_to_deck: get_current_user (JWT), insert user_deck row (unique index guards dupes)
   → optimistic local flip: v.in_deck = true

2. Later, Review tab focus → ReviewScreen.loadQueue()
   → Promise.all(dueFlashcards, newFlashcards, deck)
     → flashcards.get_new_flashcards: deck_ids − existing_flashcards = [vid]  (it's "new")
   → buildMultiModeQueue([], [vid-vocab]) → 3 cards (reading, writing, speaking), one per round

3. Round 1 (say reading): ReadingCard.handleCheck → englishMatches passes locally (no server call)
   → onAnswered(vid, true, 'reading')
   → reviewFlashcardWithMode(vid, true, 'reading', undefined, skip_srs=true)
     → submit_review: skip_srs branch → logs history only (if a card exists)
   cardModeResults[vid] = [{reading, true}]

4. Round 2 (writing): canvas → captureBase64 → api.recognizeHandwriting → EasyOCR score
   → onAnswered(vid, true, 'writing') with skip_srs=true → history-style log
   cardModeResults[vid] = [..., {writing, true}]

5. Round 3 (speaking, isFinal): record → transcribeAudio → FunASR + score_pronunciation
   → handleAnswered sees isFinal → aggregate ≥2/3 correct = true
   → reviewFlashcardWithMode(vid, true, 'speaking')   // skip_srs=false
     → submit_review: creates/advances flashcard → new_stage, next_review_at = now + SRS_INTERVALS[stage]
   → reviewSummary gets {vocab, new_stage, next_review_at}; done screen shows formatNextReview(...)

6. Back to Home (focus) → api.dashboard()
   → progress.get_dashboard: counts the freshly-written flashcard + today's review_history rows
   → progress bar animates to the new percent
```

Every arrow in that trace is one of the connections described above: the API chokepoint, the auth dependency, the unique-index invariant, the deck→new→due transition, the client/server SRS split, the three graders sharing a result shape, and the focus-driven re-pull that keeps independent screens consistent without ever talking to each other directly.

---

*End of guide.*
