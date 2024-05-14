import random
from datetime import datetime, timedelta

# Genera una fecha aleatoria entre dos fechas específicas
def fecha_aleatoria(fecha_inicio, fecha_fin):
    diferencia = fecha_fin - fecha_inicio
    dias = random.randint(0, diferencia.days)
    return fecha_inicio + timedelta(days=dias)

# Ejemplo de uso
fecha_inicio = datetime(2000, 1, 1)
fecha_fin = datetime(2024, 12, 31)

fecha_aleatoria = fecha_aleatoria(fecha_inicio, fecha_fin)
print("Fecha aleatoria generada:", fecha_aleatoria)