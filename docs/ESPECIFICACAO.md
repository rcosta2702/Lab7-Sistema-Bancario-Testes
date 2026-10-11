# Especificação - versão inicial

Aplicativo didático local de uma conta, sem dados reais. Base bancária nova autorizada pelo usuário, pois o Lab 6 anterior era de frete. O PDF chamado Lab 7 possui numeração interna 6.1 a 6.5; as entregas aqui usam 7.1 a 7.5 conforme a disciplina.

- RF-01: consultar saldo, inicialmente zero, sem alterar o estado.
- RF-02: depósito válido aumenta o saldo pelo valor exato.
- RF-03: saque válido reduz o saldo; saque maior que o saldo é recusado sem alteração.
- RB-01: aceitar valor textual positivo, até duas casas decimais, ponto ou vírgula; limite por entrada e saldo de R$ 999.999.999,99. Rejeitar valores inválidos sem arredondar.
- RNF-01: persistir em SQLite local; cada operação é transacional, com rollback em falhas.
- RNF-02: interface por comandos, resposta JSON e código de saída 0 no sucesso ou 1 no erro de negócio/armazenamento. Erros de uso do argparse retornam 2.

O escopo não inclui usuários, autenticação, rede, crédito, taxas ou integração bancária. Não é um sistema para uso financeiro real.
