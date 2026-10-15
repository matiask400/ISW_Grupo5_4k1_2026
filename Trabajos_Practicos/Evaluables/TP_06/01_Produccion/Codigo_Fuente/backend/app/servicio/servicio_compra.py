from app.modelos.modelos import ResultadoCompra, SolicitudCompra

MINIMO_ENTRADAS_POR_COMPRA = 1
MAXIMO_ENTRADAS_POR_COMPRA = 10


class ServicioCompra:
    def comprar(self, solicitud: SolicitudCompra) -> ResultadoCompra:
        error = (
            self._validar_cantidad(solicitud)
            or self._validar_visitantes(solicitud)
            or self._validar_forma_pago(solicitud)
        )
        if error:
            return ResultadoCompra.fallida(error)
        return ResultadoCompra.ok()

    @staticmethod
    def _validar_cantidad(solicitud: SolicitudCompra) -> str | None:
        if solicitud.cantidad < MINIMO_ENTRADAS_POR_COMPRA:
            return "Debe comprar al menos 1 entrada"
        if solicitud.cantidad > MAXIMO_ENTRADAS_POR_COMPRA:
            return f"La cantidad de entradas no puede superar {MAXIMO_ENTRADAS_POR_COMPRA}"
        return None

    @staticmethod
    def _validar_visitantes(solicitud: SolicitudCompra) -> str | None:
        if len(solicitud.edades) != solicitud.cantidad:
            return "Debe indicar la edad de cada visitante"
        if any(edad < 0 for edad in solicitud.edades):
            return "Las edades deben estar entre 0 y 120"
        return None

    @staticmethod
    def _validar_forma_pago(solicitud: SolicitudCompra) -> str | None:
        if solicitud.forma_pago is None:
            return "Debe seleccionar una forma de pago"
        return None
