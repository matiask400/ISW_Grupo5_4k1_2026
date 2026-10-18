URL_MERCADO_PAGO_SIMULADO = "http://localhost:5173/mercado-pago-simulado"


class PasarelaMercadoPagoSimulada:
    """Pasarela sin red: se usa sin MP_ACCESS_TOKEN y en los tests del servicio."""

    def __init__(self, url_base: str = URL_MERCADO_PAGO_SIMULADO) -> None:
        self._url_base = url_base
        self.pagos_creados: list[int] = []

    def crear_link_de_pago(self, monto: int) -> str:
        self.pagos_creados.append(monto)
        return f"{self._url_base}?monto={monto}"
