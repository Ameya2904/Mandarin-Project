import React, { useCallback, useState } from 'react';
import { View, Text, TouchableOpacity, ActivityIndicator, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useFocusEffect, useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { colors } from '@/src/theme';
import { api, Flashcard, Vocabulary } from '@/src/api/client';
import ReadingCard from '@/src/components/review/ReadingCard';
import WritingCard from '@/src/components/review/WritingCard';
import SpeakingCard from '@/src/components/review/SpeakingCard';
import { styles } from '@/src/components/review/review.styles';
import {
  STAGE_LABELS,
  MODE_META,
  buildMultiModeQueue,
  formatNextReview,
} from '@/src/components/review/reviewHelpers';
import type { Card, Mode, OnAnswered } from '@/src/components/review/types';

export default function ReviewScreen() {
  const router = useRouter();
  const [queue, setQueue] = useState<Card[]>([]);
  const [index, setIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [sessionStats, setSessionStats] = useState({ correct: 0, total: 0 });
  const [done, setDone] = useState(false);
  const [hasDeck, setHasDeck] = useState(true);
  const [cardModeResults, setCardModeResults] = useState<Record<string, { mode: Mode; correct: boolean }[]>>({});
  const [reviewSummary, setReviewSummary] = useState<
    { vocabulary: Vocabulary; new_stage: number; next_review_at: string }[]
  >([]);

  const loadQueue = useCallback(async () => {
    setLoading(true);
    setDone(false);
    setIndex(0);
    setSessionStats({ correct: 0, total: 0 });
    setCardModeResults({});
    setReviewSummary([]);
    try {
      const [due, fresh, deck] = await Promise.all([
        api.dueFlashcards(20),
        api.newFlashcards(10),
        api.deck().catch(() => []),
      ]);
      setHasDeck(deck.length > 0);
      setQueue(buildMultiModeQueue(due as Flashcard[], fresh as Vocabulary[]));
    } catch (e) {
      setQueue([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useFocusEffect(
    useCallback(() => {
      loadQueue();
    }, [loadQueue]),
  );

  const handleAnswered: OnAnswered = async (vocabId, wasCorrect, mode) => {
    const card = queue[index];

    // Accumulate per-card mode results
    const prev = cardModeResults[vocabId] ?? [];
    const updatedResults = [...prev, { mode, correct: wasCorrect }];
    setCardModeResults((r) => ({ ...r, [vocabId]: updatedResults }));

    try {
      if (card.isFinal) {
        // All 3 modes done — aggregate (≥2/3 correct = correct) and advance SRS once
        const correctCount = updatedResults.filter((r) => r.correct).length;
        const aggregateCorrect = correctCount >= 2;
        const res = await api.reviewFlashcardWithMode(vocabId, aggregateCorrect, mode);
        if (res?.new_stage != null && res?.next_review_at) {
          setReviewSummary((s) => [
            ...s,
            { vocabulary: card.vocabulary, new_stage: res.new_stage, next_review_at: res.next_review_at },
          ]);
        }
      } else {
        // Not the final mode — log history only, don't touch SRS
        await api.reviewFlashcardWithMode(vocabId, wasCorrect, mode, undefined, true);
      }
    } catch {
      // ignore network errors
    }

    setSessionStats((s) => ({
      correct: s.correct + (wasCorrect ? 1 : 0),
      total: s.total + 1,
    }));
    if (index + 1 >= queue.length) {
      setDone(true);
    } else {
      setIndex(index + 1);
    }
  };

  if (loading) {
    return (
      <View style={styles.loading}>
        <ActivityIndicator color={colors.primary} size="large" />
      </View>
    );
  }

  if (!hasDeck) {
    return (
      <SafeAreaView style={styles.safe} edges={['top']}>
        <View style={styles.emptyContainer}>
          <Text style={styles.emptyHanzi}>空</Text>
          <Text style={styles.emptyTitle}>Your deck is empty</Text>
          <Text style={styles.emptySub}>
            Add words from the NPCR library or create your own to start practicing.
          </Text>
          <TouchableOpacity
            testID="review-go-library-button"
            style={styles.emptyBtn}
            onPress={() => router.push('/library')}
          >
            <Text style={styles.emptyBtnText}>Browse Library</Text>
          </TouchableOpacity>
          <TouchableOpacity
            testID="review-add-word-button"
            style={[styles.emptyBtn, styles.emptyBtnSecondary]}
            onPress={() => router.push('/add-word')}
          >
            <Text style={[styles.emptyBtnText, styles.emptyBtnTextSecondary]}>Add Custom Word</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  if (queue.length === 0) {
    return (
      <SafeAreaView style={styles.safe} edges={['top']}>
        <View style={styles.emptyContainer}>
          <Text style={styles.emptyHanzi}>休息</Text>
          <Text style={styles.emptyTitle}>All caught up</Text>
          <Text style={styles.emptySub}>No cards due. Visit Library to add more vocabulary.</Text>
          <TouchableOpacity
            testID="review-go-library-button"
            style={styles.emptyBtn}
            onPress={() => router.push('/library')}
          >
            <Text style={styles.emptyBtnText}>Add More Words</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  if (done) {
    return (
      <SafeAreaView style={styles.safe} edges={['top']}>
        <ScrollView contentContainerStyle={styles.doneScroll}>
          <Text style={styles.emptyHanzi}>完成</Text>
          <Text style={styles.emptyTitle}>Session complete</Text>
          <Text style={styles.emptySub} testID="review-session-summary">
            {sessionStats.correct} / {sessionStats.total} correct across all modes
          </Text>

          {reviewSummary.length > 0 && (
            <View style={styles.summarySection}>
              <Text style={styles.summaryHeader}>Next Reviews</Text>
              {reviewSummary.map((item, i) => (
                <View key={i} style={styles.summaryRow}>
                  <Text style={styles.summaryHanzi}>{item.vocabulary.simplified}</Text>
                  <View style={styles.summaryRight}>
                    <Text style={styles.summaryEnglish}>{item.vocabulary.english}</Text>
                    <Text style={styles.summaryStage}>
                      {STAGE_LABELS[item.new_stage] ?? `Stage ${item.new_stage}`}
                      {' · '}
                      {formatNextReview(item.next_review_at)}
                    </Text>
                  </View>
                </View>
              ))}
            </View>
          )}

          <TouchableOpacity
            testID="review-back-to-home-button"
            style={[styles.emptyBtn, styles.doneBtn]}
            onPress={() => router.replace('/(tabs)')}
          >
            <Text style={styles.emptyBtnText}>Back to Home</Text>
          </TouchableOpacity>
          <TouchableOpacity
            testID="review-do-more-button"
            style={[styles.emptyBtn, styles.emptyBtnSecondary, styles.doneBtn]}
            onPress={loadQueue}
          >
            <Text style={[styles.emptyBtnText, styles.emptyBtnTextSecondary]}>Review More</Text>
          </TouchableOpacity>
        </ScrollView>
      </SafeAreaView>
    );
  }

  const card = queue[index];
  return (
    <SafeAreaView style={styles.safe} edges={['top']}>
      <View style={styles.header}>
        <View style={styles.progressBar}>
          <View style={[styles.progressFill, { width: `${((index + 1) / queue.length) * 100}%` }]} />
        </View>
        <Text style={styles.progressText} testID="review-progress-text">
          {index + 1} / {queue.length}
        </Text>
      </View>

      <View style={styles.modeBanner} testID={`review-mode-${card.mode}`}>
        <Ionicons name={MODE_META[card.mode].icon} size={18} color={colors.primary} />
        <View style={styles.flex}>
          <Text style={styles.modeLabel}>{MODE_META[card.mode].label}</Text>
          <Text style={styles.modeDesc}>{MODE_META[card.mode].description}</Text>
        </View>
        <Text style={styles.stageLabel}>
          {card.current_stage ? STAGE_LABELS[card.current_stage] : 'New'}
        </Text>
      </View>

      <CardBody key={`${card.vocabulary.id}-${card.mode}-${index}`} card={card} onAnswered={handleAnswered} />
    </SafeAreaView>
  );
}

function CardBody({ card, onAnswered }: { card: Card; onAnswered: OnAnswered }) {
  if (card.mode === 'reading') return <ReadingCard card={card} onAnswered={onAnswered} />;
  if (card.mode === 'writing') return <WritingCard card={card} onAnswered={onAnswered} />;
  return <SpeakingCard card={card} onAnswered={onAnswered} />;
}
