#!/usr/bin/env python3
"""Render Saptarshi's portrait as an animated monochrome terminal SVG."""
import html
import os
import sys
from pathlib import Path
from PIL import Image, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
PROFILE = __import__('json').loads((ROOT / 'config/profile.json').read_text())
NAME = PROFILE['name']
HANDLE = PROFILE['github_username']
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'assets/saptarshi-prepped.png'
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / 'saptarshi-ascii.svg'
COLS = int(os.getenv('COLS', '180'))
ART_W = 800
CELL_W = ART_W / COLS
CELL_H = CELL_W * 15 / 8
ROWS = round(COLS * 8 / 15)
RAMP = ' .`:-=+*cs#%@'
GAMMA = 1.18
WHITE_FLOOR = 0.80
PAD, TITLE, STATUS = 20, 30, 30
BG, BG2, FRAME, TEXT = '#0d1117', '#111722', '#30363d', '#c9d1d9'
CANVAS_W, CANVAS_H = ART_W + PAD * 2, TITLE + ROWS * CELL_H + STATUS + PAD
ROW_DUR = 5.8 / ROWS

im = Image.open(SRC).convert('L')
im = ImageEnhance.Contrast(im).enhance(1.05)
im = im.resize((COLS, ROWS), Image.LANCZOS)
px = im.load()
rows = []
for y in range(ROWS):
    chars = []
    for x in range(COLS):
        lum = pow(px[x, y] / 255.0, GAMMA)
        if lum >= WHITE_FLOOR:
            chars.append(' ')
        else:
            idx = max(0, min(len(RAMP)-1, int((1-lum)*(len(RAMP)-1)+0.5)))
            chars.append(RAMP[idx])
    rows.append(''.join(chars))

parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">',
'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#111722"/><stop offset="1" stop-color="#0d1117"/></linearGradient></defs>',
f'<rect width="100%" height="100%" rx="12" fill="url(#bg)"/><rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" fill="none" stroke="{FRAME}"/><line x1="0" y1="{TITLE}" x2="{CANVAS_W}" y2="{TITLE}" stroke="{FRAME}"/>']
for i, c in enumerate(['#ff5f56','#ffbd2e','#27c93f']):
    parts.append(f'<circle cx="{PAD+i*16}" cy="{TITLE/2}" r="5" fill="{c}"/>')
parts.append(f'<text x="{CANVAS_W/2}" y="{TITLE/2+4}" fill="#7d8590" font-size="12" text-anchor="middle">{HANDLE}@github: ~$ ./portrait.sh</text>')
art_top = TITLE + PAD * 0.35
for ry, line in enumerate(rows):
    y = art_top + ry * CELL_H + CELL_H * 0.74
    row_y = art_top + ry * CELL_H
    delay = ry * ROW_DUR
    safe = html.escape(line)
    parts.append(f'<clipPath id="r{ry}"><rect x="{PAD}" y="{row_y:.1f}" width="0" height="{CELL_H}"><animate attributeName="width" from="0" to="{ART_W}" begin="{delay:.3f}s" dur="{ROW_DUR:.2f}s" fill="freeze"/></rect></clipPath>')
    parts.append(f'<g clip-path="url(#r{ry})"><text xml:space="preserve" x="{PAD}" y="{y:.1f}" fill="{TEXT}" font-size="{CELL_H*0.86:.1f}" textLength="{ART_W}" lengthAdjust="spacing">{safe}</text></g>')
status_line = TITLE + ROWS * CELL_H + PAD * 0.35
parts += [f'<line x1="0" y1="{status_line:.1f}" x2="{CANVAS_W}" y2="{status_line:.1f}" stroke="{FRAME}"/>', f'<text x="{PAD}" y="{status_line+19:.1f}" fill="#7d8590" font-size="12">$ whoami → {NAME}</text>', '</svg>']
OUT.write_text(''.join(parts))
print(f'wrote {OUT}')
