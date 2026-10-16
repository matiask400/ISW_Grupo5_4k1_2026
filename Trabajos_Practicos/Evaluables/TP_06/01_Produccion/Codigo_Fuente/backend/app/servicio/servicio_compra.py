from collections.abc import Callable
from datetime import datetime

from app.modelos.modelos import ResultadoCompra, SolicitudCompra
from app.servicio.calendario_parque import CalendarioParque
from app.servicio.repositorio_compras import RepositorioComprasEnMemoria
from app.servicio.repositorio_usuarios import RepositorioUsuariosEnMemoria
from app.servicio.validador_compra import MAXIMO_ENTRADAS_POR_COMPRA, ValidadorCompra
from app.servicio.tarifario import Tarifario

class ServicioCompra:

    def __init__(
        self,
        usuarios: RepositorioUsuariosEnMemoria,
        compras: RepositorioComprasEnMemoria,
        ahora: Callable[[], datetime] = datetime.now,
        calendario: CalendarioParque | None = None,
        tarifario: Tarifario | None = None,
    ) -> None:
        self._usuarios = usuarios
        self._compras = compras
        self._validador = ValidadorCompra(ahora, calendario or CalendarioParque())
        self._tarifario = tarifario or Tarifario()

    def comprar(self, solicitud: SolicitudCompra) -> ResultadoCompra:
        error = (
            self._verificar_usuario(solicitud)
            or self._validador.validar(solicitud)
            or self._verificar_limite_por_fecha(solicitud)
        )
        if error:
            return ResultadoCompra.fallida(error)
        monto_total = self._calcular_monto_total(solicitud)
        self._compras.guardar(solicitud)
        return ResultadoCompra.ok(monto_total)

    def _verificar_usuario(self, solicitud: SolicitudCompra) -> str | None:
        if not self._usuarios.esta_registrado(solicitud.usuario_email):
            return "Debe estar registrado para comprar entradas"
        return None

    def _verificar_limite_por_fecha(self, solicitud: SolicitudCompra) -> str | None:
        ya_compradas = self._compras.entradas_compradas(
            solicitud.usuario_email, solicitud.fecha_visita
        )
        if ya_compradas + solicitud.cantidad > MAXIMO_ENTRADAS_POR_COMPRA:
            return (
                f"Solo puede comprar hasta {MAXIMO_ENTRADAS_POR_COMPRA} entradas por fecha. "
                f"Ya compró {ya_compradas} para ese día"
            )
        return None

    def _calcular_monto_total(self, solicitud: SolicitudCompra) -> int:
        return sum(
            self._tarifario.precio(solicitud.tipo_pase, edad) for edad in solicitud.edades
        )
