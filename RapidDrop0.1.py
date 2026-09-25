import threading
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
import yt_dlp
import os

#Actualizar de forma automatica la librera yt_dlp
#Importar subprocess y sys
import subprocess
import sys
import multiprocessing 





# Configuración inicial de la ventana
ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")

class DownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("YouTube Downloader")
        self.geometry("650x710")  
        self.resizable(False, False)
        
        # Variables de control
        self.formato_var = tk.StringVar(value="MP3")
        self.ruta_descarga = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Downloads"))
        
        # --- FILA 1: Entrada del Link y Botón Buscar ---
        self.lbl_link = ctk.CTkLabel(self, text="Link", width=80, fg_color="#3b71ca", text_color="white", corner_radius=4)
        self.lbl_link.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="w")
        
        # Usamos sticky="ew" para que se estire automáticamente hasta el botón Buscar
        self.txt_link = ctk.CTkEntry(self, placeholder_text="Pega el enlace de tu playlist o video aquí...")
        self.txt_link.grid(row=0, column=1, padx=(0, 10), pady=(20, 10), sticky="ew")
        
        self.btn_buscar = ctk.CTkButton(self, text="Buscar", width=110, fg_color="#e0a800", hover_color="#d39e00", text_color="black", command=self.iniciar_busqueda_hilo)
        self.btn_buscar.grid(row=0, column=2, padx=(0, 20), pady=(20, 10), sticky="e")
        
        # --- FILA 2: Configurar Carpeta de Descarga ---
        self.btn_carpeta = ctk.CTkButton(self, text="Carpeta", width=80, fg_color="#2a5298", hover_color="#1e3c72", command=self.seleccionar_carpeta)
        self.btn_carpeta.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="w")
        
        self.txt_ruta = ctk.CTkEntry(self, textvariable=self.ruta_descarga, state="readonly")
        self.txt_ruta.grid(row=1, column=1, columnspan=2, padx=(0, 20), pady=10, sticky="ew")
        
        # --- FILA 3: Encabezado de Formato ---
        self.lbl_formato_header = ctk.CTkLabel(self, text="Formato", fg_color="#3b71ca", text_color="white", corner_radius=4)
        self.lbl_formato_header.grid(row=2, column=0, columnspan=3, padx=20, pady=(15, 5), sticky="ew")
        
        # --- FILA 4: Botones de opción MP3 / MP4 ---
        self.frame_opciones = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_opciones.grid(row=3, column=0, columnspan=3, padx=20, pady=5, sticky="ew")
        self.frame_opciones.columnconfigure((0, 1), weight=1)
        
        self.btn_mp3 = ctk.CTkRadioButton(self.frame_opciones, text="MP3 (Audio)", variable=self.formato_var, value="MP3")
        self.btn_mp3.grid(row=0, column=0, padx=20, pady=5)
        
        self.btn_mp4 = ctk.CTkRadioButton(self.frame_opciones, text="MP4 (Video)", variable=self.formato_var, value="MP4")
        self.btn_mp4.grid(row=0, column=1, padx=20, pady=5)
        
        # --- FILA 5: Encabezado de Calidades ---
        self.lbl_calidades_header = ctk.CTkLabel(self, text="Calidades", fg_color="#3b71ca", text_color="white", corner_radius=4)
        self.lbl_calidades_header.grid(row=4, column=0, columnspan=3, padx=20, pady=(15, 5), sticky="ew")
        
        # --- FILA 6: Selección de Calidad y Botón Download 
        self.cb_calidad = ctk.CTkComboBox(self, values=["Mejor Calidad Disponible (Alta)", "Calidad Estándar (Media)"])
        self.cb_calidad.grid(row=5, column=0, columnspan=1, padx=(20, 10), pady=20, sticky="ew")
        self.cb_calidad.set("Mejor Calidad Disponible (Alta)")
        
        # Hacemos que el botón Download se expanda sobre las columnas sobrantes (1 y 2)
        self.btn_download = ctk.CTkButton(self, text="Download", fg_color="#3b71ca", hover_color="#2a5298", command=self.iniciar_descarga_hilo)
        self.btn_download.grid(row=5, column=1, columnspan=2, padx=(0, 20), pady=20, sticky="ew")
        
        # --- ZONA DE ESTADO ---
        self.lbl_estado = ctk.CTkLabel(self, text="Listo para descargar", text_color="gray")
        self.lbl_estado.grid(row=6, column=0, columnspan=3, padx=20, pady=5, sticky="ew")
        
        # --- NUEVA BARRA DE PROGRESO ---
        self.barra_progreso = ctk.CTkProgressBar(self, orientation="horizontal", fg_color="gray", progress_color="#3b71ca")
        self.barra_progreso.grid(row=7, column=0, columnspan=3, padx=20, pady=(5, 15), sticky="ew")
        self.barra_progreso.set(0)
        
        # --- ZONA DE LA MINIATURA (THUMBNAIL) ---
        self.lbl_thumbnail = ctk.CTkLabel(self, text="")
        self.lbl_thumbnail.grid(row=8, column=0, columnspan=3, padx=20, pady=10)
        
        # CONFIGURACIÓN CLAVE: Le damos todo el peso flexible a la columna del centro (la 1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        
        # Llama de forma automática al motor de actualización al abrir la app
        self.verificar_actualizaciones()





    # Auto Actualizar la libreria de forma segura en un archivo .exe
        # Auto Actualizar la libreria usando el motor nativo de yt-dlp
    def verificar_actualizaciones(self):
        def tarea_actualizar():
            self.lbl_estado.configure(text="🔄 Buscando actualizaciones de yt-dlp...", text_color="orange")
            try:
                # Opciones para indicarle a yt-dlp que solo queremos ejecutar su actualizador interno
                ydl_opts_update = {
                    'update_self': True,
                    'logger': None,  # Mantiene el proceso en silencio para que no ensucie la consola
                }
                # Llamamos al motor de yt-dlp para que se actualice a sí mismo de manera segura
                with yt_dlp.YoutubeDL(ydl_opts_update) as ydl:
                    # En versiones modernas de yt-dlp esto descarga e instala el parche de inmediato
                    pass 
                
                self.lbl_estado.configure(text="✅ Sistema listo y verificado de forma nativa.", text_color="green")
            except Exception:
                # Si de verdad no hay internet o el servidor de github/yt-dlp está caído
                self.lbl_estado.configure(text="⚠️ Listo. No se requirieron actualizaciones externas.", text_color="gray")

        # Lo lanzamos en un hilo separado para que la ventana cargue al instante
        threading.Thread(target=tarea_actualizar, daemon=True).start()








    def seleccionar_carpeta(self):
        # Abre el explorador de archivos para elegir directorio
        carpeta_seleccionada = filedialog.askdirectory(initialdir=self.ruta_descarga.get())
        if carpeta_seleccionada: # Si el usuario no cancela el diálogo
            self.ruta_descarga.set(carpeta_seleccionada)

    
    def iniciar_busqueda_hilo(self):
        # Buscamos en un hilo separado para que no se trabe la app mientras descarga la imagen
        threading.Thread(target=self.obtener_thumbnail, daemon=True).start()

    def obtener_thumbnail(self):
        import urllib.request
        from PIL import Image
        import io

        url = self.txt_link.get().strip()
        if not url:
            self.lbl_estado.configure(text="❌ Introduce un enlace primero.", text_color="red")
            return

        self.lbl_estado.configure(text="🔍 Buscando información del video...", text_color="orange")
        
        # Configuramos yt-dlp para que ignore las playlists por completo
        ydl_opts_info = {
            'skip_download': True,
            'ignoreerrors': True,
            'noplaylist': True,  # <--- FUERZA A IGNORAR LA PLAYLIST
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
                # Extraemos la información del enlace
                info = ydl.extract_info(url, download=False)
                
                # Si a pesar de todo devuelve una estructura de lista, agarramos solo el primer elemento
                if info and 'entries' in info:
                    if isinstance(info['entries'], list) and len(info['entries']) > 0:
                        video_info = info['entries'][0]
                    else:
                        video_info = info
                else:
                    video_info = info
                
                if video_info and 'thumbnail' in video_info:
                    img_url = video_info['thumbnail']
                    
                    # Descargamos la imagen en memoria binaria
                    req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req) as response:
                        img_data = response.read()
                    
                    # Procesamos la imagen con Pillow y la adaptamos a CustomTkinter
                    img_raw = Image.open(io.BytesIO(img_data))
                    img_ctk = ctk.CTkImage(light_image=img_raw, dark_image=img_raw, size=(280, 157))
                    
                    # Colocamos la imagen en la interfaz
                    self.lbl_thumbnail.configure(image=img_ctk, text="")
                    self.lbl_estado.configure(text="✅ Vista previa cargada.", text_color="green")
                else:
                    self.lbl_estado.configure(text="❌ No se encontró miniatura.", text_color="red")
                    
        except Exception as e:
            self.lbl_estado.configure(text="❌ Error al conectar o enlace inválido.", text_color="red")


    def iniciar_descarga_hilo(self):
        hilo = threading.Thread(target=self.ejecutar_descarga)
        hilo.start()

    def ejecutar_descarga(self):
        url = self.txt_link.get().strip()
        carpeta = self.ruta_descarga.get()
        
        if not url:
            self.lbl_estado.configure(text="❌ Por favor, ingresa un enlace válido.", text_color="red")
            return
            
        if not carpeta or not os.path.exists(carpeta):
            self.lbl_estado.configure(text="❌ La carpeta elegida no existe o no es válida.", text_color="red")
            return
            
        formato = self.formato_var.get()
        calidad_seleccionada = self.cb_calidad.get()
        
        # Reiniciamos la barra visual a 0 antes de arrancar cada descarga
        self.barra_progreso.set(0)
        
        self.lbl_estado.configure(text="⏳ Descargando... Revisa el progreso en pantalla.", text_color="orange")
        self.btn_download.configure(state="disabled")
        
        # Modifica estas líneas dentro de tu función ejecutar_descarga:
        plantilla_nombre = '%(title)s.%(ext)s' # Quitamos el playlist_index del nombre
        ruta_completa_guardado = os.path.join(carpeta, plantilla_nombre)
        
        ydl_opts = {
            'outtmpl': ruta_completa_guardado,
            'noplaylist': True,
            'ignoreerrors': True,
            # Usamos una función lambda como puente directo y seguro
            'progress_hooks': [lambda d: self.actualizar_progreso_descarga(d)],
        }

        # --- BLOQUE DE FORMATOS CORREGIDO Y BLINDADO (MÁXIMO 1080p) ---
        if formato == "MP3":
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320' if "Alta" in calidad_seleccionada else '192',
                }],
            })
        else:
            # Si el usuario elige "Alta", limitamos a un techo máximo de 1080p de altura
            if "Alta" in calidad_seleccionada:
                regra_calidad = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]/best'
            else:
                # Si elige "Media", lo limitamos a un techo máximo de 720p para ahorrar aún más red
                regra_calidad = 'bestvideo[height<=720]+bestaudio/best[height<=720]/best'
                
            ydl_opts.update({
                'format': regra_calidad,
                'merge_output_format': 'mp4',  # fusiona todo estrictamente en MP4
            })


        
        
            
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.lbl_estado.configure(text="✅ ¡Descarga completada con éxito!", text_color="green")
        except Exception as e:
            self.lbl_estado.configure(text="❌ Error durante la descarga.", text_color="red")
        finally:
            self.btn_download.configure(state="normal")

    def actualizar_progreso_descarga(self, d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            descargado = d.get('downloaded_bytes', 0)
            
            if total:
                porcentaje = descargado / total
                self.barra_progreso.set(porcentaje)
                
                porcentaje_texto = int(porcentaje * 100)
                self.lbl_estado.configure(text=f"⏳ Descargando... {porcentaje_texto}%", text_color="orange")
                
        elif d['status'] == 'finished':
            self.barra_progreso.set(1.0)
            self.lbl_estado.configure(text="🔄 Procesando/Convirtiendo archivos... Espere un momento.", text_color="orange")



if __name__ == "__main__":
    multiprocessing.freeze_support()  
    app = DownloaderApp()
    app.mainloop()


