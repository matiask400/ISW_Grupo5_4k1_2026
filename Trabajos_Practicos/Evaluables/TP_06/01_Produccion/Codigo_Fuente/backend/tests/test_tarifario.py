from app.modelos.modelos import TipoPase
from app.servicio.tarifario import Tarifario
import pytest

class TestTarifario:

    def test_adulto_con_pase_regular_paga_10000(self):
        assert Tarifario().precio(TipoPase.REGULAR, 30) == 10000

    def test_adulto_con_pase_vip_paga_20000(self):
        assert Tarifario().precio(TipoPase.VIP, 30) == 20000

    def test_nino_de_10_anios_paga_la_mitad(self):
        assert Tarifario().precio(TipoPase.REGULAR, 10) == 5000

    def test_bebe_de_2_anios_no_paga(self):
        assert Tarifario().precio(TipoPase.REGULAR, 2) == 0

    def test_mayor_de_65_anios_paga_la_mitad(self):
        assert Tarifario().precio(TipoPase.REGULAR, 65) == 5000

    @pytest.mark.parametrize(
        ("tipo_pase", "edad", "precio_esperado"),
        [
            (TipoPase.REGULAR, 3, 0),       # último gratis
            (TipoPase.REGULAR, 4, 5000),    # primero con descuento de menor
            (TipoPase.REGULAR, 15, 5000),   # último menor
            (TipoPase.REGULAR, 16, 10000),  # primero sin descuento
            (TipoPase.REGULAR, 59, 10000),  # último sin descuento
            (TipoPase.REGULAR, 60, 5000),   # primero con descuento de mayor
            (TipoPase.VIP, 3, 0),
            (TipoPase.VIP, 10, 10000),
            (TipoPase.VIP, 60, 10000),
        ],
    )
    def test_precio_en_los_bordes_de_cada_tramo(self, tipo_pase, edad, precio_esperado):
        assert Tarifario().precio(tipo_pase, edad) == precio_esperado
