#Aqui se realizara el trabajo colaborativo de la fase 4 del curso de programación del grupo 213023_100

# PARTICIPANTE 1: JENIFER ALEXANDRA SANCHEZ VARGAS

import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod
import logging
import re

# Registro de eventos y errores
logging.basicConfig(
    filename="sistema.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# Excepciones personalizadas
class ErrorSistema(Exception):
    pass

class ErrorValidacion(ErrorSistema):
    pass

class ErrorCliente(ErrorSistema):
    pass

class ErrorServicio(ErrorSistema):
    pass

class ErrorReserva(ErrorSistema):
    pass


# Clase abstracta general
class Entidad(ABC):
    def __init__(self, identificacion):
        self._identificacion = self.validar_identificacion(identificacion)

    @property
    def identificacion(self):
        return self._identificacion

    @staticmethod
    def validar_identificacion(identificacion):
        identificacion = str(identificacion).strip()

        if not identificacion.isdigit():
            raise ErrorValidacion("La identificación debe contener solo números.")

        if not 5 <= len(identificacion) <= 15:
            raise ErrorValidacion("La identificación debe tener entre 5 y 15 dígitos.")

        return identificacion

    @abstractmethod
    def mostrar_informacion(self):
        pass


# Clase Cliente
class Cliente(Entidad):
    def __init__(self, identificacion, nombre, correo, telefono):
        super().__init__(identificacion)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        logging.info(f"Cliente registrado: {self.identificacion}")

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        valor = str(valor).strip()

        if len(valor) < 3 or not all(c.isalpha() or c.isspace() for c in valor):
            raise ErrorValidacion("Ingrese un nombre válido.")

        self._nombre = valor.title()

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        valor = str(valor).strip().lower()

        if not re.fullmatch(r"[\w.-]+@[\w.-]+\.\w+", valor):
            raise ErrorValidacion("Ingrese un correo electrónico válido.")

        self._correo = valor

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        valor = str(valor).strip()

        if not valor.isdigit() or not 7 <= len(valor) <= 10:
            raise ErrorValidacion("El teléfono debe tener entre 7 y 10 números.")

        self._telefono = valor

    def mostrar_informacion(self):
        return (
            f"{self.identificacion} | {self.nombre} | "
            f"{self.correo} | {self.telefono}"
        )


# Interfaz gráfica Software FJ
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

    # Registro de clientes
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

    # Sección de servicios
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

    # Sección de reservas
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

    # Consulta de eventos y errores
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


# Ejecución de la aplicación
if __name__ == "__main__":
    ventana = tk.Tk()
    aplicacion = AplicacionSoftwareFJ(ventana)
    ventana.mainloop()



# PARTICIPANTE 2: XXXXXXXXXXXXX


# PARTICIPANTE 3: XXXXXXXXXXXXX


# PARTICIPANTE 4: XXXXXXXXXXXXX


# PARTICIPANTE 5: XXXXXXXXXXXXX
