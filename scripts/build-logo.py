# Run: python3 scripts/build-logo.py "$PWD"
# Decorative pixel train used by components/brand/ReelNestMark.tsx: the traced train redrawn on a
# pixel grid (1 unit = 16 px of the 2048 trace). Not the ReelNest logo; see scripts/build-reelnest-assets.py.
import sys, json, re
root = sys.argv[1]
# Nose: fine 1 x 0.75 steps read as a smooth slope; the last steps round off the tip into the base.
nose = "".join(f" H{80+k:g} V{45.75+0.75*k:g}" for k in range(36)) + " V74.5 H114.25 V75.5 H113.5 V76"
# Window: a slanted parallelogram like the original drawing. Both sides step down to the right
# (the left edge leans like a windshield, the right edge follows the nose), the top-left corner is
# rounded off, and the frame along the nose thickens towards the base. 22 rows of 0.75 units.
# Corner insets per row (negative keys count from the bottom row). Rows are 0.375 units, so the
# slanted sides read as smooth edges and each corner rounds over several rows.
SOFT_L = {0: 2.6, 1: 1.7, 2: 1.05, 3: 0.6, 4: 0.25, -1: 1.8, -2: 1.0, -3: 0.45, -4: 0.15}
SOFT_R = {0: 1.8, 1: 1.0, 2: 0.45, 3: 0.15, -1: 2.4, -2: 1.5, -3: 0.85, -4: 0.4, -5: 0.1}
def _window():
    rows, h = 44, 0.375
    top = 49.5
    pts = []
    for j in range(rows):
        y0 = top + h * j
        left = 67 + 0.3 * j + SOFT_L.get(j, SOFT_L.get(j - rows, 0))
        right = 84 + 0.4 * j - SOFT_R.get(j, SOFT_R.get(j - rows, 0))
        pts.append((y0, y0 + h, round(left, 3), round(right, 3)))
    d = f"M{pts[0][2]:g} {pts[0][0]:g}"
    for (y0, y1, l, r) in pts:
        d += f" H{r:g} V{y1:g}"
    for (y0, y1, l, r) in reversed(pts):
        d += f" H{l:g} V{y0:g}"
    return d + " Z"
window = _window()
def _stair_up(rows, y_top, x_right, slope):
    """Walk up a stepped edge (0.75-unit rows) whose right side leans like the window's left edge."""
    d = ""
    for j in reversed(range(rows)):
        d += f" V{y_top + 0.75 * j:g}" + (f" H{x_right + slope * (j - 1):g}" if j else "")
    return d
# Back of the train: three bands that stream into the speed lines. The two cut-ins between them end
# in stepped edges at the window's angle, so every cut reads as one deliberate slant.
CUT_A = (6, 49.5, 52.0)    # rows, top y, right x of the first row  (between band 1 and band 2)
CUT_B = (10, 58.5, 58.0)   # (between band 2 and band 3)
SLOPE = 0.6
def _cut_bottom_right(cut):
    rows, y, x = cut
    return x + SLOPE * (rows - 1), y + 0.75 * rows
a_x, a_y = _cut_bottom_right(CUT_A)
b_x, b_y = _cut_bottom_right(CUT_B)
body = ("M40 45 H79" + nose + " H28 V70.5 H36 V" + f"{b_y:g}" + f" H{b_x:g}" + _stair_up(*CUT_B, SLOPE) +
        " H36 V54" + f" H{a_x:g}" + _stair_up(*CUT_A, SLOPE) + " H40 Z " + window)
# Speed lines: one thickness (1.5), varied lengths, each sitting on a band. (x, y, w)
LINES = [(16, 46.5, 21), (10, 55.5, 23), (18, 67.5, 15), (12, 73.0, 13)]
lines = " ".join(f"M{x:g} {y:g} H{x+w:g} V{y+1.5:g} H{x:g} Z" for (x, y, w) in LINES)

# ---- Dash animation (app + README) -------------------------------------------------------
# One loop of N frames at FPS, so everything stays in step. Every sprite is a rect described per
# frame as [left x, width, opacity] in viewBox units; the group (body + trails) gets [dx, dy].
#  * Trails: each speed line stays pinned to the train as a light-trail with a taper: a solid core,
#    then a half-height tail at half strength. Their length holds steady while cruising (no flicker).
#  * Streaks: every few frames each trail sheds a thin streak off its tip that flies back and fades,
#    so the lines read as streaming rather than stretching.
#  * Dash: once per loop the train dips back for two frames (trails shorten), snaps forward and holds
#    while the trails whip out long, then settles straight back. No overshoot, no vertical bob.
#  * Afterimages: two stepped copies of the band ends smear off the back; they reach out on the dash.
#  * Wind: one streak through each cut-in between the bands, and one over the roof on the dash.
#  * Ground: dashes under the rails sweep the length of the track.
FPS, N = 20, 24
# Dash envelope per frame: -ve = anticipation (the last two frames of the loop), 1 = full stretch.
ENV = [1, 1, 0.8, 0.6, 0.42, 0.27, 0.14, 0.05] + [0] * (N - 10) + [-0.15, -0.3]
SHED_PHASE = [0, 3, 1, 4]         # stagger between the four trails
# Two tunings of the same loop. "full" is drawn for 32 dp and up. "compact" is for the header
# (22 dp, where 1 unit is half a dp): nothing thinner than a speed line, no wind, roof or ground
# sprites (they are under a pixel there), shorter trails that stay inside the header's left margin,
# and a push authored so every step lands on a whole dp.
FULL = dict(push=[3, 3, 2.5, 2, 1.5, 1, 0.5] + [0] * (N - 9) + [-0.5, -1],
            cruise=1.3, stretch=0.9, tail=0.5, thin=0.75, tail_o=0.5,
            shed_every=6, shed_fade=[0.7, 0.5, 0.3, 0.14], shed_step=11, shed_w=9, shed_gap=3, extras=True)
COMPACT = dict(push=[8, 8, 6, 4, 2] + [0] * (N - 7) + [-2, -2],
               cruise=1.15, stretch=0.8, tail=0.4, thin=1.5, tail_o=0.45,
               shed_every=6, shed_fade=[0.6, 0.35, 0.15], shed_step=6, shed_w=6, shed_gap=2, extras=False)
COMPACT_BELOW = 32                # dp: ReelNestMark uses the compact set under this height
q = lambda v: round(v * 2) / 2
def _trail(sprites, line, core, tail, c, tail_o):
    """Core + tail sprites of one speed line. core/tail are lengths per frame; tail_o opacity per frame."""
    x, y, w = line
    anchor, dy = x + w, (1.5 - c["thin"]) / 2
    sprites.append({"y": y, "h": 1.5, "ghost": False, "frames": [[anchor - k, k, 1] for k in core]})
    sprites.append({"y": y + dy, "h": c["thin"], "ghost": True,
                    "frames": [[anchor - k - t, t, o] for k, t, o in zip(core, tail, tail_o)]})
def fx(c):
    sprites = []
    add = lambda y, h, fr: sprites.append({"y": y, "h": h, "ghost": True, "frames": fr})
    for i, line in enumerate(LINES):
        x, y, w = line
        anchor = x + w
        core = [q(w * (c["cruise"] + c["stretch"] * e)) for e in ENV]
        tail = [q(k * c["tail"]) for k in core]
        _trail(sprites, line, core, tail, c, [c["tail_o"]] * N)
        fade, sw = c["shed_fade"], c["shed_w"]
        fr = []
        for k in range(N):
            j = (k + SHED_PHASE[i]) % c["shed_every"]
            if j < len(fade):
                born = (k - j) % N                 # the tip it left from (the loop wraps)
                tip = anchor - core[born] - tail[born]
                fr.append([q(tip - c["shed_gap"] - c["shed_step"] * j - sw), sw, fade[j]])
            else:
                fr.append([anchor - sw, sw, 0])
        add(y + (1.5 - c["thin"]) / 2, c["thin"], fr)
    if c["extras"]:
        # Wind through the two cut-ins: starts inside the cut and is gone in four frames. (y, phase)
        for (y, ph) in [(51.375, 2), (61.875, 6)]:
            fr = []
            for k in range(N):
                j = (k + ph) % 8
                fr.append([q(30 - 20 * j), 16, [0.75, 0.55, 0.32, 0.14][j]] if j < 4 else [30, 16, 0])
            add(y, 0.75, fr)
        # Roof whip: one long streak over the roof as the train snaps forward.
        roof = {0: (52, 26, 0.8), 1: (24, 30, 0.6), 2: (-4, 30, 0.35), 3: (-30, 28, 0.15)}
        add(43.25, 0.75, [list(roof.get(k, (52, 26, 0))) for k in range(N)])
        # Ground dashes under the rails: enter under the nose, leave past the tail. (w, phase)
        ground = [(104, 0.35), (82, 0.7), (60, 0.7), (38, 0.7), (16, 0.45), (-6, 0.2)]
        for (w, ph) in [(12, 0), (7, 3)]:
            add(84.5, 0.75, [[ground[(k + ph) % 6][0], w, ground[(k + ph) % 6][1]] for k in range(N)])
    group = [[c["push"][k], 0] for k in range(N)]
    after = [[[q(-(2.5 + 5 * max(e, 0))), round(0.34 + 0.26 * max(e, 0), 2)] for e in ENV],
             [[q(-(5 + 10 * max(e, 0))), round(0.14 + 0.2 * max(e, 0), 2)] for e in ENV]]
    return {"ms": round(N * 1000 / FPS), "sprites": sprites, "group": group, "after": after}
FX = fx(FULL)
FX_COMPACT = fx(COMPACT)

# ---- Boost (tap) and arrival (cold start): one-shots ---------------------------------------
# Crouch for two frames, launch off to the right, come back in from the left and settle on the still
# logo. How far the train travels depends on the screen, so the renderer supplies it
# (components/brand/markMotion.ts, which must agree on these frame counts); here are the trails and
# afterimages for each frame. The arrival is the boost from BOOST_ENTER_AT on.
#          crouch      launch (off to the right)   re-entry from the left, last frame = still logo
B_LEN  = [0.8, 0.6,   2.2, 2.4, 2.4, 2.4, 2.4,    2.4, 2.2, 1.8, 1.4, 1.15, 1.0]
B_SMEAR = [0, 0,      1, 1, 1, 1, 1,              1, 0.8, 0.5, 0.25, 0.1, 0]
BOOST_ENTER_AT = 7
def boost(c):
    sprites, n = [], len(B_LEN)
    for line in LINES:
        w = line[2]
        core = [q(w * m) for m in B_LEN[:-1]] + [w]
        tail = [q(k * c["tail"]) for k in core]
        _trail(sprites, line, core, tail, c, [c["tail_o"]] * (n - 1) + [0])
    after = [[[q(-(2.5 + 5 * e)), round(0.6 * e, 2)] for e in B_SMEAR],
             [[q(-(5 + 10 * e)), round(0.34 * e, 2)] for e in B_SMEAR]]
    return {"ms": round(n * 1000 / FPS), "sprites": sprites, "group": [[0, 0]] * n, "after": after}
BOOST = boost(FULL)
BOOST_COMPACT = boost(COMPACT)

# Afterimage shape: just the back end of each band (GHOST_W deep), so the smear is a clean stepped
# fade off the back and never shows inside the cut-ins or through the window.
GHOST_W = 8
ghost = " ".join(f"M{x:g} {y0:g} H{x + GHOST_W:g} V{y1:g} H{x:g} Z" for (x, y0, y1) in
                 [(40, 45, CUT_A[1]), (36, 54, CUT_B[1]), (36, b_y, 70.5), (28, 70.5, 76)])
dashes = ""
rails = ("M20 79.5 H29 V80.75 H20 Z "
         "M34 79.5 H67 V80.75 H68.5 V82 H70 V83.25 H40.5 V82 H36 V80.75 H34 Z "
         "M71 79.5 H112.5 V80.75 H111 V82 H108.5 V83.25 H74.5 V82 H72.5 V80.75 H71 Z")
LIME, CYAN, VOID = "#ffe17c", "#00E5FF", "#171e19"
VB = (10, 42, 107, 44)
# This script only generates the decorative pixel-train illustration used by ReelNestMark.
# ReelNest brand marks, launcher icons, splash and the README header come from
# scripts/build-reelnest-assets.py, which this script must never overwrite.
open(f"{root}/components/brand/markPaths.ts", "w").write(
    "// Generated by scripts/build-logo.py: decorative pixel-train art, not the app logo. Do not edit by hand.\n"
    f"export const MARK_VIEWBOX = '{' '.join(map(str, VB))}';\n"
    f"export const MARK_RATIO = {VB[2]} / {VB[3]};\n"
    f"export const MARK_BODY = '{body}';\n"
    f"export const MARK_LINES = '{lines}';\n"
    f"export const MARK_RAILS = '{rails}';\n"
    "/** ReelNest yellow (#ffe17c) and the downloading cyan, kept here for the generated pixel train art. */\n"
    f"export const MARK_LIME = '{LIME}';\nexport const MARK_CYAN = '{CYAN}';\n"
    "/** Dash loop: frames per element. Sprites are [left x, width, opacity]; group is [dx, dy]; afterimages [dx, opacity]. Ghost sprites show only while dashing. */\n"
    f"export const MARK_GHOST = '{ghost}';\n"
    "export type MarkFx = { ms: number; sprites: { y: number; h: number; ghost: boolean; frames: [number, number, number][] }[]; group: [number, number][]; after: [number, number][][] };\n"
    f"export const MARK_FX: MarkFx = {json.dumps(FX, separators=(',', ':'))};\n"
    "/** The same loop tuned for small sizes: use it under MARK_COMPACT_BELOW dp of height. */\n"
    f"export const MARK_COMPACT_BELOW = {COMPACT_BELOW};\n"
    f"export const MARK_FX_COMPACT: MarkFx = {json.dumps(FX_COMPACT, separators=(',', ':'))};\n"
    "/** Boost one-shot (crouch, launch right, re-enter from the left, settle on the still logo). The renderer supplies the travel; the arrival plays it from MARK_BOOST_ENTER_AT. */\n"
    f"export const MARK_BOOST_ENTER_AT = {BOOST_ENTER_AT};\n"
    f"export const MARK_BOOST: MarkFx = {json.dumps(BOOST, separators=(',', ':'))};\n"
    f"export const MARK_BOOST_COMPACT: MarkFx = {json.dumps(BOOST_COMPACT, separators=(',', ':'))};\n")
print("ok")

