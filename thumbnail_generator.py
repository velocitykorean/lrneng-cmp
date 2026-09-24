"""
High-CTR YouTube Thumbnail Generator for Learn English Champs
Generates vibrant, impressive, viral-optimized YouTube thumbnails with:
- Extra large, punchy 3D outlined typography in the center gap
- High-contrast color scheme (Pure White, Electric Yellow, Vibrant Cyan)
- Soft radiant aura glow behind text
- Channel branding and episode pill badge
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import config

def draw_heavy_3d_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, center_x: int, y: int, fill_color: tuple, stroke_color: tuple = (10, 15, 25), stroke_width: int = 9):
    """
    Renders extra thick stroke outline and heavy 3D drop-shadow for maximum thumbnail punchiness.
    """
    b = draw.textbbox((0, 0), text, font=font)
    tw = b[2] - b[0]
    tx = center_x - (tw // 2)

    # 1. 3D Bottom-Right Drop Shadow
    shadow_offset = stroke_width + 4
    for dx in range(-stroke_width, stroke_width + 1):
        for dy in range(-stroke_width, stroke_width + 1):
            if dx * dx + dy * dy <= stroke_width * stroke_width:
                draw.text((tx + dx + 3, y + dy + shadow_offset), text, fill=(0, 0, 0, 210), font=font)

    # 2. Outer stroke border
    for dx in range(-stroke_width, stroke_width + 1):
        for dy in range(-stroke_width, stroke_width + 1):
            if dx * dx + dy * dy <= stroke_width * stroke_width:
                draw.text((tx + dx, y + dy), text, fill=stroke_color, font=font)

    # 3. Main text fill
    draw.text((tx, y), text, fill=fill_color, font=font)

def generate_thumbnail(image_path: str, title_1: str, title_2: str, hook: str, output_path: str, ep_number: int = 1) -> str:
    """
    Generates a viral YouTube thumbnail utilizing the center gap between the podcast characters.
    """
    print(f"[Thumbnail] Generating impressive thumbnail: '{title_1} {title_2}'...")
    base = Image.open(image_path).convert("RGBA")
    if base.size != (config.VIDEO_WIDTH, config.VIDEO_HEIGHT):
        base = base.resize((config.VIDEO_WIDTH, config.VIDEO_HEIGHT), Image.Resampling.LANCZOS)

    # 1. Soft Radiant Aura Glow in the center gap
    glow_mask = Image.new("L", (config.VIDEO_WIDTH, config.VIDEO_HEIGHT), 0)
    glow_draw = ImageDraw.Draw(glow_mask)
    glow_draw.ellipse([600, 120, 1320, 680], fill=85)
    glow_mask = glow_mask.filter(ImageFilter.GaussianBlur(radius=85))

    glow_layer = Image.new("RGBA", (config.VIDEO_WIDTH, config.VIDEO_HEIGHT), (0, 229, 255, 0))
    glow_layer.putalpha(glow_mask)
    thumb = Image.alpha_composite(base, glow_layer)

    overlay = Image.new("RGBA", (config.VIDEO_WIDTH, config.VIDEO_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    font_path = config.FONT_PATH if os.path.exists(config.FONT_PATH) else config.FALLBACK_FONT_PATH
    badge_font = ImageFont.truetype(font_path, 30)
    logo_bold = ImageFont.truetype(font_path, 32)
    logo_small = ImageFont.truetype(font_path, 16)

    def get_fitted_font(text: str, base_size: int, max_w: int, min_s: int = 36):
        font = ImageFont.truetype(font_path, base_size)
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        if tw > max_w:
            scale = max_w / float(tw)
            adjusted_size = max(min_s, int(base_size * scale))
            return ImageFont.truetype(font_path, adjusted_size)
        return font

    # 2. Top Right Channel Branding Badge: LEARN ENGLISH CHAMPS
    logo_x, logo_y = 1550, 50
    draw.text((logo_x, logo_y), "LEARN ENGLISH", fill=(210, 220, 235, 230), font=logo_small)
    draw.text((logo_x, logo_y + 18), "CHAMPS", fill=(255, 255, 255, 255), font=logo_bold)
    draw.ellipse((logo_x + 145, logo_y + 16, logo_x + 180, logo_y + 51), outline=(255, 255, 255, 220), width=3)
    draw.ellipse((logo_x + 154, logo_y + 25, logo_x + 171, logo_y + 42), fill=(0, 229, 255, 240))

    # 3. Top Episode Badge Pill: • LEARN ENGLISH CHAMPS EP. XX •
    badge_text = f"• LEARN ENGLISH CHAMPS EP. {ep_number:02d} •"
    bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
    bw = bbox[2] - bbox[0]
    bh = bbox[3] - bbox[1]
    bx = (config.VIDEO_WIDTH - bw) // 2
    by = 175

    draw.rounded_rectangle(
        [bx - 25, by - 10, bx + bw + 25, by + bh + 12],
        radius=16,
        fill=(255, 45, 85, 245),
        outline=(255, 255, 255, 230),
        width=2
    )
    draw.text((bx, by), badge_text, fill=(255, 255, 255), font=badge_font)

    # 4. Main Title Line 1: Crisp Pure White (Dynamically fitted to max 820px)
    font_t1 = get_fitted_font(title_1.upper(), base_size=98, max_w=820, min_s=48)
    draw_heavy_3d_text(draw, title_1.upper(), font_t1, 960, 255, (255, 255, 255), stroke_width=9)

    # 5. Main Title Line 2: Vibrant Electric Yellow (Dynamically fitted to max 820px)
    font_t2 = get_fitted_font(title_2.upper(), base_size=98, max_w=820, min_s=48)
    draw_heavy_3d_text(draw, title_2.upper(), font_t2, 960, 365, (255, 230, 0), stroke_width=9)

    # 6. Hook Pill: Vibrant Cyan Pill with High-Contrast Navy Text (Dynamically fitted to max 800px)
    font_hook = get_fitted_font(hook, base_size=46, max_w=780, min_s=28)
    hb = draw.textbbox((0, 0), hook, font=font_hook)
    hw = hb[2] - hb[0]
    hh = hb[3] - hb[1]
    hx = (config.VIDEO_WIDTH - hw) // 2
    hy = 495

    draw.rounded_rectangle(
        [hx - 30, hy - 12, hx + hw + 30, hy + hh + 14],
        radius=22,
        fill=(0, 229, 255, 245),
        outline=(255, 255, 255, 240),
        width=3
    )
    draw.text((hx, hy), hook, fill=(10, 25, 48), font=font_hook)

    thumb = Image.alpha_composite(thumb, overlay)
    thumb.convert("RGB").save(output_path, quality=95)
    print(f"[Thumbnail] Saved impressive thumbnail to: {output_path}")
    return output_path

if __name__ == "__main__":
    generate_thumbnail(
        config.DEFAULT_IMAGE_PATH,
        "SPEAK ENGLISH",
        "WITHOUT FEAR!",
        "Overcome Shyness & Speak Fluently",
        os.path.join(config.OUTPUT_DIR, "sample_thumbnail_big.png")
    )
