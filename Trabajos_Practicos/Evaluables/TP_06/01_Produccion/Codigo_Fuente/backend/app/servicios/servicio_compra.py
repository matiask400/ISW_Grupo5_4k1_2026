from collections.abc import Callable
from datetime import datetime
from uuid import uuid4

from app.modelos.modelos import ResultadoCompra, SolicitudCompra, FormaPago
from app.servicios.calendario_parque import CalendarioParque
from app.repositorios.repositorio_compras import CompraRegistrada, RepositorioComprasEnMemoria
from app.repositorios.repositorio_usuarios import RepositorioUsuariosEnMemoria
from app.servicios.validador_compra import MAXIMO_ENTRADAS_POR_COMPRA, ValidadorCompra
from app.servicios.tarifario import Tarifario
from app.integraciones.errores import PasarelaPagoError
from app.integraciones.mercado_pago import PasarelaMercadoPago
from app.integraciones.email_smtp import ServicioEmailSMTP
from app.servicios.mail_confirmacion import armar_mail_confirmacion

class ServicioCompra:
    def __init__(
        self,
        usuarios: RepositorioUsuariosEnMemoria,
        compras: RepositorioComprasEnMemoria,
        pasarela: PasarelaMercadoPago,
        email: ServicioEmailSMTP,
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
        if not self._usuarios.esta_registrado(solicitud.usuario_email):
            return ResultadoCompra.denegada("Debe estar registrado para comprar entradas")

        error = self._validador.validar(solicitud) or self._verificar_limite_por_fecha(solicitud)
        if error:
            return ResultadoCompra.fallida(error)

        compra = CompraRegistrada(
            id=uuid4().hex,
            solicitud=solicitud,
            monto_total=self._calcular_monto_total(solicitud),
        )
        try:
            url_pago = self._iniciar_pago(compra)
        except PasarelaPagoError:
            return ResultadoCompra.fallida("No se pudo iniciar el pago. Intente nuevamente")

        self._compras.guardar(compra)
        if url_pago:
            # Con tarjeta el mail se envía cuando Mercado Pago aprueba el pago.
            return self._resultado(compra, url_pago=url_pago)
        self._notificar(compra)
        return self._resultado(compra)

    def confirmar_pago(self, payment_id: str, usuario_email: str) -> ResultadoCompra:
        """Verifica el pago con Mercado Pago y, si está aprobado, envía el mail (una sola vez)."""
        try:
            pago = self._pasarela.consultar_pago(payment_id)
        except PasarelaPagoError:
            return ResultadoCompra.fallida("No se pudo verificar el pago con Mercado Pago")

        compra = self._compras.obtener(pago.referencia) if pago.referencia else None
        if compra is None:
            return ResultadoCompra.fallida("No se encontró la compra de este pago")
        if compra.solicitud.usuario_email != usuario_email:
            return ResultadoCompra.denegada("La compra pertenece a otro usuario")
        if not pago.aprobado:
            return ResultadoCompra.fallida("El pago no fue aprobado por Mercado Pago")

        if not compra.mail_enviado:
            self._notificar(compra)
        return self._resultado(compra)

    def _notificar(self, compra: CompraRegistrada) -> None:
        mail = armar_mail_confirmacion(compra, self._tarifario)
        self._email.enviar(
            destinatario=compra.solicitud.usuario_email,
            asunto=mail.asunto,
            cuerpo=mail.texto,
            html=mail.html,
            imagenes={mail.qr_cid: mail.qr_png},
        )
        compra.mail_enviado = True

    @staticmethod
    def _resultado(compra: CompraRegistrada, url_pago: str | None = None) -> ResultadoCompra:
        return ResultadoCompra.ok(
            cantidad=compra.solicitud.cantidad,
            fecha_visita=compra.solicitud.fecha_visita,
            monto_total=compra.monto_total,
            url_pago=url_pago,
            mail_enviado_a=compra.solicitud.usuario_email if compra.mail_enviado else None,
        )

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

    def _iniciar_pago(self, compra: CompraRegistrada) -> str | None:
        """Con tarjeta devuelve la URL de Mercado Pago; en efectivo se paga en boletería."""
        if compra.solicitud.forma_pago != FormaPago.TARJETA:
            return None
        return self._pasarela.crear_link_de_pago(compra.monto_total, referencia=compra.id)
