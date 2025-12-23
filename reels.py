from PIL import Image, ImageDraw, ImageFont
from moviepy.video.VideoClip import ImageClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from gtts import gTTS
import os


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

    image_to_video(
        image_path= f"image/{post_id}.png",
        voice_text="भभुआ से बड़ी खबर। महिला से एक लाख रुपये की लूट का मामला सामने आया है।",
        id=post_id,
    )
