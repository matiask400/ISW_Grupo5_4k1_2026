import calendar
from collections.abc import Callable
from datetime import datetime
from app.modelos.modelos import ResultadoCompra, SolicitudCompra
from app.servicio.calendario_parque import CalendarioParque
from app.servicio.validador_compra import ValidadorCompra



class ServicioCompra:
    def __init__(
        self,
        ahora: Callable[[], datetime] = datetime.now,
        calendario: CalendarioParque | None = None,
    ) -> None:
        self._validador = ValidadorCompra(ahora, calendario or CalendarioParque())

    def comprar(self, solicitud: SolicitudCompra) -> ResultadoCompra:
        error = self._validador.validar(solicitud)
        if error:
            return ResultadoCompra.fallida(error)
        return ResultadoCompra.ok()
