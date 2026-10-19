import json
import httpx
import pytest
from app.integraciones.errores import PasarelaPagoError
from app.integraciones.mercado_pago import PasarelaMercadoPago

URL_CHECKOUT = "https://www.mercadopago.com.ar/checkout/v1/redirect?pref_id=123"


def crear_pasarela(responder, **opciones) -> PasarelaMercadoPago:
    """Pasarela cuyo cliente HTTP no sale a la red: 'responder' decide la respuesta."""
    cliente = httpx.Client(transport=httpx.MockTransport(responder))
    return PasarelaMercadoPago(access_token="TEST-token", cliente_http=cliente, **opciones)


def preferencia_enviada(**opciones) -> dict:
    """Crea un link de pago y devuelve la preferencia que recibió Mercado Pago."""
    pedidos = []

    def responder(pedido: httpx.Request) -> httpx.Response:
        pedidos.append(pedido)
        return httpx.Response(201, json={"id": "123", "init_point": URL_CHECKOUT})

    crear_pasarela(responder, **opciones).crear_link_de_pago(20000)
    return json.loads(pedidos[0].content)


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

    def test_si_mercado_pago_responde_error_lanza_pasarela_pago_error(self):
        def responder(pedido: httpx.Request) -> httpx.Response:
            return httpx.Response(401, json={"message": "invalid access token"})

        with pytest.raises(PasarelaPagoError):
            crear_pasarela(responder).crear_link_de_pago(20000)

    def test_la_preferencia_lleva_la_referencia_de_la_compra(self):
        pedidos = []

        def responder(pedido: httpx.Request) -> httpx.Response:
            pedidos.append(pedido)
            return httpx.Response(201, json={"id": "123", "init_point": URL_CHECKOUT})

        crear_pasarela(responder).crear_link_de_pago(20000, referencia="compra-1")

        assert json.loads(pedidos[0].content)["external_reference"] == "compra-1"

    def test_consulta_el_estado_y_la_referencia_de_un_pago(self):
        pedidos = []

        def responder(pedido: httpx.Request) -> httpx.Response:
            pedidos.append(pedido)
            return httpx.Response(
                200, json={"id": 987, "status": "approved", "external_reference": "compra-1"}
            )

        pago = crear_pasarela(responder).consultar_pago("987")

        assert pago.estado == "approved"
        assert pago.referencia == "compra-1"
        assert pago.aprobado is True
        assert pedidos[0].method == "GET"
        assert pedidos[0].url == "https://api.mercadopago.com/v1/payments/987"
        assert pedidos[0].headers["Authorization"] == "Bearer TEST-token"

    def test_si_no_puede_consultar_el_pago_lanza_pasarela_pago_error(self):
        def responder(pedido: httpx.Request) -> httpx.Response:
            return httpx.Response(404, json={"message": "Payment not found"})

        with pytest.raises(PasarelaPagoError):
            crear_pasarela(responder).consultar_pago("no-existe")

    def test_con_url_https_vuelve_a_la_app_automaticamente_al_aprobar_el_pago(self):
        url_retorno = "https://ecoharmony.vercel.app/compra-finalizada"

        preferencia = preferencia_enviada(url_retorno=url_retorno)

        assert preferencia["auto_return"] == "approved"
        assert preferencia["back_urls"]["success"] == url_retorno

    def test_con_localhost_no_pide_vuelta_automatica_porque_mercado_pago_no_la_acepta(self):
        preferencia = preferencia_enviada(url_retorno="http://localhost:5173/compra-finalizada")

        assert "auto_return" not in preferencia
