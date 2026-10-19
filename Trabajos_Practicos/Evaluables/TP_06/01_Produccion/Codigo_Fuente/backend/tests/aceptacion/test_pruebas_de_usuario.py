from tests.integracion.test_comprar_entrada import (
    URL_CHECKOUT,
    USUARIO_REGISTRADO,
    ApiMercadoPagoEnMemoria,
    ServidorSMTPEnMemoria,
    crear_servicio,
)
from tests.sistema.test_api_compras import (
    CABECERAS,
    CUERPO_VALIDO,
    ENDPOINT,
    ENDPOINT_CONFIRMAR_PAGO,
    crear_cliente,
)


class TestPruebasDeUsuarioComprarEntradas:

    def test_pu1_compra_con_tarjeta_redirige_a_mercado_pago_y_envia_mail(self):
        """PU1: fecha disponible, menos de 10 entradas, edades, pase y tarjeta (pasa)."""
        mercado_pago = ApiMercadoPagoEnMemoria()
        smtp = ServidorSMTPEnMemoria()
        cliente = crear_cliente(crear_servicio(api_mercado_pago=mercado_pago, servidor_smtp=smtp))

        compra = cliente.post(ENDPOINT, json=CUERPO_VALIDO, headers=CABECERAS)

        assert compra.status_code == 201
        assert compra.json()["url_pago"] == URL_CHECKOUT
        assert smtp.enviados == []  # todavía no pagó

        payment_id = mercado_pago.pagar("approved")
        confirmacion = cliente.post(
            ENDPOINT_CONFIRMAR_PAGO, json={"payment_id": payment_id}, headers=CABECERAS
        )

        assert confirmacion.status_code == 200
        datos = confirmacion.json()
        assert datos["mensaje"] == "Compraste 2 entradas para el 29/10/2026. Total: $20.000"
        assert datos["mail_enviado_a"] == USUARIO_REGISTRADO
        assert len(smtp.enviados) == 1
        assert smtp.enviados[0]["To"] == USUARIO_REGISTRADO

    def test_pu2_compra_sin_forma_de_pago_falla(self):
        """PU2: comprar entradas sin seleccionar forma de pago (falla)."""
        cliente = crear_cliente()
        cuerpo = {**CUERPO_VALIDO}
        del cuerpo["forma_pago"]

        respuesta = cliente.post(ENDPOINT, json=cuerpo, headers=CABECERAS)

        assert respuesta.status_code == 422
        assert respuesta.json()["detail"] == "Debe seleccionar una forma de pago"

    def test_pu3_compra_con_el_parque_cerrado_falla(self):
        """PU3: fecha de visita en la que el parque está cerrado (falla)."""
        cliente = crear_cliente()
        cuerpo = {**CUERPO_VALIDO, "fecha_visita": "2026-10-26"}  # lunes

        respuesta = cliente.post(ENDPOINT, json=cuerpo, headers=CABECERAS)

        assert respuesta.status_code == 422
        assert respuesta.json()["detail"] == "El parque está cerrado en la fecha seleccionada"

    def test_pu4_compra_de_mas_de_10_entradas_falla(self):
        """PU4: cantidad de entradas mayor a 10 (falla)."""
        cliente = crear_cliente()
        cuerpo = {**CUERPO_VALIDO, "cantidad": 11, "edades": [30] * 11}

        respuesta = cliente.post(ENDPOINT, json=cuerpo, headers=CABECERAS)

        assert respuesta.status_code == 422
        assert respuesta.json()["detail"] == "La cantidad de entradas no puede superar 10"
