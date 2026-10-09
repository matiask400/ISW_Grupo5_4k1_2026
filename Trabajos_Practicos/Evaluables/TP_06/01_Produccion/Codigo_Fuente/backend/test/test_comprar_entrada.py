import pytest
from app.modelos.SolicitudCompra import SolicitudCompra
from app.servicio.comprar_entrada import comprar_entrada
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
            tipo_pase="REGULAR",
            forma_pago="EFECTIVO",
        )
        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "La cantidad de entradas no puede superar 10"
