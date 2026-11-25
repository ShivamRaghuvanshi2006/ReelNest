/**
 * ReelNest brand palette. The mark and the generated raster assets use these values, and
 * `scripts/build-reelnest-assets.py` writes the same five colours into the SVGs and PNGs.
 * Screens never use this file directly: UI colour roles live in `constants/theme.ts`.
 */
export const brandColors = {
  /** Primary yellow: the reel, the wordmark highlight and the icon badge. */
  yellow: '#ffe17c',
  /** Deep charcoal: the page, the film spine and dark ink on yellow. */
  charcoal: '#171e19',
  /** Sage: the second spool window. */
  sage: '#b7c6c2',
  white: '#ffffff',
  black: '#000000',
} as const;
