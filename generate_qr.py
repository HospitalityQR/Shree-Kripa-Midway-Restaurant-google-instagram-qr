import os
import re
import json
import math
import qrcode
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

def load_config(config_path="config.js"):
    """Parse config.js and extract JSON settings."""
    if not os.path.exists(config_path):
        return {}
    with open(config_path, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r"window\.RESTAURANT_CONFIG\s*=\s*(\{.*?\});", content, re.DOTALL)
    if not match:
        return {}
    json_str = match.group(1)
    json_str = re.sub(r"//.*", "", json_str)
    json_str = re.sub(r",\s*([\]}])", r"\1", json_str)
    try:
        return json.loads(json_str)
    except Exception:
        return {}

def get_font(size, bold=False, italic=False, serif=False):
    """Load Windows system fonts cleanly with fallbacks."""
    candidates = []
    if serif and italic:
        candidates = ["georgiai.ttf", "timesbi.ttf", "timesi.ttf", "ariali.ttf"]
    elif serif and bold:
        candidates = ["georgiab.ttf", "timesbd.ttf", "arialbd.ttf"]
    elif serif:
        candidates = ["georgia.ttf", "times.ttf", "arial.ttf"]
    elif bold and italic:
        candidates = ["arialbi.ttf", "georgiabi.ttf", "timesbi.ttf"]
    elif bold:
        candidates = ["arialbd.ttf", "segoeuib.ttf", "georgiab.ttf", "timesbd.ttf"]
    elif italic:
        candidates = ["ariali.ttf", "georgiai.ttf", "timesi.ttf"]
    else:
        candidates = ["arial.ttf", "segoeui.ttf", "georgia.ttf"]

    for font_name in candidates:
        font_path = os.path.join("C:\\Windows\\Fonts", font_name)
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except Exception:
                pass
    return ImageFont.load_default()

def create_ambience_luxury_background(width=1200, height=1800):
    """
    Create an Ultra-Luxury Shree Kripa Ambience Background inspired directly by the
    uploaded restaurant interior photos:
    - Real Shree Kripa Dining Hall ambience (Peacock Teal velvet seating, warm golden cove
      ceiling lights, peacock mandala wall art) softly blended into the background
    - Deep Royal Peacock Teal Velvet & Warm Cove Gold color grading (#0A3C44 -> #052227 -> #031316)
    - Warm Golden Chandelier & Cove radial glow behind the brand crest and Hindi 'श्री कृपा' title
    """
    # Base gradient: Deep Peacock Teal Velvet & Warm Golden Cove
    y_idx = np.linspace(0, 1, height)[:, None]
    x_idx = np.linspace(0, 1, width)[None, :]

    # Top warm teal-gold cove -> Mid Royal Peacock Teal -> Deep Midnight Teal-Obsidian bottom
    r_base = (14 * (1 - y_idx) + 4 * y_idx)
    g_base = (62 * (1 - y_idx) + 22 * y_idx)
    b_base = (70 * (1 - y_idx) + 26 * y_idx)

    # Warm golden ceiling cove spotlight around top center (x=0.5, y=0.18)
    dist_top = np.sqrt(((x_idx - 0.5) / 0.52) ** 2 + ((y_idx - 0.18) / 0.24) ** 2)
    glow_top = np.clip(1.0 - dist_top, 0, 1) ** 1.8

    # Secondary soft peacock-emerald glow behind QR center (x=0.5, y=0.60)
    dist_mid = np.sqrt(((x_idx - 0.5) / 0.58) ** 2 + ((y_idx - 0.60) / 0.32) ** 2)
    glow_mid = np.clip(1.0 - dist_mid, 0, 1) ** 2.0

    r_grad = r_base + glow_top * 58 + glow_mid * 12
    g_grad = g_base + glow_top * 48 + glow_mid * 36
    b_grad = b_base + glow_top * 22 + glow_mid * 40

    grad_arr = np.stack([
        np.clip(r_grad, 0, 255),
        np.clip(g_grad, 0, 255),
        np.clip(b_grad, 0, 255)
    ], axis=2).astype(np.uint8)
    base_img = Image.fromarray(grad_arr, "RGB")

    # Composite actual restaurant ambience photos softly into the background
    amb_path = "ambience_1.jpg" if os.path.exists("ambience_1.jpg") else ("ambience_3.jpg" if os.path.exists("ambience_3.jpg") else None)
    if amb_path:
        try:
            amb = Image.open(amb_path).convert("RGB")
            # Cover-crop to 1200x1800
            aw, ah = amb.size
            target_ratio = width / height
            src_ratio = aw / ah
            if src_ratio > target_ratio:
                new_w = int(ah * target_ratio)
                left = (aw - new_w) // 2
                amb = amb.crop((left, 0, left + new_w, ah))
            else:
                new_h = int(aw / target_ratio)
                top = (ah - new_h) // 2
                amb = amb.crop((0, top, aw, top + new_h))
            amb = amb.resize((width, height), Image.Resampling.LANCZOS)

            # Soft architectural depth blur so foreground text & QR stay 100% crisp
            amb_blur = amb.filter(ImageFilter.GaussianBlur(radius=8))
            amb_blur = ImageEnhance.Contrast(amb_blur).enhance(1.15)
            amb_blur = ImageEnhance.Color(amb_blur).enhance(1.25)

            # Blend ambience photo with the Royal Peacock Teal & Gold gradient
            # Stronger ambience visibility in the upper/mid architectural arches, deeper vignette near edges
            amb_arr = np.array(amb_blur, dtype=np.float32)
            base_arr = np.array(base_img, dtype=np.float32)

            # Radial edge vignette so borders and footer are deep & clean
            edge_dist = np.sqrt(((x_idx - 0.5) / 0.55) ** 2 + ((y_idx - 0.45) / 0.55) ** 2)
            vignette = np.clip(1.0 - 0.45 * (edge_dist ** 1.6), 0.12, 0.30)[:, :, None]

            # Color-grade the ambience photo slightly towards Peacock Teal & Warm Gold
            graded_amb = np.zeros_like(amb_arr)
            graded_amb[:, :, 0] = amb_arr[:, :, 0] * 0.88
            graded_amb[:, :, 1] = amb_arr[:, :, 1] * 1.02 + 8
            graded_amb[:, :, 2] = amb_arr[:, :, 2] * 1.05 + 12

            blended = base_arr * (1.0 - vignette) + np.clip(graded_amb, 0, 255) * vignette
            base_img = Image.fromarray(np.clip(blended, 0, 255).astype(np.uint8), "RGB")
        except Exception as e:
            print("Ambience blend warning:", e)

    # Add subtle Peacock Mandala / Royal Arch watermark geometry & golden cove light beams
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)

    # Subtle golden cove ceiling arch lines at top (matching the stepped ceiling cove lights in the photo)
    cx, cy = width // 2, 210
    for r_arch, alpha_val in [(260, 26), (340, 20), (430, 14), (530, 10)]:
        odraw.ellipse(
            [cx - r_arch, cy - int(r_arch * 0.75), cx + r_arch, cy + int(r_arch * 0.75)],
            outline=(238, 216, 140, alpha_val),
            width=2
        )

    # Subtle Peacock Mandala geometric petals around the top medallion
    for angle_deg in range(0, 360, 15):
        rad = math.radians(angle_deg)
        x1 = cx + int(125 * math.cos(rad))
        y1 = 155 + int(125 * math.sin(rad))
        x2 = cx + int(220 * math.cos(rad))
        y2 = 155 + int(220 * math.sin(rad))
        odraw.line([x1, y1, x2, y2], fill=(212, 175, 55, 16), width=1)

    base_rgba = base_img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, overlay)
    return base_rgba.convert("RGB")

def draw_indri_luxury_borders(draw, width=1200, height=1800):
    """
    Draw the signature luxury 24k Gold double border with ornamental corner accents:
    - Outer thick gold border (#C5A034)
    - Inner hairline gold border (#9A7B24)
    - Corner royal diamond flourishes
    """
    gold_outer = (197, 160, 52)
    gold_inner = (165, 132, 42)
    gold_bright = (238, 216, 140)

    # Outer border (width=4) at 36px inset
    m1 = 36
    draw.rectangle([m1, m1, width - m1, height - m1], outline=gold_outer, width=4)

    # Inner border (width=1) at 52px inset
    m2 = 52
    draw.rectangle([m2, m2, width - m2, height - m2], outline=gold_inner, width=1)

    # Ornamental corner L-brackets & diamonds inside the frame
    c_len = 42
    for cx, cy, dx, dy in [
        (m2 + 10, m2 + 10, 1, 1),
        (width - m2 - 10, m2 + 10, -1, 1),
        (m2 + 10, height - m2 - 10, 1, -1),
        (width - m2 - 10, height - m2 - 10, -1, -1),
    ]:
        draw.line([cx, cy, cx + dx * c_len, cy], fill=gold_bright, width=2)
        draw.line([cx, cy, cx, cy + dy * c_len], fill=gold_bright, width=2)
        draw.polygon([(cx, cy - 5), (cx + 5, cy), (cx, cy + 5), (cx - 5, cy)], fill=gold_bright)

def draw_sparkle(draw, cx, cy, radius=12, color=(212, 175, 55)):
    """Draw a 4-point luxury star sparkle."""
    r_outer = radius
    r_inner = max(2, int(radius * 0.28))
    pts = []
    for i in range(8):
        angle = i * (math.pi / 4.0) - (math.pi / 2.0)
        r = r_outer if i % 2 == 0 else r_inner
        px = cx + math.cos(angle) * r
        py = cy + math.sin(angle) * r
        pts.append((px, py))
    draw.polygon(pts, fill=color)

def draw_star_5pt(draw, cx, cy, radius=9, color=(212, 175, 55)):
    """Draw a crisp 5-pointed gold rating star."""
    r_outer = radius
    r_inner = radius * 0.42
    pts = []
    for i in range(10):
        angle = i * (math.pi / 5.0) - (math.pi / 2.0)
        r = r_outer if i % 2 == 0 else r_inner
        pts.append((cx + math.cos(angle) * r, cy + math.sin(angle) * r))
    draw.polygon(pts, fill=color)

def draw_5_stars_row(draw, start_x, cy, star_radius=8, spacing=20, color=(212, 165, 32)):
    """Draw a row of 5 gold stars."""
    for i in range(5):
        draw_star_5pt(draw, start_x + i * spacing, cy, radius=star_radius, color=color)

def draw_google_g_icon(draw, cx, cy, radius=14):
    """Draw a clean Google 'G' multi-color icon inside a white circle."""
    draw.ellipse([cx - radius - 3, cy - radius - 3, cx + radius + 3, cy + radius + 3], fill=(255, 255, 255))
    bbox = [cx - radius, cy - radius, cx + radius, cy + radius]
    draw.pieslice(bbox, 220, 325, fill=(234, 67, 53))   # Red top
    draw.pieslice(bbox, 135, 220, fill=(251, 188, 5))   # Yellow left
    draw.pieslice(bbox, 45, 135, fill=(52, 168, 83))    # Green bottom
    draw.pieslice(bbox, 345, 45, fill=(66, 133, 244))   # Blue right
    inner_r = int(radius * 0.56)
    draw.ellipse([cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r], fill=(255, 255, 255))
    draw.rectangle([cx, cy - int(radius * 0.22), cx + radius, cy + int(radius * 0.24)], fill=(66, 133, 244))

def draw_instagram_icon(draw, cx, cy, size=26):
    """Draw a clean Instagram camera glyph."""
    half = size // 2
    draw.rounded_rectangle(
        [cx - half, cy - half, cx + half, cy + half],
        radius=7,
        fill=(214, 41, 118),
        outline=(255, 255, 255),
        width=2
    )
    r_lens = int(size * 0.24)
    draw.ellipse([cx - r_lens, cy - r_lens, cx + r_lens, cy + r_lens], outline=(255, 255, 255), width=2)
    draw.ellipse([cx + half - 7, cy - half + 4, cx + half - 4, cy - half + 7], fill=(255, 255, 255))

def generate_styled_qr(url, box_size=16, border=2, fill_color=(18, 18, 18), back_color=(255, 255, 255)):
    """Generate a high-contrast, ultra-scannable QR code image."""
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGBA")
    return img

def draw_brand_header(canvas, draw, w=1200):
    """
    Draw the Shree Kripa Midway Restaurant Header:
    1. 24k Gold Rim Circular SK Logo Medallion
    2. Official Hindi 'श्री कृपा' Calligraphy with Golden Bansuri Flute & Mor Pankh (Peacock Feather)
    3. 'MIDWAY RESTAURANT' in 24k Brushed Gold
    4. 'PURE VEG • RAU, NH 3, INDORE' in crisp white
    5. Ornamental 24k Gold Divider with Central Diamond
    """
    # 1. Circular SK Logo with 24k Gold Rim
    logo_path = "logo_with_gold_rim.png" if os.path.exists("logo_with_gold_rim.png") else "logo.png"
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        logo_size = 205
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        canvas.paste(logo, (int((w - logo_size) / 2), 54), mask=logo)

    # 2. Official Hindi 'श्री कृपा' Calligraphy with Golden Flute & Peacock Feather
    hindi_path = "shree_kripa_hindi_title.png"
    if os.path.exists(hindi_path):
        hindi_img = Image.open(hindi_path).convert("RGBA")
        target_w = 570
        target_h = int(hindi_img.size[1] * (target_w / hindi_img.size[0]))
        hindi_img = hindi_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        hx = int((w - target_w) / 2) + 12
        hy = 208
        canvas.paste(hindi_img, (hx, hy), mask=hindi_img)

    # 3. 'MIDWAY RESTAURANT' in 24k Champagne Gold
    font_midway = get_font(36, bold=True)
    midway_text = "M I D W A Y   R E S T A U R A N T"
    bbox = draw.textbbox((0, 0), midway_text, font=font_midway)
    draw.text(((w - (bbox[2] - bbox[0])) / 2, 448), midway_text, fill=(242, 216, 135), font=font_midway)

    # 4. Subtitle: PURE VEG • RAU, NH 3, INDORE
    font_sub = get_font(23, bold=True)
    sub_text = "100% PURE VEG  •  RAU, NH 3, INDORE"
    bbox = draw.textbbox((0, 0), sub_text, font=font_sub)
    draw.text(((w - (bbox[2] - bbox[0])) / 2, 498), sub_text, fill=(255, 255, 255), font=font_sub)

    # 5. Gold Divider Line + Central Diamond
    div_y = 544
    draw.line([200, div_y, w - 200, div_y], fill=(197, 160, 52), width=2)
    draw.polygon([(w // 2, div_y - 7), (w // 2 + 7, div_y), (w // 2, div_y + 7), (w // 2 - 7, div_y)], fill=(242, 216, 135))

def draw_footer(canvas, draw, w=1200):
    """
    Draw the La Indri-style Bottom Address & Phone Box + Gold Sparkle Thank-You Footer
    over a rich dark Peacock-Teal glass panel.
    """
    font_addr = get_font(22, bold=False)
    font_phone = get_font(27, bold=True)
    font_thanks = get_font(28, bold=False, italic=True, serif=True)

    info_x1, info_y1 = 115, 1525
    info_x2, info_y2 = w - 115, 1658

    glass = Image.new("RGBA", (w, 1800), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glass)
    gdraw.rounded_rectangle(
        [info_x1, info_y1, info_x2, info_y2],
        radius=12,
        fill=(4, 24, 29, 220),
        outline=(197, 160, 52, 255),
        width=2
    )
    canvas_rgba = canvas.convert("RGBA")
    canvas_rgba = Image.alpha_composite(canvas_rgba, glass)
    canvas.paste(canvas_rgba.convert("RGB"))

    addr_text = "Near Maharana Pratap Bridge, Pigdamber, Rau, NH 3, Indore"
    bbox = draw.textbbox((0, 0), addr_text, font=font_addr)
    draw.text(((w - (bbox[2] - bbox[0])) / 2, info_y1 + 24), addr_text, fill=(235, 242, 242), font=font_addr)

    phone_text = "Call / Reservation: 91110 30307"
    bbox = draw.textbbox((0, 0), phone_text, font=font_phone)
    draw.text(((w - (bbox[2] - bbox[0])) / 2, info_y1 + 70), phone_text, fill=(242, 216, 135), font=font_phone)

    thanks_text = "Thank you for dining with us!"
    bbox = draw.textbbox((0, 0), thanks_text, font=font_thanks)
    tw = bbox[2] - bbox[0]
    tx = (w - tw) / 2
    ty = 1692
    draw.text((tx, ty), thanks_text, fill=(238, 216, 140), font=font_thanks)

    draw_sparkle(draw, tx - 32, ty + 16, radius=11, color=(238, 216, 140))
    draw_sparkle(draw, tx + tw + 32, ty + 16, radius=11, color=(238, 216, 140))

def build_hub_standee(config, output_filenames=["table_standee_printable.png", "standee_front_printable.png"]):
    """
    Generate the 300 DPI Primary Table Standee matching La Indri's exact layout,
    customized with Shree Kripa's Hindi 'श्री कृपा' calligraphy and Peacock Teal & Warm Gold Ambience.
    """
    w, h = 1200, 1800
    canvas = create_ambience_luxury_background(w, h)
    draw = ImageDraw.Draw(canvas)
    draw_indri_luxury_borders(draw, w, h)
    draw_brand_header(canvas, draw, w)

    font_cta = get_font(46, bold=True)
    font_pill = get_font(22, bold=True)

    cta_text = "SCAN TO CONNECT"
    bbox = draw.textbbox((0, 0), cta_text, font=font_cta)
    draw.text(((w - (bbox[2] - bbox[0])) / 2, 570), cta_text, fill=(255, 255, 255), font=font_cta)

    pill_y = 642
    pill_h = 52
    pill_w_g = 255
    pill_w_i = 215
    gap = 24
    total_pills_w = pill_w_g + gap + pill_w_i
    start_x = int((w - total_pills_w) / 2)

    gx1, gy1 = start_x, pill_y
    gx2, gy2 = gx1 + pill_w_g, pill_y + pill_h
    draw.rounded_rectangle([gx1, gy1, gx2, gy2], radius=26, fill=(6, 38, 45), outline=(212, 175, 55), width=2)
    draw_google_g_icon(draw, gx1 + 32, gy1 + pill_h // 2, radius=13)
    draw.text((gx1 + 58, gy1 + 13), "Google Review", fill=(255, 255, 255), font=font_pill)

    ix1, iy1 = gx2 + gap, pill_y
    ix2, iy2 = ix1 + pill_w_i, pill_y + pill_h
    draw.rounded_rectangle([ix1, iy1, ix2, iy2], radius=26, fill=(6, 38, 45), outline=(212, 175, 55), width=2)
    draw_instagram_icon(draw, ix1 + 34, iy1 + pill_h // 2, size=24)
    draw.text((ix1 + 58, iy1 + 13), "Instagram", fill=(255, 255, 255), font=font_pill)

    qr_url = config.get("landingPageUrl", "https://hospitalityqr.github.io/Shree-Kripa-Midway-Restaurant-google-instagram-qr/")
    qr_img = generate_styled_qr(qr_url, box_size=18, border=2, fill_color=(12, 24, 28))

    card_size = 720
    qr_size = 640
    qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)

    card_x = int((w - card_size) / 2)
    card_y = 735

    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow_layer)
    sdraw.rounded_rectangle(
        [card_x - 4, card_y + 8, card_x + card_size + 4, card_y + card_size + 16],
        radius=28,
        fill=(0, 0, 0, 125)
    )
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=16))
    canvas_rgba = Image.alpha_composite(canvas.convert("RGBA"), shadow_layer)
    canvas = canvas_rgba.convert("RGB")
    draw = ImageDraw.Draw(canvas)

    draw.rounded_rectangle(
        [card_x, card_y, card_x + card_size, card_y + card_size],
        radius=26,
        fill=(255, 255, 255),
        outline=(197, 160, 52),
        width=4
    )
    canvas.paste(qr_img, (card_x + (card_size - qr_size) // 2, card_y + (card_size - qr_size) // 2))

    draw_footer(canvas, draw, w)

    for fn in output_filenames:
        canvas.save(fn, quality=95, dpi=(300, 300))
        print(f"[OK] Generated {fn} (300 DPI)")

def build_dual_direct_standee(config, output_filename="standee_dual_direct_static.png"):
    """
    Generate 300 DPI Dual Direct Static Standee (Left QR -> Google Review, Right QR -> Instagram)
    with Hindi 'श्री कृपा' calligraphy and Peacock Teal & Warm Gold Ambience.
    """
    w, h = 1200, 1800
    canvas = create_ambience_luxury_background(w, h)
    draw = ImageDraw.Draw(canvas)
    draw_indri_luxury_borders(draw, w, h)
    draw_brand_header(canvas, draw, w)

    font_cta = get_font(42, bold=True)
    font_sub_cta = get_font(23, bold=True)
    font_card_head = get_font(26, bold=True)
    font_card_sub = get_font(20, bold=True)
    font_feature_title = get_font(25, bold=True)
    font_feature_item = get_font(22, bold=False)

    cta_text = "SCAN TO CONNECT DIRECTLY"
    bbox = draw.textbbox((0, 0), cta_text, font=font_cta)
    draw.text(((w - (bbox[2] - bbox[0])) / 2, 568), cta_text, fill=(255, 255, 255), font=font_cta)

    sub_cta = "Point Your Camera Directly At Either QR Below  •  Instant Open"
    bbox = draw.textbbox((0, 0), sub_cta, font=font_sub_cta)
    draw.text(((w - (bbox[2] - bbox[0])) / 2, 624), sub_cta, fill=(242, 216, 135), font=font_sub_cta)

    google_url = config.get("googleReviewUrl", "https://share.google/MwO49jjEmQJTSvkte")
    insta_url = config.get("instagramUrl", "https://www.instagram.com/shree_kripa_restaurant?stkn=YjdsMzlvMTNlc3dz")

    qr_g = generate_styled_qr(google_url, box_size=14, border=2, fill_color=(12, 24, 28)).resize((410, 410), Image.Resampling.LANCZOS)
    qr_i = generate_styled_qr(insta_url, box_size=14, border=2, fill_color=(12, 24, 28)).resize((410, 410), Image.Resampling.LANCZOS)

    card_w, card_h = 475, 585
    left_x = 100
    right_x = w - 100 - card_w
    cards_y = 678

    # Left Card: Google Review
    draw.rounded_rectangle([left_x, cards_y, left_x + card_w, cards_y + card_h], radius=24, fill=(255, 255, 255), outline=(197, 160, 52), width=4)
    draw.rounded_rectangle([left_x + 28, cards_y + 20, left_x + card_w - 28, cards_y + 74], radius=27, fill=(6, 42, 49), outline=(197, 160, 52), width=2)
    draw_google_g_icon(draw, left_x + 68, cards_y + 47, radius=14)
    draw.text((left_x + 100, cards_y + 32), "GOOGLE REVIEW", fill=(255, 255, 255), font=font_card_head)
    canvas.paste(qr_g, (left_x + (card_w - 410) // 2, cards_y + 92))
    # Draw 5 vector gold stars + RATE US ON GOOGLE
    draw_5_stars_row(draw, left_x + 76, cards_y + 533, star_radius=8, spacing=20, color=(218, 165, 32))
    draw.text((left_x + 182, cards_y + 522), "RATE US ON GOOGLE", fill=(8, 52, 60), font=font_card_sub)

    # Right Card: Instagram
    draw.rounded_rectangle([right_x, cards_y, right_x + card_w, cards_y + card_h], radius=24, fill=(255, 255, 255), outline=(197, 160, 52), width=4)
    draw.rounded_rectangle([right_x + 28, cards_y + 20, right_x + card_w - 28, cards_y + 74], radius=27, fill=(6, 42, 49), outline=(197, 160, 52), width=2)
    draw_instagram_icon(draw, right_x + 76, cards_y + 47, size=26)
    draw.text((right_x + 112, cards_y + 32), "INSTAGRAM", fill=(255, 255, 255), font=font_card_head)
    canvas.paste(qr_i, (right_x + (card_w - 410) // 2, cards_y + 92))
    i_foot = "FOLLOW @SHREE_KRIPA_RESTAURANT"
    bbox = draw.textbbox((0, 0), i_foot, font=font_card_sub)
    draw.text((right_x + (card_w - (bbox[2] - bbox[0])) / 2, cards_y + 522), i_foot, fill=(8, 52, 60), font=font_card_sub)

    # Luxury Hospitality Highlights Strip
    feat_x1, feat_y1 = 115, 1300
    feat_x2, feat_y2 = w - 115, 1488
    glass = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glass)
    gdraw.rounded_rectangle([feat_x1, feat_y1, feat_x2, feat_y2], radius=16, fill=(5, 30, 36, 215), outline=(197, 160, 52, 255), width=2)
    canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), glass).convert("RGB"))
    draw = ImageDraw.Draw(canvas)

    ft_head = "PURE DESI GHEE  •  ROYAL AMBIENCE  •  FAMILY DINING"
    bbox = draw.textbbox((0, 0), ft_head, font=font_feature_title)
    ft_w = bbox[2] - bbox[0]
    ft_x = (w - ft_w) / 2
    draw.text((ft_x, feat_y1 + 24), ft_head, fill=(242, 216, 135), font=font_feature_title)
    draw_sparkle(draw, ft_x - 28, feat_y1 + 37, radius=10, color=(242, 216, 135))
    draw_sparkle(draw, ft_x + ft_w + 28, feat_y1 + 37, radius=10, color=(242, 216, 135))

    ft_line1 = "100% Pure Vegetarian Preparation  •  Amul Butter & Fresh Pure Paneer"
    bbox = draw.textbbox((0, 0), ft_line1, font=font_feature_item)
    draw.text(((w - (bbox[2] - bbox[0])) / 2, feat_y1 + 78), ft_line1, fill=(255, 255, 255), font=font_feature_item)

    ft_line2 = "\"Ek Baar Khaiye, Baar-Baar Aaiye\"  —  Share Your Experience & Tag Us!"
    bbox = draw.textbbox((0, 0), ft_line2, font=font_feature_item)
    draw.text(((w - (bbox[2] - bbox[0])) / 2, feat_y1 + 124), ft_line2, fill=(215, 232, 232), font=font_feature_item)

    draw_footer(canvas, draw, w)
    canvas.save(output_filename, quality=95, dpi=(300, 300))
    print(f"[OK] Generated {output_filename} (300 DPI)")

def build_single_direct_standee(config, url, mode="google", output_filename="standee_google_direct.png"):
    """
    Generate 300 DPI Single Direct Standee (Google Review Direct OR Instagram Direct)
    with Hindi 'श्री कृपा' calligraphy and Peacock Teal & Warm Gold Ambience.
    """
    w, h = 1200, 1800
    canvas = create_ambience_luxury_background(w, h)
    draw = ImageDraw.Draw(canvas)
    draw_indri_luxury_borders(draw, w, h)
    draw_brand_header(canvas, draw, w)

    font_cta = get_font(44, bold=True)
    font_pill = get_font(24, bold=True)

    if mode == "google":
        cta_text = "RATE US ON GOOGLE"
        pill_label = "Google Review  •  5-Star Rating"
    else:
        cta_text = "FOLLOW US ON INSTAGRAM"
        pill_label = "@shree_kripa_restaurant"

    bbox = draw.textbbox((0, 0), cta_text, font=font_cta)
    draw.text(((w - (bbox[2] - bbox[0])) / 2, 570), cta_text, fill=(255, 255, 255), font=font_cta)

    pill_w = 450
    pill_h = 54
    px1 = int((w - pill_w) / 2)
    py1 = 642
    draw.rounded_rectangle([px1, py1, px1 + pill_w, py1 + pill_h], radius=27, fill=(6, 38, 45), outline=(212, 175, 55), width=2)
    if mode == "google":
        draw_google_g_icon(draw, px1 + 38, py1 + pill_h // 2, radius=14)
    else:
        draw_instagram_icon(draw, px1 + 38, py1 + pill_h // 2, size=26)
    draw.text((px1 + 70, py1 + 13), pill_label, fill=(255, 255, 255), font=font_pill)

    qr_img = generate_styled_qr(url, box_size=18, border=2, fill_color=(12, 24, 28))
    card_size = 720
    qr_size = 640
    qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
    card_x = int((w - card_size) / 2)
    card_y = 735

    draw.rounded_rectangle(
        [card_x, card_y, card_x + card_size, card_y + card_size],
        radius=26,
        fill=(255, 255, 255),
        outline=(197, 160, 52),
        width=4
    )
    canvas.paste(qr_img, (card_x + (card_size - qr_size) // 2, card_y + (card_size - qr_size) // 2))

    draw_footer(canvas, draw, w)
    canvas.save(output_filename, quality=95, dpi=(300, 300))
    print(f"[OK] Generated {output_filename} (300 DPI)")

def main():
    config = load_config("config.js")
    landing_url = config.get("landingPageUrl", "https://hospitalityqr.github.io/Shree-Kripa-Midway-Restaurant-google-instagram-qr/")
    google_url = config.get("googleReviewUrl", "https://share.google/MwO49jjEmQJTSvkte")
    insta_url = config.get("instagramUrl", "https://www.instagram.com/shree_kripa_restaurant?stkn=YjdsMzlvMTNlc3dz")

    print("Generating standalone high-res QR codes...")
    qr_hub = generate_styled_qr(landing_url, box_size=18, border=2, fill_color=(12, 24, 28))
    qr_hub.save("qr_code.png")
    qr_hub.save("qr_landing_page.png")

    qr_google = generate_styled_qr(google_url, box_size=18, border=2, fill_color=(12, 24, 28))
    qr_google.save("qr_google_direct.png")

    qr_insta = generate_styled_qr(insta_url, box_size=18, border=2, fill_color=(12, 24, 28))
    qr_insta.save("qr_instagram_direct.png")
    print("[OK] Generated qr_code.png, qr_landing_page.png, qr_google_direct.png, qr_instagram_direct.png")

    build_hub_standee(config, ["table_standee_printable.png", "standee_front_printable.png"])
    build_dual_direct_standee(config, "standee_dual_direct_static.png")
    build_single_direct_standee(config, google_url, mode="google", output_filename="standee_google_direct.png")
    build_single_direct_standee(config, insta_url, mode="instagram", output_filename="standee_instagram_direct.png")

if __name__ == "__main__":
    main()
