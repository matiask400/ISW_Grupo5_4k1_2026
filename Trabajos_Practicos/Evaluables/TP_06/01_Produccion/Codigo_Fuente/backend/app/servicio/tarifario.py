from app.modelos.modelos import TipoPase

PRECIOS_BASE = {TipoPase.REGULAR: 10000, TipoPase.VIP: 20000}
EDAD_MAXIMA_GRATIS = 3
EDAD_MAXIMA_MENOR = 15
EDAD_MINIMA_MAYOR = 60
PORCENTAJE_DESCUENTO = 50


class Tarifario:
    def precio(self, tipo_pase: TipoPase, edad: int) -> int:
        precio_base = PRECIOS_BASE[tipo_pase]
        if edad <= EDAD_MAXIMA_GRATIS:
            return 0
        if self._tiene_descuento(edad):
            return precio_base * (100 - PORCENTAJE_DESCUENTO) // 100
        return precio_base

    @staticmethod
    def _tiene_descuento(edad: int) -> bool:
        return edad <= EDAD_MAXIMA_MENOR or edad >= EDAD_MINIMA_MAYOR
