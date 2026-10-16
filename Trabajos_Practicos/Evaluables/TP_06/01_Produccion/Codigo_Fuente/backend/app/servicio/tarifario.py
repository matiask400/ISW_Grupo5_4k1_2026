from app.modelos.modelos import TipoPase

PRECIOS_BASE = {TipoPase.REGULAR: 10000, TipoPase.VIP: 20000}  # FAQ 6


class Tarifario:
    def precio(self, tipo_pase: TipoPase, edad: int) -> int:
        return PRECIOS_BASE[tipo_pase]
