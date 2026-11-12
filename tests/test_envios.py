"""Casos de caja negra y blanca sobre los requisitos del cotizador."""

import pytest

from envios import calc


CAJA_NEGRA = [
    pytest.param((50, 'urbana', 'normal', 3, None), 41000, None, False, id='CN-01'),
    pytest.param((0, 'urbana', 'normal', 3, None), None, 'peso inválido', False, id='CN-02'),
    pytest.param((50.01, 'urbana', 'normal', 3, None), None, 'peso inválido', False, id='CN-03'),
    pytest.param((2, 'costera', 'normal', 3, None), None, None, False, id='CN-04'),
    pytest.param((2, 'rural', 'normal', 0, None), None, None, False, id='CN-05'),
    pytest.param((3, 'urbana', 'normal', 4, None), 6000, None, False, id='CN-06'),
    pytest.param((10, 'rural', 'normal', 4, None), 11300, None, False, id='CN-07'),
    pytest.param((10.5, 'nacional', 'normal', 4, None), 14100, None, False, id='CN-08'),
    pytest.param((4, 'rural', 'vip', 6, 'ENVIO10'), 10600, None, False, id='CN-09'),
    pytest.param((4, 'rural', 'frecuente', 7, 'OTRO'), 12700, None, False, id='CN-10'),
    pytest.param((2, 'urbana', 'vip', 3, 'ENVIO10'), 5000, None, False, id='CN-11'),
    pytest.param((-0.01, 'urbana', 'normal', 3, None), None, 'peso inválido', False, id='CN-12'),
    pytest.param((0.01, 'urbana', 'normal', 3, None), 6000, None, False, id='CN-13'),
    pytest.param((2.99, 'urbana', 'normal', 4, None), 6000, None, False, id='CN-14'),
    pytest.param((3.01, 'urbana', 'normal', 4, None), 9000, None, False, id='CN-15'),
    pytest.param((9.99, 'urbana', 'normal', 4, None), 9000, None, False, id='CN-16'),
    pytest.param((10.01, 'urbana', 'normal', 4, None), 9000, None, False, id='CN-17'),
    pytest.param((49.99, 'urbana', 'normal', 3, None), 41000, None, False, id='CN-18'),
    pytest.param((4, 'urbana', 'normal', 5, None), 9000, None, False, id='CN-19'),
    pytest.param((4, 'urbana', 'normal', 6, None), 11000, None, False, id='CN-20'),
    pytest.param((4, 'urbana', 'vip', 4, None), 7700, None, False, id='CN-21'),
    pytest.param((4, 'urbana', 'normal', 8, None), None, None, False, id='CN-22'),
    pytest.param((4, 'urbana', 'normal', 1, None), 9000, None, False, id='CN-23'),
    pytest.param((4, 'rural', 'frecuente', 7, None), 12700, None, False, id='CN-24'),
    pytest.param((4, 'urbana', 'normal', 4, 'ENVIO10'), 8100, None, False, id='CN-25'),
    pytest.param((10, 'urbana', 'normal', 4, None), 9000, None, False, id='CN-26'),
]

CAJA_BLANCA = [
    pytest.param((2.99, 'urbana', 'normal', 4, None), 6000, None, False, id='CB-01'),
    pytest.param((0, 'urbana', 'normal', 3, None), None, 'peso inválido', False, id='CB-02'),
    pytest.param((50.01, 'urbana', 'normal', 3, None), None, 'peso inválido', False, id='CB-03'),
    pytest.param((3.01, 'urbana', 'normal', 4, None), 9000, None, False, id='CB-04'),
    pytest.param((10.01, 'urbana', 'normal', 4, None), 9000, None, False, id='CB-05'),
    pytest.param((2.99, 'rural', 'normal', 4, None), 7500, None, False, id='CB-06'),
    pytest.param((2.99, 'nacional', 'normal', 4, None), 9000, None, False, id='CB-07'),
    pytest.param((2, 'costera', 'normal', 3, None), None, None, False, id='CB-08'),
    pytest.param((2.99, 'urbana', 'normal', 7, None), 8000, None, False, id='CB-09'),
    pytest.param((2.99, 'urbana', 'frecuente', 4, None), 5700, None, False, id='CB-10'),
    pytest.param((2.99, 'urbana', 'vip', 4, None), 5100, None, False, id='CB-11'),
    pytest.param((2.99, 'urbana', 'normal', 4, 'OTRO'), 6000, None, False, id='CB-12'),
    pytest.param((4, 'urbana', 'normal', 4, 'ENVIO10'), 8100, None, False, id='CB-13'),
    pytest.param((2, 'urbana', 'vip', 3, 'ENVIO10'), 5000, None, False, id='CB-14'),
    pytest.param((2.99, 'urbana', 'normal', 4, None), 6000, None, True, id='CB-15'),
]


def verificar_cotizacion(entradas, esperado, mensaje, diagnostico, capsys):
    if esperado is None:
        patron = f"^{mensaje}$" if mensaje else None
        with pytest.raises(ValueError, match=patron):
            calc(*entradas)
        return

    resultado = calc(*entradas, flag=True) if diagnostico else calc(*entradas)
    assert resultado == esperado
    if diagnostico:
        assert capsys.readouterr().out.startswith("costo:")


@pytest.mark.parametrize("entradas, esperado, mensaje, diagnostico", CAJA_NEGRA)
def test_requisitos(entradas, esperado, mensaje, diagnostico, capsys):
    verificar_cotizacion(entradas, esperado, mensaje, diagnostico, capsys)


@pytest.mark.parametrize("entradas, esperado, mensaje, diagnostico", CAJA_BLANCA)
def test_caminos(entradas, esperado, mensaje, diagnostico, capsys):
    verificar_cotizacion(entradas, esperado, mensaje, diagnostico, capsys)
