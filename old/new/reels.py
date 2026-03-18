from PIL import Image, ImageDraw, ImageFont
from moviepy.video.VideoClip import ImageClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from gtts import gTTS
import os

# =====================================================
# ORIGINAL IMAGE CREATOR (UNCHANGED)
# =====================================================
def create_news_image(banner_head, headline, id):
    bg = Image.open("../assets/bg.png").convert("RGB")
    bg = bg.resize((800, 800))

    overlay = Image.new("RGBA", bg.size, (0, 0, 0, 60))
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay).convert("RGB")

    draw = ImageDraw.Draw(bg)

    banner_font = ImageFont.truetype("../fonts/Baloo2-Bold.ttf", 42)
    headline_font = ImageFont.truetype("../fonts/Baloo2-Bold.ttf", 36)
    copyright_font = ImageFont.truetype("../fonts/Baloo2-Regular.ttf", 20)

    # Banner
    banner_height = 100
    draw.rectangle([0, 0, 800, banner_height], fill=(222, 28, 55))
    bw, bh = draw.textbbox((0, 0), banner_head, font=banner_font)[2:]
    draw.text(
        ((800 - bw) // 2, (banner_height - bh) // 2),
        banner_head,
        font=banner_font,
        fill=(255, 255, 255),
    )

    # Text wrapping
    def wrap_text(text, font, max_width):
        words, lines, line = text.split(), [], ""
        for word in words:
            test = f"{line} {word}".strip()
            w = draw.textbbox((0, 0), test, font=font)[2]
            if w <= max_width:
                line = test
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
        return lines

    margin = 40
    max_width = 800 - 2 * margin
    lines = wrap_text(headline, headline_font, max_width)
    line_height = headline_font.getbbox("A")[3] + 12
    box_height = len(lines) * line_height + 40
    top = (800 - box_height) // 2 + 20

    box = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    box_draw = ImageDraw.Draw(box)
    box_draw.rectangle(
        [margin, top - 20, 800 - margin, top + box_height - 20],
        fill=(0, 0, 0, 80),
    )
    bg = Image.alpha_composite(bg.convert("RGBA"), box)

    draw = ImageDraw.Draw(bg)
    for i, line in enumerate(lines):
        lw = draw.textbbox((0, 0), line, font=headline_font)[2]
        draw.text(
            ((800 - lw) // 2, top + i * line_height),
            line,
            font=headline_font,
            fill=(255, 255, 255),
        )

    draw.text((20, 760), "© Br45 News",
              font=copyright_font, fill=(220, 220, 220))

    os.makedirs("image", exist_ok=True)
    img_path = f"image/{id}.png"
    bg.save(img_path)
    return img_path


# =====================================================
# IMAGE ➜ VIDEO (SAME SIZE, SAME ID, REEL FOLDER)
# =====================================================
def image_to_video(image_path, voice_text, id):
    os.makedirs("reel", exist_ok=True)
    os.makedirs("audio", exist_ok=True)

    # Voice
    audio_path = f"audio/{id}.mp3"
    tts = gTTS(text=voice_text, lang="hi")
    tts.save(audio_path)
    audio = AudioFileClip(audio_path)

    # Image → video (NO resize)
    clip = ImageClip(image_path).with_duration(audio.duration)
    clip = clip.with_audio(audio)

    out_path = f"reel/{id}.mp4"

    clip.write_videofile(
        out_path,
        fps=30,
        codec="libx264",
        audio_codec="aac",
    )

    print("✅ Video saved:", out_path)


# =====================================================
# RUN
# =====================================================
if __name__ == "__main__":
    post_id = "post_102"

    img_path = create_news_image(
        banner_head="Bhabua, Kaimur | Jun 13, 2025",
        headline=(
            "जानकारी के अनुसार मध्य ग्रामीण बैंक से पैसा निकाल कर "
            "एक महिला अपने घर परासिया जा रही थी। तभी बाइक सवार बदमाशों "
            "ने बबूरा मस्जिद के आगे महिला से एक लाख रुपए छीनकर फरार हो गये। "
            "मामले में दो से तीन लोगों को हिरासत में लेकर पूछताछ की जा रही है।"
        ),
        id=post_id,
    )

    image_to_video(
        image_path=img_path,
        voice_text="भभुआ से बड़ी खबर। महिला से एक लाख रुपये की लूट का मामला सामने आया है।",
        id=post_id,
    )
