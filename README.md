# 🎬 TranslatorTool (Traductor Automático de Cursos y Videos)

¡Hola! 👋 Esta es una herramienta que te permite **traducir videos y cursos completos al español** de forma totalmente automática.

Si tienes un curso en inglés (por ejemplo, de Udemy o Domestika), esta herramienta tomará todos los videos, extraerá lo que dicen, lo traducirá, creará subtítulos y hasta le pondrá una nueva voz en español. ¡Y además mantendrá todos tus archivos PDF y carpetas ordenadas exactamente igual que en el curso original!

---

## 🌟 ¿Qué hace exactamente?

1. **Escucha y Traduce**: Extrae el audio original, reconoce lo que dicen y lo traduce al español.
2. **Crea Subtítulos**: Genera un archivo `.srt` con los subtítulos en español para cada video.
3. **Pone Voz en Español**: Genera un nuevo audio en español sincronizado con el video.
4. **Guarda tus Archivos**: Si en tus carpetas hay PDFs, Excels o documentos de texto, los copiará intactos a la carpeta final para que no pierdas nada.
5. **No desordena nada**: Te entregará una nueva carpeta con exactamente las mismas subcarpetas que tu curso original, pero con los videos ya traducidos.

---

## 🛠️ ¿Qué necesitas para empezar?

Para que esto funcione en tu computadora, solo necesitas dos cosas:

1. **Tener Python instalado** (Versión 3.11 o superior).
2. **Tener FFmpeg instalado** (Es un programa oculto que permite manipular videos y audios. Debes asegurarte de tenerlo instalado y agregado al PATH de tu sistema Windows/Mac).

---

## ⚙️ ¿Cómo lo instalo?

1. Descarga esta carpeta con todos los archivos.
2. Abre tu terminal (Símbolo del sistema o PowerShell).
3. Navega hasta esta carpeta.
4. Instala los requerimientos escribiendo este comando y presionando Enter:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 ¿Cómo se usa?

¡Usarlo es muy fácil porque tiene una interfaz visual!

1. Abre tu terminal en la carpeta de este programa.
2. Escribe este comando y presiona Enter:
   ```bash
   streamlit run app_streamlit.py
   ```
3. Se abrirá una ventana en tu navegador de internet. 
4. Desde esa ventana solo tienes que:
   - Seleccionar la carpeta donde tienes tu curso original en inglés.
   - Seleccionar en qué carpeta quieres que se guarde el curso traducido.
   - Elegir qué voz en español quieres que narre los videos.
   - ¡Hacer clic en **Procesar** y dejar que la magia ocurra! ☕

*(Dependiendo de la duración de tus videos y la potencia de tu computadora, este proceso puede tardar un poco. ¡Puedes ir a tomar un café mientras trabaja!)*
