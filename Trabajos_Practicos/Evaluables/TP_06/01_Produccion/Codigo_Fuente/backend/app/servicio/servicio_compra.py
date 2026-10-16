import calendar
from collections.abc import Callable
from datetime import datetime
from app.modelos.modelos import ResultadoCompra, SolicitudCompra
from app.servicio.calendario_parque import CalendarioParque
from app.servicio.validador_compra import ValidadorCompra
from app.servicio.repositorio_usuarios import RepositorioUsuariosEnMemoria


class ServicioCompra:
    def __init__(
        self,
        usuarios: RepositorioUsuariosEnMemoria,
        ahora: Callable[[], datetime] = datetime.now,
        calendario: CalendarioParque | None = None,
    ) -> None:
        self._usuarios = usuarios
        self._validador = ValidadorCompra(ahora, calendario or CalendarioParque())


    def comprar(self, solicitud: SolicitudCompra) -> ResultadoCompra:
        if not self._usuarios.esta_registrado(solicitud.usuario_email):
            return ResultadoCompra.fallida("Debe estar registrado para comprar entradas")
        error = self._validador.validar(solicitud)
        if error:
            return ResultadoCompra.fallida(error)
        return ResultadoCompra.ok()
