from datetime import date

LUNES = 0
FERIADOS_CERRADO = {(12, 25), (1, 1)}  # (mes, día)


class CalendarioParque:
    def esta_abierto(self, fecha: date) -> bool:
        es_feriado = (fecha.month, fecha.day) in FERIADOS_CERRADO
        return fecha.weekday() != LUNES and not es_feriado
