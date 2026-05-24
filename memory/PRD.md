# Mandarin Learning App - Product Requirements

## Vision
Help serious Mandarin learners move from passive recognition to active speaking and sentence construction through a structured, calm, focused mobile experience built on the NPCR curriculum.

## Phase 1 MVP (Complete)
1. **Auth System** — JWT-based signup/login with bcrypt password hashing
2. **Spaced Repetition Flashcards** — 6-stage SRS (1d, 2d, 1w, 1m, 3m, 1y) with correct/incorrect progression
3. **NPCR Lessons** — 5 lessons pre-seeded with vocabulary, dialogues, grammar notes
4. **Sentence Drills** — Substitution and transformation drills tied to lessons
5. **Speaking Practice** — Text-based pronunciation evaluation (audio capture deferred to Phase 2)
6. **Progress Tracking** — Streak, retention rate, mastered count, weak words
7. **Home Dashboard** — Daily progress, due reviews, quick action tiles
8. **Profile/Settings** — Daily goal editing, logout

## Phase 2 (Future)
- Real audio recording with Whisper API integration
- Tone-specific feedback
- Adaptive scheduling based on response time
- More NPCR lessons (6-20+)
- Sentence reordering and expansion drills
- Dark mode theme

## Design Philosophy
Calm, focused, educational. Organic & Earthy palette: primary green #4A7C59, off-white background #FDFCF9, large readable hanzi. Avoid gamification overload.

## Tech Stack
- **Backend:** FastAPI + Motor (MongoDB async) + JWT auth + bcrypt
- **Frontend:** Expo React Native + Expo Router + React Native Safe Area
- **Database:** MongoDB (collections: users, lessons, vocabulary, flashcards, review_history, drills, drill_attempts, speaking_attempts)
