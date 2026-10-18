import httpx

from app.integraciones.errores import PasarelaPagoError

URL_PREFERENCIAS = "https://api.mercadopago.com/checkout/preferences"


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

    def crear_link_de_pago(self, monto: int) -> str:
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
        respuesta = self._cliente.post(
            URL_PREFERENCIAS,
            json=preferencia,
            headers={"Authorization": f"Bearer {self._access_token}"},
        )
        if respuesta.is_error:
            raise PasarelaPagoError(f"Mercado Pago respondió {respuesta.status_code}")
        return respuesta.json()["init_point"]
