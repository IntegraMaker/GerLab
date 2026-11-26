# Microdesafio — Issue #7: a volta do carteiro

**Tempo estimado:** ~5 minutos (tentativa inicial de até 10 minutos).

## Contexto
Na Issue #7, o carteiro dá "voltas" na caixa de saída. Em cada volta, ele
tenta entregar **uma vez** cada carta `PENDENTE`:
- deu certo → `ENVIADO`;
- deu errado → `tentativas` + 1; na **3ª** falha → `FALHA` (nunca mais tenta).

Aqui você vai fazer a volta do carteiro em miniatura, **sem Flask, sem banco
e sem importar nada de `app/`**. Cada carta é um dicionário:

```python
{"para": "ana@ifpb.edu.br", "estado": "PENDENTE", "tentativas": 0}
```

O carteiro é uma **função** `entregar(carta)`: se a entrega falhar, ela
**levanta um erro** (como o Gmail fora do ar).

## O que fazer
Complete `dar_uma_volta(cartas, entregar)` em `carteiro.py`. Para cada carta
com `estado` igual a `"PENDENTE"`:
1. some 1 em `carta["tentativas"]`;
2. chame `entregar(carta)`;
3. se não deu erro → `carta["estado"] = "ENVIADO"`;
4. se deu erro e `tentativas` chegou a `MAXIMO_TENTATIVAS` → `carta["estado"] = "FALHA"`
   (com menos tentativas, continua `"PENDENTE"`).

Cartas `ENVIADO` ou `FALHA` são **puladas** (o carteiro nem tenta).

Os testes em `test_carteiro.py` já estão prontos. **Não altere os testes.**

## Como rodar os testes
```bash
docker compose exec app pytest desafios/issue-007 -v
```
Antes da sua solução, alguns testes falham (é esperado). Depois, todos devem passar.

## Dicas (use só se travar)
1. Percorra as cartas com `for carta in cartas:`.
2. Para pular as que não estão pendentes: `if carta["estado"] != "PENDENTE": continue`.
3. Para "tentar e, se der erro, fazer outra coisa":
   ```python
   try:
       ...            # o que pode dar erro
   except Exception:
       ...            # o que fazer se deu erro
   else:
       ...            # o que fazer se NÃO deu erro
   ```
4. Use a constante `MAXIMO_TENTATIVAS` (não escreva o número 3 direto — lembra do desafio da #5?).

## Regras
- Escreva sua solução **exclusivamente** em `desafios/issue-007/`.
- Não importe nem altere nada da pasta `app/`.
- **Salve o arquivo** antes de rodar os testes.
- Ao terminar, avise o agente para fazer o commit `learn(issue-007): concluir desafio prático`.
