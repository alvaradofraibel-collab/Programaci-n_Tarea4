
# Clase Servicio provisional para pruebas
# Se reemplazará por la clase del integrante 2

from abc import ABC, abstractmethod


class Servicio(ABC):

    def __init__(self, nombre, precio_hora):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")

        if isinstance(precio_hora, bool) or not isinstance(
            precio_hora, (int, float)
        ):
            raise ValueError("El precio debe ser numérico.")

        if precio_hora <= 0:
            raise ValueError("El precio debe ser mayor que cero.")

        self.nombre = nombre.strip()
        self.precio_hora = precio_hora

    @abstractmethod
    def calcular_costo(self, duracion):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass

    @abstractmethod
    def validar_parametros(self, duracion):
        pass
