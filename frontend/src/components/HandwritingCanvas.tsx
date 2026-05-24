/**
 * Cross-platform handwriting canvas. Uses SVG paths driven by PanResponder so it
 * works identically on web, iOS and Android without native dependencies.
 * Exposes captureBase64() via ref — captures the rendered View as a PNG string
 * suitable for upload to the /api/writing/recognize endpoint.
 */
import React, {
  forwardRef,
  useImperativeHandle,
  useRef,
  useState,
} from 'react';
import {
  View,
  PanResponder,
  StyleSheet,
  TouchableOpacity,
  Text,
  Platform,
} from 'react-native';
import Svg, { Path } from 'react-native-svg';
import { captureRef } from 'react-native-view-shot';
import { Ionicons } from '@expo/vector-icons';
import { colors, spacing, radius, fontSize } from '@/src/theme';

export type HandwritingCanvasHandle = {
  captureBase64: () => Promise<string>;
  clear: () => void;
  isEmpty: () => boolean;
};

type Props = {
  height?: number;
  testID?: string;
};

const HandwritingCanvas = forwardRef<HandwritingCanvasHandle, Props>(
  ({ height = 260, testID }, ref) => {
    const viewShotRef = useRef<View>(null);
    const [paths, setPaths] = useState<string[]>([]);
    const [currentPath, setCurrentPath] = useState<string>('');

    const panResponder = useRef(
      PanResponder.create({
        onStartShouldSetPanResponder: () => true,
        onMoveShouldSetPanResponder: () => true,
        onPanResponderGrant: (evt) => {
          const { locationX, locationY } = evt.nativeEvent;
          setCurrentPath(`M${locationX.toFixed(1)},${locationY.toFixed(1)}`);
        },
        onPanResponderMove: (evt) => {
          const { locationX, locationY } = evt.nativeEvent;
          setCurrentPath((prev) => `${prev} L${locationX.toFixed(1)},${locationY.toFixed(1)}`);
        },
        onPanResponderRelease: () => {
          setCurrentPath((prev) => {
            if (prev) setPaths((p) => [...p, prev]);
            return '';
          });
        },
      }),
    ).current;

    useImperativeHandle(
      ref,
      () => ({
        clear: () => {
          setPaths([]);
          setCurrentPath('');
        },
        isEmpty: () => paths.length === 0 && !currentPath,
        captureBase64: async () => {
          if (!viewShotRef.current) throw new Error('Canvas not ready');
          const result = await captureRef(viewShotRef.current, {
            format: 'png',
            quality: 0.8,
            result: 'base64',
            // Important: white bg & enough resolution for the LLM to see strokes clearly.
            width: 512,
            height: 512,
          });
          return result;
        },
      }),
      [paths, currentPath],
    );

    return (
      <View testID={testID} style={[styles.wrap, { height }]}>
        <View
          ref={viewShotRef}
          collapsable={false}
          style={[styles.canvas, { height }]}
          {...panResponder.panHandlers}
          testID="handwriting-canvas-surface"
        >
          <Svg width="100%" height="100%" style={StyleSheet.absoluteFill}>
            {/* Light center guide */}
            <Path
              d={`M0,${height / 2} L9999,${height / 2}`}
              stroke={colors.border}
              strokeWidth={1}
              strokeDasharray="4 6"
            />
            {paths.map((d, i) => (
              <Path
                key={i}
                d={d}
                stroke={colors.textPrimary}
                strokeWidth={Platform.OS === 'web' ? 4 : 5}
                strokeLinecap="round"
                strokeLinejoin="round"
                fill="none"
              />
            ))}
            {currentPath ? (
              <Path
                d={currentPath}
                stroke={colors.textPrimary}
                strokeWidth={Platform.OS === 'web' ? 4 : 5}
                strokeLinecap="round"
                strokeLinejoin="round"
                fill="none"
              />
            ) : null}
          </Svg>
          {paths.length === 0 && !currentPath && (
            <View style={styles.placeholder} pointerEvents="none">
              <Ionicons name="brush-outline" size={28} color={colors.textTertiary} />
              <Text style={styles.placeholderText}>Write the characters here</Text>
            </View>
          )}
        </View>

        <View style={styles.toolbar}>
          <TouchableOpacity
            testID="handwriting-undo-button"
            style={styles.toolBtn}
            onPress={() => setPaths((p) => p.slice(0, -1))}
            disabled={paths.length === 0}
          >
            <Ionicons name="arrow-undo" size={18} color={paths.length === 0 ? colors.textTertiary : colors.textPrimary} />
            <Text style={[styles.toolText, paths.length === 0 && { color: colors.textTertiary }]}>Undo</Text>
          </TouchableOpacity>
          <TouchableOpacity
            testID="handwriting-clear-button"
            style={styles.toolBtn}
            onPress={() => {
              setPaths([]);
              setCurrentPath('');
            }}
            disabled={paths.length === 0 && !currentPath}
          >
            <Ionicons name="trash-outline" size={18} color={paths.length === 0 ? colors.textTertiary : colors.textPrimary} />
            <Text style={[styles.toolText, paths.length === 0 && { color: colors.textTertiary }]}>Clear</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  },
);

HandwritingCanvas.displayName = 'HandwritingCanvas';

const styles = StyleSheet.create({
  wrap: { width: '100%' },
  canvas: {
    backgroundColor: '#FFFFFF',
    borderRadius: radius.lg,
    borderWidth: 1,
    borderColor: colors.border,
    overflow: 'hidden',
    position: 'relative',
  },
  placeholder: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.sm,
  },
  placeholderText: { color: colors.textTertiary, fontSize: fontSize.sm },
  toolbar: {
    flexDirection: 'row',
    gap: spacing.md,
    marginTop: spacing.sm,
    justifyContent: 'flex-end',
  },
  toolBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: radius.sm,
    minHeight: 36,
  },
  toolText: { fontSize: fontSize.sm, color: colors.textPrimary, fontWeight: '500' },
});

export default HandwritingCanvas;
