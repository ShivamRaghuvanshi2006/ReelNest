import React, { useMemo } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { useTheme } from '../../context/ThemeContext';
import { ThemeColors, type } from '../../constants/theme';

/**
 * The REELNEST wordmark: Cabinet Grotesk in every font style, with NEST in the accent.
 * Matches assets/brand/reelnest-wordmark.svg without shipping a second copy of the lettering.
 */
export function Wordmark({ width }: { width?: number }) {
  const { colors } = useTheme();
  const styles = useMemo(() => makeStyles(colors), [colors]);
  return (
    <View style={[styles.wrap, width ? { maxWidth: width } : null]} accessible accessibilityRole="image" accessibilityLabel="ReelNest">
      <Text style={styles.word}>
        REEL<Text style={styles.nest}>NEST</Text>
      </Text>
    </View>
  );
}

const makeStyles = (c: ThemeColors) =>
  StyleSheet.create({
    wrap: { alignItems: 'center' },
    word: { ...type.brand, fontSize: type.size.display, letterSpacing: -1, color: c.text },
    nest: { color: c.accentText },
  });
