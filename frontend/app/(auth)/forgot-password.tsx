import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  ActivityIndicator,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Link, useRouter } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient';
import Animated, { FadeInDown } from 'react-native-reanimated';
import { colors, spacing, radius, fontSize, shadows, accents, gradients } from '@/src/theme';
import PressableScale from '@/src/components/PressableScale';
import { api } from '@/src/api/client';
import { useAuth } from '@/src/contexts/AuthContext';

export default function ForgotPasswordScreen() {
  const router = useRouter();
  const { resetPassword } = useAuth();
  const [phase, setPhase] = useState<'request' | 'reset'>('request');
  const [email, setEmail] = useState('');
  const [code, setCode] = useState('');
  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [focused, setFocused] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  const requestCode = async () => {
    setError('');
    if (!email) {
      setError('Please enter your email.');
      return;
    }
    setSubmitting(true);
    try {
      const res = await api.forgotPassword(email.trim());
      // No mail service in this app, so the backend returns the code directly.
      setCode(res.reset_token);
      setPhase('reset');
    } catch (e: any) {
      setError(e.message || 'Could not send a reset code.');
    } finally {
      setSubmitting(false);
    }
  };

  const submitReset = async () => {
    setError('');
    if (!code || !password) {
      setError('Please fill in all fields.');
      return;
    }
    if (password.length < 6) {
      setError('Password must be at least 6 characters.');
      return;
    }
    if (password !== confirm) {
      setError('Passwords do not match.');
      return;
    }
    setSubmitting(true);
    try {
      await resetPassword(code.trim(), password);
      router.replace('/(tabs)');
    } catch (e: any) {
      setError(e.message || 'Could not reset your password.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <SafeAreaView style={styles.safe} edges={['top', 'bottom']}>
      <Text style={styles.watermark} pointerEvents="none">
        间隔
      </Text>
      <KeyboardAvoidingView
        style={styles.flex}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      >
        <ScrollView contentContainerStyle={styles.scroll} keyboardShouldPersistTaps="handled">
          <Animated.View entering={FadeInDown.duration(500)} style={styles.brandBlock}>
            <LinearGradient
              colors={gradients.hero}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 1 }}
              style={styles.brandBadge}
            >
              <Text style={styles.brandHanzi}>重置</Text>
            </LinearGradient>
            <Text style={styles.brandTitle}>Reset Password</Text>
            <Text style={styles.brandSubtitle}>
              {phase === 'request'
                ? 'Enter your email and we’ll generate a reset code for your account.'
                : 'Enter the reset code below along with your new password.'}
            </Text>
          </Animated.View>

          <Animated.View entering={FadeInDown.delay(120).duration(500)} style={styles.form}>
            {phase === 'request' ? (
              <>
                <Text style={styles.label}>Email</Text>
                <TextInput
                  testID="forgot-email-input"
                  style={[styles.input, focused === 'email' && styles.inputFocused]}
                  autoCapitalize="none"
                  autoCorrect={false}
                  keyboardType="email-address"
                  placeholder="you@example.com"
                  placeholderTextColor={colors.textTertiary}
                  value={email}
                  onChangeText={setEmail}
                  onFocus={() => setFocused('email')}
                  onBlur={() => setFocused(null)}
                />
              </>
            ) : (
              <>
                <Text style={styles.notice}>
                  A reset code was generated for {email.trim()}. In a production app it would be
                  emailed to you — for now it has been filled in below.
                </Text>

                <Text style={styles.label}>Reset code</Text>
                <TextInput
                  testID="forgot-code-input"
                  style={[styles.input, focused === 'code' && styles.inputFocused]}
                  autoCapitalize="none"
                  autoCorrect={false}
                  placeholder="Reset code"
                  placeholderTextColor={colors.textTertiary}
                  value={code}
                  onChangeText={setCode}
                  onFocus={() => setFocused('code')}
                  onBlur={() => setFocused(null)}
                />

                <Text style={styles.label}>New password</Text>
                <TextInput
                  testID="forgot-password-input"
                  style={[styles.input, focused === 'password' && styles.inputFocused]}
                  secureTextEntry
                  placeholder="At least 6 characters"
                  placeholderTextColor={colors.textTertiary}
                  value={password}
                  onChangeText={setPassword}
                  onFocus={() => setFocused('password')}
                  onBlur={() => setFocused(null)}
                />

                <Text style={styles.label}>Confirm new password</Text>
                <TextInput
                  testID="forgot-confirm-input"
                  style={[styles.input, focused === 'confirm' && styles.inputFocused]}
                  secureTextEntry
                  placeholder="Re-enter your new password"
                  placeholderTextColor={colors.textTertiary}
                  value={confirm}
                  onChangeText={setConfirm}
                  onFocus={() => setFocused('confirm')}
                  onBlur={() => setFocused(null)}
                />
              </>
            )}

            {error ? (
              <Text testID="forgot-error-text" style={styles.error}>
                {error}
              </Text>
            ) : null}

            <PressableScale
              testID="forgot-submit-button"
              onPress={phase === 'request' ? requestCode : submitReset}
              disabled={submitting}
              style={styles.btnWrap}
            >
              <LinearGradient
                colors={gradients.hero}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 1 }}
                style={[styles.primaryBtn, submitting && styles.btnDisabled]}
              >
                {submitting ? (
                  <ActivityIndicator color="#fff" />
                ) : (
                  <Text style={styles.primaryBtnText}>
                    {phase === 'request' ? 'Send reset code' : 'Reset password'}
                  </Text>
                )}
              </LinearGradient>
            </PressableScale>

            <View style={styles.footer}>
              <Text style={styles.footerText}>Remembered it? </Text>
              <Link href="/(auth)/login" asChild>
                <PressableScale testID="forgot-go-to-login-link">
                  <Text style={styles.footerLink}>Back to log in</Text>
                </PressableScale>
              </Link>
            </View>
          </Animated.View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.background },
  flex: { flex: 1 },
  scroll: { flexGrow: 1, padding: spacing.lg, justifyContent: 'center' },
  watermark: {
    position: 'absolute',
    top: 0,
    right: -24,
    fontSize: 150,
    fontWeight: '700',
    color: colors.primary,
    opacity: 0.05,
  },
  brandBlock: { alignItems: 'center', marginBottom: spacing.xxl },
  brandBadge: {
    width: 124,
    height: 96,
    borderRadius: radius.xl,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: spacing.lg,
    ...shadows.glow(accents.teal.base),
  },
  brandHanzi: {
    fontSize: 44,
    color: '#fff',
    fontWeight: '700',
  },
  brandTitle: {
    fontSize: fontSize.xxl,
    fontWeight: '700',
    color: colors.textPrimary,
    letterSpacing: -0.3,
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
  notice: {
    fontSize: fontSize.sm,
    color: colors.textSecondary,
    backgroundColor: colors.primaryLight,
    padding: spacing.md,
    borderRadius: radius.md,
    lineHeight: 20,
    marginBottom: spacing.xs,
  },
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
  inputFocused: { borderColor: colors.primary, ...shadows.sm },
  error: {
    color: colors.error,
    fontSize: fontSize.sm,
    marginTop: spacing.md,
    backgroundColor: colors.errorLight,
    padding: spacing.md,
    borderRadius: radius.md,
  },
  btnWrap: { marginTop: spacing.xl, borderRadius: radius.md },
  primaryBtn: {
    borderRadius: radius.md,
    paddingVertical: 16,
    alignItems: 'center',
    minHeight: 52,
    justifyContent: 'center',
    ...shadows.glow(accents.teal.base),
  },
  primaryBtnText: { color: '#fff', fontSize: fontSize.lg, fontWeight: '700' },
  btnDisabled: { opacity: 0.7 },
  footer: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: spacing.xl,
  },
  footerText: { color: colors.textSecondary, fontSize: fontSize.base },
  footerLink: { color: colors.primary, fontSize: fontSize.base, fontWeight: '700' },
});
