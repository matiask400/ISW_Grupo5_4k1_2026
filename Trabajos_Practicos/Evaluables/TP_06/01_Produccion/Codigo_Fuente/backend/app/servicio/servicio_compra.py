from collections.abc import Callable
from datetime import datetime

from app.modelos.modelos import ResultadoCompra, SolicitudCompra, FormaPago
from app.servicio.calendario_parque import CalendarioParque
from app.servicio.repositorio_compras import RepositorioComprasEnMemoria
from app.servicio.repositorio_usuarios import RepositorioUsuariosEnMemoria
from app.servicio.validador_compra import MAXIMO_ENTRADAS_POR_COMPRA, ValidadorCompra
from app.servicio.tarifario import Tarifario
from app.servicio.pasarela_pago import PasarelaMercadoPagoSimulada
from app.servicio.servicio_email import ServicioEmailSimulado

ASUNTO_MAIL_CONFIRMACION = "Confirmación de compra - EcoHarmony Park"

class ServicioCompra:
    def __init__(
        self,
        usuarios: RepositorioUsuariosEnMemoria,
        compras: RepositorioComprasEnMemoria,
        pasarela: PasarelaMercadoPagoSimulada,
        email: ServicioEmailSimulado,
        ahora: Callable[[], datetime] = datetime.now,
        calendario: CalendarioParque | None = None,
        tarifario: Tarifario | None = None,
    ) -> None:
        self._usuarios = usuarios
        self._compras = compras
        self._pasarela = pasarela
        self._email = email
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
        resultado = ResultadoCompra.ok(
            cantidad=solicitud.cantidad,
            fecha_visita=solicitud.fecha_visita,
            monto_total=monto_total,
            url_pago=self._iniciar_pago(solicitud, monto_total),
            mail_enviado_a=solicitud.usuario_email,
        )
        self._notificar(resultado)
        return resultado

    def _notificar(self, resultado: ResultadoCompra) -> None:
            self._email.enviar(
                destinatario=resultado.mail_enviado_a,
                asunto=ASUNTO_MAIL_CONFIRMACION,
                cuerpo=resultado.mensaje,
            )

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

    def _iniciar_pago(self, solicitud: SolicitudCompra, monto: int) -> str | None:
        """Con tarjeta devuelve la URL de Mercado Pago; en efectivo se paga en boletería."""
        if solicitud.forma_pago != FormaPago.TARJETA:
            return None
        return self._pasarela.crear_link_de_pago(monto)
