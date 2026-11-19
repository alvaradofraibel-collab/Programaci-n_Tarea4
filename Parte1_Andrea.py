"""Integrante 1 - Clientes."""


import re
from abc import ABC, abstractmethod


# ======================================================================
# EXCEPCIONES
# ======================================================================

class ErrorSoftwareFJ(Exception):
    """Error base del sistema."""


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Datos de cliente incorrectos."""


# ======================================================================
# ENTIDAD
# ======================================================================

class Entidad(ABC):
    """Clase base de la que heredan los objetos con identificador propio
    (Cliente, Reserva, ...).

    El identificador se genera automáticamente (1, 2, 3...) por cada tipo de
    entidad. Es privado y de solo lectura (encapsulación).
    """

    _contadores = {}  # un contador independiente por cada subclase

    def __init__(self):
        tipo = type(self)
        Entidad._contadores[tipo] = Entidad._contadores.get(tipo, 0) + 1
        self.__id = Entidad._contadores[tipo]

    @property
    def id(self):
        """Identificador único (solo lectura)."""
        return self.__id

    @abstractmethod
    def describir(self):
        """Devuelve una descripción en texto de la entidad."""

    def __eq__(self, otro):
        if type(self) is not type(otro):
            return NotImplemented
        return self.__id == otro.id

    def __hash__(self):
        return hash((type(self), self.__id))

    def __str__(self):
        return self.describir()


# ======================================================================
# CLIENTE
# ======================================================================

class Cliente(Entidad):
    """Representa un cliente del sistema de reservas.

    Todos los atributos son privados (encapsulación) y se acceden mediante
    propiedades con setters que validan los datos personales. Si un dato es
    incorrecto se lanza ClienteInvalidoError.
    """

    _LETRAS = "A-Za-zÁÉÍÓÚáéíóúÜü"
    _PATRON_NOMBRE = re.compile(rf"^[{_LETRAS}]+(?: [{_LETRAS}]+)*$")
    _PATRON_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")

    def __init__(self, nombre, email, telefono, documento=None):
        # Primero se valida; el id solo se genera si todos los datos son correctos
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.documento = documento  # opcional
        super().__init__()

    # ---------- nombre ----------
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str):
            raise ClienteInvalidoError("El nombre debe ser texto.")
        valor = " ".join(valor.split())
        if len(valor) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.")
        if not self._PATRON_NOMBRE.match(valor):
            raise ClienteInvalidoError(
                f"El nombre '{valor}' solo puede contener letras y espacios."
            )
        self.__nombre = valor.title()

    # ---------- email ----------
    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        if not isinstance(valor, str) or not self._PATRON_EMAIL.match(valor.strip()):
            raise ClienteInvalidoError(f"El email '{valor}' no es válido.")
        self.__email = valor.strip().lower()

    # ---------- teléfono ----------
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        texto = str(valor).strip().replace(" ", "")
        if not texto.isdigit() or len(texto) != 10 or not texto.startswith("3"):
            raise ClienteInvalidoError(
                f"El teléfono '{valor}' debe tener 10 dígitos y empezar por 3."
            )
        self.__telefono = texto

    # ---------- documento (opcional) ----------
    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        if valor is None:
            self.__documento = None
            return
        texto = str(valor).strip()
        if not texto.isdigit() or not 6 <= len(texto) <= 10:
            raise ClienteInvalidoError(
                f"El documento '{valor}' debe tener entre 6 y 10 dígitos."
            )
        self.__documento = texto

    # ---------- métodos ----------
    def describir(self):
        doc = f" | Doc: {self.documento}" if self.documento else ""
        return f"Cliente #{self.id}: {self.nombre} | {self.email} | Tel: {self.telefono}{doc}"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono,
            "documento": self.documento,
        }


# ======================================================================
# PRUEBA RÁPIDA (solo corre al ejecutar este archivo directamente)
# ======================================================================

if __name__ == "__main__":
    print("1) Cliente válido")
    ana = Cliente("ana gómez", "ana@correo.com", "3101234567")
    print("  ", ana)

    casos_invalidos = [
        ("Email malo", ("Luis Pérez", "luis-correo.com", "3109876543")),
        ("Nombre con número y teléfono con letras", ("Car1os", "carlos@correo.com", "abc123")),
        ("Nombre muy corto", ("Al", "al@correo.com", "3101234567")),
        ("Teléfono que no empieza por 3", ("Ana Gómez", "ana@correo.com", "2101234567")),
    ]
    for i, (titulo, datos) in enumerate(casos_invalidos, start=2):
        print(f"\n{i}) Cliente inválido: {titulo}")
        try:
            Cliente(*datos)
        except ClienteInvalidoError as e:
            print(f"   [ERROR CONTROLADO] {e}")

    print("\n6) Encapsulación: el id no se puede modificar")
    try:
        ana.id = 99
    except AttributeError:
        print("   [OK] El id es de solo lectura") 