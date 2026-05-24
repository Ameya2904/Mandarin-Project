import React, { useCallback, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  FlatList,
  ActivityIndicator,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useFocusEffect, useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { colors, spacing, radius, fontSize, getToneColor } from '@/src/theme';
import { api, Lesson } from '@/src/api/client';

type Sentence = {
  chinese: string;
  pinyin: string;
  english: string;
  lesson_title: string;
  lesson_number: number;
};

export default function SpeakScreen() {
  const router = useRouter();
  const [sentences, setSentences] = useState<Sentence[]>([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const lessons: Lesson[] = await api.lessons();
      const collected: Sentence[] = [];
      for (const lesson of lessons) {
        for (const line of lesson.dialogue || []) {
          collected.push({
            chinese: line.chinese,
            pinyin: line.pinyin,
            english: line.english,
            lesson_title: lesson.title,
            lesson_number: lesson.lesson_number,
          });
        }
      }
      setSentences(collected);
    } catch (e) {
      setSentences([]);
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
        <Text style={styles.title}>Speaking Practice</Text>
        <Text style={styles.subtitle}>Active production from NPCR dialogues</Text>
      </View>

      {loading ? (
        <View style={styles.loading}>
          <ActivityIndicator color={colors.primary} size="large" />
        </View>
      ) : (
        <FlatList
          data={sentences}
          keyExtractor={(item, i) => `${item.lesson_number}-${i}`}
          contentContainerStyle={styles.list}
          renderItem={({ item }) => (
            <TouchableOpacity
              testID={`speak-sentence-${item.chinese}`}
              style={styles.sentenceCard}
              onPress={() =>
                router.push({
                  pathname: '/speak-practice',
                  params: {
                    chinese: item.chinese,
                    pinyin: item.pinyin,
                    english: item.english,
                  },
                })
              }
            >
              <View style={styles.sentenceRow}>
                <View style={styles.flex}>
                  <Text style={styles.lessonTag}>Lesson {item.lesson_number}</Text>
                  <Text style={styles.sentenceHanzi}>{item.chinese}</Text>
                  <Text style={[styles.sentencePinyin, { color: getToneColor(item.pinyin) }]}>
                    {item.pinyin}
                  </Text>
                  <Text style={styles.sentenceEnglish}>{item.english}</Text>
                </View>
                <View style={styles.micButton}>
                  <Ionicons name="mic" size={22} color="#fff" />
                </View>
              </View>
            </TouchableOpacity>
          )}
        />
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.background },
  flex: { flex: 1 },
  loading: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  header: { padding: spacing.lg, paddingBottom: spacing.md },
  title: { fontSize: fontSize.display, color: colors.textPrimary, fontWeight: '400', letterSpacing: -0.5 },
  subtitle: { fontSize: fontSize.base, color: colors.textSecondary, marginTop: 4 },
  list: { padding: spacing.lg, paddingTop: 0 },
  sentenceCard: {
    backgroundColor: colors.surface,
    borderRadius: radius.lg,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.lg,
    marginBottom: spacing.md,
  },
  sentenceRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  lessonTag: { fontSize: fontSize.xs, color: colors.textTertiary, textTransform: 'uppercase', letterSpacing: 1 },
  sentenceHanzi: { fontSize: fontSize.xxl, color: colors.textPrimary, fontWeight: '500', marginTop: 6 },
  sentencePinyin: { fontSize: fontSize.base, marginTop: 4 },
  sentenceEnglish: { fontSize: fontSize.sm, color: colors.textSecondary, marginTop: 4 },
  micButton: {
    width: 48,
    height: 48,
    borderRadius: radius.full,
    backgroundColor: colors.primary,
    alignItems: 'center',
    justifyContent: 'center',
  },
});
