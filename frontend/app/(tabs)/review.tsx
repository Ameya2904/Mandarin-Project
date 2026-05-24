import React, { useCallback, useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ActivityIndicator,
  ScrollView,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useFocusEffect, useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { colors, spacing, radius, fontSize, getToneColor } from '@/src/theme';
import { api, Flashcard, Vocabulary } from '@/src/api/client';

type Card = {
  vocabulary: Vocabulary;
  current_stage: number | null; // null = new card
};

const STAGE_LABELS: Record<number, string> = {
  1: 'Stage 1 · 1 day',
  2: 'Stage 2 · 2 days',
  3: 'Stage 3 · 1 week',
  4: 'Stage 4 · 1 month',
  5: 'Stage 5 · 3 months',
  6: 'Stage 6 · 1 year',
};

export default function ReviewScreen() {
  const router = useRouter();
  const [queue, setQueue] = useState<Card[]>([]);
  const [index, setIndex] = useState(0);
  const [revealed, setRevealed] = useState(false);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [sessionStats, setSessionStats] = useState({ correct: 0, total: 0 });
  const [done, setDone] = useState(false);

  const loadQueue = useCallback(async () => {
    setLoading(true);
    setDone(false);
    setIndex(0);
    setRevealed(false);
    setSessionStats({ correct: 0, total: 0 });
    try {
      const [due, fresh] = await Promise.all([api.dueFlashcards(20), api.newFlashcards(10)]);
      const dueCards: Card[] = due.map((c: Flashcard) => ({
        vocabulary: c.vocabulary,
        current_stage: c.current_stage,
      }));
      const newCards: Card[] = fresh.map((v: Vocabulary) => ({
        vocabulary: v,
        current_stage: null,
      }));
      // Interleave: due cards first, then new
      setQueue([...dueCards, ...newCards]);
    } catch (e) {
      setQueue([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useFocusEffect(
    useCallback(() => {
      loadQueue();
    }, [loadQueue])
  );

  const currentCard = queue[index];

  const handleAnswer = async (wasCorrect: boolean) => {
    if (!currentCard || submitting) return;
    setSubmitting(true);
    try {
      await api.reviewFlashcard(currentCard.vocabulary.id, wasCorrect);
      setSessionStats((s) => ({
        correct: s.correct + (wasCorrect ? 1 : 0),
        total: s.total + 1,
      }));

      if (index + 1 >= queue.length) {
        setDone(true);
      } else {
        setIndex(index + 1);
        setRevealed(false);
      }
    } catch (e) {
      // ignore
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.loading}>
        <ActivityIndicator color={colors.primary} size="large" />
      </View>
    );
  }

  if (queue.length === 0) {
    return (
      <SafeAreaView style={styles.safe} edges={['top']}>
        <View style={styles.emptyContainer}>
          <Text style={styles.emptyHanzi}>休息</Text>
          <Text style={styles.emptyTitle}>All caught up</Text>
          <Text style={styles.emptySub}>
            No cards due for review. Visit Lessons to introduce new vocabulary.
          </Text>
          <TouchableOpacity
            testID="review-go-to-lessons-button"
            style={styles.emptyBtn}
            onPress={() => router.push('/(tabs)/lessons')}
          >
            <Text style={styles.emptyBtnText}>Browse Lessons</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  if (done) {
    return (
      <SafeAreaView style={styles.safe} edges={['top']}>
        <View style={styles.emptyContainer}>
          <Text style={styles.emptyHanzi}>完成</Text>
          <Text style={styles.emptyTitle}>Session complete</Text>
          <Text style={styles.emptySub} testID="review-session-summary">
            {sessionStats.correct} / {sessionStats.total} correct
          </Text>
          <TouchableOpacity
            testID="review-back-to-home-button"
            style={styles.emptyBtn}
            onPress={() => router.replace('/(tabs)')}
          >
            <Text style={styles.emptyBtnText}>Back to Home</Text>
          </TouchableOpacity>
          <TouchableOpacity
            testID="review-do-more-button"
            style={[styles.emptyBtn, styles.emptyBtnSecondary]}
            onPress={loadQueue}
          >
            <Text style={[styles.emptyBtnText, styles.emptyBtnTextSecondary]}>Review More</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  const vocab = currentCard.vocabulary;
  const stageLabel = currentCard.current_stage
    ? STAGE_LABELS[currentCard.current_stage]
    : 'New card · first review';

  return (
    <SafeAreaView style={styles.safe} edges={['top']}>
      <View style={styles.header}>
        <View style={styles.progressBar}>
          <View
            style={[
              styles.progressFill,
              { width: `${((index + 1) / queue.length) * 100}%` },
            ]}
          />
        </View>
        <Text style={styles.progressText} testID="review-progress-text">
          {index + 1} / {queue.length}
        </Text>
      </View>

      <ScrollView contentContainerStyle={styles.cardScroll}>
        <View style={styles.card} testID="review-flashcard">
          <Text style={styles.stageLabel}>{stageLabel}</Text>
          <Text style={styles.hanzi} testID="review-flashcard-hanzi">
            {vocab.simplified}
          </Text>

          {revealed ? (
            <View style={styles.revealBlock} testID="review-flashcard-reveal">
              <Text style={[styles.pinyin, { color: getToneColor(vocab.pinyin) }]}>
                {vocab.pinyin}
              </Text>
              <Text style={styles.english}>{vocab.english}</Text>
              <View style={styles.divider} />
              <Text style={styles.exampleLabel}>Example</Text>
              <Text style={styles.exampleHanzi}>{vocab.example_chinese}</Text>
              <Text style={[styles.examplePinyin, { color: getToneColor(vocab.example_pinyin) }]}>
                {vocab.example_pinyin}
              </Text>
              <Text style={styles.exampleEnglish}>{vocab.example_english}</Text>
            </View>
          ) : (
            <TouchableOpacity
              testID="flashcard-reveal-button"
              style={styles.revealBtn}
              onPress={() => setRevealed(true)}
            >
              <Ionicons name="eye-outline" size={20} color={colors.primary} />
              <Text style={styles.revealBtnText}>Show Answer</Text>
            </TouchableOpacity>
          )}
        </View>
      </ScrollView>

      {revealed && (
        <View style={styles.actionRow} testID="review-action-row">
          <TouchableOpacity
            testID="flashcard-mark-incorrect-button"
            style={[styles.actionBtn, styles.incorrectBtn]}
            onPress={() => handleAnswer(false)}
            disabled={submitting}
          >
            <Ionicons name="close" size={26} color={colors.error} />
            <Text style={[styles.actionLabel, { color: colors.error }]}>I forgot</Text>
          </TouchableOpacity>
          <TouchableOpacity
            testID="flashcard-mark-correct-button"
            style={[styles.actionBtn, styles.correctBtn]}
            onPress={() => handleAnswer(true)}
            disabled={submitting}
          >
            <Ionicons name="checkmark" size={26} color={colors.success} />
            <Text style={[styles.actionLabel, { color: colors.success }]}>I knew it</Text>
          </TouchableOpacity>
        </View>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.background },
  loading: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: colors.background },
  header: {
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.md,
    paddingBottom: spacing.sm,
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
  },
  progressBar: {
    flex: 1,
    height: 4,
    backgroundColor: colors.border,
    borderRadius: radius.full,
    overflow: 'hidden',
  },
  progressFill: { height: '100%', backgroundColor: colors.primary, borderRadius: radius.full },
  progressText: { fontSize: fontSize.sm, color: colors.textSecondary, fontWeight: '500' },
  cardScroll: { flexGrow: 1, padding: spacing.lg, justifyContent: 'center' },
  card: {
    backgroundColor: colors.surface,
    borderRadius: radius.xl,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.xl,
    minHeight: 380,
    alignItems: 'center',
    justifyContent: 'center',
  },
  stageLabel: {
    fontSize: fontSize.xs,
    color: colors.textTertiary,
    letterSpacing: 1,
    textTransform: 'uppercase',
    marginBottom: spacing.lg,
  },
  hanzi: {
    fontSize: fontSize.hanziLg,
    color: colors.textPrimary,
    fontWeight: '500',
    textAlign: 'center',
  },
  revealBtn: {
    marginTop: spacing.xl,
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 14,
    paddingHorizontal: spacing.xl,
    borderRadius: radius.full,
    borderWidth: 1,
    borderColor: colors.primary,
    gap: spacing.sm,
    minHeight: 48,
  },
  revealBtnText: { color: colors.primary, fontSize: fontSize.base, fontWeight: '600' },
  revealBlock: { marginTop: spacing.xl, alignItems: 'center', width: '100%' },
  pinyin: { fontSize: fontSize.xxl, fontWeight: '400', letterSpacing: 1, textAlign: 'center' },
  english: {
    fontSize: fontSize.lg,
    color: colors.textPrimary,
    marginTop: spacing.sm,
    textAlign: 'center',
  },
  divider: {
    height: 1,
    backgroundColor: colors.border,
    width: '60%',
    marginVertical: spacing.lg,
  },
  exampleLabel: {
    fontSize: fontSize.xs,
    color: colors.textTertiary,
    letterSpacing: 1,
    textTransform: 'uppercase',
    marginBottom: spacing.sm,
  },
  exampleHanzi: { fontSize: fontSize.xl, color: colors.textPrimary, textAlign: 'center' },
  examplePinyin: { fontSize: fontSize.base, marginTop: 4, textAlign: 'center' },
  exampleEnglish: { fontSize: fontSize.sm, color: colors.textSecondary, marginTop: 4, textAlign: 'center' },
  actionRow: {
    flexDirection: 'row',
    padding: spacing.lg,
    gap: spacing.md,
    backgroundColor: colors.background,
  },
  actionBtn: {
    flex: 1,
    borderRadius: radius.lg,
    padding: spacing.lg,
    alignItems: 'center',
    gap: spacing.xs,
    minHeight: 76,
    justifyContent: 'center',
  },
  correctBtn: { backgroundColor: colors.successLight, borderWidth: 1, borderColor: colors.success },
  incorrectBtn: { backgroundColor: colors.errorLight, borderWidth: 1, borderColor: colors.error },
  actionLabel: { fontSize: fontSize.base, fontWeight: '600' },
  emptyContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: spacing.xl,
  },
  emptyHanzi: { fontSize: 88, color: colors.primary, fontWeight: '300', marginBottom: spacing.md },
  emptyTitle: { fontSize: fontSize.xxl, color: colors.textPrimary, fontWeight: '500' },
  emptySub: {
    fontSize: fontSize.base,
    color: colors.textSecondary,
    textAlign: 'center',
    marginTop: spacing.md,
    paddingHorizontal: spacing.xl,
    lineHeight: 22,
  },
  emptyBtn: {
    backgroundColor: colors.primary,
    paddingHorizontal: spacing.xl,
    paddingVertical: 14,
    borderRadius: radius.full,
    marginTop: spacing.xl,
    minHeight: 48,
    justifyContent: 'center',
  },
  emptyBtnSecondary: { backgroundColor: 'transparent', borderWidth: 1, borderColor: colors.primary, marginTop: spacing.md },
  emptyBtnText: { color: '#fff', fontSize: fontSize.base, fontWeight: '600' },
  emptyBtnTextSecondary: { color: colors.primary },
});
