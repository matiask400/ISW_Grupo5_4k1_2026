from app.modelos.modelos import ResultadoCompra, SolicitudCompra


class ServicioCompra:
    def comprar(self, solicitud: SolicitudCompra) -> ResultadoCompra:
        if solicitud.cantidad > 10:
            return ResultadoCompra(
                exitosa=False, error="La cantidad de entradas no puede superar 10"
            )
        return ResultadoCompra(exitosa=True)