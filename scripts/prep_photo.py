#!/usr/bin/env python3
"""Prepare Saptarshi's portrait for high-contrast terminal ASCII rendering.

The supplied photo already has a clean white background. The script therefore
avoids a mandatory heavyweight background-removal model and instead performs
white-background masking, tone normalization, edge preservation, and square crop.
"""
import sys
from pathlib import Path
import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
INP = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "assets/saptarshi-source.jpg"
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "assets/saptarshi-prepped.png"

img = cv2.imread(str(INP), cv2.IMREAD_COLOR)
if img is None:
    raise FileNotFoundError(INP)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# White background -> low-contrast/bright region; retain the darker subject.
mask = (gray < 245).astype(np.uint8) * 255
kernel = np.ones((5, 5), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
mask = cv2.GaussianBlur(mask, (0, 0), 1.0)

smooth = gray.copy()
for _ in range(2):
    smooth = cv2.bilateralFilter(smooth, 9, 35, 9)

subject = smooth[mask > 32]
lo, hi = np.percentile(subject, [2, 98]) if subject.size else (30, 240)
tone = np.clip((smooth.astype(np.float32) - lo) / max(hi - lo, 1), 0, 1) * 255
out = tone * (mask / 255.0) + 255.0 * (1 - mask / 255.0)
out = np.clip(out, 0, 255).astype(np.uint8)

ys, xs = np.where(mask > 32)
if len(xs) == 0:
    raise RuntimeError("Could not detect the portrait subject.")
side = max(xs.max() - xs.min(), ys.max() - ys.min()) + 70
cx, cy = (xs.min() + xs.max()) // 2, (ys.min() + ys.max()) // 2
canvas = np.full((side, side), 255, dtype=np.uint8)
x0, y0 = cx - side // 2, cy - side // 2
sx0, sy0 = max(x0, 0), max(y0, 0)
sx1, sy1 = min(x0 + side, out.shape[1]), min(y0 + side, out.shape[0])
canvas[sy0-y0:sy1-y0, sx0-x0:sx1-x0] = out[sy0:sy1, sx0:sx1]

OUT.parent.mkdir(parents=True, exist_ok=True)
Image.fromarray(canvas, mode="L").save(OUT)
print(f"wrote {OUT} {canvas.shape}")
