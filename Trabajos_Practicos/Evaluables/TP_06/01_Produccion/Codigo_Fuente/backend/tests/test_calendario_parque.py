from datetime import date

from app.servicio.calendario_parque import CalendarioParque


class TestCalendarioParque:

    def test_cerrado_los_lunes(self):
        assert CalendarioParque().esta_abierto(date(2026, 10, 12)) is False

    def test_abierto_un_martes(self):
        assert CalendarioParque().esta_abierto(date(2026, 10, 13)) is True
