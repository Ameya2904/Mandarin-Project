import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useLocalSearchParams, useRouter, Stack } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { colors, spacing, radius, fontSize, getToneColor } from '@/src/theme';
import { api } from '@/src/api/client';

export default function SpeakPracticeScreen() {
  const router = useRouter();
  const params = useLocalSearchParams<{ chinese: string; pinyin: string; english: string }>();

  const target = String(params.chinese || '');
  const pinyin = String(params.pinyin || '');
  const english = String(params.english || '');

  const [revealed, setRevealed] = useState(false);
  const [spoken, setSpoken] = useState('');
  const [result, setResult] = useState<{ correct: boolean; score: number; feedback: string } | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const handleCheck = async () => {
    if (!spoken.trim() || submitting) return;
    setSubmitting(true);
    try {
      const r = await api.evaluateSpeaking(target, spoken);
      setResult(r);
    } catch (e) {
      // ignore
    } finally {
      setSubmitting(false);
    }
  };

  const handleReset = () => {
    setSpoken('');
    setResult(null);
    setRevealed(false);
  };

  return (
    <SafeAreaView style={styles.safe} edges={['top']}>
      <Stack.Screen options={{ headerShown: false }} />
      <KeyboardAvoidingView
        style={styles.flex}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      >
        <View style={styles.header}>
          <TouchableOpacity
            testID="speak-close-button"
            onPress={() => router.back()}
            style={styles.backBtn}
          >
            <Ionicons name="close" size={24} color={colors.textPrimary} />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Speaking Practice</Text>
        </View>

        <ScrollView contentContainerStyle={styles.scroll} keyboardShouldPersistTaps="handled">
          <Text style={styles.label}>Say this in Mandarin</Text>
          <View style={styles.targetCard} testID="speak-target-card">
            <Text style={styles.targetEnglish}>{english}</Text>
            {revealed ? (
              <>
                <Text style={styles.targetHanzi}>{target}</Text>
                <Text style={[styles.targetPinyin, { color: getToneColor(pinyin) }]}>
                  {pinyin}
                </Text>
              </>
            ) : (
              <TouchableOpacity
                testID="speak-reveal-target-button"
                style={styles.revealBtn}
                onPress={() => setRevealed(true)}
              >
                <Ionicons name="eye-outline" size={18} color={colors.primary} />
                <Text style={styles.revealBtnText}>Show Mandarin</Text>
              </TouchableOpacity>
            )}
          </View>

          <Text style={styles.label}>Type what you would say (in Chinese characters)</Text>
          <Text style={styles.hint}>
            This MVP uses text-based evaluation. Real audio capture will arrive in the next phase.
          </Text>

          <TextInput
            testID="speak-input"
            style={[
              styles.input,
              result?.correct === true && styles.inputCorrect,
              result?.correct === false && styles.inputIncorrect,
            ]}
            value={spoken}
            onChangeText={setSpoken}
            placeholder="例如: 你好"
            placeholderTextColor={colors.textTertiary}
            editable={!result}
            autoCorrect={false}
            autoCapitalize="none"
          />

          {result && (
            <View
              testID="speak-feedback"
              style={[styles.feedback, result.correct ? styles.feedbackCorrect : styles.feedbackIncorrect]}
            >
              <View style={styles.feedbackHeader}>
                <Ionicons
                  name={result.correct ? 'checkmark-circle' : 'alert-circle'}
                  size={24}
                  color={result.correct ? colors.success : colors.error}
                />
                <Text style={[styles.feedbackTitle, { color: result.correct ? colors.success : colors.error }]}>
                  {result.feedback}
                </Text>
              </View>
              <View style={styles.scoreBar}>
                <View style={[styles.scoreFill, { width: `${result.score}%`, backgroundColor: result.correct ? colors.success : colors.error }]} />
              </View>
              <Text style={styles.scoreText}>Match score: {result.score}%</Text>
              <View style={styles.compareBlock}>
                <Text style={styles.compareLabel}>Target</Text>
                <Text style={styles.compareHanzi}>{target}</Text>
                <Text style={styles.compareLabel}>You said</Text>
                <Text style={styles.compareHanzi}>{spoken}</Text>
              </View>
            </View>
          )}
        </ScrollView>

        <View style={styles.footer}>
          {result ? (
            <View style={styles.footerRow}>
              <TouchableOpacity
                testID="speak-try-again-button"
                style={[styles.btn, styles.btnSecondary]}
                onPress={handleReset}
              >
                <Text style={[styles.btnText, { color: colors.primary }]}>Try again</Text>
              </TouchableOpacity>
              <TouchableOpacity
                testID="speak-back-list-button"
                style={[styles.btn, styles.btnPrimary]}
                onPress={() => router.back()}
              >
                <Text style={[styles.btnText, { color: '#fff' }]}>Next sentence</Text>
              </TouchableOpacity>
            </View>
          ) : (
            <TouchableOpacity
              testID="speak-check-button"
              style={[styles.btn, styles.btnPrimary, !spoken && styles.btnDisabled]}
              onPress={handleCheck}
              disabled={!spoken || submitting}
            >
              <Text style={[styles.btnText, { color: '#fff' }]}>Check Pronunciation</Text>
            </TouchableOpacity>
          )}
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.background },
  flex: { flex: 1 },
  header: { flexDirection: 'row', alignItems: 'center', padding: spacing.md, gap: spacing.sm },
  backBtn: { padding: spacing.sm, minWidth: 48, minHeight: 48, justifyContent: 'center' },
  headerTitle: { fontSize: fontSize.base, color: colors.textPrimary, fontWeight: '500' },
  scroll: { padding: spacing.lg, flexGrow: 1 },
  label: {
    fontSize: fontSize.xs,
    color: colors.textTertiary,
    letterSpacing: 1,
    textTransform: 'uppercase',
    marginBottom: spacing.sm,
    marginTop: spacing.md,
  },
  hint: { fontSize: fontSize.xs, color: colors.textTertiary, marginBottom: spacing.sm },
  targetCard: {
    backgroundColor: colors.surface,
    borderRadius: radius.xl,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.lg,
    alignItems: 'center',
    minHeight: 180,
    justifyContent: 'center',
  },
  targetEnglish: { fontSize: fontSize.lg, color: colors.textPrimary, fontWeight: '500', textAlign: 'center' },
  targetHanzi: { fontSize: fontSize.hanzi, color: colors.textPrimary, fontWeight: '500', marginTop: spacing.md, textAlign: 'center' },
  targetPinyin: { fontSize: fontSize.lg, marginTop: spacing.sm },
  revealBtn: {
    marginTop: spacing.lg,
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
    paddingHorizontal: spacing.md,
    paddingVertical: 10,
    borderRadius: radius.full,
    borderWidth: 1,
    borderColor: colors.primary,
    minHeight: 44,
  },
  revealBtnText: { color: colors.primary, fontWeight: '600', fontSize: fontSize.sm },
  input: {
    borderBottomWidth: 2,
    borderBottomColor: colors.textPrimary,
    paddingVertical: spacing.md,
    fontSize: fontSize.xxl,
    color: colors.textPrimary,
    textAlign: 'center',
    minHeight: 60,
  },
  inputCorrect: { borderBottomColor: colors.success },
  inputIncorrect: { borderBottomColor: colors.error },
  feedback: { padding: spacing.md, borderRadius: radius.lg, marginTop: spacing.lg },
  feedbackCorrect: { backgroundColor: colors.successLight },
  feedbackIncorrect: { backgroundColor: colors.errorLight },
  feedbackHeader: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  feedbackTitle: { fontSize: fontSize.base, fontWeight: '600', flex: 1 },
  scoreBar: { height: 6, backgroundColor: 'rgba(0,0,0,0.06)', borderRadius: radius.full, overflow: 'hidden', marginTop: spacing.md },
  scoreFill: { height: '100%', borderRadius: radius.full },
  scoreText: { fontSize: fontSize.sm, color: colors.textSecondary, marginTop: 6 },
  compareBlock: { marginTop: spacing.md },
  compareLabel: { fontSize: fontSize.xs, color: colors.textTertiary, marginTop: spacing.sm, textTransform: 'uppercase', letterSpacing: 1 },
  compareHanzi: { fontSize: fontSize.xl, color: colors.textPrimary, marginTop: 2 },
  footer: { padding: spacing.lg },
  footerRow: { flexDirection: 'row', gap: spacing.md },
  btn: { flex: 1, paddingVertical: 16, borderRadius: radius.md, alignItems: 'center', justifyContent: 'center', minHeight: 52 },
  btnPrimary: { backgroundColor: colors.primary },
  btnSecondary: { backgroundColor: 'transparent', borderWidth: 1, borderColor: colors.primary },
  btnDisabled: { opacity: 0.5 },
  btnText: { fontSize: fontSize.base, fontWeight: '600' },
});
