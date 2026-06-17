/**
 * Lessons tab — the NPCR lesson index.
 *
 * Lists every lesson with its per-user progress bar; tapping opens the lesson
 * detail screen. Reloads on focus so mastered/started counts stay current.
 */
import React, { useCallback, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  ActivityIndicator,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useFocusEffect, useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import Animated, { FadeInDown } from 'react-native-reanimated';
import { colors, spacing, radius, fontSize, shadows, accents, accentCycle } from '@/src/theme';
import PressableScale from '@/src/components/PressableScale';
import { api, Lesson } from '@/src/api/client';

export default function LessonsScreen() {
  const router = useRouter();
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const data = await api.lessons();
      setLessons(data);
    } catch (e) {
      setLessons([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useFocusEffect(
    useCallback(() => {
      load();
    }, [load])
  );

  return (
    <SafeAreaView style={styles.safe} edges={['top']}>
      <View style={styles.header}>
        <Text style={styles.title}>Lessons</Text>
        <Text style={styles.subtitle}>New Practical Chinese Reader</Text>
      </View>

      {loading ? (
        <View style={styles.loading}>
          <ActivityIndicator color={colors.primary} size="large" />
        </View>
      ) : (
        <FlatList
          data={lessons}
          keyExtractor={(item) => item.id}
          contentContainerStyle={styles.list}
          showsVerticalScrollIndicator={false}
          renderItem={({ item, index }) => {
            const accent = accents[accentCycle[index % accentCycle.length]];
            return (
              <Animated.View entering={FadeInDown.delay(index * 45).duration(380)}>
                <PressableScale
                  testID={`lesson-card-${item.lesson_number}`}
                  style={styles.lessonCard}
                  onPress={() => router.push(`/lesson/${item.id}`)}
                >
                  <View style={styles.lessonRow}>
                    <View style={[styles.lessonNumber, { backgroundColor: accent.soft }]}>
                      <Text style={[styles.lessonNumberText, { color: accent.base }]}>
                        {item.lesson_number}
                      </Text>
                    </View>
                    <View style={styles.lessonInfo}>
                      <Text style={styles.lessonTitle}>{item.title}</Text>
                      <Text style={styles.lessonSub}>{item.subtitle}</Text>
                      <View style={styles.lessonMeta}>
                        <View style={[styles.metaPill, { backgroundColor: accent.soft }]}>
                          <Text style={[styles.metaPillText, { color: accent.base }]}>{item.level}</Text>
                        </View>
                        <Text style={styles.metaText}>
                          {item.vocabulary_count} words · {item.progress?.mastered || 0} mastered
                        </Text>
                      </View>
                    </View>
                    <Ionicons name="chevron-forward" size={22} color={colors.textTertiary} />
                  </View>
                  {item.progress && item.progress.total > 0 && (
                    <View style={styles.lessonProgressBar}>
                      <View
                        style={[
                          styles.lessonProgressFill,
                          {
                            backgroundColor: accent.base,
                            width: `${(item.progress.started / item.progress.total) * 100}%`,
                          },
                        ]}
                      />
                    </View>
                  )}
                </PressableScale>
              </Animated.View>
            );
          }}
        />
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.background },
  loading: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  header: { padding: spacing.lg, paddingBottom: spacing.md },
  title: { fontSize: fontSize.display, color: colors.textPrimary, fontWeight: '700', letterSpacing: -0.5 },
  subtitle: { fontSize: fontSize.base, color: colors.textSecondary, marginTop: 4 },
  list: { padding: spacing.lg, paddingTop: 0, gap: spacing.md },
  lessonCard: {
    backgroundColor: colors.surface,
    borderRadius: radius.lg,
    padding: spacing.lg,
    marginBottom: spacing.md,
    borderWidth: 1,
    borderColor: colors.border,
    ...shadows.sm,
  },
  lessonRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  lessonNumber: {
    width: 48,
    height: 48,
    borderRadius: radius.md,
    alignItems: 'center',
    justifyContent: 'center',
  },
  lessonNumberText: { fontSize: fontSize.lg, fontWeight: '700' },
  lessonInfo: { flex: 1 },
  lessonTitle: { fontSize: fontSize.lg, color: colors.textPrimary, fontWeight: '700' },
  lessonSub: { fontSize: fontSize.sm, color: colors.textSecondary, marginTop: 2 },
  lessonMeta: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, marginTop: spacing.sm },
  metaPill: {
    paddingHorizontal: spacing.sm,
    paddingVertical: 2,
    borderRadius: radius.sm,
  },
  metaPillText: { fontSize: fontSize.xs, fontWeight: '700' },
  metaText: { fontSize: fontSize.xs, color: colors.textTertiary },
  lessonProgressBar: {
    marginTop: spacing.md,
    height: 4,
    backgroundColor: colors.surfaceAlt,
    borderRadius: radius.full,
    overflow: 'hidden',
  },
  lessonProgressFill: { height: '100%', borderRadius: radius.full },
});
