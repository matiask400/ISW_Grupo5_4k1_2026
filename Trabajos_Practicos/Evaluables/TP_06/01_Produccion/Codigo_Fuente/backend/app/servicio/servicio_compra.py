from app.modelos.modelos import ResultadoCompra, SolicitudCompra
from datetime import date, datetime
from collections.abc import Callable
from app.servicio.calendario_parque import CalendarioParque
from datetime import date, datetime, time
import calendar

MINIMO_ENTRADAS_POR_COMPRA = 1
MAXIMO_ENTRADAS_POR_COMPRA = 10
EDAD_MINIMA = 0
EDAD_MAXIMA = 120
HORA_LIMITE_COMPRA_MISMO_DIA = time(17, 30)


def sumar_un_mes(fecha: date) -> date:
    """Misma fecha del mes siguiente; si ese día no existe, el último del mes."""
    anio = fecha.year + fecha.month // 12
    mes = fecha.month % 12 + 1
    ultimo_dia_del_mes = calendar.monthrange(anio, mes)[1]
    return date(anio, mes, min(fecha.day, ultimo_dia_del_mes))

class ServicioCompra:
    def __init__(self, ahora: Callable[[], datetime] = datetime.now, calendario: CalendarioParque | None = None,) -> None:
        self._ahora = ahora
        self._calendario = calendario or CalendarioParque()

    def comprar(self, solicitud: SolicitudCompra) -> ResultadoCompra:
        error = (
            self._validar_fecha(solicitud)
            or self._validar_cantidad(solicitud)
            or self._validar_visitantes(solicitud)
            or self._validar_tipo_pase(solicitud)
            or self._validar_forma_pago(solicitud)
        )
        if error:
            return ResultadoCompra.fallida(error)
        return ResultadoCompra.ok()

    @staticmethod
    def _validar_cantidad(solicitud: SolicitudCompra) -> str | None:
        if solicitud.cantidad < MINIMO_ENTRADAS_POR_COMPRA:
            return "Debe comprar al menos 1 entrada"
        if solicitud.cantidad > MAXIMO_ENTRADAS_POR_COMPRA:
            return f"La cantidad de entradas no puede superar {MAXIMO_ENTRADAS_POR_COMPRA}"
        return None

    @staticmethod
    def _validar_visitantes(solicitud: SolicitudCompra) -> str | None:
        if len(solicitud.edades) != solicitud.cantidad:
            return "Debe indicar la edad de cada visitante"
        if any(not EDAD_MINIMA <= edad <= EDAD_MAXIMA for edad in solicitud.edades):
            return f"Las edades deben estar entre {EDAD_MINIMA} y {EDAD_MAXIMA}"
        return None

    @staticmethod
    def _validar_forma_pago(solicitud: SolicitudCompra) -> str | None:
        if solicitud.forma_pago is None:
            return "Debe seleccionar una forma de pago"
        return None

    @staticmethod
    def _validar_tipo_pase(solicitud: SolicitudCompra) -> str | None:
        if solicitud.tipo_pase is None:
            return "Debe seleccionar un tipo de pase"
        return None

    def _validar_fecha(self, solicitud: SolicitudCompra) -> str | None:
        ahora = self._ahora()
        if solicitud.fecha_visita == ahora.date() and ahora.time() > HORA_LIMITE_COMPRA_MISMO_DIA:
            return "Las compras para el día de hoy se permiten hasta las 17:30"
        if solicitud.fecha_visita < self._ahora().date():
            return "La fecha de visita debe ser hoy o una fecha futura"
        if solicitud.fecha_visita > sumar_un_mes(self._ahora().date()):
            return "Solo se pueden comprar entradas con hasta 1 mes de anticipación"
        if not self._calendario.esta_abierto(solicitud.fecha_visita):
            return "El parque está cerrado en la fecha seleccionada"
        return None
