import React, { useCallback, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  TextInput,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useFocusEffect, useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { colors, spacing, radius, fontSize } from '@/src/theme';
import { api } from '@/src/api/client';
import { useAuth } from '@/src/contexts/AuthContext';

type Stats = {
  total_reviews: number;
  correct_reviews: number;
  retention_rate: number;
  mastered_count: number;
  learning_count: number;
  weak_words: { simplified: string; pinyin: string; english: string; correct: number; incorrect: number }[];
  speaking_attempts: number;
  streak_count: number;
};

export default function ProfileScreen() {
  const router = useRouter();
  const { user, logout, refreshUser } = useAuth();
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [draftGoal, setDraftGoal] = useState('20');

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const data = await api.stats();
      setStats(data);
      setDraftGoal(String(user?.daily_goal || 20));
    } catch (e) {
      setStats(null);
    } finally {
      setLoading(false);
    }
  }, [user]);

  useFocusEffect(
    useCallback(() => {
      load();
    }, [load])
  );

  const handleLogout = async () => {
    Alert.alert('Logout', 'Are you sure you want to log out?', [
      { text: 'Cancel', style: 'cancel' },
      {
        text: 'Logout',
        style: 'destructive',
        onPress: async () => {
          await logout();
          router.replace('/(auth)/login');
        },
      },
    ]);
  };

  const handleSaveGoal = async () => {
    const goal = parseInt(draftGoal, 10);
    if (Number.isNaN(goal) || goal < 1 || goal > 200) {
      Alert.alert('Invalid', 'Daily goal must be between 1 and 200.');
      return;
    }
    try {
      await api.updateMe({ daily_goal: goal });
      await refreshUser();
      setEditing(false);
    } catch (e: any) {
      Alert.alert('Error', e.message || 'Could not save');
    }
  };

  return (
    <SafeAreaView style={styles.safe} edges={['top']}>
      <ScrollView contentContainerStyle={styles.scroll}>
        {/* User card */}
        <View style={styles.userCard} testID="profile-user-card">
          <View style={styles.avatar}>
            <Text style={styles.avatarText}>
              {user?.name?.[0]?.toUpperCase() || '?'}
            </Text>
          </View>
          <Text style={styles.userName}>{user?.name}</Text>
          <Text style={styles.userEmail}>{user?.email}</Text>
        </View>

        {loading ? (
          <ActivityIndicator color={colors.primary} style={{ marginTop: spacing.xl }} />
        ) : (
          <>
            {/* Stats grid */}
            <Text style={styles.sectionTitle}>Your Progress</Text>
            <View style={styles.statsGrid}>
              <View style={styles.statBox} testID="profile-stat-streak">
                <Ionicons name="flame" size={24} color={colors.warning} />
                <Text style={styles.statValue}>{stats?.streak_count || 0}</Text>
                <Text style={styles.statLabel}>Day Streak</Text>
              </View>
              <View style={styles.statBox} testID="profile-stat-mastered">
                <Ionicons name="ribbon-outline" size={24} color={colors.primary} />
                <Text style={styles.statValue}>{stats?.mastered_count || 0}</Text>
                <Text style={styles.statLabel}>Mastered</Text>
              </View>
              <View style={styles.statBox} testID="profile-stat-retention">
                <Ionicons name="trending-up-outline" size={24} color={colors.success} />
                <Text style={styles.statValue}>{stats?.retention_rate || 0}%</Text>
                <Text style={styles.statLabel}>Retention</Text>
              </View>
              <View style={styles.statBox} testID="profile-stat-reviews">
                <Ionicons name="repeat" size={24} color={colors.tone4} />
                <Text style={styles.statValue}>{stats?.total_reviews || 0}</Text>
                <Text style={styles.statLabel}>Reviews</Text>
              </View>
            </View>

            {/* Weak words */}
            {stats?.weak_words && stats.weak_words.length > 0 && (
              <>
                <Text style={styles.sectionTitle}>Words to Strengthen</Text>
                <View style={styles.weakList} testID="profile-weak-words">
                  {stats.weak_words.map((w, i) => (
                    <View key={i} style={styles.weakRow}>
                      <Text style={styles.weakHanzi}>{w.simplified}</Text>
                      <View style={styles.flex}>
                        <Text style={styles.weakPinyin}>{w.pinyin}</Text>
                        <Text style={styles.weakEnglish}>{w.english}</Text>
                      </View>
                      <Text style={styles.weakRatio}>
                        {w.correct}/{w.correct + w.incorrect}
                      </Text>
                    </View>
                  ))}
                </View>
              </>
            )}

            {/* Settings */}
            <Text style={styles.sectionTitle}>Settings</Text>
            <View style={styles.settingsCard}>
              <View style={styles.settingRow}>
                <View style={styles.flex}>
                  <Text style={styles.settingLabel}>Daily Goal</Text>
                  <Text style={styles.settingHint}>Reviews per day</Text>
                </View>
                {editing ? (
                  <View style={styles.editRow}>
                    <TextInput
                      testID="profile-daily-goal-input"
                      style={styles.goalInput}
                      keyboardType="numeric"
                      value={draftGoal}
                      onChangeText={setDraftGoal}
                    />
                    <TouchableOpacity
                      testID="profile-save-goal-button"
                      style={styles.editBtn}
                      onPress={handleSaveGoal}
                    >
                      <Text style={styles.editBtnText}>Save</Text>
                    </TouchableOpacity>
                  </View>
                ) : (
                  <TouchableOpacity
                    testID="profile-edit-goal-button"
                    onPress={() => setEditing(true)}
                    style={styles.goalBadge}
                  >
                    <Text style={styles.goalBadgeText}>{user?.daily_goal || 20}</Text>
                    <Ionicons name="pencil" size={14} color={colors.primary} />
                  </TouchableOpacity>
                )}
              </View>
            </View>

            <TouchableOpacity
              testID="profile-logout-button"
              style={styles.logoutBtn}
              onPress={handleLogout}
            >
              <Ionicons name="log-out-outline" size={20} color={colors.error} />
              <Text style={styles.logoutText}>Log out</Text>
            </TouchableOpacity>
          </>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.background },
  flex: { flex: 1 },
  scroll: { padding: spacing.lg, paddingBottom: spacing.xxl },
  userCard: { alignItems: 'center', padding: spacing.lg },
  avatar: {
    width: 80,
    height: 80,
    borderRadius: radius.full,
    backgroundColor: colors.primaryLight,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: spacing.md,
  },
  avatarText: { fontSize: 36, color: colors.primary, fontWeight: '500' },
  userName: { fontSize: fontSize.xxl, color: colors.textPrimary, fontWeight: '500' },
  userEmail: { fontSize: fontSize.sm, color: colors.textSecondary, marginTop: 4 },
  sectionTitle: {
    fontSize: fontSize.base,
    color: colors.textSecondary,
    fontWeight: '500',
    marginTop: spacing.xl,
    marginBottom: spacing.md,
    letterSpacing: 0.5,
    textTransform: 'uppercase',
  },
  statsGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.md },
  statBox: {
    width: '47%',
    backgroundColor: colors.surface,
    borderRadius: radius.lg,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.md,
    alignItems: 'flex-start',
    minHeight: 100,
  },
  statValue: { fontSize: fontSize.display, color: colors.textPrimary, fontWeight: '500', marginTop: spacing.sm },
  statLabel: { fontSize: fontSize.sm, color: colors.textSecondary },
  weakList: {
    backgroundColor: colors.surface,
    borderRadius: radius.lg,
    borderWidth: 1,
    borderColor: colors.border,
    overflow: 'hidden',
  },
  weakRow: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
    gap: spacing.md,
  },
  weakHanzi: { fontSize: fontSize.xxl, color: colors.textPrimary, fontWeight: '500', width: 60 },
  weakPinyin: { fontSize: fontSize.base, color: colors.textPrimary },
  weakEnglish: { fontSize: fontSize.sm, color: colors.textSecondary, marginTop: 2 },
  weakRatio: { fontSize: fontSize.sm, color: colors.error, fontWeight: '600' },
  settingsCard: {
    backgroundColor: colors.surface,
    borderRadius: radius.lg,
    borderWidth: 1,
    borderColor: colors.border,
    overflow: 'hidden',
  },
  settingRow: { flexDirection: 'row', alignItems: 'center', padding: spacing.md, gap: spacing.md, minHeight: 56 },
  settingLabel: { fontSize: fontSize.base, color: colors.textPrimary, fontWeight: '500' },
  settingHint: { fontSize: fontSize.sm, color: colors.textTertiary, marginTop: 2 },
  goalBadge: {
    backgroundColor: colors.primaryLight,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: radius.full,
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
  },
  goalBadgeText: { color: colors.primary, fontWeight: '600', fontSize: fontSize.base },
  editRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  goalInput: {
    width: 64,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: radius.sm,
    padding: spacing.sm,
    textAlign: 'center',
    fontSize: fontSize.base,
    color: colors.textPrimary,
  },
  editBtn: { backgroundColor: colors.primary, paddingHorizontal: spacing.md, paddingVertical: spacing.sm, borderRadius: radius.sm },
  editBtnText: { color: '#fff', fontWeight: '600' },
  logoutBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.sm,
    backgroundColor: colors.errorLight,
    paddingVertical: spacing.md,
    borderRadius: radius.lg,
    marginTop: spacing.xl,
    minHeight: 48,
  },
  logoutText: { color: colors.error, fontSize: fontSize.base, fontWeight: '600' },
});
