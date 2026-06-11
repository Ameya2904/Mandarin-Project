import React, { useEffect, useState } from 'react';
import { View, Text, TouchableOpacity, ActivityIndicator, ScrollView, Linking } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import {
  AudioModule,
  useAudioRecorder,
  RecordingPresets,
  setAudioModeAsync,
} from 'expo-audio';
import { colors } from '@/src/theme';
import { api } from '@/src/api/client';
import { styles } from './review.styles';
import type { Card, OnAnswered } from './types';

type SpeakingResult = {
  correct: boolean;
  score: number;
  feedback: string;
  transcribed: string;
  spokenPinyin: string;
  targetPinyin: string;
  tonesWrong: number;
};

export default function SpeakingCard({ card, onAnswered }: { card: Card; onAnswered: OnAnswered }) {
  const vocab = card.vocabulary;
  const recorder = useAudioRecorder(RecordingPresets.HIGH_QUALITY);
  const [permission, setPermission] = useState<'undetermined' | 'granted' | 'denied' | 'blocked'>('undetermined');
  const [recording, setRecording] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<SpeakingResult | null>(null);
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
      // expo-audio's stop() can resolve before the file is fully flushed to
      // disk. Give it a brief moment so the upload can read a complete file;
      // the API layer also retries on a dropped read as a safety net.
      await new Promise((r) => setTimeout(r, 250));
      setUploading(true);
      const data = await api.transcribeAudio(uri, vocab.simplified, vocab.id);
      setResult({
        correct: !!data.correct,
        score: data.score ?? 0,
        feedback: data.feedback || 'Transcription complete',
        transcribed: data.transcribed_text || '',
        spokenPinyin: data.spoken_pinyin || '',
        targetPinyin: data.target_pinyin || '',
        tonesWrong: data.tones_wrong ?? 0,
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
            {result.targetPinyin ? <Text style={styles.pinyinSmall}>{result.targetPinyin}</Text> : null}
            <Text style={styles.compareLabel}>AI heard</Text>
            <Text style={styles.compareHanzi}>{result.transcribed || '(silence)'}</Text>
            {result.spokenPinyin ? (
              <Text
                style={[
                  styles.pinyinSmall,
                  { color: result.spokenPinyin === result.targetPinyin ? colors.success : colors.error },
                ]}
              >
                {result.spokenPinyin}
              </Text>
            ) : null}
            <Text style={styles.scoreText}>Match score: {result.score}%</Text>
            {!result.correct && result.tonesWrong ? (
              <Text style={styles.toneNote} testID="review-speaking-tone-note">
                {result.tonesWrong} {result.tonesWrong === 1 ? 'syllable has' : 'syllables have'} the
                right sound but the wrong tone — partial credit given.
              </Text>
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
