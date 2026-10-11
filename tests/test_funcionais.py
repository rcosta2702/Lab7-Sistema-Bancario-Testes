import json
from pathlib import Path
import subprocess
import sys

APP = Path(__file__).resolve().parents[1] / "app.py"


def executar(caminho, *argumentos):
    resultado = subprocess.run([sys.executable, str(APP), "--banco", str(caminho), *argumentos], capture_output=True, text=True, encoding="utf-8", env={**__import__('os').environ, "PYTHONIOENCODING": "utf-8"}, timeout=15)
    return resultado.returncode, json.loads(resultado.stdout)


def test_f01_jornada_cliente(tmp_path):
    caminho = tmp_path / "cliente.sqlite3"
    assert executar(caminho, "saldo") == (0, {"saldo": "0.00"})
    assert executar(caminho, "depositar", "100,50") == (0, {"saldo": "100.50"})
    assert executar(caminho, "sacar", "40.25") == (0, {"saldo": "60.25"})
    assert executar(caminho, "saldo") == (0, {"saldo": "60.25"})


def test_f02_saque_recusado(tmp_path):
    caminho = tmp_path / "cliente.sqlite3"
    executar(caminho, "depositar", "10")
    assert executar(caminho, "sacar", "11") == (1, {"erro": "Saldo insuficiente."})
    assert executar(caminho, "saldo") == (0, {"saldo": "10.00"})


def test_f03_valor_invalido(tmp_path):
    caminho = tmp_path / "cliente.sqlite3"
    codigo, resposta = executar(caminho, "depositar", "abc")
    assert codigo == 1 and "erro" in resposta
    assert executar(caminho, "saldo") == (0, {"saldo": "0.00"})


def test_f04_falha_de_armazenamento(tmp_path):
    assert executar(tmp_path / "inexistente" / "conta.sqlite3", "saldo") == (1, {"erro": "Não foi possível acessar o banco de dados."})
