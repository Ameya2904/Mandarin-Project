import React, { useCallback, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SectionList,
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

type LessonGroup = {
  lesson_number: number;
  lesson_title: string;
  sentences: Sentence[];
};

type Section = {
  lesson_number: number;
  lesson_title: string;
  sentences: Sentence[];
  data: Sentence[];
};

export default function SpeakScreen() {
  const router = useRouter();
  const [groups, setGroups] = useState<LessonGroup[]>([]);
  const [expanded, setExpanded] = useState<Set<number>>(new Set());
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const lessons: Lesson[] = await api.lessons();
      const groupMap: Record<number, LessonGroup> = {};
      for (const lesson of lessons) {
        groupMap[lesson.lesson_number] = {
          lesson_number: lesson.lesson_number,
          lesson_title: lesson.title,
          sentences: [],
        };
        for (const line of lesson.dialogue || []) {
          groupMap[lesson.lesson_number].sentences.push({
            chinese: line.chinese,
            pinyin: line.pinyin,
            english: line.english,
            lesson_title: lesson.title,
            lesson_number: lesson.lesson_number,
          });
        }
      }
      setGroups(
        Object.values(groupMap).sort((a, b) => a.lesson_number - b.lesson_number)
      );
    } catch {
      setGroups([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useFocusEffect(
    useCallback(() => {
      load();
    }, [load])
  );

  const toggle = (lessonNumber: number) => {
    setExpanded((prev) => {
      const next = new Set(prev);
      if (next.has(lessonNumber)) next.delete(lessonNumber);
      else next.add(lessonNumber);
      return next;
    });
  };

  const sections: Section[] = groups.map((g) => ({
    ...g,
    data: expanded.has(g.lesson_number) ? g.sentences : [],
  }));

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
        <SectionList
          sections={sections}
          keyExtractor={(item, i) => `${item.lesson_number}-${i}`}
          contentContainerStyle={styles.list}
          stickySectionHeadersEnabled={false}
          renderSectionHeader={({ section }) => {
            const isOpen = expanded.has(section.lesson_number);
            return (
              <TouchableOpacity
                style={styles.folderHeader}
                onPress={() => toggle(section.lesson_number)}
                activeOpacity={0.7}
              >
                <View style={styles.folderIconWrap}>
                  <Ionicons
                    name={isOpen ? 'folder-open-outline' : 'folder-outline'}
                    size={20}
                    color={colors.primary}
                  />
                </View>
                <View style={styles.folderMeta}>
                  <Text style={styles.folderLabel}>Lesson {section.lesson_number}</Text>
                  <Text style={styles.folderTitle} numberOfLines={1}>
                    {section.lesson_title}
                  </Text>
                </View>
                <Text style={styles.folderCount}>{section.sentences.length}</Text>
                <Ionicons
                  name={isOpen ? 'chevron-up' : 'chevron-down'}
                  size={16}
                  color={colors.textTertiary}
                />
              </TouchableOpacity>
            );
          }}
          renderItem={({ item, index, section }) => {
            const isLast = index === section.data.length - 1;
            return (
              <TouchableOpacity
                testID={`speak-sentence-${item.chinese}`}
                style={[styles.sentenceCard, isLast && styles.sentenceCardLast]}
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
            );
          }}
          renderSectionFooter={({ section }) =>
            expanded.has(section.lesson_number) ? <View style={styles.sectionFooter} /> : null
          }
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
  list: { padding: spacing.lg, paddingTop: 0, paddingBottom: spacing.xxl },

  folderHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    backgroundColor: colors.surface,
    borderRadius: radius.lg,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.md,
    marginBottom: spacing.xs,
    minHeight: 56,
  },
  folderIconWrap: {
    width: 36,
    height: 36,
    borderRadius: radius.md,
    backgroundColor: colors.primaryLight,
    alignItems: 'center',
    justifyContent: 'center',
  },
  folderMeta: { flex: 1 },
  folderLabel: {
    fontSize: fontSize.xs,
    color: colors.textTertiary,
    fontWeight: '600',
    letterSpacing: 1,
    textTransform: 'uppercase',
  },
  folderTitle: { fontSize: fontSize.base, color: colors.textPrimary, fontWeight: '500', marginTop: 1 },
  folderCount: {
    fontSize: fontSize.sm,
    color: colors.textTertiary,
    fontWeight: '500',
    marginRight: spacing.xs,
  },

  sentenceCard: {
    backgroundColor: colors.surface,
    borderLeftWidth: 2,
    borderLeftColor: colors.primaryLight,
    borderRightWidth: 1,
    borderRightColor: colors.border,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
    padding: spacing.lg,
    marginLeft: spacing.lg,
  },
  sentenceCardLast: {
    borderBottomLeftRadius: radius.lg,
    borderBottomRightRadius: radius.lg,
    marginBottom: 0,
  },
  sentenceRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  sentenceHanzi: { fontSize: fontSize.xxl, color: colors.textPrimary, fontWeight: '500' },
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
  sectionFooter: { height: spacing.md },
});
