"""Mail de confirmación de compra: versión de texto y versión HTML con el QR de la entrada."""

import io
from dataclasses import dataclass
from html import escape

import segno

from app.modelos.modelos import FormaPago, ResultadoCompra, formatear_pesos
from app.repositorios.repositorio_compras import CompraRegistrada
from app.servicios.tarifario import Tarifario

ASUNTO_MAIL_CONFIRMACION = "Confirmación de compra - EcoHarmony Park"
QR_CID = "qr-entrada"

# Paleta del parque (FAQ 3)
VERDE_OSCURO = "#386641"
VERDE = "#6a994e"
VERDE_CLARO = "#a7c957"
CREMA = "#f2e8cf"

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
    segno.make(contenido, error="m").save(salida, kind="png", scale=8, border=2, dark=VERDE_OSCURO)
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
        f'<tr><td style="padding:8px 0;border-bottom:1px solid #e6dfc8;">'
        f"Visitante {i} · {edad} años</td>"
        f'<td align="right" style="padding:8px 0;border-bottom:1px solid #e6dfc8;">'
        f"{_precio(monto)}</td></tr>"
        for i, (edad, monto) in enumerate(subtotales, start=1)
    )
    # Tablas y estilos en línea: es lo que mejor soportan los clientes de correo.
    return f"""\
<!DOCTYPE html>
<html lang="es">
<body style="margin:0;padding:0;background:{CREMA};font-family:Lato,Arial,Helvetica,sans-serif;color:#22301f;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{CREMA};padding:24px 12px;">
    <tr><td align="center">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
             style="max-width:560px;background:#ffffff;border-radius:16px;overflow:hidden;">
        <tr><td style="background:{VERDE_OSCURO};padding:28px 32px;color:#ffffff;">
          <div style="font-size:13px;letter-spacing:2px;color:{VERDE_CLARO};">ECOHARMONY PARK</div>
          <div style="font-size:26px;font-weight:bold;margin-top:6px;">¡Tu entrada está confirmada!</div>
        </td></tr>
        <tr><td style="padding:28px 32px 8px;">
          <p style="margin:0 0 6px;font-size:16px;">{escape(resumen)}</p>
          <p style="margin:0;font-size:14px;color:{VERDE};">{escape(pago)}</p>
        </td></tr>
        <tr><td align="center" style="padding:20px 32px;">
          <div style="border:2px dashed {VERDE_CLARO};border-radius:14px;padding:20px;">
            <img src="cid:{QR_CID}" width="200" height="200" alt="QR de tu entrada"
                 style="display:block;margin:0 auto;">
            <div style="margin-top:12px;font-size:12px;letter-spacing:1px;color:#6b7563;">CÓDIGO DE ENTRADA</div>
            <div style="font-size:22px;font-weight:bold;letter-spacing:3px;color:{VERDE_OSCURO};">
              {escape(compra.codigo_entrada)}</div>
            <div style="margin-top:6px;font-size:13px;color:#6b7563;">Mostralo al ingresar al parque.</div>
          </div>
        </td></tr>
        <tr><td style="padding:8px 32px 24px;">
          <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="font-size:14px;">
            <tr><td style="padding:8px 0;color:#6b7563;">Pase</td>
                <td align="right" style="padding:8px 0;">{NOMBRE_PASE[solicitud.tipo_pase.value]}</td></tr>
            <tr><td style="padding:8px 0;color:#6b7563;">Fecha de visita</td>
                <td align="right" style="padding:8px 0;">{solicitud.fecha_visita.strftime("%d/%m/%Y")}</td></tr>
            {filas}
            <tr><td style="padding:12px 0;font-weight:bold;font-size:16px;">Total</td>
                <td align="right" style="padding:12px 0;font-weight:bold;font-size:16px;color:{VERDE_OSCURO};">
                  ${formatear_pesos(compra.monto_total)}</td></tr>
          </table>
        </td></tr>
        <tr><td style="background:{CREMA};padding:18px 32px;font-size:12px;color:#6b7563;text-align:center;">
          Abierto de 8:30 a 19 · Cerrado los lunes, el 25/12 y el 1/1
        </td></tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""
