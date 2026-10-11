# Lab 7 - Sistema bancário, testes e qualidade

## Entregas

| Exercício | Arquivos |
| --- | --- |
| 7.1 - Roteiro | [docs/ROTEIRO_DE_TESTES.md](docs/ROTEIRO_DE_TESTES.md) |
| 7.2 - Unitário | tests/test_unitarios.py; evidencias/antes-unitarios.txt |
| 7.3 - Integração | tests/test_integracao.py; evidencias/antes-integracao.txt |
| 7.4 - Funcional | tests/test_funcionais.py; evidencias/antes-funcionais.txt |
| 7.5 - Regressão e poupança | banco/servico.py; tests/test_poupanca.py; evidencias/depois-regressao.txt; evidencias/depois-completa.txt |

## Preparar e executar

Requer Python 3.14+. Na pasta deste projeto:

```console
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements-dev.txt
.venv\Scripts\python -m pytest -v
```

No PyCharm, abra esta pasta como projeto separado e selecione `.venv/Scripts/python.exe`. Para testar, execute a pasta `tests` com pytest. O projeto não depende dos arquivos do Lab 6.

## Usar o banco

```console
python app.py saldo
python app.py depositar 200
python app.py sacar 25,50
python app.py investir 75
python app.py poupanca
```

A sequência em banco novo termina com corrente 99,50, poupança 75,00 e total 174,50. Os valores são simulados e persistem em `conta.sqlite3`, excluído do Git. Para outro arquivo: `python app.py --banco exemplo.sqlite3 saldo`.

Depósito e saque retornam o saldo corrente em JSON. Investir transfere o valor da corrente para a poupança, sem rendimento automático. As premissas e limites estão em [docs/ESPECIFICACAO.md](docs/ESPECIFICACAO.md).

## Arquitetura

`app.py` recebe comandos; `banco/servico.py` coordena transações e SQLite; `banco/dominio.py` contém regras puras com valores em centavos inteiros. A execução do aplicativo usa apenas a biblioteca padrão. Pytest é dependência exclusiva de testes.

Os resultados registrados foram obtidos diretamente no ambiente local. Não se declara execução visual na IDE nem entrega automática na plataforma acadêmica.
