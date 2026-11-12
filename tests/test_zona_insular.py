"""Pruebas de aceptación para la nueva zona insular."""

import pytest

from envios import calc


@pytest.mark.parametrize(
    "peso, cliente, dia, total",
    [
        pytest.param(2, "normal", 4, 10200, id="SC-01"),
        pytest.param(4, "vip", 6, 15000, id="SC-02"),
    ],
)
def test_tarifa_insular_sin_cupon(peso, cliente, dia, total):
    assert calc(peso, "insular", cliente, dia) == total


@pytest.mark.parametrize(
    "cupon",
    [pytest.param("ENVIO10", id="SC-03"), pytest.param("OTRO", id="SC-04")],
)
def test_zona_insular_rechaza_cualquier_cupon(cupon):
    with pytest.raises(ValueError, match="^la zona insular no acepta cupones$"):
        calc(2, "insular", "normal", 4, cupon)
