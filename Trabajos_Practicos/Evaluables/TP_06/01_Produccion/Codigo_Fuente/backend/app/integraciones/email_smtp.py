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

    def enviar(self, destinatario: str, asunto: str, cuerpo: str) -> None:
        mail = EmailMessage()
        mail["From"] = self._usuario
        mail["To"] = destinatario
        mail["Subject"] = asunto
        mail.set_content(cuerpo)

        with self._smtp(self._host, self._puerto) as servidor:
            servidor.starttls()
            servidor.login(self._usuario, self._contrasena)
            servidor.send_message(mail)
