import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class SimuladorSenalesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Señales AC/DC y Rectificación")
        self.root.geometry("1200x700") 
        
        # --- Variables de control (Parámetros compartidos) ---
        self.frecuencia_var = tk.DoubleVar(value=50.0)
        self.amplitud_var = tk.DoubleVar(value=5.0)
        self.duracion_var = tk.DoubleVar(value=0.1)
        self.rc_var = tk.DoubleVar(value=0.02)

        # --- Variables para mostrar/ocultar gráficos ---
        self.show_ac = tk.BooleanVar(value=True)
        self.show_dc = tk.BooleanVar(value=False)
        self.show_hw = tk.BooleanVar(value=False)  # Media onda
        self.show_fw = tk.BooleanVar(value=False)  # Onda completa
        self.show_hw_cap = tk.BooleanVar(value=False) # Media onda + Cap
        self.show_fw_cap = tk.BooleanVar(value=False) # Onda completa + Cap

        self.crear_interfaz()
        self.actualizar_grafico()

    def crear_interfaz(self):
        # --- Panel Izquierdo: Gráfico ---
        self.frame_grafico = ttk.Frame(self.root)
        self.frame_grafico.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
        
        # --- Añadimos la barra de herramientas de Matplotlib ---
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame_grafico)
        self.toolbar.update()
        
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # --- Panel Derecho: Controles ---
        self.frame_controles = ttk.Frame(self.root, width=350, padding="10")
        self.frame_controles.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Label(self.frame_controles, text="⚙️ Parámetros Globales", font=("Arial", 14, "bold")).pack(pady=10)

        # Sliders de parámetros
        self.crear_slider(self.frame_controles, "Frecuencia (Hz)", self.frecuencia_var, 1, 200, 1)
        self.crear_slider(self.frame_controles, "Amplitud (V)", self.amplitud_var, 1, 24, 0.5)
        self.crear_slider(self.frame_controles, "Duración (s)", self.duracion_var, 0.02, 0.2, 0.01)
        self.crear_slider(self.frame_controles, "Constante RC (s)", self.rc_var, 0.001, 0.1, 0.001)

        ttk.Separator(self.frame_controles, orient='horizontal').pack(fill='x', pady=15)
        ttk.Label(self.frame_controles, text="📈 Señales a Mostrar", font=("Arial", 14, "bold")).pack(pady=10)

        # Checkboxes de gráficos
        self.crear_checkbox(self.frame_controles, "Señal AC Original", self.show_ac)
        self.crear_checkbox(self.frame_controles, "Corriente Continua (DC)", self.show_dc)
        self.crear_checkbox(self.frame_controles, "Rectificación Media Onda", self.show_hw)
        self.crear_checkbox(self.frame_controles, "Media Onda + Capacitor", self.show_hw_cap)
        self.crear_checkbox(self.frame_controles, "Rectificación Onda Completa", self.show_fw)
        self.crear_checkbox(self.frame_controles, "Onda Completa + Capacitor", self.show_fw_cap)

    def crear_slider(self, parent, texto, variable, desde, hasta, resolucion):
        marco = ttk.Frame(parent)
        marco.pack(fill='x', pady=5)
        
        # Sub-frame para alinear el texto y la entrada numérica
        header_frame = ttk.Frame(marco)
        header_frame.pack(fill='x')
        
        ttk.Label(header_frame, text=texto).pack(side=tk.LEFT)
        
        # 1. Variable de texto independiente para evitar que el slider pelee con el teclado
        texto_var = tk.StringVar(value=str(variable.get()))
        
        entrada = ttk.Entry(header_frame, textvariable=texto_var, width=8, justify="right")
        entrada.pack(side=tk.RIGHT)
        
        # 2. Función que se llama cuando movemos el slider con el ratón
        def on_slider_move(val):
            # Formateamos el valor para que no muestre demasiados decimales
            texto_var.set(str(round(float(val), 3))) 
            self.actualizar_grafico()

        # El slider ahora usa on_slider_move como comando
        slider = tk.Scale(marco, from_=desde, to=hasta, variable=variable, 
                          resolution=resolucion, orient=tk.HORIZONTAL, 
                          command=on_slider_move)
        slider.pack(fill='x')

        # 3. Función que se llama cuando el usuario presiona Enter o sale del cuadro de texto
        def on_text_enter(event=None):
            try:
                # Intentamos convertir lo que escribió el usuario a número
                nuevo_valor = float(texto_var.get())
                
                # Limitamos el valor para que no se salga de los límites del slider
                nuevo_valor = max(desde, min(hasta, nuevo_valor))
                
                # Actualizamos el slider y el texto validado
                variable.set(nuevo_valor)
                texto_var.set(str(nuevo_valor))
                
                # Actualizamos el gráfico
                self.actualizar_grafico()
                
            except ValueError:
                # Si el usuario escribió letras o algo inválido, restauramos el valor anterior
                texto_var.set(str(variable.get()))

        # Vinculamos los eventos de teclado y pérdida de foco
        entrada.bind("<Return>", on_text_enter)
        entrada.bind("<FocusOut>", on_text_enter)

    def crear_checkbox(self, parent, texto, variable):
        cb = ttk.Checkbutton(parent, text=texto, variable=variable, command=self.actualizar_grafico)
        cb.pack(fill='x', pady=2, anchor='w')

    def calcular_capacitor(self, senal_base, t, rc):
        # Simula el efecto de descarga del capacitor
        suavizada = [senal_base[0]]
        for i in range(1, len(t)):
            dt = t[i] - t[i-1]
            descarga = suavizada[-1] * np.exp(-dt / rc)
            valor = max(senal_base[i], descarga)
            suavizada.append(valor)
        return np.array(suavizada)

    def actualizar_grafico(self, event=None):
        try:
            # 1. Obtener parámetros actuales
            f = self.frecuencia_var.get()
            v_max = self.amplitud_var.get()
            duracion = self.duracion_var.get()
            rc = self.rc_var.get()

            # 2. Generar vector de tiempo
            t = np.linspace(0, duracion, 2000)

            # 3. Calcular señales base compartidas
            ac = v_max * np.sin(2 * np.pi * f * t)
            dc = np.full_like(t, v_max)
            media_onda = np.maximum(ac, 0)
            onda_completa = np.abs(ac)

            # 4. Limpiar gráfico actual
            self.ax.clear()

            # 5. Dibujar solo las señales seleccionadas por el usuario
            hay_graficos = False
            t_ms = t * 1000  # Convertir a milisegundos para el eje X

            if self.show_ac.get():
                self.ax.plot(t_ms, ac, label="AC Original", color='#1f77b4', alpha=0.6)
                hay_graficos = True
            if self.show_dc.get():
                self.ax.plot(t_ms, dc, label="DC (Constante)", color='black', linestyle='--')
                hay_graficos = True
            if self.show_hw.get():
                self.ax.plot(t_ms, media_onda, label="Media Onda", color='#ff7f0e', linestyle='-.')
                hay_graficos = True
            if self.show_fw.get():
                self.ax.plot(t_ms, onda_completa, label="Onda Completa", color='#2ca02c', linestyle=':')
                hay_graficos = True
            if self.show_hw_cap.get():
                hw_cap = self.calcular_capacitor(media_onda, t, rc)
                self.ax.plot(t_ms, hw_cap, label=f"Media Onda + Cap (RC={rc:.3f})", color='#d62728')
                hay_graficos = True
            if self.show_fw_cap.get():
                fw_cap = self.calcular_capacitor(onda_completa, t, rc)
                self.ax.plot(t_ms, fw_cap, label=f"Onda Completa + Cap (RC={rc:.3f})", color='#9467bd')
                hay_graficos = True

            # 6. Configurar diseño del gráfico
            self.ax.set_title("Análisis de Señales Eléctricas y Filtrado")
            self.ax.set_xlabel("Tiempo (ms)")
            self.ax.set_ylabel("Voltaje (V)")
            self.ax.grid(True, linestyle='--', alpha=0.7)
            self.ax.axhline(0, color='black', linewidth=1)

            if hay_graficos:
                self.ax.legend(loc="lower left")

            self.fig.tight_layout()
            self.canvas.draw()
            
        except (tk.TclError, AttributeError):
            # Si ocurre un error porque la ventana se está cerrando, lo ignoramos
            pass
        # 1. Obtener parámetros actuales
        f = self.frecuencia_var.get()
        v_max = self.amplitud_var.get()
        duracion = self.duracion_var.get()
        rc = self.rc_var.get()

        # 2. Generar vector de tiempo
        t = np.linspace(0, duracion, 2000)

        # 3. Calcular señales base compartidas
        ac = v_max * np.sin(2 * np.pi * f * t)
        dc = np.full_like(t, v_max)
        media_onda = np.maximum(ac, 0)
        onda_completa = np.abs(ac)

        # 4. Limpiar gráfico actual
        self.ax.clear()

        # 5. Dibujar solo las señales seleccionadas por el usuario
        hay_graficos = False
        t_ms = t * 1000  # Convertir a milisegundos para el eje X

        if self.show_ac.get():
            self.ax.plot(t_ms, ac, label="AC Original", color='#1f77b4', alpha=0.6)
            hay_graficos = True
        if self.show_dc.get():
            self.ax.plot(t_ms, dc, label="DC (Constante)", color='black', linestyle='--')
            hay_graficos = True
        if self.show_hw.get():
            self.ax.plot(t_ms, media_onda, label="Media Onda", color='#ff7f0e', linestyle='-.')
            hay_graficos = True
        if self.show_fw.get():
            self.ax.plot(t_ms, onda_completa, label="Onda Completa", color='#2ca02c', linestyle=':')
            hay_graficos = True
        if self.show_hw_cap.get():
            hw_cap = self.calcular_capacitor(media_onda, t, rc)
            self.ax.plot(t_ms, hw_cap, label=f"Media Onda + Cap (RC={rc:.3f})", color='#d62728')
            hay_graficos = True
        if self.show_fw_cap.get():
            fw_cap = self.calcular_capacitor(onda_completa, t, rc)
            self.ax.plot(t_ms, fw_cap, label=f"Onda Completa + Cap (RC={rc:.3f})", color='#9467bd')
            hay_graficos = True

        # 6. Configurar diseño del gráfico
        self.ax.set_title("Análisis de Señales Eléctricas y Filtrado")
        self.ax.set_xlabel("Tiempo (ms)")
        self.ax.set_ylabel("Voltaje (V)")
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.axhline(0, color='black', linewidth=1)

        if hay_graficos:
            self.ax.legend(loc="lower left")

        self.fig.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorSenalesApp(root)
    root.mainloop()