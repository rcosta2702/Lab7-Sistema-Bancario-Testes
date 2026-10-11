"""Regras puras; valores internos são centavos inteiros."""

import re
from decimal import Decimal


def centavos(texto: str) -> int:
    """RB-01: valor entre 0,01 e 999.999.999,99, sem arredondamento."""
    if not isinstance(texto, str) or not re.fullmatch(r"[0-9]{1,9}([.,][0-9]{1,2})?", texto):
        raise ValueError("Valor inválido: informe um número positivo com até duas casas decimais.")
    valor = int(Decimal(texto.replace(",", ".")) * 100)
    if valor <= 0:
        raise ValueError("Valor deve ser maior que zero.")
    return valor


def formatar(valor: int) -> str:
    return f"{valor // 100}.{valor % 100:02d}"


def depositar(saldo: int, valor: int) -> int:
    if type(valor) is not int or valor <= 0:
        raise ValueError("Valor deve ser um inteiro positivo em centavos.")
    if saldo + valor > 99_999_999_999:
        raise ValueError("Limite de saldo excedido.")
    return saldo + valor


def sacar(saldo: int, valor: int) -> int:
    if type(valor) is not int or valor <= 0:
        raise ValueError("Valor deve ser um inteiro positivo em centavos.")
    if valor > saldo:
        raise ValueError("Saldo insuficiente.")
    return saldo - valor
