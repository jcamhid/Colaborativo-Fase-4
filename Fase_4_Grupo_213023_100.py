# GESTIÓN SOFTWARE FJ (FASE 4 - componente practico)
# PARTICIPANTE 1: JENIFER ALEXANDRA SANCHEZ VARGAS

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
        self.ventana.geometry("980x700")
        self.ventana.minsize(820, 580)
        self.clientes = []
        self.servicios = []
        self.reservas = []
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

        pie = ttk.Frame(self.ventana)
        pie.pack(fill="x", padx=15, pady=5)

        ttk.Button(
            pie,
            text="Consultar registros del sistema",
            command=self.consultar_logs
        ).pack(side="left", padx=5)

        ttk.Button(
            pie,
            text="Simular 10+ operaciones",
            command=self.simular_operaciones
        ).pack(side="left", padx=5)

        tk.Label(
            pie,
            text="Software FJ | Gestión empresarial",
            foreground="gray"
        ).pack(side="right", padx=5)

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
        registro_ok = False
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
            self._actualizar_combos()
            registro_ok = True

        except ErrorSistema as error:
            logging.error(f"Error al registrar cliente: {error}")
            messagebox.showerror("Error de registro", str(error))

        except Exception as error:
            logging.exception("Error inesperado al registrar cliente.")
            messagebox.showerror(
                "Error inesperado",
                "No fue posible completar el registro."
            )
        else:
            for entrada in self.campos.values():
                entrada.delete(0, tk.END)
            messagebox.showinfo(
                "Registro exitoso",
                "El cliente fue registrado correctamente."
            )
        finally:
            if registro_ok:
                logging.info("Flujo de registro de cliente finalizado.")

    def crear_servicios(self):
        ttk.Label(
            self.tab_servicios,
            text="Gestión de servicios",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # Ingreso manual de servicios por parte del usuario
        marco_srv = ttk.LabelFrame(self.tab_servicios, text="Registrar servicio")
        marco_srv.pack(fill="x", padx=20, pady=5)

        ttk.Label(marco_srv, text="Tipo:").grid(row=0, column=0, padx=10, pady=4, sticky="w")
        self.cb_tipo_srv = ttk.Combobox(
            marco_srv,
            values=["Reserva de Salas", "Alquiler de Equipos", "Asesorías Especializadas"],
            state="readonly",
            width=30
        )
        self.cb_tipo_srv.grid(row=0, column=1, padx=10, pady=4, sticky="w")
        self.cb_tipo_srv.current(0)

        ttk.Label(marco_srv, text="Código:").grid(row=1, column=0, padx=10, pady=4, sticky="w")
        self.ent_cod_srv = ttk.Entry(marco_srv, width=33)
        self.ent_cod_srv.grid(row=1, column=1, padx=10, pady=4, sticky="w")

        ttk.Label(marco_srv, text="Tarifa base:").grid(row=2, column=0, padx=10, pady=4, sticky="w")
        self.ent_tar_srv = ttk.Entry(marco_srv, width=33)
        self.ent_tar_srv.grid(row=2, column=1, padx=10, pady=4, sticky="w")

        ttk.Label(marco_srv, text="Capacidad / Equipo / Área:").grid(row=3, column=0, padx=10, pady=4, sticky="w")
        self.ent_det_srv = ttk.Entry(marco_srv, width=33)
        self.ent_det_srv.grid(row=3, column=1, padx=10, pady=4, sticky="w")

        ttk.Button(marco_srv, text="Guardar servicio", command=self.guardar_servicio).grid(row=4, column=0, columnspan=2, pady=8)

        # Cálculo de costo con parámetros opcionales
        marco_calc = ttk.LabelFrame(self.tab_servicios, text="Calcular costo de servicio")
        marco_calc.pack(fill="x", padx=20, pady=5)

        ttk.Label(marco_calc, text="Servicio:").grid(row=0, column=0, padx=10, pady=4, sticky="w")
        self.cb_srv_calc = ttk.Combobox(marco_calc, state="readonly", width=40)
        self.cb_srv_calc.grid(row=0, column=1, padx=10, pady=4, sticky="w")

        ttk.Label(marco_calc, text="Horas / Días / Sesiones:").grid(row=1, column=0, padx=10, pady=4, sticky="w")
        self.ent_cant_calc = ttk.Entry(marco_calc, width=20)
        self.ent_cant_calc.grid(row=1, column=1, padx=10, pady=4, sticky="w")

        ttk.Label(marco_calc, text="Opcional (Desc % / Seguro 1 / IVA):").grid(row=2, column=0, padx=10, pady=4, sticky="w")
        self.ent_opc_calc = ttk.Entry(marco_calc, width=20)
        self.ent_opc_calc.grid(row=2, column=1, padx=10, pady=4, sticky="w")
        self.ent_opc_calc.insert(0, "0")

        ttk.Button(marco_calc, text="Calcular costo", command=self.calcular_costo_srv).grid(row=3, column=0, columnspan=2, pady=6)

        self.txt_lista_srv = tk.Text(self.tab_servicios, height=5, wrap="word", font=("Arial", 10))
        self.txt_lista_srv.pack(fill="both", expand=True, padx=20, pady=5)
        self.txt_lista_srv.config(state="disabled")

    def guardar_servicio(self):
        try:
            tipo = self.cb_tipo_srv.get()
            cod = self.ent_cod_srv.get().strip()
            tar = self.ent_tar_srv.get().strip()
            det = self.ent_det_srv.get().strip()

            if not cod or not tar or not det:
                raise ErrorServicio("Complete código, tarifa base y detalle del servicio.")

            if any(s.codigo_servicio == cod for s in self.servicios):
                raise ErrorServicio(f"El código de servicio '{cod}' ya existe.")

            if tipo == "Reserva de Salas":
                try:
                    cap = int(det)
                except ValueError as exc:
                    raise ErrorServicio("La capacidad de la sala debe ser un número entero.") from exc
                srv = ReservaSalas(cod, tar, cap)
            elif tipo == "Alquiler de Equipos":
                srv = AlquilerEquipos(cod, tar, det)
            else:
                srv = AsesoriasEspecializadas(cod, tar, det)

            self.servicios.append(srv)
            self._actualizar_combos()
        except ErrorSistema as err:
            logging.error(f"Error al guardar servicio: {err}")
            messagebox.showerror("Error de servicio", str(err))
        except Exception:
            logging.exception("Error inesperado al guardar servicio.")
            messagebox.showerror("Error inesperado", "No se pudo guardar el servicio.")
        else:
            self.ent_cod_srv.delete(0, tk.END)
            self.ent_tar_srv.delete(0, tk.END)
            self.ent_det_srv.delete(0, tk.END)
            messagebox.showinfo("Servicio guardado", srv.mostrar_detalle())

    def calcular_costo_srv(self):
        try:
            if not self.servicios:
                raise ErrorServicio("No hay servicios registrados.")
            sel = self.cb_srv_calc.get()
            if not sel:
                raise ErrorServicio("Seleccione un servicio.")
            cod = sel.split(" - ")[0]
            srv = next((s for s in self.servicios if s.codigo_servicio == cod), None)
            if srv is None:
                raise ErrorServicio("Servicio no encontrado.")

            cant = self.ent_cant_calc.get().strip()
            opc = self.ent_opc_calc.get().strip() or "0"
            if not cant:
                raise ErrorServicio("Ingrese la cantidad (horas, días o sesiones).")

            if isinstance(srv, ReservaSalas):
                total = srv.calcular_costo(float(cant), descuento_porcentaje=float(opc))
            elif isinstance(srv, AlquilerEquipos):
                seg = opc.lower() in ("1", "true", "si", "sí")
                total = srv.calcular_costo(int(cant), incluye_seguro=seg)
            else:
                iva = float(opc) if float(opc) > 0 else 0.19
                total = srv.calcular_costo(int(cant), impuesto_iva=iva)

            messagebox.showinfo("Costo calculado", f"{srv.mostrar_detalle()}\nTotal: ${total:,.2f}")
        except ErrorSistema as err:
            logging.error(f"Error al calcular costo: {err}")
            messagebox.showerror("Error de cálculo", str(err))
        except ValueError as exc:
            logging.error(f"Dato numérico inválido en cálculo: {exc}")
            messagebox.showerror("Error de formato", "Ingrese valores numéricos válidos.")
        except Exception:
            logging.exception("Error inesperado en cálculo de costo.")
            messagebox.showerror("Error inesperado", "No fue posible calcular el costo.")

    def crear_reservas(self):
        ttk.Label(
            self.tab_reservas,
            text="Gestión de reservas",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        marco_res = ttk.LabelFrame(self.tab_reservas, text="Registrar y administrar reserva")
        marco_res.pack(fill="x", padx=20, pady=5)

        ttk.Label(marco_res, text="Cliente:").grid(row=0, column=0, padx=10, pady=4, sticky="w")
        self.cb_res_cli = ttk.Combobox(marco_res, state="readonly", width=40)
        self.cb_res_cli.grid(row=0, column=1, padx=10, pady=4, sticky="w")

        ttk.Label(marco_res, text="Servicio:").grid(row=1, column=0, padx=10, pady=4, sticky="w")
        self.cb_res_srv = ttk.Combobox(marco_res, state="readonly", width=40)
        self.cb_res_srv.grid(row=1, column=1, padx=10, pady=4, sticky="w")

        ttk.Label(marco_res, text="Duración:").grid(row=2, column=0, padx=10, pady=4, sticky="w")
        self.ent_res_dur = ttk.Entry(marco_res, width=20)
        self.ent_res_dur.grid(row=2, column=1, padx=10, pady=4, sticky="w")

        ttk.Label(marco_res, text="Opcional (Desc / Seguro 1 / IVA):").grid(row=3, column=0, padx=10, pady=4, sticky="w")
        self.ent_res_opc = ttk.Entry(marco_res, width=20)
        self.ent_res_opc.grid(row=3, column=1, padx=10, pady=4, sticky="w")
        self.ent_res_opc.insert(0, "0")

        acciones = ttk.Frame(marco_res)
        acciones.grid(row=4, column=0, columnspan=2, pady=8)
        ttk.Button(acciones, text="Crear y procesar", command=self.crear_reserva_accion).pack(side="left", padx=5)
        ttk.Button(acciones, text="Confirmar", command=self.confirmar_reserva_accion).pack(side="left", padx=5)
        ttk.Button(acciones, text="Cancelar", command=self.cancelar_reserva_accion).pack(side="left", padx=5)

        self.tabla_res = ttk.Treeview(
            self.tab_reservas,
            columns=("cod", "cli", "srv", "dur", "total", "estado"),
            show="headings",
            height=6
        )
        for col, tit in zip(("cod", "cli", "srv", "dur", "total", "estado"), ("Código", "Cliente", "Servicio", "Duración", "Total", "Estado")):
            self.tabla_res.heading(col, text=tit)
            self.tabla_res.column(col, width=140)
        self.tabla_res.pack(fill="both", expand=True, padx=20, pady=8)

    def _actualizar_combos(self):
        vals_cli = [f"{c.identificacion} - {c.nombre}" for c in self.clientes]
        self.cb_res_cli["values"] = vals_cli
        if vals_cli:
            self.cb_res_cli.current(0)

        vals_srv = [f"{s.codigo_servicio} - {s.nombre_servicio}" for s in self.servicios]
        self.cb_srv_calc["values"] = vals_srv
        self.cb_res_srv["values"] = vals_srv
        if vals_srv:
            self.cb_srv_calc.current(0)
            self.cb_res_srv.current(0)

        self.txt_lista_srv.config(state="normal")
        self.txt_lista_srv.delete("1.0", tk.END)
        for s in self.servicios:
            self.txt_lista_srv.insert(tk.END, f"- {s.mostrar_detalle()}\n")
        self.txt_lista_srv.config(state="disabled")

    def _actualizar_tabla_reservas(self):
        for fila in self.tabla_res.get_children():
            self.tabla_res.delete(fila)
        for r in self.reservas:
            self.tabla_res.insert("", "end", values=(
                r.codigo_reserva,
                f"{r.cliente.identificacion} - {r.cliente.nombre}",
                r.servicio.nombre_servicio,
                r.duracion,
                f"${r.costo_total:,.2f}",
                r.estado
            ))

    def crear_reserva_accion(self):
        try:
            if not self.clientes:
                raise ErrorReserva("Debe registrar al menos un cliente.")
            if not self.servicios:
                raise ErrorReserva("Debe registrar al menos un servicio.")

            sel_cli = self.cb_res_cli.get()
            sel_srv = self.cb_res_srv.get()
            dur = self.ent_res_dur.get().strip()
            opc = self.ent_res_opc.get().strip() or "0"

            if not sel_cli or not sel_srv or not dur:
                raise ErrorReserva("Seleccione cliente, servicio e indique la duración.")

            id_cli = sel_cli.split(" - ")[0]
            cod_srv = sel_srv.split(" - ")[0]

            cli = next((c for c in self.clientes if c.identificacion == id_cli), None)
            srv = next((s for s in self.servicios if s.codigo_servicio == cod_srv), None)

            if cli is None:
                raise ErrorCliente("Cliente no encontrado.")
            if srv is None:
                raise ErrorServicio("Servicio no disponible.")

            cod_res = f"R-{len(self.reservas) + 1:03d}"
            res = Reserva(cod_res, cli, srv, dur)
            res.procesar(parametro_opcional=opc)
            self.reservas.append(res)
            self._actualizar_tabla_reservas()
            messagebox.showinfo("Reserva creada", f"Reserva {res.codigo_reserva} procesada (${res.costo_total:,.2f}).")
        except ErrorSistema as err:
            logging.error(f"Error de reserva: {err}")
            messagebox.showerror("Error de reserva", str(err))
        except Exception:
            logging.exception("Error inesperado al crear reserva.")
            messagebox.showerror("Error inesperado", "No se pudo crear la reserva.")

    def _reserva_elegida(self):
        sel = self.tabla_res.selection()
        if not sel:
            raise ErrorReserva("Seleccione una reserva en la tabla.")
        cod = self.tabla_res.item(sel[0], "values")[0]
        res = next((r for r in self.reservas if r.codigo_reserva == cod), None)
        if res is None:
            raise ErrorReserva("Reserva no encontrada.")
        return res

    def confirmar_reserva_accion(self):
        try:
            res = self._reserva_elegida()
            res.confirmar()
            self._actualizar_tabla_reservas()
            messagebox.showinfo("Confirmada", f"Reserva {res.codigo_reserva} confirmada.")
        except ErrorSistema as err:
            logging.error(f"Error al confirmar: {err}")
            messagebox.showerror("Error", str(err))

    def cancelar_reserva_accion(self):
        try:
            res = self._reserva_elegida()
            res.cancelar()
            self._actualizar_tabla_reservas()
            messagebox.showinfo("Cancelada", f"Reserva {res.codigo_reserva} cancelada.")
        except ErrorSistema as err:
            logging.error(f"Error al cancelar: {err}")
            messagebox.showerror("Error", str(err))

    def simular_operaciones(self):
        """Ejecuta 10+ operaciones de prueba (válidas e inválidas) sin base de datos."""
        reporte = []

        def probar(titulo, fn):
            try:
                fn()
            except ErrorSistema as err:
                logging.error(f"[SIMULACIÓN - {titulo}] {err}")
                reporte.append(f"Controlado - {titulo}: {err}")
            except Exception as err:
                logging.exception(f"[SIMULACIÓN - {titulo}] Error inesperado.")
                reporte.append(f"Fallo - {titulo}: {err}")
            else:
                reporte.append(f"OK - {titulo}")

        def p1():
            c = Cliente("1002003001", "Sofia Ramirez", "sofia@mail.com", "3005551122")
            if not any(x.identificacion == c.identificacion for x in self.clientes):
                self.clientes.append(c)
                self.tabla.insert("", "end", values=(c.identificacion, c.nombre, c.correo, c.telefono))

        def p2():
            Cliente("1002003002", "Juan99", "juan@mail.com", "3005551123")

        def p3():
            Cliente("1002003003", "Diana Lopez", "correo_invalido", "3005551124")

        def p4():
            s = ReservaSalas("SL-01", 50000, 8)
            if not any(x.codigo_servicio == s.codigo_servicio for x in self.servicios):
                self.servicios.append(s)

        def p5():
            s = AlquilerEquipos("EQ-01", 30000, "Laptop")
            if not any(x.codigo_servicio == s.codigo_servicio for x in self.servicios):
                self.servicios.append(s)

        def p6():
            s = AsesoriasEspecializadas("AS-01", 100000, "Bases de Datos")
            if not any(x.codigo_servicio == s.codigo_servicio for x in self.servicios):
                self.servicios.append(s)

        def p7():
            ReservaSalas("SL-ERR", -10000, 4)

        def p8():
            r = Reserva(f"SIM-{len(self.reservas)+1}", self.clientes[0], next(x for x in self.servicios if isinstance(x, ReservaSalas)), 2)
            r.procesar("10")
            r.confirmar()
            self.reservas.append(r)

        def p9():
            r = Reserva(f"SIM-{len(self.reservas)+1}", self.clientes[0], next(x for x in self.servicios if isinstance(x, AlquilerEquipos)), 3)
            r.procesar("1")
            self.reservas.append(r)

        def p10():
            r = Reserva(f"SIM-{len(self.reservas)+1}", self.clientes[0], next(x for x in self.servicios if isinstance(x, AsesoriasEspecializadas)), 0)
            r.procesar()

        def p11():
            r = Reserva(f"SIM-{len(self.reservas)+1}", self.clientes[0], next(x for x in self.servicios if isinstance(x, AsesoriasEspecializadas)), 1)
            r.procesar()
            r.cancelar()
            r.confirmar()

        for titulo, fn in [
            ("1. Cliente válido", p1),
            ("2. Cliente inválido (nombre)", p2),
            ("3. Cliente inválido (correo)", p3),
            ("4. Servicio Sala válido", p4),
            ("5. Servicio Equipo válido", p5),
            ("6. Servicio Asesoría válido", p6),
            ("7. Servicio tarifa inválida", p7),
            ("8. Reserva Sala exitosa", p8),
            ("9. Reserva Equipo con seguro", p9),
            ("10. Reserva duración inválida", p10),
            ("11. Reserva cancelada sin reconfirmar", p11),
        ]:
            probar(titulo, fn)

        self._actualizar_combos()
        self._actualizar_tabla_reservas()
        messagebox.showinfo("Simulación", "\n".join(reporte))

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
# (Módulo de Servicios, Clases Abstractas e Hijas con Polimorfismo + Reserva)

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
        except ValueError as exc:
            logging.error(f"Tarifa de servicio inválida: {tarifa}")
            raise ErrorServicio("La tarifa base debe ser un valor numérico positivo.") from exc

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


class Reserva:
    """Integra cliente, servicio, duración y estado con confirmación y cancelación."""
    def __init__(self, codigo_reserva, cliente, servicio, duracion):
        if not isinstance(cliente, Cliente):
            raise ErrorReserva("Cliente no válido para la reserva.")
        if not isinstance(servicio, Servicio):
            raise ErrorReserva("Servicio no válido para la reserva.")
        self.codigo_reserva = codigo_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"
        self.costo_total = 0.0

    def procesar(self, parametro_opcional="0"):
        try:
            if self.estado == "Cancelada":
                raise ErrorReserva("No se puede procesar una reserva cancelada.")
            if isinstance(self.servicio, ReservaSalas):
                self.costo_total = self.servicio.calcular_costo(float(self.duracion), descuento_porcentaje=float(parametro_opcional))
            elif isinstance(self.servicio, AlquilerEquipos):
                seg = str(parametro_opcional).lower() in ("1", "true", "si", "sí")
                self.costo_total = self.servicio.calcular_costo(int(self.duracion), incluye_seguro=seg)
            elif isinstance(self.servicio, AsesoriasEspecializadas):
                iva = float(parametro_opcional) if float(parametro_opcional) > 0 else 0.19
                self.costo_total = self.servicio.calcular_costo(int(self.duracion), impuesto_iva=iva)
            else:
                raise ErrorReserva("Servicio no reconocido.")
            self.estado = "Procesada"
            logging.info(f"Reserva {self.codigo_reserva} procesada: ${self.costo_total}")
        except ErrorServicio as exc:
            self.estado = "Fallida"
            raise ErrorReserva(f"Fallo al procesar reserva {self.codigo_reserva}: {exc}") from exc
        except ValueError as exc:
            self.estado = "Fallida"
            raise ErrorReserva("Parámetro inválido en reserva.") from exc

    def confirmar(self):
        if self.estado == "Cancelada":
            raise ErrorReserva(f"No se puede confirmar la reserva {self.codigo_reserva} porque está cancelada.")
        if self.estado == "Pendiente":
            raise ErrorReserva(f"Procese la reserva {self.codigo_reserva} antes de confirmarla.")
        self.estado = "Confirmada"
        logging.info(f"Reserva {self.codigo_reserva} confirmada.")

    def cancelar(self):
        if self.estado == "Cancelada":
            raise ErrorReserva(f"La reserva {self.codigo_reserva} ya está cancelada.")
        self.estado = "Cancelada"
        logging.info(f"Reserva {self.codigo_reserva} cancelada.")

# Ejecución de la aplicación principal
if __name__ == "__main__":
    ventana = tk.Tk()
    aplicacion = AplicacionSoftwareFJ(ventana)
    ventana.mainloop()
