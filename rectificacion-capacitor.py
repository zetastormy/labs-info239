import numpy as np
import matplotlib.pyplot as plt

# Parámetros
f = 50  # frecuencia de red
Vmax = 5  # voltaje pico
t = np.linspace(0, 0.1, 2000)  # 100 ms, buena resolución

# Señal original AC
ac = Vmax * np.sin(2 * np.pi * f * t)

# Media onda: eliminar parte negativa
media_onda = np.maximum(ac, 0)

# Simulación del capacitor (RC)
RC = 0.01  # constante de tiempo RC (más grande = más suave)
suavizada = [media_onda[0]]
for i in range(1, len(t)):
    dt = t[i] - t[i - 1]
    descarga = suavizada[-1] * np.exp(-dt / RC)
    valor = max(media_onda[i], descarga)
    suavizada.append(valor)
suavizada = np.array(suavizada)

# Graficar
plt.figure(figsize=(12, 6))
plt.plot(t * 1000, media_onda, linestyle='--', label='Media Onda (sin capacitor)', color='orange')
plt.plot(t * 1000, suavizada, label='Media Onda + Capacitor', color='green')
plt.title("Rectificación de Media Onda con y sin Capacitor")
plt.xlabel("Tiempo (ms)")
plt.ylabel("Voltaje (V)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
