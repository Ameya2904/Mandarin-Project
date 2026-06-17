import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  ActivityIndicator,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Link, useRouter } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient';
import Animated, { FadeInDown } from 'react-native-reanimated';
import { colors, spacing, fontSize, accents, gradients } from '@/src/theme';
import { makeAuthStyles } from './auth.styles';
import PressableScale from '@/src/components/PressableScale';
import { useAuth } from '@/src/contexts/AuthContext';

export default function LoginScreen() {
  const router = useRouter();
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [focused, setFocused] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  const onSubmit = async () => {
    setError('');
    if (!email || !password) {
      setError('Please enter your email and password.');
      return;
    }
    setSubmitting(true);
    try {
      await login(email.trim(), password);
      router.replace('/(tabs)');
    } catch (e: any) {
      setError(e.message || 'Login failed');
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
              <Text style={styles.brandHanzi}>间</Text>
            </LinearGradient>
            <Text style={styles.brandTitle}>SpacedChinese</Text>
            <Text style={styles.brandSubtitle}>
              Structured Mandarin training, from recognition to fluency.
            </Text>
          </Animated.View>

          <Animated.View entering={FadeInDown.delay(120).duration(500)} style={styles.form}>
            <Text style={styles.label}>Email</Text>
            <TextInput
              testID="login-email-input"
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

            <Text style={styles.label}>Password</Text>
            <TextInput
              testID="login-password-input"
              style={[styles.input, focused === 'password' && styles.inputFocused]}
              secureTextEntry
              placeholder="••••••••"
              placeholderTextColor={colors.textTertiary}
              value={password}
              onChangeText={setPassword}
              onFocus={() => setFocused('password')}
              onBlur={() => setFocused(null)}
            />

            <Link href="/(auth)/forgot-password" asChild>
              <PressableScale testID="login-forgot-password-link" style={styles.forgotWrap}>
                <Text style={styles.forgotLink}>Forgot password?</Text>
              </PressableScale>
            </Link>

            {error ? (
              <Text testID="login-error-text" style={styles.error}>
                {error}
              </Text>
            ) : null}

            <PressableScale
              testID="login-submit-button"
              onPress={onSubmit}
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
                  <Text style={styles.primaryBtnText}>Log in</Text>
                )}
              </LinearGradient>
            </PressableScale>

            <View style={styles.footer}>
              <Text style={styles.footerText}>New here? </Text>
              <Link href="/(auth)/signup" asChild>
                <PressableScale testID="login-go-to-signup-link">
                  <Text style={styles.footerLink}>Create an account</Text>
                </PressableScale>
              </Link>
            </View>
          </Animated.View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = makeAuthStyles({
  accent: colors.primary,
  glow: accents.teal.base,
  badgeWidth: 96,
  hanziSize: 52,
  titleSize: fontSize.display,
  titleLetterSpacing: -0.5,
  brandMarginBottom: spacing.xxl,
});
