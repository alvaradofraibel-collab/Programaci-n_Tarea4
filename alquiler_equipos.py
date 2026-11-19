
# Fase 4 - Integrante 3
# Servicio especializado: Alquiler de equipos

from servicio import Servicio


class AlquilerEquipos(Servicio):
    """Gestiona el alquiler de equipos."""

    def __init__(self, nombre, precio_hora, cantidad):
        super().__init__(nombre, precio_hora)

        if not isinstance(cantidad, int) or isinstance(cantidad, bool):
            raise ValueError("La cantidad debe ser un número entero.")

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        self.__cantidad = cantidad

    def validar_parametros(self, duracion):
        if isinstance(duracion, bool) or not isinstance(
            duracion, (int, float)
        ):
            raise ValueError("La duración debe ser numérica.")

        if duracion <= 0:
            raise ValueError("La duración debe ser mayor que cero.")

        return True

    def calcular_costo(self, duracion):
        self.validar_parametros(duracion)
        return self.precio_hora * duracion * self.__cantidad

    def describir_servicio(self):
        return (
            f"Alquiler de {self.__cantidad} equipo(s): "
            f"{self.nombre}"
        )
