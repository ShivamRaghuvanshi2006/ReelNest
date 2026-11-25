import { reelnestEngine, type NativePermissionStatus } from 'reelnest-engine';

/**
 * Typed permission status built on the engine module's getPermissionStatus
 * (docs/NATIVE_CONTRACT.md section 6, Permissions). Always check the specific field: this is an object, never a boolean.
 */
export interface PermissionStatus extends NativePermissionStatus {
  /** POST_NOTIFICATIONS is granted (always true below Android 13 where the module reports "granted"). */
  hasNotificationPermission: boolean;
  /** Legacy WRITE_EXTERNAL_STORAGE is granted or not needed on this Android version. */
  hasStoragePermission: boolean;
  /** Notifications and storage are usable. Battery optimization is advisory and not included. */
  isPermissionGranted: boolean;
}

function toStatus(native: NativePermissionStatus): PermissionStatus {
  const hasNotificationPermission = native.notifications === 'granted';
  const hasStoragePermission = native.legacyStorage !== 'denied';
  return {
    ...native,
    hasNotificationPermission,
    hasStoragePermission,
    isPermissionGranted: hasNotificationPermission && hasStoragePermission,
  };
}

/** Prompts for whatever is missing (notifications, legacy storage) and returns the re-read status. */
export async function requestReelNestPermissions(): Promise<PermissionStatus> {
  const before = await reelnestEngine.getPermissionStatus();
  if (before.notifications !== 'granted') {
    await reelnestEngine.requestNotifications();
  }
  if (before.legacyStorage === 'denied') {
    await reelnestEngine.requestLegacyStorage();
  }
  return toStatus(await reelnestEngine.getPermissionStatus());
}

/** Opens the system battery optimization screen so downloads survive Doze. */
export async function openBatterySettings(): Promise<void> {
  await reelnestEngine.openBatterySettings();
}
