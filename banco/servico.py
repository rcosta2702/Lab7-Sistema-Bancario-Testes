"""Integração entre regras de domínio e persistência SQLite."""

import sqlite3
from contextlib import closing

from banco import dominio


class Banco:
    def __init__(self, caminho):
        self.caminho = str(caminho)
        with closing(self._conectar()) as conexao, conexao:
            conexao.execute("BEGIN IMMEDIATE")
            conexao.execute("CREATE TABLE IF NOT EXISTS conta (id INTEGER PRIMARY KEY CHECK(id=1), saldo INTEGER NOT NULL CHECK(saldo>=0))")
            conexao.execute("INSERT OR IGNORE INTO conta(id, saldo) VALUES(1, 0)")
            colunas = {linha[1] for linha in conexao.execute("PRAGMA table_info(conta)")}
            if "poupanca" not in colunas:
                conexao.execute("ALTER TABLE conta ADD COLUMN poupanca INTEGER NOT NULL DEFAULT 0 CHECK(poupanca>=0)")

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

    def posicao(self):
        """RF-05: leitura dos dois saldos na mesma consulta."""
        with closing(self._conectar()) as conexao:
            return conexao.execute("SELECT saldo, poupanca FROM conta WHERE id=1").fetchone()

    def investir(self, texto):
        """RF-04/RNF-04: débito e crédito atômicos, sem criação de dinheiro."""
        valor = dominio.centavos(texto)
        with closing(self._conectar()) as conexao, conexao:
            conexao.execute("BEGIN IMMEDIATE")
            saldo, poupanca = conexao.execute("SELECT saldo, poupanca FROM conta WHERE id=1").fetchone()
            novo_saldo = dominio.sacar(saldo, valor)
            nova_poupanca = dominio.depositar(poupanca, valor)
            conexao.execute("UPDATE conta SET saldo=?, poupanca=? WHERE id=1", (novo_saldo, nova_poupanca))
        return novo_saldo, nova_poupanca
