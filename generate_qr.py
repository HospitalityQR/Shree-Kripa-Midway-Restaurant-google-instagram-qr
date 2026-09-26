"""
=============================================================================
🦚 SHREE KRIPA MIDWAY RESTAURANT - LUXURY QR CODE & 300 DPI STANDEE GENERATOR
=============================================================================
Architecture replicated from La Indri and elevated with ultra-premium styling:
- Multi-mode support: Dual-Link Landing Page, Direct Google Review, Direct Instagram
- True 300 DPI print-ready standees (table_standee_printable, standee_dual_direct_static, etc.)
- Deep Velvet Burgundy-Mahogany radial gradient background with subtle micro-texture
- Dual 24k brushed gold borders and bevelled medallion framing
=============================================================================
"""

import sys
import os
import re
import math
import numpy as np
import qrcode
from PIL import Image, ImageDraw, ImageFont

def load_config():
    config = {
        "restaurantName": "Shree Kripa",
        "subtitle": "Midway Restaurant",
        "tagline": "100% Pure Veg • Pigdamber, Rau • Indore",
        "qrMode": "dual_link",
        "landingPageUrl": "https://hospitalityqr.github.io/Shree-Kripa-Midway-Restaurant-google-instagram-qr/",
        "googleReviewLink": "https://share.google/MwO49jjEmQJTSvkte",
        "instagramLink": "https://www.instagram.com/shree_kripa_restaurant?stkn=YjdsMzlvMTNlc3dz",
        "instagramUsername": "@shree_kripa_restaurant",
        "phoneNumber": "9111030307",
        "phoneButtonText": "Call / Reservation: 91110 30307",
        "address": "Near Maharana Pratap Bridge, Pigdamber, Rau, NH 3, Indore",
        "shortAddress": "Near Maharana Pratap Bridge, Pigdamber, Rau, Indore",
        "footerThanks": "Thank You For Visiting Shree Kripa ✨"
    }
    if os.path.exists("config.js"):
        try:
            with open("config.js", "r", encoding="utf-8") as f:
                content = f.read()
            for key in config.keys():
                m = re.search(rf'{key}\s*:\s*["\']([^"\']+)["\']', content)
                if m:
                    config[key] = m.group(1)
        except Exception as e:
            print("Notice: Could not parse config.js, using defaults:", e)
    return config

def create_luxury_burgundy_background(w, h):
    """
    Generate exact luxury gradient:
    Top: #3B0712 (59, 7, 18) deep burgundy-mahogany
    Bottom: #1A090C (26, 9, 12) dark velvet mahogany-brown
    Very subtle warm radial glow behind logo at cx=w/2, cy=180
    """
    y, x = np.ogrid[:h, :w]
    t = (y / float(h)).astype(np.float32)[..., None]

    c_top = np.array([59, 7, 18], dtype=np.float32)
    c_bot = np.array([26, 9, 12], dtype=np.float32)
    base_grad = c_top * (1.0 - t) + c_bot * t
    img_arr = np.broadcast_to(base_grad, (h, w, 3)).copy()

    # Subtle warm radial glow behind logo
    cx, cy = w / 2.0, 180.0
    dist_logo = np.sqrt((x - cx)**2 + (y - cy)**2)
    r_glow = 400.0
    glow_mask = np.clip(1.0 - (dist_logo / r_glow), 0.0, 1.0) ** 2
    glow_arr = np.array([32, 12, 10], dtype=np.float32)
    img_arr += glow_mask[..., None] * glow_arr

    # Subtle velvet micro-texture
    np.random.seed(42)
    noise = np.random.normal(0, 1.2, (h, w, 1))
    img_arr = np.clip(img_arr + noise, 0, 255).astype(np.uint8)

    return Image.fromarray(img_arr, mode="RGB")

def draw_gold_sparkle(draw, cx, cy, size, fill_color):
    """Draw a refined luxury gold 4-point sparkle star"""
    r = size
    r_in = size * 0.28
    pts = [
        (cx, cy - r), (cx + r_in, cy - r_in),
        (cx + r, cy), (cx + r_in, cy + r_in),
        (cx, cy + r), (cx - r_in, cy + r_in),
        (cx - r, cy), (cx - r_in, cy - r_in)
    ]
    draw.polygon(pts, fill=fill_color)

def make_qr_image(url, fill_color="#000000", back_color="#ffffff", box_size=20):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=3,
    )
    qr.add_data(url)
    qr.make(fit=True)
    return qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")

def get_fonts():
    try:
        brand_font = ImageFont.truetype("arialbd.ttf", 48)
        instruction_font = ImageFont.truetype("arialbd.ttf", 44)
        sub_font = ImageFont.truetype("arial.ttf", 25)
        badge_font = ImageFont.truetype("arialbd.ttf", 23)
        addr1_font = ImageFont.truetype("arialbd.ttf", 31)
        addr2_font = ImageFont.truetype("arial.ttf", 26)
        phone_font = ImageFont.truetype("arialbd.ttf", 36)
        thanks_font = ImageFont.truetype("georgiai.ttf", 34)
    except Exception:
        brand_font = ImageFont.load_default()
        instruction_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        badge_font = ImageFont.load_default()
        addr1_font = ImageFont.load_default()
        addr2_font = ImageFont.load_default()
        phone_font = ImageFont.load_default()
        thanks_font = ImageFont.load_default()
    return brand_font, instruction_font, sub_font, badge_font, addr1_font, addr2_font, phone_font, thanks_font

def generate_all_assets():
    cfg = load_config()
    print(f"[*] Generating assets for {cfg['restaurantName']} (Mode: {cfg['qrMode']})...")

    # 1. Base QR Codes
    landing_url = cfg["landingPageUrl"]
    google_url = cfg["googleReviewLink"]
    insta_url = cfg["instagramLink"]

    img_landing = make_qr_image(landing_url, fill_color="#000000")
    img_landing.save("qr_landing_page.png", "PNG")

    img_google = make_qr_image(google_url, fill_color="#000000")
    img_google.save("qr_google_direct.png", "PNG")

    img_insta = make_qr_image(insta_url, fill_color="#000000")
    img_insta.save("qr_instagram_direct.png", "PNG")

    img_lux = make_qr_image(landing_url, fill_color="#000000")
    img_lux.save("qr_luxury.png", "PNG")

    mode = cfg.get("qrMode", "dual_link").lower()
    if mode == "google_only":
        primary_qr = img_google
        primary_inst = "RATE US ON GOOGLE"
        primary_badge_ico = "google_icon.png"
        primary_badge_txt = "Google 5-Star Reviews"
    elif mode == "insta_only":
        primary_qr = img_insta
        primary_inst = "FOLLOW US ON INSTAGRAM"
        primary_badge_ico = "instagram_icon.png"
        primary_badge_txt = "Follow @shree_kripa_restaurant"
    else:  # "dual_link"
        primary_qr = img_landing
        primary_inst = "SCAN TO CONNECT"
        primary_badge_ico = None
        primary_badge_txt = "Google Reviews • Instagram"

    primary_qr.save("qr_code.png", "PNG")
    primary_qr.save("qr_standard.png", "PNG")

    # 2. Primary Standee (table_standee_printable.png)
    if mode == "dual_link":
        generate_dual_link_standee(primary_qr, cfg)
    else:
        generate_single_direct_standee(
            primary_qr,
            title=primary_inst,
            tagline=cfg["tagline"],
            badge_icon=primary_badge_ico,
            badge_text=primary_badge_txt,
            out_filenames=["table_standee_printable.png", "front_page_standee.png"]
        )

    # 3. Dual Direct Static Standee (Google Left, Instagram Right)
    generate_dual_standee_card(img_google, img_insta, cfg)

    # 4. Dedicated Google Standee
    generate_single_direct_standee(
        img_google,
        title="RATE US ON GOOGLE",
        tagline="SHARE YOUR 5-STAR EXPERIENCE",
        badge_icon="google_icon.png",
        badge_text="Google 5-Star Reviews",
        out_filenames=["standee_google_direct.png"]
    )

    # 5. Dedicated Instagram Standee
    generate_single_direct_standee(
        img_insta,
        title="FOLLOW US ON INSTAGRAM",
        tagline="@SHREE_KRIPA_RESTAURANT • PURE VEG & REELS",
        badge_icon="instagram_icon.png",
        badge_text="Follow on Instagram",
        out_filenames=["standee_instagram_direct.png"]
    )

    print("  [+] All 300 DPI Standees and QR codes generated with ultra-premium styling successfully!")

def generate_single_direct_standee(qr_img, title, tagline, badge_icon, badge_text, out_filenames):
    cfg = load_config()
    w, h = 1200, 1800
    
    standee = create_luxury_burgundy_background(w, h)
    draw = ImageDraw.Draw(standee)

    # 1. Thin, subtle satin gold double border
    border_margin = 42
    draw.rectangle([border_margin, border_margin, w - border_margin, h - border_margin], outline="#c5a034", width=2)
    draw.rectangle([border_margin + 8, border_margin + 8, w - border_margin - 8, h - border_margin - 8], outline="#dfc476", width=1)

    brand_font, instruction_font, sub_font, badge_font, addr1_font, addr2_font, phone_font, thanks_font = get_fonts()

    # 2. Header: Logo Medallion (Prominent 250x250)
    logo_file = "logo_with_gold_rim.png" if os.path.exists("logo_with_gold_rim.png") else "logo.png"
    if os.path.exists(logo_file):
        logo = Image.open(logo_file).convert("RGBA").resize((250, 250), Image.Resampling.LANCZOS)
        standee.paste(logo, ((w - 250) // 2, 65), logo)

    # 3. Brand Title: GOLD
    name_display = f"{cfg.get('restaurantName', 'SHREE KRIPA').upper()} MIDWAY RESTAURANT"
    nb = draw.textbbox((0, 0), name_display, font=brand_font)
    draw.text(((w - (nb[2] - nb[0])) // 2, 330), name_display, fill="#eed88c", font=brand_font)

    # 4. Location Subtitle: WHITE
    tb2 = draw.textbbox((0, 0), tagline, font=sub_font)
    draw.text(((w - (tb2[2] - tb2[0])) // 2, 390), tagline, fill="#ffffff", font=sub_font)

    # 5. Instruction Title: WHITE
    ib = draw.textbbox((0, 0), title, font=instruction_font)
    draw.text(((w - (ib[2] - ib[0])) // 2, 445), title, fill="#ffffff", font=instruction_font)

    # 6. Clean Pill Badge
    bb = draw.textbbox((0, 0), badge_text, font=badge_font)
    b_w = (bb[2] - bb[0]) + 76
    b_h = 56
    b_x = (w - b_w) // 2
    b_y = 510
    draw.rounded_rectangle([b_x, b_y, b_x + b_w, b_y + b_h], radius=28, fill="#2a0a12", outline="#c5a034", width=1)
    if badge_icon and os.path.exists(badge_icon):
        ico = Image.open(badge_icon).convert("RGBA").resize((34, 34), Image.Resampling.LANCZOS)
        standee.paste(ico, (b_x + 16, b_y + 11), ico)
    draw.text((b_x + 64, b_y + 14), badge_text, fill="#ffffff", font=badge_font)

    # 7. Big Direct QR Card with balanced white quiet zone
    qr_card_size = 700
    qr_card_x = (w - qr_card_size) // 2
    qr_card_y = 593
    margin_pad = 14
    qr_size = qr_card_size - 2 * margin_pad
    draw.rounded_rectangle(
        [qr_card_x, qr_card_y, qr_card_x + qr_card_size, qr_card_y + qr_card_size],
        radius=30, fill="#ffffff", outline="#c5a034", width=2
    )
    qr_resized = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
    standee.paste(qr_resized, (qr_card_x + margin_pad, qr_card_y + margin_pad))

    # 8. Address + Phone Framed in Thin Gold Box
    box_w = 980
    box_h = 176
    box_x = (w - box_w) // 2
    box_y = 1345
    draw.rounded_rectangle(
        [box_x, box_y, box_x + box_w, box_y + box_h],
        radius=20, fill=None, outline="#c5a034", width=2
    )

    addr_line1 = "Shree Kripa Midway Restaurant,"
    addr_line2 = "Near Maharana Pratap Bridge, Pigdamber, Rau, Indore"
    phone_text = cfg.get("phoneButtonText", "Call / Reservation: 91110 30307")

    # Address lines in WHITE
    a1_b = draw.textbbox((0, 0), addr_line1, font=addr1_font)
    draw.text(((w - (a1_b[2] - a1_b[0])) // 2, box_y + 18), addr_line1, fill="#ffffff", font=addr1_font)

    a2_b = draw.textbbox((0, 0), addr_line2, font=addr2_font)
    draw.text(((w - (a2_b[2] - a2_b[0])) // 2, box_y + 60), addr_line2, fill="#ffffff", font=addr2_font)

    # Phone line in GOLD & BOLD
    pb = draw.textbbox((0, 0), phone_text, font=phone_font)
    draw.text(((w - (pb[2] - pb[0])) // 2, box_y + 108), phone_text, fill="#eed88c", font=phone_font)

    # 9. Bottom Thanks with Gold Sparkles
    thanks_text = "Thank You For Visiting Shree Kripa"
    thb = draw.textbbox((0, 0), thanks_text, font=thanks_font)
    tw = thb[2] - thb[0]
    tx = (w - tw) // 2
    draw.text((tx, 1545), thanks_text, fill="#eed88c", font=thanks_font)
    draw_gold_sparkle(draw, tx - 24, 1561, 9, "#c5a034")
    draw_gold_sparkle(draw, tx + tw + 24, 1561, 9, "#c5a034")

    for fn in out_filenames:
        standee.save(fn, "PNG", dpi=(300, 300))

def generate_dual_link_standee(qr_img, cfg):
    w, h = 1200, 1800
    standee = create_luxury_burgundy_background(w, h)
    draw = ImageDraw.Draw(standee)

    # 1. Thin, subtle satin gold double border
    border_margin = 42
    draw.rectangle([border_margin, border_margin, w - border_margin, h - border_margin], outline="#c5a034", width=2)
    draw.rectangle([border_margin + 8, border_margin + 8, w - border_margin - 8, h - border_margin - 8], outline="#dfc476", width=1)

    brand_font, instruction_font, sub_font, badge_font, addr1_font, addr2_font, phone_font, thanks_font = get_fonts()

    # 2. Header: Logo Medallion
    logo_file = "logo_with_gold_rim.png" if os.path.exists("logo_with_gold_rim.png") else "logo.png"
    if os.path.exists(logo_file):
        logo = Image.open(logo_file).convert("RGBA").resize((250, 250), Image.Resampling.LANCZOS)
        standee.paste(logo, ((w - 250) // 2, 65), logo)

    # 3. Brand Title: GOLD
    name_display = f"{cfg.get('restaurantName', 'SHREE KRIPA').upper()} MIDWAY RESTAURANT"
    nb = draw.textbbox((0, 0), name_display, font=brand_font)
    draw.text(((w - (nb[2] - nb[0])) // 2, 330), name_display, fill="#eed88c", font=brand_font)

    # 4. Location Subtitle: WHITE
    tag_text = cfg.get("tagline", "100% Pure Veg • Pigdamber, Rau • Indore").replace("*", "•")
    tb2 = draw.textbbox((0, 0), tag_text, font=sub_font)
    draw.text(((w - (tb2[2] - tb2[0])) // 2, 390), tag_text, fill="#ffffff", font=sub_font)

    # 5. Instruction Title: WHITE
    inst_text = "SCAN TO CONNECT"
    ib = draw.textbbox((0, 0), inst_text, font=instruction_font)
    draw.text(((w - (ib[2] - ib[0])) // 2, 445), inst_text, fill="#ffffff", font=instruction_font)

    # 6. Badges for Google and Instagram side-by-side
    g_text = "Rate Us on Google"
    i_text = "Follow Us on Instagram"
    gb_box = draw.textbbox((0, 0), g_text, font=badge_font)
    g_badge_w = (gb_box[2] - gb_box[0]) + 68 + 20
    g_badge_h = 56

    ib_box = draw.textbbox((0, 0), i_text, font=badge_font)
    i_badge_w = (ib_box[2] - ib_box[0]) + 68 + 20
    i_badge_h = 56

    gap = 18
    total_badges_w = g_badge_w + i_badge_w + gap
    start_badges_x = (w - total_badges_w) // 2
    badges_y = 510

    # Badge 1: Google
    draw.rounded_rectangle(
        [start_badges_x, badges_y, start_badges_x + g_badge_w, badges_y + g_badge_h],
        radius=28, fill="#2a0a12", outline="#c5a034", width=1
    )
    if os.path.exists("google_icon.png"):
        g_ico = Image.open("google_icon.png").convert("RGBA").resize((34, 34), Image.Resampling.LANCZOS)
        standee.paste(g_ico, (start_badges_x + 16, badges_y + 11), g_ico)
    draw.text((start_badges_x + 64, badges_y + 14), g_text, fill="#ffffff", font=badge_font)

    # Badge 2: Instagram
    insta_x = start_badges_x + g_badge_w + gap
    draw.rounded_rectangle(
        [insta_x, badges_y, insta_x + i_badge_w, badges_y + i_badge_h],
        radius=28, fill="#2a0a12", outline="#c5a034", width=1
    )
    if os.path.exists("instagram_icon.png"):
        i_ico = Image.open("instagram_icon.png").convert("RGBA").resize((34, 34), Image.Resampling.LANCZOS)
        standee.paste(i_ico, (insta_x + 16, badges_y + 11), i_ico)
    draw.text((insta_x + 64, badges_y + 14), i_text, fill="#ffffff", font=badge_font)

    # 7. Main QR Card with balanced white quiet zone
    qr_card_size = 700
    qr_card_x = (w - qr_card_size) // 2
    qr_card_y = 593
    margin_pad = 14
    qr_size = qr_card_size - 2 * margin_pad
    draw.rounded_rectangle(
        [qr_card_x, qr_card_y, qr_card_x + qr_card_size, qr_card_y + qr_card_size],
        radius=30, fill="#ffffff", outline="#c5a034", width=2
    )
    qr_resized = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
    standee.paste(qr_resized, (qr_card_x + margin_pad, qr_card_y + margin_pad))

    # 8. Address + Phone Framed in Thin Gold Box
    box_w = 980
    box_h = 176
    box_x = (w - box_w) // 2
    box_y = 1345
    draw.rounded_rectangle(
        [box_x, box_y, box_x + box_w, box_y + box_h],
        radius=20, fill=None, outline="#c5a034", width=2
    )

    addr_line1 = "Shree Kripa Midway Restaurant,"
    addr_line2 = "Near Maharana Pratap Bridge, Pigdamber, Rau, Indore"
    phone_text = cfg.get("phoneButtonText", "Call / Reservation: 91110 30307")

    # Address lines in WHITE
    a1_b = draw.textbbox((0, 0), addr_line1, font=addr1_font)
    draw.text(((w - (a1_b[2] - a1_b[0])) // 2, box_y + 18), addr_line1, fill="#ffffff", font=addr1_font)

    a2_b = draw.textbbox((0, 0), addr_line2, font=addr2_font)
    draw.text(((w - (a2_b[2] - a2_b[0])) // 2, box_y + 60), addr_line2, fill="#ffffff", font=addr2_font)

    # Phone line in GOLD & BOLD
    pb = draw.textbbox((0, 0), phone_text, font=phone_font)
    draw.text(((w - (pb[2] - pb[0])) // 2, box_y + 108), phone_text, fill="#eed88c", font=phone_font)

    # 9. Bottom Thanks with Gold Sparkles
    thanks_text = "Thank You For Visiting Shree Kripa"
    thb = draw.textbbox((0, 0), thanks_text, font=thanks_font)
    tw = thb[2] - thb[0]
    tx = (w - tw) // 2
    draw.text((tx, 1545), thanks_text, fill="#eed88c", font=thanks_font)
    draw_gold_sparkle(draw, tx - 24, 1561, 9, "#c5a034")
    draw_gold_sparkle(draw, tx + tw + 24, 1561, 9, "#c5a034")

    standee.save("table_standee_printable.png", "PNG", dpi=(300, 300))
    standee.save("front_page_standee.png", "PNG", dpi=(300, 300))

def generate_dual_standee_card(img_google, img_insta, cfg):
    w, h = 1400, 1800
    standee = create_luxury_burgundy_background(w, h)
    draw = ImageDraw.Draw(standee)

    # Thin, subtle satin gold double border
    draw.rectangle([40, 40, w - 40, h - 40], outline="#c5a034", width=2)
    draw.rectangle([48, 48, w - 48, h - 48], outline="#dfc476", width=1)

    try:
        title_font = ImageFont.truetype("arialbd.ttf", 54)
        sub_font = ImageFont.truetype("arial.ttf", 25)
        box_title_font = ImageFont.truetype("arialbd.ttf", 34)
        box_sub_font = ImageFont.truetype("arial.ttf", 23)
        addr1_font = ImageFont.truetype("arialbd.ttf", 31)
        addr2_font = ImageFont.truetype("arial.ttf", 26)
        phone_font = ImageFont.truetype("arialbd.ttf", 36)
        thanks_font = ImageFont.truetype("georgiai.ttf", 34)
    except Exception:
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        box_title_font = ImageFont.load_default()
        box_sub_font = ImageFont.load_default()
        addr1_font = ImageFont.load_default()
        addr2_font = ImageFont.load_default()
        phone_font = ImageFont.load_default()
        thanks_font = ImageFont.load_default()

    logo_file = "logo_with_gold_rim.png" if os.path.exists("logo_with_gold_rim.png") else "logo.png"
    if os.path.exists(logo_file):
        logo = Image.open(logo_file).convert("RGBA").resize((200, 200), Image.Resampling.LANCZOS)
        standee.paste(logo, ((w - 200) // 2, 55), logo)

    title = f"{cfg.get('restaurantName', 'SHREE KRIPA').upper()} MIDWAY RESTAURANT"
    tb = draw.textbbox((0, 0), title, font=title_font)
    draw.text(((w - (tb[2] - tb[0])) // 2, 270), title, fill="#eed88c", font=title_font)

    sub = "100% PURE VEG • PIGDAMBER, RAU • INDORE"
    sb = draw.textbbox((0, 0), sub, font=sub_font)
    draw.text(((w - (sb[2] - sb[0])) // 2, 342), sub, fill="#ffffff", font=sub_font)

    card_w, card_h = 560, 830
    y_pos = 400

    # Google Column (Left)
    x_g = 105
    draw.rounded_rectangle([x_g, y_pos, x_g + card_w, y_pos + card_h], radius=24, fill="#320e17", outline="#c5a034", width=2)
    g_title = "RATE US 5-STARS"
    gt_b = draw.textbbox((0, 0), g_title, font=box_title_font)
    draw.text((x_g + (card_w - (gt_b[2] - gt_b[0])) // 2, y_pos + 30), g_title, fill="#ffffff", font=box_title_font)
    g_sub = "Google Reviews"
    gs_b = draw.textbbox((0, 0), g_sub, font=box_sub_font)
    draw.text((x_g + (card_w - (gs_b[2] - gs_b[0])) // 2, y_pos + 74), g_sub, fill="#eed88c", font=box_sub_font)

    qr_box_size = 450
    qr_x_g = x_g + (card_w - qr_box_size) // 2
    margin_dual = 16
    qr_inner_dual = qr_box_size - 2 * margin_dual
    draw.rounded_rectangle([qr_x_g, y_pos + 125, qr_x_g + qr_box_size, y_pos + 125 + qr_box_size], radius=20, fill="#ffffff", outline="#c5a034", width=2)
    qr_g_resized = img_google.resize((qr_inner_dual, qr_inner_dual), Image.Resampling.LANCZOS)
    standee.paste(qr_g_resized, (qr_x_g + margin_dual, y_pos + 125 + margin_dual))

    # Google badge pill
    draw.rounded_rectangle([x_g + 80, y_pos + 615, x_g + card_w - 80, y_pos + 675], radius=30, fill="#22060d", outline="#c5a034", width=1)
    if os.path.exists("google_icon.png"):
        g_ico = Image.open("google_icon.png").convert("RGBA").resize((32, 32), Image.Resampling.LANCZOS)
        standee.paste(g_ico, (x_g + 95, y_pos + 634), g_ico)
    g_lbl = "Google Reviews"
    draw.text((x_g + 145, y_pos + 633), g_lbl, fill="#ffffff", font=box_sub_font)

    g_btn = "Scan to Rate 5 Stars on Google"
    gbtn_b = draw.textbbox((0, 0), g_btn, font=box_sub_font)
    draw.text((x_g + (card_w - (gbtn_b[2] - gbtn_b[0])) // 2, y_pos + 725), g_btn, fill="#eed88c", font=box_sub_font)

    # Instagram Column (Right)
    x_i = 735
    draw.rounded_rectangle([x_i, y_pos, x_i + card_w, y_pos + card_h], radius=24, fill="#320e17", outline="#c5a034", width=2)
    i_title = "FOLLOW US"
    it_b = draw.textbbox((0, 0), i_title, font=box_title_font)
    draw.text((x_i + (card_w - (it_b[2] - it_b[0])) // 2, y_pos + 30), i_title, fill="#ffffff", font=box_title_font)
    i_sub = cfg.get("instagramUsername", "@shree_kripa_restaurant")
    is_b = draw.textbbox((0, 0), i_sub, font=box_sub_font)
    draw.text((x_i + (card_w - (is_b[2] - is_b[0])) // 2, y_pos + 74), i_sub, fill="#eed88c", font=box_sub_font)

    qr_x_i = x_i + (card_w - qr_box_size) // 2
    draw.rounded_rectangle([qr_x_i, y_pos + 125, qr_x_i + qr_box_size, y_pos + 125 + qr_box_size], radius=20, fill="#ffffff", outline="#c5a034", width=2)
    qr_i_resized = img_insta.resize((qr_inner_dual, qr_inner_dual), Image.Resampling.LANCZOS)
    standee.paste(qr_i_resized, (qr_x_i + margin_dual, y_pos + 125 + margin_dual))

    # Instagram badge pill
    draw.rounded_rectangle([x_i + 80, y_pos + 615, x_i + card_w - 80, y_pos + 675], radius=30, fill="#22060d", outline="#c5a034", width=1)
    if os.path.exists("instagram_icon.png"):
        i_ico = Image.open("instagram_icon.png").convert("RGBA").resize((32, 32), Image.Resampling.LANCZOS)
        standee.paste(i_ico, (x_i + 95, y_pos + 634), i_ico)
    i_lbl = "Instagram Reels"
    draw.text((x_i + 145, y_pos + 633), i_lbl, fill="#ffffff", font=box_sub_font)

    i_btn = "Scan to Follow on Instagram"
    ibtn_b = draw.textbbox((0, 0), i_btn, font=box_sub_font)
    draw.text((x_i + (card_w - (ibtn_b[2] - ibtn_b[0])) // 2, y_pos + 725), i_btn, fill="#eed88c", font=box_sub_font)

    # Address + Phone Framed in Thin Gold Box
    box_w = 980
    box_h = 176
    box_x = (w - box_w) // 2
    box_y = 1335
    draw.rounded_rectangle(
        [box_x, box_y, box_x + box_w, box_y + box_h],
        radius=20, fill=None, outline="#c5a034", width=2
    )

    addr_line1 = "Shree Kripa Midway Restaurant,"
    addr_line2 = "Near Maharana Pratap Bridge, Pigdamber, Rau, Indore"
    phone_text = cfg.get("phoneButtonText", "Call / Reservation: 91110 30307")

    a1_b = draw.textbbox((0, 0), addr_line1, font=addr1_font)
    draw.text(((w - (a1_b[2] - a1_b[0])) // 2, box_y + 18), addr_line1, fill="#ffffff", font=addr1_font)

    a2_b = draw.textbbox((0, 0), addr_line2, font=addr2_font)
    draw.text(((w - (a2_b[2] - a2_b[0])) // 2, box_y + 60), addr_line2, fill="#ffffff", font=addr2_font)

    pb = draw.textbbox((0, 0), phone_text, font=phone_font)
    draw.text(((w - (pb[2] - pb[0])) // 2, box_y + 108), phone_text, fill="#eed88c", font=phone_font)

    thanks_text = "Thank You For Visiting Shree Kripa"
    th_b = draw.textbbox((0, 0), thanks_text, font=thanks_font)
    tw = th_b[2] - th_b[0]
    tx = (w - tw) // 2
    draw.text((tx, 1535), thanks_text, fill="#eed88c", font=thanks_font)
    draw_gold_sparkle(draw, tx - 24, 1551, 9, "#c5a034")
    draw_gold_sparkle(draw, tx + tw + 24, 1551, 9, "#c5a034")

    standee.save("standee_dual_direct_static.png", "PNG", dpi=(300, 300))

if __name__ == "__main__":
    generate_all_assets()
