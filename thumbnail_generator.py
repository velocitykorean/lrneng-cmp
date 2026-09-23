import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import config

def draw_stroke_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, center_x: int, y: int, fill_color: tuple, stroke_color: tuple = (15, 20, 30), stroke_width: int = 7):
    """
    Renders thick stroke outline and drop shadow for maximum thumbnail readability.
    """
    b = draw.textbbox((0, 0), text, font=font)
    tw = b[2] - b[0]
    tx = center_x - (tw // 2)

    # 1. Soft drop shadow offset
    shadow_offset = stroke_width + 2
    for dx in range(-stroke_width, stroke_width + 1):
        for dy in range(-stroke_width, stroke_width + 1):
            if dx * dx + dy * dy <= stroke_width * stroke_width:
                draw.text((tx + dx, y + dy + shadow_offset), text, fill=(0, 0, 0, 180), font=font)

    # 2. Outer stroke border
    for dx in range(-stroke_width, stroke_width + 1):
        for dy in range(-stroke_width, stroke_width + 1):
            if dx * dx + dy * dy <= stroke_width * stroke_width:
                draw.text((tx + dx, y + dy), text, fill=stroke_color, font=font)

    # 3. Main text fill
    draw.text((tx, y), text, fill=fill_color, font=font)

def generate_thumbnail(image_path: str, title_1: str, title_2: str, hook: str, output_path: str, ep_number: int = 1) -> str:
    """
    Generates a high-CTR YouTube thumbnail using the center gap space between the podcast characters.
    """
    print(f"[Thumbnail] Generating thumbnail: '{title_1} {title_2}'...")
    base = Image.open(image_path).convert("RGBA")
    if base.size != (config.VIDEO_WIDTH, config.VIDEO_HEIGHT):
        base = base.resize((config.VIDEO_WIDTH, config.VIDEO_HEIGHT), Image.Resampling.LANCZOS)

    # 1. Center Glow in the gap space
    glow_mask = Image.new("L", (config.VIDEO_WIDTH, config.VIDEO_HEIGHT), 0)
    glow_draw = ImageDraw.Draw(glow_mask)
    glow_draw.ellipse([620, 140, 1300, 660], fill=75)
    glow_mask = glow_mask.filter(ImageFilter.GaussianBlur(radius=80))

    glow_layer = Image.new("RGBA", (config.VIDEO_WIDTH, config.VIDEO_HEIGHT), (0, 229, 255, 0))
    glow_layer.putalpha(glow_mask)
    thumb = Image.alpha_composite(base, glow_layer)

    # Create overlay for crisp text and shapes
    overlay = Image.new("RGBA", (config.VIDEO_WIDTH, config.VIDEO_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    font_path = config.FONT_PATH if os.path.exists(config.FONT_PATH) else config.FALLBACK_FONT_PATH
    badge_font = ImageFont.truetype(font_path, 28)
    main_font = ImageFont.truetype(font_path, 76)
    sub_font = ImageFont.truetype(font_path, 40)
    logo_bold = ImageFont.truetype(font_path, 32)
    logo_small = ImageFont.truetype(font_path, 16)

    # 2. Top Right Logo Badge
    logo_x, logo_y = 1660, 50
    draw.text((logo_x, logo_y), "ENGLISH", fill=(220, 220, 220, 220), font=logo_small)
    draw.text((logo_x, logo_y + 18), "PODCAST", fill=(255, 255, 255, 255), font=logo_bold)
    draw.ellipse((logo_x + 160, logo_y + 22, logo_x + 185, logo_y + 47), outline=(255, 255, 255, 220), width=3)
    draw.ellipse((logo_x + 167, logo_y + 29, logo_x + 178, logo_y + 40), fill=(0, 229, 255, 240))

    # 3. Episode Pill Badge
    badge_text = f"- ENGLISH PODCAST EP. {ep_number:02d} -"
    bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
    bw = bbox[2] - bbox[0]
    bh = bbox[3] - bbox[1]
    bx = (config.VIDEO_WIDTH - bw) // 2
    by = 190

    draw.rounded_rectangle([bx - 22, by - 8, bx + bw + 22, by + bh + 10], radius=14, fill=(255, 45, 85, 240), outline=(255, 255, 255, 220), width=2)
    draw.text((bx, by), badge_text, fill=(255, 255, 255), font=badge_font)

    # 4. Main Title Line 1 (Crisp White)
    draw_stroke_text(draw, title_1.upper(), main_font, 960, 270, (255, 255, 255), stroke_width=7)

    # 5. Main Title Line 2 (Vibrant Yellow #FFE600)
    draw_stroke_text(draw, title_2.upper(), main_font, 960, 370, (255, 230, 0), stroke_width=7)

    # 6. Hook Pill (Cyan #00E5FF)
    hb = draw.textbbox((0, 0), hook, font=sub_font)
    hw = hb[2] - hb[0]
    hh = hb[3] - hb[1]
    hx = (config.VIDEO_WIDTH - hw) // 2
    hy = 490

    draw.rounded_rectangle([hx - 25, hy - 10, hx + hw + 25, hy + hh + 12], radius=18, fill=(0, 229, 255, 240), outline=(255, 255, 255, 240), width=3)
    draw.text((hx, hy), hook, fill=(10, 25, 45), font=sub_font)

    thumb = Image.alpha_composite(thumb, overlay)
    thumb.convert("RGB").save(output_path, quality=95)
    print(f"[Thumbnail] Saved thumbnail to: {output_path}")
    return output_path

if __name__ == "__main__":
    generate_thumbnail(
        config.DEFAULT_IMAGE_PATH,
        "STOP SAYING",
        "VERY TIRED!",
        "10 Natural Alternatives",
        os.path.join(config.OUTPUT_DIR, "sample_thumbnail.png")
    )
