import calendar
from collections.abc import Callable
from datetime import datetime
from app.modelos.modelos import ResultadoCompra, SolicitudCompra
from app.servicio.calendario_parque import CalendarioParque
from app.servicio.validador_compra import ValidadorCompra,MAXIMO_ENTRADAS_POR_COMPRA
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
        self._entradas_compradas: dict[str, int] = {}


    def comprar(self, solicitud: SolicitudCompra) -> ResultadoCompra:
        error = (
            self._verificar_usuario(solicitud)
            or self._validador.validar(solicitud)
            or self._verificar_limite_por_fecha(solicitud)
        )
        if error:
            return ResultadoCompra.fallida(error)
        email = solicitud.usuario_email
        self._entradas_compradas[email] = self._entradas_compradas.get(email, 0) + solicitud.cantidad
        return ResultadoCompra.ok()

    def _verificar_usuario(self, solicitud: SolicitudCompra) -> str | None:
        if not self._usuarios.esta_registrado(solicitud.usuario_email):
            return "Debe estar registrado para comprar entradas"
        return None

    def _verificar_limite_por_fecha(self, solicitud: SolicitudCompra) -> str | None:
        ya_compradas = self._entradas_compradas.get(solicitud.usuario_email, 0)
        if ya_compradas + solicitud.cantidad > MAXIMO_ENTRADAS_POR_COMPRA:
            return (
                f"Solo puede comprar hasta {MAXIMO_ENTRADAS_POR_COMPRA} entradas por fecha. "
                f"Ya compró {ya_compradas} para ese día"
            )
        return None
