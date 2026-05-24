import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  Platform,
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
import { api } from '@/src/api/client';

type Result = {
  transcribed_text: string;
  correct?: boolean;
  score?: number;
  feedback?: string;
  target_text?: string;
};

export default function SpeakPracticeScreen() {
  const router = useRouter();
  const params = useLocalSearchParams<{ chinese: string; pinyin: string; english: string }>();
  const target = String(params.chinese || '');
  const pinyin = String(params.pinyin || '');
  const english = String(params.english || '');

  const recorder = useAudioRecorder(RecordingPresets.HIGH_QUALITY);

  const [revealed, setRevealed] = useState(false);
  const [permission, setPermission] = useState<'undetermined' | 'granted' | 'denied' | 'blocked'>('undetermined');
  const [recording, setRecording] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<Result | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Configure audio mode and check existing permission state.
  useEffect(() => {
    (async () => {
      try {
        await setAudioModeAsync({
          playsInSilentMode: true,
          allowsRecording: true,
        });
        const status = await AudioModule.getRecordingPermissionsAsync();
        if (status.granted) setPermission('granted');
        else if (!status.canAskAgain) setPermission('blocked');
        else setPermission('undetermined');
      } catch (e) {
        // ignore
      }
    })();
  }, []);

  const requestPermission = useCallback(async () => {
    try {
      const status = await AudioModule.requestRecordingPermissionsAsync();
      if (status.granted) {
        setPermission('granted');
        return true;
      }
      setPermission(status.canAskAgain ? 'denied' : 'blocked');
      return false;
    } catch (e) {
      setPermission('denied');
      return false;
    }
  }, []);

  const handleStartRecording = async () => {
    setErrorMsg(null);
    setResult(null);
    if (permission !== 'granted') {
      const ok = await requestPermission();
      if (!ok) {
        setErrorMsg('Microphone access is needed to practice pronunciation.');
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

  const handleStopAndUpload = async () => {
    if (!recording) return;
    setRecording(false);
    try {
      await recorder.stop();
      const uri = recorder.uri;
      if (!uri) {
        setErrorMsg('No audio captured. Try again.');
        return;
      }
      setUploading(true);
      const data = await api.transcribeAudio(uri, target);
      setResult(data);
    } catch (e: any) {
      setErrorMsg(e?.message || 'Transcription failed');
    } finally {
      setUploading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setErrorMsg(null);
    setRevealed(false);
  };

  const renderRecordButton = () => {
    if (uploading) {
      return (
        <View style={[styles.recordBtn, styles.recordBtnUploading]}>
          <ActivityIndicator color="#fff" />
          <Text style={styles.recordBtnLabel}>Transcribing...</Text>
        </View>
      );
    }
    if (recording) {
      return (
        <TouchableOpacity
          testID="speak-stop-record-button"
          style={[styles.recordBtn, styles.recordBtnActive]}
          onPress={handleStopAndUpload}
        >
          <View style={styles.recordingDot} />
          <Text style={styles.recordBtnLabel}>Tap to stop & transcribe</Text>
        </TouchableOpacity>
      );
    }
    return (
      <TouchableOpacity
        testID="speak-record-audio-button"
        style={styles.recordBtn}
        onPress={handleStartRecording}
      >
        <Ionicons name="mic" size={28} color="#fff" />
        <Text style={styles.recordBtnLabel}>Tap to record</Text>
      </TouchableOpacity>
    );
  };

  return (
    <SafeAreaView style={styles.safe} edges={['top']}>
      <Stack.Screen options={{ headerShown: false }} />
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

      <ScrollView contentContainerStyle={styles.scroll}>
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

        {permission === 'blocked' && (
          <View style={[styles.feedback, styles.feedbackIncorrect]} testID="speak-permission-blocked">
            <Ionicons name="alert-circle" size={22} color={colors.error} />
            <View style={styles.flex}>
              <Text style={[styles.feedbackTitle, { color: colors.error }]}>
                Microphone access is blocked
              </Text>
              <Text style={styles.feedbackSub}>
                Open Settings to enable microphone for SpacedChinese.
              </Text>
              <TouchableOpacity
                testID="speak-open-settings-button"
                onPress={() => Linking.openSettings()}
                style={styles.settingsBtn}
              >
                <Text style={styles.settingsBtnText}>Open Settings</Text>
              </TouchableOpacity>
            </View>
          </View>
        )}

        {errorMsg && permission !== 'blocked' && (
          <View style={[styles.feedback, styles.feedbackIncorrect]} testID="speak-error">
            <Ionicons name="alert-circle" size={22} color={colors.error} />
            <Text style={[styles.feedbackTitle, { color: colors.error, flex: 1 }]}>
              {errorMsg}
            </Text>
          </View>
        )}

        {result && (
          <View
            testID="speak-feedback"
            style={[
              styles.feedback,
              result.correct ? styles.feedbackCorrect : styles.feedbackIncorrect,
            ]}
          >
            <View style={styles.feedbackHeader}>
              <Ionicons
                name={result.correct ? 'checkmark-circle' : 'information-circle'}
                size={24}
                color={result.correct ? colors.success : colors.warning}
              />
              <Text
                style={[
                  styles.feedbackTitle,
                  { color: result.correct ? colors.success : colors.warning, flex: 1 },
                ]}
              >
                {result.feedback || 'Transcription complete'}
              </Text>
            </View>
            {typeof result.score === 'number' && (
              <>
                <View style={styles.scoreBar}>
                  <View
                    style={[
                      styles.scoreFill,
                      {
                        width: `${result.score}%`,
                        backgroundColor: result.correct ? colors.success : colors.warning,
                      },
                    ]}
                  />
                </View>
                <Text style={styles.scoreText}>Match score: {result.score}%</Text>
              </>
            )}
            <View style={styles.compareBlock}>
              <Text style={styles.compareLabel}>Target</Text>
              <Text style={styles.compareHanzi}>{target}</Text>
              <Text style={styles.compareLabel}>Whisper heard</Text>
              <Text style={styles.compareHanzi} testID="speak-transcribed-text">
                {result.transcribed_text || '(silence)'}
              </Text>
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
          <View style={styles.recordWrap}>
            {renderRecordButton()}
            {Platform.OS === 'web' && (
              <Text style={styles.hint} testID="speak-web-hint">
                Web recording works on Chrome/Firefox. Allow microphone when prompted.
              </Text>
            )}
          </View>
        )}
      </View>
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
  hint: { fontSize: fontSize.xs, color: colors.textTertiary, marginTop: spacing.sm, textAlign: 'center' },
  targetCard: {
    backgroundColor: colors.surface,
    borderRadius: radius.xl,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.lg,
    alignItems: 'center',
    minHeight: 200,
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
  feedback: { padding: spacing.md, borderRadius: radius.lg, marginTop: spacing.lg, gap: spacing.sm, flexDirection: 'row' },
  feedbackCorrect: { backgroundColor: colors.successLight, flexDirection: 'column' },
  feedbackIncorrect: { backgroundColor: colors.errorLight, flexDirection: 'column' },
  feedbackHeader: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  feedbackTitle: { fontSize: fontSize.base, fontWeight: '600' },
  feedbackSub: { fontSize: fontSize.sm, color: colors.textSecondary, marginTop: 4 },
  scoreBar: {
    height: 6,
    backgroundColor: 'rgba(0,0,0,0.06)',
    borderRadius: radius.full,
    overflow: 'hidden',
    marginTop: spacing.md,
  },
  scoreFill: { height: '100%', borderRadius: radius.full },
  scoreText: { fontSize: fontSize.sm, color: colors.textSecondary, marginTop: 6 },
  compareBlock: { marginTop: spacing.md },
  compareLabel: {
    fontSize: fontSize.xs,
    color: colors.textTertiary,
    marginTop: spacing.sm,
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  compareHanzi: { fontSize: fontSize.xl, color: colors.textPrimary, marginTop: 2 },
  footer: { padding: spacing.lg },
  recordWrap: { alignItems: 'center', gap: spacing.sm },
  recordBtn: {
    width: '100%',
    backgroundColor: colors.primary,
    borderRadius: radius.full,
    paddingVertical: 18,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.sm,
    minHeight: 60,
  },
  recordBtnActive: { backgroundColor: colors.secondary },
  recordBtnUploading: { backgroundColor: colors.textSecondary },
  recordBtnLabel: { color: '#fff', fontSize: fontSize.base, fontWeight: '600' },
  recordingDot: { width: 14, height: 14, borderRadius: 7, backgroundColor: '#fff' },
  settingsBtn: {
    marginTop: spacing.sm,
    backgroundColor: colors.primary,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: radius.sm,
    alignSelf: 'flex-start',
    minHeight: 36,
    justifyContent: 'center',
  },
  settingsBtnText: { color: '#fff', fontSize: fontSize.sm, fontWeight: '600' },
  footerRow: { flexDirection: 'row', gap: spacing.md },
  btn: { flex: 1, paddingVertical: 16, borderRadius: radius.md, alignItems: 'center', justifyContent: 'center', minHeight: 52 },
  btnPrimary: { backgroundColor: colors.primary },
  btnSecondary: { backgroundColor: 'transparent', borderWidth: 1, borderColor: colors.primary },
  btnText: { fontSize: fontSize.base, fontWeight: '600' },
});
