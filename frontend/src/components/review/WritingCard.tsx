/**
 * Writing review card — handwrite the characters for an English+pinyin prompt.
 *
 * Captures the canvas as a PNG, sends it to the OCR endpoint, and treats the
 * result as "passed" when the score and identity score clear their thresholds.
 * The user can still "Mark correct anyway" when the OCR is unfairly harsh.
 */
import React, { useRef, useState } from 'react';
import { View, Text, TouchableOpacity, ActivityIndicator, ScrollView } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { colors, getToneColor } from '@/src/theme';
import { api } from '@/src/api/client';
import HandwritingCanvas, { HandwritingCanvasHandle } from '@/src/components/HandwritingCanvas';
import { styles } from './review.styles';
import type { Card, OnAnswered, WritingResult } from './types';

export default function WritingCard({ card, onAnswered }: { card: Card; onAnswered: OnAnswered }) {
  const vocab = card.vocabulary;
  const canvasRef = useRef<HandwritingCanvasHandle>(null);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<WritingResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    setError(null);
    if (!canvasRef.current || canvasRef.current.isEmpty()) {
      setError('Please write the characters first.');
      return;
    }
    setSubmitting(true);
    try {
      const base64 = await canvasRef.current.captureBase64();
      const r = await api.recognizeHandwriting(base64, vocab.simplified, vocab.id);
      // composite >= 80 AND at least 2/3 of characters correct
      const passed = r.score >= 80 && r.identity_score >= 67;
      setResult({
        score: r.score,
        identity_score: r.identity_score,
        quality_score: r.quality_score,
        feedback: r.feedback,
        characters: r.characters,
        recognized: r.recognized_text,
        passed,
      });
    } catch (e: any) {
      setError(e?.message || 'Recognition failed');
    } finally {
      setSubmitting(false);
    }
  };

  const qualityBarColor = (q: number) =>
    q >= 80 ? colors.success : q >= 50 ? colors.warning : colors.error;

  return (
    <ScrollView contentContainerStyle={styles.cardScroll}>
      <View style={styles.card}>
        <Text style={styles.englishPrompt}>{vocab.english}</Text>
        <Text style={[styles.pinyinSmall, { color: getToneColor(vocab.pinyin) }]}>{vocab.pinyin}</Text>
        <Text style={styles.writePrompt}>Handwrite the Chinese characters below</Text>

        <View style={styles.canvasWrap}>
          <HandwritingCanvas ref={canvasRef} height={240} testID="review-handwriting" />
        </View>

        {error && (
          <View style={[styles.feedback, styles.feedbackIncorrect]} testID="review-writing-error">
            <Ionicons name="alert-circle" size={20} color={colors.error} />
            <Text style={[styles.feedbackTitle, { color: colors.error, flex: 1 }]}>{error}</Text>
          </View>
        )}

        {result && (
          <View testID="review-writing-feedback" style={styles.writingFeedback}>
            {result.characters.length > 0 ? (
              <View style={styles.charTileRow}>
                {result.characters.map((c, i) => (
                  <View
                    key={i}
                    style={[
                      styles.charTile,
                      c.match ? styles.charTileGood : c.recognized ? styles.charTileBad : styles.charTileBlank,
                    ]}
                  >
                    <Text style={styles.charTargetLabel}>{c.target}</Text>
                    <Text style={styles.charRecognized}>{c.recognized || '—'}</Text>
                    <View style={styles.qualityBar}>
                      <View
                        style={[
                          styles.qualityFill,
                          { width: `${c.quality}%` as any, backgroundColor: qualityBarColor(c.quality) },
                        ]}
                      />
                    </View>
                    <Text style={styles.qualityPct}>{c.quality}%</Text>
                    {c.notes ? <Text style={styles.charNote}>{c.notes}</Text> : null}
                  </View>
                ))}
              </View>
            ) : (
              <>
                <Text style={styles.compareLabel}>Target</Text>
                <Text style={styles.compareHanzi}>{vocab.simplified}</Text>
                <Text style={styles.compareLabel}>AI read</Text>
                <Text style={styles.compareHanzi} testID="review-writing-recognized">
                  {result.recognized || '(unreadable)'}
                </Text>
              </>
            )}

            <Text style={styles.subScore}>
              Identity {result.identity_score}% · Quality {result.quality_score}%
            </Text>

            {result.feedback ? (
              <View style={styles.overallNotes}>
                <Ionicons
                  name={result.passed ? 'checkmark-circle' : 'information-circle'}
                  size={18}
                  color={result.passed ? colors.success : colors.warning}
                />
                <Text style={[styles.overallNotesText, { color: result.passed ? colors.success : colors.warning }]}>
                  {result.feedback}
                </Text>
              </View>
            ) : null}
          </View>
        )}
      </View>

      <View style={styles.footer}>
        {result ? (
          <View style={styles.actionRow}>
            <TouchableOpacity
              testID="review-mark-incorrect"
              style={[styles.actionBtn, styles.incorrectBtn]}
              onPress={() => onAnswered(vocab.id, false, 'writing')}
            >
              <Ionicons name="close" size={22} color={colors.error} />
              <Text style={[styles.actionLabel, { color: colors.error }]}>Incorrect</Text>
            </TouchableOpacity>
            <TouchableOpacity
              testID="review-mark-correct"
              style={[styles.actionBtn, result.passed ? styles.correctBtn : styles.correctBtnMuted]}
              onPress={() => onAnswered(vocab.id, true, 'writing')}
            >
              <Ionicons name="checkmark" size={22} color={colors.success} />
              <Text style={[styles.actionLabel, { color: colors.success }]}>
                {result.passed ? 'Correct' : 'Mark correct anyway'}
              </Text>
            </TouchableOpacity>
          </View>
        ) : (
          <TouchableOpacity
            testID="review-writing-submit"
            style={[styles.primaryBtn, submitting && styles.btnDisabled]}
            onPress={handleSubmit}
            disabled={submitting}
          >
            {submitting ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text style={styles.primaryBtnText}>Submit writing</Text>
            )}
          </TouchableOpacity>
        )}
      </View>
    </ScrollView>
  );
}
