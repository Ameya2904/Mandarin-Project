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
  Platform,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useFocusEffect, useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { colors, spacing, radius, fontSize, shadows, accents, gradients } from '@/src/theme';
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

type ScheduleEntry = { date: string; count: number };

function formatScheduleDate(dateStr: string): string {
  const today = new Date();
  const tomorrow = new Date(today);
  tomorrow.setDate(today.getDate() + 1);
  const d = new Date(dateStr + 'T12:00:00');
  if (d.toDateString() === tomorrow.toDateString()) return 'Tomorrow';
  const diffDays = Math.round((d.getTime() - today.getTime()) / 86_400_000);
  if (diffDays < 7) return d.toLocaleDateString(undefined, { weekday: 'long' });
  return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
}

export default function ProfileScreen() {
  const router = useRouter();
  const { user, logout, refreshUser } = useAuth();
  const [stats, setStats] = useState<Stats | null>(null);
  const [schedule, setSchedule] = useState<ScheduleEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [draftGoal, setDraftGoal] = useState('20');
  const [changingPw, setChangingPw] = useState(false);
  const [currentPw, setCurrentPw] = useState('');
  const [newPw, setNewPw] = useState('');
  const [confirmPw, setConfirmPw] = useState('');
  const [pwSubmitting, setPwSubmitting] = useState(false);
  const [pwError, setPwError] = useState('');
  const [pwSuccess, setPwSuccess] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [data, sched] = await Promise.all([api.stats(), api.reviewSchedule(14)]);
      setStats(data);
      setSchedule(sched);
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
    const doLogout = async () => {
      await logout();
      router.replace('/(auth)/login');
    };

    if (Platform.OS === 'web') {
      // Alert.alert is a no-op on web, use window.confirm instead.
      // eslint-disable-next-line no-undef
      if (typeof window !== 'undefined' && window.confirm('Are you sure you want to log out?')) {
        await doLogout();
      }
      return;
    }

    Alert.alert('Logout', 'Are you sure you want to log out?', [
      { text: 'Cancel', style: 'cancel' },
      { text: 'Logout', style: 'destructive', onPress: doLogout },
    ]);
  };

  const resetPwForm = () => {
    setChangingPw(false);
    setCurrentPw('');
    setNewPw('');
    setConfirmPw('');
    setPwError('');
  };

  const handleChangePassword = async () => {
    setPwError('');
    setPwSuccess(false);
    if (!currentPw || !newPw) {
      setPwError('Please fill in all fields.');
      return;
    }
    if (newPw.length < 6) {
      setPwError('New password must be at least 6 characters.');
      return;
    }
    if (newPw !== confirmPw) {
      setPwError('New passwords do not match.');
      return;
    }
    setPwSubmitting(true);
    try {
      await api.changePassword(currentPw, newPw);
      resetPwForm();
      setPwSuccess(true);
    } catch (e: any) {
      setPwError(e.message || 'Could not change password.');
    } finally {
      setPwSubmitting(false);
    }
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
          <LinearGradient
            colors={gradients.hero}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 1 }}
            style={styles.avatar}
          >
            <Text style={styles.avatarText}>
              {user?.name?.[0]?.toUpperCase() || '?'}
            </Text>
          </LinearGradient>
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
              <StatBox testID="profile-stat-streak" icon="flame" accent="amber" value={stats?.streak_count || 0} label="Day Streak" />
              <StatBox testID="profile-stat-mastered" icon="ribbon" accent="violet" value={stats?.mastered_count || 0} label="Mastered" />
              <StatBox testID="profile-stat-retention" icon="trending-up" accent="green" value={`${stats?.retention_rate || 0}%`} label="Retention" />
              <StatBox testID="profile-stat-reviews" icon="repeat" accent="blue" value={stats?.total_reviews || 0} label="Reviews" />
            </View>

            {/* Upcoming reviews */}
            {schedule.length > 0 && (
              <>
                <Text style={styles.sectionTitle}>Upcoming Reviews</Text>
                <View style={styles.scheduleCard} testID="profile-schedule">
                  {schedule.map((entry, i) => (
                    <View
                      key={entry.date}
                      style={[styles.scheduleRow, i < schedule.length - 1 && styles.scheduleRowBorder]}
                    >
                      <Text style={styles.scheduleDate}>{formatScheduleDate(entry.date)}</Text>
                      <View style={styles.scheduleBadge}>
                        <Text style={styles.scheduleBadgeText}>{entry.count}</Text>
                      </View>
                    </View>
                  ))}
                </View>
              </>
            )}

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

            {/* Security */}
            <Text style={styles.sectionTitle}>Security</Text>
            <View style={styles.settingsCard}>
              {!changingPw ? (
                <TouchableOpacity
                  testID="profile-change-password-button"
                  style={styles.settingRow}
                  onPress={() => {
                    setPwSuccess(false);
                    setChangingPw(true);
                  }}
                >
                  <View style={styles.flex}>
                    <Text style={styles.settingLabel}>Change Password</Text>
                    <Text style={styles.settingHint}>
                      {pwSuccess ? 'Password updated' : 'Update your account password'}
                    </Text>
                  </View>
                  <Ionicons name="chevron-forward" size={20} color={colors.textTertiary} />
                </TouchableOpacity>
              ) : (
                <View style={styles.pwForm}>
                  <TextInput
                    testID="profile-current-password-input"
                    style={styles.pwInput}
                    secureTextEntry
                    placeholder="Current password"
                    placeholderTextColor={colors.textTertiary}
                    value={currentPw}
                    onChangeText={setCurrentPw}
                  />
                  <TextInput
                    testID="profile-new-password-input"
                    style={styles.pwInput}
                    secureTextEntry
                    placeholder="New password (min 6 characters)"
                    placeholderTextColor={colors.textTertiary}
                    value={newPw}
                    onChangeText={setNewPw}
                  />
                  <TextInput
                    testID="profile-confirm-password-input"
                    style={styles.pwInput}
                    secureTextEntry
                    placeholder="Confirm new password"
                    placeholderTextColor={colors.textTertiary}
                    value={confirmPw}
                    onChangeText={setConfirmPw}
                  />

                  {pwError ? (
                    <Text testID="profile-password-error" style={styles.pwError}>
                      {pwError}
                    </Text>
                  ) : null}

                  <View style={styles.pwActions}>
                    <TouchableOpacity
                      testID="profile-cancel-password-button"
                      style={[styles.pwBtn, styles.pwBtnGhost]}
                      onPress={resetPwForm}
                      disabled={pwSubmitting}
                    >
                      <Text style={styles.pwBtnGhostText}>Cancel</Text>
                    </TouchableOpacity>
                    <TouchableOpacity
                      testID="profile-save-password-button"
                      style={[styles.pwBtn, styles.pwBtnPrimary, pwSubmitting && styles.btnDisabled]}
                      onPress={handleChangePassword}
                      disabled={pwSubmitting}
                    >
                      {pwSubmitting ? (
                        <ActivityIndicator color="#fff" />
                      ) : (
                        <Text style={styles.pwBtnPrimaryText}>Update</Text>
                      )}
                    </TouchableOpacity>
                  </View>
                </View>
              )}
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

function StatBox({
  testID,
  icon,
  accent,
  value,
  label,
}: {
  testID: string;
  icon: keyof typeof Ionicons.glyphMap;
  accent: keyof typeof accents;
  value: string | number;
  label: string;
}) {
  return (
    <View style={styles.statBox} testID={testID}>
      <View style={[styles.statChip, { backgroundColor: accents[accent].soft }]}>
        <Ionicons name={icon} size={22} color={accents[accent].base} />
      </View>
      <Text style={[styles.statValue, { color: accents[accent].base }]}>{value}</Text>
      <Text style={styles.statLabel}>{label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.background },
  flex: { flex: 1 },
  scroll: { padding: spacing.lg, paddingBottom: spacing.xxl },
  userCard: { alignItems: 'center', padding: spacing.lg },
  avatar: {
    width: 84,
    height: 84,
    borderRadius: radius.full,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: spacing.md,
    ...shadows.glow(accents.teal.base),
  },
  avatarText: { fontSize: 38, color: '#fff', fontWeight: '700' },
  userName: { fontSize: fontSize.xxl, color: colors.textPrimary, fontWeight: '700' },
  userEmail: { fontSize: fontSize.sm, color: colors.textSecondary, marginTop: 4 },
  sectionTitle: {
    fontSize: fontSize.base,
    color: colors.textSecondary,
    fontWeight: '700',
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
    padding: spacing.md,
    alignItems: 'flex-start',
    minHeight: 110,
    ...shadows.sm,
  },
  statChip: {
    width: 40,
    height: 40,
    borderRadius: radius.md,
    alignItems: 'center',
    justifyContent: 'center',
  },
  statValue: { fontSize: fontSize.display, fontWeight: '700', marginTop: spacing.sm },
  statLabel: { fontSize: fontSize.sm, color: colors.textSecondary },
  weakList: {
    backgroundColor: colors.surface,
    borderRadius: radius.lg,
    overflow: 'hidden',
    ...shadows.sm,
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
    overflow: 'hidden',
    ...shadows.sm,
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
  pwForm: { padding: spacing.md, gap: spacing.sm },
  pwInput: {
    backgroundColor: colors.background,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: radius.md,
    paddingHorizontal: spacing.md,
    paddingVertical: 12,
    fontSize: fontSize.base,
    color: colors.textPrimary,
    minHeight: 46,
  },
  pwError: {
    color: colors.error,
    fontSize: fontSize.sm,
    backgroundColor: colors.errorLight,
    padding: spacing.sm,
    borderRadius: radius.sm,
  },
  pwActions: { flexDirection: 'row', gap: spacing.sm, marginTop: spacing.xs },
  pwBtn: {
    flex: 1,
    paddingVertical: spacing.md,
    borderRadius: radius.md,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 46,
  },
  pwBtnGhost: { backgroundColor: colors.background, borderWidth: 1, borderColor: colors.border },
  pwBtnGhostText: { color: colors.textSecondary, fontWeight: '600', fontSize: fontSize.base },
  pwBtnPrimary: { backgroundColor: colors.primary },
  pwBtnPrimaryText: { color: '#fff', fontWeight: '700', fontSize: fontSize.base },
  btnDisabled: { opacity: 0.7 },
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
  scheduleCard: {
    backgroundColor: colors.surface,
    borderRadius: radius.lg,
    overflow: 'hidden',
    ...shadows.sm,
  },
  scheduleRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', padding: spacing.md, minHeight: 48 },
  scheduleRowBorder: { borderBottomWidth: 1, borderBottomColor: colors.border },
  scheduleDate: { fontSize: fontSize.base, color: colors.textPrimary },
  scheduleBadge: { backgroundColor: colors.primaryLight, borderRadius: radius.full, paddingHorizontal: spacing.md, paddingVertical: 4, minWidth: 36, alignItems: 'center' },
  scheduleBadgeText: { color: colors.primary, fontWeight: '600', fontSize: fontSize.sm },
});
