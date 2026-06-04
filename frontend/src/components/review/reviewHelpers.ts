import { Ionicons } from '@expo/vector-icons';
import type { Flashcard, Vocabulary } from '@/src/api/client';
import type { Card, Mode } from './types';

export const STAGE_LABELS: Record<number, string> = {
  1: 'Stage 1 · 1 day',
  2: 'Stage 2 · 2 days',
  3: 'Stage 3 · 1 week',
  4: 'Stage 4 · 1 month',
  5: 'Stage 5 · 3 months',
  6: 'Stage 6 · 1 year',
};

export const MODE_META: Record<
  Mode,
  { label: string; icon: keyof typeof Ionicons.glyphMap; description: string }
> = {
  reading: { label: 'Reading', icon: 'book-outline', description: 'Type the English meaning' },
  writing: { label: 'Writing', icon: 'brush-outline', description: 'Handwrite the Chinese characters' },
  speaking: { label: 'Speaking', icon: 'mic-outline', description: 'Say the Chinese aloud' },
};

export const MODES: Mode[] = ['reading', 'writing', 'speaking'];

export function shuffleArray<T>(arr: T[]): T[] {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

export function buildMultiModeQueue(dueCards: Flashcard[], newVocab: Vocabulary[]): Card[] {
  const entries = [
    ...dueCards.map((c) => ({ vocabulary: c.vocabulary, current_stage: c.current_stage })),
    ...newVocab.map((v) => ({ vocabulary: v, current_stage: null })),
  ];
  if (entries.length === 0) return [];

  // For each card assign 3 shuffled modes, one per round
  const rounds: Card[][] = [[], [], []];
  entries.forEach((entry) => {
    const modes = shuffleArray([...MODES] as Mode[]);
    modes.forEach((mode, roundIdx) => {
      rounds[roundIdx].push({
        vocabulary: entry.vocabulary,
        current_stage: entry.current_stage,
        mode,
        round: roundIdx,
        isFinal: roundIdx === 2,
      });
    });
  });

  // Shuffle within each round so same card doesn't follow itself across rounds
  rounds.forEach((r) => shuffleArray(r));
  return [...rounds[0], ...rounds[1], ...rounds[2]];
}

export function formatNextReview(isoDate: string): string {
  const diffDays = Math.round((new Date(isoDate).getTime() - Date.now()) / 86_400_000);
  if (diffDays <= 1) return 'tomorrow';
  if (diffDays < 7) return `in ${diffDays} days`;
  if (diffDays < 14) return 'in 1 week';
  if (diffDays < 30) return `in ${Math.round(diffDays / 7)} weeks`;
  if (diffDays < 60) return 'in 1 month';
  if (diffDays < 365) return `in ${Math.round(diffDays / 30)} months`;
  return 'in 1 year';
}

function normalize(text: string): string {
  return (text || '').trim().toLowerCase();
}

export function englishMatches(answer: string, target: string): boolean {
  const a = normalize(answer).replace(/[.;]+$/, '');
  // Allow any of the semicolon/comma-separated meanings
  const parts = target
    .split(/[;,/]|\bor\b/)
    .map((s) => normalize(s).replace(/^(to |a |an |the )/, '').trim())
    .filter(Boolean);
  const cleaned = a.replace(/^(to |a |an |the )/, '').trim();
  return parts.some((p) => p === cleaned || cleaned === p.replace(/[.;]+$/, ''));
}
