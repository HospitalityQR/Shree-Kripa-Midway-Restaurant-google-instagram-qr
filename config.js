// =============================================================================
// 🦚 SHREE KRIPA MIDWAY RESTAURANT - CONFIGURATION SETTINGS
// =============================================================================
// Sirf yahan details badlein — Poora webpage, standee aur links automatically update ho jayenge!
// Is restaurant ka kisi dusre restaurant se koi lena-dena nahi hai (100% Isolated).
// =============================================================================

var RESTAURANT_CONFIG = {
    // 1. Restaurant Basic Details
    restaurantId: "shree-kripa",
    restaurantName: "Shree Kripa",
    subtitle: "Midway Restaurant",
    tagline: "100% Pure Veg • Pigdamber, Rau • Indore",
    logoImage: "logo_with_gold_rim.png",
    cleanLogoImage: "logo.png",

    // 2. Standee & QR Mode:
    // "dual_link"   -> Single QR opens the Landing Page (both Google & Instagram buttons)
    // "google_only" -> Single QR opens Google Review directly (Static)
    // "insta_only"  -> Single QR opens Instagram directly (Static)
    qrMode: "dual_link",

    // 3. Standee Premium Text
    standeeHeading: "SCAN TO CONNECT",
    standeeSubheading: "Rate Us on Google • Follow Us on Instagram",

    // 4. Google Review Link & Luxury Text
    googleReviewLink: "https://share.google/MwO49jjEmQJTSvkte",
    googleRatingText: "Rate Us on Google",
    googleRatingSubtext: "Share your 5-Star experience on Google",

    // 5. Instagram Link & Profile Handle
    instagramLink: "https://www.instagram.com/shree_kripa_restaurant?stkn=YjdsMzlvMTNlc3dz",
    instagramUsername: "@shree_kripa_restaurant",
    instagramActionText: "Follow Us on Instagram",
    instagramSubtext: "@shree_kripa_restaurant \n• Pure Veg, Ambience & Reels",

    // 6. Contact & Location Details
    phoneNumber: "9111030307",
    phoneDisplay: "+91 91110 30307",
    phoneButtonText: "Call / Reservation: 91110 30307",
    address: "Near Maharana Pratap Bridge, Pigdamber, Rau, NH 3, Indore",
    shortAddress: "Near Maharana Pratap Bridge, Pigdamber, Rau, Indore",
    mapsLink: "https://www.google.com/maps/search/?api=1&query=Shree+Kripa+Midway+Restaurant+Pigdamber+Rau+Indore",

    // 7. Footer Message (Italic Gold)
    footerThanks: "Thank You For Visiting Shree Kripa ✨",
    footerCity: "100% Pure Veg • Pure Desi Ghee • Rau, Indore",

    // 8. Hosted Landing Page URL on HospitalityQR / GitHub Pages
    landingPageUrl: "https://hospitalityqr.github.io/Shree-Kripa-Midway-Restaurant-google-instagram-qr/"
};

if (typeof module !== 'undefined' && module.exports) {
    module.exports = RESTAURANT_CONFIG;
}
