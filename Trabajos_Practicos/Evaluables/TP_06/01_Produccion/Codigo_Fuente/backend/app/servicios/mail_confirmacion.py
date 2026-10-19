import io
from dataclasses import dataclass
from html import escape
from pathlib import Path
from string import Template

import segno

from app.modelos.modelos import FormaPago, ResultadoCompra, formatear_pesos
from app.repositorios.repositorio_compras import CompraRegistrada
from app.servicios.tarifario import Tarifario

ASUNTO_MAIL_CONFIRMACION = "Confirmación de compra - EcoHarmony Park"
QR_CID = "qr-entrada"
COLOR_QR = "#386641"

CARPETA_PLANTILLAS = Path(__file__).parent / "plantillas"
PLANTILLA_MAIL = Template((CARPETA_PLANTILLAS / "mail_confirmacion.html").read_text(encoding="utf-8"))
PLANTILLA_FILA = Template((CARPETA_PLANTILLAS / "fila_visitante.html").read_text(encoding="utf-8"))

NOMBRE_PASE = {"REGULAR": "Regular", "VIP": "VIP"}
INDICACION_PAGO = {
    FormaPago.EFECTIVO: "Pagás en boletería al llegar al parque.",
    FormaPago.TARJETA: "Pagado con Mercado Pago.",
}


@dataclass
class MailConfirmacion:
    asunto: str
    texto: str
    html: str
    qr_png: bytes
    qr_cid: str = QR_CID


def generar_qr_png(contenido: str) -> bytes:
    salida = io.BytesIO()
    segno.make(contenido, error="m").save(salida, kind="png", scale=8, border=2, dark=COLOR_QR)
    return salida.getvalue()


def armar_mail_confirmacion(compra: CompraRegistrada, tarifario: Tarifario) -> MailConfirmacion:
    solicitud = compra.solicitud
    resumen = ResultadoCompra.ok(
        cantidad=solicitud.cantidad,
        fecha_visita=solicitud.fecha_visita,
        monto_total=compra.monto_total,
    ).mensaje
    pago = INDICACION_PAGO[solicitud.forma_pago]
    subtotales = [(edad, tarifario.precio(solicitud.tipo_pase, edad)) for edad in solicitud.edades]

    texto = (
        f"¡Gracias por tu compra!\n\n{resumen}\n{pago}\n\n"
        f"Código de entrada: {compra.codigo_entrada}\n"
        "Mostrá este código (o el QR del mail) al ingresar al parque.\n\n"
        "EcoHarmony Park · Abierto de 8:30 a 19 (cerrado los lunes)"
    )
    return MailConfirmacion(
        asunto=ASUNTO_MAIL_CONFIRMACION,
        texto=texto,
        html=_html(compra, resumen, pago, subtotales),
        qr_png=generar_qr_png(compra.codigo_entrada),
    )


def _precio(monto: int) -> str:
    return "Gratis" if monto == 0 else f"${formatear_pesos(monto)}"


def _html(
    compra: CompraRegistrada, resumen: str, pago: str, subtotales: list[tuple[int, int]]
) -> str:
    solicitud = compra.solicitud
    filas = "".join(
        PLANTILLA_FILA.substitute(numero=i, edad=edad, precio=_precio(monto)).strip()
        for i, (edad, monto) in enumerate(subtotales, start=1)
    )
    return PLANTILLA_MAIL.substitute(
        resumen=escape(resumen),
        pago=escape(pago),
        qr_cid=QR_CID,
        codigo_entrada=escape(compra.codigo_entrada),
        pase=NOMBRE_PASE[solicitud.tipo_pase.value],
        fecha_visita=solicitud.fecha_visita.strftime("%d/%m/%Y"),
        filas_visitantes=filas,
        total=f"${formatear_pesos(compra.monto_total)}",
    )
