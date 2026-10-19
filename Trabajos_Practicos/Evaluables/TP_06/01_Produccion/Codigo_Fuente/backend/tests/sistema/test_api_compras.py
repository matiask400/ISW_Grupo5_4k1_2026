import pytest
from fastapi.testclient import TestClient

from app.api.dependencias import ConfiguracionFaltanteError, obtener_servicio_compra
from app.main import app, origenes_permitidos
from app.servicios.servicio_compra import ServicioCompra
from tests.integracion.test_comprar_entrada import (
    OTRO_USUARIO_REGISTRADO,
    USUARIO_REGISTRADO,
    ApiMercadoPagoEnMemoria,
    crear_servicio,
)

ENDPOINT = "/api/compras"
ENDPOINT_CONFIRMAR_PAGO = "/api/compras/confirmar-pago"
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

    def test_confirmar_pago_sin_identificar_al_usuario_recibe_401(self):
        cliente = crear_cliente()

        respuesta = cliente.post(ENDPOINT_CONFIRMAR_PAGO, json={"payment_id": "1"})

        assert respuesta.status_code == 401

    def test_confirmar_un_pago_no_aprobado_recibe_422(self):
        mercado_pago = ApiMercadoPagoEnMemoria()
        cliente = crear_cliente(crear_servicio(api_mercado_pago=mercado_pago))
        cliente.post(ENDPOINT, json=CUERPO_VALIDO, headers=CABECERAS)
        payment_id = mercado_pago.pagar("rejected")

        respuesta = cliente.post(
            ENDPOINT_CONFIRMAR_PAGO, json={"payment_id": payment_id}, headers=CABECERAS
        )

        assert respuesta.status_code == 422
        assert respuesta.json()["detail"] == "El pago no fue aprobado por Mercado Pago"

    def test_confirmar_el_pago_de_otro_usuario_recibe_403(self):
        mercado_pago = ApiMercadoPagoEnMemoria()
        cliente = crear_cliente(crear_servicio(api_mercado_pago=mercado_pago))
        cliente.post(ENDPOINT, json=CUERPO_VALIDO, headers=CABECERAS)
        payment_id = mercado_pago.pagar("approved")

        respuesta = cliente.post(
            ENDPOINT_CONFIRMAR_PAGO,
            json={"payment_id": payment_id},
            headers={"X-Usuario-Email": OTRO_USUARIO_REGISTRADO},
        )

        assert respuesta.status_code == 403


class TestCors:

    def test_sin_configurar_solo_permite_el_frontend_local(self):
        assert origenes_permitidos(None) == ["http://localhost:5173"]

    def test_suma_los_origenes_configurados_sin_barra_final(self):
        valor = "https://ecoharmony.vercel.app/, https://otro.vercel.app"

        assert origenes_permitidos(valor) == [
            "http://localhost:5173",
            "https://ecoharmony.vercel.app",
            "https://otro.vercel.app",
        ]

    def test_el_frontend_local_puede_llamar_a_la_api(self):
        respuesta = TestClient(app).options(
            ENDPOINT,
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type,x-usuario-email",
            },
        )

        assert respuesta.status_code == 200
        assert respuesta.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_salud_responde_ok():
    respuesta = TestClient(app).get("/salud")

    assert respuesta.status_code == 200
    assert respuesta.json() == {"estado": "ok"}


CONFIGURACION_COMPLETA = {
    "MP_ACCESS_TOKEN": "TEST-token",
    "SMTP_USUARIO": "entradas@ecoharmony.test",
    "SMTP_CONTRASENA": "clave-de-prueba",
}


@pytest.fixture
def entorno(monkeypatch):
    """Variables de entorno controladas y servicio sin cachear entre tests."""
    for nombre, valor in CONFIGURACION_COMPLETA.items():
        monkeypatch.setenv(nombre, valor)
    obtener_servicio_compra.cache_clear()
    yield monkeypatch
    obtener_servicio_compra.cache_clear()


def test_la_app_usa_un_unico_servicio_para_conservar_las_compras_entre_requests(entorno):
    primero = obtener_servicio_compra()
    segundo = obtener_servicio_compra()

    assert isinstance(primero, ServicioCompra)
    assert primero is segundo


@pytest.mark.parametrize("variable", sorted(CONFIGURACION_COMPLETA))
def test_sin_configurar_mercado_pago_o_smtp_la_app_no_arranca(entorno, variable):
    entorno.delenv(variable)

    with pytest.raises(ConfiguracionFaltanteError, match=variable):
        obtener_servicio_compra()
