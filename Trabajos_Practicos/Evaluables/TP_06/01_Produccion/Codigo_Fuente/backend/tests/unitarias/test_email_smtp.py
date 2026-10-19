from unittest.mock import MagicMock

from app.integraciones.email_smtp import ServicioEmailSMTP


class TestServicioEmailSMTP:

    def test_se_autentica_y_envia_el_mail_con_los_datos_correctos(self):
        smtp = MagicMock()
        servicio = ServicioEmailSMTP(
            host="smtp.gmail.com",
            puerto=587,
            usuario="parque@gmail.com",
            contrasena="clave-de-aplicacion",
            smtp=smtp,
        )

        servicio.enviar("ana@mail.com", "Confirmación de compra", "Compraste 2 entradas")

        smtp.assert_called_once_with("smtp.gmail.com", 587)
        servidor = smtp.return_value.__enter__.return_value
        servidor.starttls.assert_called_once()
        servidor.login.assert_called_once_with("parque@gmail.com", "clave-de-aplicacion")
        mail = servidor.send_message.call_args.args[0]
        assert mail["From"] == "parque@gmail.com"
        assert mail["To"] == "ana@mail.com"
        assert mail["Subject"] == "Confirmación de compra"
        assert mail.get_content().strip() == "Compraste 2 entradas"

    def test_con_html_envia_version_de_texto_y_html_con_la_imagen_incrustada(self):
        smtp = MagicMock()
        servicio = ServicioEmailSMTP("smtp.gmail.com", 587, "parque@gmail.com", "clave", smtp=smtp)
        png = b"\x89PNG\r\n\x1a\nimagen-de-prueba"

        servicio.enviar(
            "ana@mail.com",
            "Confirmación de compra",
            "Compraste 2 entradas",
            html='<p>Compraste 2 entradas</p><img src="cid:qr-entrada">',
            imagenes={"qr-entrada": png},
        )

        mail = smtp.return_value.__enter__.return_value.send_message.call_args.args[0]
        assert mail.get_body(("plain",)).get_content().strip() == "Compraste 2 entradas"
        assert 'src="cid:qr-entrada"' in mail.get_body(("html",)).get_content()
        imagen = next(parte for parte in mail.walk() if parte["Content-ID"] == "<qr-entrada>")
        assert imagen.get_content_type() == "image/png"
        assert imagen.get_content() == png
