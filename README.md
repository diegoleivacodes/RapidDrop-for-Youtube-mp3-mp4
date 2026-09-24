# RapidDrop-for-Youtube-mp3-mp4
A clean, ad-free, and high-speed YouTube downloader for your PC. No limits, no malware.

Una aplicación de escritorio moderna, rápida y ligera construida en Python para descargar audios (MP3) y videos (MP4) individuales de YouTube de forma directa, sin anuncios ni restricciones de velocidad.El proyecto cuenta con un diseño de interfaz gráfica limpio, asíncrono y optimizado, empaquetado en un archivo ejecutable .exe autónomo ideal para usuarios finales.

# Características principalesDescargas sin límites: 
Extrae contenido a máxima velocidad aprovechando todo tu ancho de banda de internet de forma privada.
Detección inteligente de enlaces: Ignora metadatos pesados de listas de reproducción cuando solo deseas un video individual.
Selector visual de carpetas: Permite configurar dinámicamente el directorio de guardado mediante el explorador nativo del sistema.
Buscador de miniaturas: Descarga y muestra la portada (thumbnail) del video en tiempo real antes de iniciar la descarga.
Barra de progreso en tiempo real: Indicador visual fluido que calcula el porcentaje exacto y el estado de la conversión.
Motor de auto-actualización nativo: Incluye un hilo de fondo que actualiza los componentes de extracción de forma silenciosa para blindar el software contra los bloqueos constantes de YouTube.

# Tecnologías utilizadas
Lenguaje: PythonMotor de descarga: yt-dlp 
Interfaz Gráfica (GUI): CustomTkinter & Tkinter
Procesamiento de Imágenes: Pillow (PIL) (Para la renderización dinámica de las miniaturas)
Compilación: PyInstaller (Configurado con soporte para multi-procesamiento en Windows para evitar bucles de procesos). 

# Nota sobre el desarrollo
Este software fue diseñado e implementado por mí utilizando Inteligencia Artificial (IA) como copiloto de desarrollo. La IA asistió en la maquetación inicial de la cuadrícula visual y en el planteamiento de algoritmos base.

# Cómo compilar tu propio ejecutable 
Si realizas cambios en el código y deseas volver a generar el archivo .exe independiente para Windows, asegúrate de tener instaladas las dependencias y ejecuta el siguiente comando en tu terminal (CMD/Bash) dentro de la carpeta donde se encuentre el archivo.py

python -m PyInstaller --noconfirm --onefile --windowed --collect-all customtkinter YtDwld0.1.py
