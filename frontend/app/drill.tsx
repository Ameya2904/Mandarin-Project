import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  Linking,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useLocalSearchParams, useRouter, Stack } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import {
  AudioModule,
  useAudioRecorder,
  RecordingPresets,
  setAudioModeAsync,
} from 'expo-audio';
import { colors, spacing, radius, fontSize, getToneColor } from '@/src/theme';
import { api, Drill, Lesson } from '@/src/api/client';

export default function DrillScreen() {
  const router = useRouter();
  const { lesson } = useLocalSearchParams<{ lesson?: string }>();
  // When a lesson is passed in (e.g. from a lesson screen) we go straight to
  // its drills. Otherwise the learner first picks which lesson to drill.
  const [selectedLesson, setSelectedLesson] = useState<number | null>(
    lesson ? Number(lesson) : null
  );
  const [lessonOptions, setLessonOptions] = useState<Lesson[]>([]);
  const [drills, setDrills] = useState<Drill[]>([]);
  const [index, setIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [done, setDone] = useState(false);
  const [sessionStats, setSessionStats] = useState({ correct: 0, total: 0 });

  // Hint tiers: 0 = none, 1 = chinese characters, 2 = pinyin
  const [hintLevel, setHintLevel] = useState(0);

  // Audio recording state
  const recorder = useAudioRecorder(RecordingPresets.HIGH_QUALITY);
  const [permission, setPermission] = useState<'undetermined' | 'granted' | 'denied' | 'blocked'>('undetermined');
  const [recording, setRecording] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<null | { correct: boolean; score: number; feedback: string; transcribed: string; spokenPinyin: string; tonesWrong: number }>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Configure audio + check mic permission once.
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

  // Load the lesson picker list (when no lesson chosen) or the drills for the
  // chosen lesson.
  useEffect(() => {
    let cancelled = false;
    (async () => {
      setLoading(true);
      if (selectedLesson == null) {
        try {
          const ls = await api.lessons();
          if (!cancelled) setLessonOptions(ls);
        } catch {
          if (!cancelled) setLessonOptions([]);
        } finally {
          if (!cancelled) setLoading(false);
        }
        return;
      }
      try {
        const data = await api.drills(selectedLesson);
        if (!cancelled) setDrills(data);
      } catch {
        if (!cancelled) setDrills([]);
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [selectedLesson]);

  const startLesson = (lessonNumber: number) => {
    setDrills([]);
    setIndex(0);
    setDone(false);
    setSessionStats({ correct: 0, total: 0 });
    resetCard();
    setSelectedLesson(lessonNumber);
  };

  const current = drills[index];

  const resetCard = () => {
    setHintLevel(0);
    setResult(null);
    setErrorMsg(null);
    setRecording(false);
    setUploading(false);
  };

  const handleNext = () => {
    if (index + 1 >= drills.length) {
      setDone(true);
    } else {
      setIndex(index + 1);
      resetCard();
    }
  };

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

  const stopAndCheck = async () => {
    setRecording(false);
    if (!current) return;
    try {
      await recorder.stop();
      const uri = recorder.uri;
      if (!uri) {
        setErrorMsg('No audio captured. Try again.');
        return;
      }
      setUploading(true);
      const r = await api.transcribeAudio(uri, current.expected_answer);
      const isCorrect = !!r.correct;
      const fb = {
        correct: isCorrect,
        score: r.score ?? 0,
        feedback: r.feedback || 'Transcription complete',
        transcribed: r.transcribed_text || '',
        spokenPinyin: r.spoken_pinyin || '',
        tonesWrong: r.tones_wrong ?? 0,
      };
      setResult(fb);
      setSessionStats((s) => ({ correct: s.correct + (isCorrect ? 1 : 0), total: s.total + 1 }));

      try {
        await api.drillAttempt(current.id, r.transcribed_text || '', isCorrect);
      } catch {
        // ignore
      }
    } catch (e: any) {
      setErrorMsg(e?.message || 'Transcription failed');
    } finally {
      setUploading(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.loading}>
        <ActivityIndicator color={colors.primary} size="large" />
      </View>
    );
  }

  // Lesson picker — shown when no lesson was passed in.
  if (selectedLesson == null) {
    return (
      <SafeAreaView style={styles.safe} edges={['top']}>
        <Stack.Screen options={{ headerShown: false }} />
        <View style={styles.header}>
          <TouchableOpacity testID="drill-picker-close-button" onPress={() => router.back()} style={styles.backBtn}>
            <Ionicons name="close" size={24} color={colors.textPrimary} />
          </TouchableOpacity>
          <Text style={styles.pickerHeaderTitle}>Choose a lesson</Text>
        </View>
        <ScrollView contentContainerStyle={styles.pickerScroll}>
          <Text style={styles.pickerSubtitle}>Pick a lesson to practice its drills.</Text>
          {lessonOptions.length === 0 ? (
            <Text style={styles.pickerEmpty}>No lessons available yet.</Text>
          ) : (
            lessonOptions.map((l) => (
              <TouchableOpacity
                key={l.lesson_number}
                testID={`drill-lesson-option-${l.lesson_number}`}
                style={styles.lessonRow}
                onPress={() => startLesson(l.lesson_number)}
                activeOpacity={0.7}
              >
                <View style={styles.lessonNumBadge}>
                  <Text style={styles.lessonNumText}>{l.lesson_number}</Text>
                </View>
                <View style={styles.flex}>
                  <Text style={styles.lessonRowLabel}>Lesson {l.lesson_number}</Text>
                  <Text style={styles.lessonRowTitle} numberOfLines={1}>{l.title}</Text>
                </View>
                <Ionicons name="chevron-forward" size={18} color={colors.textTertiary} />
              </TouchableOpacity>
            ))
          )}
        </ScrollView>
      </SafeAreaView>
    );
  }

  if (drills.length === 0) {
    return (
      <SafeAreaView style={styles.safe} edges={['top']}>
        <View style={styles.empty}>
          <Text style={styles.emptyHanzi}>没有</Text>
          <Text style={styles.emptyTitle}>No drills available</Text>
          <TouchableOpacity
            testID="drill-back-button"
            style={styles.btn}
            onPress={() => (lesson ? router.back() : setSelectedLesson(null))}
          >
            <Text style={styles.btnText}>{lesson ? 'Go back' : 'Pick another lesson'}</Text>
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

      <View style={styles.header}>
        <TouchableOpacity testID="drill-close-button" onPress={() => router.back()} style={styles.backBtn}>
          <Ionicons name="close" size={24} color={colors.textPrimary} />
        </TouchableOpacity>
        <View style={styles.progressBar}>
          <View style={[styles.progressFill, { width: `${((index + 1) / drills.length) * 100}%` }]} />
        </View>
        <Text style={styles.progressText}>
          {index + 1}/{drills.length}
        </Text>
      </View>

      <ScrollView contentContainerStyle={styles.scroll}>
        <Text style={styles.drillType}>
          {current.drill_type === 'substitution' ? 'Substitution Drill' : current.drill_type === 'transformation' ? 'Transformation Drill' : 'Drill'}
        </Text>

        <View style={styles.promptCard} testID="drill-prompt-card">
          <Text style={styles.promptLabel}>Say this in Mandarin</Text>
          <Text style={styles.englishTarget}>{current.expected_english}</Text>
          <Text style={styles.instructionInline}>
            ({current.instruction_english})
          </Text>
        </View>

        {/* Hint tiers */}
        {!result && (
          <View style={styles.hintBlock} testID="drill-hint-block">
            {hintLevel >= 1 && (
              <View style={styles.hintRow}>
                <Text style={styles.hintLabel}>Characters</Text>
                <Text style={styles.hintHanzi}>{current.expected_answer}</Text>
              </View>
            )}
            {hintLevel >= 2 && (
              <View style={styles.hintRow}>
                <Text style={styles.hintLabel}>Pinyin</Text>
                <Text style={[styles.hintPinyin, { color: getToneColor(current.expected_pinyin) }]}>
                  {current.expected_pinyin}
                </Text>
              </View>
            )}
            {hintLevel < 2 && (
              <TouchableOpacity
                testID="drill-hint-button"
                style={styles.hintBtn}
                onPress={() => setHintLevel((h) => h + 1)}
              >
                <Ionicons name="bulb-outline" size={18} color={colors.warning} />
                <Text style={styles.hintBtnText}>
                  {hintLevel === 0 ? 'Show characters' : 'Show pinyin'}
                </Text>
              </TouchableOpacity>
            )}
          </View>
        )}

        {permission === 'blocked' && (
          <View style={[styles.feedback, styles.feedbackIncorrect]} testID="drill-permission-blocked">
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
          <View style={[styles.feedback, styles.feedbackIncorrect]} testID="drill-error">
            <Ionicons name="alert-circle" size={20} color={colors.error} />
            <Text style={[styles.feedbackTitle, { color: colors.error, flex: 1 }]}>{errorMsg}</Text>
          </View>
        )}

        {result && (
          <View
            testID="drill-feedback"
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
            {!result.correct && result.tonesWrong ? (
              <Text style={styles.toneNote} testID="drill-tone-note">
                {result.tonesWrong} {result.tonesWrong === 1 ? 'syllable has' : 'syllables have'} the
                right sound but the wrong tone — partial credit given.
              </Text>
            ) : null}
            <Text style={styles.compareLabel}>Target</Text>
            <Text style={styles.compareHanzi}>{current.expected_answer}</Text>
            <Text style={[styles.comparePinyin, { color: getToneColor(current.expected_pinyin) }]}>
              {current.expected_pinyin}
            </Text>
            <Text style={styles.compareLabel}>Heard</Text>
            <Text style={styles.compareHanzi}>{result.transcribed || '(silence)'}</Text>
            {result.spokenPinyin ? (
              <Text style={[styles.comparePinyin, { color: getToneColor(result.spokenPinyin) }]}>
                {result.spokenPinyin}
              </Text>
            ) : null}
            <Text style={styles.scoreText}>Match score: {result.score}%</Text>
            {hintLevel > 0 && (
              <Text style={styles.hintUsedNote}>
                {hintLevel === 1 ? '· Used character hint' : '· Used character + pinyin hint'}
              </Text>
            )}
          </View>
        )}
      </ScrollView>

      <View style={styles.footer}>
        {result ? (
          <TouchableOpacity testID="drill-next-button" style={styles.primaryBtn} onPress={handleNext}>
            <Text style={styles.primaryBtnText}>
              {index + 1 >= drills.length ? 'Finish' : 'Next'}
            </Text>
            <Ionicons name="arrow-forward" size={20} color="#fff" />
          </TouchableOpacity>
        ) : recording ? (
          <TouchableOpacity
            testID="drill-stop-record-button"
            style={[styles.primaryBtn, { backgroundColor: colors.secondary }]}
            onPress={stopAndCheck}
          >
            <View style={styles.recordingDot} />
            <Text style={styles.primaryBtnText}>Stop & check</Text>
          </TouchableOpacity>
        ) : uploading ? (
          <View style={[styles.primaryBtn, { backgroundColor: colors.textSecondary }]}>
            <ActivityIndicator color="#fff" />
            <Text style={styles.primaryBtnText}>Transcribing...</Text>
          </View>
        ) : (
          <TouchableOpacity testID="drill-record-button" style={styles.primaryBtn} onPress={startRec}>
            <Ionicons name="mic" size={20} color="#fff" />
            <Text style={styles.primaryBtnText}>Tap to speak</Text>
          </TouchableOpacity>
        )}
      </View>
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
  promptCard: { backgroundColor: colors.surface, borderRadius: radius.xl, borderWidth: 1, borderColor: colors.border, padding: spacing.lg, alignItems: 'center' },
  promptLabel: { fontSize: fontSize.xs, color: colors.textTertiary, letterSpacing: 1, textTransform: 'uppercase' },
  englishTarget: { fontSize: fontSize.xxl, color: colors.textPrimary, fontWeight: '500', marginTop: spacing.md, textAlign: 'center' },
  instructionInline: { fontSize: fontSize.sm, color: colors.textSecondary, marginTop: spacing.md, textAlign: 'center', fontStyle: 'italic' },
  hintBlock: { marginTop: spacing.lg, gap: spacing.sm },
  hintRow: { backgroundColor: colors.surfaceAlt, padding: spacing.md, borderRadius: radius.md, alignItems: 'center' },
  hintLabel: { fontSize: fontSize.xs, color: colors.textTertiary, textTransform: 'uppercase', letterSpacing: 1, marginBottom: 4 },
  hintHanzi: { fontSize: fontSize.xl, color: colors.textPrimary },
  hintPinyin: { fontSize: fontSize.base, fontWeight: '500' },
  hintBtn: { flexDirection: 'row', alignItems: 'center', alignSelf: 'center', gap: spacing.xs, paddingHorizontal: spacing.md, paddingVertical: spacing.sm, borderRadius: radius.full, borderWidth: 1, borderColor: colors.warning, backgroundColor: '#FDF4DD', minHeight: 36 },
  hintBtnText: { color: colors.warning, fontSize: fontSize.sm, fontWeight: '600' },
  feedback: { padding: spacing.md, borderRadius: radius.lg, marginTop: spacing.lg, gap: spacing.xs, flexDirection: 'column' },
  feedbackHeader: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  feedbackCorrect: { backgroundColor: colors.successLight },
  feedbackIncorrect: { backgroundColor: colors.errorLight },
  feedbackTitle: { fontSize: fontSize.base, fontWeight: '600' },
  compareLabel: { fontSize: 10, color: colors.textTertiary, textTransform: 'uppercase', letterSpacing: 1, marginTop: spacing.sm },
  compareHanzi: { fontSize: fontSize.xl, color: colors.textPrimary, marginTop: 2 },
  comparePinyin: { fontSize: fontSize.sm, marginTop: 2 },
  scoreText: { fontSize: fontSize.sm, color: colors.textSecondary, marginTop: spacing.sm },
  toneNote: { fontSize: fontSize.sm, color: colors.textSecondary, fontStyle: 'italic', marginBottom: spacing.xs },
  hintUsedNote: { fontSize: fontSize.xs, color: colors.textTertiary, marginTop: 4, fontStyle: 'italic' },
  settingsBtn: { backgroundColor: colors.primary, paddingHorizontal: spacing.md, paddingVertical: spacing.sm, borderRadius: radius.sm, alignSelf: 'flex-start', marginTop: spacing.sm, minHeight: 36, justifyContent: 'center' },
  settingsBtnText: { color: '#fff', fontWeight: '600', fontSize: fontSize.sm },
  footer: { padding: spacing.lg },
  primaryBtn: { backgroundColor: colors.primary, borderRadius: radius.md, paddingVertical: 16, alignItems: 'center', justifyContent: 'center', flexDirection: 'row', gap: spacing.sm, minHeight: 52 },
  primaryBtnText: { color: '#fff', fontSize: fontSize.lg, fontWeight: '600' },
  recordingDot: { width: 12, height: 12, borderRadius: 6, backgroundColor: '#fff' },
  pickerHeaderTitle: { fontSize: fontSize.lg, color: colors.textPrimary, fontWeight: '600' },
  pickerScroll: { padding: spacing.lg, paddingTop: 0 },
  pickerSubtitle: { fontSize: fontSize.base, color: colors.textSecondary, marginBottom: spacing.md },
  pickerEmpty: { fontSize: fontSize.base, color: colors.textTertiary, textAlign: 'center', marginTop: spacing.xl },
  lessonRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
    backgroundColor: colors.surface,
    borderRadius: radius.lg,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.md,
    marginBottom: spacing.sm,
    minHeight: 60,
  },
  lessonNumBadge: {
    width: 40,
    height: 40,
    borderRadius: radius.md,
    backgroundColor: colors.primaryLight,
    alignItems: 'center',
    justifyContent: 'center',
  },
  lessonNumText: { fontSize: fontSize.base, fontWeight: '700', color: colors.primary },
  lessonRowLabel: { fontSize: fontSize.xs, color: colors.textTertiary, textTransform: 'uppercase', letterSpacing: 1, fontWeight: '600' },
  lessonRowTitle: { fontSize: fontSize.base, color: colors.textPrimary, fontWeight: '500', marginTop: 1 },
  empty: { flex: 1, alignItems: 'center', justifyContent: 'center', padding: spacing.xl },
  emptyHanzi: { fontSize: 88, color: colors.primary, fontWeight: '300', marginBottom: spacing.md },
  emptyTitle: { fontSize: fontSize.xxl, color: colors.textPrimary, fontWeight: '500' },
  emptySub: { fontSize: fontSize.base, color: colors.textSecondary, textAlign: 'center', marginTop: spacing.md },
  btn: { backgroundColor: colors.primary, paddingHorizontal: spacing.xl, paddingVertical: 14, borderRadius: radius.full, marginTop: spacing.xl, minHeight: 48, justifyContent: 'center' },
  btnText: { color: '#fff', fontSize: fontSize.base, fontWeight: '600' },
});
