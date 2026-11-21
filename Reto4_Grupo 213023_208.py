# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# ESCUELA DE CIENCIAS BÁSICAS TECNOLOGÍA E INGENIERÍA
# CURSO: PROGRAMACIÓN
# FASE 4
# SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS


from abc import ABC, abstractmethod
from enum import Enum
import logging


# APORTE INTEGRANTE 4
# Registro de eventos y errores mediante logs
# Archivo original: Participante 4.py


logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# APORTE INTEGRANTE 1
# Funcionalidades:
# - Excepciones personalizadas
# - Clase abstracta Entidad
# - Clase Cliente
# - Encapsulación y validaciones

# EXCEPCIONES PERSONALIZADAS


class ErrorSoftwareFJ(Exception):
    pass

class ClienteInvalidoError(ErrorSoftwareFJ):
    pass

class ReservaError(ErrorSoftwareFJ):
    pass

class ServicioNoDisponibleError(ErrorSoftwareFJ):
    pass


# CLASE ABSTRACTA ENTIDAD


class Entidad(ABC):

    @abstractmethod
    def mostrar_info(self):
        pass


# CLIENTE


class Cliente(Entidad):

    def __init__(self, nombre, identificacion, correo):
        if not nombre.strip():
            raise ClienteInvalidoError("Nombre inválido")

        if not identificacion.strip():
            raise ClienteInvalidoError("Identificación inválida")

        if "@" not in correo:
            raise ClienteInvalidoError("Correo inválido")

        self.__nombre = nombre
        self.__identificacion = identificacion
        self.__correo = correo

    @property
    def nombre(self):
        return self.__nombre

    @property
    def identificacion(self):
        return self.__identificacion

    @property
    def correo(self):
        return self.__correo

    def mostrar_info(self):
        return (
            f"Cliente: {self.__nombre}\n"
            f"ID: {self.__identificacion}\n"
            f"Correo: {self.__correo}"
        )


# APORTE INTEGRANTE 2
# Funcionalidades:
# - Clase abstracta Servicio
# - Clase ReservaSalas
# - Herencia y polimorfismo
# - Cálculo de costos con validaciones

# SERVICIO ABSTRACTO


class Servicio(ABC):

    def __init__(self, nombre, tarifa_hora):
        if not nombre.strip():
            raise ValueError("Nombre inválido")

        if tarifa_hora <= 0:
            raise ValueError("Tarifa inválida")

        self._nombre = nombre
        self._tarifa_hora = tarifa_hora
        self.disponible = True

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_hora(self):
        return self._tarifa_hora

    @abstractmethod
    def validar_parametros(self, duracion):
        pass

    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass


# RESERVA DE SALAS


class ReservaSalas(Servicio):

    def __init__(self, nombre, tarifa_hora, capacidad):
        super().__init__(nombre, tarifa_hora)
        self.capacidad = capacidad

    def validar_parametros(self, duracion):
        if duracion <= 0:
            raise ValueError("Duración inválida")

    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        self.validar_parametros(duracion)

        subtotal = self.tarifa_hora * duracion

        subtotal += subtotal * impuesto / 100
        subtotal -= subtotal * descuento / 100

        return subtotal

    def describir_servicio(self):
        return (
            f"Reserva de sala: {self.nombre} "
            f"(Capacidad {self.capacidad})"
        )


# APORTE INTEGRANTE 3
# Servicio especializado: Alquiler de Equipos

class AlquilerEquipos(Servicio):
    """Gestiona el alquiler de equipos."""

    def __init__(self, nombre, tarifa_hora, cantidad):
        super().__init__(nombre, tarifa_hora)

        if not isinstance(cantidad, int):
            raise ValueError(
                "La cantidad debe ser un número entero."
            )

        if cantidad <= 0:
            raise ValueError(
                "La cantidad debe ser mayor que cero."
            )

        self.__cantidad = cantidad

    def validar_parametros(self, duracion):

        if not isinstance(duracion, (int, float)):
            raise ValueError(
                "La duración debe ser numérica."
            )

        if duracion <= 0:
            raise ValueError(
                "La duración debe ser mayor que cero."
            )

        return True

    def calcular_costo(
        self,
        duracion,
        impuesto=0,
        descuento=0
    ):

        self.validar_parametros(duracion)

        subtotal = (
            self.tarifa_hora
            * duracion
            * self.__cantidad
        )

        subtotal += subtotal * impuesto / 100
        subtotal -= subtotal * descuento / 100

        return subtotal

    def describir_servicio(self):
        return (
            f"Alquiler de {self.__cantidad} equipo(s): "
            f"{self.nombre}"
        )


# APORTE INTEGRANTE 3
# Servicio especializado: Asesoría Especializada


class AsesoriaEspecializada(Servicio):
    """Gestiona asesorías especializadas."""

    def __init__(
        self,
        nombre,
        tarifa_hora,
        especialidad
    ):
        super().__init__(nombre, tarifa_hora)

        if (
            not isinstance(especialidad, str)
            or not especialidad.strip()
        ):
            raise ValueError(
                "La especialidad no puede estar vacía."
            )

        self.__especialidad = especialidad.strip()

    def validar_parametros(self, duracion):

        if not isinstance(duracion, (int, float)):
            raise ValueError(
                "La duración debe ser numérica."
            )

        if duracion <= 0:
            raise ValueError(
                "La duración debe ser mayor que cero."
            )

        return True

    def calcular_costo(
        self,
        duracion,
        impuesto=0,
        descuento=0
    ):

        self.validar_parametros(duracion)

        subtotal = self.tarifa_hora * duracion

        subtotal += subtotal * impuesto / 100
        subtotal -= subtotal * descuento / 100

        return subtotal

    def describir_servicio(self):
        return (
            f"Asesoría especializada en "
            f"{self.__especialidad}: "
            f"{self.nombre}"
        )


# APORTE INTEGRANTE 4
# Estados de Reserva
# Gestión de Reservas
# Gestor Principal
# Manejo Avanzado de Excepciones

# ESTADOS DE RESERVA


class EstadoReserva(Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"



# RESERVA


class Reserva:

    def __init__(
        self,
        cliente,
        servicio,
        duracion
    ):
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = EstadoReserva.PENDIENTE

    def confirmar(self):

        if not self.servicio.disponible:
            raise ServicioNoDisponibleError(
                "Servicio no disponible"
            )

        self.estado = EstadoReserva.CONFIRMADA

        logging.info(
            f"Reserva confirmada para "
            f"{self.cliente.nombre}"
        )

    def cancelar(self):

        self.estado = EstadoReserva.CANCELADA

        logging.warning(
            f"Reserva cancelada por "
            f"{self.cliente.nombre}"
        )

    def procesar(self):

        try:

            self.confirmar()

            costo = self.servicio.calcular_costo(
                self.duracion
            )

            return costo

        except Exception as e:

            logging.error(str(e))

            raise ReservaError(
                "Error procesando reserva"
            ) from e



# GESTOR PRINCIPAL


class GestorFJ:

    def __init__(self):
        self.clientes = []
        self.reservas = []

    def registrar_cliente(
        self,
        cliente
    ):
        self.clientes.append(cliente)

    def agregar_reserva(
        self,
        reserva
    ):
        self.reservas.append(reserva)

    def mostrar_resumen(self):

        print(
            "\n=== RESUMEN GENERAL ==="
        )

        print(
            f"Clientes registrados: "
            f"{len(self.clientes)}"
        )

        print(
            f"Reservas registradas: "
            f"{len(self.reservas)}"
        )


# INTEGRACIÓN FINAL DEL PROYECTO
# Simulación General del Sistema
# Casos válidos e inválidos
# Demostración del manejo de excepciones
# Registro de eventos y errores


if __name__ == "__main__":

    gestor = GestorFJ()

    try:

        print("=" * 50)
        print("SISTEMA SOFTWARE FJ")
        print("=" * 50)

     
        # REGISTRO DE CLIENTES
      

        c1 = Cliente(
            "Juan Perez",
            "1001",
            "juan@gmail.com"
        )

        c2 = Cliente(
            "Maria Lopez",
            "1002",
            "maria@gmail.com"
        )

        gestor.registrar_cliente(c1)
        gestor.registrar_cliente(c2)

        print("\nCLIENTES REGISTRADOS")
        print("------------------------")
        print(c1.mostrar_info())
        print()
        print(c2.mostrar_info())

        
        # CREACION DE SERVICIOS
      

        s1 = ReservaSalas(
            "Sala Ejecutiva",
            30000,
            15
        )

        s2 = AlquilerEquipos(
            "Computadores",
            10000,
            5
        )

        s3 = AsesoriaEspecializada(
            "Python",
            50000,
            "Programacion"
        )

        print("\nSERVICIOS DISPONIBLES")
        print("------------------------")
        print(s1.describir_servicio())
        print()
        print(s2.describir_servicio())
        print()
        print(s3.describir_servicio())

        # =====================================
        # RESERVAS VALIDAS
        # =====================================

        r1 = Reserva(c1, s1, 3)
        r2 = Reserva(c2, s2, 4)
        r3 = Reserva(c1, s3, 2)

        gestor.agregar_reserva(r1)
        gestor.agregar_reserva(r2)
        gestor.agregar_reserva(r3)

        print("\nRESERVAS PROCESADAS")
        print("------------------------")

        print(
            "Costo reserva sala:",
            r1.procesar()
        )

        print(
            "Costo alquiler equipos:",
            r2.procesar()
        )

        print(
            "Costo asesoria:",
            r3.procesar()
        )

        
        # PRUEBAS DE ERRORES
       

        print("\nPRUEBAS DE EXCEPCIONES")
        print("------------------------")

        try:
            Cliente(
                "",
                "1003",
                "correo@gmail.com"
            )
        except Exception as error:
            print(
                "Error controlado:",
                error
            )

        try:
            Cliente(
                "Pedro",
                "",
                "correo@gmail.com"
            )
        except Exception as error:
            print(
                "Error controlado:",
                error
            )

        try:
            Cliente(
                "Pedro",
                "1004",
                "correo"
            )
        except Exception as error:
            print(
                "Error controlado:",
                error
            )

        try:
            s1.calcular_costo(-1)
        except Exception as error:
            print(
                "Error controlado:",
                error
            )

        try:
            s2.calcular_costo(0)
        except Exception as error:
            print(
                "Error controlado:",
                error
            )

        try:
            s3.calcular_costo(-5)
        except Exception as error:
            print(
                "Error controlado:",
                error
            )

        
        # RESUMEN DEL SISTEMA
     

        gestor.mostrar_resumen()

    except Exception as error:

        logging.critical(
            f"Error general: {error}"
        )

        print(
            "\nError general del sistema:",
            error
        )

    finally:

        print(
            "\nSistema finalizado correctamente."
        )