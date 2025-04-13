import numpy as np
import matplotlib.pyplot as plt
import heapq

MEDIA_LLEGADAS = 20
MEDIA_SERVICIO = 12
HORAS_DIA = 10
CAPACIDAD = 10
DIAS_SIMULACION = 10000
mu_servicio = 60 / MEDIA_SERVICIO


def simulacion_un_dia():
    tiempo = 0
    estado_sistema = 0
    coches_perdidos = 0

    eventos = []

    tiempo_llegada = np.random.exponential(1 / MEDIA_LLEGADAS)
    heapq.heappush(eventos, (tiempo_llegada, 'llegada'))

    while tiempo < HORAS_DIA:
        if not eventos:
            break

        tiempo_evento, tipo_evento = heapq.heappop(eventos)
        tiempo = tiempo_evento

        if tipo_evento == 'llegada':
            if estado_sistema < CAPACIDAD:
                estado_sistema += 1
                if estado_sistema == 1:
                    tiempo_servicio = np.random.exponential(1 / mu_servicio)
                    tiempo_salida = tiempo + tiempo_servicio
                    heapq.heappush(eventos, (tiempo_salida, 'salida'))
            else:
                coches_perdidos += 1

            tiempo_llegada = tiempo + np.random.exponential(1 / MEDIA_LLEGADAS)
            heapq.heappush(eventos, (tiempo_llegada, 'llegada'))

        elif tipo_evento == 'salida':
            estado_sistema -= 1
            if estado_sistema > 0:
                tiempo_servicio = np.random.exponential(1 / mu_servicio)
                tiempo_salida = tiempo + tiempo_servicio
                heapq.heappush(eventos, (tiempo_salida, 'salida'))

    return coches_perdidos


coches_perdidos_diarios = []
for _ in range(DIAS_SIMULACION):
    perdidos = simulacion_un_dia()
    coches_perdidos_diarios.append(perdidos)

media_perdidos = np.mean(coches_perdidos_diarios)
desviacion = np.std(coches_perdidos_diarios)
intervalo_confianza = (media_perdidos - 1.96 * desviacion / np.sqrt(DIAS_SIMULACION),
                       media_perdidos + 1.96 * desviacion / np.sqrt(DIAS_SIMULACION))

print(f"Media de coches perdidos por día: {media_perdidos:.2f}")
print(f"Desviación estándar: {desviacion:.2f}")
print(f"Intervalo de confianza 95%: ({intervalo_confianza[0]:.2f}, {intervalo_confianza[1]:.2f})")

# Histograma de resultados
plt.hist(coches_perdidos_diarios, bins=20, edgecolor='black')
plt.title('Distribución de coches perdidos por día')
plt.xlabel('Coches perdidos')
plt.ylabel('Frecuencia')
plt.axvline(media_perdidos, color='red', linestyle='dashed', linewidth=1, label=f'Media: {media_perdidos:.2f}')
plt.legend()
plt.show()