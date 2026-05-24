import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useLocalSearchParams, useRouter, Stack } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { colors, spacing, radius, fontSize, getToneColor } from '@/src/theme';
import { api, Drill } from '@/src/api/client';

function normalize(text: string): string {
  // eslint-disable-next-line no-misleading-character-class
  return (text || '').replace(/[\s\W_，。!?,.!?]/g, '');
}

export default function DrillScreen() {
  const router = useRouter();
  const { lesson } = useLocalSearchParams<{ lesson?: string }>();
  const [drills, setDrills] = useState<Drill[]>([]);
  const [index, setIndex] = useState(0);
  const [answer, setAnswer] = useState('');
  const [feedback, setFeedback] = useState<{ correct: boolean; message: string } | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [sessionStats, setSessionStats] = useState({ correct: 0, total: 0 });
  const [done, setDone] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        const data = await api.drills(lesson ? Number(lesson) : undefined);
        setDrills(data);
      } catch (e) {
        setDrills([]);
      } finally {
        setLoading(false);
      }
    })();
  }, [lesson]);

  const current = drills[index];

  const handleSubmit = async () => {
    if (!current || submitting) return;
    setSubmitting(true);

    const normalizedAnswer = normalize(answer);
    const normalizedExpected = normalize(current.expected_answer);
    const isCorrect = normalizedAnswer === normalizedExpected;

    setFeedback({
      correct: isCorrect,
      message: isCorrect ? 'Perfect! 完美!' : `Expected: ${current.expected_answer}`,
    });
    setSessionStats((s) => ({
      correct: s.correct + (isCorrect ? 1 : 0),
      total: s.total + 1,
    }));

    try {
      await api.drillAttempt(current.id, answer, isCorrect);
    } catch {
      // ignore
    }
    setSubmitting(false);
  };

  const handleNext = () => {
    if (index + 1 >= drills.length) {
      setDone(true);
    } else {
      setIndex(index + 1);
      setAnswer('');
      setFeedback(null);
    }
  };

  if (loading) {
    return (
      <View style={styles.loading}>
        <ActivityIndicator color={colors.primary} size="large" />
      </View>
    );
  }

  if (drills.length === 0) {
    return (
      <SafeAreaView style={styles.safe} edges={['top']}>
        <View style={styles.empty}>
          <Text style={styles.emptyHanzi}>没有</Text>
          <Text style={styles.emptyTitle}>No drills available</Text>
          <TouchableOpacity testID="drill-back-button" style={styles.btn} onPress={() => router.back()}>
            <Text style={styles.btnText}>Go back</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  if (done) {
    return (
      <SafeAreaView style={styles.safe} edges={['top']}>
        <View style={styles.empty}>
          <Text style={styles.emptyHanzi}>完成</Text>
          <Text style={styles.emptyTitle}>Drills complete</Text>
          <Text style={styles.emptySub} testID="drill-session-summary">
            {sessionStats.correct} / {sessionStats.total} correct
          </Text>
          <TouchableOpacity
            testID="drill-back-home-button"
            style={styles.btn}
            onPress={() => router.replace('/(tabs)')}
          >
            <Text style={styles.btnText}>Back to Home</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.safe} edges={['top']}>
      <Stack.Screen options={{ headerShown: false }} />
      <KeyboardAvoidingView
        style={styles.flex}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      >
        <View style={styles.header}>
          <TouchableOpacity
            testID="drill-close-button"
            onPress={() => router.back()}
            style={styles.backBtn}
          >
            <Ionicons name="close" size={24} color={colors.textPrimary} />
          </TouchableOpacity>
          <View style={styles.progressBar}>
            <View style={[styles.progressFill, { width: `${((index + 1) / drills.length) * 100}%` }]} />
          </View>
          <Text style={styles.progressText}>
            {index + 1}/{drills.length}
          </Text>
        </View>

        <ScrollView contentContainerStyle={styles.scroll} keyboardShouldPersistTaps="handled">
          <Text style={styles.drillType}>
            {current.drill_type === 'substitution' ? 'Substitution Drill' : current.drill_type === 'transformation' ? 'Transformation Drill' : 'Drill'}
          </Text>

          <View style={styles.promptCard} testID="drill-prompt-card">
            <Text style={styles.promptLabel}>Base sentence</Text>
            <Text style={styles.promptHanzi}>{current.prompt_chinese}</Text>
            <Text style={styles.promptEnglish}>{current.prompt_english}</Text>
          </View>

          <View style={styles.instructionCard} testID="drill-instruction-card">
            <Ionicons name="information-circle-outline" size={20} color={colors.primary} />
            <View style={styles.flex}>
              <Text style={styles.instructionText}>{current.instruction_english}</Text>
              <Text style={styles.instructionChinese}>{current.instruction_chinese}</Text>
            </View>
          </View>

          <Text style={styles.inputLabel}>Your answer (in Chinese)</Text>
          <TextInput
            testID="drill-sentence-input"
            style={[styles.input, feedback?.correct === true && styles.inputCorrect, feedback?.correct === false && styles.inputIncorrect]}
            value={answer}
            onChangeText={setAnswer}
            placeholder="Type here..."
            placeholderTextColor={colors.textTertiary}
            editable={!feedback}
            autoCorrect={false}
            autoCapitalize="none"
          />

          {feedback && (
            <View
              testID="drill-feedback"
              style={[styles.feedback, feedback.correct ? styles.feedbackCorrect : styles.feedbackIncorrect]}
            >
              <Ionicons
                name={feedback.correct ? 'checkmark-circle' : 'close-circle'}
                size={22}
                color={feedback.correct ? colors.success : colors.error}
              />
              <View style={styles.flex}>
                <Text style={[styles.feedbackText, { color: feedback.correct ? colors.success : colors.error }]}>
                  {feedback.message}
                </Text>
                <Text style={[styles.feedbackPinyin, { color: getToneColor(current.expected_pinyin) }]}>
                  {current.expected_pinyin}
                </Text>
                <Text style={styles.feedbackEnglish}>{current.expected_english}</Text>
              </View>
            </View>
          )}
        </ScrollView>

        <View style={styles.footer}>
          {feedback ? (
            <TouchableOpacity testID="drill-next-button" style={styles.primaryBtn} onPress={handleNext}>
              <Text style={styles.primaryBtnText}>
                {index + 1 >= drills.length ? 'Finish' : 'Next'}
              </Text>
              <Ionicons name="arrow-forward" size={20} color="#fff" />
            </TouchableOpacity>
          ) : (
            <TouchableOpacity
              testID="drill-submit-button"
              style={[styles.primaryBtn, !answer && styles.btnDisabled]}
              onPress={handleSubmit}
              disabled={!answer || submitting}
            >
              <Text style={styles.primaryBtnText}>Check</Text>
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
  loading: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: colors.background },
  header: { flexDirection: 'row', alignItems: 'center', padding: spacing.md, gap: spacing.md },
  backBtn: { padding: spacing.sm, minWidth: 48, minHeight: 48, justifyContent: 'center' },
  progressBar: { flex: 1, height: 4, backgroundColor: colors.border, borderRadius: radius.full, overflow: 'hidden' },
  progressFill: { height: '100%', backgroundColor: colors.primary, borderRadius: radius.full },
  progressText: { fontSize: fontSize.sm, color: colors.textSecondary, fontWeight: '500' },
  scroll: { padding: spacing.lg, flexGrow: 1 },
  drillType: { fontSize: fontSize.xs, color: colors.textTertiary, letterSpacing: 1, textTransform: 'uppercase', marginBottom: spacing.md },
  promptCard: {
    backgroundColor: colors.surface,
    borderRadius: radius.xl,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.lg,
    alignItems: 'center',
  },
  promptLabel: { fontSize: fontSize.xs, color: colors.textTertiary, letterSpacing: 1, textTransform: 'uppercase' },
  promptHanzi: { fontSize: fontSize.hanzi, color: colors.textPrimary, fontWeight: '500', marginTop: spacing.sm, textAlign: 'center' },
  promptEnglish: { fontSize: fontSize.base, color: colors.textSecondary, marginTop: spacing.sm, textAlign: 'center' },
  instructionCard: {
    backgroundColor: colors.primaryLight,
    borderRadius: radius.lg,
    padding: spacing.md,
    flexDirection: 'row',
    gap: spacing.sm,
    marginTop: spacing.lg,
    alignItems: 'flex-start',
  },
  instructionText: { fontSize: fontSize.base, color: colors.textPrimary, fontWeight: '500' },
  instructionChinese: { fontSize: fontSize.sm, color: colors.textSecondary, marginTop: 2 },
  inputLabel: {
    fontSize: fontSize.sm,
    color: colors.textSecondary,
    fontWeight: '500',
    marginTop: spacing.lg,
    marginBottom: spacing.sm,
  },
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
  feedback: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: spacing.sm,
    padding: spacing.md,
    borderRadius: radius.lg,
    marginTop: spacing.lg,
  },
  feedbackCorrect: { backgroundColor: colors.successLight },
  feedbackIncorrect: { backgroundColor: colors.errorLight },
  feedbackText: { fontSize: fontSize.base, fontWeight: '600' },
  feedbackPinyin: { fontSize: fontSize.sm, marginTop: 4 },
  feedbackEnglish: { fontSize: fontSize.sm, color: colors.textSecondary, marginTop: 2 },
  footer: { padding: spacing.lg },
  primaryBtn: {
    backgroundColor: colors.primary,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: spacing.sm,
    paddingVertical: 16,
    borderRadius: radius.md,
    minHeight: 52,
  },
  primaryBtnText: { color: '#fff', fontSize: fontSize.lg, fontWeight: '600' },
  btnDisabled: { opacity: 0.5 },
  empty: { flex: 1, alignItems: 'center', justifyContent: 'center', padding: spacing.xl },
  emptyHanzi: { fontSize: 88, color: colors.primary, fontWeight: '300', marginBottom: spacing.md },
  emptyTitle: { fontSize: fontSize.xxl, color: colors.textPrimary, fontWeight: '500' },
  emptySub: { fontSize: fontSize.base, color: colors.textSecondary, textAlign: 'center', marginTop: spacing.md },
  btn: { backgroundColor: colors.primary, paddingHorizontal: spacing.xl, paddingVertical: 14, borderRadius: radius.full, marginTop: spacing.xl, minHeight: 48, justifyContent: 'center' },
  btnText: { color: '#fff', fontSize: fontSize.base, fontWeight: '600' },
});
