import smtplib
from email.message import EmailMessage


class ServicioEmailSMTP:
    def __init__(
        self,
        host: str,
        puerto: int,
        usuario: str,
        contrasena: str,
        smtp=smtplib.SMTP,
    ) -> None:
        self._host = host
        self._puerto = puerto
        self._usuario = usuario
        self._contrasena = contrasena
        self._smtp = smtp

    def enviar(
        self,
        destinatario: str,
        asunto: str,
        cuerpo: str,
        html: str | None = None,
        imagenes: dict[str, bytes] | None = None,
    ) -> None:
        """'imagenes' son PNG incrustados en el HTML: {"qr": png} se usa como <img src="cid:qr">."""
        mail = EmailMessage()
        mail["From"] = self._usuario
        mail["To"] = destinatario
        mail["Subject"] = asunto
        mail.set_content(cuerpo)
        if html:
            mail.add_alternative(html, subtype="html")
            parte_html = mail.get_payload()[-1]
            for cid, png in (imagenes or {}).items():
                parte_html.add_related(png, "image", "png", cid=f"<{cid}>")

        with self._smtp(self._host, self._puerto) as servidor:
            servidor.starttls()
            servidor.login(self._usuario, self._contrasena)
            servidor.send_message(mail)
