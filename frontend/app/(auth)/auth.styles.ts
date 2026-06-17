// Shared styles for the three auth screens (login / signup / forgot-password).
// They are visually near-identical; the only real differences are the accent
// color and a little brand-block sizing, captured as factory options.
import { StyleSheet } from 'react-native';
import { colors, spacing, radius, fontSize, shadows } from '@/src/theme';

export type AuthStyleOptions = {
  /** Accent for watermark, focused inputs, and footer links (primary or secondary). */
  accent: string;
  /** Glow color for the brand badge and primary button. */
  glow: string;
  /** Brand badge width (height is fixed). */
  badgeWidth: number;
  /** Brand badge hanzi size. */
  hanziSize: number;
  /** Brand title font size + tracking. */
  titleSize: number;
  titleLetterSpacing: number;
  /** Spacing below the brand block. */
  brandMarginBottom: number;
};

export function makeAuthStyles(o: AuthStyleOptions) {
  return StyleSheet.create({
    safe: { flex: 1, backgroundColor: colors.background },
    flex: { flex: 1 },
    scroll: { flexGrow: 1, padding: spacing.lg, justifyContent: 'center' },
    watermark: {
      position: 'absolute',
      top: 0,
      right: -24,
      fontSize: 150,
      fontWeight: '700',
      color: o.accent,
      opacity: 0.05,
    },
    brandBlock: { alignItems: 'center', marginBottom: o.brandMarginBottom },
    brandBadge: {
      width: o.badgeWidth,
      height: 96,
      borderRadius: radius.xl,
      alignItems: 'center',
      justifyContent: 'center',
      marginBottom: spacing.lg,
      ...shadows.glow(o.glow),
    },
    brandHanzi: { fontSize: o.hanziSize, color: '#fff', fontWeight: '700' },
    brandTitle: {
      fontSize: o.titleSize,
      fontWeight: '700',
      color: colors.textPrimary,
      letterSpacing: o.titleLetterSpacing,
    },
    brandSubtitle: {
      fontSize: fontSize.base,
      color: colors.textSecondary,
      textAlign: 'center',
      marginTop: spacing.sm,
      lineHeight: 22,
      paddingHorizontal: spacing.lg,
    },
    form: { gap: spacing.xs },
    label: {
      fontSize: fontSize.sm,
      color: colors.textSecondary,
      marginTop: spacing.md,
      marginBottom: spacing.xs,
      fontWeight: '600',
    },
    input: {
      backgroundColor: colors.surface,
      borderWidth: 1.5,
      borderColor: colors.border,
      borderRadius: radius.md,
      paddingHorizontal: spacing.md,
      paddingVertical: 14,
      fontSize: fontSize.lg,
      color: colors.textPrimary,
      minHeight: 48,
    },
    inputFocused: { borderColor: o.accent, ...shadows.sm },
    error: {
      color: colors.error,
      fontSize: fontSize.sm,
      marginTop: spacing.md,
      backgroundColor: colors.errorLight,
      padding: spacing.md,
      borderRadius: radius.md,
    },
    // Reset-code notice (forgot-password only).
    notice: {
      fontSize: fontSize.sm,
      color: colors.textSecondary,
      backgroundColor: colors.primaryLight,
      padding: spacing.md,
      borderRadius: radius.md,
      lineHeight: 20,
      marginBottom: spacing.xs,
    },
    // Forgot-password link (login only).
    forgotWrap: { alignSelf: 'flex-end', marginTop: spacing.sm, paddingVertical: spacing.xs },
    forgotLink: { color: o.accent, fontSize: fontSize.sm, fontWeight: '600' },
    btnWrap: { marginTop: spacing.xl, borderRadius: radius.md },
    primaryBtn: {
      borderRadius: radius.md,
      paddingVertical: 16,
      alignItems: 'center',
      minHeight: 52,
      justifyContent: 'center',
      ...shadows.glow(o.glow),
    },
    primaryBtnText: { color: '#fff', fontSize: fontSize.lg, fontWeight: '700' },
    btnDisabled: { opacity: 0.7 },
    footer: { flexDirection: 'row', justifyContent: 'center', marginTop: spacing.xl },
    footerText: { color: colors.textSecondary, fontSize: fontSize.base },
    footerLink: { color: o.accent, fontSize: fontSize.base, fontWeight: '700' },
  });
}
