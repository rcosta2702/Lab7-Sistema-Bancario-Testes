import sqlite3

import pytest

from banco.servico import Banco


def test_i01_persistencia_apos_reabrir(tmp_path):
    caminho = tmp_path / "conta.sqlite3"
    banco = Banco(caminho)
    assert banco.saldo() == 0
    banco.movimentar("depositar", "100.50")
    banco.movimentar("sacar", "40.25")
    assert Banco(caminho).saldo() == 6025


def test_i02_falha_preserva_saldo(tmp_path):
    banco = Banco(tmp_path / "conta.sqlite3")
    banco.movimentar("depositar", "50")
    with pytest.raises(ValueError, match="Saldo insuficiente"):
        banco.movimentar("sacar", "50.01")
    assert banco.saldo() == 5000
    banco.movimentar("depositar", "1")
    assert banco.saldo() == 5100


def test_i03_entrada_invalida_nao_persiste(tmp_path):
    banco = Banco(tmp_path / "conta.sqlite3")
    with pytest.raises(ValueError):
        banco.movimentar("depositar", "1.001")
    with pytest.raises(ValueError):
        banco.movimentar("apagar", "1")
    assert banco.saldo() == 0


def test_i04_duas_instancias_compartilham_saldo(tmp_path):
    caminho = tmp_path / "conta.sqlite3"
    primeiro, segundo = Banco(caminho), Banco(caminho)
    primeiro.movimentar("depositar", "10")
    segundo.movimentar("depositar", "20")
    assert primeiro.saldo() == 3000
