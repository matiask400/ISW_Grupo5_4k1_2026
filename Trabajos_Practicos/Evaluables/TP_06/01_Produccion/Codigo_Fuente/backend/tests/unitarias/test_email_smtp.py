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
        assert mail["From"] == "EcoHarmony Park <parque@gmail.com>"
        assert mail["To"] == "ana@mail.com"
        assert mail["Subject"] == "Confirmación de compra"
        assert mail.get_content().strip() == "Compraste 2 entradas"

    def test_el_mail_tiene_remitente_con_nombre_y_encabezados_completos(self):
        smtp = MagicMock()
        servicio = ServicioEmailSMTP(
            host="smtp.gmail.com",
            puerto=587,
            usuario="parque@gmail.com",
            contrasena="clave",
            smtp=smtp,
        )

        servicio.enviar("ana@mail.com", "Confirmación de compra", "Compraste 2 entradas")

        mail = smtp.return_value.__enter__.return_value.send_message.call_args.args[0]
        assert mail["From"] == "EcoHarmony Park <parque@gmail.com>"
        assert mail["Message-ID"] is not None
        assert mail["Date"] is not None
        assert mail.get_body(preferencelist=("html",)) is not None
