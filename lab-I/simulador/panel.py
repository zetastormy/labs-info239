import tkinter as tk
from tkinter import ttk

class PanelControles:
    def __init__(self, parent, callback_actualizar):
        self.parent = parent
        self.callback_actualizar = callback_actualizar
        
        self.paneles_vars = []
        
        self.frame_botones = ttk.Frame(self.parent)
        self.frame_botones.pack(fill='x', pady=5, padx=5)
        
        ttk.Button(self.frame_botones, text="➕ Añadir Gráfico", command=self.agregar_grafico).pack(side=tk.LEFT, padx=2, expand=True, fill='x')
        ttk.Button(self.frame_botones, text="➖ Quitar Gráfico", command=self.quitar_grafico).pack(side=tk.LEFT, padx=2, expand=True, fill='x')
        
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # AHORA: Inicia vacío y actualizamos la vista para asegurar el lienzo en blanco
        self.callback_actualizar()

    def agregar_grafico(self):
        num_grafico = len(self.paneles_vars) + 1
        frame_pestana = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame_pestana, text=f"Gráfico {num_grafico}")
        
        # Variables, incluyendo el estado de animación
        vars_dict = {
            "frecuencia": tk.DoubleVar(value=50.0),
            "amplitud": tk.DoubleVar(value=5.0),
            "duracion": tk.DoubleVar(value=0.1),
            "rc": tk.DoubleVar(value=0.02),
            "show_ac": tk.BooleanVar(value=True),
            "show_dc": tk.BooleanVar(value=False),
            "show_hw": tk.BooleanVar(value=False),
            "show_fw": tk.BooleanVar(value=False),
            "show_hw_cap": tk.BooleanVar(value=False),
            "show_fw_cap": tk.BooleanVar(value=False),
            "is_playing": tk.BooleanVar(value=False),
            "fase_actual": tk.DoubleVar(value=0.0)
        }
        
        self.paneles_vars.append((frame_pestana, vars_dict))
        
        # Botón de animación individual
        btn_play = ttk.Button(frame_pestana, text="▶ Play")
        # Usamos lambda con valores por defecto para que capture las variables de esta iteración específica
        btn_play.config(command=lambda b=btn_play, v=vars_dict: self.toggle_play(b, v))
        btn_play.pack(fill='x', pady=(0, 10))

        ttk.Label(frame_pestana, text="⚙️ Parámetros", font=("Arial", 12, "bold")).pack(pady=5)
        self.crear_slider(frame_pestana, "Frecuencia (Hz)", vars_dict["frecuencia"], 1, 200, 1)
        self.crear_slider(frame_pestana, "Amplitud (V)", vars_dict["amplitud"], 1, 24, 0.5)
        self.crear_slider(frame_pestana, "Duración (s)", vars_dict["duracion"], 0.02, 0.2, 0.01)
        self.crear_slider(frame_pestana, "Constante RC (s)", vars_dict["rc"], 0.001, 0.1, 0.001)

        ttk.Separator(frame_pestana, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(frame_pestana, text="📈 Señales a Mostrar", font=("Arial", 12, "bold")).pack(pady=5)

        self.crear_checkbox(frame_pestana, "Señal AC Original", vars_dict["show_ac"])
        self.crear_checkbox(frame_pestana, "Corriente Continua (DC)", vars_dict["show_dc"])
        self.crear_checkbox(frame_pestana, "Rectificación Media Onda", vars_dict["show_hw"])
        self.crear_checkbox(frame_pestana, "Media Onda + Capacitor", vars_dict["show_hw_cap"])
        self.crear_checkbox(frame_pestana, "Rectificación Onda Completa", vars_dict["show_fw"])
        self.crear_checkbox(frame_pestana, "Onda Completa + Capacitor", vars_dict["show_fw_cap"])
        
        self.notebook.select(frame_pestana)
        self.callback_actualizar()

    def toggle_play(self, btn, vars_dict):
        if vars_dict["is_playing"].get():
            # Detener y resetear
            vars_dict["is_playing"].set(False)
            vars_dict["fase_actual"].set(0.0)
            btn.config(text="▶ Play")
        else:
            # Iniciar animación
            vars_dict["is_playing"].set(True)
            btn.config(text="⏹ Detener")
        self.callback_actualizar()

    def quitar_grafico(self):
        if len(self.paneles_vars) > 0:
            frame_pestana, _ = self.paneles_vars.pop()
            self.notebook.forget(frame_pestana)
            frame_pestana.destroy()
            self.callback_actualizar()

    def crear_slider(self, parent, texto, variable, desde, hasta, resolucion):
        marco = ttk.Frame(parent)
        marco.pack(fill='x', pady=2)
        ttk.Label(marco, text=texto).pack(side=tk.TOP, anchor='w')
        slider = tk.Scale(marco, from_=desde, to=hasta, variable=variable, 
                          resolution=resolucion, orient=tk.HORIZONTAL, 
                          command=lambda _: self.callback_actualizar())
        slider.pack(fill='x')

    def crear_checkbox(self, parent, texto, variable):
        cb = ttk.Checkbutton(parent, text=texto, variable=variable, command=self.callback_actualizar)
        cb.pack(fill='x', pady=1, anchor='w')

    def obtener_configuraciones(self):
        configs = []
        for _, vars_dict in self.paneles_vars:
            config = {k: v.get() for k, v in vars_dict.items()}
            configs.append(config)
        return configs