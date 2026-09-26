"""
Quick Restaurant Creator for Hospitality QR Platform
Usage:
    python new_restaurant.py "Restaurant Name"
Example:
    python new_restaurant.py "Chef Bhupis Kitchen"
"""

import sys
import os
import re
import shutil

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'[^\w\-]', '', text)
    return text

def create_new_restaurant(name):
    slug = slugify(name)
    if not slug:
        print("Error: Invalid restaurant name")
        return

    if os.path.exists(slug):
        print(f"Error: Folder '{slug}' already exists!")
        return

    print(f"[*] Creating new restaurant: '{name}' in folder '{slug}'...")
    os.makedirs(slug, exist_ok=True)

    # Copy HTML, Standee, Icons, and generator script from root
    for f in ["index.html", "standee.html", "generate_qr.py", "google_icon.png", "instagram_icon.png", "google_logo.png"]:
        if os.path.exists(f):
            shutil.copy2(f, os.path.join(slug, f))

    # Generate custom config.js
    cfg_content = f"""// =============================================================================
// 🍽️ {name.upper()} - RESTAURANT & QR CODE CONFIGURATION
// =============================================================================
// 100% Isolated: Changes here will ONLY affect this restaurant!
// =============================================================================

var RESTAURANT_CONFIG = {{
    restaurantId: "{slug}",
    restaurantName: "{name}",
    subtitle: "Cafe & Restaurant",
    tagline: "Multi-Cuisine • Pure Veg",
    logoImage: "logo_with_gold_rim.png",
    cleanLogoImage: "logo.png",

    // QR & Standee Mode:
    // "dual_link"   = Single QR opens Landing Page (Google Review & Instagram buttons)
    // "google_only" = Single QR directly opens Google Review (Static)
    // "insta_only"  = Single QR directly opens Instagram (Static)
    qrMode: "dual_link",

    standeeHeading: "SCAN TO CONNECT",
    standeeSubheading: "Rate Us on Google • Follow Us on Instagram",

    googleReviewLink: "https://google.com",
    googleRatingText: "Rate Us on Google",
    googleRatingSubtext: "Share your 5-Star experience on Google",

    instagramLink: "https://instagram.com",
    instagramUsername: "@{slug.replace('-', '')}",
    instagramActionText: "Follow Us on Instagram",
    instagramSubtext: "@{slug.replace('-', '')} • Food & Updates",

    phoneNumber: "9876543210",
    phoneDisplay: "98765 43210",
    phoneButtonText: "Call / Reservation: 98765 43210",
    address: "{name}, Indore, Madhya Pradesh",
    shortAddress: "{name}, Indore",
    mapsLink: "https://maps.google.com/?q={name.replace(' ', '+')}+Indore",

    footerThanks: "Thank You For Visiting {name} ✨",
    footerCity: "Crafted with passion in Indore",

    landingPageUrl: "https://hospitalityqr.github.io/indri-qr/{slug}/"
}};

if (typeof module !== 'undefined' && module.exports) {{
    module.exports = RESTAURANT_CONFIG;
}}
"""
    with open(os.path.join(slug, "config.js"), "w", encoding="utf-8") as f:
        f.write(cfg_content)

    print(f"\n[SUCCESS] '{name}' folder successfully created at: ./{slug}/")
    print("Steps to finish setup:")
    print(f"  1. Put your restaurant logo image inside ./{slug}/ and name it 'logo.png'")
    print(f"  2. Edit ./{slug}/config.js with Google review link, Instagram link & phone number")
    print(f"  3. Run: cd {slug} && python generate_qr.py")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python new_restaurant.py \"Restaurant Name\"")
    else:
        create_new_restaurant(sys.argv[1])
