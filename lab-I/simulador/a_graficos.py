import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class GestorGraficos:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.fig = plt.Figure(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent_frame)
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.parent_frame)
        self.toolbar.update()
        
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

    def calcular_capacitor(self, senal_base, t, rc):
        suavizada = [senal_base[0]]
        for i in range(1, len(t)):
            dt = t[i] - t[i-1]
            descarga = suavizada[-1] * np.exp(-dt / rc)
            valor = max(senal_base[i], descarga)
            suavizada.append(valor)
        return np.array(suavizada)

    def actualizar_graficos(self, configuraciones, es_animacion=False):
        self.fig.clear()
        n = len(configuraciones)
        
        if n == 0:
            self.canvas.draw()
            return

        axes = self.fig.subplots(n, 1)
        if n == 1:
            axes = [axes]

        for i, (ax, config) in enumerate(zip(axes, configuraciones)):
            f = config["frecuencia"]
            v_max = config["amplitud"]
            duracion = config["duracion"]
            rc = config["rc"]
            fase = config["fase_actual"] # Extraemos la fase animada

            # Añadimos un pequeño historial de tiempo para calcular bien el capacitor
            periodo = 1.0 / f
            puntos_extra = 200
            t_padding = np.linspace(-periodo, 0, puntos_extra, endpoint=False)
            t_main = np.linspace(0, duracion, 2000)
            t_full = np.concatenate([t_padding, t_main])

            # Cálculos matemáticos con la fase aplicada
            ac_full = v_max * np.sin(2 * np.pi * f * t_full + fase)
            media_onda_full = np.maximum(ac_full, 0)
            onda_completa_full = np.abs(ac_full)

            # Recortamos los puntos extra para la visualización de las señales simples
            ac = ac_full[puntos_extra:]
            dc = np.full_like(t_main, v_max)
            media_onda = media_onda_full[puntos_extra:]
            onda_completa = onda_completa_full[puntos_extra:]

            t_ms = t_main * 1000
            hay_graficos = False

            if config["show_ac"]:
                ax.plot(t_ms, ac, label="AC Original", color='#1f77b4', alpha=0.6)
                hay_graficos = True
            if config["show_dc"]:
                ax.plot(t_ms, dc, label="DC", color='black', linestyle='--')
                hay_graficos = True
            if config["show_hw"]:
                ax.plot(t_ms, media_onda, label="Media Onda", color='#ff7f0e', linestyle='-.')
                hay_graficos = True
            if config["show_fw"]:
                ax.plot(t_ms, onda_completa, label="Onda Completa", color='#2ca02c', linestyle=':')
                hay_graficos = True
            if config["show_hw_cap"]:
                # El capacitor necesita todo el historial
                hw_cap_full = self.calcular_capacitor(media_onda_full, t_full, rc)
                ax.plot(t_ms, hw_cap_full[puntos_extra:], label="Media Onda + Cap", color='#d62728')
                hay_graficos = True
            if config["show_fw_cap"]:
                fw_cap_full = self.calcular_capacitor(onda_completa_full, t_full, rc)
                ax.plot(t_ms, fw_cap_full[puntos_extra:], label="Onda Completa + Cap", color='#9467bd')
                hay_graficos = True

            ax.set_title(f"Gráfico {i+1} (f={f}Hz, Vmax={v_max}V, RC={rc:.3f}s)", fontsize=10)
            ax.set_ylabel("Voltaje (V)")
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.axhline(0, color='black', linewidth=1)
            
            # Limitar ejes para que no vibre la animación
            ax.set_ylim(-26, 26)
            ax.set_xlim(0, duracion * 1000)
            
            if i == n - 1:
                ax.set_xlabel("Tiempo (ms)")
                
            if hay_graficos:
                ax.legend(loc="upper right", fontsize=8)

        if not es_animacion:
            self.fig.tight_layout()
            self.canvas.draw()
        else:
            self.canvas.draw_idle()