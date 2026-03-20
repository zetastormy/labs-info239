import numpy as np
import matplotlib.pyplot as plt

# Tiempo simulado
t = np.linspace(0, 0.04, 1000)  # 40 ms (~2 ciclos de 50 Hz)

# Señal DC: constante
dc_voltage = np.full_like(t, 5)  # 5 Voltios constantes

# Señal AC: senoide
frequency = 1200  # Hz (frecuencia de red eléctrica)
amplitude = 5   # voltios
ac_voltage = amplitude * np.sin(2 * np.pi * frequency * t)

# Crear gráfico
plt.figure(figsize=(10, 5))
plt.plot(t * 1000, dc_voltage, label="Corriente Continua (DC)", linestyle='--')
plt.plot(t * 1000, ac_voltage, label="Corriente Alterna (AC)")
plt.title("Comparación entre Corriente Continua y Corriente Alterna")
plt.xlabel("Tiempo (ms)")
plt.ylabel("Voltaje (V)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()