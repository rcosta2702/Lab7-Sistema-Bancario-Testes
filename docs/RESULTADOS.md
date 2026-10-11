# Resultados dos exercícios 7.2 a 7.5

Data de execução: 11/10/2026. Ambiente: Windows, Python 3.14.3, pytest 9.1.1, SQLite da biblioteca padrão. Logs completos com horário UTC, comandos e código de saída, além de XML JUnit, estão em `evidencias/`.

| Entrega | Execução | Resultado observado | Evidência |
| --- | --- | --- | --- |
| 7.2 - Unitários | `python -m pytest -v tests/test_unitarios.py` | 26 aprovados, 0 falhas | antes-unitarios.txt e .xml |
| 7.3 - Integração | `python -m pytest -v tests/test_integracao.py` | 4 aprovados, 0 falhas | antes-integracao.txt e .xml |
| 7.4 - Funcionais | `python -m pytest -v tests/test_funcionais.py` | 4 aprovados, 0 falhas | antes-funcionais.txt e .xml |
| Base anterior | Três arquivos acima | 34 aprovados, 0 falhas | antes-baseline.txt e .xml |
| 7.5 - Regressão após poupança | Mesmos três arquivos, inalterados | 34 aprovados, 0 falhas | depois-regressao.txt e .xml |
| Funcionalidade nova | `python -m pytest -v tests/test_poupanca.py` | 14 aprovados, 0 falhas | depois-poupanca.txt e .xml |
| Versão final completa | `python -m pytest -v tests` | 48 aprovados, 0 falhas | depois-completa.txt e .xml |

## Evidência da regressão

A versão inicial foi registrada no commit `f0991b3`, tag `baseline-sem-poupanca`, antes de implementar o investimento. Os três arquivos de testes originais têm os mesmos hashes SHA-256 em `antes-hashes.json` e `depois-hashes.json`; o script de execução comparou esses hashes e confirmou a igualdade. Logo, os testes de regressão não foram afrouxados para aceitar o código novo.

Antes da implementação, os 14 casos novos falharam porque investir, consultar poupança e o novo comando ainda não existiam; a saída bruta está em `poupanca-red.txt`. O teste funcional dessa etapa produziu erro de leitura JSON porque o argparse ainda recusava o comando investir e não emitia a resposta JSON esperada. Após implementar a extensão, todos passaram.

## Análise

Os testes cobertos não detectaram regressões em consulta, depósito, saque, validação ou persistência. A extensão conserva a soma dos saldos, rejeita saldo insuficiente, migra o esquema anterior e faz rollback em falha de escrita. A concorrência foi exercitada com duas tentativas simultâneas contra o mesmo banco: uma foi aceita e outra recusada, sem saldo negativo.

Os testes funcionais executaram processos reais da interface de comandos; não são apenas chamadas diretas de funções. Os testes de integração utilizaram arquivos SQLite temporários reais. Nenhuma transação bancária real foi realizada.

## Limites da verificação

Execução automatizada local pelo Codex, não pela interface do PyCharm. A base bancária foi criada nesta atividade com autorização do usuário, porque o Lab 6 anterior tratava de frete. O conjunto não inclui avaliação de carga prolongada, falha de energia, autenticação, múltiplas contas ou banco remoto. Não se afirma garantia absoluta de ausência de defeitos; há evidência de aprovação dos cenários listados no roteiro.
