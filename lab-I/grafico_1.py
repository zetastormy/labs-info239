import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Tiempo simulado
t = np.linspace(0, 0.04, 1000)  # 40 ms (~2 ciclos de 50 Hz)

# Señal DC: constante
dc_voltage = np.full_like(t, 5)  # 5 Voltios constantes

# Señal AC: senoide
frequency = 1200  # Hz (frecuencia de red eléctrica)
amplitude = 5   # voltios
ac_voltage = amplitude * np.sin(2 * np.pi * frequency * t)

# Crear gráfico
fig, ax = plt.subplots(figsize=(10, 5))
line_dc, = ax.plot([], [], label="Corriente Continua (DC)", linestyle='--')
line_ac, = ax.plot([], [], label="Corriente Alterna (AC)")
ax.set_xlim(0, 40)  # ms
ax.set_ylim(-6, 6)
ax.set_title("Comparación entre Corriente Continua y Corriente Alterna")
ax.set_xlabel("Tiempo (ms)")
ax.set_ylabel("Voltaje (V)")
ax.grid(True)
ax.legend()

def init():
    line_dc.set_data([], [])
    line_ac.set_data([], [])
    return line_dc, line_ac

def animate(frame):
    # frame va de 0 a len(t)-1
    current_t = t[:frame+1] * 1000
    current_dc = dc_voltage[:frame+1]
    current_ac = ac_voltage[:frame+1]
    line_dc.set_data(current_t, current_dc)
    line_ac.set_data(current_t, current_ac)
    return line_dc, line_ac

anim = FuncAnimation(fig, animate, init_func=init, frames=len(t), interval=50, blit=True)
plt.tight_layout()
plt.show()
