import re
from datetime import date

from app.modelos.modelos import FormaPago, SolicitudCompra, TipoPase
from app.repositorios.repositorio_compras import CompraRegistrada
from app.servicios.mail_confirmacion import armar_mail_confirmacion, generar_qr_png
from app.servicios.tarifario import Tarifario


def crear_compra(forma_pago: FormaPago = FormaPago.EFECTIVO) -> CompraRegistrada:
    return CompraRegistrada(
        id="compra-1",
        solicitud=SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 10, 29),
            cantidad=3,
            edades=[35, 10, 2],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=forma_pago,
        ),
        monto_total=15000,
    )


class TestCodigoDeEntrada:

    def test_cada_compra_tiene_un_codigo_de_entrada_aleatorio(self):
        primera, segunda = crear_compra(), crear_compra()

        assert re.fullmatch(r"EHP-[A-Z0-9]{8}", primera.codigo_entrada)
        assert primera.codigo_entrada != segunda.codigo_entrada


class TestMailConfirmacion:

    def test_el_qr_contiene_el_codigo_de_entrada(self):
        compra = crear_compra()

        mail = armar_mail_confirmacion(compra, Tarifario())

        assert mail.qr_png.startswith(b"\x89PNG")
        assert mail.qr_png == generar_qr_png(compra.codigo_entrada)
        assert f'src="cid:{mail.qr_cid}"' in mail.html

    def test_el_texto_y_el_html_informan_cantidad_fecha_total_y_codigo(self):
        compra = crear_compra()

        mail = armar_mail_confirmacion(compra, Tarifario())

        for cuerpo in (mail.texto, mail.html):
            assert "Compraste 3 entradas para el 29/10/2026. Total: $15.000" in cuerpo
            assert compra.codigo_entrada in cuerpo

    def test_el_html_detalla_el_subtotal_de_cada_visitante(self):
        mail = armar_mail_confirmacion(crear_compra(), Tarifario())

        assert "35 años" in mail.html and "$10.000" in mail.html
        assert "10 años" in mail.html and "$5.000" in mail.html
        assert "2 años" in mail.html and "Gratis" in mail.html
        assert "Regular" in mail.html

    def test_indica_como_se_paga_segun_la_forma_de_pago(self):
        efectivo = armar_mail_confirmacion(crear_compra(FormaPago.EFECTIVO), Tarifario())
        tarjeta = armar_mail_confirmacion(crear_compra(FormaPago.TARJETA), Tarifario())

        assert "Pagás en boletería" in efectivo.html
        assert "Pagado con Mercado Pago" in tarjeta.html
