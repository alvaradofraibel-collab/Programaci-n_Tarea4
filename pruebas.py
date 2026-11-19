
# Fase 4 - Pruebas del integrante 3

from alquiler_equipos import AlquilerEquipos
from asesoria_especializada import AsesoriaEspecializada

# Prueba 1: Alquiler de equipos
print("=== ALQUILER DE EQUIPOS ===")

equipo = AlquilerEquipos("Computador", 10000, 2)

print(equipo.describir_servicio())
print("Costo total:", equipo.calcular_costo(3))

# Prueba 2: Asesoría especializada
print("\n=== ASESORIA ESPECIALIZADA ===")

asesoria = AsesoriaEspecializada(
    "Asesoria en Python", 50000, "Programacion"
)

print(asesoria.describir_servicio())
print("Costo total:", asesoria.calcular_costo(2))

# Prueba 3: Validación de errores
print("\n=== PRUEBA DE ERRORES ===")

try:
    equipo.calcular_costo(-2)
except ValueError as error:
    print("Error controlado:", error)

print("\nPruebas finalizadas correctamente.")
