from datetime import date

LUNES = 0  # convención de date.weekday(): 0 = lunes ... 6 = domingo


class CalendarioParque:
    def esta_abierto(self, fecha: date) -> bool:
        return fecha.weekday() != LUNES
