/**
 * Reading review card — show the hanzi, type the English meaning.
 *
 * Checks the answer locally first (englishMatches) for an instant result, then
 * falls back to the WordNet synonym API only when the quick check fails.
 */
import React, { useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  ActivityIndicator,
  ScrollView,
  TextInput,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { colors, getToneColor } from '@/src/theme';
import { api } from '@/src/api/client';
import { englishMatches } from './reviewHelpers';
import { styles } from './review.styles';
import type { Card, OnAnswered } from './types';

export default function ReadingCard({ card, onAnswered }: { card: Card; onAnswered: OnAnswered }) {
  const vocab = card.vocabulary;
  const [answer, setAnswer] = useState('');
  const [result, setResult] = useState<null | { correct: boolean }>(null);
  const [checking, setChecking] = useState(false);

  const handleCheck = async () => {
    if (englishMatches(answer, vocab.english)) {
      setResult({ correct: true });
      return;
    }
    setChecking(true);
    try {
      const { match } = await api.semanticMatch(answer, vocab.english);
      setResult({ correct: match });
    } catch {
      setResult({ correct: false });
    } finally {
      setChecking(false);
    }
  };

  return (
    <KeyboardAvoidingView style={styles.flex} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
      <ScrollView contentContainerStyle={styles.cardScroll} keyboardShouldPersistTaps="handled">
        <View style={styles.card}>
          <Text style={styles.hanzi}>{vocab.simplified}</Text>
          <Text style={styles.pinyinSmall}>(hidden until you answer)</Text>

          <Text style={styles.inputLabel}>What does this mean in English?</Text>
          <TextInput
            testID="review-reading-input"
            style={[
              styles.input,
              result?.correct === true && styles.inputCorrect,
              result?.correct === false && styles.inputIncorrect,
            ]}
            value={answer}
            onChangeText={setAnswer}
            placeholder="English meaning..."
            placeholderTextColor={colors.textTertiary}
            autoCapitalize="none"
            autoCorrect={false}
            editable={!result}
          />

          {result && (
            <View
              testID="review-reading-feedback"
              style={[styles.feedback, result.correct ? styles.feedbackCorrect : styles.feedbackIncorrect]}
            >
              <Ionicons
                name={result.correct ? 'checkmark-circle' : 'close-circle'}
                size={22}
                color={result.correct ? colors.success : colors.error}
              />
              <View style={styles.flex}>
                <Text style={[styles.feedbackTitle, { color: result.correct ? colors.success : colors.error }]}>
                  {result.correct ? 'Correct!' : 'Not quite'}
                </Text>
                <Text style={[styles.pinyinSmall, { color: getToneColor(vocab.pinyin) }]}>{vocab.pinyin}</Text>
                <Text style={styles.englishAnswer}>{vocab.english}</Text>
              </View>
            </View>
          )}
        </View>
      </ScrollView>

      <View style={styles.footer}>
        {result ? (
          <View style={styles.actionRow}>
            <TouchableOpacity
              testID="review-mark-incorrect"
              style={[styles.actionBtn, styles.incorrectBtn]}
              onPress={() => onAnswered(vocab.id, false, 'reading')}
            >
              <Ionicons name="close" size={22} color={colors.error} />
              <Text style={[styles.actionLabel, { color: colors.error }]}>Mark incorrect</Text>
            </TouchableOpacity>
            <TouchableOpacity
              testID="review-mark-correct"
              style={[styles.actionBtn, styles.correctBtn]}
              onPress={() => onAnswered(vocab.id, true, 'reading')}
            >
              <Ionicons name="checkmark" size={22} color={colors.success} />
              <Text style={[styles.actionLabel, { color: colors.success }]}>Continue</Text>
            </TouchableOpacity>
          </View>
        ) : (
          <TouchableOpacity
            testID="review-reading-check"
            style={[styles.primaryBtn, (!answer || checking) && styles.btnDisabled]}
            onPress={handleCheck}
            disabled={!answer || checking}
          >
            {checking ? (
              <ActivityIndicator size="small" color="#fff" />
            ) : (
              <Text style={styles.primaryBtnText}>Check</Text>
            )}
          </TouchableOpacity>
        )}
      </View>
    </KeyboardAvoidingView>
  );
}
