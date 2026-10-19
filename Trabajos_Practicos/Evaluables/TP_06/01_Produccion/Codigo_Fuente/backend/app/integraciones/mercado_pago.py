from dataclasses import dataclass

import httpx

from app.integraciones.errores import PasarelaPagoError

URL_PREFERENCIAS = "https://api.mercadopago.com/checkout/preferences"
URL_PAGOS = "https://api.mercadopago.com/v1/payments"
ESTADO_APROBADO = "approved"


@dataclass
class PagoMercadoPago:
    estado: str
    referencia: str | None

    @property
    def aprobado(self) -> bool:
        return self.estado == ESTADO_APROBADO


class PasarelaMercadoPago:
    def __init__(
        self,
        access_token: str,
        url_retorno: str = "http://localhost:5173/compra-finalizada",
        cliente_http: httpx.Client | None = None,
    ) -> None:
        self._access_token = access_token
        self._url_retorno = url_retorno
        self._cliente = cliente_http or httpx.Client(timeout=10)

    def crear_link_de_pago(self, monto: int, referencia: str | None = None) -> str:
        preferencia = {
            "items": [
                {
                    "title": "Entradas EcoHarmony Park",
                    "quantity": 1,
                    "unit_price": monto,
                    "currency_id": "ARS",
                }
            ],
            "back_urls": {
                "success": self._url_retorno,
                "failure": self._url_retorno,
                "pending": self._url_retorno,
            },
        }
        # Mercado Pago vuelve automáticamente a la app solo si la URL de retorno es
        # pública (https); con localhost no acepta auto_return y el comprador tiene
        # que tocar "Volver al sitio".
        if self._url_retorno.startswith("https://"):
            preferencia["auto_return"] = "approved"
        if referencia:
            # Permite saber a qué compra corresponde el pago cuando se confirma.
            preferencia["external_reference"] = referencia
        respuesta = self._cliente.post(URL_PREFERENCIAS, json=preferencia, headers=self._cabeceras())
        self._verificar(respuesta)
        return respuesta.json()["init_point"]

    def consultar_pago(self, payment_id: str) -> PagoMercadoPago:
        """Estado real del pago según Mercado Pago (no se confía en la URL de retorno)."""
        respuesta = self._cliente.get(f"{URL_PAGOS}/{payment_id}", headers=self._cabeceras())
        self._verificar(respuesta)
        datos = respuesta.json()
        return PagoMercadoPago(estado=datos["status"], referencia=datos.get("external_reference"))

    def _cabeceras(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._access_token}"}

    @staticmethod
    def _verificar(respuesta: httpx.Response) -> None:
        if respuesta.is_error:
            raise PasarelaPagoError(f"Mercado Pago respondió {respuesta.status_code}")
