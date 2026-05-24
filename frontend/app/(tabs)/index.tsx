import React, { useCallback, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  RefreshControl,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useFocusEffect, useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { colors, spacing, radius, fontSize } from '@/src/theme';
import { api, Dashboard } from '@/src/api/client';
import { useAuth } from '@/src/contexts/AuthContext';

export default function HomeScreen() {
  const router = useRouter();
  const { user } = useAuth();
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const load = useCallback(async () => {
    try {
      const data = await api.dashboard();
      setDashboard(data);
    } catch (e) {
      // ignore
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useFocusEffect(
    useCallback(() => {
      load();
    }, [load])
  );

  if (loading) {
    return (
      <View style={styles.loading}>
        <ActivityIndicator color={colors.primary} size="large" />
      </View>
    );
  }

  const reviewsToday = dashboard?.reviews_today || 0;
  const goal = dashboard?.daily_goal || 20;
  const progressPercent = dashboard?.progress_percent || 0;
  const dueCount = dashboard?.due_count || 0;
  const newCount = dashboard?.new_count || 0;
  const hasReviews = dueCount + newCount > 0;

  return (
    <SafeAreaView style={styles.safe} edges={['top']}>
      <ScrollView
        contentContainerStyle={styles.scroll}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={() => {
              setRefreshing(true);
              load();
            }}
            tintColor={colors.primary}
          />
        }
      >
        <View style={styles.headerRow}>
          <View style={styles.flex}>
            <Text style={styles.greeting}>你好</Text>
            <Text style={styles.userName} testID="home-greeting-name">
              {user?.name || 'Learner'}
            </Text>
          </View>
          <View style={styles.streakBadge} testID="home-streak-badge">
            <Ionicons name="flame" size={18} color={colors.warning} />
            <Text style={styles.streakText}>{dashboard?.streak_count || 0}</Text>
          </View>
        </View>

        {/* Daily progress card */}
        <View style={styles.progressCard} testID="home-daily-progress-card">
          <View style={styles.progressHeader}>
            <Text style={styles.progressLabel}>Today's Progress</Text>
            <Text style={styles.progressCount}>
              {reviewsToday} / {goal}
            </Text>
          </View>
          <View style={styles.progressBar}>
            <View
              style={[styles.progressFill, { width: `${progressPercent}%` }]}
              testID="home-progress-fill"
            />
          </View>
          <Text style={styles.progressHint}>
            {progressPercent >= 100
              ? 'Daily goal complete. 完美!'
              : `${goal - reviewsToday} reviews to reach your goal`}
          </Text>
        </View>

        {/* Continue learning CTA */}
        <TouchableOpacity
          testID="home-continue-learning-button"
          style={[styles.continueBtn, !hasReviews && styles.continueBtnMuted]}
          onPress={() => router.push('/(tabs)/review')}
          disabled={!hasReviews}
        >
          <View style={styles.flex}>
            <Text style={styles.continueLabel}>Continue Learning</Text>
            <Text style={styles.continueSubLabel}>
              {hasReviews
                ? `${dueCount} due · ${newCount} new available`
                : 'All caught up. Add new words from Lessons.'}
            </Text>
          </View>
          <Ionicons name="arrow-forward" size={22} color="#fff" />
        </TouchableOpacity>

        {/* Quick action tiles */}
        <Text style={styles.sectionTitle}>Practice</Text>
        <View style={styles.tileRow}>
          <TouchableOpacity
            testID="home-tile-flashcards"
            style={styles.tile}
            onPress={() => router.push('/(tabs)/review')}
          >
            <Ionicons name="albums-outline" size={28} color={colors.primary} />
            <Text style={styles.tileTitle}>Flashcards</Text>
            <Text style={styles.tileSub}>{dueCount} due</Text>
          </TouchableOpacity>
          <TouchableOpacity
            testID="home-tile-drills"
            style={styles.tile}
            onPress={() => router.push('/drill')}
          >
            <Ionicons name="construct-outline" size={28} color={colors.primary} />
            <Text style={styles.tileTitle}>Drills</Text>
            <Text style={styles.tileSub}>Build sentences</Text>
          </TouchableOpacity>
        </View>
        <View style={styles.tileRow}>
          <TouchableOpacity
            testID="home-tile-library"
            style={styles.tile}
            onPress={() => router.push('/library')}
          >
            <Ionicons name="library-outline" size={28} color={colors.primary} />
            <Text style={styles.tileTitle}>Library</Text>
            <Text style={styles.tileSub}>Browse & add words</Text>
          </TouchableOpacity>
          <TouchableOpacity
            testID="home-tile-add-word"
            style={styles.tile}
            onPress={() => router.push('/add-word')}
          >
            <Ionicons name="add-circle-outline" size={28} color={colors.primary} />
            <Text style={styles.tileTitle}>Add Word</Text>
            <Text style={styles.tileSub}>Custom vocab</Text>
          </TouchableOpacity>
        </View>
        <View style={styles.tileRow}>
          <TouchableOpacity
            testID="home-tile-speak"
            style={styles.tile}
            onPress={() => router.push('/(tabs)/speak')}
          >
            <Ionicons name="mic-outline" size={28} color={colors.primary} />
            <Text style={styles.tileTitle}>Speak</Text>
            <Text style={styles.tileSub}>Pronunciation</Text>
          </TouchableOpacity>
          <TouchableOpacity
            testID="home-tile-lessons"
            style={styles.tile}
            onPress={() => router.push('/(tabs)/lessons')}
          >
            <Ionicons name="book-outline" size={28} color={colors.primary} />
            <Text style={styles.tileTitle}>Lessons</Text>
            <Text style={styles.tileSub}>NPCR Library</Text>
          </TouchableOpacity>
        </View>

        {/* Memory snapshot */}
        <Text style={styles.sectionTitle}>Memory Snapshot</Text>
        <View style={styles.statsRow}>
          <View style={styles.statCard} testID="home-stat-mastered">
            <Text style={styles.statValue}>{dashboard?.mastered_count || 0}</Text>
            <Text style={styles.statLabel}>Mastered</Text>
          </View>
          <View style={styles.statCard} testID="home-stat-total">
            <Text style={styles.statValue}>{dashboard?.total_cards || 0}</Text>
            <Text style={styles.statLabel}>Learning</Text>
          </View>
          <View style={styles.statCard} testID="home-stat-correct-today">
            <Text style={styles.statValue}>{dashboard?.correct_today || 0}</Text>
            <Text style={styles.statLabel}>Correct Today</Text>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.background },
  flex: { flex: 1 },
  loading: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: colors.background },
  scroll: { padding: spacing.lg, paddingBottom: spacing.xxl },
  headerRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.lg,
  },
  greeting: {
    fontSize: fontSize.xxl,
    color: colors.textSecondary,
    fontWeight: '300',
  },
  userName: {
    fontSize: fontSize.display,
    color: colors.textPrimary,
    fontWeight: '400',
    letterSpacing: -0.5,
    marginTop: 2,
  },
  streakBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FDF4DD',
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: radius.full,
    gap: spacing.xs,
  },
  streakText: { fontSize: fontSize.base, fontWeight: '600', color: colors.warning },
  progressCard: {
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: radius.xl,
    borderWidth: 1,
    borderColor: colors.border,
    marginBottom: spacing.md,
  },
  progressHeader: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: spacing.md },
  progressLabel: { fontSize: fontSize.base, color: colors.textSecondary, fontWeight: '500' },
  progressCount: { fontSize: fontSize.lg, color: colors.textPrimary, fontWeight: '600' },
  progressBar: {
    height: 8,
    backgroundColor: colors.surfaceAlt,
    borderRadius: radius.full,
    overflow: 'hidden',
  },
  progressFill: { height: '100%', backgroundColor: colors.primary, borderRadius: radius.full },
  progressHint: { fontSize: fontSize.sm, color: colors.textTertiary, marginTop: spacing.md },
  continueBtn: {
    backgroundColor: colors.primary,
    padding: spacing.lg,
    borderRadius: radius.xl,
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.xl,
    minHeight: 78,
  },
  continueBtnMuted: { backgroundColor: colors.textTertiary },
  continueLabel: { color: '#fff', fontSize: fontSize.xl, fontWeight: '600' },
  continueSubLabel: { color: 'rgba(255,255,255,0.85)', fontSize: fontSize.sm, marginTop: 4 },
  sectionTitle: {
    fontSize: fontSize.lg,
    color: colors.textPrimary,
    fontWeight: '500',
    marginBottom: spacing.md,
    marginTop: spacing.md,
  },
  tileRow: { flexDirection: 'row', gap: spacing.md, marginBottom: spacing.md },
  tile: {
    flex: 1,
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: radius.lg,
    borderWidth: 1,
    borderColor: colors.border,
    minHeight: 110,
  },
  tileTitle: { fontSize: fontSize.lg, color: colors.textPrimary, fontWeight: '600', marginTop: spacing.sm },
  tileSub: { fontSize: fontSize.sm, color: colors.textTertiary, marginTop: 2 },
  statsRow: { flexDirection: 'row', gap: spacing.sm },
  statCard: {
    flex: 1,
    backgroundColor: colors.surfaceAlt,
    padding: spacing.md,
    borderRadius: radius.lg,
    alignItems: 'center',
  },
  statValue: { fontSize: fontSize.xxl, color: colors.primary, fontWeight: '500' },
  statLabel: { fontSize: fontSize.xs, color: colors.textSecondary, marginTop: 4, textAlign: 'center' },
});
