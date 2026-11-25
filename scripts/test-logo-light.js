#!/usr/bin/env node
// Brand marks: the ReelNest emblem uses the official palette from constants/brand.ts and no hex literals;
// the wordmark reads theme roles, so it stays legible on light pages.
process.removeAllListeners('warning');
const fs = require('fs');
const path = require('path');
const read = (p) => fs.readFileSync(path.join(__dirname, '..', p), 'utf8');
let failed = 0;
const check = (n, c) => { if (c) console.log(`  ok   ${n}`); else { failed++; console.error(`  FAIL ${n}`); } };

const strip = (s) => s.replace(/\/\*[\s\S]*?\*\//g, '').replace(/^\s*\/\/.*$/gm, '');
const mark = strip(read('components/brand/ReelNestMark.tsx'));
const word = strip(read('components/settings/Wordmark.tsx'));
const brand = read('constants/brand.ts');

check('ReelNestMark uses the shared brand palette', /brandColors/.test(mark) && !/#[0-9a-fA-F]{3,8}\b/.test(mark));
check('ReelNestMark has no theme-dependent recolouring', !/useTheme\(\)/.test(mark));
check('brand palette is the official five colours', /yellow: '#ffe17c'/.test(brand) && /charcoal: '#171e19'/.test(brand) && /sage: '#b7c6c2'/.test(brand));
check('Wordmark reads the theme roles', /useTheme\(\)/.test(word) && /\bc\.text\b/.test(word) && /\bc\.accentText\b/.test(word));
check('Wordmark has no hex literals', !/#[0-9a-fA-F]{3,8}\b/.test(word));

const lum = (h) => { const c = [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16) / 255).map((v) => (v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4)); return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]; };
const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((m, n) => n - m); return (x + 0.05) / (y + 0.05); };
(async () => {
  const { palettes, buildColors } = await import('../constants/theme.ts');
  const l = palettes.light;
  const light = buildColors('light', 'yellow');
  check(`light wordmark text contrast >= 4.5 (${ratio(l.text, l.bg).toFixed(1)})`, ratio(l.text, l.bg) >= 4.5);
  check(`light NEST accent contrast >= 4.5 (${ratio(light.accentText, l.bg).toFixed(1)})`, ratio(light.accentText, l.bg) >= 4.5);
  check(`mark black outline contrast >= 3 on the light page (${ratio('#000000', l.bg).toFixed(1)})`, ratio('#000000', l.bg) >= 3);
  process.exit(failed ? 1 : 0);
})();
