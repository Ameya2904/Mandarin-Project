/**
 * Design tokens for the Mandarin learning app.
 * Source: /app/design_guidelines.json — Organic & Earthy, evolved into a
 * brighter, multi-accent palette while keeping green as the brand anchor.
 */

export const colors = {
  primary: '#3E9D6B',
  primaryDark: '#2E7E54',
  primaryLight: '#E2F4EA',
  secondary: '#7C53E0',
  background: '#F7F6F2',
  surface: '#FFFFFF',
  surfaceAlt: '#F1EFE8',
  textPrimary: '#1B1D1C',
  textSecondary: '#62655F',
  textTertiary: '#9A9D96',
  border: '#E7E4DB',
  borderStrong: '#CDC9BD',
  success: '#2E9E5B',
  successLight: '#E2F4EA',
  error: '#E0567E',
  errorLight: '#FCE6EC',
  warning: '#E8932B',
  warningLight: '#FCEFD9',

  // Tone colors for pinyin
  tone1: '#E0567E',
  tone2: '#E8932B',
  tone3: '#2E9E5B',
  tone4: '#2F6FED',
  tone0: '#9A9D96',
};

/**
 * Vibrant accent palette. Each accent has a saturated `base` (icons, numbers,
 * accents) and a `soft` tint used as a chip/background fill behind it.
 */
export const accents = {
  green: { base: '#2E9E5B', soft: '#E2F4EA' },
  blue: { base: '#2F6FED', soft: '#E5EDFD' },
  violet: { base: '#7C53E0', soft: '#EDE8FB' },
  amber: { base: '#E8932B', soft: '#FCEFD9' },
  rose: { base: '#E0567E', soft: '#FCE6EC' },
  teal: { base: '#1FA8A0', soft: '#DEF4F2' },
};

export type AccentName = keyof typeof accents;

// Stable ordered list for cycling accents across lists (lessons, etc.)
export const accentCycle: AccentName[] = ['green', 'blue', 'violet', 'amber', 'rose', 'teal'];

/** Linear-gradient color stops (use with expo-linear-gradient). */
export const gradients = {
  hero: ['#2E9E5B', '#1FA8A0'] as const, // green → teal, the primary CTA
  violet: ['#7C53E0', '#5B7CF0'] as const,
  amber: ['#F0A93C', '#E0567E'] as const, // streak / celebration
  surface: ['#FFFFFF', '#F7F6F2'] as const,
};

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};

export const radius = {
  sm: 8,
  md: 12,
  lg: 16,
  xl: 24,
  full: 999,
};

export const fontSize = {
  xs: 12,
  sm: 13,
  base: 15,
  lg: 17,
  xl: 20,
  xxl: 24,
  display: 32,
  hanzi: 56,
  hanziLg: 72,
};

export const shadows = {
  sm: {
    shadowColor: '#1B1D1C',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 4,
    elevation: 2,
  },
  md: {
    shadowColor: '#1B1D1C',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 12,
    elevation: 4,
  },
  lg: {
    shadowColor: '#1B1D1C',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.14,
    shadowRadius: 22,
    elevation: 8,
  },
  /** Colored glow for vibrant CTAs — pass the accent base color. */
  glow: (color: string) => ({
    shadowColor: color,
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.32,
    shadowRadius: 16,
    elevation: 6,
  }),
};

/**
 * Get tone color based on the diacritic mark of a pinyin syllable.
 * Returns the color for the first tone-marked vowel found.
 */
export function getToneColor(pinyin: string): string {
  if (!pinyin) return colors.tone0;
  const tone1Chars = 'āēīōūǖĀĒĪŌŪǕ';
  const tone2Chars = 'áéíóúǘÁÉÍÓÚǗ';
  const tone3Chars = 'ǎěǐǒǔǚǍĚǏǑǓǙ';
  const tone4Chars = 'àèìòùǜÀÈÌÒÙǛ';

  for (const ch of pinyin) {
    if (tone1Chars.includes(ch)) return colors.tone1;
    if (tone2Chars.includes(ch)) return colors.tone2;
    if (tone3Chars.includes(ch)) return colors.tone3;
    if (tone4Chars.includes(ch)) return colors.tone4;
  }
  return colors.tone0;
}
