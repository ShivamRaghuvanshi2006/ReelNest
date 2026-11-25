import React, { useCallback, useMemo } from 'react';
import { Platform, StyleSheet, View } from 'react-native';
import * as Clipboard from 'expo-clipboard';
import { Screen, EmptyBlock } from '../components/ui';
import { useReelNestEngine } from '../context/EngineContext';
import { useTheme } from '../context/ThemeContext';
import { ThemeColors } from '../constants/theme';
import { empty } from '../constants/copy';
import { reelnestEngine } from 'reelnest-engine';
import { START_ENGINE_LABEL, engineFailureAction } from '../utils/addErrorNotice';

export default function EngineErrorScreen() {
  const { colors } = useTheme();
  const styles = useMemo(() => makeStyles(colors), [colors]);
  const { engineStatus, retryEngine } = useReelNestEngine();
  const failure = engineFailureAction(engineStatus.kind === 'unavailable' ? engineStatus.code : undefined);
  const message = engineStatus.kind === 'starting'
    ? 'The downloader took too long to start.'
    : engineStatus.message || "The downloader didn't say why.";

  const copyDetails = useCallback(async () => {
    const details = [
      empty.engineError.title,
      message,
      `Platform: ${Platform.OS} ${String(Platform.Version)}`,
    ].join('\n');
    try {
      await Clipboard.setStringAsync(details);
    } catch {
      // Clipboard unavailable; nothing else to do.
    }
  }, [message]);

  // Pick folder again: choose a folder (it is persisted as the target), then start the engine.
  const primaryPress = useCallback(async () => {
    if (failure.action === 'pickFolder') {
      try {
        await reelnestEngine.pickDownloadFolder();
      } catch {
        // The picker failed; starting again below still reports the real reason.
      }
    }
    await retryEngine();
  }, [failure.action, retryEngine]);

  return (
    <Screen edges={['top', 'bottom', 'left', 'right']} testID="engine-error">
      <View style={styles.center}>
        <EmptyBlock
          icon="warning"
          error
          title={empty.engineError.title}
          body={message}
          primary={{ label: failure.label, onPress: primaryPress }}
          secondary={
            failure.action === 'pickFolder'
              ? { label: START_ENGINE_LABEL, onPress: () => void retryEngine() }
              : { label: 'Copy details', onPress: copyDetails }
          }
        />
      </View>
    </Screen>
  );
}

const makeStyles = (_c: ThemeColors) => StyleSheet.create({ center: { flex: 1, justifyContent: 'center' } });
