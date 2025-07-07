from PIL import Image, ImageDraw, ImageFont

def create_news_image(banner_head, headline, id):
    print("i am image creator")
    # --- Load Background Image ---
    bg = Image.open("assets/bg.png").convert("RGB")
    bg = bg.resize((800, 800))

    # --- Optional: Darken background for better contrast ---
    overlay = Image.new("RGBA", bg.size, (0, 0, 0, 60))  # semi-transparent black
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay).convert("RGB")

    # --- Draw Context ---
    draw = ImageDraw.Draw(bg)

    # --- Load Fonts ---
    banner_font = ImageFont.truetype("fonts/Baloo2-Bold.ttf", 42)
    headline_font = ImageFont.truetype("fonts/Baloo2-Bold.ttf", 36)
    copyright_font = ImageFont.truetype("fonts/Baloo2-Regular.ttf", 20)

    # --- Banner ---
    banner_height = 100
    draw.rectangle([0, 0, 800, banner_height], fill=(222, 28, 55))
    bw, bh = draw.textbbox((0, 0), banner_head, font=banner_font)[2:]
    draw.text(((800 - bw) // 2, (banner_height - bh) // 2),
              banner_head, font=banner_font, fill=(255, 255, 255))

    # --- Headline Wrapping ---
    def wrap_text(text, font, max_width):
        words, lines, line = text.split(), [], ""
        for word in words:
            test_line = f"{line} {word}".strip()
            w = draw.textbbox((0, 0), test_line, font=font)[2]
            if w <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
        return lines

    # Headline box
    margin = 40
    text_area_width = 800 - 2 * margin
    lines = wrap_text(headline, headline_font, text_area_width)
    line_height = headline_font.getbbox("A")[3] + 12
    headline_height = len(lines) * line_height + 40
    headline_top = (800 - headline_height) // 2 + 20

    # --- Create semi-transparent black box ---
    headline_box = [margin, headline_top - 20, 800 - margin, headline_top + headline_height - 20]
    black_box = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    box_draw = ImageDraw.Draw(black_box)
    box_draw.rectangle(headline_box, fill=(0, 0, 0, 80))  # black with transparency
    bg = Image.alpha_composite(bg.convert("RGBA"), black_box)

    # Draw wrapped text (white)
    draw = ImageDraw.Draw(bg)
    for i, line in enumerate(lines):
        lw = draw.textbbox((0, 0), line, font=headline_font)[2]
        draw.text(((800 - lw) // 2, headline_top + i * line_height),
                  line, font=headline_font, fill=(255, 255, 255))

    # Copyright bottom-left
    copyright_text = "© Br45 News"
    cw, ch = draw.textbbox((0, 0), copyright_text, font=copyright_font)[2:]
    draw.text((20, 800 - ch - 20), copyright_text,
              font=copyright_font, fill=(220, 220, 220))

    # Save image with id as filename
    filename = f"image/{id}.png"
    bg.convert("RGB").save(filename)
    print(f"✅ Saved as '{filename}'")

# --- Example Usage ---
if __name__ == "__main__":
    create_news_image(
        banner_head="Bhabua, Kaimur | Jun 13, 2025",
        headline="जानकारी के अनुसार मध्य ग्रामीण बैंक से पैसा निकाल कर एक महिला अपने घर परासिया जा रही थी। तभी बाइक सवार बदमाशों ने बबूरा मस्जिद के आगे महिला से एक लाख रुपए छीनकर फरार हो गये। मामले में भभुआ एसडीपीओ ने शुक्रवार की सुबह बताया मामले में दो से तीन लोगों को हिरासत में लेकर पूछ-ताछ की जा रही हैं ।",
        id="post_102"
    )
