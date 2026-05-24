/**
 * Design tokens for the Mandarin learning app.
 * Source: /app/design_guidelines.json — Organic & Earthy, calm focus.
 */

export const colors = {
  primary: '#4A7C59',
  primaryDark: '#3A6346',
  primaryLight: '#E8F0EA',
  secondary: '#C0392B',
  background: '#FDFCF9',
  surface: '#FFFFFF',
  surfaceAlt: '#F5F3EC',
  textPrimary: '#1C1C1E',
  textSecondary: '#6C6C70',
  textTertiary: '#9C9C9F',
  border: '#E5E2D9',
  borderStrong: '#C9C5B8',
  success: '#5C8A65',
  successLight: '#EAF3EC',
  error: '#C0392B',
  errorLight: '#FBEAE8',
  warning: '#D4A017',

  // Tone colors for pinyin
  tone1: '#D9534F',
  tone2: '#D4A017',
  tone3: '#5C8A65',
  tone4: '#4A6C8C',
  tone0: '#8A8A8E',
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
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.04,
    shadowRadius: 2,
    elevation: 1,
  },
  md: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 6,
    elevation: 2,
  },
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
