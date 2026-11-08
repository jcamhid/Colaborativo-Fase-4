#Aqui se realizara el trabajo colaborativo de la fase 4 del curso de programación del grupo 213023_100

# PARTICIPANTE 1: JENIFER ALEXANDRA SANCHEZ VARGAS

# Librerías necesarias para el funcionamiento inicial del sistema.
from abc import ABC, abstractmethod
import logging
import re

# CONFIGURACIÓN DEL ARCHIVO DE LOGS
# Los eventos y errores importantes del sistema se guardarán automáticamente en el archivo sistema.log.
logging.basicConfig(
    filename="sistema.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# EXCEPCIONES PERSONALIZADAS
class ErrorSistema(Exception):
    """Excepción general utilizada por el sistema."""
    pass

class ErrorValidacion(ErrorSistema):
    """Se genera cuando un dato ingresado no es válido."""
    pass
class ErrorCliente(ErrorSistema):
    """Se genera cuando ocurre un problema relacionado con un cliente."""
    pass
class ErrorServicio(ErrorSistema):
    """Se utilizará para los errores relacionados con servicios."""
    pass
class ErrorReserva(ErrorSistema):
    """Se utilizará para los errores relacionados con reservas."""
    pass

# CLASE ABSTRACTA GENERAL
class Entidad(ABC):
    """ Clase abstracta que representa una entidad general del sistema.
    Las demás clases pueden heredar de esta clase para mantener
    una estructura común dentro del programa."""
    def __init__(self, identificacion):
        self._identificacion = self.validar_identificacion(identificacion)
    @property
    def identificacion(self):
        """Permite consultar la identificación de la entidad."""
        return self._identificacion
    @staticmethod
    def validar_identificacion(identificacion):
      
    """Verifica que la identificación tenga un formato válido."""
        identificacion = str(identificacion).strip()
        if not identificacion:
            raise ErrorValidacion(
                "The identification cannot be empty."
            )
        if not identificacion.isdigit():
            raise ErrorValidacion(
                "The identification must contain only numbers."
            )
        if len(identificacion) < 5 or len(identificacion) > 15:
            raise ErrorValidacion(
                "The identification must contain between 5 and 15 digits."
            )
        return identificacion

    @abstractmethod
    def mostrar_informacion(self):
        """
        Método que deberá ser implementado por las clases hijas.
        """
        pass

# CLASE CLIENTE
class Cliente(Entidad):
    """Representa un cliente de Software FJ. Los datos son protegidos mediante encapsulación y se validan
    antes de ser almacenados."""
    def __init__(self, identificacion, nombre, correo, telefono):

        # Inicializa la identificación usando la clase padre.
        super().__init__(identificacion)

        # Se utilizan propiedades para realizar las validaciones.
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

        # Registra la creación correcta del cliente.
        logging.info(
            f"Cliente registrado correctamente: {self._identificacion}"
        )
   
    # NOMBRE
       @property
    def nombre(self):
        return self._nombre
    @nombre.setter
    def nombre(self, nombre):
        nombre = str(nombre).strip()
        if not nombre:
            logging.error("Intento de registrar un nombre vacío.")
            raise ErrorValidacion(
                "The customer name cannot be empty."
            )
        if len(nombre) < 3:
            logging.error(
                f"Nombre demasiado corto: {nombre}"
            )
            raise ErrorValidacion(
                "The customer name must contain at least 3 characters."
            )

        # Solo se permiten letras y espacios.
        if not all(
            caracter.isalpha() or caracter.isspace()
            for caracter in nombre
        ):
            logging.error(
                f"Nombre con caracteres no permitidos: {nombre}"
            )
            raise ErrorValidacion(
                "The customer name can only contain letters and spaces."
            )

        self._nombre = nombre.title()

      # CORREO ELECTRÓNICO
   
    @property
    def correo(self):
        return self._correo
    @correo.setter
    def correo(self, correo):
        correo = str(correo).strip().lower()

        # Expresión regular sencilla para validar el correo.
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron, correo):
            logging.error(
                f"Correo electrónico inválido: {correo}"
            )
            raise ErrorValidacion(
                "The email address is not valid."
            )
        self._correo = correo

    # TELÉFONO
     @property
    def telefono(self):
        return self._telefono
    @telefono.setter
    def telefono(self, telefono):
        telefono = str(telefono).strip()
        if not telefono.isdigit():
            logging.error(
                f"Teléfono inválido: {telefono}"
            )
            raise ErrorValidacion(
                "The phone number must contain only numbers."
            )
        if len(telefono) < 7 or len(telefono) > 10:
            logging.error(
                f"Longitud de teléfono incorrecta: {telefono}"
            )
            raise ErrorValidacion(
                "The phone number must contain between 7 and 10 digits."
            )
        self._telefono = telefono

    # INFORMACIÓN DEL CLIENTE
       def mostrar_informacion(self):
        """
        Retorna la información básica del cliente.
        """
        return (
            f"ID: {self.identificacion} | "
            f"Name: {self.nombre} | "
            f"Email: {self.correo} | "
            f"Phone: {self.telefono}"
        )


# PARTICIPANTE 2: XXXXXXXXXXXXX


# PARTICIPANTE 3: XXXXXXXXXXXXX


# PARTICIPANTE 4: XXXXXXXXXXXXX


# PARTICIPANTE 5: XXXXXXXXXXXXX
