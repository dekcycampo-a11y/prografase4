import logging
from abc import ABC, abstractmethod
from datetime import datetime

# CONFIGURACIÓN DE LOGS
logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# EXCEPCIONES PERSONALIZADAS
class ErrorSistema(Exception):
    pass

class DatoInvalidoError(ErrorSistema):
    pass

class ServicioNoDisponibleError(ErrorSistema):
    pass

class ReservaError(ErrorSistema):
    pass


# CLASE ABSTRACTA ENTIDAD
class Entidad(ABC):

    def __init__(self, identificacion):
        if not identificacion:
            raise DatoInvalidoError("Identificación obligatoria")
        self._identificacion = identificacion

    @property
    def identificacion(self):
        return self._identificacion

    @abstractmethod
    def describir(self):
        pass


# CLASE CLIENTE
class Cliente(Entidad):

    def __init__(self, identificacion, nombre, correo, telefono):
        super().__init__(identificacion)

        if not nombre.strip():
            raise DatoInvalidoError("Nombre inválido")

        if "@" not in correo or "." not in correo:
            raise DatoInvalidoError("Correo inválido")

        if not telefono.isdigit() or len(telefono) < 7:
            raise DatoInvalidoError("Teléfono inválido")

        self._nombre = nombre
        self._correo = correo
        self._telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    def describir(self):
        return f"Cliente: {self.nombre} - {self._correo}"


# CLASE ABSTRACTA SERVICIO
class Servicio(Entidad):

    def __init__(self, identificacion, nombre, precio):
        super().__init__(identificacion)

        if precio <= 0:
            raise DatoInvalidoError("Precio inválido")

        self._nombre = nombre
        self._precio = precio
        self._disponible = True

    @property
    def nombre(self):
        return self._nombre

    @property
    def precio(self):
        return self._precio

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, estado):
        if not isinstance(estado, bool):
            raise DatoInvalidoError("Estado inválido")
        self._disponible = estado

    @abstractmethod
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        pass


# SERVICIO DE RESERVA DE SALAS
class ReservaSala(Servicio):

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        if duracion <= 0:
            raise DatoInvalidoError("Duración inválida")
        if not 0 <= descuento <= 100:
            raise DatoInvalidoError("Descuento inválido")
        if impuesto < 0:
            raise DatoInvalidoError("Impuesto inválido")

        total = self.precio * duracion
        total -= total * descuento / 100
        total += total * impuesto / 100
        return total

    def describir(self):
        return f"Sala: {self.nombre}"


# SERVICIO DE ALQUILER DE EQUIPOS
class AlquilerEquipo(Servicio):

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        if duracion <= 0:
            raise DatoInvalidoError("Duración inválida")
        if not 0 <= descuento <= 100:
            raise DatoInvalidoError("Descuento inválido")
        if impuesto < 0:
            raise DatoInvalidoError("Impuesto inválido")

        total = self.precio * duracion
        total -= total * descuento / 100
        total += total * impuesto / 100
        return total

    def describir(self):
        return f"Equipo: {self.nombre}"


# SERVICIO DE ASESORÍAS
class Asesoria(Servicio):

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        if duracion <= 0:
            raise DatoInvalidoError("Duración inválida")
        if not 0 <= descuento <= 100:
            raise DatoInvalidoError("Descuento inválido")
        if impuesto < 0:
            raise DatoInvalidoError("Impuesto inválido")

        total = self.precio * duracion
        total -= total * descuento / 100
        total += total * impuesto / 100
        return total

    def describir(self):
        return f"Asesoría: {self.nombre}"


# CLASE RESERVA
class Reserva(Entidad):

    def __init__(self, identificacion, cliente, servicio, duracion):
        super().__init__(identificacion)

        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("Cliente incorrecto")

        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("Servicio incorrecto")

        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatoInvalidoError("Duración incorrecta")

        if not servicio.disponible:
            raise ServicioNoDisponibleError("Servicio no disponible")

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = "Pendiente"
        self._costo = servicio.calcular_costo(duracion)

    @property
    def estado(self):
        return self._estado

    @property
    def costo(self):
        return self._costo

    def confirmar(self):
        if self._estado != "Pendiente":
            raise ReservaError("No se puede confirmar")
        self._estado = "Confirmada"

    def cancelar(self):
        if self._estado == "Cancelada":
            raise ReservaError("Reserva ya cancelada")
        self._estado = "Cancelada"

    def describir(self):
        return (
            f"Reserva {self.identificacion} | "
            f"Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} | "
            f"Estado: {self._estado} | "
            f"Costo: ${self._costo:,.0f}"
        )


# SISTEMA PRINCIPAL
class SistemaSoftwareFJ:

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("Cliente inválido")

        if any(c.identificacion == cliente.identificacion
               for c in self.clientes):
            raise DatoInvalidoError("Cliente duplicado")

        self.clientes.append(cliente)
        logging.info("Cliente registrado: %s", cliente.nombre)

    def registrar_servicio(self, servicio):
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("Servicio inválido")

        if any(s.identificacion == servicio.identificacion
               for s in self.servicios):
            raise DatoInvalidoError("Servicio duplicado")

        self.servicios.append(servicio)
        logging.info("Servicio registrado: %s", servicio.nombre)

    def crear_reserva(self, identificacion, cliente, servicio, duracion):

        if cliente not in self.clientes:
            raise ReservaError("Cliente no registrado")

        if servicio not in self.servicios:
            raise ReservaError("Servicio no registrado")

        if any(r.identificacion == identificacion
               for r in self.reservas):
            raise ReservaError("Reserva duplicada")

        reserva = Reserva(
            identificacion, cliente, servicio, duracion
        )

        self.reservas.append(reserva)
        logging.info("Reserva creada: %s", identificacion)
        return reserva

    def buscar_reserva(self, identificacion):
        for reserva in self.reservas:
            if reserva.identificacion == identificacion:
                return reserva

        raise ReservaError("Reserva no encontrada")

    def confirmar_reserva(self, identificacion):
        reserva = self.buscar_reserva(identificacion)
        reserva.confirmar()
        logging.info("Reserva confirmada: %s", identificacion)

    def cancelar_reserva(self, identificacion):
        reserva = self.buscar_reserva(identificacion)
        reserva.cancelar()
        logging.info("Reserva cancelada: %s", identificacion)

    def listar_clientes(self):
        for cliente in self.clientes:
            print(cliente.describir())

    def listar_servicios(self):
        for servicio in self.servicios:
            print(servicio.describir())

    def listar_reservas(self):
        for reserva in self.reservas:
            print(reserva.describir())


# ==========================================
# PROGRAMA PRINCIPAL Y PRUEBAS
# ==========================================

def ejecutar_pruebas():

    sistema = SistemaSoftwareFJ()

    print("\n===== SISTEMA SOFTWARE FJ =====")

    # OPERACIÓN 1: Registrar cliente
    try:
        cliente1 = Cliente(
            "101", "Carlos Pérez",
            "carlos@gmail.com", "3001234567"
        )
        sistema.registrar_cliente(cliente1)
        print("1. Cliente registrado correctamente")

    except ErrorSistema as e:
        logging.exception("Error al registrar cliente")
        print("Error:", e)

    # OPERACIÓN 2: Registrar segundo cliente
    try:
        cliente2 = Cliente(
            "102", "María López",
            "maria@gmail.com", "3101234567"
        )
        sistema.registrar_cliente(cliente2)
        print("2. Segundo cliente registrado")

    except ErrorSistema as e:
        logging.exception("Error al registrar cliente")
        print("Error:", e)

    # OPERACIÓN 3: Intentar registrar cliente inválido
    try:
        cliente_invalido = Cliente(
            "103", "Pedro", "correo incorrecto", "123"
        )
        sistema.registrar_cliente(cliente_invalido)

    except ErrorSistema as e:
        logging.exception("Registro de cliente inválido")
        print("3. Error controlado:", e)

    # OPERACIÓN 4: Registrar reserva de sala
    try:
        sala = ReservaSala("S01", "Sala de reuniones", 50000)
        sistema.registrar_servicio(sala)
        print("4. Sala registrada")

    except ErrorSistema as e:
        logging.exception("Error al registrar sala")
        print("Error:", e)

    # OPERACIÓN 5: Registrar alquiler de equipo
    try:
        equipo = AlquilerEquipo("E01", "Computador", 30000)
        sistema.registrar_servicio(equipo)
        print("5. Equipo registrado")

    except ErrorSistema as e:
        logging.exception("Error al registrar equipo")
        print("Error:", e)

    # OPERACIÓN 6: Registrar asesoría
    try:
        asesoria = Asesoria("A01", "Asesoría informática", 80000)
        sistema.registrar_servicio(asesoria)
        print("6. Asesoría registrada")

    except ErrorSistema as e:
        logging.exception("Error al registrar asesoría")
        print("Error:", e)

    # OPERACIÓN 7: Intentar registrar servicio inválido
    try:
        servicio_invalido = ReservaSala(
            "S02", "Sala inválida", -100
        )
        sistema.registrar_servicio(servicio_invalido)

    except ErrorSistema as e:
        logging.exception("Servicio inválido")
        print("7. Error controlado:", e)

    # OPERACIÓN 8: Crear reserva correctamente
    try:
        reserva1 = sistema.crear_reserva(
            "R01", cliente1, sala, 2
        )
        print("8. Reserva creada:", reserva1.describir())

    except ErrorSistema as e:
        logging.exception("Error al crear reserva")
        print("Error:", e)

    # OPERACIÓN 9: Confirmar reserva
    try:
        sistema.confirmar_reserva("R01")
        print("9. Reserva confirmada")

    except ErrorSistema as e:
        logging.exception("Error al confirmar reserva")
        print("Error:", e)

    # OPERACIÓN 10: Crear segunda reserva
    try:
        reserva2 = sistema.crear_reserva(
            "R02", cliente2, equipo, 3
        )
        print("10. Segunda reserva creada")

    except ErrorSistema as e:
        logging.exception("Error al crear reserva")
        print("Error:", e)

    # OPERACIÓN 11: Cancelar reserva
    try:
        sistema.cancelar_reserva("R02")
        print("11. Reserva cancelada")

    except ErrorSistema as e:
        logging.exception("Error al cancelar reserva")
        print("Error:", e)

    # OPERACIÓN 12: Intentar reservar servicio no registrado
    try:
        sistema.crear_reserva(
            "R03", cliente1, Asesoria("A02", "Asesoría", 50000), 2
        )

    except ErrorSistema as e:
        logging.exception("Intento de reserva incorrecto")
        print("12. Error controlado:", e)

    # OPERACIÓN 13: Crear reserva de asesoría
    try:
        reserva3 = sistema.crear_reserva(
            "R03", cliente1, asesoria, 2
        )
        print("13. Reserva de asesoría creada")

    except ErrorSistema as e:
        logging.exception("Error en asesoría")
        print("Error:", e)

    # OPERACIÓN 14: Calcular costo con descuento e impuesto
    try:
        costo = sala.calcular_costo(
            2, descuento=10, impuesto=19
        )
        print("14. Costo con descuento e impuesto: $", costo)

    except ErrorSistema as e:
        logging.exception("Error en cálculo")
        print("Error:", e)

    # OPERACIÓN 15: Intentar confirmar una reserva inexistente
    try:
        sistema.confirmar_reserva("R99")

    except ErrorSistema as e:
        logging.exception("Reserva inexistente")
        print("15. Error controlado:", e)

    # OPERACIÓN 16: Servicio no disponible
    try:
        equipo.disponible = False
        sistema.crear_reserva("R04", cliente2, equipo, 2)

    except ErrorSistema as e:
        logging.exception("Servicio no disponible")
        print("16. Error controlado:", e)

    finally:
        print("\nProceso de pruebas finalizado.")
        logging.info("Finalización de las pruebas")


# EJECUTAR SISTEMA
if __name__ == "__main__":
    ejecutar_pruebas()