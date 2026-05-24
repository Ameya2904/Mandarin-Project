import React, { useEffect, useState } from 'react';
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

  useEffect(() => {
    (async () => {
      if (!id) return;
      try {
        const data = await api.lesson(id);
        setLesson(data);
      } catch (e) {
        setLesson(null);
      } finally {
        setLoading(false);
      }
    })();
  }, [id]);

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

  return (
    <SafeAreaView style={styles.safe} edges={['top']}>
      <Stack.Screen options={{ headerShown: false }} />
      <View style={styles.header}>
        <TouchableOpacity
          testID="lesson-back-button"
          onPress={() => router.back()}
          style={styles.backBtn}
        >
          <Ionicons name="arrow-back" size={24} color={colors.textPrimary} />
        </TouchableOpacity>
        <Text style={styles.lessonNumber}>Lesson {lesson.lesson_number}</Text>
      </View>

      <ScrollView contentContainerStyle={styles.scroll}>
        <Text style={styles.title}>{lesson.title}</Text>
        <Text style={styles.subtitle}>{lesson.subtitle}</Text>
        <Text style={styles.description}>{lesson.description}</Text>

        {/* CTA buttons */}
        <View style={styles.ctaRow}>
          <TouchableOpacity
            testID="lesson-practice-review-btn"
            style={styles.ctaBtn}
            onPress={() => router.push('/(tabs)/review')}
          >
            <Ionicons name="albums-outline" size={20} color="#fff" />
            <Text style={styles.ctaText}>Review</Text>
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

        {/* Dialogue */}
        {lesson.dialogue && lesson.dialogue.length > 0 && (
          <>
            <Text style={styles.sectionTitle}>Dialogue · 对话</Text>
            <View style={styles.dialogueCard}>
              {lesson.dialogue.map((line, i) => (
                <View key={i} style={styles.dialogueRow}>
                  <Text style={styles.dialogueSpeaker}>{line.speaker}</Text>
                  <Text style={styles.dialogueHanzi}>{line.chinese}</Text>
                  <Text style={[styles.dialoguePinyin, { color: getToneColor(line.pinyin) }]}>
                    {line.pinyin}
                  </Text>
                  <Text style={styles.dialogueEnglish}>{line.english}</Text>
                </View>
              ))}
            </View>
          </>
        )}

        {/* Grammar */}
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

        {/* Vocabulary */}
        {lesson.vocabulary && lesson.vocabulary.length > 0 && (
          <>
            <Text style={styles.sectionTitle}>Vocabulary · 生词 ({lesson.vocabulary.length})</Text>
            <View style={styles.vocabList}>
              {lesson.vocabulary.map((v, i) => (
                <View key={v.id} style={[styles.vocabRow, i === lesson.vocabulary!.length - 1 && styles.lastRow]}>
                  <Text style={styles.vocabHanzi}>{v.simplified}</Text>
                  <View style={styles.flex}>
                    <Text style={[styles.vocabPinyin, { color: getToneColor(v.pinyin) }]}>{v.pinyin}</Text>
                    <Text style={styles.vocabEnglish}>{v.english}</Text>
                  </View>
                  <View style={styles.posBadge}>
                    <Text style={styles.posText}>{v.part_of_speech.slice(0, 3)}</Text>
                  </View>
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
  ctaBtn: {
    flex: 1,
    backgroundColor: colors.primary,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 14,
    borderRadius: radius.md,
    gap: spacing.sm,
    minHeight: 48,
  },
  ctaSecondary: { backgroundColor: 'transparent', borderWidth: 1, borderColor: colors.primary },
  ctaText: { color: '#fff', fontWeight: '600', fontSize: fontSize.base },
  sectionTitle: {
    fontSize: fontSize.base,
    color: colors.textSecondary,
    fontWeight: '500',
    marginTop: spacing.xl,
    marginBottom: spacing.md,
    letterSpacing: 0.5,
    textTransform: 'uppercase',
  },
  dialogueCard: {
    backgroundColor: colors.surface,
    borderRadius: radius.lg,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.md,
    gap: spacing.md,
  },
  dialogueRow: { paddingBottom: spacing.md, borderBottomWidth: 1, borderBottomColor: colors.border },
  dialogueSpeaker: { fontSize: fontSize.xs, color: colors.textTertiary, fontWeight: '500', marginBottom: 4 },
  dialogueHanzi: { fontSize: fontSize.xl, color: colors.textPrimary, marginBottom: 4 },
  dialoguePinyin: { fontSize: fontSize.base },
  dialogueEnglish: { fontSize: fontSize.sm, color: colors.textSecondary, marginTop: 4 },
  grammarCard: {
    backgroundColor: colors.surfaceAlt,
    borderRadius: radius.lg,
    padding: spacing.md,
    marginBottom: spacing.md,
  },
  grammarTitle: { fontSize: fontSize.base, color: colors.textPrimary, fontWeight: '600' },
  grammarText: { fontSize: fontSize.sm, color: colors.textSecondary, marginTop: 4, lineHeight: 20 },
  vocabList: {
    backgroundColor: colors.surface,
    borderRadius: radius.lg,
    borderWidth: 1,
    borderColor: colors.border,
    overflow: 'hidden',
  },
  vocabRow: { flexDirection: 'row', alignItems: 'center', padding: spacing.md, borderBottomWidth: 1, borderBottomColor: colors.border, gap: spacing.md },
  lastRow: { borderBottomWidth: 0 },
  vocabHanzi: { fontSize: fontSize.xxl, color: colors.textPrimary, fontWeight: '500', width: 60 },
  vocabPinyin: { fontSize: fontSize.base, fontWeight: '500' },
  vocabEnglish: { fontSize: fontSize.sm, color: colors.textSecondary, marginTop: 2 },
  posBadge: {
    backgroundColor: colors.surfaceAlt,
    paddingHorizontal: spacing.sm,
    paddingVertical: 2,
    borderRadius: radius.sm,
  },
  posText: { fontSize: 10, color: colors.textTertiary, textTransform: 'uppercase', fontWeight: '500' },
});
