/**
 * API client for the Mandarin learning backend.
 * All routes are prefixed with /api and use bearer token auth.
 */
import { storage } from '@/src/utils/storage';

const BASE_URL = process.env.EXPO_PUBLIC_BACKEND_URL || '';
const TOKEN_KEY = 'mandarin_auth_token';

export type Vocabulary = {
  id: string;
  lesson_id: string;
  lesson_number: number;
  simplified: string;
  traditional: string;
  pinyin: string;
  english: string;
  part_of_speech: string;
  example_chinese: string;
  example_pinyin: string;
  example_english: string;
};

export type Flashcard = {
  id: string;
  user_id: string;
  vocabulary_id: string;
  current_stage: number;
  next_review_at: string;
  correct_count: number;
  incorrect_count: number;
  vocabulary: Vocabulary;
};

export type Lesson = {
  id: string;
  lesson_number: number;
  title: string;
  subtitle: string;
  description: string;
  level: string;
  video_url: string;
  dialogue: { speaker: string; chinese: string; pinyin: string; english: string }[];
  grammar_notes: { title: string; explanation: string }[];
  vocabulary_count: number;
  vocabulary?: Vocabulary[];
  progress?: { mastered: number; started: number; total: number };
};

export type Drill = {
  id: string;
  lesson_number: number;
  drill_type: string;
  prompt_chinese: string;
  prompt_english: string;
  instruction_english: string;
  instruction_chinese: string;
  expected_answer: string;
  expected_pinyin: string;
  expected_english: string;
};

export type Dashboard = {
  due_count: number;
  new_count: number;
  total_cards: number;
  mastered_count: number;
  reviews_today: number;
  correct_today: number;
  daily_goal: number;
  streak_count: number;
  progress_percent: number;
};

export type UserPublic = {
  id: string;
  email: string;
  name: string;
  daily_goal: number;
  streak_count: number;
  created_at: string;
};

async function getToken(): Promise<string | null> {
  return storage.secureGet<string>(TOKEN_KEY, '');
}

export async function setAuthToken(token: string): Promise<void> {
  await storage.secureSet(TOKEN_KEY, token);
}

export async function clearAuthToken(): Promise<void> {
  await storage.secureRemove(TOKEN_KEY);
}

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const token = await getToken();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...((init.headers as Record<string, string>) || {}),
  };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(`${BASE_URL}/api${path}`, { ...init, headers });
  const text = await res.text();
  const data = text ? JSON.parse(text) : null;

  if (!res.ok) {
    const message = data?.detail || data?.message || `Request failed (${res.status})`;
    throw new Error(message);
  }
  return data as T;
}

// Auth
export const api = {
  signup: (email: string, password: string, name: string) =>
    request<{ access_token: string; user: UserPublic }>('/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ email, password, name }),
    }),
  login: (email: string, password: string) =>
    request<{ access_token: string; user: UserPublic }>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    }),
  me: () => request<UserPublic>('/auth/me'),
  updateMe: (payload: { name?: string; daily_goal?: number; learner_level?: string }) =>
    request<UserPublic>('/auth/me', { method: 'PUT', body: JSON.stringify(payload) }),
  forgotPassword: (email: string) =>
    request<{ reset_token: string; expires_in_minutes: number }>('/auth/forgot-password', {
      method: 'POST',
      body: JSON.stringify({ email }),
    }),
  resetPassword: (token: string, new_password: string) =>
    request<{ access_token: string; user: UserPublic }>('/auth/reset-password', {
      method: 'POST',
      body: JSON.stringify({ token, new_password }),
    }),
  changePassword: (current_password: string, new_password: string) =>
    request<{ success: boolean }>('/auth/change-password', {
      method: 'POST',
      body: JSON.stringify({ current_password, new_password }),
    }),

  dashboard: () => request<Dashboard>('/progress/dashboard'),
  stats: () =>
    request<{
      total_reviews: number;
      correct_reviews: number;
      retention_rate: number;
      mastered_count: number;
      learning_count: number;
      weak_words: { simplified: string; pinyin: string; english: string; correct: number; incorrect: number }[];
      speaking_attempts: number;
      streak_count: number;
    }>('/progress/stats'),

  lessons: () => request<Lesson[]>('/lessons'),
  lesson: (id: string) => request<Lesson>(`/lessons/${id}`),

  semanticMatch: (answer: string, target: string) =>
    request<{ match: boolean }>('/vocabulary/semantic-match', {
      method: 'POST',
      body: JSON.stringify({ answer, target }),
    }),

  dueFlashcards: (limit = 20) => request<Flashcard[]>(`/flashcards/due?limit=${limit}`),
  newFlashcards: (limit = 10, lessonId?: string) =>
    request<Vocabulary[]>(`/flashcards/new?limit=${limit}${lessonId ? `&lesson_id=${lessonId}` : ''}`),
  drills: (lessonNumber?: number) =>
    request<Drill[]>(`/drills${lessonNumber !== undefined ? `?lesson_number=${lessonNumber}` : ''}`),
  drillAttempt: (drill_id: string, user_answer: string, was_correct: boolean, response_time_ms?: number) =>
    request<{ success: boolean }>('/drills/attempt', {
      method: 'POST',
      body: JSON.stringify({ drill_id, user_answer, was_correct, response_time_ms }),
    }),

  // Deck management
  deck: () => request<any[]>('/deck'),
  addToDeck: (vocabulary_ids: string[]) =>
    request<{ added: number }>('/deck/add', { method: 'POST', body: JSON.stringify({ vocabulary_ids }) }),
  removeFromDeck: (vocabulary_id: string) =>
    request<{ removed: boolean }>(`/deck/${vocabulary_id}`, { method: 'DELETE' }),

  // Vocabulary library
  library: (params: { q?: string; lesson_number?: number; source?: 'npcr' | 'custom' } = {}) => {
    const search = new URLSearchParams();
    if (params.q) search.set('q', params.q);
    if (params.lesson_number !== undefined) search.set('lesson_number', String(params.lesson_number));
    if (params.source) search.set('source', params.source);
    const qs = search.toString();
    return request<(Vocabulary & { in_deck: boolean; is_custom: boolean })[]>(
      `/vocabulary/library${qs ? `?${qs}` : ''}`
    );
  },

  createCustomVocab: (payload: {
    simplified: string;
    pinyin: string;
    english: string;
    example_chinese?: string;
    example_pinyin?: string;
    example_english?: string;
  }) =>
    request<Vocabulary>('/vocabulary/custom', { method: 'POST', body: JSON.stringify(payload) }),

  deleteCustomVocab: (vocab_id: string) =>
    request<{ deleted: boolean }>(`/vocabulary/custom/${vocab_id}`, { method: 'DELETE' }),

  // Writing recognition
  recognizeHandwriting: (image_base64: string, target_chinese: string, vocabulary_id?: string) =>
    request<{
      correct: boolean;
      score: number;
      identity_score: number;
      quality_score: number;
      feedback: string;
      characters: {
        target: string;
        recognized: string;
        match: boolean;
        quality: number;
        notes: string;
      }[];
      recognized_text: string;
      target_text: string;
    }>('/writing/recognize', {
      method: 'POST',
      body: JSON.stringify({ image_base64, target_chinese, vocabulary_id }),
    }),

  reviewSchedule: (days = 14) =>
    request<{ date: string; count: number }[]>(`/flashcards/schedule?days=${days}`),

  reviewFlashcardWithMode: (
    vocabulary_id: string,
    was_correct: boolean,
    mode: 'reading' | 'writing' | 'speaking',
    response_time_ms?: number,
    skip_srs?: boolean,
  ) =>
    request<{ success: boolean; new_stage: number; next_review_at: string }>(
      '/flashcards/review',
      {
        method: 'POST',
        body: JSON.stringify({ vocabulary_id, was_correct, mode, response_time_ms, skip_srs }),
      },
    ),

  transcribeAudio: async (
    audioUri: string,
    target_chinese: string,
    vocabulary_id?: string,
  ): Promise<{
    transcribed_text: string;
    correct?: boolean;
    score?: number;
    feedback?: string;
    target_text?: string;
    target_pinyin?: string;
    spoken_pinyin?: string;
    tones_wrong?: number;
    syllables_right?: number;
    syllable_count?: number;
  }> => {
    const token = await getToken();
    const form = new FormData();
    const filename = audioUri.split('/').pop() || 'audio.m4a';
    const ext = (filename.split('.').pop() || 'm4a').toLowerCase();
    const typeMap: Record<string, string> = {
      m4a: 'audio/m4a',
      mp4: 'audio/mp4',
      wav: 'audio/wav',
      webm: 'audio/webm',
      mp3: 'audio/mpeg',
    };
    const mime = typeMap[ext] || 'audio/m4a';

    // Web: convert blob URL → Blob → File
    if (audioUri.startsWith('blob:') || audioUri.startsWith('data:')) {
      const blob = await (await fetch(audioUri)).blob();
      const file = new File([blob], filename, { type: mime });
      form.append('file', file);
    } else {
      // Native: append as { uri, name, type }
      form.append('file', { uri: audioUri, name: filename, type: mime } as any);
    }

    const url = `${BASE_URL}/api/speaking/transcribe?target_chinese=${encodeURIComponent(target_chinese)}${vocabulary_id ? `&vocabulary_id=${vocabulary_id}` : ''}`;
    const headers: Record<string, string> = { Accept: 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    // The recording file can be momentarily unreadable right after stop(),
    // which makes RN reject the upload with "Network request failed" before it
    // even reaches the server. Retry a few times with a short delay so the
    // now-flushed file uploads cleanly. Real server errors (4xx/5xx) are not
    // retried. TIMEOUT_MS guards against a genuinely hung request.
    const TIMEOUT_MS = 30000;
    const MAX_ATTEMPTS = 3;
    const RETRY_DELAY_MS = 400;
    let lastErr: unknown;
    for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
      try {
        const res = await fetch(url, {
          method: 'POST',
          body: form as any,
          headers,
          signal: controller.signal,
        });
        const text = await res.text();
        const data = text ? JSON.parse(text) : {};
        if (!res.ok) {
          // A real server error (e.g. 4xx/5xx) — don't retry, surface it.
          throw new Error(data?.detail || `Transcription failed (${res.status})`);
        }
        return data;
      } catch (err: any) {
        lastErr = err;
        // Only retry transient network/abort failures, not server errors.
        const isNetwork =
          err?.name === 'AbortError' ||
          /network request failed|network error/i.test(err?.message || '');
        if (!isNetwork || attempt === MAX_ATTEMPTS) throw err;
        await new Promise((r) => setTimeout(r, RETRY_DELAY_MS));
      } finally {
        clearTimeout(timer);
      }
    }
    throw lastErr;
  },
};
