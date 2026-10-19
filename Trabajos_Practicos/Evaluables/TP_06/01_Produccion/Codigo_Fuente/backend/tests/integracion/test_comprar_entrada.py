import json
import pytest
import httpx

from datetime import date, datetime, timedelta
from email.message import EmailMessage
from app.modelos.modelos import FormaPago, SolicitudCompra, TipoPase
from app.servicios.servicio_compra import ServicioCompra
from app.repositorios.repositorio_usuarios import RepositorioUsuariosEnMemoria
from app.repositorios.repositorio_compras import RepositorioComprasEnMemoria
from app.integraciones.email_smtp import ServicioEmailSMTP
from app.integraciones.mercado_pago import PasarelaMercadoPago

AHORA = datetime(2026, 10, 22, 10, 0)
HOY = AHORA.date()
FECHA_VALIDA = date(2026, 10, 29)
USUARIO_REGISTRADO = "ana@mail.com"
OTRO_USUARIO_REGISTRADO = "juan@mail.com"
URL_CHECKOUT = "https://www.mercadopago.com.ar/checkout/v1/redirect?pref_id=TEST-123"


class ApiMercadoPagoEnMemoria:
    """Atiende en memoria los pedidos HTTP que hace PasarelaMercadoPago a la API de Mercado Pago."""

    def __init__(self, status: int = 201) -> None:
        self._status = status
        self.preferencias: list[dict] = []
        self._pagos: dict[str, dict] = {}
        self.cliente_http = httpx.Client(transport=httpx.MockTransport(self._responder))

    def _responder(self, pedido: httpx.Request) -> httpx.Response:
        if pedido.method == "GET":
            pago = self._pagos.get(pedido.url.path.rsplit("/", 1)[-1])
            return httpx.Response(200, json=pago) if pago else httpx.Response(404)
        self.preferencias.append(json.loads(pedido.content))
        if self._status >= 400:
            return httpx.Response(self._status)
        return httpx.Response(self._status, json={"id": "TEST-123", "init_point": URL_CHECKOUT})

    def pagar(self, estado: str = "approved", referencia: str | None = None) -> str:
        """El comprador paga la última preferencia creada; devuelve el payment_id."""
        payment_id = str(len(self._pagos) + 1)
        referencia = referencia or self.preferencias[-1]["external_reference"]
        self._pagos[payment_id] = {
            "id": payment_id,
            "status": estado,
            "external_reference": referencia,
        }
        return payment_id

    @property
    def montos(self) -> list[int]:
        return [p["items"][0]["unit_price"] for p in self.preferencias]


class ServidorSMTPEnMemoria:

    def __init__(self) -> None:
        self.enviados: list[EmailMessage] = []

    def conectar(self, host: str, puerto: int) -> "ServidorSMTPEnMemoria":
        return self

    def __enter__(self) -> "ServidorSMTPEnMemoria":
        return self

    def __exit__(self, *excepcion) -> None:
        return None

    def starttls(self) -> None:
        pass

    def login(self, usuario: str, contrasena: str) -> None:
        pass

    def send_message(self, mail: EmailMessage) -> None:
        self.enviados.append(mail)


def assert_mail_con_qr(mail: EmailMessage, mensaje: str) -> None:
    assert mensaje in mail.get_body(("plain",)).get_content()
    html = mail.get_body(("html",)).get_content()
    assert mensaje in html
    assert 'src="cid:qr-entrada"' in html
    qr = next(parte for parte in mail.walk() if parte["Content-ID"] == "<qr-entrada>")
    assert qr.get_content_type() == "image/png"


def crear_servicio(
    ahora: datetime = AHORA,
    api_mercado_pago: ApiMercadoPagoEnMemoria | None = None,
    servidor_smtp: ServidorSMTPEnMemoria | None = None,
) -> ServicioCompra:
    api_mercado_pago = api_mercado_pago or ApiMercadoPagoEnMemoria()
    servidor_smtp = servidor_smtp or ServidorSMTPEnMemoria()
    return ServicioCompra(
        ahora=lambda: ahora,
        usuarios=RepositorioUsuariosEnMemoria({USUARIO_REGISTRADO, OTRO_USUARIO_REGISTRADO}),
        compras=RepositorioComprasEnMemoria(),
        pasarela=PasarelaMercadoPago(
            access_token="TEST-token",
            cliente_http=api_mercado_pago.cliente_http,
        ),
        email=ServicioEmailSMTP(
            host="smtp.test",
            puerto=587,
            usuario="entradas@ecoharmony.test",
            contrasena="clave-de-prueba",
            smtp=servidor_smtp.conectar,
        ),
    )


class TestComprarEntrada:

    def test_no_deberia_comprar_mas_10_entradas(self):
        servicio = crear_servicio()

        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=11,
            edades=[30] * 11,
            tipo_pase= TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )
        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == ("La cantidad de entradas no puede superar 10")

    def test_no_deberia_comprar_sin_seleccionar_forma_de_pago(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, 25],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=None,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Debe seleccionar una forma de pago"

    def test_rechaza_0_entradas(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=0,
            edades=[],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )
        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Debe comprar al menos 1 entrada"

    def test_rechaza_cantidad_menor_a_1(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=-1,
            edades=[],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Debe comprar al menos 1 entrada"

    def test_permite_comprar_2_entradas(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True

    def test_permite_exactamente_10_entradas(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=10,
            edades=[30] * 10,
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True

    def test_rechaza_si_falta_la_edad_de_algun_visitante(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=3,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Debe indicar la edad de cada visitante"

    def test_rechaza_edad_negativa(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, -1],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Las edades deben estar entre 0 y 120"

    def test_rechaza_edad_mayor_a_120(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, 121],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Las edades deben estar entre 0 y 120"

    def test_permite_edades_en_los_limites(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[0, 120],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True

    def test_no_deberia_comprar_sin_tipo_de_pase(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=None,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Debe seleccionar un tipo de pase"

    def test_permite_comprar_pase_vip(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.VIP,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True

    def test_rechaza_fecha_de_visita_pasada(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 10, 7),
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "La fecha de visita debe ser hoy o una fecha futura"

    def test_rechaza_otra_fecha_pasada(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=HOY - timedelta(days=1),
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "La fecha de visita debe ser hoy o una fecha futura"

    def test_permite_comprar_para_el_dia_de_hoy(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=HOY,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True

    def test_no_deberia_comprar_si_el_parque_esta_cerrado(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 10, 26),
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "El parque está cerrado en la fecha seleccionada"

    def test_no_deberia_comprar_con_mas_de_un_mes_de_anticipacion(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 11, 24),
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Solo se pueden comprar entradas con hasta 1 mes de anticipación"

    def test_permite_comprar_justo_un_mes_despues_cruzando_el_anio(self):
        servicio = crear_servicio(ahora=datetime(2026, 12, 20, 10, 0))
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2027, 1, 20),
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True

    def test_permite_comprar_exactamente_un_mes_despues(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 11, 22),
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True

    def test_permite_comprar_hasta_fin_del_mes_siguiente_corto(self):
        servicio = crear_servicio(ahora=datetime(2027, 1, 31, 10, 0))
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2027, 2, 28),
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True

    def test_no_deberia_comprar_para_hoy_despues_de_las_17_30(self):
        servicio = crear_servicio(ahora=datetime(2026, 10, 22, 17, 31))
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=HOY,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Las compras para el día de hoy se permiten hasta las 17:30"

    def test_permite_comprar_para_hoy_a_las_17_30_en_punto(self):
        servicio = crear_servicio(ahora=datetime(2026, 10, 22, 17, 30))
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=HOY,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True

    def test_despues_de_las_17_30_puede_comprar_para_otro_dia(self):
        servicio = crear_servicio(ahora=datetime(2026, 10, 22, 17, 31))
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True

    def test_no_deberia_comprar_un_usuario_no_registrado(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="intruso@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Debe estar registrado para comprar entradas"

    def test_no_deberia_superar_10_entradas_sumando_compras_de_la_misma_fecha(self):
        servicio = crear_servicio()
        primera_compra = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=8,
            edades=[30] * 8,
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )
        segunda_compra = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=3,
            edades=[30] * 3,
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )
        servicio.comprar(primera_compra)

        resultado = servicio.comprar(segunda_compra)

        assert resultado.exitosa is False
        assert resultado.error == (
            "Solo puede comprar hasta 10 entradas por fecha. Ya compró 8 para ese día"
        )

    def test_otro_usuario_puede_comprar_para_la_misma_fecha(self):
        servicio = crear_servicio()
        compra_de_ana = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=10,
            edades=[30] * 10,
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )
        compra_de_juan = SolicitudCompra(
            usuario_email="juan@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[40, 38],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )
        servicio.comprar(compra_de_ana)

        resultado = servicio.comprar(compra_de_juan)

        assert resultado.exitosa is True

    def test_mismo_usuario_puede_comprar_para_otra_fecha(self):
        servicio = crear_servicio()
        compra_del_jueves = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=10,
            edades=[30] * 10,
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )
        compra_del_viernes = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 10, 30),
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )
        servicio.comprar(compra_del_jueves)

        resultado = servicio.comprar(compra_del_viernes)

        assert resultado.exitosa is True

    def test_permite_completar_exactamente_10_entradas_en_varias_compras(self):
        servicio = crear_servicio()
        primera_compra = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=8,
            edades=[30] * 8,
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )
        segunda_compra = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )
        servicio.comprar(primera_compra)

        resultado = servicio.comprar(segunda_compra)

        assert resultado.exitosa is True

    def test_una_compra_fallida_no_suma_al_total_del_dia(self):
        servicio = crear_servicio()
        compra_fallida = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=8,
            edades=[30] * 8,
            tipo_pase=TipoPase.REGULAR,
            forma_pago=None,
        )
        compra_valida = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=10,
            edades=[30] * 10,
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )
        servicio.comprar(compra_fallida)

        resultado = servicio.comprar(compra_valida)

        assert resultado.exitosa is True

    def test_informa_el_monto_total_segun_tipo_de_pase_y_edades(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=4,
            edades=[35, 33, 10, 2],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True
        assert resultado.monto_total == 25000

    @pytest.mark.parametrize(
        ("tipo_pase", "monto_esperado"),
        [(TipoPase.REGULAR, 40000), (TipoPase.VIP, 80000)],
    )
    def test_monto_total_con_edades_en_todos_los_tramos(self, tipo_pase, monto_esperado):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=8,
            edades=[0, 1, 4, 15, 16, 59, 60, 120],
            tipo_pase=tipo_pase,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True
        assert resultado.monto_total == monto_esperado

    def test_informa_cantidad_y_fecha_al_finalizar_la_compra(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.cantidad == 2
        assert resultado.fecha_visita == FECHA_VALIDA

    def test_informa_un_mensaje_con_cantidad_fecha_y_total(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.mensaje == "Compraste 2 entradas para el 29/10/2026. Total: $20.000"

    def test_con_una_sola_entrada_el_mensaje_esta_en_singular(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 10, 30),
            cantidad=1,
            edades=[30],
            tipo_pase=TipoPase.VIP,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.mensaje == "Compraste 1 entrada para el 30/10/2026. Total: $20.000"

    def test_una_compra_fallida_no_tiene_mensaje_de_confirmacion(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=11,
            edades=[30] * 11,
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.mensaje is None

    def test_pago_con_tarjeta_devuelve_url_de_mercado_pago(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.TARJETA,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.url_pago == URL_CHECKOUT

    def test_pago_en_efectivo_no_redirige_a_mercado_pago(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.url_pago is None

    def test_el_pago_se_crea_por_el_monto_de_la_compra(self):
        mercado_pago = ApiMercadoPagoEnMemoria()
        servicio = crear_servicio(api_mercado_pago=mercado_pago)
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=3,
            edades=[30, 28, 10],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.TARJETA,
        )

        servicio.comprar(solicitud)

        assert mercado_pago.montos == [25000]

    def test_una_compra_invalida_no_genera_ningun_pago(self):
        mercado_pago = ApiMercadoPagoEnMemoria()
        servicio = crear_servicio(api_mercado_pago=mercado_pago)
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=11,
            edades=[30] * 11,
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.TARJETA,
        )

        servicio.comprar(solicitud)

        assert mercado_pago.preferencias == []

    def test_una_compra_en_efectivo_envia_mail_de_confirmacion_al_registrarse(self):
        smtp = ServidorSMTPEnMemoria()
        servicio = crear_servicio(servidor_smtp=smtp)
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert len(smtp.enviados) == 1
        mail = smtp.enviados[0]
        assert mail["To"] == "ana@mail.com"
        assert mail["Subject"] == "Confirmación de compra - EcoHarmony Park"
        assert_mail_con_qr(mail, resultado.mensaje)

    def test_una_compra_invalida_no_envia_mail(self):
        smtp = ServidorSMTPEnMemoria()
        servicio = crear_servicio(servidor_smtp=smtp)
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=None,
        )

        servicio.comprar(solicitud)

        assert smtp.enviados == []

    def test_informa_a_que_direccion_se_envio_el_mail(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.mail_enviado_a == "ana@mail.com"

    def test_usuario_no_registrado_se_informa_como_acceso_denegado(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="intruso@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.acceso_denegado is True

    def test_si_no_se_puede_iniciar_el_pago_la_compra_falla_y_no_se_registra(self):
            mercado_pago_caido = ApiMercadoPagoEnMemoria(status=503)
            servicio = crear_servicio(api_mercado_pago=mercado_pago_caido)
            compra_con_tarjeta = SolicitudCompra(
                usuario_email="ana@mail.com",
                fecha_visita=FECHA_VALIDA,
                cantidad=10,
                edades=[30] * 10,
                tipo_pase=TipoPase.REGULAR,
                forma_pago=FormaPago.TARJETA,
            )
            compra_en_efectivo = SolicitudCompra(
                usuario_email="ana@mail.com",
                fecha_visita=FECHA_VALIDA,
                cantidad=10,
                edades=[30] * 10,
                tipo_pase=TipoPase.REGULAR,
                forma_pago=FormaPago.EFECTIVO,
            )

            resultado = servicio.comprar(compra_con_tarjeta)

            assert resultado.exitosa is False
            assert resultado.error == "No se pudo iniciar el pago. Intente nuevamente"
            assert servicio.comprar(compra_en_efectivo).exitosa is True


def compra_con_tarjeta(usuario_email: str = USUARIO_REGISTRADO) -> SolicitudCompra:
    return SolicitudCompra(
        usuario_email=usuario_email,
        fecha_visita=FECHA_VALIDA,
        cantidad=2,
        edades=[30, 28],
        tipo_pase=TipoPase.REGULAR,
        forma_pago=FormaPago.TARJETA,
    )


class TestConfirmarPagoConTarjeta:
    """Con tarjeta, el mail se envía recién cuando Mercado Pago aprueba el pago."""

    def setup_method(self):
        self.mercado_pago = ApiMercadoPagoEnMemoria()
        self.smtp = ServidorSMTPEnMemoria()
        self.servicio = crear_servicio(api_mercado_pago=self.mercado_pago, servidor_smtp=self.smtp)

    def test_al_registrar_la_compra_con_tarjeta_todavia_no_envia_mail(self):
        resultado = self.servicio.comprar(compra_con_tarjeta())

        assert resultado.exitosa is True
        assert resultado.mail_enviado_a is None
        assert self.smtp.enviados == []

    def test_cuando_mercado_pago_aprueba_el_pago_envia_el_mail(self):
        self.servicio.comprar(compra_con_tarjeta())
        payment_id = self.mercado_pago.pagar("approved")

        resultado = self.servicio.confirmar_pago(payment_id, USUARIO_REGISTRADO)

        assert resultado.exitosa is True
        assert resultado.mensaje == "Compraste 2 entradas para el 29/10/2026. Total: $20.000"
        assert resultado.mail_enviado_a == USUARIO_REGISTRADO
        assert len(self.smtp.enviados) == 1
        mail = self.smtp.enviados[0]
        assert mail["To"] == USUARIO_REGISTRADO
        assert mail["Subject"] == "Confirmación de compra - EcoHarmony Park"
        assert_mail_con_qr(mail, resultado.mensaje)

    @pytest.mark.parametrize("estado", ["rejected", "pending", "in_process", "cancelled"])
    def test_si_el_pago_no_esta_aprobado_no_envia_mail(self, estado):
        self.servicio.comprar(compra_con_tarjeta())
        payment_id = self.mercado_pago.pagar(estado)

        resultado = self.servicio.confirmar_pago(payment_id, USUARIO_REGISTRADO)

        assert resultado.exitosa is False
        assert resultado.error == "El pago no fue aprobado por Mercado Pago"
        assert self.smtp.enviados == []

    def test_confirmar_dos_veces_el_mismo_pago_no_reenvia_el_mail(self):
        self.servicio.comprar(compra_con_tarjeta())
        payment_id = self.mercado_pago.pagar("approved")

        self.servicio.confirmar_pago(payment_id, USUARIO_REGISTRADO)
        segunda = self.servicio.confirmar_pago(payment_id, USUARIO_REGISTRADO)

        assert segunda.exitosa is True
        assert segunda.mail_enviado_a == USUARIO_REGISTRADO
        assert len(self.smtp.enviados) == 1

    def test_un_pago_que_mercado_pago_no_conoce_no_se_confirma(self):
        resultado = self.servicio.confirmar_pago("no-existe", USUARIO_REGISTRADO)

        assert resultado.exitosa is False
        assert resultado.error == "No se pudo verificar el pago con Mercado Pago"
        assert self.smtp.enviados == []

    def test_un_pago_de_otra_compra_no_se_confirma(self):
        payment_id = self.mercado_pago.pagar("approved", referencia="compra-desconocida")

        resultado = self.servicio.confirmar_pago(payment_id, USUARIO_REGISTRADO)

        assert resultado.exitosa is False
        assert resultado.error == "No se encontró la compra de este pago"
        assert self.smtp.enviados == []

    def test_otro_usuario_no_puede_confirmar_la_compra(self):
        self.servicio.comprar(compra_con_tarjeta())
        payment_id = self.mercado_pago.pagar("approved")

        resultado = self.servicio.confirmar_pago(payment_id, OTRO_USUARIO_REGISTRADO)

        assert resultado.acceso_denegado is True
        assert self.smtp.enviados == []
