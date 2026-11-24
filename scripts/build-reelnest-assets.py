#!/usr/bin/env python3
"""
ReelNest Brand Asset Generator
Generates clean SVG vectors and pixel-perfect raster assets for ReelNest.
Colors:
  Primary Yellow: #ffe17c
  Deep Charcoal:  #171e19
  Sage:           #b7c6c2
  White:          #ffffff
  Black:          #000000
"""

import math
import os
import struct
import zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_BRAND = os.path.join(ROOT, "assets", "brand")
ASSETS = os.path.join(ROOT, "assets")
SITE_ASSETS = os.path.join(ROOT, "site", "assets")
SITE = os.path.join(ROOT, "site")

os.makedirs(ASSETS_BRAND, exist_ok=True)
os.makedirs(SITE_ASSETS, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. SVGs
# ---------------------------------------------------------------------------

# Standalone Mark (100x100)
# A bold Neo-Brutalist Film Reel + 'R' Emblem with hard shadow and 2px black borders
REELNEST_MARK_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100%" height="100%">
  <!-- Neo-Brutalist 4px Hard Shadow -->
  <g transform="translate(4, 4)">
    <circle cx="50" cy="46" r="38" fill="#000000" />
    <path d="M 50 46 L 76 86 L 60 86 L 44 56 Z" fill="#000000" />
    <rect x="18" y="16" width="16" height="70" rx="4" fill="#000000" />
  </g>

  <!-- Film Reel Outer Rim & Stem Fills -->
  <!-- Outer Reel Circle -->
  <circle cx="50" cy="46" r="38" fill="#ffe17c" stroke="#000000" stroke-width="3" />
  
  <!-- "R" Leg Kickstand -->
  <path d="M 48 46 L 74 86 L 58 86 L 38 52 Z" fill="#ffe17c" stroke="#000000" stroke-width="3" stroke-linejoin="round" />

  <!-- "R" Vertical Spine / Film Strip -->
  <rect x="18" y="16" width="16" height="70" rx="4" fill="#171e19" stroke="#000000" stroke-width="3" />

  <!-- Film Strip Sprocket Holes / Perforations -->
  <rect x="22" y="24" width="8" height="6" rx="1.5" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
  <rect x="22" y="38" width="8" height="6" rx="1.5" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
  <rect x="22" y="52" width="8" height="6" rx="1.5" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
  <rect x="22" y="66" width="8" height="6" rx="1.5" fill="#ffffff" stroke="#000000" stroke-width="1.5" />

  <!-- Film Reel Spool Cutouts (Windows) -->
  <circle cx="50" cy="24" r="7" fill="#171e19" stroke="#000000" stroke-width="2" />
  <circle cx="70" cy="40" r="7" fill="#b7c6c2" stroke="#000000" stroke-width="2" />
  <circle cx="62" cy="62" r="7" fill="#ffffff" stroke="#000000" stroke-width="2" />

  <!-- Central Reel Core & Hub Spindle -->
  <circle cx="50" cy="46" r="13" fill="#171e19" stroke="#000000" stroke-width="3" />
  <circle cx="50" cy="46" r="6" fill="#ffe17c" stroke="#000000" stroke-width="2" />
  <circle cx="50" cy="46" r="2.5" fill="#000000" />
</svg>
"""

# Monochrome Mark (for Android 13+ themed icon)
REELNEST_MARK_MONO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100%" height="100%">
  <circle cx="50" cy="46" r="38" fill="#ffffff" />
  <path d="M 48 46 L 74 86 L 58 86 L 38 52 Z" fill="#ffffff" />
  <rect x="18" y="16" width="16" height="70" rx="4" fill="#ffffff" />
  
  <rect x="22" y="24" width="8" height="6" rx="1.5" fill="#000000" />
  <rect x="22" y="38" width="8" height="6" rx="1.5" fill="#000000" />
  <rect x="22" y="52" width="8" height="6" rx="1.5" fill="#000000" />
  <rect x="22" y="66" width="8" height="6" rx="1.5" fill="#000000" />

  <circle cx="50" cy="24" r="7" fill="#000000" />
  <circle cx="70" cy="40" r="7" fill="#000000" />
  <circle cx="62" cy="62" r="7" fill="#000000" />

  <circle cx="50" cy="46" r="13" fill="#000000" />
  <circle cx="50" cy="46" r="6" fill="#ffffff" />
  <circle cx="50" cy="46" r="2.5" fill="#000000" />
</svg>
"""

# App Icon Tile SVG (1024x1024)
REELNEST_ICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="100%" height="100%">
  <!-- Background: Deep Charcoal -->
  <rect width="1024" height="1024" fill="#171e19" />
  
  <!-- Subtle Radial Dot Matrix in Yellow (32x32 grid) -->
  <defs>
    <pattern id="dot-grid" width="32" height="32" patternUnits="userSpaceOnUse">
      <circle cx="16" cy="16" r="1.5" fill="#ffe17c" opacity="0.12" />
    </pattern>
  </defs>
  <rect width="1024" height="1024" fill="url(#dot-grid)" />

  <!-- Neo-Brutalist Badge Container (with 16px hard black shadow) -->
  <g transform="translate(192, 192)">
    <!-- Hard Shadow -->
    <rect x="16" y="16" width="640" height="640" rx="36" fill="#000000" />
    <!-- White Card with 4px Black Border -->
    <rect x="0" y="0" width="640" height="640" rx="36" fill="#ffe17c" stroke="#000000" stroke-width="12" />
    
    <!-- Centered Emblem (scaled 5.2x) -->
    <g transform="translate(60, 60) scale(5.2)">
      <!-- Hard Shadow for Emblem Inside -->
      <g transform="translate(3, 3)">
        <circle cx="50" cy="46" r="38" fill="#000000" opacity="0.4" />
        <path d="M 50 46 L 76 86 L 60 86 L 44 56 Z" fill="#000000" opacity="0.4" />
        <rect x="18" y="16" width="16" height="70" rx="4" fill="#000000" opacity="0.4" />
      </g>

      <!-- Outer Reel Circle -->
      <circle cx="50" cy="46" r="38" fill="#ffffff" stroke="#000000" stroke-width="3" />
      
      <!-- "R" Leg Kickstand -->
      <path d="M 48 46 L 74 86 L 58 86 L 38 52 Z" fill="#ffffff" stroke="#000000" stroke-width="3" stroke-linejoin="round" />

      <!-- "R" Vertical Spine / Film Strip -->
      <rect x="18" y="16" width="16" height="70" rx="4" fill="#171e19" stroke="#000000" stroke-width="3" />

      <!-- Film Strip Sprockets -->
      <rect x="22" y="24" width="8" height="6" rx="1.5" fill="#ffe17c" stroke="#000000" stroke-width="1.5" />
      <rect x="22" y="38" width="8" height="6" rx="1.5" fill="#ffe17c" stroke="#000000" stroke-width="1.5" />
      <rect x="22" y="52" width="8" height="6" rx="1.5" fill="#ffe17c" stroke="#000000" stroke-width="1.5" />
      <rect x="22" y="66" width="8" height="6" rx="1.5" fill="#ffe17c" stroke="#000000" stroke-width="1.5" />

      <!-- Spool Cutouts -->
      <circle cx="50" cy="24" r="7" fill="#171e19" stroke="#000000" stroke-width="2" />
      <circle cx="70" cy="40" r="7" fill="#b7c6c2" stroke="#000000" stroke-width="2" />
      <circle cx="62" cy="62" r="7" fill="#ffe17c" stroke="#000000" stroke-width="2" />

      <!-- Core Hub -->
      <circle cx="50" cy="46" r="13" fill="#171e19" stroke="#000000" stroke-width="3" />
      <circle cx="50" cy="46" r="6" fill="#ffe17c" stroke="#000000" stroke-width="2" />
      <circle cx="50" cy="46" r="2.5" fill="#000000" />
    </g>
  </g>
</svg>
"""

# Typographic Wordmark SVG
REELNEST_WORDMARK_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 80" width="100%" height="100%">
  <!-- Mini Mark -->
  <g transform="translate(6, 6) scale(0.68)">
    <g transform="translate(4, 4)">
      <circle cx="50" cy="46" r="38" fill="#000000" />
      <path d="M 50 46 L 76 86 L 60 86 L 44 56 Z" fill="#000000" />
      <rect x="18" y="16" width="16" height="70" rx="4" fill="#000000" />
    </g>
    <circle cx="50" cy="46" r="38" fill="#ffe17c" stroke="#000000" stroke-width="3.5" />
    <path d="M 48 46 L 74 86 L 58 86 L 38 52 Z" fill="#ffe17c" stroke="#000000" stroke-width="3.5" />
    <rect x="18" y="16" width="16" height="70" rx="4" fill="#171e19" stroke="#000000" stroke-width="3.5" />
    <rect x="22" y="24" width="8" height="6" rx="1.5" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
    <rect x="22" y="38" width="8" height="6" rx="1.5" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
    <rect x="22" y="52" width="8" height="6" rx="1.5" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
    <rect x="22" y="66" width="8" height="6" rx="1.5" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
    <circle cx="50" cy="24" r="7" fill="#171e19" stroke="#000000" stroke-width="2" />
    <circle cx="70" cy="40" r="7" fill="#b7c6c2" stroke="#000000" stroke-width="2" />
    <circle cx="62" cy="62" r="7" fill="#ffffff" stroke="#000000" stroke-width="2" />
    <circle cx="50" cy="46" r="13" fill="#171e19" stroke="#000000" stroke-width="3.5" />
    <circle cx="50" cy="46" r="6" fill="#ffe17c" stroke="#000000" stroke-width="2" />
    <circle cx="50" cy="46" r="2.5" fill="#000000" />
  </g>

  <!-- Wordmark Text -->
  <text x="86" y="54" font-family="'Cabinet Grotesk', -apple-system, sans-serif" font-weight="900" font-size="44" letter-spacing="-1" fill="#171e19">REEL<tspan fill="#ffe17c" stroke="#171e19" stroke-width="2">NEST</tspan></text>
</svg>
"""

# Write SVGs
for p in [
    os.path.join(ASSETS_BRAND, "reelnest-mark.svg"),
    os.path.join(ASSETS_BRAND, "maglev-mark.svg"),
    os.path.join(SITE_ASSETS, "mark.svg"),
    os.path.join(SITE, "favicon.svg")
]:
    with open(p, "w", encoding="utf-8") as f:
        f.write(REELNEST_MARK_SVG)

for p in [
    os.path.join(ASSETS_BRAND, "reelnest-mark-mono.svg"),
    os.path.join(ASSETS_BRAND, "maglev-mark-mono.svg")
]:
    with open(p, "w", encoding="utf-8") as f:
        f.write(REELNEST_MARK_MONO_SVG)

for p in [
    os.path.join(ASSETS_BRAND, "reelnest-icon.svg"),
    os.path.join(ASSETS_BRAND, "maglev-icon.svg")
]:
    with open(p, "w", encoding="utf-8") as f:
        f.write(REELNEST_ICON_SVG)

for p in [
    os.path.join(ASSETS_BRAND, "reelnest-wordmark.svg"),
    os.path.join(ASSETS_BRAND, "maglev-wordmark.svg"),
    os.path.join(SITE_ASSETS, "wordmark.svg")
]:
    with open(p, "w", encoding="utf-8") as f:
        f.write(REELNEST_WORDMARK_SVG)

print("SVGs created successfully.")

# ---------------------------------------------------------------------------
# 2. Pure Python PNG Renderer
# ---------------------------------------------------------------------------

def write_png(filename, width, height, rgba_buffer):
    raw = bytearray()
    row_len = width * 4
    for y in range(height):
        raw.append(0)  # filter type 0 (None)
        start = y * row_len
        raw.extend(rgba_buffer[start : start + row_len])
    compressed = zlib.compress(bytes(raw), 9)

    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)

    header = b'\x89PNG\r\n\x1a\n'
    ihdr = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    with open(filename, 'wb') as f:
        f.write(header)
        f.write(chunk(b'IHDR', ihdr))
        f.write(chunk(b'IDAT', compressed))
        f.write(chunk(b'IEND', b''))

# Raster drawing primitives
def blend_pixel(buf, width, height, x, y, r, g, b, a=255):
    if 0 <= x < width and 0 <= y < height:
        idx = (y * width + x) * 4
        if a >= 255:
            buf[idx] = r
            buf[idx+1] = g
            buf[idx+2] = b
            buf[idx+3] = 255
        elif a > 0:
            bg_a = buf[idx+3] / 255.0
            fg_a = a / 255.0
            out_a = fg_a + bg_a * (1.0 - fg_a)
            if out_a > 0:
                buf[idx] = int((r * fg_a + buf[idx] * bg_a * (1.0 - fg_a)) / out_a)
                buf[idx+1] = int((g * fg_a + buf[idx+1] * bg_a * (1.0 - fg_a)) / out_a)
                buf[idx+2] = int((b * fg_a + buf[idx+2] * bg_a * (1.0 - fg_a)) / out_a)
                buf[idx+3] = int(out_a * 255)

def fill_rect(buf, width, height, rx, ry, rw, rh, color):
    r, g, b, a = color
    x0, y0 = max(0, int(rx)), max(0, int(ry))
    x1, y1 = min(width, int(rx + rw)), min(height, int(ry + rh))
    for y in range(y0, y1):
        for x in range(x0, x1):
            blend_pixel(buf, width, height, x, y, r, g, b, a)

def fill_circle(buf, width, height, cx, cy, radius, color):
    r, g, b, a = color
    r2 = radius * radius
    x0, y0 = max(0, int(cx - radius - 1)), max(0, int(cy - radius - 1))
    x1, y1 = min(width, int(cx + radius + 1)), min(height, int(cy + radius + 1))
    for y in range(y0, y1):
        for x in range(x0, x1):
            d2 = (x - cx) ** 2 + (y - cy) ** 2
            if d2 <= r2:
                # anti-alias edge
                dist = math.sqrt(d2)
                alpha_factor = 1.0
                if dist > radius - 1.0:
                    alpha_factor = max(0.0, radius - dist)
                blend_pixel(buf, width, height, x, y, r, g, b, int(a * alpha_factor))

def fill_ring(buf, width, height, cx, cy, r_inner, r_outer, color):
    r, g, b, a = color
    x0, y0 = max(0, int(cx - r_outer - 1)), max(0, int(cy - r_outer - 1))
    x1, y1 = min(width, int(cx + r_outer + 1)), min(height, int(cy + r_outer + 1))
    for y in range(y0, y1):
        for x in range(x0, x1):
            d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
            if r_inner <= d <= r_outer:
                alpha_factor = 1.0
                if d < r_inner + 1.0:
                    alpha_factor = max(0.0, d - r_inner)
                elif d > r_outer - 1.0:
                    alpha_factor = max(0.0, r_outer - d)
                blend_pixel(buf, width, height, x, y, r, g, b, int(a * alpha_factor))

def fill_polygon(buf, width, height, points, color):
    r, g, b, a = color
    min_x = max(0, int(min(p[0] for p in points)))
    max_x = min(width, int(max(p[0] for p in points) + 1))
    min_y = max(0, int(min(p[1] for p in points)))
    max_y = min(height, int(max(p[1] for p in points) + 1))
    n = len(points)
    for y in range(min_y, max_y):
        py = y + 0.5
        nodes = []
        j = n - 1
        for i in range(n):
            pi_x, pi_y = points[i]
            pj_x, pj_y = points[j]
            if (pi_y < py and pj_y >= py) or (pj_y < py and pi_y >= py):
                nodes.append(pi_x + (py - pi_y) / (pj_y - pi_y) * (pj_x - pi_x))
            j = i
        nodes.sort()
        for k in range(0, len(nodes), 2):
            if k + 1 < len(nodes):
                x_start = max(min_x, int(nodes[k]))
                x_end = min(max_x, int(nodes[k+1] + 1))
                for x in range(x_start, x_end):
                    blend_pixel(buf, width, height, x, y, r, g, b, a)

def draw_reelnest_emblem(buf, width, height, origin_x, origin_y, scale, mono=False):
    # Palette
    YELLOW = (255, 255, 255, 255) if mono else (255, 225, 124, 255)
    CHARCOAL = (0, 0, 0, 255) if mono else (23, 30, 25, 255)
    SAGE = (200, 200, 200, 255) if mono else (183, 198, 194, 255)
    WHITE = (255, 255, 255, 255)
    BLACK = (0, 0, 0, 255)

    def s(val):
        return val * scale
    
    # Coordinates mapped from 100x100 viewBox
    def pt(vx, vy):
        return (origin_x + s(vx), origin_y + s(vy))

    # 1. Hard Shadow if not mono
    if not mono:
        sh_offset = s(4)
        sh_col = (0, 0, 0, 255)
        fill_circle(buf, width, height, origin_x + sh_offset + s(50), origin_y + sh_offset + s(46), s(38), sh_col)
        fill_polygon(buf, width, height, [
            pt(48 + 4, 46 + 4), pt(74 + 4, 86 + 4), pt(58 + 4, 86 + 4), pt(38 + 4, 52 + 4)
        ], sh_col)
        fill_rect(buf, width, height, origin_x + sh_offset + s(18), origin_y + sh_offset + s(16), s(16), s(70), sh_col)

    # 2. Outer Reel Circle + 3px Black Stroke
    fill_circle(buf, width, height, origin_x + s(50), origin_y + s(46), s(38), BLACK)
    fill_circle(buf, width, height, origin_x + s(50), origin_y + s(46), s(35), YELLOW)

    # 3. 'R' Kickstand Leg + 3px Black Stroke
    fill_polygon(buf, width, height, [
        pt(47, 45), pt(75.5, 87.5), pt(56.5, 87.5), pt(36.5, 51)
    ], BLACK)
    fill_polygon(buf, width, height, [
        pt(48, 46), pt(74, 86), pt(58, 86), pt(38, 52)
    ], YELLOW)

    # 4. Vertical Film Spine + 3px Black Stroke
    fill_rect(buf, width, height, origin_x + s(16.5), origin_y + s(14.5), s(19), s(73), BLACK)
    fill_rect(buf, width, height, origin_x + s(18), origin_y + s(16), s(16), s(70), CHARCOAL)

    # 5. Film Perforations
    for vy in [24, 38, 52, 66]:
        fill_rect(buf, width, height, origin_x + s(20.5), origin_y + s(vy - 1), s(11), s(8), BLACK)
        fill_rect(buf, width, height, origin_x + s(22), origin_y + s(vy), s(8), s(6), WHITE if not mono else BLACK)

    # 6. Spool Window Apertures
    # Aperture 1 (top)
    fill_circle(buf, width, height, origin_x + s(50), origin_y + s(24), s(8.5), BLACK)
    fill_circle(buf, width, height, origin_x + s(50), origin_y + s(24), s(6.5), CHARCOAL if not mono else BLACK)

    # Aperture 2 (right)
    fill_circle(buf, width, height, origin_x + s(70), origin_y + s(40), s(8.5), BLACK)
    fill_circle(buf, width, height, origin_x + s(70), origin_y + s(40), s(6.5), SAGE if not mono else BLACK)

    # Aperture 3 (bottom-right)
    fill_circle(buf, width, height, origin_x + s(62), origin_y + s(62), s(8.5), BLACK)
    fill_circle(buf, width, height, origin_x + s(62), origin_y + s(62), s(6.5), WHITE if not mono else BLACK)

    # 7. Center Hub Spindle
    fill_circle(buf, width, height, origin_x + s(50), origin_y + s(46), s(14), BLACK)
    fill_circle(buf, width, height, origin_x + s(50), origin_y + s(46), s(12), CHARCOAL if not mono else BLACK)
    fill_circle(buf, width, height, origin_x + s(50), origin_y + s(46), s(7), BLACK)
    fill_circle(buf, width, height, origin_x + s(50), origin_y + s(46), s(5.5), YELLOW)
    fill_circle(buf, width, height, origin_x + s(50), origin_y + s(46), s(2.5), BLACK)


# --- 1. Launcher icon (1024x1024) ---
print("Rendering assets/icon.png (1024x1024)...")
icon_buf = bytearray(1024 * 1024 * 4)
# Deep Charcoal background
fill_rect(icon_buf, 1024, 1024, 0, 0, 1024, 1024, (23, 30, 25, 255))
# Subtle yellow dot pattern (32x32)
for dy in range(16, 1024, 32):
    for dx in range(16, 1024, 32):
        fill_circle(icon_buf, 1024, 1024, dx, dy, 2.0, (255, 225, 124, 30))

# Neo-Brutalist White/Yellow Badge with 12px black border and 16px hard shadow
BADGE_SIZE = 680
BX = (1024 - BADGE_SIZE) // 2
BY = (1024 - BADGE_SIZE) // 2
SH = 16
# Shadow
fill_rect(icon_buf, 1024, 1024, BX + SH, BY + SH, BADGE_SIZE, BADGE_SIZE, (0, 0, 0, 255))
# Outer border
fill_rect(icon_buf, 1024, 1024, BX, BY, BADGE_SIZE, BADGE_SIZE, (0, 0, 0, 255))
# Yellow Badge Fill
fill_rect(icon_buf, 1024, 1024, BX + 10, BY + 10, BADGE_SIZE - 20, BADGE_SIZE - 20, (255, 225, 124, 255))

# Draw Emblem centered
draw_reelnest_emblem(icon_buf, 1024, 1024, BX + 80, BY + 80, 5.2)
write_png(os.path.join(ASSETS, "icon.png"), 1024, 1024, icon_buf)


# --- 2. Adaptive Foreground (1024x1024, transparent) ---
print("Rendering assets/adaptive-icon.png (1024x1024)...")
adapt_buf = bytearray(1024 * 1024 * 4)
# Fit inside 66% safe circle (radius 338px)
draw_reelnest_emblem(adapt_buf, 1024, 1024, (1024 - 600) // 2, (1024 - 600) // 2, 6.0)
write_png(os.path.join(ASSETS, "adaptive-icon.png"), 1024, 1024, adapt_buf)


# --- 3. Adaptive Monochrome (1024x1024, transparent, white silhouette) ---
print("Rendering assets/adaptive-icon-monochrome.png (1024x1024)...")
mono_buf = bytearray(1024 * 1024 * 4)
draw_reelnest_emblem(mono_buf, 1024, 1024, (1024 - 600) // 2, (1024 - 600) // 2, 6.0, mono=True)
write_png(os.path.join(ASSETS, "adaptive-icon-monochrome.png"), 1024, 1024, mono_buf)


# --- 4. Splash Screen (1284x2778) ---
print("Rendering assets/splash.png (1284x2778)...")
splash_buf = bytearray(1284 * 2778 * 4)
# Deep Charcoal full screen
fill_rect(splash_buf, 1284, 2778, 0, 0, 1284, 2778, (23, 30, 25, 255))
# Centered Neo-Brutalist badge (480x480)
S_BADGE = 480
S_BX = (1284 - S_BADGE) // 2
S_BY = (2778 - S_BADGE) // 2 - 80
fill_rect(splash_buf, 1284, 2778, S_BX + 12, S_BY + 12, S_BADGE, S_BADGE, (0, 0, 0, 255))
fill_rect(splash_buf, 1284, 2778, S_BX, S_BY, S_BADGE, S_BADGE, (0, 0, 0, 255))
fill_rect(splash_buf, 1284, 2778, S_BX + 8, S_BY + 8, S_BADGE - 16, S_BADGE - 16, (255, 225, 124, 255))

draw_reelnest_emblem(splash_buf, 1284, 2778, S_BX + 60, S_BY + 60, 3.6)
write_png(os.path.join(ASSETS, "splash.png"), 1284, 2778, splash_buf)


# --- 5. Favicon (48x48) ---
print("Rendering assets/favicon.png (48x48)...")
fav_buf = bytearray(48 * 48 * 4)
fill_rect(fav_buf, 48, 48, 0, 0, 48, 48, (23, 30, 25, 255))
fill_rect(fav_buf, 48, 48, 2, 2, 44, 44, (255, 225, 124, 255))
draw_reelnest_emblem(fav_buf, 48, 48, 4, 4, 0.4)
write_png(os.path.join(ASSETS, "favicon.png"), 48, 48, fav_buf)

print("All raster assets generated successfully!")
