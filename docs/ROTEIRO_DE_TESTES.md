# Exercício 7.1 - Roteiro de testes

## Preparação e critério de aceite

Python 3.14 e pytest; cada teste de integração/funcional usa banco temporário independente. A etapa inicial deve passar antes da nova funcionalidade. Reexecutar os mesmos arquivos, sem alterar suas expectativas, após adicionar poupança. Aceite: todos os casos passam e operações recusadas preservam os saldos. Os testes amostram o contrato; não provam ausência de todos os defeitos.

| ID | Tipo | Requisito | Pré-condição / dados | Passos | Resultado esperado |
| --- | --- | --- | --- | --- | --- |
| U01 | Unitário | RB-01 | 0.01; 100,50; 100; limite | Converter em centavos | 1; 10050; 10000; 99999999999 |
| U02 | Unitário | RB-01 | Zero, negativo, não finito, texto, fração de centavo, bool, nulo | Converter cada entrada | ValueError |
| U03 | Unitário | RF-02 | Saldo 100,10; depósito 0,20 | Somar e formatar | 100,30 sem perda de precisão |
| U04 | Unitário | RF-03 | Saldo 100; saque 100 | Sacar todo o saldo | Zero |
| U05 | Unitário | RF-03 | Saldo 100; saque 100,01 | Sacar | Saldo insuficiente |
| U06 | Unitário | RB-01 | Operação com 0, -1, bool ou fração de centavo | Depositar/sacar | ValueError |
| U07 | Unitário | RB-01 | Saldo no teto; depósito 0,01 | Depositar | Limite excedido |
| I01 | Integração | RF-01/02/03, RNF-01 | Banco novo | Depositar 100,50; sacar 40,25; reabrir serviço | Saldo persistido 60,25 |
| I02 | Integração | RF-03, RNF-01 | Saldo 50 | Sacar 50,01; consultar; depositar 1 | Falha preserva 50; próxima operação chega a 51 |
| I03 | Integração | RB-01 | Banco novo | Depositar 1.001; operação desconhecida | Ambas recusadas; saldo zero |
| I04 | Integração | RNF-01 | Duas instâncias no mesmo arquivo | Depositar 10 e 20 em sequência | Saldo compartilhado 30 |
| F01 | Funcional | RF-01/02/03 | Aplicativo iniciado em processos reais | Consultar; depositar 100,50; sacar 40,25; consultar | Saídas JSON corretas; saldo final 60,25 |
| F02 | Funcional | RF-03 | Saldo 10 | Comando sacar 11; consultar | Código 1, mensagem de erro e saldo 10 |
| F03 | Funcional | RB-01 | Banco novo | Comando depositar abc; consultar | Código 1 e saldo zero |
| F04 | Funcional | RNF-02 | Diretório do banco inexistente | Comando saldo | Erro de armazenamento sem traceback |

## Separação dos níveis

Unitários chamam somente funções puras. Integração combina serviço, regras e SQLite real. Funcionais chamam app.py em subprocessos, pela mesma interface disponível ao usuário, e verificam saída e persistência sem substituir componentes por mocks.

## Regressão planejada

Preservar todos os casos acima. A extensão de poupança terá casos novos para transferência entre saldos, saldo insuficiente, conservação do total, persistência, rollback e uso pela interface. As regras detalhadas serão acrescentadas à especificação antes da implementação da extensão.

## Casos da extensão 7.5

| ID | Tipo | Requisito | Pré-condição e passos | Resultado esperado |
| --- | --- | --- | --- | --- |
| P01 | Integração | RF-04 | Depositar 100; investir 40,25 | Corrente 59,75; poupança 40,25; total 100 |
| P02 | Integração | RF-04, RNF-01 | Depositar/investir 0,01; reabrir | Corrente zero; poupança 0,01 |
| P03 | Integração | RF-04 | Saldo 10; investir 10,01 | Recusa sem alteração |
| P04 | Integração | RB-01 | Investir 0, -1, 1.001, NaN e abc | Cinco recusas; saldo preservado |
| P05 | Integração | RNF-03 | Criar esquema antigo com 123,45; abrir; investir 23,45; reabrir | Migração preserva valores; saldo 100 e poupança 23,45 |
| P06 | Integração | RNF-04 | Saldo 100; trigger SQLite força falha ao investir 40 | Exceção e rollback: 100 e zero |
| P07 | Integração/regressão | RF-02/03/04 | Depositar 100; investir 40; depositar 10; sacar 20 | Corrente 50; poupança 40 |
| P08 | Funcional | RF-04/05 | Comandos reais: depositar 200; investir 75,50; consultar; tentar investir 125 | Corrente 124,50; poupança 75,50; total 200; erro preserva valores |
| P09 | Integração | RNF-04 | Saldo 100; duas threads tentam investir 80 | Apenas uma aprovada; corrente 20; poupança 80 |
| P10 | Integração | RB-01 | Poupança no teto; corrente 0,01; investir 0,01 | Limite excedido e corrente preservada |
