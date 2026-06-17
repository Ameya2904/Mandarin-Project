/**
 * Add-word — form to create a custom vocabulary entry.
 *
 * Chinese / pinyin / English are required; the example sentence is optional.
 * On save the backend auto-adds the new word to the user's deck.
 */
import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
  ActivityIndicator,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter, Stack } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { colors, spacing, radius, fontSize } from '@/src/theme';
import { api } from '@/src/api/client';

export default function AddWordScreen() {
  const router = useRouter();
  const [simplified, setSimplified] = useState('');
  const [pinyin, setPinyin] = useState('');
  const [english, setEnglish] = useState('');
  const [exampleChinese, setExampleChinese] = useState('');
  const [examplePinyin, setExamplePinyin] = useState('');
  const [exampleEnglish, setExampleEnglish] = useState('');
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);

  const handleSave = async () => {
    setError('');
    if (!simplified.trim() || !pinyin.trim() || !english.trim()) {
      setError('Chinese, Pinyin, and English are required.');
      return;
    }
    setSaving(true);
    try {
      await api.createCustomVocab({
        simplified: simplified.trim(),
        pinyin: pinyin.trim(),
        english: english.trim(),
        example_chinese: exampleChinese.trim() || undefined,
        example_pinyin: examplePinyin.trim() || undefined,
        example_english: exampleEnglish.trim() || undefined,
      });
      router.back();
    } catch (e: any) {
      setError(e.message || 'Could not save the word');
    } finally {
      setSaving(false);
    }
  };

  return (
    <SafeAreaView style={styles.safe} edges={['top']}>
      <Stack.Screen options={{ headerShown: false }} />
      <KeyboardAvoidingView style={styles.flex} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
        <View style={styles.header}>
          <TouchableOpacity testID="add-word-back-button" onPress={() => router.back()} style={styles.backBtn}>
            <Ionicons name="arrow-back" size={24} color={colors.textPrimary} />
          </TouchableOpacity>
          <Text style={styles.title}>Add Custom Word</Text>
        </View>

        <ScrollView contentContainerStyle={styles.scroll} keyboardShouldPersistTaps="handled">
          <Text style={styles.subtitle}>
            New words are automatically added to your deck and ready for review.
          </Text>

          <Section title="Required">
            <Field label="Chinese (simplified)" required>
              <TextInput
                testID="add-word-simplified-input"
                style={styles.input}
                value={simplified}
                onChangeText={setSimplified}
                placeholder="例如: 朋友"
                placeholderTextColor={colors.textTertiary}
                autoCorrect={false}
              />
            </Field>
            <Field label="Pinyin" required>
              <TextInput
                testID="add-word-pinyin-input"
                style={styles.input}
                value={pinyin}
                onChangeText={setPinyin}
                placeholder="péngyǒu"
                placeholderTextColor={colors.textTertiary}
                autoCapitalize="none"
                autoCorrect={false}
              />
            </Field>
            <Field label="English meaning" required>
              <TextInput
                testID="add-word-english-input"
                style={styles.input}
                value={english}
                onChangeText={setEnglish}
                placeholder="friend"
                placeholderTextColor={colors.textTertiary}
                autoCapitalize="none"
              />
            </Field>
          </Section>

          <Section title="Example sentence (optional)">
            <Field label="Chinese example">
              <TextInput
                testID="add-word-example-chinese-input"
                style={styles.input}
                value={exampleChinese}
                onChangeText={setExampleChinese}
                placeholder="他是我的朋友"
                placeholderTextColor={colors.textTertiary}
              />
            </Field>
            <Field label="Pinyin example">
              <TextInput
                testID="add-word-example-pinyin-input"
                style={styles.input}
                value={examplePinyin}
                onChangeText={setExamplePinyin}
                placeholder="Tā shì wǒ de péngyǒu"
                placeholderTextColor={colors.textTertiary}
                autoCapitalize="none"
              />
            </Field>
            <Field label="English example">
              <TextInput
                testID="add-word-example-english-input"
                style={styles.input}
                value={exampleEnglish}
                onChangeText={setExampleEnglish}
                placeholder="He is my friend"
                placeholderTextColor={colors.textTertiary}
              />
            </Field>
          </Section>

          {error ? (
            <Text testID="add-word-error" style={styles.error}>
              {error}
            </Text>
          ) : null}
        </ScrollView>

        <View style={styles.footer}>
          <TouchableOpacity
            testID="add-word-save-button"
            style={[styles.saveBtn, saving && { opacity: 0.6 }]}
            onPress={handleSave}
            disabled={saving}
          >
            {saving ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text style={styles.saveBtnText}>Save & Add to Deck</Text>
            )}
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <View style={styles.section}>
      <Text style={styles.sectionTitle}>{title}</Text>
      {children}
    </View>
  );
}

function Field({ label, required, children }: { label: string; required?: boolean; children: React.ReactNode }) {
  return (
    <View style={styles.field}>
      <Text style={styles.fieldLabel}>
        {label} {required && <Text style={{ color: colors.error }}>*</Text>}
      </Text>
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.background },
  flex: { flex: 1 },
  header: { flexDirection: 'row', alignItems: 'center', padding: spacing.md, gap: spacing.sm },
  backBtn: { padding: spacing.sm, minWidth: 48, minHeight: 48, justifyContent: 'center' },
  title: { fontSize: fontSize.xl, color: colors.textPrimary, fontWeight: '500' },
  subtitle: { fontSize: fontSize.sm, color: colors.textSecondary, marginBottom: spacing.lg, paddingHorizontal: spacing.lg },
  scroll: { paddingBottom: spacing.xxl },
  section: { paddingHorizontal: spacing.lg, marginBottom: spacing.lg },
  sectionTitle: { fontSize: fontSize.xs, color: colors.textTertiary, textTransform: 'uppercase', letterSpacing: 1, marginBottom: spacing.md, fontWeight: '600' },
  field: { marginBottom: spacing.md },
  fieldLabel: { fontSize: fontSize.sm, color: colors.textSecondary, marginBottom: spacing.xs, fontWeight: '500' },
  input: { backgroundColor: colors.surface, borderRadius: radius.md, borderWidth: 1, borderColor: colors.border, padding: spacing.md, fontSize: fontSize.lg, color: colors.textPrimary, minHeight: 48 },
  error: { color: colors.error, padding: spacing.md, marginHorizontal: spacing.lg, backgroundColor: colors.errorLight, borderRadius: radius.md, fontSize: fontSize.sm },
  footer: { padding: spacing.lg, borderTopWidth: 1, borderTopColor: colors.border, backgroundColor: colors.background },
  saveBtn: { backgroundColor: colors.primary, paddingVertical: 16, borderRadius: radius.md, alignItems: 'center', justifyContent: 'center', minHeight: 52 },
  saveBtnText: { color: '#fff', fontSize: fontSize.lg, fontWeight: '600' },
});
