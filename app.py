"""Interface de comandos do banco didático. Execute com --help."""

import argparse
import json
import sqlite3

from banco.dominio import formatar
from banco.servico import Banco


def main():
    parser = argparse.ArgumentParser(description="Banco didático - Lab 7")
    parser.add_argument("--banco", default="conta.sqlite3", help="Arquivo SQLite da conta")
    comandos = parser.add_subparsers(dest="comando", required=True)
    comandos.add_parser("saldo", help="Consultar saldo da conta corrente")
    for nome in ("depositar", "sacar"):
        comando = comandos.add_parser(nome)
        comando.add_argument("valor", help="Valor em reais, por exemplo 100,50")
    args = parser.parse_args()
    try:
        banco = Banco(args.banco)
        saldo = banco.saldo() if args.comando == "saldo" else banco.movimentar(args.comando, args.valor)
        print(json.dumps({"saldo": formatar(saldo)}, ensure_ascii=False))
        return 0
    except ValueError as erro:
        print(json.dumps({"erro": str(erro)}, ensure_ascii=False))
        return 1
    except sqlite3.Error:
        print(json.dumps({"erro": "Não foi possível acessar o banco de dados."}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
