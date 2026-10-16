from fastapi.testclient import TestClient
from app.api.dependencias import obtener_servicio_compra
from app.main import app
from app.servicio.servicio_compra import ServicioCompra
from app.servicio.servicio_email import ServicioEmailSimulado
from tests.test_comprar_entrada import USUARIO_REGISTRADO, crear_servicio

ENDPOINT = "/api/compras"
CABECERAS = {"X-Usuario-Email": USUARIO_REGISTRADO}
CUERPO_VALIDO = {
    "fecha_visita": "2026-10-29",
    "cantidad": 2,
    "edades": [30, 28],
    "tipo_pase": "REGULAR",
    "forma_pago": "TARJETA",
}


def crear_cliente(servicio: ServicioCompra | None = None) -> TestClient:
    servicio = servicio or crear_servicio()
    app.dependency_overrides[obtener_servicio_compra] = lambda: servicio
    return TestClient(app)


class TestApiComprarEntradas:

    def test_pu1_compra_con_tarjeta_redirige_a_mercado_pago_y_envia_mail(self):
        email = ServicioEmailSimulado()
        cliente = crear_cliente(crear_servicio(email=email))

        respuesta = cliente.post(ENDPOINT, json=CUERPO_VALIDO, headers=CABECERAS)

        assert respuesta.status_code == 201
        datos = respuesta.json()
        assert datos["url_pago"] == "http://localhost:5173/mercado-pago-simulado?monto=20000"
        assert datos["mensaje"] == "Compraste 2 entradas para el 29/10/2026. Total: $20.000"
        assert datos["mail_enviado_a"] == USUARIO_REGISTRADO
        assert len(email.enviados) == 1

    def test_pu2_compra_sin_forma_de_pago_falla(self):
        cliente = crear_cliente()
        cuerpo = {**CUERPO_VALIDO}
        del cuerpo["forma_pago"]

        respuesta = cliente.post(ENDPOINT, json=cuerpo, headers=CABECERAS)

        assert respuesta.status_code == 422
        assert respuesta.json()["detail"] == "Debe seleccionar una forma de pago"

    def test_pu3_compra_con_el_parque_cerrado_falla(self):
        cliente = crear_cliente()
        cuerpo = {**CUERPO_VALIDO, "fecha_visita": "2026-10-26"}  # lunes

        respuesta = cliente.post(ENDPOINT, json=cuerpo, headers=CABECERAS)

        assert respuesta.status_code == 422
        assert respuesta.json()["detail"] == "El parque está cerrado en la fecha seleccionada"

    def test_pu4_compra_de_mas_de_10_entradas_falla(self):
        cliente = crear_cliente()
        cuerpo = {**CUERPO_VALIDO, "cantidad": 11, "edades": [30] * 11}

        respuesta = cliente.post(ENDPOINT, json=cuerpo, headers=CABECERAS)

        assert respuesta.status_code == 422
        assert respuesta.json()["detail"] == "La cantidad de entradas no puede superar 10"

    def test_usuario_no_registrado_recibe_403(self):
        cliente = crear_cliente()

        respuesta = cliente.post(
            ENDPOINT, json=CUERPO_VALIDO, headers={"X-Usuario-Email": "intruso@mail.com"}
        )

        assert respuesta.status_code == 403

    def test_sin_identificar_al_usuario_recibe_401(self):
        cliente = crear_cliente()

        respuesta = cliente.post(ENDPOINT, json=CUERPO_VALIDO)

        assert respuesta.status_code == 401
