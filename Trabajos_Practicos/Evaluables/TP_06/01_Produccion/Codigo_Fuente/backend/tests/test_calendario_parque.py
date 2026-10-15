from datetime import date

from app.servicio.calendario_parque import CalendarioParque


class TestCalendarioParque:

    def test_cerrado_los_lunes(self):
        assert CalendarioParque().esta_abierto(date(2026, 10, 12)) is False

    def test_abierto_un_martes(self):
        assert CalendarioParque().esta_abierto(date(2026, 10, 13)) is True

    def test_cerrado_el_25_de_diciembre(self):
        assert CalendarioParque().esta_abierto(date(2026, 12, 25)) is False

    def test_cerrado_el_25_de_diciembre_de_cualquier_anio(self):
        assert CalendarioParque().esta_abierto(date(2027, 12, 25)) is False

    def test_cerrado_el_1_de_enero(self):
        assert CalendarioParque().esta_abierto(date(2027, 1, 1)) is False
