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
    comandos.add_parser("poupanca", help="Consultar conta corrente, poupança e total")
    for nome in ("depositar", "sacar", "investir"):
        comando = comandos.add_parser(nome)
        comando.add_argument("valor", help="Valor em reais, por exemplo 100,50")
    args = parser.parse_args()
    try:
        banco = Banco(args.banco)
        if args.comando in ("investir", "poupanca"):
            saldo, poupanca = banco.investir(args.valor) if args.comando == "investir" else banco.posicao()
            resposta = {"saldo": formatar(saldo), "poupanca": formatar(poupanca), "total": formatar(saldo + poupanca)}
        else:
            saldo = banco.saldo() if args.comando == "saldo" else banco.movimentar(args.comando, args.valor)
            resposta = {"saldo": formatar(saldo)}
        print(json.dumps(resposta, ensure_ascii=False))
        return 0
    except ValueError as erro:
        print(json.dumps({"erro": str(erro)}, ensure_ascii=False))
        return 1
    except sqlite3.Error:
        print(json.dumps({"erro": "Não foi possível acessar o banco de dados."}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
