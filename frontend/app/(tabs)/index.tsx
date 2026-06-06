import React, { useCallback, useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  ActivityIndicator,
  RefreshControl,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useFocusEffect, useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import * as Haptics from 'expo-haptics';
import Animated, {
  FadeInDown,
  ZoomIn,
  useAnimatedStyle,
  useSharedValue,
  withTiming,
} from 'react-native-reanimated';
import { colors, spacing, radius, fontSize, shadows, accents, gradients, AccentName } from '@/src/theme';
import PressableScale from '@/src/components/PressableScale';
import { api, Dashboard } from '@/src/api/client';
import { useAuth } from '@/src/contexts/AuthContext';

type Tile = {
  testID: string;
  icon: keyof typeof Ionicons.glyphMap;
  title: string;
  sub: string;
  accent: AccentName;
  route: string;
};

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

  const reviewsToday = dashboard?.reviews_today || 0;
  const goal = dashboard?.daily_goal || 20;
  const progressPercent = dashboard?.progress_percent || 0;
  const dueCount = dashboard?.due_count || 0;
  const newCount = dashboard?.new_count || 0;
  const hasReviews = dueCount + newCount > 0;
  const goalComplete = progressPercent >= 100;

  // Animate the progress bar fill whenever the percentage changes.
  const progress = useSharedValue(0);
  useEffect(() => {
    progress.value = withTiming(Math.min(progressPercent, 100), { duration: 800 });
  }, [progressPercent, progress]);
  const fillStyle = useAnimatedStyle(() => ({ width: `${progress.value}%` }));

  if (loading) {
    return (
      <View style={styles.loading}>
        <ActivityIndicator color={colors.primary} size="large" />
      </View>
    );
  }

  const tiles: Tile[] = [
    { testID: 'home-tile-flashcards', icon: 'albums', title: 'Flashcards', sub: `${dueCount} due`, accent: 'green', route: '/(tabs)/review' },
    { testID: 'home-tile-drills', icon: 'construct', title: 'Drills', sub: 'Build sentences', accent: 'blue', route: '/drill' },
    { testID: 'home-tile-library', icon: 'library', title: 'Library', sub: 'Browse & add words', accent: 'violet', route: '/library' },
    { testID: 'home-tile-add-word', icon: 'add-circle', title: 'Add Word', sub: 'Custom vocab', accent: 'amber', route: '/add-word' },
    { testID: 'home-tile-speak', icon: 'mic', title: 'Speak', sub: 'Pronunciation', accent: 'rose', route: '/(tabs)/speak' },
    { testID: 'home-tile-lessons', icon: 'book', title: 'Lessons', sub: 'NPCR Library', accent: 'teal', route: '/(tabs)/lessons' },
  ];

  return (
    <SafeAreaView style={styles.safe} edges={['top']}>
      {/* Oversized brand watermark — 间隔 ("spaced", as in spaced repetition) */}
      <Text style={styles.watermark} pointerEvents="none">
        间隔
      </Text>

      <ScrollView
        contentContainerStyle={styles.scroll}
        showsVerticalScrollIndicator={false}
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
          <LinearGradient
            colors={gradients.amber}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 1 }}
            style={styles.streakBadge}
          >
            <Ionicons name="flame" size={18} color="#fff" />
            <Text style={styles.streakText} testID="home-streak-badge">
              {dashboard?.streak_count || 0}
            </Text>
          </LinearGradient>
        </View>

        {/* Daily progress card */}
        <Animated.View
          entering={FadeInDown.duration(450)}
          style={styles.progressCard}
          testID="home-daily-progress-card"
        >
          <View style={styles.progressHeader}>
            <Text style={styles.progressLabel}>Today&apos;s Progress</Text>
            <Text style={styles.progressCount}>
              {reviewsToday} / {goal}
            </Text>
          </View>
          <View style={styles.progressBar}>
            <Animated.View style={[styles.progressFill, fillStyle]} testID="home-progress-fill">
              <LinearGradient
                colors={gradients.hero}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 0 }}
                style={StyleSheet.absoluteFill}
              />
            </Animated.View>
          </View>
          {goalComplete ? (
            <Animated.View entering={ZoomIn.springify().damping(12)} style={styles.goalDoneRow}>
              <Ionicons name="checkmark-circle" size={18} color={colors.success} />
              <Text style={styles.goalDoneText}>Daily goal complete. 完美!</Text>
            </Animated.View>
          ) : (
            <Text style={styles.progressHint}>
              {goal - reviewsToday} reviews to reach your goal
            </Text>
          )}
        </Animated.View>

        {/* Continue learning CTA */}
        <PressableScale
          testID="home-continue-learning-button"
          onPress={() => {
            Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
            router.push('/(tabs)/review');
          }}
          disabled={!hasReviews}
          style={styles.continueWrap}
        >
          <LinearGradient
            colors={hasReviews ? gradients.hero : ([colors.textTertiary, colors.textTertiary] as const)}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 1 }}
            style={[styles.continueBtn, hasReviews && shadows.glow(accents.teal.base)]}
          >
            <View style={styles.flex}>
              <Text style={styles.continueLabel}>Continue Learning</Text>
              <Text style={styles.continueSubLabel}>
                {hasReviews
                  ? `${dueCount} due · ${newCount} new available`
                  : 'All caught up. Add new words from Lessons.'}
              </Text>
            </View>
            <View style={styles.continueArrow}>
              <Ionicons name="arrow-forward" size={22} color="#fff" />
            </View>
          </LinearGradient>
        </PressableScale>

        {/* Quick action tiles */}
        <Text style={styles.sectionTitle}>Practice</Text>
        <View style={styles.tileGrid}>
          {tiles.map((tile, i) => (
            <Animated.View
              key={tile.testID}
              entering={FadeInDown.delay(80 + i * 50).duration(400)}
              style={styles.tileWrap}
            >
              <PressableScale
                testID={tile.testID}
                style={styles.tile}
                onPress={() => router.push(tile.route as any)}
              >
                <View style={[styles.tileChip, { backgroundColor: accents[tile.accent].soft }]}>
                  <Ionicons name={tile.icon} size={24} color={accents[tile.accent].base} />
                </View>
                <Text style={styles.tileTitle}>{tile.title}</Text>
                <Text style={styles.tileSub}>{tile.sub}</Text>
              </PressableScale>
            </Animated.View>
          ))}
        </View>

        {/* Memory snapshot */}
        <Text style={styles.sectionTitle}>Memory Snapshot</Text>
        <View style={styles.statsRow}>
          <StatCard
            testID="home-stat-mastered"
            value={dashboard?.mastered_count || 0}
            label="Mastered"
            accent="violet"
          />
          <StatCard
            testID="home-stat-total"
            value={dashboard?.total_cards || 0}
            label="Learning"
            accent="blue"
          />
          <StatCard
            testID="home-stat-correct-today"
            value={dashboard?.correct_today || 0}
            label="Correct Today"
            accent="green"
          />
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

function StatCard({
  testID,
  value,
  label,
  accent,
}: {
  testID: string;
  value: number;
  label: string;
  accent: AccentName;
}) {
  return (
    <View style={styles.statCard} testID={testID}>
      <View style={[styles.statDot, { backgroundColor: accents[accent].soft }]}>
        <View style={[styles.statDotInner, { backgroundColor: accents[accent].base }]} />
      </View>
      <Text style={[styles.statValue, { color: accents[accent].base }]}>{value}</Text>
      <Text style={styles.statLabel}>{label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.background },
  flex: { flex: 1 },
  loading: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: colors.background },
  scroll: { padding: spacing.lg, paddingBottom: spacing.xxl },
  watermark: {
    position: 'absolute',
    top: -24,
    right: -20,
    fontSize: 150,
    fontWeight: '700',
    color: colors.primary,
    opacity: 0.05,
  },
  headerRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.lg,
  },
  greeting: {
    fontSize: fontSize.xxl,
    color: colors.textSecondary,
    fontWeight: '400',
  },
  userName: {
    fontSize: fontSize.display,
    color: colors.textPrimary,
    fontWeight: '700',
    letterSpacing: -0.5,
    marginTop: 2,
  },
  streakBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: radius.full,
    gap: spacing.xs,
    ...shadows.glow(accents.amber.base),
  },
  streakText: { fontSize: fontSize.base, fontWeight: '700', color: '#fff' },
  progressCard: {
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: radius.xl,
    marginBottom: spacing.md,
    ...shadows.md,
  },
  progressHeader: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: spacing.md },
  progressLabel: { fontSize: fontSize.base, color: colors.textSecondary, fontWeight: '600' },
  progressCount: { fontSize: fontSize.lg, color: colors.textPrimary, fontWeight: '700' },
  progressBar: {
    height: 10,
    backgroundColor: colors.surfaceAlt,
    borderRadius: radius.full,
    overflow: 'hidden',
  },
  progressFill: { height: '100%', borderRadius: radius.full, overflow: 'hidden' },
  progressHint: { fontSize: fontSize.sm, color: colors.textTertiary, marginTop: spacing.md },
  goalDoneRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.xs, marginTop: spacing.md },
  goalDoneText: { fontSize: fontSize.sm, color: colors.success, fontWeight: '600' },
  continueWrap: { marginBottom: spacing.xl, borderRadius: radius.xl },
  continueBtn: {
    padding: spacing.lg,
    borderRadius: radius.xl,
    flexDirection: 'row',
    alignItems: 'center',
    minHeight: 80,
  },
  continueLabel: { color: '#fff', fontSize: fontSize.xl, fontWeight: '700' },
  continueSubLabel: { color: 'rgba(255,255,255,0.9)', fontSize: fontSize.sm, marginTop: 4 },
  continueArrow: {
    width: 40,
    height: 40,
    borderRadius: radius.full,
    backgroundColor: 'rgba(255,255,255,0.2)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  sectionTitle: {
    fontSize: fontSize.lg,
    color: colors.textPrimary,
    fontWeight: '700',
    marginBottom: spacing.md,
    marginTop: spacing.md,
  },
  tileGrid: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between' },
  tileWrap: { width: '48%', marginBottom: spacing.md },
  tile: {
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: radius.lg,
    minHeight: 124,
    ...shadows.sm,
  },
  tileChip: {
    width: 48,
    height: 48,
    borderRadius: radius.md,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: spacing.sm,
  },
  tileTitle: { fontSize: fontSize.lg, color: colors.textPrimary, fontWeight: '700' },
  tileSub: { fontSize: fontSize.sm, color: colors.textTertiary, marginTop: 2 },
  statsRow: { flexDirection: 'row', gap: spacing.sm },
  statCard: {
    flex: 1,
    backgroundColor: colors.surface,
    padding: spacing.md,
    borderRadius: radius.lg,
    alignItems: 'center',
    ...shadows.sm,
  },
  statDot: {
    width: 28,
    height: 28,
    borderRadius: radius.full,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: spacing.xs,
  },
  statDotInner: { width: 10, height: 10, borderRadius: radius.full },
  statValue: { fontSize: fontSize.xxl, fontWeight: '700' },
  statLabel: { fontSize: fontSize.xs, color: colors.textSecondary, marginTop: 4, textAlign: 'center' },
});
