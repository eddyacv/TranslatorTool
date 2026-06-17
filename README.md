# 🎬 TranslatorTool

Herramienta desarrollada en Python para traducir cursos y videos automáticamente al español.

## Características

* Traducción automática de audio usando Whisper.
* Generación de subtítulos en español (.srt).
* Generación de audio en español mediante TTS.
* Sincronización automática por segmentos.
* Conserva la estructura original de carpetas.
* Copia automáticamente materiales del curso:

  * PDF
  * DOCX
  * XLSX
  * TXT
  * HTML
* Permite mantener audio original y agregar español como segunda pista.
* Selección de voces desde la interfaz.
* Vista previa y descarga de ejemplos de voz.
* Limpieza automática de archivos temporales.

---

## Estructura de salida

Ejemplo:

Curso original:

Nivel 1/
├── clase1.mp4
├── clase1.pdf

Resultado:

Curso_ES/
├── Nivel 1
│   ├── clase1_es.mp4
│   ├── clase1_es.srt
│   └── clase1.pdf
│
└── recursos
├── voces
├── cache
└── logs

---

## Requisitos

* Python 3.11 o superior
* FFmpeg instalado y agregado al PATH

Verificar:

```bash
ffmpeg -version
```

---

## Instalación

Instalar dependencias:

```bash
pip install streamlit
pip install faster-whisper
pip install deep-translator
pip install edge-tts
```

---

## Ejecución

Desde la carpeta del proyecto:

```bash
python -m streamlit run app_streamlit.py
```

La aplicación abrirá automáticamente:

```text
http://localhost:8501
```

---

## Flujo de trabajo

1. Seleccionar carpeta del curso.
2. Seleccionar carpeta de destino.
3. Elegir modelo Whisper.
4. Elegir voz.
5. Configurar subtítulos y audio.
6. Procesar.

La herramienta:

* Detecta videos.
* Transcribe audio.
* Traduce al español.
* Genera subtítulos.
* Genera audio sincronizado.
* Conserva materiales del curso.
* Mantiene la estructura de carpetas.

---

## Tecnologías utilizadas

* Python
* Streamlit
* FFmpeg
* Faster-Whisper
* Edge-TTS
* Deep Translator

---

## Estado del proyecto

Versión inicial enfocada en:

* Cursos Udemy
* Domestika
* Coloso
* Tutoriales educativos
* Bibliotecas de aprendizaje personal

Proyecto desarrollado para automatizar la traducción y organización de contenido educativo.
