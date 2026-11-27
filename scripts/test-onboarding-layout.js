#!/usr/bin/env node
/**
 * Onboarding layout contract.
 *
 * StepLayout centres its main column (alignItems: 'center'). A child that only asks to stretch
 * (alignSelf: 'stretch', like the mobile-data options or the folder row) sits inside an animated
 * Chunk wrapper; if that wrapper has no width of its own it shrinks to its content, the rows inside
 * collapse to a sliver and wrap one letter per line, and the step renders blank (found on a device,
 * 0.12, step 5 "Download on mobile data?").
 *
 * Checks: Chunk forwards a style to its Animated.View, and the `extra` Chunk is stretched to the
 * column's full width.
 */
const fs = require('fs');
const path = require('path');

const file = path.join(__dirname, '..', 'components', 'onboarding', 'StepLayout.tsx');
const src = fs.readFileSync(file, 'utf8');
let failed = 0;
function check(name, ok) {
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}`);
  if (!ok) failed++;
}

const chunkStart = src.indexOf('function Chunk(');
const chunkEnd = src.indexOf('\nexport function StepLayout', chunkStart);
const chunkFn = chunkStart >= 0 && chunkEnd >= 0 ? src.slice(chunkStart, chunkEnd + 2) : null;
const chunkArgs = chunkFn ? chunkFn.slice(chunkFn.indexOf('('), chunkFn.indexOf(')') + 1) : '';
check('Chunk is defined', !!chunkFn);
check('Chunk accepts a style prop', /\bstyle\b/.test(chunkArgs));
check(
  'Chunk passes that style to its Animated.View',
  !!chunkFn && /<Animated\.View[\s\S]*?style=\{\[[^\]]*\bstyle\b/.test(chunkFn),
);

const extraChunk = src.match(/\{extra \? <Chunk([^>]*)>\{extra\}<\/Chunk> : null\}/);
check('the extra slot is wrapped in a Chunk', !!extraChunk);
const extraStyle = extraChunk && extraChunk[1].match(/style=\{(?:styles\.)?(\w+)\}/);
const stretchKey = extraStyle && extraStyle[1];
check('the extra Chunk gets a style', !!stretchKey);
const stretchRule = stretchKey && new RegExp(`\\b${stretchKey}:\\s*\\{[^}]*alignSelf:\\s*'stretch'`).test(src);
check("that style stretches it to the column width (alignSelf: 'stretch')", !!stretchRule);

if (failed) {
  console.error(`\n${failed} onboarding layout check(s) failed`);
  process.exit(1);
}
console.log('\nOnboarding layout: all checks pass');
