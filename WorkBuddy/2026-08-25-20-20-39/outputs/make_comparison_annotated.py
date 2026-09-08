from PIL import Image, ImageDraw, ImageFont
import os

OUT = "/Users/temu/WorkBuddy/2026-08-25-20-20-39/outputs"
BASE_IMG = os.path.join(OUT, "A_clean_e_commerce_comparison__2026-08-26T07-28-36.png")
FONT_DIR = "/System/Library/Fonts/Supplemental"

def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

img = Image.open(BASE_IMG).convert("RGB")
W, H = img.size
print("image size", W, H)
draw = ImageDraw.Draw(img)

GREEN = "#1E7A46"
RED = "#C0392B"
TITLE_COL = "#1A1A1A"
TXT_COL = "#333333"

# ---- Top title ----
draw.text((W // 2, int(H * 0.05)), "WHY OUR SOCKS ARE BETTER",
          font=font("Arial Bold.ttf", 40), fill=TITLE_COL, anchor="mm")

# ---- Left features ----
left_features = [
    ("NO CONSTRICTION", "protects circulation", 0.06, 0.18, (0.32, 0.09)),
    ("LOOSE, COMFORTABLE FIT", "allows natural movement", 0.06, 0.35, (0.30, 0.30)),
    ("BREATHABLE MESH", "keeps feet dry", 0.06, 0.52, (0.30, 0.44)),
    ("SEAMLESS TOE", "reduces friction", 0.06, 0.70, (0.09, 0.86)),
    ("THICK CUSHIONED SOLE", "absorbs impact & protects feet", 0.06, 0.88, (0.16, 0.94)),
]

for idx, (title, sub, cx_r, cy_r, target_r) in enumerate(left_features):
    cx, cy = int(W * cx_r), int(H * cy_r)
    target = (int(W * target_r[0]), int(H * target_r[1]))
    # green circle
    draw.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=GREEN)
    # white check
    draw.line([(cx - 5, cy), (cx - 1, cy + 5), (cx + 7, cy - 6)], fill="white", width=3, joint="curve")
    # text: first feature placed above the line so the leader line doesn't cross text
    if idx == 0:
        draw.text((cx + 25, cy - 26), title, font=font("Arial Bold.ttf", 19), fill=GREEN, anchor="lm")
        draw.text((cx + 25, cy - 6), sub, font=font("Arial.ttf", 16), fill=TXT_COL, anchor="lm")
    else:
        draw.text((cx + 25, cy - 10), title, font=font("Arial Bold.ttf", 19), fill=GREEN, anchor="lm")
        draw.text((cx + 25, cy + 12), sub, font=font("Arial.ttf", 16), fill=TXT_COL, anchor="lm")
    # line to target
    start = (cx + 14, cy)
    draw.line([start, target], fill=GREEN, width=2)
    draw.ellipse([target[0] - 4, target[1] - 4, target[0] + 4, target[1] + 4], fill=GREEN)

# ---- Right features (placed on the left side of right leg to avoid clipping) ----
right_features = [
    ("ELASTIC CUFF", "snug fit may restrict circulation", 0.74, 0.26, (0.74, 0.30)),
    ("SEAMED TOE", "may cause friction & irritation", 0.74, 0.82, (0.68, 0.95)),
]

for title, sub, cx_r, cy_r, target_r in right_features:
    cx, cy = int(W * cx_r), int(H * cy_r)
    target = (int(W * target_r[0]), int(H * target_r[1]))
    # red circle
    draw.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=RED)
    # white cross
    draw.line([(cx - 5, cy - 5), (cx + 5, cy + 5)], fill="white", width=3)
    draw.line([(cx - 5, cy + 5), (cx + 5, cy - 5)], fill="white", width=3)
    # text (place to the left of the circle to avoid right-edge clipping)
    draw.text((cx - 25, cy - 10), title, font=font("Arial Bold.ttf", 19), fill=RED, anchor="rm")
    draw.text((cx - 25, cy + 12), sub, font=font("Arial.ttf", 16), fill=TXT_COL, anchor="rm")
    # line to target
    start = (cx + 14, cy)
    draw.line([start, target], fill=RED, width=2)
    draw.ellipse([target[0] - 4, target[1] - 4, target[0] + 4, target[1] + 4], fill=RED)

# ---- Bottom labels ----
draw.text((int(W * 0.28), int(H * 0.96)), "Diabetic Socks", font=font("Arial Bold.ttf", 34), fill=TITLE_COL, anchor="mm")
draw.text((int(W * 0.74), int(H * 0.96)), "Regular Athletic Socks", font=font("Arial Bold.ttf", 34), fill=TITLE_COL, anchor="mm")

out_path = os.path.join(OUT, "wide_socks_comparison_annotated.png")
img.save(out_path)
print("saved:", out_path)
