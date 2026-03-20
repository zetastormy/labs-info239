import sys
import numpy as np

import tkinter as tk
from tkinter import ttk

from simulador.a_graficos import GestorGraficos
from simulador.b_panel import PanelControles

class SimuladorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Comparativo de Señales AC/DC")
        self.root.geometry("1400x800")

        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
        
        self.frame_izq = ttk.Frame(self.root)
        self.frame_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.frame_der = ttk.Frame(self.root, width=380)
        self.frame_der.pack(side=tk.RIGHT, fill=tk.Y)
        self.frame_der.pack_propagate(False)
        
        self.gestor_graficos = GestorGraficos(self.frame_izq)
        self.panel_controles = PanelControles(self.frame_der, self.actualizar_vista)

        # Iniciar el bucle de animación
        self.animar_ondas()

    def actualizar_vista(self, es_animacion=False):
        if hasattr(self, "panel_controles"):
            configs = self.panel_controles.obtener_configuraciones()
            self.gestor_graficos.actualizar_graficos(configs, es_animacion)

    def animar_ondas(self):
        hay_animacion = False
        
        # Iterar sobre las variables de cada pestaña
        for _, vars_dict in self.panel_controles.paneles_vars:
            if vars_dict["is_playing"].get():
                f = vars_dict["frecuencia"].get()
                velocidad = 0.02 # Ajuste de velocidad visual
                
                # Incrementar la fase
                fase = vars_dict["fase_actual"].get()
                fase += 2 * np.pi * f * velocidad * (30 / 1000.0)
                vars_dict["fase_actual"].set(fase)
                
                hay_animacion = True
        
        # Si al menos un gráfico se movió, actualizamos la pantalla
        if hay_animacion:
            self.actualizar_vista(es_animacion=True)
            
        self.root.after(30, self.animar_ondas)

    def cerrar_aplicacion(self):        
        self.root.quit()
        self.root.destroy()
        
        sys.exit()

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    if 'clam' in style.theme_names():
        style.theme_use('clam')
        
    app = SimuladorApp(root)
    root.mainloop()