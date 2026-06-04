import React, { useCallback, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  FlatList,
  ActivityIndicator,
  Alert,
  Platform,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useFocusEffect, useRouter, Stack } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { colors, spacing, radius, fontSize, getToneColor } from '@/src/theme';
import { api, Vocabulary } from '@/src/api/client';

type LibraryItem = Vocabulary & { in_deck: boolean; is_custom: boolean };

export default function LibraryScreen() {
  const router = useRouter();
  const [items, setItems] = useState<LibraryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState('');
  const [filter, setFilter] = useState<'all' | 'npcr' | 'custom'>('all');
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [submitting, setSubmitting] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const data = await api.library({
        q: query || undefined,
        source: filter === 'all' ? undefined : filter,
      });
      setItems(data);
    } catch (e) {
      setItems([]);
    } finally {
      setLoading(false);
    }
  }, [query, filter]);

  useFocusEffect(
    useCallback(() => {
      load();
    }, [load]),
  );

  const toggleSelect = (id: string) => {
    setSelected((s) => {
      const next = new Set(s);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const handleAddSelected = async () => {
    if (selected.size === 0) return;
    setSubmitting(true);
    try {
      const r = await api.addToDeck(Array.from(selected));
      setSelected(new Set());
      await load();
      const msg = `${r.added} word${r.added === 1 ? '' : 's'} added to your deck.`;
      if (Platform.OS === 'web') {
        // eslint-disable-next-line no-undef
        if (typeof window !== 'undefined') window.alert(msg);
      } else {
        Alert.alert('Added', msg);
      }
    } catch (e: any) {
      Alert.alert('Error', e.message || 'Could not add');
    } finally {
      setSubmitting(false);
    }
  };

  const handleAddSingle = async (id: string) => {
    try {
      await api.addToDeck([id]);
      setItems((prev) => prev.map((it) => (it.id === id ? { ...it, in_deck: true } : it)));
    } catch (e) {
      // ignore
    }
  };

  const handleRemove = async (id: string) => {
    try {
      await api.removeFromDeck(id);
      setItems((prev) => prev.map((it) => (it.id === id ? { ...it, in_deck: false } : it)));
    } catch (e) {
      // ignore
    }
  };

  const deleteCustom = async (id: string) => {
    try {
      await api.deleteCustomVocab(id);
      setItems((prev) => prev.filter((it) => it.id !== id));
      setSelected((s) => {
        const next = new Set(s);
        next.delete(id);
        return next;
      });
    } catch (e: any) {
      Alert.alert('Error', e?.message || 'Could not delete word');
    }
  };

  const handleDelete = (item: LibraryItem) => {
    const message = `Delete "${item.simplified}"? This removes it from your library and deck permanently.`;
    if (Platform.OS === 'web') {
      if (typeof window !== 'undefined' && window.confirm(message)) deleteCustom(item.id);
      return;
    }
    Alert.alert('Delete word', message, [
      { text: 'Cancel', style: 'cancel' },
      { text: 'Delete', style: 'destructive', onPress: () => deleteCustom(item.id) },
    ]);
  };

  return (
    <SafeAreaView style={styles.safe} edges={['top']}>
      <Stack.Screen options={{ headerShown: false }} />

      <View style={styles.header}>
        <TouchableOpacity testID="library-back-button" onPress={() => router.back()} style={styles.backBtn}>
          <Ionicons name="arrow-back" size={24} color={colors.textPrimary} />
        </TouchableOpacity>
        <View style={styles.flex}>
          <Text style={styles.title}>Vocabulary Library</Text>
          <Text style={styles.subtitle}>Tap to add words to your deck</Text>
        </View>
        <TouchableOpacity
          testID="library-add-custom-button"
          onPress={() => router.push('/add-word')}
          style={styles.headerAction}
        >
          <Ionicons name="add-circle" size={28} color={colors.primary} />
        </TouchableOpacity>
      </View>

      <View style={styles.searchRow}>
        <Ionicons name="search" size={18} color={colors.textTertiary} />
        <TextInput
          testID="library-search-input"
          style={styles.search}
          placeholder="Search Chinese, pinyin, or English..."
          placeholderTextColor={colors.textTertiary}
          value={query}
          onChangeText={setQuery}
          onSubmitEditing={load}
          returnKeyType="search"
          autoCapitalize="none"
        />
        {query.length > 0 && (
          <TouchableOpacity onPress={() => { setQuery(''); setTimeout(load, 0); }}>
            <Ionicons name="close-circle" size={18} color={colors.textTertiary} />
          </TouchableOpacity>
        )}
      </View>

      <View style={styles.filterRow}>
        {(['all', 'npcr', 'custom'] as const).map((f) => (
          <TouchableOpacity
            key={f}
            testID={`library-filter-${f}`}
            style={[styles.filterChip, filter === f && styles.filterChipActive]}
            onPress={() => setFilter(f)}
          >
            <Text style={[styles.filterText, filter === f && styles.filterTextActive]}>
              {f === 'all' ? 'All' : f === 'npcr' ? 'NPCR' : 'Custom'}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      {loading ? (
        <View style={styles.loading}>
          <ActivityIndicator color={colors.primary} size="large" />
        </View>
      ) : (
        <FlatList
          data={items}
          keyExtractor={(i) => i.id}
          contentContainerStyle={styles.list}
          ListEmptyComponent={() => (
            <View style={styles.empty}>
              <Text style={styles.emptyText}>No words found. Try a different search or filter.</Text>
            </View>
          )}
          renderItem={({ item }) => {
            const isSelected = selected.has(item.id);
            return (
              <TouchableOpacity
                testID={`library-row-${item.simplified}`}
                style={[styles.row, isSelected && styles.rowSelected]}
                onPress={() => (item.in_deck ? null : toggleSelect(item.id))}
                activeOpacity={item.in_deck ? 1 : 0.7}
              >
                <Text style={styles.rowHanzi}>{item.simplified}</Text>
                <View style={styles.flex}>
                  <Text style={[styles.rowPinyin, { color: getToneColor(item.pinyin) }]}>{item.pinyin}</Text>
                  <Text style={styles.rowEnglish} numberOfLines={2}>
                    {item.english}
                  </Text>
                  <View style={styles.rowMeta}>
                    {item.lesson_number ? (
                      <View style={styles.metaPill}>
                        <Text style={styles.metaPillText}>L{item.lesson_number}</Text>
                      </View>
                    ) : (
                      <View style={[styles.metaPill, { backgroundColor: colors.tone3 + '20' }]}>
                        <Text style={[styles.metaPillText, { color: colors.tone3 }]}>Custom</Text>
                      </View>
                    )}
                  </View>
                </View>
                {item.is_custom && (
                  <TouchableOpacity
                    testID={`library-delete-${item.simplified}`}
                    onPress={() => handleDelete(item)}
                    style={styles.deleteBtn}
                    hitSlop={8}
                  >
                    <Ionicons name="trash-outline" size={20} color={colors.error} />
                  </TouchableOpacity>
                )}
                {item.in_deck ? (
                  <TouchableOpacity
                    testID={`library-remove-${item.simplified}`}
                    onPress={() => handleRemove(item.id)}
                    style={styles.deckBadge}
                  >
                    <Ionicons name="checkmark-circle" size={22} color={colors.success} />
                    <Text style={styles.deckBadgeText}>In deck</Text>
                  </TouchableOpacity>
                ) : isSelected ? (
                  <View style={[styles.deckBadge, { backgroundColor: colors.primaryLight }]}>
                    <Ionicons name="checkbox" size={22} color={colors.primary} />
                  </View>
                ) : (
                  <TouchableOpacity
                    testID={`library-add-${item.simplified}`}
                    onPress={() => handleAddSingle(item.id)}
                    style={styles.addBtn}
                  >
                    <Ionicons name="add" size={22} color={colors.primary} />
                  </TouchableOpacity>
                )}
              </TouchableOpacity>
            );
          }}
        />
      )}

      {selected.size > 0 && (
        <View style={styles.bulkBar} testID="library-bulk-bar">
          <Text style={styles.bulkText}>{selected.size} selected</Text>
          <TouchableOpacity
            testID="library-bulk-add-button"
            style={[styles.bulkBtn, submitting && { opacity: 0.6 }]}
            onPress={handleAddSelected}
            disabled={submitting}
          >
            {submitting ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text style={styles.bulkBtnText}>Add to deck</Text>
            )}
          </TouchableOpacity>
        </View>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.background },
  flex: { flex: 1 },
  loading: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  header: { padding: spacing.md, flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  backBtn: { padding: spacing.sm, minWidth: 48, minHeight: 48, justifyContent: 'center' },
  headerAction: { padding: spacing.sm, minWidth: 48, minHeight: 48, justifyContent: 'center', alignItems: 'center' },
  title: { fontSize: fontSize.xxl, color: colors.textPrimary, fontWeight: '500' },
  subtitle: { fontSize: fontSize.sm, color: colors.textSecondary },
  searchRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    marginHorizontal: spacing.lg,
    paddingHorizontal: spacing.md,
    backgroundColor: colors.surface,
    borderRadius: radius.md,
    borderWidth: 1,
    borderColor: colors.border,
  },
  search: { flex: 1, paddingVertical: 12, fontSize: fontSize.base, color: colors.textPrimary, minHeight: 44 },
  filterRow: { flexDirection: 'row', gap: spacing.sm, paddingHorizontal: spacing.lg, marginTop: spacing.md, marginBottom: spacing.sm },
  filterChip: { paddingHorizontal: spacing.md, paddingVertical: spacing.sm, borderRadius: radius.full, backgroundColor: colors.surface, borderWidth: 1, borderColor: colors.border, minHeight: 36, justifyContent: 'center' },
  filterChipActive: { backgroundColor: colors.primary, borderColor: colors.primary },
  filterText: { fontSize: fontSize.sm, color: colors.textSecondary, fontWeight: '500' },
  filterTextActive: { color: '#fff' },
  list: { padding: spacing.lg, paddingTop: 0, paddingBottom: 100 },
  empty: { padding: spacing.xl, alignItems: 'center' },
  emptyText: { color: colors.textSecondary, textAlign: 'center' },
  row: { flexDirection: 'row', alignItems: 'center', backgroundColor: colors.surface, borderRadius: radius.lg, borderWidth: 1, borderColor: colors.border, padding: spacing.md, gap: spacing.md, marginBottom: spacing.sm, minHeight: 76 },
  rowSelected: { borderColor: colors.primary, backgroundColor: colors.primaryLight },
  rowHanzi: { fontSize: fontSize.xxl, color: colors.textPrimary, fontWeight: '500', width: 60 },
  rowPinyin: { fontSize: fontSize.base, fontWeight: '500' },
  rowEnglish: { fontSize: fontSize.sm, color: colors.textSecondary, marginTop: 2 },
  rowMeta: { flexDirection: 'row', gap: spacing.xs, marginTop: 4 },
  metaPill: { backgroundColor: colors.surfaceAlt, paddingHorizontal: spacing.sm, paddingVertical: 2, borderRadius: radius.sm },
  metaPillText: { fontSize: 10, color: colors.textSecondary, fontWeight: '600', textTransform: 'uppercase' },
  addBtn: { width: 36, height: 36, borderRadius: radius.full, backgroundColor: colors.primaryLight, alignItems: 'center', justifyContent: 'center' },
  deleteBtn: { width: 36, height: 36, borderRadius: radius.full, backgroundColor: colors.errorLight, alignItems: 'center', justifyContent: 'center' },
  deckBadge: { flexDirection: 'row', alignItems: 'center', gap: 4, paddingHorizontal: spacing.sm, paddingVertical: spacing.xs, borderRadius: radius.full, backgroundColor: colors.successLight, minHeight: 32 },
  deckBadgeText: { fontSize: fontSize.xs, color: colors.success, fontWeight: '600' },
  bulkBar: { position: 'absolute', bottom: 0, left: 0, right: 0, padding: spacing.lg, backgroundColor: colors.surface, borderTopWidth: 1, borderTopColor: colors.border, flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  bulkText: { fontSize: fontSize.base, color: colors.textPrimary, fontWeight: '500' },
  bulkBtn: { backgroundColor: colors.primary, paddingHorizontal: spacing.lg, paddingVertical: spacing.md, borderRadius: radius.md, minHeight: 44, justifyContent: 'center' },
  bulkBtnText: { color: '#fff', fontWeight: '600' },
});
