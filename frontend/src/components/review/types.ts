import type { Vocabulary } from '@/src/api/client';

export type Mode = 'reading' | 'writing' | 'speaking';

export type Card = {
  vocabulary: Vocabulary;
  current_stage: number | null;
  mode: Mode;
  round: number; // 0 | 1 | 2
  isFinal: boolean; // true when this is the card's 3rd and last mode in the session
};

export type OnAnswered = (vocabId: string, wasCorrect: boolean, mode: Mode) => void;

export type CharResult = {
  target: string;
  recognized: string;
  match: boolean;
  quality: number;
  notes: string;
};

export type WritingResult = {
  score: number;
  identity_score: number;
  quality_score: number;
  feedback: string;
  characters: CharResult[];
  recognized: string;
  passed: boolean;
};
