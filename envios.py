"""Cotizador de envíos con una estrategia de recargo por destino."""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Protocol

PESO_MAXIMO = Decimal("50")
LIMITE_TRAMO_1 = Decimal("3")
LIMITE_TRAMO_2 = Decimal("10")
TARIFA_TRAMO_1 = Decimal("6000")
TARIFA_TRAMO_2 = Decimal("9000")
COSTO_KG_EXCEDENTE = Decimal("800")
RECARGO_RURAL = Decimal("0.25")
RECARGO_NACIONAL = Decimal("0.50")
RECARGO_FIN_DE_SEMANA = Decimal("2000")
DESCUENTO_FRECUENTE = Decimal("0.05")
DESCUENTO_VIP = Decimal("0.15")
DESCUENTO_CUPON = Decimal("0.10")
CUPON_PROMOCIONAL = "ENVIO10"
COSTO_MINIMO = Decimal("5000")
UNIDAD_REDONDEO = Decimal("1E2")
DIAS_VALIDOS = range(1, 8)
DIAS_FIN_DE_SEMANA = (6, 7)


class EstrategiaZona(Protocol):
    def aplicar(self, tarifa: Decimal) -> Decimal:
        ...


class SinRecargo:
    def aplicar(self, tarifa: Decimal) -> Decimal:
        return tarifa


@dataclass(frozen=True)
class RecargoPorcentual:
    tasa: Decimal

    def aplicar(self, tarifa: Decimal) -> Decimal:
        return tarifa * (1 + self.tasa)


ESTRATEGIAS_ZONA: dict[str, EstrategiaZona] = {
    "urbana": SinRecargo(),
    "rural": RecargoPorcentual(RECARGO_RURAL),
    "nacional": RecargoPorcentual(RECARGO_NACIONAL),
}
DESCUENTOS_CLIENTE = {
    "frecuente": DESCUENTO_FRECUENTE,
    "vip": DESCUENTO_VIP,
}


def _validar_peso(peso: float) -> Decimal:
    peso_decimal = Decimal(str(peso))
    if not peso_decimal.is_finite() or not 0 < peso_decimal <= PESO_MAXIMO:
        raise ValueError("peso inválido")
    return peso_decimal


def _seleccionar_zona(zona: str) -> EstrategiaZona:
    estrategia = ESTRATEGIAS_ZONA.get(zona)
    if estrategia is None:
        raise ValueError("zona inválida")
    return estrategia


def _validar_dia(dia: int) -> None:
    if dia not in DIAS_VALIDOS:
        raise ValueError("día inválido")


def _tarifa_base(peso: Decimal) -> Decimal:
    if peso <= LIMITE_TRAMO_1:
        return TARIFA_TRAMO_1
    if peso <= LIMITE_TRAMO_2:
        return TARIFA_TRAMO_2
    return TARIFA_TRAMO_2 + (peso - LIMITE_TRAMO_2) * COSTO_KG_EXCEDENTE


def _aplicar_descuentos(tarifa: Decimal, cliente: str, cupon: str | None) -> Decimal:
    descuento = DESCUENTOS_CLIENTE.get(cliente, 0)
    tarifa *= 1 - descuento
    if cupon == CUPON_PROMOCIONAL:
        tarifa *= 1 - DESCUENTO_CUPON
    return tarifa


def _aplicar_recargo_fin_de_semana(tarifa: Decimal, dia: int) -> Decimal:
    if dia in DIAS_FIN_DE_SEMANA:
        return tarifa + RECARGO_FIN_DE_SEMANA
    return tarifa


def _total(tarifa: Decimal) -> int:
    return int(max(tarifa, COSTO_MINIMO).quantize(UNIDAD_REDONDEO, ROUND_HALF_UP))


def calc(p, z, c, d, cup=None):
    """Devuelve el costo en pesos de un envío."""
    peso = _validar_peso(p)
    estrategia = _seleccionar_zona(z)
    _validar_dia(d)
    tarifa = estrategia.aplicar(_tarifa_base(peso))
    tarifa = _aplicar_descuentos(tarifa, c, cup)
    return _total(_aplicar_recargo_fin_de_semana(tarifa, d))
