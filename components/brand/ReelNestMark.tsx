import React from 'react';
import { Pressable, View } from 'react-native';
import Svg, { Circle, G, Path, Rect } from 'react-native-svg';
import { haptic } from '../../constants/haptics';
import { brandColors } from '../../constants/brand';

export interface ReelNestMarkProps {
  /** Rendered height in dp (width equals height for a 1:1 square). */
  height?: number;
  width?: number;
  /** Kept for call-site compatibility; the ReelNest mark is always still. */
  cruising?: boolean;
  tappable?: boolean;
  /** Kept for call-site compatibility; the ReelNest mark has no arrival animation. */
  arrive?: boolean;
}

/**
 * ReelNest brand emblem: a neo-brutalist film reel with an R monogram.
 *
 * Official colours (constants/brand.ts):
 *   primary yellow #ffe17c, deep charcoal #171e19, sage #b7c6c2, white, black.
 *
 * The look is a 3 px black outline and a 4 px hard black shadow, with geometric
 * film-strip perforations and spool apertures.
 */
export function ReelNestMark({ height = 24, width, tappable = false }: ReelNestMarkProps) {
  const size = width ?? height;

  const markSvg = (
    <Svg width={size} height={size} viewBox="0 0 100 100">
      {/* 4px hard black shadow */}
      <G transform="translate(4, 4)">
        <Circle cx="50" cy="46" r="38" fill={brandColors.black} />
        <Path d="M 50 46 L 76 86 L 60 86 L 44 56 Z" fill={brandColors.black} />
        <Rect x="18" y="16" width="16" height="70" rx="4" fill={brandColors.black} />
      </G>

      {/* Outer reel circle and R kickstand */}
      <Circle cx="50" cy="46" r="38" fill={brandColors.yellow} stroke={brandColors.black} strokeWidth="3" />
      <Path
        d="M 48 46 L 74 86 L 58 86 L 38 52 Z"
        fill={brandColors.yellow}
        stroke={brandColors.black}
        strokeWidth="3"
        strokeLinejoin="round"
      />

      {/* Film strip vertical spine */}
      <Rect
        x="18"
        y="16"
        width="16"
        height="70"
        rx="4"
        fill={brandColors.charcoal}
        stroke={brandColors.black}
        strokeWidth="3"
      />

      {/* Film strip sprocket perforations */}
      <Rect x="22" y="24" width="8" height="6" rx="1.5" fill={brandColors.white} stroke={brandColors.black} strokeWidth="1.5" />
      <Rect x="22" y="38" width="8" height="6" rx="1.5" fill={brandColors.white} stroke={brandColors.black} strokeWidth="1.5" />
      <Rect x="22" y="52" width="8" height="6" rx="1.5" fill={brandColors.white} stroke={brandColors.black} strokeWidth="1.5" />
      <Rect x="22" y="66" width="8" height="6" rx="1.5" fill={brandColors.white} stroke={brandColors.black} strokeWidth="1.5" />

      {/* Reel cutouts */}
      <Circle cx="50" cy="24" r="7" fill={brandColors.charcoal} stroke={brandColors.black} strokeWidth="2" />
      <Circle cx="70" cy="40" r="7" fill={brandColors.sage} stroke={brandColors.black} strokeWidth="2" />
      <Circle cx="62" cy="62" r="7" fill={brandColors.white} stroke={brandColors.black} strokeWidth="2" />

      {/* Central spindle hub */}
      <Circle cx="50" cy="46" r="13" fill={brandColors.charcoal} stroke={brandColors.black} strokeWidth="3" />
      <Circle cx="50" cy="46" r="6" fill={brandColors.yellow} stroke={brandColors.black} strokeWidth="2" />
      <Circle cx="50" cy="46" r="2.5" fill={brandColors.black} />
    </Svg>
  );

  if (!tappable) {
    return <View style={{ width: size, height: size }}>{markSvg}</View>;
  }

  return (
    <Pressable
      onPress={() => haptic('tap')}
      hitSlop={12}
      accessibilityRole="image"
      accessibilityLabel="ReelNest logo"
    >
      <View style={{ width: size, height: size }}>{markSvg}</View>
    </Pressable>
  );
}
