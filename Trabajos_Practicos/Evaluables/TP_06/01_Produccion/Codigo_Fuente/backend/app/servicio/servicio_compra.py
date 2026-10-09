from app.modelos.modelos import ResultadoCompra, SolicitudCompra


MAXIMO_ENTRADAS_POR_COMPRA = 10


class ServicioCompra:
    def comprar(self, solicitud: SolicitudCompra) -> ResultadoCompra:
        if solicitud.cantidad > MAXIMO_ENTRADAS_POR_COMPRA:
            return ResultadoCompra.fallida(
                f"La cantidad de entradas no puede superar {MAXIMO_ENTRADAS_POR_COMPRA}"
            )
        return ResultadoCompra.ok()