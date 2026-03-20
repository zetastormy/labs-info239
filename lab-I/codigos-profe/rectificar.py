import numpy as np
import matplotlib.pyplot as plt

# Tiempo de simulación
t = np.linspace(0, 0.04, 1000)  # 40ms (~2 ciclos de 50Hz)

# Señal AC original
frecuencia = 50  # Hz
amplitud = 5  # Voltios
ac = amplitud * np.sin(2 * np.pi * frecuencia * t)

# Rectificación de media onda
media_onda = np.maximum(ac, 0)

# Rectificación de onda completa
onda_completa = np.abs(ac)

# Graficar todo
plt.figure(figsize=(12, 8))

# Señal AC original
plt.subplot(3, 1, 1)
plt.plot(t * 1000, ac, label="Señal AC Original")
plt.title("Corriente Alterna (AC)")
plt.ylabel("Voltaje (V)")
plt.grid(True)
plt.legend()

# Rectificación de media onda
plt.subplot(3, 1, 2)
plt.plot(t * 1000, media_onda, color='orange', label="Media Onda")
plt.title("Rectificación de Media Onda")
plt.ylabel("Voltaje (V)")
plt.grid(True)
plt.legend()

# Rectificación de onda completa
plt.subplot(3, 1, 3)
plt.plot(t * 1000, onda_completa, color='green', label="Onda Completa")
plt.title("Rectificación de Onda Completa")
plt.xlabel("Tiempo (ms)")
plt.ylabel("Voltaje (V)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
