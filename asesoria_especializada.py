
# Fase 4 - Integrante 3
# Servicio especializado: Asesoria Especializada

from servicio import Servicio


class AsesoriaEspecializada(Servicio):
    """Gestiona asesorías especializadas."""

    def __init__(self, nombre, precio_hora, especialidad):
        super().__init__(nombre, precio_hora)

        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ValueError("La especialidad no puede estar vacía.")

        self.__especialidad = especialidad.strip()

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
        return self.precio_hora * duracion

    def describir_servicio(self):
        return (
            f"Asesoría especializada en {self.__especialidad}: "
            f"{self.nombre}"
        )
