import React, { useCallback, useEffect, useRef, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ActivityIndicator,
  ScrollView,
  TextInput,
  KeyboardAvoidingView,
  Platform,
  Linking,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useFocusEffect, useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import {
  AudioModule,
  useAudioRecorder,
  RecordingPresets,
  setAudioModeAsync,
} from 'expo-audio';
import { colors, spacing, radius, fontSize, getToneColor } from '@/src/theme';
import { api, Flashcard, Vocabulary } from '@/src/api/client';
import HandwritingCanvas, { HandwritingCanvasHandle } from '@/src/components/HandwritingCanvas';

type Mode = 'reading' | 'writing' | 'speaking';

type Card = {
  vocabulary: Vocabulary;
  current_stage: number | null;
  mode: Mode;
};

const STAGE_LABELS: Record<number, string> = {
  1: 'Stage 1 · 1 day',
  2: 'Stage 2 · 2 days',
  3: 'Stage 3 · 1 week',
  4: 'Stage 4 · 1 month',
  5: 'Stage 5 · 3 months',
  6: 'Stage 6 · 1 year',
};

const MODE_META: Record<Mode, { label: string; icon: keyof typeof Ionicons.glyphMap; description: string }> = {
  reading: { label: 'Reading', icon: 'book-outline', description: 'Type the English meaning' },
  writing: { label: 'Writing', icon: 'brush-outline', description: 'Handwrite the Chinese characters' },
  speaking: { label: 'Speaking', icon: 'mic-outline', description: 'Say the Chinese aloud' },
};

const MODES: Mode[] = ['reading', 'writing', 'speaking'];

function normalize(text: string): string {
  return (text || '').trim().toLowerCase();
}

function englishMatches(answer: string, target: string): boolean {
  const a = normalize(answer).replace(/[.;]+$/, '');
  // Allow any of the semicolon/comma-separated meanings
  const parts = target.split(/[;,/]|\bor\b/).map((s) => normalize(s).replace(/^(to |a |an |the )/, '').trim()).filter(Boolean);
  const cleaned = a.replace(/^(to |a |an |the )/, '').trim();
  return parts.some((p) => p === cleaned || cleaned === p.replace(/[.;]+$/, ''));
}

export default function ReviewScreen() {
  const router = useRouter();
  const [queue, setQueue] = useState<Card[]>([]);
  const [index, setIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [sessionStats, setSessionStats] = useState({ correct: 0, total: 0 });
  const [done, setDone] = useState(false);
  const [hasDeck, setHasDeck] = useState(true);

  const loadQueue = useCallback(async () => {
    setLoading(true);
    setDone(false);
    setIndex(0);
    setSessionStats({ correct: 0, total: 0 });
    try {
      const [due, fresh, deck] = await Promise.all([
        api.dueFlashcards(20),
        api.newFlashcards(10),
        api.deck().catch(() => []),
      ]);
      setHasDeck(deck.length > 0);
      const dueCards: Card[] = due.map((c: Flashcard) => ({
        vocabulary: c.vocabulary,
        current_stage: c.current_stage,
        mode: MODES[Math.floor(Math.random() * MODES.length)],
      }));
      const newCards: Card[] = fresh.map((v: Vocabulary) => ({
        vocabulary: v,
        current_stage: null,
        mode: MODES[Math.floor(Math.random() * MODES.length)],
      }));
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
    }, [loadQueue]),
  );

  const handleAnswered = async (vocabId: string, wasCorrect: boolean, mode: Mode) => {
    try {
      await api.reviewFlashcardWithMode(vocabId, wasCorrect, mode);
    } catch {
      // ignore
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
          <Text style={styles.emptySub}>
            No cards due. Visit Library to add more vocabulary.
          </Text>
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

  const card = queue[index];
  return (
    <SafeAreaView style={styles.safe} edges={['top']}>
      <View style={styles.header}>
        <View style={styles.progressBar}>
          <View
            style={[styles.progressFill, { width: `${((index + 1) / queue.length) * 100}%` }]}
          />
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

      <CardBody
        key={`${card.vocabulary.id}-${card.mode}-${index}`}
        card={card}
        onAnswered={handleAnswered}
      />
    </SafeAreaView>
  );
}

// =====================
// Card body
// =====================

function CardBody({
  card,
  onAnswered,
}: {
  card: Card;
  onAnswered: (vocabId: string, wasCorrect: boolean, mode: Mode) => void;
}) {
  if (card.mode === 'reading') return <ReadingCard card={card} onAnswered={onAnswered} />;
  if (card.mode === 'writing') return <WritingCard card={card} onAnswered={onAnswered} />;
  return <SpeakingCard card={card} onAnswered={onAnswered} />;
}

// ----- Reading mode -----
function ReadingCard({ card, onAnswered }: { card: Card; onAnswered: (id: string, ok: boolean, m: Mode) => void }) {
  const vocab = card.vocabulary;
  const [answer, setAnswer] = useState('');
  const [result, setResult] = useState<null | { correct: boolean }>(null);

  const handleCheck = () => {
    const ok = englishMatches(answer, vocab.english);
    setResult({ correct: ok });
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
            style={[styles.primaryBtn, !answer && styles.btnDisabled]}
            onPress={handleCheck}
            disabled={!answer}
          >
            <Text style={styles.primaryBtnText}>Check</Text>
          </TouchableOpacity>
        )}
      </View>
    </KeyboardAvoidingView>
  );
}

// ----- Writing mode -----
function WritingCard({ card, onAnswered }: { card: Card; onAnswered: (id: string, ok: boolean, m: Mode) => void }) {
  const vocab = card.vocabulary;
  const canvasRef = useRef<HandwritingCanvasHandle>(null);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<null | { correct: boolean; score: number; feedback: string; recognized: string }>(null);
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
      setResult({ correct: r.correct, score: r.score, feedback: r.feedback, recognized: r.recognized_text });
    } catch (e: any) {
      setError(e?.message || 'Recognition failed');
    } finally {
      setSubmitting(false);
    }
  };

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
          <View
            testID="review-writing-feedback"
            style={[styles.feedback, result.correct ? styles.feedbackCorrect : styles.feedbackIncorrect]}
          >
            <View style={styles.feedbackHeader}>
              <Ionicons
                name={result.correct ? 'checkmark-circle' : 'information-circle'}
                size={22}
                color={result.correct ? colors.success : colors.warning}
              />
              <Text style={[styles.feedbackTitle, { color: result.correct ? colors.success : colors.warning, flex: 1 }]}>
                {result.feedback}
              </Text>
            </View>
            <Text style={styles.compareLabel}>Target</Text>
            <Text style={styles.compareHanzi}>{vocab.simplified}</Text>
            <Text style={styles.compareLabel}>AI read</Text>
            <Text style={styles.compareHanzi} testID="review-writing-recognized">
              {result.recognized || '(unreadable)'}
            </Text>
            <Text style={styles.scoreText}>Match score: {result.score}%</Text>
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
              <Text style={[styles.actionLabel, { color: colors.error }]}>Mark incorrect</Text>
            </TouchableOpacity>
            <TouchableOpacity
              testID="review-mark-correct"
              style={[styles.actionBtn, styles.correctBtn]}
              onPress={() => onAnswered(vocab.id, true, 'writing')}
            >
              <Ionicons name="checkmark" size={22} color={colors.success} />
              <Text style={[styles.actionLabel, { color: colors.success }]}>Continue</Text>
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

// ----- Speaking mode -----
function SpeakingCard({ card, onAnswered }: { card: Card; onAnswered: (id: string, ok: boolean, m: Mode) => void }) {
  const vocab = card.vocabulary;
  const recorder = useAudioRecorder(RecordingPresets.HIGH_QUALITY);
  const [permission, setPermission] = useState<'undetermined' | 'granted' | 'denied' | 'blocked'>('undetermined');
  const [recording, setRecording] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<null | { correct: boolean; score: number; feedback: string; transcribed: string }>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        await setAudioModeAsync({ playsInSilentMode: true, allowsRecording: true });
        const status = await AudioModule.getRecordingPermissionsAsync();
        if (status.granted) setPermission('granted');
        else if (!status.canAskAgain) setPermission('blocked');
        else setPermission('undetermined');
      } catch {
        // ignore
      }
    })();
  }, []);

  const requestPermission = async () => {
    const status = await AudioModule.requestRecordingPermissionsAsync();
    if (status.granted) {
      setPermission('granted');
      return true;
    }
    setPermission(status.canAskAgain ? 'denied' : 'blocked');
    return false;
  };

  const startRec = async () => {
    setErrorMsg(null);
    setResult(null);
    if (permission !== 'granted') {
      const ok = await requestPermission();
      if (!ok) {
        setErrorMsg('Microphone access needed.');
        return;
      }
    }
    try {
      await recorder.prepareToRecordAsync();
      recorder.record();
      setRecording(true);
    } catch (e: any) {
      setErrorMsg(e?.message || 'Could not start recording');
    }
  };

  const stopAndUpload = async () => {
    setRecording(false);
    try {
      await recorder.stop();
      const uri = recorder.uri;
      if (!uri) {
        setErrorMsg('No audio captured.');
        return;
      }
      setUploading(true);
      const data = await api.transcribeAudio(uri, vocab.simplified, vocab.id);
      setResult({
        correct: !!data.correct,
        score: data.score ?? 0,
        feedback: data.feedback || 'Transcription complete',
        transcribed: data.transcribed_text || '',
      });
    } catch (e: any) {
      setErrorMsg(e?.message || 'Transcription failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.cardScroll}>
      <View style={styles.card}>
        <Text style={styles.englishPrompt}>{vocab.english}</Text>
        <Text style={styles.writePrompt}>Say the Chinese aloud</Text>

        {permission === 'blocked' && (
          <View style={[styles.feedback, styles.feedbackIncorrect]} testID="review-speaking-permission">
            <Ionicons name="alert-circle" size={22} color={colors.error} />
            <View style={styles.flex}>
              <Text style={[styles.feedbackTitle, { color: colors.error }]}>Microphone blocked</Text>
              <TouchableOpacity onPress={() => Linking.openSettings()} style={styles.settingsBtn}>
                <Text style={styles.settingsBtnText}>Open Settings</Text>
              </TouchableOpacity>
            </View>
          </View>
        )}

        {errorMsg && (
          <View style={[styles.feedback, styles.feedbackIncorrect]} testID="review-speaking-error">
            <Ionicons name="alert-circle" size={20} color={colors.error} />
            <Text style={[styles.feedbackTitle, { color: colors.error, flex: 1 }]}>{errorMsg}</Text>
          </View>
        )}

        {result && (
          <View
            testID="review-speaking-feedback"
            style={[styles.feedback, result.correct ? styles.feedbackCorrect : styles.feedbackIncorrect]}
          >
            <View style={styles.feedbackHeader}>
              <Ionicons
                name={result.correct ? 'checkmark-circle' : 'information-circle'}
                size={22}
                color={result.correct ? colors.success : colors.warning}
              />
              <Text style={[styles.feedbackTitle, { color: result.correct ? colors.success : colors.warning, flex: 1 }]}>
                {result.feedback}
              </Text>
            </View>
            <Text style={styles.compareLabel}>Target</Text>
            <Text style={styles.compareHanzi}>{vocab.simplified}</Text>
            <Text style={styles.compareLabel}>Whisper heard</Text>
            <Text style={styles.compareHanzi}>{result.transcribed || '(silence)'}</Text>
            <Text style={styles.scoreText}>Match score: {result.score}%</Text>
          </View>
        )}
      </View>

      <View style={styles.footer}>
        {result ? (
          <View style={styles.actionRow}>
            <TouchableOpacity
              testID="review-mark-incorrect"
              style={[styles.actionBtn, styles.incorrectBtn]}
              onPress={() => onAnswered(vocab.id, false, 'speaking')}
            >
              <Ionicons name="close" size={22} color={colors.error} />
              <Text style={[styles.actionLabel, { color: colors.error }]}>Mark incorrect</Text>
            </TouchableOpacity>
            <TouchableOpacity
              testID="review-mark-correct"
              style={[styles.actionBtn, styles.correctBtn]}
              onPress={() => onAnswered(vocab.id, true, 'speaking')}
            >
              <Ionicons name="checkmark" size={22} color={colors.success} />
              <Text style={[styles.actionLabel, { color: colors.success }]}>Continue</Text>
            </TouchableOpacity>
          </View>
        ) : recording ? (
          <TouchableOpacity
            testID="review-speak-stop"
            style={[styles.primaryBtn, { backgroundColor: colors.secondary }]}
            onPress={stopAndUpload}
          >
            <View style={styles.recordingDot} />
            <Text style={styles.primaryBtnText}>Stop & transcribe</Text>
          </TouchableOpacity>
        ) : uploading ? (
          <View style={[styles.primaryBtn, { backgroundColor: colors.textSecondary }]}>
            <ActivityIndicator color="#fff" />
            <Text style={styles.primaryBtnText}>Transcribing...</Text>
          </View>
        ) : (
          <TouchableOpacity testID="review-speak-record" style={styles.primaryBtn} onPress={startRec}>
            <Ionicons name="mic" size={20} color="#fff" />
            <Text style={styles.primaryBtnText}>Tap to record</Text>
          </TouchableOpacity>
        )}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.background },
  flex: { flex: 1 },
  loading: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: colors.background },
  header: { paddingHorizontal: spacing.lg, paddingTop: spacing.md, paddingBottom: spacing.sm, flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  progressBar: { flex: 1, height: 4, backgroundColor: colors.border, borderRadius: radius.full, overflow: 'hidden' },
  progressFill: { height: '100%', backgroundColor: colors.primary, borderRadius: radius.full },
  progressText: { fontSize: fontSize.sm, color: colors.textSecondary, fontWeight: '500' },
  modeBanner: {
    marginHorizontal: spacing.lg,
    marginTop: spacing.sm,
    padding: spacing.md,
    backgroundColor: colors.primaryLight,
    borderRadius: radius.lg,
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
  },
  modeLabel: { fontSize: fontSize.base, color: colors.textPrimary, fontWeight: '600' },
  modeDesc: { fontSize: fontSize.xs, color: colors.textSecondary, marginTop: 2 },
  stageLabel: { fontSize: 10, color: colors.textTertiary, textTransform: 'uppercase', letterSpacing: 1, fontWeight: '500' },
  cardScroll: { flexGrow: 1, padding: spacing.lg },
  card: { backgroundColor: colors.surface, borderRadius: radius.xl, borderWidth: 1, borderColor: colors.border, padding: spacing.lg, gap: spacing.sm },
  hanzi: { fontSize: fontSize.hanziLg, color: colors.textPrimary, fontWeight: '500', textAlign: 'center' },
  englishPrompt: { fontSize: fontSize.xxl, color: colors.textPrimary, fontWeight: '400', textAlign: 'center', marginTop: spacing.sm },
  pinyinSmall: { fontSize: fontSize.sm, color: colors.textTertiary, textAlign: 'center' },
  writePrompt: { fontSize: fontSize.xs, color: colors.textTertiary, textAlign: 'center', textTransform: 'uppercase', letterSpacing: 1, marginTop: spacing.md, marginBottom: spacing.sm },
  inputLabel: { fontSize: fontSize.sm, color: colors.textSecondary, fontWeight: '500', marginTop: spacing.lg },
  input: { borderBottomWidth: 2, borderBottomColor: colors.textPrimary, paddingVertical: spacing.md, fontSize: fontSize.xl, color: colors.textPrimary, textAlign: 'center', minHeight: 56 },
  inputCorrect: { borderBottomColor: colors.success },
  inputIncorrect: { borderBottomColor: colors.error },
  canvasWrap: { marginTop: spacing.md },
  feedback: { padding: spacing.md, borderRadius: radius.lg, marginTop: spacing.md, gap: spacing.xs, flexDirection: 'column' },
  feedbackHeader: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  feedbackCorrect: { backgroundColor: colors.successLight },
  feedbackIncorrect: { backgroundColor: colors.errorLight },
  feedbackTitle: { fontSize: fontSize.base, fontWeight: '600' },
  englishAnswer: { fontSize: fontSize.base, color: colors.textPrimary, marginTop: 4 },
  compareLabel: { fontSize: 10, color: colors.textTertiary, textTransform: 'uppercase', letterSpacing: 1, marginTop: spacing.sm },
  compareHanzi: { fontSize: fontSize.xl, color: colors.textPrimary, marginTop: 2 },
  scoreText: { fontSize: fontSize.sm, color: colors.textSecondary, marginTop: spacing.sm },
  settingsBtn: { backgroundColor: colors.primary, paddingHorizontal: spacing.md, paddingVertical: spacing.sm, borderRadius: radius.sm, alignSelf: 'flex-start', marginTop: spacing.sm, minHeight: 36, justifyContent: 'center' },
  settingsBtnText: { color: '#fff', fontWeight: '600', fontSize: fontSize.sm },
  footer: { padding: spacing.lg },
  primaryBtn: { backgroundColor: colors.primary, borderRadius: radius.md, paddingVertical: 16, alignItems: 'center', justifyContent: 'center', flexDirection: 'row', gap: spacing.sm, minHeight: 52 },
  primaryBtnText: { color: '#fff', fontSize: fontSize.lg, fontWeight: '600' },
  btnDisabled: { opacity: 0.5 },
  recordingDot: { width: 12, height: 12, borderRadius: 6, backgroundColor: '#fff' },
  actionRow: { flexDirection: 'row', gap: spacing.md },
  actionBtn: { flex: 1, borderRadius: radius.lg, padding: spacing.md, alignItems: 'center', gap: spacing.xs, minHeight: 64, justifyContent: 'center', flexDirection: 'row' },
  correctBtn: { backgroundColor: colors.successLight, borderWidth: 1, borderColor: colors.success },
  incorrectBtn: { backgroundColor: colors.errorLight, borderWidth: 1, borderColor: colors.error },
  actionLabel: { fontSize: fontSize.sm, fontWeight: '600' },
  emptyContainer: { flex: 1, alignItems: 'center', justifyContent: 'center', padding: spacing.xl },
  emptyHanzi: { fontSize: 88, color: colors.primary, fontWeight: '300', marginBottom: spacing.md },
  emptyTitle: { fontSize: fontSize.xxl, color: colors.textPrimary, fontWeight: '500' },
  emptySub: { fontSize: fontSize.base, color: colors.textSecondary, textAlign: 'center', marginTop: spacing.md, paddingHorizontal: spacing.xl, lineHeight: 22 },
  emptyBtn: { backgroundColor: colors.primary, paddingHorizontal: spacing.xl, paddingVertical: 14, borderRadius: radius.full, marginTop: spacing.xl, minHeight: 48, justifyContent: 'center' },
  emptyBtnSecondary: { backgroundColor: 'transparent', borderWidth: 1, borderColor: colors.primary, marginTop: spacing.md },
  emptyBtnText: { color: '#fff', fontSize: fontSize.base, fontWeight: '600' },
  emptyBtnTextSecondary: { color: colors.primary },
});
