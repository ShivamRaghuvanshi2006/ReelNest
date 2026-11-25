# ReelNest rebrand report

Date: 2026-11-25 · Version: 0.33 (versionCode 33) · Branch: `main`

The previous product name has been removed from the repository: user-visible copy, identifiers,
file names, directories, package names, native symbols, build metadata, workflows, tests, docs and
the marketing site. The name now appears nowhere in tracked content.

## 1. Final state

| Item | Value |
|---|---|
| App name | `ReelNest` |
| Expo slug / URL scheme | `reelnest` / `reelnest://` |
| Android package | `com.reelnest` |
| iOS bundle identifier | `com.reelnest.client` |
| Expo module | `reelnest-engine` (`modules/reelnest-engine`) |
| Kotlin namespace | `com.reelnest.engine` |
| Rust crate / cdylib | `reelnest-core` / `libreelnest_core.so` |
| Release secrets | `REELNEST_KEYSTORE_B64`, `REELNEST_KEYSTORE_PASSWORD`, `REELNEST_KEY_ALIAS`, `REELNEST_KEY_PASSWORD` |
| Repository | `https://github.com/ShivamRaghuvanshi2006/ReelNest` |
| Site | `https://harshdayal.dev/reelnest` |

## 2. What was renamed

**Content.** 539 text files had case-sensitive replacements: `MAGLEV` → `REELNEST`,
`Maglev` → `ReelNest`, `maglev` → `reelnest`. A final case-insensitive scan over every tracked text
file (excluding `node_modules/`, `.git/`, `.expo/`) returns **zero** matches.

**Paths.** 303 paths contained the old name and were renamed. Git records 293 as renames; the
remaining 11 deletions and 8 additions are intentional splits:

- `components/brand/MaglevMark.tsx` → `components/brand/PixelTrain.tsx`. This file is the
  decorative pixel-train illustration, not the logo, so it no longer shares a name with the real
  emblem. Its exports are now `PixelTrain` / `PixelTrainProps`. `components/brand/ReelNestMark.tsx`
  is the official logo and stays separate.
- `modules/maglev-engine/` → `modules/reelnest-engine/`, including `com/maglev/engine/**` →
  `com/reelnest/engine/**` and every `Maglev*.kt` class: `ReelNestEngineModule`,
  `ReelNestBrowserView`, `ReelNestTorrentService`, `ReelNestTileService`,
  `ReelNestQuickShareModule`, `ReelNestFileProvider`, `ReelNestWatchModule`.
- `native/maglev-core/` → `native/reelnest-core/` (crate `reelnest-core`, library
  `reelnest_core`, JNI exports, vendor tree).
- `distribution/fdroid/com.maglev.yml` → `distribution/fdroid/com.reelnest.yml`.
- Android resources: `ic_tile_maglev.xml` → `ic_tile_reelnest.xml`,
  `maglev_mark.xml` → `reelnest_mark.xml`, style `ReelNestQuickShare`.
- `assets/brand/maglev-*.svg` → `reelnest-*.svg`; four byte-identical duplicate SVGs were deleted
  so only one copy of each asset remains.
- `site/assets/qr-maglev.svg` → `site/assets/qr-reelnest.svg`.
- `scripts/generate-icons.js` was deleted: it was stale and still wrote old-brand assets.

**Metadata and delivery.**

- `app.json`: name, slug, scheme, Android package, iOS bundle, homepage.
- `package.json` and `package-lock.json`: root name and the `reelnest-engine` workspace dependency.
- F-Droid recipe, fastlane title/short/full descriptions and changelogs, release-notes generator,
  blocklist/miner headers and generators, device and performance scripts, Maestro flows
  (`reelnest://` scheme; `appId` stays `com.reelnest`).
- GitHub workflows and plugins: `REELNEST_*` secrets, `ReelNest-*` artifacts, APK names.
- Docs: `AGENTS.md`, `DESIGN.md`, `LEDGER.md`, `docs/**`, `distribution/**`, `README.md`.
- Website: `site/build/*` constants plus the regenerated HTML for the home page, comparison page,
  alternative pages, privacy page, `llms.txt`, `sitemap.xml` and `robots.txt`. Repo, Obtainium and
  download links now point at `ShivamRaghuvanshi2006/ReelNest`.

**User-visible copy.** Header wordmark, onboarding, home, add-torrent and link flows, torrent
detail, settings (including About and licenses), error/empty states, notification channel and
action labels, the "Download with ReelNest" text-selection action, quick-share sheet, home-screen
tile label and the About version block.

## 3. Assets

- `assets/brand/reelnest-mark.svg`, `reelnest-icon.svg`, `reelnest-wordmark.svg`,
  `readme-header.svg`, `reelnest-logo-source.svg` use the official palette: yellow `#ffe17c`,
  charcoal `#171e19`, sage `#b7c6c2`, white, black.
- `constants/brand.ts` is the single source for those five colours; the mark reads it and
  `scripts/build-reelnest-assets.py` writes the same values into the rasters.
- `components/brand/ReelNestMark.tsx` renders the official emblem (the source of `useMarkInk`
  and the mark path data). `components/brand/PixelTrain.tsx` keeps the animated illustration used
  by onboarding and the stats screen.
- Launcher icon, adaptive icon layers, splash, favicon and social card were regenerated from the
  same script; `app.json` points at the regenerated files.

## 4. Verification performed

All commands were run locally on Windows against the real working tree.

| Check | Command | Result |
|---|---|---|
| TypeScript | `npx tsc --noEmit` | Pass, no diagnostics |
| Expo public config | `npx expo config --type public` | Resolves; name/slug/scheme/package correct |
| Expo prebuild config | `npx expo config --type prebuild` | Resolves; all config plugins load |
| Dependency graph | `npm install --ignore-scripts` | Workspace `reelnest-engine` links, 592 packages |
| Test suite | all 160 scripts from `package.json` `test`, run one by one | 160/160 pass |
| Contract tests | `node scripts/test-p3-reality-contracts.js` | 25 pass, 1 pre-existing skip, 0 P0 failures |
| Site build | `node site/build/build-site.mjs` | v0.33, 37 FAQ items, 10 apps × 47 compare rows |
| Name scan | case-insensitive search for the old name | 0 matches outside `node_modules/`, `.git/`, `.expo/` |
| Path scan | recursive filename search | 0 paths with the old name |

Rebrand-related test fixes were limited to assertions that hard-coded the old name or repo URL, plus
Windows-only ESM/path bugs found while running the suite (`pathToFileURL` instead of raw absolute
paths, `[\\/]service[\\/]` path matching). No product behaviour was weakened to make a test pass.

## 5. Not verified, and known gaps

These need a machine with the Android SDK/NDK, Gradle and Rust, or owner action in GitHub.

1. **No APK/AAB or native build was produced.** This environment has no Android SDK, Gradle, NDK
   or Rust toolchain, so Kotlin/Rust were not compiled and no device or emulator run happened.
   CI must prove the renamed JNI symbols, `com.reelnest` package and 16 KB page alignment.
2. **GitHub repository secrets are still named `MAGLEV_*`.** Workflows now read `REELNEST_*`. Until
   the owner renames the four secrets, `plugins/withReleaseSigning.js` falls back to debug signing.
3. **No new release key or certificate.** The site APK fingerprint and F-Droid
   `AllowedAPKSigningKeys` still reference the old certificate, and `com.reelnest` is a new
   application ID, so existing installs cannot update in place — they need an uninstall/reinstall.
4. **Store listing screenshots and any alternate launcher icons were not recaptured**; they need a
   device running the rebuilt app.
5. **Site hosting route.** The canonical URL changed from `/maglev` to `/reelnest`. The HTML, asset
   prefix, sitemap and JSON-LD all use the new path, but `harshdayal.dev` must serve that route
   (Next.js rewrite) before the deployed site resolves.
6. **Typography differs from the brief.** The brief asked for Cabinet Grotesk headings and Satoshi
   body. The app ships Cabinet Grotesk headings with Inter body/telemetry; Satoshi files exist but
   are not wired into `constants/fontStyles.ts`. Changing it would alter every screen and the
   `test-font-style.js` contract, so it was left as-is.
7. **Surface styling differs from the brief.** The brief asked for 2 px black borders and 4/8 px hard
   shadows. The existing design system uses 1 px hairline borders and the neo-brutalist emblem; it
   was kept to avoid a full visual rewrite. A 2 px/shadow pass would be its own change with design
   contract updates.
8. **Historical material.** `distribution/apk-scan.md` is kept as evidence of a specific old binary
   and now describes it without using the retired product name; it does not describe the current
   build. Old release tags and published APKs on GitHub are immutable and still carry the old
   package name.

## 6. Follow-up for the owner

1. Rename the four GitHub secrets to `REELNEST_*` and add the new keystore.
2. Push this branch and let CI build the universal, arm64-v8a, armeabi-v7a and x86_64 APKs; confirm
   the APKs are not debug-signed on `main`.
3. Install on a device, walk onboarding → add torrent → download → play, then recapture store
   screenshots.
4. Publish the `/reelnest` route on `harshdayal.dev` and update the store listing and F-Droid
   metadata with the new certificate.
5. Optionally schedule the typography and 2 px-border passes as separate, contract-backed changes.
