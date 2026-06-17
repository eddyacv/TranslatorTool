import os
import tkinter as tk
from tkinter import filedialog

import streamlit as st

from processor import process_single_video, copy_course_materials
from video_utils import is_video
from audio_utils import SPANISH_VOICES, create_voice_sample


def select_folder():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    folder = filedialog.askdirectory()
    root.destroy()
    return folder


st.set_page_config(
    page_title="Traductor de videos",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Traductor profesional de videos a español")
st.write("Genera subtítulos y agrega audio español como segunda pista sincronizada por segmentos.")

if "input_folder" not in st.session_state:
    st.session_state.input_folder = ""

if "output_folder_base" not in st.session_state:
    st.session_state.output_folder_base = ""

st.subheader("📁 Carpetas")

col_a, col_b = st.columns([4, 1])

with col_a:
    input_folder_text = st.text_input(
        "Carpeta origen",
        value=st.session_state.input_folder
    )

with col_b:
    st.write("")
    st.write("")
    if st.button("Buscar origen"):
        selected = select_folder()
        if selected:
            st.session_state.input_folder = selected
            st.rerun()

col_c, col_d = st.columns([4, 1])

with col_c:
    output_folder_text = st.text_input(
        "Carpeta destino base",
        value=st.session_state.output_folder_base
    )

with col_d:
    st.write("")
    st.write("")
    if st.button("Buscar destino"):
        selected = select_folder()
        if selected:
            st.session_state.output_folder_base = selected
            st.rerun()

input_folder = input_folder_text
output_folder_base = output_folder_text

if input_folder and output_folder_base:
    parent_name = os.path.basename(os.path.normpath(input_folder))
    preview_output_folder = os.path.join(output_folder_base, f"{parent_name}_ES")
    st.info(f"Carpeta final de salida: {preview_output_folder}")

st.divider()

st.subheader("⚙️ Opciones")

col1, col2 = st.columns(2)

with col1:
    keep_srt = st.checkbox("Mantener subtítulos .srt en la carpeta", value=True)
    burn_subs = st.checkbox("Incrustar subtítulos visualmente en el video", value=False)
    copy_materials = st.checkbox("Copiar PDFs y materiales del curso", value=True)

with col2:
    generate_audio = st.checkbox("Agregar audio español como segunda pista", value=True)
    clean_temp = st.checkbox("Eliminar audios temporales al finalizar", value=True)

model_size = st.selectbox(
    "Modelo Whisper",
    ["tiny", "base", "small"],
    index=2
)

if model_size == "tiny":
    st.info("⚡ Tiny: rápido, menor precisión.")
elif model_size == "base":
    st.info("⚖️ Base: balance entre velocidad y calidad.")
elif model_size == "small":
    st.info("🎯 Small: recomendado para cursos y tutoriales.")

st.divider()

st.subheader("🎙️ Voz española")

voice_label = st.selectbox(
    "Selecciona una voz",
    list(SPANISH_VOICES.keys())
)

voice_code = SPANISH_VOICES[voice_label]

test_text = st.text_area(
    "Texto de prueba",
    value="Hola, esta es una prueba de voz en español para traducir tus videos.",
    height=100
)

if st.button("🔊 Generar prueba de voz"):
    try:
        sample_path = create_voice_sample(
            text=test_text,
            voice_label=voice_label,
            voice_code=voice_code
        )

        st.success(f"Voz generada correctamente: {sample_path}")

        with open(sample_path, "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3")

        with open(sample_path, "rb") as file:
            st.download_button(
                label="⬇️ Descargar ejemplo de voz",
                data=file,
                file_name=os.path.basename(sample_path),
                mime="audio/mp3"
            )

    except Exception as e:
        st.error(f"Error generando la voz: {e}")

st.divider()

start = st.button("🚀 Procesar curso")

if start:
    if not input_folder or not os.path.exists(input_folder):
        st.error("La carpeta origen no existe.")
        st.stop()

    if not output_folder_base:
        st.error("Selecciona la carpeta destino base.")
        st.stop()

    parent_name = os.path.basename(os.path.normpath(input_folder))
    output_folder = os.path.join(output_folder_base, f"{parent_name}_ES")

    os.makedirs(output_folder, exist_ok=True)

    videos = []

    for root_dir, dirs, files in os.walk(input_folder):
        for file in files:
            if is_video(file):
                videos.append(os.path.join(root_dir, file))

    if not videos:
        st.warning("No se encontraron videos.")
        st.stop()

    if copy_materials:
        copy_course_materials(input_folder, output_folder)

    st.info(f"Videos encontrados: {len(videos)}")
    st.info(f"Guardando resultado en: {output_folder}")

    progress_bar = st.progress(0)
    status_text = st.empty()
    log_box = st.empty()

    logs = []

    for index, video_path in enumerate(videos, start=1):
        status_text.write(f"Procesando {index}/{len(videos)}: {video_path}")

        try:
            process_single_video(
                input_video=video_path,
                input_folder=input_folder,
                output_folder=output_folder,
                generate_subs=True,
                burn_subs=burn_subs,
                generate_audio=generate_audio,
                keep_srt=keep_srt,
                model_size=model_size,
                voice=voice_code,
                clean_temp=clean_temp
            )

            logs.append(f"✅ Procesado: {video_path}")

        except Exception as e:
            logs.append(f"❌ Error en {video_path}: {e}")

        progress_bar.progress(index / len(videos))
        log_box.text("\n".join(logs[-10:]))

    st.success("Proceso terminado.")