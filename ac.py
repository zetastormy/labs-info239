import numpy as np
import matplotlib.pyplot as plt

# Parámetros de la señal
# frecuencia = 100000        # Hz
frecuencia = [v for v in range(0)]
amplitud = 5          # Voltios
duracion = 0.05         # segundos (50 ms)
t = np.linspace(0, duracion, 1000)

# Generar la señal senoidal
senal = amplitud * np.sin(2 * np.pi * frecuencia * t)

# Calcular período
periodo = 1 / frecuencia

# Graficar
plt.figure(figsize=(10, 4))
plt.plot(t * 1000, senal, label=f'{frecuencia} Hz, {amplitud} V')
plt.title("⚡ Señal Eléctrica Alterna (AC)")
plt.xlabel("Tiempo (ms)")
plt.ylabel("Voltaje (V)")
plt.grid(True)
plt.axhline(0, color='black', linewidth=0.5)
plt.legend()
plt.tight_layout()
plt.show()