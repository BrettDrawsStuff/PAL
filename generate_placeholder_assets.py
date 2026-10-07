"""
Generates placeholder PNG sequences for every PAL animation state.
These are NOT final art — just simple shape-based stand-ins so the
app's sprite-sequence loading mechanism can be built and tested before
real hand-drawn frames exist. Replace each state's frame_0N.png files
with real artwork later, using the exact same filenames/folder names.

Run: python3 generate_placeholder_assets.py
Output: assets/pal/<state>/frame_01.png ... frame_06.png
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

OUT_ROOT = os.path.join(os.path.dirname(__file__), "assets", "pal")
SIZE = 160
FRAMES = 6

# Color tokens (matching the prototype's palette)
ORANGE = (255, 106, 61)
CYAN = (52, 216, 200)
PINK = (255, 79, 160)
DARK = (28, 16, 23)
WARN = (255, 92, 92)

try:
    FONT = ImageFont.load_default()
except Exception:
    FONT = None

def blank():
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))

def draw_label(draw, text):
    # Optional dev caption (off by default) — set label_each=True in
    # save_sequence to burn the state/frame name into each placeholder.
    draw.rectangle([0, SIZE - 16, SIZE, SIZE], fill=(0, 0, 0, 140))
    draw.text((4, SIZE - 14), text, fill=(255, 255, 255, 230), font=FONT)

def draw_pal_circle(draw, cx, cy, r, color):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color + (255,))

def save_sequence(state, frame_builder, label_each=False):
    folder = os.path.join(OUT_ROOT, state)
    os.makedirs(folder, exist_ok=True)
    for i in range(FRAMES):
        img = blank()
        draw = ImageDraw.Draw(img)
        frame_builder(draw, i)
        if label_each:
            draw_label(draw, f"{state} {i+1}/{FRAMES}")
        img.save(os.path.join(folder, f"frame_{i+1:02d}.png"))
    print(f"  wrote {state} ({FRAMES} frames)")

cx, cy = SIZE // 2, SIZE // 2 - 6
base_r = 46

# ---- idle: gentle breathing scale ----
def f_idle(draw, i):
    t = i / (FRAMES - 1)
    scale = 1 + 0.06 * math.sin(t * math.pi)
    draw_pal_circle(draw, cx, cy, base_r * scale, ORANGE)

# ---- idle fidget variants: small head-tilt / blink-like squash ----
def f_idle_fidget_1(draw, i):
    t = i / (FRAMES - 1)
    squash = 1 - 0.1 * math.sin(t * math.pi)
    draw.ellipse([cx - base_r, cy - base_r * squash, cx + base_r, cy + base_r * squash], fill=ORANGE + (255,))

def f_idle_fidget_2(draw, i):
    t = i / (FRAMES - 1)
    offset = 8 * math.sin(t * math.pi * 2)
    draw_pal_circle(draw, cx + offset, cy, base_r, ORANGE)

# ---- wake: scale up from nothing with slight overshoot ----
def f_wake(draw, i):
    t = i / (FRAMES - 1)
    scale = min(1.15, 1.3 * t) if t < 0.8 else 1.0
    draw_pal_circle(draw, cx, cy, base_r * max(scale, 0.05), PINK)

# ---- sleep: scale down to nothing ----
def f_sleep(draw, i):
    t = i / (FRAMES - 1)
    scale = max(0.02, 1 - t)
    draw_pal_circle(draw, cx, cy, base_r * scale, PINK)

# ---- listening: attentive lean + small "ear" tick marks ----
def f_listening(draw, i):
    t = i / (FRAMES - 1)
    lean = 4 * math.sin(t * math.pi)
    draw_pal_circle(draw, cx + lean, cy, base_r, CYAN)
    draw.line([cx - 10, cy - base_r - 6, cx - 10, cy - base_r + 4], fill=(255,255,255,200), width=3)
    draw.line([cx + 10, cy - base_r - 6, cx + 10, cy - base_r + 4], fill=(255,255,255,200), width=3)

# ---- thinking: vertical bob ----
def f_thinking(draw, i):
    t = i / (FRAMES - 1)
    bob = 8 * math.sin(t * math.pi * 2)
    draw_pal_circle(draw, cx, cy + bob, base_r, CYAN)
    for k, dx in enumerate([-18, 0, 18]):
        dot_phase = (t * 3 - k * 0.3) % 1
        dot_y = cy - base_r - 16 - 6 * math.sin(dot_phase * math.pi)
        draw.ellipse([cx+dx-4, dot_y-4, cx+dx+4, dot_y+4], fill=(255,255,255,220))

# ---- alert: quick side-to-side jitter ----
def f_alert(draw, i):
    t = i / (FRAMES - 1)
    jitter = 10 * math.sin(t * math.pi * 4)
    draw_pal_circle(draw, cx + jitter, cy, base_r, ORANGE)
    draw.ellipse([cx-base_r-14, cy-base_r-14, cx+base_r+14, cy+base_r+14], outline=(255,255,255,120), width=3)

# ---- found: pop + radiating sparkle burst ----
def f_found(draw, i):
    t = i / (FRAMES - 1)
    scale = 0.8 + 0.3 * math.sin(min(t * 1.6, 1) * math.pi)
    draw_pal_circle(draw, cx, cy, base_r * scale, PINK)
    if t > 0.3:
        burst = (t - 0.3) / 0.7
        for ang in range(0, 360, 45):
            rad = math.radians(ang)
            x1 = cx + math.cos(rad) * (base_r + 6)
            y1 = cy + math.sin(rad) * (base_r + 6)
            x2 = cx + math.cos(rad) * (base_r + 6 + burst * 22)
            y2 = cy + math.sin(rad) * (base_r + 6 + burst * 22)
            draw.line([x1, y1, x2, y2], fill=(255, 220, 120, 230), width=3)

# ---- searching: rotating "scan" ring ----
def f_searching(draw, i):
    t = i / (FRAMES - 1)
    draw_pal_circle(draw, cx, cy, base_r, CYAN)
    ang = t * 360
    rad = math.radians(ang)
    x2 = cx + math.cos(rad) * (base_r + 16)
    y2 = cy + math.sin(rad) * (base_r + 16)
    draw.ellipse([cx-base_r-16, cy-base_r-16, cx+base_r+16, cy+base_r+16], outline=(255,255,255,90), width=2)
    draw.line([cx, cy, x2, y2], fill=(255,255,255,200), width=3)

# ---- welcome back (short absence): quick friendly bounce ----
def f_welcome_back_short(draw, i):
    t = i / (FRAMES - 1)
    bounce = abs(math.sin(t * math.pi)) * 10
    draw_pal_circle(draw, cx, cy - bounce, base_r, ORANGE)

# ---- welcome back (long absence): bigger double bounce ----
def f_welcome_back_long(draw, i):
    t = i / (FRAMES - 1)
    bounce = abs(math.sin(t * math.pi * 2)) * 14
    draw_pal_circle(draw, cx, cy - bounce, base_r, ORANGE)

# ---- warm recognition: soft warm glow pulse ----
def f_warm_recognition(draw, i):
    t = i / (FRAMES - 1)
    glow = 1 + 0.15 * math.sin(t * math.pi)
    draw.ellipse([cx-base_r*glow-10, cy-base_r*glow-10, cx+base_r*glow+10, cy+base_r*glow+10], fill=(255, 180, 120, 70))
    draw_pal_circle(draw, cx, cy, base_r, PINK)

# ---- teaching: pointing accent (small arrow/line) ----
def f_teaching(draw, i):
    t = i / (FRAMES - 1)
    draw_pal_circle(draw, cx, cy, base_r, CYAN)
    lean = 6 * math.sin(min(t * 1.5, 1) * math.pi)
    draw.line([cx + base_r - 4, cy, cx + base_r + 24 + lean, cy - 18], fill=(255,255,255,230), width=4)

# ---- defining a term: small "?" turning into "!" ----
def f_defining_term(draw, i):
    t = i / (FRAMES - 1)
    draw_pal_circle(draw, cx, cy, base_r, CYAN)
    mark = "?" if t < 0.5 else "!"
    try:
        draw.text((cx - 6, cy - 14), mark, fill=(255,255,255,255), font=FONT)
    except Exception:
        pass

# ---- honest uncertainty: head tilt + "?" ----
def f_uncertain(draw, i):
    t = i / (FRAMES - 1)
    tilt = 6 * math.sin(t * math.pi)
    draw_pal_circle(draw, cx + tilt, cy, base_r, ORANGE)
    try:
        draw.text((cx + base_r - 6, cy - base_r - 6), "?", fill=(255,255,255,255), font=FONT)
    except Exception:
        pass

# ---- mural changed / flagging: color glitch shift ----
def f_mural_changed(draw, i):
    t = i / (FRAMES - 1)
    color = ORANGE if int(t * 6) % 2 == 0 else CYAN
    offset = 4 if int(t * 6) % 2 == 0 else -4
    draw_pal_circle(draw, cx + offset, cy, base_r, color)

# ---- error / connection issue: red flash ----
def f_error(draw, i):
    t = i / (FRAMES - 1)
    flash = 0.5 + 0.5 * math.sin(t * math.pi * 3)
    r = (int(DARK[0] + (WARN[0]-DARK[0]) * flash), int(DARK[1] + (WARN[1]-DARK[1]) * flash), int(DARK[2] + (WARN[2]-DARK[2]) * flash))
    draw_pal_circle(draw, cx, cy, base_r, r)

STATES = [
    ("idle", f_idle),
    ("idle_fidget_1", f_idle_fidget_1),
    ("idle_fidget_2", f_idle_fidget_2),
    ("wake", f_wake),
    ("sleep", f_sleep),
    ("listening", f_listening),
    ("thinking", f_thinking),
    ("alert", f_alert),
    ("found", f_found),
    ("searching", f_searching),
    ("welcome_back_short", f_welcome_back_short),
    ("welcome_back_long", f_welcome_back_long),
    ("warm_recognition", f_warm_recognition),
    ("teaching", f_teaching),
    ("defining_term", f_defining_term),
    ("uncertain", f_uncertain),
    ("mural_changed", f_mural_changed),
    ("error", f_error),
]

if __name__ == "__main__":
    print(f"Generating {len(STATES)} placeholder state sequences into {OUT_ROOT} ...")
    for name, builder in STATES:
        save_sequence(name, builder)
    print("Done.")
