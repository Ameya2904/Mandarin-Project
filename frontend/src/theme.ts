/**
 * Design tokens for the Mandarin learning app.
 *
 * Direction: "Sophisticated Dark" — a deep charcoal canvas with layered
 * surfaces, a muted jade brand anchor, and a restrained multi-accent palette
 * (desaturated, no gradients-as-decoration, no colored glow). Elevation comes
 * from surface contrast and hairline borders rather than heavy shadows.
 *
 * The token *shape* is intentionally unchanged from the previous (light) theme
 * so existing screens keep working; only the values were retuned for dark.
 */

export const colors = {
  // `primary` is deep enough that white button labels stay legible on it; the
  // brighter jade lives in `accents.green` / `success` for text & icons on dark.
  primary: '#3E9C73',
  primaryDark: '#2E7E5C',
  primaryLight: '#16271F', // dark jade tint — used as a fill behind jade content
  secondary: '#8E78E0',
  background: '#0F1412', // near-black canvas, faint cool-green undertone
  surface: '#181F1C', // elevated card
  surfaceAlt: '#212925', // chips, progress tracks, insets
  textPrimary: '#EDEFEC',
  textSecondary: '#A2AAA4',
  textTertiary: '#6E766F',
  border: '#252D29', // hairline divider / card edge
  borderStrong: '#36413B',
  success: '#52B98C',
  successLight: '#16271F',
  error: '#E76E91',
  errorLight: '#2A1620',
  warning: '#E0A24B',
  warningLight: '#2A2012',

  /** Text/icon color that sits on top of a saturated accent fill. */
  onAccent: '#0F1412',

  // Tone colors for pinyin — brightened a touch for legibility on dark.
  tone1: '#F07A98',
  tone2: '#E8AB5C',
  tone3: '#5FC295',
  tone4: '#6F9DF2',
  tone0: '#8B938C',
};

/**
 * Muted accent palette. Each accent has a desaturated `base` (icons, numbers,
 * accents) and a dark `soft` tint used as a chip/background fill behind it —
 * the soft fill sits just above `surface` so the chip reads on a dark card.
 */
export const accents = {
  green: { base: '#52B98C', soft: '#16271F' },
  blue: { base: '#6F9DF2', soft: '#161F2C' },
  violet: { base: '#9E8AE6', soft: '#1F1B2C' },
  amber: { base: '#E0A24B', soft: '#271F12' },
  rose: { base: '#E76E91', soft: '#281720' },
  teal: { base: '#4FC3B9', soft: '#13241F' },
};

export type AccentName = keyof typeof accents;

// Stable ordered list for cycling accents across lists (lessons, etc.)
export const accentCycle: AccentName[] = ['green', 'blue', 'violet', 'amber', 'rose', 'teal'];

/**
 * Linear-gradient color stops (use with expo-linear-gradient).
 *
 * Deliberately restrained: close-valued, deep two-stop blends so they read as a
 * solid, considered fill rather than a candy gradient. White/onAccent text sits
 * legibly on all of them.
 */
export const gradients = {
  hero: ['#3E9C73', '#2E8C84'] as const, // jade → teal, the primary CTA
  violet: ['#6E5BB6', '#54599E'] as const,
  amber: ['#C58A3C', '#B05C7E'] as const, // streak / celebration
  surface: ['#1B221F', '#101513'] as const,
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

/**
 * Shadows on a dark canvas barely register, so elevation is carried mostly by
 * surface contrast and the `hairline` border below. These stay subtle and
 * neutral — there is intentionally no colored "glow".
 */
export const shadows = {
  sm: {
    shadowColor: '#000000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
    elevation: 2,
  },
  md: {
    shadowColor: '#000000',
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.28,
    shadowRadius: 14,
    elevation: 5,
  },
  lg: {
    shadowColor: '#000000',
    shadowOffset: { width: 0, height: 12 },
    shadowOpacity: 0.36,
    shadowRadius: 24,
    elevation: 10,
  },
  /**
   * Formerly a colored glow; now a neutral elevation so existing call sites keep
   * working without the candy look. The `color` argument is ignored on purpose.
   */
  glow: (_color?: string) => ({
    shadowColor: '#000000',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.34,
    shadowRadius: 18,
    elevation: 7,
  }),
};

/**
 * Hairline border used to give cards a crisp edge on the dark canvas. Spread
 * onto card styles: `{ ...hairline }`.
 */
export const hairline = {
  borderWidth: 1,
  borderColor: colors.border,
} as const;

/** Convenience: a standard elevated card surface (surface + hairline + sm shadow). */
export const card = {
  backgroundColor: colors.surface,
  borderWidth: 1,
  borderColor: colors.border,
  ...shadows.sm,
} as const;

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
