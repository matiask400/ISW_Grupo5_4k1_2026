from app.modelos.modelos import TipoPase
from app.servicio.tarifario import Tarifario


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
