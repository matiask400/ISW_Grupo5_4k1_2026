from datetime import date, datetime, timedelta
from app.modelos.modelos import FormaPago, SolicitudCompra, TipoPase
from app.servicio.servicio_compra import ServicioCompra
from app.servicio.repositorio_usuarios import RepositorioUsuariosEnMemoria
from app.servicio.repositorio_compras import RepositorioComprasEnMemoria

AHORA = datetime(2026, 10, 22, 10, 0)
HOY = AHORA.date()
FECHA_VALIDA = date(2026, 10, 29)
USUARIO_REGISTRADO = "ana@mail.com"
OTRO_USUARIO_REGISTRADO = "juan@mail.com"


def crear_servicio(ahora: datetime = AHORA) -> ServicioCompra:
    return ServicioCompra(
        ahora=lambda: ahora,
        usuarios=RepositorioUsuariosEnMemoria({USUARIO_REGISTRADO, OTRO_USUARIO_REGISTRADO}),
        compras=RepositorioComprasEnMemoria(),
    )

class TestComprarEntrada:

    def test_no_deberia_comprar_mas_10_entradas(self):
        servicio = crear_servicio()

        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=11,
            edades=[30] * 11,
            tipo_pase= TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )
        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == ("La cantidad de entradas no puede superar 10")

    def test_no_deberia_comprar_sin_seleccionar_forma_de_pago(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, 25],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=None,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Debe seleccionar una forma de pago"

    def test_rechaza_0_entradas(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=0,
            edades=[],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )
        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Debe comprar al menos 1 entrada"

    def test_rechaza_cantidad_menor_a_1(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=-1,
            edades=[],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Debe comprar al menos 1 entrada"

    def test_permite_comprar_2_entradas(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True

    def test_permite_exactamente_10_entradas(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=10,
            edades=[30] * 10,
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True

    def test_rechaza_si_falta_la_edad_de_algun_visitante(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=3,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Debe indicar la edad de cada visitante"

    def test_rechaza_edad_negativa(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, -1],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Las edades deben estar entre 0 y 120"

    def test_rechaza_edad_mayor_a_120(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, 121],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Las edades deben estar entre 0 y 120"

    def test_permite_edades_en_los_limites(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[0, 120],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True

    def test_no_deberia_comprar_sin_tipo_de_pase(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=None,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Debe seleccionar un tipo de pase"

    def test_permite_comprar_pase_vip(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.VIP,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True

    def test_rechaza_fecha_de_visita_pasada(self):
        servicio = crear_servicio()
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

    def test_permite_comprar_para_hoy_a_las_17_30_en_punto(self):
        servicio = crear_servicio(ahora=datetime(2026, 10, 22, 17, 30))
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

    def test_despues_de_las_17_30_puede_comprar_para_otro_dia(self):
        servicio = crear_servicio(ahora=datetime(2026, 10, 22, 17, 31))
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True

    def test_no_deberia_comprar_un_usuario_no_registrado(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="intruso@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is False
        assert resultado.error == "Debe estar registrado para comprar entradas"

    def test_no_deberia_superar_10_entradas_sumando_compras_de_la_misma_fecha(self):
        servicio = crear_servicio()
        primera_compra = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=8,
            edades=[30] * 8,
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )
        segunda_compra = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=3,
            edades=[30] * 3,
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )
        servicio.comprar(primera_compra)

        resultado = servicio.comprar(segunda_compra)

        assert resultado.exitosa is False
        assert resultado.error == (
            "Solo puede comprar hasta 10 entradas por fecha. Ya compró 8 para ese día"
        )

    def test_otro_usuario_puede_comprar_para_la_misma_fecha(self):
        servicio = crear_servicio()
        compra_de_ana = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=10,
            edades=[30] * 10,
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )
        compra_de_juan = SolicitudCompra(
            usuario_email="juan@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[40, 38],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )
        servicio.comprar(compra_de_ana)

        resultado = servicio.comprar(compra_de_juan)

        assert resultado.exitosa is True

    def test_mismo_usuario_puede_comprar_para_otra_fecha(self):
        servicio = crear_servicio()
        compra_del_jueves = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=10,
            edades=[30] * 10,
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )
        compra_del_viernes = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 10, 30),  # Fecha posterior
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )
        servicio.comprar(compra_del_jueves)

        resultado = servicio.comprar(compra_del_viernes)

        assert resultado.exitosa is True

    def test_permite_completar_exactamente_10_entradas_en_varias_compras(self):
        servicio = crear_servicio()
        primera_compra = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=8,
            edades=[30] * 8,
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )
        segunda_compra = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )
        servicio.comprar(primera_compra)

        resultado = servicio.comprar(segunda_compra)

        assert resultado.exitosa is True

    def test_una_compra_fallida_no_suma_al_total_del_dia(self):
        servicio = crear_servicio()
        compra_fallida = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=8,
            edades=[30] * 8,
            tipo_pase=TipoPase.REGULAR,
            forma_pago=None,
        )
        compra_valida = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=10,
            edades=[30] * 10,
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )
        servicio.comprar(compra_fallida)

        resultado = servicio.comprar(compra_valida)

        assert resultado.exitosa is True

    def test_informa_el_monto_total_segun_tipo_de_pase_y_edades(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=4,
            edades=[35, 33, 10, 2],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.exitosa is True
        assert resultado.monto_total == 25000

    def test_informa_cantidad_y_fecha_al_finalizar_la_compra(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.cantidad == 2
        assert resultado.fecha_visita == FECHA_VALIDA

    def test_informa_un_mensaje_con_cantidad_fecha_y_total(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.mensaje == "Compraste 2 entradas para el 29/10/2026. Total: $20.000"

    def test_con_una_sola_entrada_el_mensaje_esta_en_singular(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=date(2026, 10, 30),
            cantidad=1,
            edades=[30],
            tipo_pase=TipoPase.VIP,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.mensaje == "Compraste 1 entrada para el 30/10/2026. Total: $20.000"

    def test_una_compra_fallida_no_tiene_mensaje_de_confirmacion(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=11,
            edades=[30] * 11,
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.mensaje is None

    def test_pago_con_tarjeta_devuelve_url_de_mercado_pago(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.TARJETA,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.url_pago == "http://localhost:5173/mercado-pago-simulado?monto=20000"

    def test_pago_en_efectivo_no_redirige_a_mercado_pago(self):
        servicio = crear_servicio()
        solicitud = SolicitudCompra(
            usuario_email="ana@mail.com",
            fecha_visita=FECHA_VALIDA,
            cantidad=2,
            edades=[30, 28],
            tipo_pase=TipoPase.REGULAR,
            forma_pago=FormaPago.EFECTIVO,
        )

        resultado = servicio.comprar(solicitud)

        assert resultado.url_pago is None
