// Shared microphone-capture state machine for pronunciation practice.
//
// Three screens (review SpeakingCard, drill, speak-practice) all need the same
// flow: configure the audio mode, track mic permission, record, then stop and
// upload to /api/speaking/transcribe. This hook owns that flow; callers only
// decide what to do with the returned transcription.
//
// Usage:
//   const mic = useAudioCapture();
//   await mic.startRecording();
//   const data = await mic.stopAndTranscribe(targetChinese, vocabId);
import { useCallback, useEffect, useState } from 'react';
import { Linking } from 'react-native';
import {
  AudioModule,
  useAudioRecorder,
  RecordingPresets,
  setAudioModeAsync,
} from 'expo-audio';
import { api } from '@/src/api/client';

export type MicPermission = 'undetermined' | 'granted' | 'denied' | 'blocked';

/** The shape returned by the transcribe endpoint (and thus stopAndTranscribe). */
export type TranscribeResult = Awaited<ReturnType<typeof api.transcribeAudio>>;

export type AudioCapture = {
  permission: MicPermission;
  recording: boolean;
  uploading: boolean;
  error: string | null;
  setError: (msg: string | null) => void;
  /** Begin recording. Returns false (and sets `error`) if mic access is denied. */
  startRecording: () => Promise<boolean>;
  /** Stop, upload, and return the transcription — or null if it failed (see `error`). */
  stopAndTranscribe: (target: string, vocabularyId?: string) => Promise<TranscribeResult | null>;
  /** Open the OS settings page so the user can unblock the mic. */
  openSettings: () => void;
};

export function useAudioCapture(): AudioCapture {
  const recorder = useAudioRecorder(RecordingPresets.HIGH_QUALITY);
  const [permission, setPermission] = useState<MicPermission>('undetermined');
  const [recording, setRecording] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Configure the audio session and read the current permission state once.
  useEffect(() => {
    (async () => {
      try {
        await setAudioModeAsync({ playsInSilentMode: true, allowsRecording: true });
        const status = await AudioModule.getRecordingPermissionsAsync();
        if (status.granted) setPermission('granted');
        else if (!status.canAskAgain) setPermission('blocked');
        else setPermission('undetermined');
      } catch {
        // ignore — permission stays 'undetermined' and is requested on first record
      }
    })();
  }, []);

  const ensurePermission = useCallback(async () => {
    if (permission === 'granted') return true;
    try {
      const status = await AudioModule.requestRecordingPermissionsAsync();
      if (status.granted) {
        setPermission('granted');
        return true;
      }
      setPermission(status.canAskAgain ? 'denied' : 'blocked');
      return false;
    } catch {
      setPermission('denied');
      return false;
    }
  }, [permission]);

  const startRecording = useCallback(async () => {
    setError(null);
    if (!(await ensurePermission())) {
      setError('Microphone access is needed to practice pronunciation.');
      return false;
    }
    try {
      await recorder.prepareToRecordAsync();
      recorder.record();
      setRecording(true);
      return true;
    } catch (e: any) {
      setError(e?.message || 'Could not start recording');
      return false;
    }
  }, [ensurePermission, recorder]);

  const stopAndTranscribe = useCallback(
    async (target: string, vocabularyId?: string): Promise<TranscribeResult | null> => {
      setRecording(false);
      try {
        await recorder.stop();
        const uri = recorder.uri;
        if (!uri) {
          setError('No audio captured. Try again.');
          return null;
        }
        // expo-audio's stop() can resolve before the file is flushed to disk;
        // wait briefly so the upload reads a complete file (the API layer also
        // retries a dropped read as a safety net).
        await new Promise((r) => setTimeout(r, 250));
        setUploading(true);
        return await api.transcribeAudio(uri, target, vocabularyId);
      } catch (e: any) {
        setError(e?.message || 'Transcription failed');
        return null;
      } finally {
        setUploading(false);
      }
    },
    [recorder],
  );

  const openSettings = useCallback(() => Linking.openSettings(), []);

  return {
    permission,
    recording,
    uploading,
    error,
    setError,
    startRecording,
    stopAndTranscribe,
    openSettings,
  };
}
