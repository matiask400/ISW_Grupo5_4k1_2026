from app.modelos.modelos import TipoPase


class Tarifario:
    def precio(self, tipo_pase: TipoPase, edad: int) -> int:
        return 10000
