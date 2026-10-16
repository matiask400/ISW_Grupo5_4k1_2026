from app.modelos.modelos import TipoPase

PRECIOS_BASE = {TipoPase.REGULAR: 10000, TipoPase.VIP: 20000}  # FAQ 6


class Tarifario:
    def precio(self, tipo_pase: TipoPase, edad: int) -> int:
        precio_base = PRECIOS_BASE[tipo_pase]
        if edad <= 15:
            return precio_base // 2
        return precio_base
