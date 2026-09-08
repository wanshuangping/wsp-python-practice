from PIL import Image, ImageDraw, ImageFont
import os

OUT = "/Users/temu/WorkBuddy/2026-08-25-20-20-39/outputs"
USER_IMG = "/Users/temu/.workbuddy/clipboard-images/clipboard-2026-08-26T06-46-46-884Z-5328a045.jpg"
PLAIN_IMG = os.path.join(OUT, "A_single_ordinary_gray_athleti_2026-08-26T07-22-31.png")
FONT_DIR = "/System/Library/Fonts/Supplemental"

def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

W, H = 1600, 1120
canvas = Image.new("RGB", (W, H), "white")
draw = ImageDraw.Draw(canvas)

# ---- Title ----
draw.text((W // 2, 42), "WHY OUR SOCKS ARE BETTER",
          font=font("Arial Bold.ttf", 46), fill="#1A1A1A", anchor="mm")
draw.text((W // 2, 98), "Extra Wide Non-Binding Design   vs   Ordinary Tight Socks",
          font=font("Arial.ttf", 24), fill="#666666", anchor="mm")

# ---- Cards ----
draw.rounded_rectangle([60, 150, 760, 1050], radius=18, fill="#F7F7F7")
draw.rounded_rectangle([840, 150, 1540, 1050], radius=18, fill="#F7F7F7")
draw.line([(W // 2, 150), (W // 2, 1050)], fill="#DDDDDD", width=2)

# ---- Labels ----
draw.text((410, 188), "OUR SOCKS", font=font("Arial Bold.ttf", 30), fill="#1E7A46", anchor="mm")
draw.text((410, 220), "Extra Wide Diabetic Socks", font=font("Arial.ttf", 21), fill="#555555", anchor="mm")
draw.text((1190, 188), "REGULAR SOCKS", font=font("Arial Bold.ttf", 30), fill="#C0392B", anchor="mm")
draw.text((1190, 220), "Ordinary Athletic Socks", font=font("Arial.ttf", 21), fill="#555555", anchor="mm")

# ---- Socks images ----
u = Image.open(USER_IMG).convert("RGB")
u.thumbnail((360, 430))
canvas.paste(u, (410 - u.width // 2, 250))

p = Image.open(PLAIN_IMG).convert("RGBA")
p.thumbnail((360, 430))
bg = Image.new("RGBA", p.size, (255, 255, 255, 255))
p = Image.alpha_composite(bg, p).convert("RGB")
canvas.paste(p, (1190 - p.width // 2, 250))

# ---- Feature lists ----
features_left = [
    "Loose, non-binding top",
    "Protects circulation",
    "Breathable mesh fabric",
    "Seamless toe, no friction",
    "Stays up all day",
]
features_right = [
    "Tight elastic cuff",
    "May restrict circulation",
    "Traps heat & sweat",
    "Can leave red marks",
    "Uncomfortable all day",
]

fnt = font("Arial.ttf", 23)
fy, gap = 700, 66
for i, (lt, rt) in enumerate(zip(features_left, features_right)):
    y = fy + i * gap
    # left green check
    cx_l = 100
    draw.ellipse([cx_l - 14, y - 14, cx_l + 14, y + 14], fill="#1E7A46")
    draw.line([(cx_l - 7, y - 1), (cx_l - 1, y + 5), (cx_l + 8, y - 7)], fill="white", width=3, joint="curve")
    draw.text((128, y), lt, font=fnt, fill="#333333", anchor="lm")
    # right red cross
    cx_r = 930
    draw.ellipse([cx_r - 14, y - 14, cx_r + 14, y + 14], fill="#C0392B")
    draw.line([(cx_r - 7, y - 7), (cx_r + 7, y + 7)], fill="white", width=3)
    draw.line([(cx_r - 7, y + 7), (cx_r + 7, y - 7)], fill="white", width=3)
    draw.text((958, y), rt, font=fnt, fill="#333333", anchor="lm")

# ---- Bottom CTA ----
draw.text((W // 2, 1090), "3 PAIRS    •    Diabetic-Friendly    •    For Swollen Feet",
          font=font("Arial Bold.ttf", 24), fill="#1E7A46", anchor="mm")

out_path = os.path.join(OUT, "wide_socks_comparison.png")
canvas.save(out_path)
print("saved:", out_path)
