import tkinter as tk
from tkinter import ttk, messagebox

from .a_slider import Slider

class PanelControles:
    def __init__(self, parent, callback_actualizar):
        self.parent = parent
        self.callback_actualizar = callback_actualizar
        
        self.paneles_vars = []
        self.visibilidad_widgets = []
        
        self.frame_botones = ttk.Frame(self.parent)
        self.frame_botones.pack(fill='x', pady=5, padx=5)
        
        ttk.Button(self.frame_botones, text="➕ Añadir Gráfico", command=self.agregar_grafico).pack(side=tk.LEFT, padx=2, expand=True, fill='x')
        ttk.Button(self.frame_botones, text="➖ Quitar Gráfico", command=self.quitar_grafico).pack(side=tk.LEFT, padx=2, expand=True, fill='x')
        
        self.frame_visibilidad = ttk.LabelFrame(self.parent, text="Mostrar en Pantalla")
        self.frame_visibilidad.pack(fill='x', padx=5, pady=(0, 5))
        
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.callback_actualizar()

    def agregar_grafico(self):
        if len(self.paneles_vars) >= 5:
            messagebox.showerror(
                title="Error", 
                message="¿Para que quieres tantos graficos?\nMax 5 Graficos por ahora..."
            )
            return

        num_grafico = len(self.paneles_vars) + 1
        frame_pestana = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame_pestana, text=f"Gráfico {num_grafico}")
        
        vars_dict = {
            "mostrar_grafico": tk.BooleanVar(value=True),
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
            "show_periodo": tk.BooleanVar(value=True),
            "is_playing": tk.BooleanVar(value=False),
            "fase_actual": tk.DoubleVar(value=0.0)
        }
        
        self.paneles_vars.append((frame_pestana, vars_dict))
        
        cb_vis = ttk.Checkbutton(
            self.frame_visibilidad,
            text=f"G{num_grafico}",
            variable=vars_dict["mostrar_grafico"],
            command=self.callback_actualizar
        )
        cb_vis.pack(side=tk.LEFT, padx=5)
        self.visibilidad_widgets.append(cb_vis)

        btn_play = ttk.Button(frame_pestana, text="▶ Play")
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

        ttk.Separator(frame_pestana, orient='horizontal').pack(fill='x', pady=5)
        self.crear_checkbox(frame_pestana, "Línea Referencial de Período", vars_dict["show_periodo"])
        
        self.notebook.select(frame_pestana)
        self.callback_actualizar()

    def toggle_play(self, btn, vars_dict):
        if vars_dict["is_playing"].get():
            vars_dict["is_playing"].set(False)
            vars_dict["fase_actual"].set(0.0)
            btn.config(text="▶ Play")
        else:
            vars_dict["is_playing"].set(True)
            btn.config(text="⏹ Detener")
        self.callback_actualizar()

    def quitar_grafico(self):
        if len(self.paneles_vars) > 0:
            frame_pestana, _ = self.paneles_vars.pop()
            self.notebook.forget(frame_pestana)
            frame_pestana.destroy()
            
            cb_vis = self.visibilidad_widgets.pop()
            cb_vis.destroy()
            
            self.callback_actualizar()

    def crear_slider(self, parent, texto, variable, desde, hasta, resolucion):
        slider_custom = Slider(
            parent=parent, 
            label_text=texto, 
            from_=desde, 
            to=hasta, 
            value=variable.get(), 
            step=resolucion
        )
        slider_custom.pack(fill='x', pady=5)
        
        def on_slider_change(*args):
            try:
                nuevo_valor = slider_custom.get_value()
                variable.set(nuevo_valor)
                self.callback_actualizar()
            except tk.TclError:
                pass

        slider_custom.value_var.trace_add("write", on_slider_change)

    def crear_checkbox(self, parent, texto, variable):
        cb = ttk.Checkbutton(parent, text=texto, variable=variable, command=self.callback_actualizar)
        cb.pack(fill='x', pady=1, anchor='w')

    def obtener_configuraciones(self):
        configs = []
        for _, vars_dict in self.paneles_vars:
            if vars_dict["mostrar_grafico"].get():
                config = {k: v.get() for k, v in vars_dict.items()}
                configs.append(config)
        return configs