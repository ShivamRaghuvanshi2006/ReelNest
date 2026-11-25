import React from 'react';
import { ReelNestMark } from '../brand/ReelNestMark';

export interface BrandMarkProps {
  /** Rendered height in dp; width equals height for the square emblem. */
  height?: number;
}

/** The onboarding hero: the ReelNest emblem, tappable for a small haptic. */
export function BrandMark({ height = 96 }: BrandMarkProps) {
  return <ReelNestMark height={height} tappable />;
}
