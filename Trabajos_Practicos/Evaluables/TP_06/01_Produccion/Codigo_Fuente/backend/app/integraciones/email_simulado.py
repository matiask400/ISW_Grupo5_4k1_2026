from dataclasses import dataclass


@dataclass
class MailEnviado:
    destinatario: str
    asunto: str
    cuerpo: str


class ServicioEmailSimulado:
    def __init__(self) -> None:
        self.enviados: list[MailEnviado] = []

    def enviar(self, destinatario: str, asunto: str, cuerpo: str) -> None:
        self.enviados.append(MailEnviado(destinatario, asunto, cuerpo))
