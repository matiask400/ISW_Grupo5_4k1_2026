from datetime import date, datetime, timedelta
from app.modelos.modelos import FormaPago, SolicitudCompra, TipoPase
from app.servicio.servicio_compra import ServicioCompra

AHORA = datetime(2026, 10, 22, 10, 0)
HOY = AHORA.date()
FECHA_VALIDA = date(2026, 10, 29)


def crear_servicio(ahora: datetime = AHORA) -> ServicioCompra:
    return ServicioCompra(ahora=lambda: ahora)


class TestComprarEntrada:

    def test_no_deberia_comprar_mas_10_entradas(self):
        servicio = ServicioCompra()

        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 12, 15),
            cantidad=11,
            edades=[30] * 11,
            tipo_pase= TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )
        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == ("La cantidad de entradas no puede superar 10")

    def test_no_deberia_comprar_sin_seleccionar_forma_de_pago(self):
        servicio = ServicioCompra()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 12, 15),
            cantidad=2,
            edades=[30, 25],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=None,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Debe seleccionar una forma de pago"

    def test_rechaza_0_entradas(self):
        servicio = ServicioCompra()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 12, 15),
            cantidad=0,
            edades=[],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )
        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Debe comprar al menos 1 entrada"

    def test_rechaza_cantidad_menor_a_1(self):
        servicio = ServicioCompra()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 12, 15),
            cantidad=-1,
            edades=[],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Debe comprar al menos 1 entrada"

    def test_permite_comprar_2_entradas(self):
        servicio = ServicioCompra()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 12, 15),
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True

    def test_permite_exactamente_10_entradas(self):
        servicio = ServicioCompra()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 12, 15),
            cantidad=10,
            edades=[30] * 10,
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True

    def test_rechaza_si_falta_la_edad_de_algun_visitante(self):
        servicio = ServicioCompra()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 12, 15),
            cantidad=3,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Debe indicar la edad de cada visitante"

    def test_rechaza_edad_negativa(self):
        servicio = ServicioCompra()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 12, 15),
            cantidad=2,
            edades=[30, -1],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Las edades deben estar entre 0 y 120"

    def test_rechaza_edad_mayor_a_120(self):
        servicio = ServicioCompra()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 12, 15),
            cantidad=2,
            edades=[30, 121],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Las edades deben estar entre 0 y 120"

    def test_permite_edades_en_los_limites(self):
        servicio = ServicioCompra()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 12, 15),
            cantidad=2,
            edades=[0, 120],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True

    def test_no_deberia_comprar_sin_tipo_de_pase(self):
        servicio = ServicioCompra()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 12, 15),
            cantidad=2,
            edades=[30, 28],
            tipo_pase=None,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Debe seleccionar un tipo de pase"

    def test_permite_comprar_pase_vip(self):
        servicio = ServicioCompra()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 12, 15),
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.VIP,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True

    def test_rechaza_fecha_de_visita_pasada(self):
        servicio = ServicioCompra()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 10, 7),
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "La fecha de visita debe ser hoy o una fecha futura"

    def test_rechaza_otra_fecha_pasada(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=HOY - timedelta(days=1),
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "La fecha de visita debe ser hoy o una fecha futura"

    def test_permite_comprar_para_el_dia_de_hoy(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=HOY,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True

    def test_no_deberia_comprar_si_el_parque_esta_cerrado(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 10, 26),
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "El parque está cerrado en la fecha seleccionada"

    def test_no_deberia_comprar_con_mas_de_un_mes_de_anticipacion(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 11, 24),
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Solo se pueden comprar entradas con hasta 1 mes de anticipación"

    def test_permite_comprar_justo_un_mes_despues_cruzando_el_anio(self):
        servicio = crear_servicio(ahora=datetime(2026, 12, 20, 10, 0))
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2027, 1, 20),
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True

    def test_permite_comprar_exactamente_un_mes_despues(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 11, 22),
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True

    def test_permite_comprar_hasta_fin_del_mes_siguiente_corto(self):
        servicio = crear_servicio(ahora=datetime(2027, 1, 31, 10, 0))
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2027, 2, 28),
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True

    def test_no_deberia_comprar_para_hoy_despues_de_las_17_30(self):
        servicio = crear_servicio(ahora=datetime(2026, 10, 22, 17, 31))
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=HOY,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Las compras para el día de hoy se permiten hasta las 17:30"
