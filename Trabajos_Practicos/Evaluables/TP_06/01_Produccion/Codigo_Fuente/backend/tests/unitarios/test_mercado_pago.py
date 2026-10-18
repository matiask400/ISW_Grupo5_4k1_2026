import json

import httpx

from app.integraciones.mercado_pago import PasarelaMercadoPago

URL_CHECKOUT = "https://www.mercadopago.com.ar/checkout/v1/redirect?pref_id=123"


def crear_pasarela(responder) -> PasarelaMercadoPago:
    """Pasarela cuyo cliente HTTP no sale a la red: 'responder' decide la respuesta."""
    cliente = httpx.Client(transport=httpx.MockTransport(responder))
    return PasarelaMercadoPago(access_token="TEST-token", cliente_http=cliente)


class TestPasarelaMercadoPago:

    def test_crea_preferencia_y_devuelve_la_url_de_checkout(self):
        pedidos = []

        def responder(pedido: httpx.Request) -> httpx.Response:
            pedidos.append(pedido)
            return httpx.Response(201, json={"id": "123", "init_point": URL_CHECKOUT})

        url = crear_pasarela(responder).crear_link_de_pago(20000)

        assert url == URL_CHECKOUT
        pedido = pedidos[0]
        assert pedido.url == "https://api.mercadopago.com/checkout/preferences"
        assert pedido.headers["Authorization"] == "Bearer TEST-token"
        item = json.loads(pedido.content)["items"][0]
        assert item["unit_price"] == 20000
        assert item["currency_id"] == "ARS"
