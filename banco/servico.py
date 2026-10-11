"""Integração entre regras de domínio e persistência SQLite."""

import sqlite3
from contextlib import closing

from banco import dominio


class Banco:
    def __init__(self, caminho):
        self.caminho = str(caminho)
        with closing(self._conectar()) as conexao, conexao:
            conexao.execute("CREATE TABLE IF NOT EXISTS conta (id INTEGER PRIMARY KEY CHECK(id=1), saldo INTEGER NOT NULL CHECK(saldo>=0))")
            conexao.execute("INSERT OR IGNORE INTO conta(id, saldo) VALUES(1, 0)")

    def _conectar(self):
        return sqlite3.connect(self.caminho, timeout=5)

    def saldo(self):
        with closing(self._conectar()) as conexao:
            return conexao.execute("SELECT saldo FROM conta WHERE id=1").fetchone()[0]

    def movimentar(self, operacao, texto):
        if operacao not in ("depositar", "sacar"):
            raise ValueError("Operação inválida.")
        valor = dominio.centavos(texto)
        with closing(self._conectar()) as conexao, conexao:
            conexao.execute("BEGIN IMMEDIATE")
            saldo = conexao.execute("SELECT saldo FROM conta WHERE id=1").fetchone()[0]
            regra = dominio.depositar if operacao == "depositar" else dominio.sacar
            novo = regra(saldo, valor)
            conexao.execute("UPDATE conta SET saldo=? WHERE id=1", (novo,))
        return novo
