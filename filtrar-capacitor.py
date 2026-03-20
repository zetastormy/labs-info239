import numpy as np
import matplotlib.pyplot as plt

# Parámetros de la señal
f = 50  # frecuencia en Hz
Vmax = 5  # voltaje máximo
t = np.linspace(0, 0.1, 2000)  # 100 ms

# Señal AC
ac = Vmax * np.sin(2 * np.pi * f * t)

# Rectificación de onda completa
rectificada = np.abs(ac)

# Simulación del efecto del capacitor
# Parámetros de descarga (simulados, no exactos)
RC = 1  # constante de tiempo del filtro (puedes cambiar este valor)
suavizada = [rectificada[0]]
for i in range(1, len(t)):
    descarga = suavizada[-1] * np.exp(-(t[i] - t[i-1]) / RC)
    valor = max(rectificada[i], descarga)
    suavizada.append(valor)
suavizada = np.array(suavizada)

# Graficar
plt.figure(figsize=(12, 6))
plt.plot(t * 1000, rectificada, label="Rectificada (sin capacitor)", linestyle="--")
plt.plot(t * 1000, suavizada, label="Rectificada + Capacitor", linewidth=2)
plt.title("Filtrado de señal rectificada con un capacitor")
plt.xlabel("Tiempo (ms)")
plt.ylabel("Voltaje (V)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()