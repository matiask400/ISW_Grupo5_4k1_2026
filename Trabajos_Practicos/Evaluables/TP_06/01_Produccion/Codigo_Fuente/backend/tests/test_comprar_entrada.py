import pytest
from app.modelos.modelos import SolicitudCompra, TipoPase, FormaPago
from app.servicio.servicio_compra import ServicioCompra
from datetime import date

"""
Probar comprar entradas ingresando una cantidad de entradas mayor a 10
"""

class TestComprarEntrada:

    def test_no_deberia_comprar_mas_10_entradas(self):
        servicio = ServicioCompra()

        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 12, 15),
            cantidad=11,
            edades=[30] * 11,
            tipo_pase= TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )
        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == ("La cantidad de entradas no puede superar 10")

    def test_no_deberia_comprar_sin_seleccionar_forma_de_pago(self):
        servicio = ServicioCompra()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 12, 15),
            cantidad=2,
            edades=[30, 25],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=None,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Debe seleccionar una forma de pago"

    def test_rechaza_0_entradas(self):
        servicio = ServicioCompra()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 12, 15),
            cantidad=0,
            edades=[],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )
        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Debe comprar al menos 1 entrada"

    def test_rechaza_cantidad_menor_a_1(self):
        servicio = ServicioCompra()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 12, 15),
            cantidad=-1,
            edades=[],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Debe comprar al menos 1 entrada"

    def test_permite_comprar_2_entradas(self):
        servicio = ServicioCompra()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 12, 15),
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True

    def test_permite_exactamente_10_entradas(self):
        servicio = ServicioCompra()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 12, 15),
            cantidad=10,
            edades=[30] * 10,
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True

    def test_rechaza_si_falta_la_edad_de_algun_visitante(self):
        servicio = ServicioCompra()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 12, 15),
            cantidad=3,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Debe indicar la edad de cada visitante"

    def test_rechaza_edad_negativa(self):
        servicio = ServicioCompra()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 12, 15),
            cantidad=2,
            edades=[30, -1],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Las edades deben estar entre 0 y 120"

    def test_rechaza_edad_mayor_a_120(self):
        servicio = ServicioCompra()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 12, 15),
            cantidad=2,
            edades=[30, 121],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Las edades deben estar entre 0 y 120"

    def test_permite_edades_en_los_limites(self):
        servicio = ServicioCompra()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 12, 15),
            cantidad=2,
            edades=[0, 120],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True

    def test_no_deberia_comprar_sin_tipo_de_pase(self):
        servicio = ServicioCompra()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 12, 15),
            cantidad=2,
            edades=[30, 28],
            tipo_pase=None,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Debe seleccionar un tipo de pase"
