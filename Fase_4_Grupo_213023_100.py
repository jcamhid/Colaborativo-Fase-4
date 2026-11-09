## PARTICIPANTE 1: JENIFER ALEXANDRA SANCHEZ VARGAS

# Librerías necesarias para el funcionamiento inicial del sistema.
import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod
import logging
import re

# CONFIGURACIÓN DEL ARCHIVO DE LOGS
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

# (Estructura base, Excepciones, Clase Entidad, Cliente e Interfaz Gráfica)

class Entidad(ABC):
    """Clase abstracta que representa una entidad general del sistema."""
    def __init__(self, identificacion):
        self._identificacion = self.validar_identificacion(identificacion)

    @property
    def identificacion(self):
        return self._identificacion

    @staticmethod
    def validar_identificacion(identificacion):
        identificacion = str(identificacion).strip()
        if not identificacion:
            raise ErrorValidacion("La identificación no puede estar vacía.")
        if not identificacion.isdigit():
            raise ErrorValidacion("La identificación debe contener solo números.")
        if not 5 <= len(identificacion) <= 15:
            raise ErrorValidacion("La identificación debe tener entre 5 y 15 dígitos.")
        return identificacion

    @abstractmethod
    def mostrar_informacion(self):
        pass


class Cliente(Entidad):
    """Representa un cliente de Software FJ."""
    def __init__(self, identificacion, nombre, correo, telefono):
        super().__init__(identificacion)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        logging.info(f"Cliente registrado correctamente: {self._identificacion}")

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        nombre = str(nombre).strip()
        if not nombre:
            logging.error("Intento de registrar un nombre vacío.")
            raise ErrorValidacion("El nombre del cliente no puede estar vacío.")
        if len(nombre) < 3:
            logging.error(f"Nombre demasiado corto: {nombre}")
            raise ErrorValidacion("El nombre del cliente debe contener al menos 3 caracteres.")
        if not all(caracter.isalpha() or caracter.isspace() for caracter in nombre):
            logging.error(f"Nombre con caracteres no permitidos: {nombre}")
            raise ErrorValidacion("El nombre del cliente solo puede contener letras y espacios.")
        self._nombre = nombre.title()

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, correo):
        correo = str(correo).strip().lower()
        if not re.fullmatch(r"[\w.-]+@[\w.-]+\.\w+", correo):
            logging.error(f"Correo electrónico inválido: {correo}")
            raise ErrorValidacion("Ingrese un correo electrónico válido.")
        self._correo = correo

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, telefono):
        telefono = str(telefono).strip()
        if not telefono.isdigit() or not 7 <= len(telefono) <= 10:
            logging.error(f"Teléfono inválido: {telefono}")
            raise ErrorValidacion("El teléfono debe tener entre 7 y 10 números.")
        self._telefono = telefono

    def mostrar_informacion(self):
        return f"ID: {self.identificacion} | Nombre: {self.nombre} | Correo: {self.correo} | Teléfono: {self.telefono}"


class AplicacionSoftwareFJ:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Software FJ - Gestión de clientes, servicios y reservas")
        self.ventana.geometry("950x650")
        self.ventana.minsize(800, 550)
        self.clientes = []
        self.crear_interfaz()

    def crear_interfaz(self):
        encabezado = tk.Frame(self.ventana, bg="#19365C")
        encabezado.pack(fill="x")

        tk.Label(
            encabezado, text="SOFTWARE FJ",
            font=("Arial", 23, "bold"),
            bg="#19365C", fg="white"
        ).pack(pady=(15, 3))

        tk.Label(
            encabezado,
            text="Sistema de gestión de clientes, servicios y reservas",
            bg="#19365C", fg="white"
        ).pack(pady=(0, 15))

        self.pestanas = ttk.Notebook(self.ventana)
        self.pestanas.pack(fill="both", expand=True, padx=15, pady=15)

        self.tab_clientes = ttk.Frame(self.pestanas)
        self.tab_servicios = ttk.Frame(self.pestanas)
        self.tab_reservas = ttk.Frame(self.pestanas)

        self.pestanas.add(self.tab_clientes, text="Clientes")
        self.pestanas.add(self.tab_servicios, text="Servicios")
        self.pestanas.add(self.tab_reservas, text="Reservas")

        self.crear_clientes()
        self.crear_servicios()
        self.crear_reservas()

        ttk.Button(
            self.ventana,
            text="Consultar registros del sistema",
            command=self.consultar_logs
        ).pack(pady=5)

        tk.Label(
            self.ventana,
            text="Software FJ | Gestión empresarial",
            fg="gray"
        ).pack(pady=5)

    def crear_clientes(self):
        ttk.Label(
            self.tab_clientes,
            text="Gestión de clientes",
            font=("Arial", 16, "bold")
        ).pack(pady=12)

        formulario = ttk.LabelFrame(
            self.tab_clientes,
            text="Registrar nuevo cliente"
        )
        formulario.pack(fill="x", padx=20, pady=10)

        self.campos = {}

        for fila, campo in enumerate(
            ["Identificación", "Nombre", "Correo", "Teléfono"]
        ):
            ttk.Label(formulario, text=campo + ":").grid(
                row=fila, column=0, padx=10, pady=7, sticky="w"
            )
            entrada = ttk.Entry(formulario, width=40)
            entrada.grid(row=fila, column=1, padx=10, pady=7)
            self.campos[campo] = entrada

        ttk.Button(
            formulario,
            text="Registrar cliente",
            command=self.registrar_cliente
        ).grid(row=4, column=0, columnspan=2, pady=12)

        columnas = ("id", "nombre", "correo", "telefono")
        self.tabla = ttk.Treeview(
            self.tab_clientes,
            columns=columnas,
            show="headings"
        )

        for columna, titulo in zip(
            columnas,
            ["Identificación", "Nombre", "Correo", "Teléfono"]
        ):
            self.tabla.heading(columna, text=titulo)
            self.tabla.column(columna, width=170)

        self.tabla.pack(fill="both", expand=True, padx=15, pady=10)

    def registrar_cliente(self):
        try:
            datos = [
                self.campos[c].get().strip()
                for c in ["Identificación", "Nombre", "Correo", "Teléfono"]
            ]

            if not all(datos):
                raise ErrorValidacion("Todos los campos son obligatorios.")

            if any(c.identificacion == datos[0] for c in self.clientes):
                raise ErrorCliente("El cliente ya se encuentra registrado.")

            cliente = Cliente(*datos)
            self.clientes.append(cliente)

            self.tabla.insert("", "end", values=(
                cliente.identificacion,
                cliente.nombre,
                cliente.correo,
                cliente.telefono
            ))

            for entrada in self.campos.values():
                entrada.delete(0, tk.END)

            messagebox.showinfo(
                "Registro exitoso",
                "El cliente fue registrado correctamente."
            )

        except ErrorSistema as error:
            logging.error(f"Error al registrar cliente: {error}")
            messagebox.showerror("Error de registro", str(error))

        except Exception as error:
            logging.exception("Error inesperado al registrar cliente.")
            messagebox.showerror(
                "Error inesperado",
                "No fue posible completar el registro."
            )

    def crear_servicios(self):
        ttk.Label(
            self.tab_servicios,
            text="Gestión de servicios",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        for servicio in [
            "Reserva de salas",
            "Alquiler de equipos",
            "Asesorías especializadas"
        ]:
            ttk.Label(
                self.tab_servicios,
                text=servicio,
                font=("Arial", 12)
            ).pack(pady=12)

        ttk.Label(
            self.tab_servicios,
            text="Módulo pendiente de integración."
        ).pack(pady=15)

    def crear_reservas(self):
        ttk.Label(
            self.tab_reservas,
            text="Gestión de reservas",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        ttk.Label(
            self.tab_reservas,
            text="Aquí se administrarán las reservas de los clientes."
        ).pack(pady=15)

        ttk.Label(
            self.tab_reservas,
            text="Módulo pendiente de integración."
        ).pack(pady=10)

    def consultar_logs(self):
        ventana_logs = tk.Toplevel(self.ventana)
        ventana_logs.title("Registros del sistema")
        ventana_logs.geometry("750x450")

        texto = tk.Text(ventana_logs, wrap="word", font=("Arial", 10))
        texto.pack(fill="both", expand=True, padx=10, pady=10)

        try:
            with open("sistema.log", "r", encoding="utf-8") as archivo:
                contenido = archivo.read()
                texto.insert(tk.END, contenido or "No hay registros disponibles.")
        except FileNotFoundError:
            texto.insert(tk.END, "Todavía no existen registros.")

        texto.config(state="disabled")

# PARTICIPANTE 2: JULIAN CAMILO HIDALGO CALIZ
# (Módulo de Servicios, Clases Abstractas e Hijas con Polimorfismo)

class Servicio(ABC):
    """Clase abstracta que representa un servicio general ofrecido por Software FJ."""
    def __init__(self, codigo_servicio, nombre_servicio, tarifa_base):
        self._codigo_servicio = self.validar_codigo(codigo_servicio)
        self._nombre_servicio = nombre_servicio
        self._tarifa_base = self.validar_tarifa(tarifa_base)

    @property
    def codigo_servicio(self):
        return self._codigo_servicio

    @property
    def nombre_servicio(self):
        return self._nombre_servicio

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @staticmethod
    def validar_codigo(codigo):
        codigo = str(codigo).strip()
        if not codigo:
            logging.error("Código de servicio vacío.")
            raise ErrorServicio("El código del servicio no puede estar vacío.")
        return codigo

    @staticmethod
    def validar_tarifa(tarifa):
        try:
            t = float(tarifa)
            if t < 0:
                raise ValueError()
            return t
        except ValueError:
            logging.error(f"Tarifa de servicio inválida: {tarifa}")
            raise ErrorServicio("La tarifa base debe ser un valor numérico positivo.")

    @abstractmethod
    def calcular_costo(self, *args, **kwargs):
        """Método abstracto para el cálculo de costos (Polimorfismo)."""
        pass

    @abstractmethod
    def mostrar_detalle(self):
        """Método abstracto para describir el servicio."""
        pass


class ReservaSalas(Servicio):
    """Servicio especializado en la reserva de salas."""
    def __init__(self, codigo, tarifa_base, capacidad_personas):
        super().__init__(codigo, "Reserva de Salas", tarifa_base)
        self.capacidad_personas = capacidad_personas

    def calcular_costo(self, horas, descuento_porcentaje=0):
        if horas <= 0:
            raise ErrorServicio("Las horas de reserva deben ser mayores a cero.")
        subtotal = self.tarifa_base * horas
        descuento = subtotal * (descuento_porcentaje / 100)
        total = subtotal - descuento
        logging.info(f"Costo calculado (Reserva Salas) [{self.codigo_servicio}]: ${total}")
        return total

    def mostrar_detalle(self):
        return f"Sala [{self.codigo_servicio}] - Tarifa/Hora: ${self.tarifa_base} - Capacidad: {self.capacidad_personas} pers."


class AlquilerEquipos(Servicio):
    """Servicio especializado en alquiler de equipos tecnológicos."""
    def __init__(self, codigo, tarifa_base, tipo_equipo):
        super().__init__(codigo, "Alquiler de Equipos", tarifa_base)
        self.tipo_equipo = tipo_equipo

    def calcular_costo(self, dias, incluye_seguro=False):
        if dias <= 0:
            raise ErrorServicio("Los días de alquiler deben ser mayores a cero.")
        subtotal = self.tarifa_base * dias
        seguro = 20000 if incluye_seguro else 0
        total = subtotal + seguro
        logging.info(f"Costo calculado (Alquiler Equipos) [{self.codigo_servicio}]: ${total}")
        return total

    def mostrar_detalle(self):
        return f"Equipo [{self.codigo_servicio}] ({self.tipo_equipo}) - Tarifa/Día: ${self.tarifa_base}"


class AsesoriasEspecializadas(Servicio):
    """Servicio especializado en asesorías profesionales."""
    def __init__(self, codigo, tarifa_base, area_especialidad):
        super().__init__(codigo, "Asesorías Especializadas", tarifa_base)
        self.area_especialidad = area_especialidad

    def calcular_costo(self, sesiones, impuesto_iva=0.19):
        if sesiones <= 0:
            raise ErrorServicio("El número de sesiones debe ser mayor a cero.")
        subtotal = self.tarifa_base * sesiones
        total = subtotal * (1 + impuesto_iva)
        logging.info(f"Costo calculado (Asesorías) [{self.codigo_servicio}]: ${total}")
        return total

    def mostrar_detalle(self):
        return f"Asesoría [{self.codigo_servicio}] en {self.area_especialidad} - Tarifa/Sesión: ${self.tarifa_base}"


# Ejecución de la aplicación principal
if __name__ == "__main__":
    ventana = tk.Tk()
    aplicacion = AplicacionSoftwareFJ(ventana)
    ventana.mainloop()