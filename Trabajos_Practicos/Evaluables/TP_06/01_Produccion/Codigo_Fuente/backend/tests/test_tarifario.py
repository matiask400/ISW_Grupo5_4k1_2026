from app.modelos.modelos import TipoPase
from app.servicio.tarifario import Tarifario


class TestTarifario:

    def test_adulto_con_pase_regular_paga_10000(self):
        assert Tarifario().precio(TipoPase.REGULAR, 30) == 10000

    def test_adulto_con_pase_vip_paga_20000(self):
        assert Tarifario().precio(TipoPase.VIP, 30) == 20000
