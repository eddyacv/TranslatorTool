import os
import asyncio
import edge_tts

from faster_whisper import WhisperModel
from deep_translator import GoogleTranslator


SPANISH_VOICES = {
    "Perú - Mujer - Camila": "es-PE-CamilaNeural",
    "Perú - Hombre - Alex": "es-PE-AlexNeural",
    "México - Mujer - Dalia": "es-MX-DaliaNeural",
    "México - Hombre - Jorge": "es-MX-JorgeNeural",
    "España - Mujer - Elvira": "es-ES-ElviraNeural",
    "España - Hombre - Álvaro": "es-ES-AlvaroNeural",
    "Argentina - Mujer - Elena": "es-AR-ElenaNeural",
    "Colombia - Mujer - Salomé": "es-CO-SalomeNeural",
    "Chile - Mujer - Catalina": "es-CL-CatalinaNeural",
}


def seconds_to_srt_time(seconds):
    ms = int((seconds - int(seconds)) * 1000)
    s = int(seconds) % 60
    m = int(seconds // 60) % 60
    h = int(seconds // 3600)

    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def transcribe_translate_segments(audio_path, srt_path, model_size="small"):
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_path)

    translator = GoogleTranslator(source="auto", target="es")

    final_segments = []

    with open(srt_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments, start=1):
            original_text = segment.text.strip()

            try:
                translated_text = translator.translate(original_text)
            except Exception:
                translated_text = original_text

            item = {
                "index": i,
                "start": segment.start,
                "end": segment.end,
                "text": translated_text
            }

            final_segments.append(item)

            f.write(f"{i}\n")
            f.write(f"{seconds_to_srt_time(segment.start)} --> {seconds_to_srt_time(segment.end)}\n")
            f.write(f"{translated_text}\n\n")

    return final_segments


async def generate_tts(text, voice, output_path):
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save(output_path)


def generate_tts_sync(text, voice, output_path):
    asyncio.run(generate_tts(text, voice, output_path))


async def generate_voice_sample(text, voice, output_path):
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save(output_path)


def create_voice_sample(text, voice_label, voice_code):
    output_dir = os.path.join("recursos", "voces")
    os.makedirs(output_dir, exist_ok=True)

    safe_name = (
        voice_label.replace(" ", "_")
        .replace("-", "")
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
    )

    output_path = os.path.join(output_dir, f"{safe_name}.mp3")

    asyncio.run(generate_voice_sample(text, voice_code, output_path))

    return output_path