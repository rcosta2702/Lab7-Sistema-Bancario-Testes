import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

import pytest

from banco.servico import Banco


def test_p01_transferencia_conserva_total(tmp_path):
    banco = Banco(tmp_path / "conta.sqlite3")
    banco.movimentar("depositar", "100")
    assert banco.investir("40.25") == (5975, 4025)
    assert banco.posicao() == (5975, 4025)
    assert sum(banco.posicao()) == 10000


def test_p02_investir_todo_saldo_e_persistir(tmp_path):
    caminho = tmp_path / "conta.sqlite3"
    banco = Banco(caminho)
    banco.movimentar("depositar", "0.01")
    assert banco.investir("0.01") == (0, 1)
    assert Banco(caminho).posicao() == (0, 1)


def test_p03_insuficiente_nao_altera(tmp_path):
    banco = Banco(tmp_path / "conta.sqlite3")
    banco.movimentar("depositar", "10")
    with pytest.raises(ValueError, match="Saldo insuficiente"):
        banco.investir("10.01")
    assert banco.posicao() == (1000, 0)


@pytest.mark.parametrize("valor", ["0", "-1", "1.001", "NaN", "abc"])
def test_p04_valor_invalido(tmp_path, valor):
    banco = Banco(tmp_path / "conta.sqlite3")
    banco.movimentar("depositar", "10")
    with pytest.raises(ValueError):
        banco.investir(valor)
    assert banco.posicao() == (1000, 0)


def test_p05_migracao_preserva_versao_inicial(tmp_path):
    caminho = tmp_path / "legado.sqlite3"
    with sqlite3.connect(caminho) as conexao:
        conexao.execute("CREATE TABLE conta(id INTEGER PRIMARY KEY CHECK(id=1), saldo INTEGER NOT NULL CHECK(saldo>=0))")
        conexao.execute("INSERT INTO conta VALUES(1, 12345)")
    assert Banco(caminho).posicao() == (12345, 0)
    banco = Banco(caminho)
    banco.investir("23.45")
    assert Banco(caminho).posicao() == (10000, 2345)


def test_p06_rollback_falha_no_banco(tmp_path):
    caminho = tmp_path / "conta.sqlite3"
    banco = Banco(caminho)
    banco.movimentar("depositar", "100")
    with sqlite3.connect(caminho) as conexao:
        conexao.execute("CREATE TRIGGER falhar BEFORE UPDATE OF poupanca ON conta BEGIN SELECT RAISE(ABORT, 'falha simulada'); END")
    with pytest.raises(sqlite3.IntegrityError, match="falha simulada"):
        banco.investir("40")
    assert banco.posicao() == (10000, 0)


def test_p07_operacoes_antigas_apos_investir(tmp_path):
    banco = Banco(tmp_path / "conta.sqlite3")
    banco.movimentar("depositar", "100")
    banco.investir("40")
    banco.movimentar("depositar", "10")
    banco.movimentar("sacar", "20")
    assert banco.posicao() == (5000, 4000)
    assert banco.saldo() == 5000


def test_p08_jornada_funcional_poupanca(tmp_path):
    app = Path(__file__).resolve().parents[1] / "app.py"
    caminho = tmp_path / "cliente.sqlite3"
    def executar(*args):
        retorno = subprocess.run([sys.executable, str(app), "--banco", str(caminho), *args], capture_output=True, text=True, encoding="utf-8", env={**os.environ, "PYTHONIOENCODING": "utf-8"}, timeout=15)
        return retorno.returncode, json.loads(retorno.stdout)
    assert executar("depositar", "200") == (0, {"saldo": "200.00"})
    assert executar("investir", "75,50") == (0, {"saldo": "124.50", "poupanca": "75.50", "total": "200.00"})
    assert executar("poupanca") == (0, {"saldo": "124.50", "poupanca": "75.50", "total": "200.00"})
    assert executar("investir", "125") == (1, {"erro": "Saldo insuficiente."})
    assert executar("saldo") == (0, {"saldo": "124.50"})


def test_p09_investimentos_concorrentes(tmp_path):
    caminho = tmp_path / "conta.sqlite3"
    banco = Banco(caminho)
    banco.movimentar("depositar", "100")
    def tentar(_):
        try:
            Banco(caminho).investir("80")
            return True
        except ValueError:
            return False
    with ThreadPoolExecutor(max_workers=2) as executor:
        resultados = list(executor.map(tentar, range(2)))
    assert sorted(resultados) == [False, True]
    assert banco.posicao() == (2000, 8000)


def test_p10_limite_poupanca_preserva_corrente(tmp_path):
    banco = Banco(tmp_path / "conta.sqlite3")
    banco.movimentar("depositar", "999999999.99")
    banco.investir("999999999.99")
    banco.movimentar("depositar", "0.01")
    with pytest.raises(ValueError, match="Limite"):
        banco.investir("0.01")
    assert banco.posicao() == (1, 99_999_999_999)
