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

export default function SignupScreen() {
  const router = useRouter();
  const { signup } = useAuth();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [focused, setFocused] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  const onSubmit = async () => {
    setError('');
    if (!name || !email || !password) {
      setError('Please fill in all fields.');
      return;
    }
    if (password.length < 6) {
      setError('Password must be at least 6 characters.');
      return;
    }
    setSubmitting(true);
    try {
      await signup(email.trim(), password, name.trim());
      router.replace('/(tabs)');
    } catch (e: any) {
      setError(e.message || 'Signup failed');
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
              colors={gradients.violet}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 1 }}
              style={styles.brandBadge}
            >
              <Text style={styles.brandHanzi}>开始</Text>
            </LinearGradient>
            <Text style={styles.brandTitle}>Begin Your Journey</Text>
            <Text style={styles.brandSubtitle}>
              Build real Mandarin fluency, one focused session at a time.
            </Text>
          </Animated.View>

          <Animated.View entering={FadeInDown.delay(120).duration(500)} style={styles.form}>
            <Text style={styles.label}>Name</Text>
            <TextInput
              testID="signup-name-input"
              style={[styles.input, focused === 'name' && styles.inputFocused]}
              placeholder="Your name"
              placeholderTextColor={colors.textTertiary}
              value={name}
              onChangeText={setName}
              onFocus={() => setFocused('name')}
              onBlur={() => setFocused(null)}
            />

            <Text style={styles.label}>Email</Text>
            <TextInput
              testID="signup-email-input"
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
              testID="signup-password-input"
              style={[styles.input, focused === 'password' && styles.inputFocused]}
              secureTextEntry
              placeholder="At least 6 characters"
              placeholderTextColor={colors.textTertiary}
              value={password}
              onChangeText={setPassword}
              onFocus={() => setFocused('password')}
              onBlur={() => setFocused(null)}
            />

            {error ? (
              <Text testID="signup-error-text" style={styles.error}>
                {error}
              </Text>
            ) : null}

            <PressableScale
              testID="signup-submit-button"
              onPress={onSubmit}
              disabled={submitting}
              style={styles.btnWrap}
            >
              <LinearGradient
                colors={gradients.violet}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 1 }}
                style={[styles.primaryBtn, submitting && styles.btnDisabled]}
              >
                {submitting ? (
                  <ActivityIndicator color="#fff" />
                ) : (
                  <Text style={styles.primaryBtnText}>Create account</Text>
                )}
              </LinearGradient>
            </PressableScale>

            <View style={styles.footer}>
              <Text style={styles.footerText}>Already have an account? </Text>
              <Link href="/(auth)/login" asChild>
                <PressableScale testID="signup-go-to-login-link">
                  <Text style={styles.footerLink}>Log in</Text>
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
  accent: colors.secondary,
  glow: accents.violet.base,
  badgeWidth: 124,
  hanziSize: 44,
  titleSize: fontSize.xxl,
  titleLetterSpacing: -0.3,
  brandMarginBottom: spacing.xl,
});
