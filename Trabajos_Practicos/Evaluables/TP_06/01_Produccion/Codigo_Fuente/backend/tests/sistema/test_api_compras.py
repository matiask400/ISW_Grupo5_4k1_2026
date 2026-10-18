import pytest
from fastapi.testclient import TestClient

from app.api.dependencias import ConfiguracionFaltanteError, obtener_servicio_compra
from app.main import app
from app.servicios.servicio_compra import ServicioCompra
from tests.integracion.test_comprar_entrada import USUARIO_REGISTRADO, crear_servicio

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
    """Cliente HTTP de prueba que usa un servicio con datos y reloj controlados."""
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
