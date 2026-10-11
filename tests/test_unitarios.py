import pytest

from banco.dominio import centavos, depositar, formatar, sacar


@pytest.mark.parametrize("entrada,esperado", [("0.01", 1), ("100,50", 10050), ("100", 10000), ("999999999.99", 99999999999)])
def test_u01_converter_valor(entrada, esperado):
    assert centavos(entrada) == esperado


@pytest.mark.parametrize("entrada", ["0", "-1", "NaN", "Infinity", "1.001", "abc", "", "1000000000", True, None])
def test_u02_rejeitar_valor(entrada):
    with pytest.raises(ValueError):
        centavos(entrada)


def test_u03_deposito_exato():
    assert depositar(10010, 20) == 10030
    assert formatar(10030) == "100.30"


def test_u04_saque_total():
    assert sacar(10000, 10000) == 0


def test_u05_saque_insuficiente():
    with pytest.raises(ValueError, match="Saldo insuficiente"):
        sacar(10000, 10001)


@pytest.mark.parametrize("operacao", [depositar, sacar])
@pytest.mark.parametrize("valor", [0, -1, True, 0.1])
def test_u06_operacao_invalida(operacao, valor):
    with pytest.raises(ValueError):
        operacao(10000, valor)


def test_u07_limite_de_saldo():
    with pytest.raises(ValueError, match="Limite"):
        depositar(99_999_999_999, 1)
