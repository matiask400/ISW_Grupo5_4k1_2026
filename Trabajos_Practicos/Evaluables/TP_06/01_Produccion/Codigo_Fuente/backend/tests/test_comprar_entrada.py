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
