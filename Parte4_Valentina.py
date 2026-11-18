#Parte 4 - Integracion y reservas

import logging
from enum import Enum


#EXCEPCIONES PERSONALIZADAS 


class ErrorSoftwareFJ(Exception):
    """Error base del sistema."""


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Datos de cliente incorrectos."""


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Datos o parámetros de servicio incorrectos."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """El servicio existe pero no se puede reservar ahora."""


class ReservaInvalidaError(ErrorSoftwareFJ):
    """No se pudo crear la reserva."""


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Operación que no corresponde al estado actual (ej. cancelar algo ya cancelado)."""


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """El cálculo de costos dio un resultado imposible o recibió valores absurdos."""



#CONFIGURACIÓN  logs.txt 
logging.basicConfig(
    filename="logs.txt",
    filemode="w",  # "w" = log limpio en cada ejecución; usa "a" si prefieres acumular
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)
log = logging.getLogger("SoftwareFJ")


#RESERVA 

class EstadoReserva(Enum):
    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"
    PROCESADA = "procesada"


class Reserva(Entidad):
    IVA = 0.19

    def __init__(self, cliente, servicio, horas):
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva necesita un Cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva necesita un Servicio válido.")
        try:
            servicio.validar_parametros(horas)
        except ServicioInvalidoError as e:
            # ENCADENAMIENTO: "from e" guarda el error original como causa.
            raise ReservaInvalidaError("Duración no válida para este servicio.") from e
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = EstadoReserva.PENDIENTE
        self._costo_final = None
        super().__init__()

    @property
    def estado(self):
        return self._estado

    def confirmar(self):
        if self._estado != EstadoReserva.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"Reserva #{self.id}: solo se confirma una reserva pendiente (está {self._estado.value})."
            )
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(f"'{self._servicio.nombre}' no está disponible.")
        self._estado = EstadoReserva.CONFIRMADA

    def cancelar(self, motivo="sin motivo indicado"):
        if self._estado in (EstadoReserva.CANCELADA, EstadoReserva.PROCESADA):
            raise OperacionNoPermitidaError(
                f"Reserva #{self.id}: no se puede cancelar, ya está {self._estado.value}."
            )
        self._estado = EstadoReserva.CANCELADA
        log.info("Reserva #%s cancelada (%s)", self.id, motivo)

    def procesar(self, descuento=0.0):
        """Calcula el costo final. Demuestra try / except / else / finally."""
        try:
            if self._estado != EstadoReserva.CONFIRMADA:
                raise OperacionNoPermitidaError(
                    f"Reserva #{self.id}: debe estar confirmada para procesarse (está {self._estado.value})."
                )
            costo = self._servicio.calcular_costo(self._horas, descuento, self.IVA)
        except ValueError as e:
            # Error "genérico" de Python convertido a error propio, con causa original
            raise CalculoInconsistenteError(f"Reserva #{self.id}: parámetros de cálculo inválidos.") from e
        else:
            # Solo se ejecuta si NO hubo excepción
            self._costo_final = costo
            self._estado = EstadoReserva.PROCESADA
            log.info("Reserva #%s procesada. Total con IVA: $%s", self.id, f"{costo:,.2f}")
            return costo
        finally:
            # Se ejecuta SIEMPRE (haya error o no)
            log.info("Fin del intento de procesamiento de la reserva #%s", self.id)

    def describir(self):
        total = f"${self._costo_final:,.2f}" if self._costo_final is not None else "pendiente de cálculo"
        return (f"Reserva #{self.id}: {self._cliente.nombre} -> {self._servicio.nombre} "
                f"({self._horas} h) | {self._estado.value} | Total: {total}")


#GESTOR 
class GestorFJ:
    TIPOS_SERVICIO = {"sala": ReservaSalas, "equipo": AlquilerEquipos, "asesoria": AsesoriaEspecializada}

    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []

    @staticmethod
    def _registrar_error(contexto, error):
        mensaje = f"{contexto} -> {type(error).__name__}: {error}"
        if error.__cause__ is not None:  # si hay una causa encadenada, también se registra
            mensaje += f" | causa: {type(error.__cause__).__name__}: {error.__cause__}"
        log.error(mensaje)
        print(f"   [ERROR CONTROLADO] {mensaje}")

    def registrar_cliente(self, nombre, email, telefono):
        try:
            cliente = Cliente(nombre, email, telefono)
        except ClienteInvalidoError as e:
            self._registrar_error("Registro de cliente", e)
            return None
        else:
            self._clientes.append(cliente)
            log.info("Cliente registrado: %s", cliente.describir())
            print(f"   [OK] {cliente.describir()}")
            return cliente

    def crear_servicio(self, tipo, **datos):
        try:
            clase = self.TIPOS_SERVICIO[tipo]
            servicio = clase(**datos)  # si faltan datos, Python lanza TypeError
        except KeyError:
            self._registrar_error("Creación de servicio", ServicioInvalidoError(f"Tipo desconocido: {tipo!r}"))
            return None
        except TypeError as e:
            # parámetros faltantes o sobrantes
            error = ServicioInvalidoError("Parámetros faltantes o incorrectos.")
            error.__cause__ = e
            self._registrar_error("Creación de servicio", error)
            return None
        except ServicioInvalidoError as e:
            self._registrar_error("Creación de servicio", e)
            return None
        else:
            self._servicios.append(servicio)
            log.info("Servicio creado: %s", servicio.describir())
            print(f"   [OK] {servicio.describir()}")
            return servicio

    def crear_reserva(self, cliente, servicio, horas):
        try:
            reserva = Reserva(cliente, servicio, horas)
        except ReservaInvalidaError as e:
            self._registrar_error("Creación de reserva", e)
            return None
        else:
            self._reservas.append(reserva)
            log.info("Reserva creada: %s", reserva.describir())
            print(f"   [OK] {reserva.describir()}")
            return reserva

    def ejecutar(self, descripcion, accion):
        """Ejecuta cualquier operación sobre una reserva sin que el programa se caiga."""
        try:
            resultado = accion()
        except ErrorSoftwareFJ as e:  # errores propios del sistema
            self._registrar_error(descripcion, e)
        except Exception as e:  # cualquier imprevisto: se registra y se sigue
            self._registrar_error(f"{descripcion} (error inesperado)", e)
        else:
            print(f"   [OK] {descripcion}" + (f" -> ${resultado:,.2f}" if resultado else ""))
            return resultado

    def resumen(self):
        print("\n=== RESUMEN FINAL ===")
        print(f"Clientes: {len(self._clientes)} | Servicios: {len(self._servicios)} | "
              f"Reservas: {len(self._reservas)}")
        for r in self._reservas:
            print("  ", r.describir())

#SIMULACIÓN Y MAIN
def simular():
    g = GestorFJ()
    log.info("===== INICIO DE LA SIMULACIÓN =====")

    print("\n1) Cliente válido")
    ana = g.registrar_cliente("ana gómez", "ana@correo.com", "3101234567")

    print("\n2) Cliente inválido (email malo)")
    g.registrar_cliente("Luis Pérez", "luis-correo.com", "3109876543")

    print("\n3) Cliente inválido (teléfono con letras y nombre con número)")
    g.registrar_cliente("Car1os", "carlos@correo.com", "abc123")

    print("\n4) Servicio válido: sala")
    sala = g.crear_servicio("sala", nombre="Sala Ejecutiva", tarifa_hora=50000, capacidad=10)

    print("\n5) Servicio válido: equipo")
    equipo = g.crear_servicio("equipo", nombre="Portátil Pro", tarifa_hora=8000, tipo_equipo="Portátil")

    print("\n6) Servicio válido: asesoría")
    asesoria = g.crear_servicio("asesoria", nombre="Asesoría Cloud", tarifa_hora=120000, nivel="senior")

    print("\n7) Servicio inválido (falta el parámetro 'capacidad')")
    g.crear_servicio("sala", nombre="Sala Fantasma", tarifa_hora=40000)

    print("\n8) Servicio inválido (tarifa negativa)")
    g.crear_servicio("equipo", nombre="Proyector", tarifa_hora=-500, tipo_equipo="Proyector")

    print("\n9) Reserva válida: confirmar y procesar (con 10 % de descuento)")
    r1 = g.crear_reserva(ana, sala, 3)
    g.ejecutar("Confirmar reserva de sala", r1.confirmar)
    g.ejecutar("Procesar reserva de sala", lambda: r1.procesar(descuento=0.10))

    print("\n10) Reserva fallida: duración excesiva para una asesoría (encadenamiento)")
    g.crear_reserva(ana, asesoria, 20)

    print("\n11) Operación no permitida: procesar sin confirmar y cancelar dos veces")
    r2 = g.crear_reserva(ana, equipo, 5)
    g.ejecutar("Procesar reserva de equipo sin confirmar", r2.procesar)
    g.ejecutar("Cancelar reserva de equipo", lambda: r2.cancelar("el cliente cambió de idea"))
    g.ejecutar("Cancelar reserva de equipo otra vez", r2.cancelar)

    print("\n12) Servicio no disponible y cálculo inconsistente (descuento de 150 %)")
    sala.disponible = False
    r3 = g.crear_reserva(ana, sala, 2)
    g.ejecutar("Confirmar reserva (sala no disponible)", r3.confirmar)
    sala.disponible = True
    g.ejecutar("Confirmar reserva (sala ya disponible)", r3.confirmar)
    g.ejecutar("Procesar reserva con descuento 1.5", lambda: r3.procesar(descuento=1.5))

    g.resumen()
    log.info("===== FIN DE LA SIMULACIÓN: el sistema siguió activo todo el tiempo =====")


if __name__ == "__main__":
    simular()
