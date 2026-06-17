/**
 * Lesson detail — dialogue (split by part), grammar notes, and the vocab list.
 *
 * Deck membership is edited in place with optimistic updates (the `in_deck`
 * flag is flipped locally before the request resolves) so toggles feel instant.
 */
import React, { useCallback, useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useLocalSearchParams, useRouter, Stack } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { colors, spacing, radius, fontSize, getToneColor } from '@/src/theme';
import { api, Lesson } from '@/src/api/client';

export default function LessonDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const router = useRouter();
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [loading, setLoading] = useState(true);
  const [adding, setAdding] = useState(false);

  const load = useCallback(async () => {
    if (!id) return;
    try {
      const data = await api.lesson(id);
      setLesson(data);
    } catch (e) {
      setLesson(null);
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    load();
  }, [load]);

  const handleAddAll = async () => {
    if (!lesson?.vocabulary) return;
    setAdding(true);
    try {
      const ids = lesson.vocabulary.filter((v: any) => !v.in_deck).map((v) => v.id);
      if (ids.length > 0) await api.addToDeck(ids);
      await load();
    } finally {
      setAdding(false);
    }
  };

  const handleAddOne = async (vocabId: string) => {
    try {
      await api.addToDeck([vocabId]);
      setLesson((prev) => {
        if (!prev?.vocabulary) return prev;
        return {
          ...prev,
          vocabulary: prev.vocabulary.map((v: any) => (v.id === vocabId ? { ...v, in_deck: true } : v)),
        };
      });
    } catch {}
  };

  const handleRemoveOne = async (vocabId: string) => {
    try {
      await api.removeFromDeck(vocabId);
      setLesson((prev) => {
        if (!prev?.vocabulary) return prev;
        return {
          ...prev,
          vocabulary: prev.vocabulary.map((v: any) => (v.id === vocabId ? { ...v, in_deck: false } : v)),
        };
      });
    } catch {}
  };

  if (loading) {
    return (
      <View style={styles.loading}>
        <ActivityIndicator color={colors.primary} size="large" />
      </View>
    );
  }

  if (!lesson) {
    return (
      <SafeAreaView style={styles.safe} edges={['top']}>
        <View style={styles.loading}>
          <Text style={styles.notFound}>Lesson not found</Text>
        </View>
      </SafeAreaView>
    );
  }

  const notInDeckCount = (lesson.vocabulary || []).filter((v: any) => !v.in_deck).length;

  return (
    <SafeAreaView style={styles.safe} edges={['top']}>
      <Stack.Screen options={{ headerShown: false }} />
      <View style={styles.header}>
        <TouchableOpacity testID="lesson-back-button" onPress={() => router.back()} style={styles.backBtn}>
          <Ionicons name="arrow-back" size={24} color={colors.textPrimary} />
        </TouchableOpacity>
        <Text style={styles.lessonNumber}>Lesson {lesson.lesson_number}</Text>
      </View>

      <ScrollView contentContainerStyle={styles.scroll}>
        <Text style={styles.title}>{lesson.title}</Text>
        <Text style={styles.subtitle}>{lesson.subtitle}</Text>
        <Text style={styles.description}>{lesson.description}</Text>

        <View style={styles.ctaRow}>
          <TouchableOpacity
            testID="lesson-add-all-btn"
            style={[styles.ctaBtn, (adding || notInDeckCount === 0) && styles.ctaDisabled]}
            onPress={handleAddAll}
            disabled={adding || notInDeckCount === 0}
          >
            {adding ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <>
                <Ionicons name="add-circle-outline" size={20} color="#fff" />
                <Text style={styles.ctaText}>
                  {notInDeckCount === 0 ? 'All in deck' : `Add ${notInDeckCount} to deck`}
                </Text>
              </>
            )}
          </TouchableOpacity>
          <TouchableOpacity
            testID="lesson-practice-drill-btn"
            style={[styles.ctaBtn, styles.ctaSecondary]}
            onPress={() => router.push({ pathname: '/drill', params: { lesson: String(lesson.lesson_number) } })}
          >
            <Ionicons name="construct-outline" size={20} color={colors.primary} />
            <Text style={[styles.ctaText, { color: colors.primary }]}>Drills</Text>
          </TouchableOpacity>
        </View>

        {lesson.dialogue && lesson.dialogue.length > 0 && (
          <>
            <Text style={styles.sectionTitle}>Dialogue · 对话</Text>
            {[1, 2].map((part) => {
              const lines = lesson.dialogue!.filter((l: any) => l.part === part);
              if (lines.length === 0) return null;
              return (
                <View key={part} style={styles.dialoguePart}>
                  <Text style={styles.partLabel}>Part {part}</Text>
                  <View style={styles.dialogueCard}>
                    {lines.map((line: any, i: number) => (
                      <View key={i} style={[styles.dialogueRow, i === lines.length - 1 && styles.lastDialogueRow]}>
                        <Text style={styles.dialogueSpeaker}>{line.speaker}</Text>
                        <Text style={styles.dialogueHanzi}>{line.chinese}</Text>
                        <Text style={[styles.dialoguePinyin, { color: getToneColor(line.pinyin) }]}>
                          {line.pinyin}
                        </Text>
                        <Text style={styles.dialogueEnglish}>{line.english}</Text>
                      </View>
                    ))}
                  </View>
                </View>
              );
            })}
          </>
        )}

        {lesson.grammar_notes && lesson.grammar_notes.length > 0 && (
          <>
            <Text style={styles.sectionTitle}>Grammar · 语法</Text>
            {lesson.grammar_notes.map((note, i) => (
              <View key={i} style={styles.grammarCard}>
                <Text style={styles.grammarTitle}>{note.title}</Text>
                <Text style={styles.grammarText}>{note.explanation}</Text>
              </View>
            ))}
          </>
        )}

        {lesson.vocabulary && lesson.vocabulary.length > 0 && (
          <>
            <Text style={styles.sectionTitle}>Vocabulary · 生词 ({lesson.vocabulary.length})</Text>
            <View style={styles.vocabList}>
              {lesson.vocabulary.map((v: any, i: number) => (
                <View key={v.id} style={[styles.vocabRow, i === lesson.vocabulary!.length - 1 && styles.lastRow]}>
                  <Text style={styles.vocabHanzi}>{v.simplified}</Text>
                  <View style={styles.flex}>
                    <Text style={[styles.vocabPinyin, { color: getToneColor(v.pinyin) }]}>{v.pinyin}</Text>
                    <Text style={styles.vocabEnglish}>{v.english}</Text>
                  </View>
                  {v.in_deck ? (
                    <TouchableOpacity
                      testID={`lesson-remove-${v.simplified}`}
                      onPress={() => handleRemoveOne(v.id)}
                      style={styles.deckBadge}
                    >
                      <Ionicons name="checkmark-circle" size={18} color={colors.success} />
                      <Text style={styles.deckBadgeText}>In deck</Text>
                    </TouchableOpacity>
                  ) : (
                    <TouchableOpacity
                      testID={`lesson-add-${v.simplified}`}
                      onPress={() => handleAddOne(v.id)}
                      style={styles.addBtn}
                    >
                      <Ionicons name="add" size={20} color={colors.primary} />
                    </TouchableOpacity>
                  )}
                </View>
              ))}
            </View>
          </>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.background },
  flex: { flex: 1 },
  loading: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  notFound: { color: colors.textSecondary },
  header: { flexDirection: 'row', alignItems: 'center', padding: spacing.md, gap: spacing.sm },
  backBtn: { padding: spacing.sm, minWidth: 48, minHeight: 48, justifyContent: 'center' },
  lessonNumber: { fontSize: fontSize.sm, color: colors.textSecondary, fontWeight: '500', letterSpacing: 1, textTransform: 'uppercase' },
  scroll: { padding: spacing.lg, paddingTop: 0, paddingBottom: spacing.xxl },
  title: { fontSize: fontSize.display, color: colors.textPrimary, fontWeight: '500', letterSpacing: -0.5 },
  subtitle: { fontSize: fontSize.base, color: colors.primary, marginTop: 4, fontWeight: '500' },
  description: { fontSize: fontSize.base, color: colors.textSecondary, marginTop: spacing.md, lineHeight: 22 },
  ctaRow: { flexDirection: 'row', gap: spacing.md, marginTop: spacing.lg },
  ctaBtn: { flex: 1, backgroundColor: colors.primary, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', paddingVertical: 14, borderRadius: radius.md, gap: spacing.sm, minHeight: 48 },
  ctaSecondary: { backgroundColor: 'transparent', borderWidth: 1, borderColor: colors.primary },
  ctaDisabled: { opacity: 0.5 },
  ctaText: { color: '#fff', fontWeight: '600', fontSize: fontSize.base },
  sectionTitle: { fontSize: fontSize.base, color: colors.textSecondary, fontWeight: '500', marginTop: spacing.xl, marginBottom: spacing.md, letterSpacing: 0.5, textTransform: 'uppercase' },
  dialoguePart: { marginBottom: spacing.md },
  partLabel: { fontSize: fontSize.xs, color: colors.textTertiary, fontWeight: '600', letterSpacing: 1, textTransform: 'uppercase', marginBottom: spacing.sm },
  dialogueCard: { backgroundColor: colors.surface, borderRadius: radius.lg, borderWidth: 1, borderColor: colors.border, padding: spacing.md, gap: spacing.md },
  dialogueRow: { paddingBottom: spacing.md, borderBottomWidth: 1, borderBottomColor: colors.border },
  lastDialogueRow: { paddingBottom: 0, borderBottomWidth: 0 },
  dialogueSpeaker: { fontSize: fontSize.xs, color: colors.textTertiary, fontWeight: '500', marginBottom: 4 },
  dialogueHanzi: { fontSize: fontSize.xl, color: colors.textPrimary, marginBottom: 4 },
  dialoguePinyin: { fontSize: fontSize.base },
  dialogueEnglish: { fontSize: fontSize.sm, color: colors.textSecondary, marginTop: 4 },
  grammarCard: { backgroundColor: colors.surfaceAlt, borderRadius: radius.lg, padding: spacing.md, marginBottom: spacing.md },
  grammarTitle: { fontSize: fontSize.base, color: colors.textPrimary, fontWeight: '600' },
  grammarText: { fontSize: fontSize.sm, color: colors.textSecondary, marginTop: 4, lineHeight: 20 },
  vocabList: { backgroundColor: colors.surface, borderRadius: radius.lg, borderWidth: 1, borderColor: colors.border, overflow: 'hidden' },
  vocabRow: { flexDirection: 'row', alignItems: 'center', padding: spacing.md, borderBottomWidth: 1, borderBottomColor: colors.border, gap: spacing.md, minHeight: 72 },
  lastRow: { borderBottomWidth: 0 },
  vocabHanzi: { fontSize: fontSize.xxl, color: colors.textPrimary, fontWeight: '500', width: 60 },
  vocabPinyin: { fontSize: fontSize.base, fontWeight: '500' },
  vocabEnglish: { fontSize: fontSize.sm, color: colors.textSecondary, marginTop: 2 },
  addBtn: { width: 36, height: 36, borderRadius: radius.full, backgroundColor: colors.primaryLight, alignItems: 'center', justifyContent: 'center' },
  deckBadge: { flexDirection: 'row', alignItems: 'center', gap: 4, paddingHorizontal: spacing.sm, paddingVertical: spacing.xs, borderRadius: radius.full, backgroundColor: colors.successLight, minHeight: 32 },
  deckBadgeText: { fontSize: fontSize.xs, color: colors.success, fontWeight: '600' },
});
