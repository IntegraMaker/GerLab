# Microdesafio — Issue #3: uma "lixeira" de computadores

**Tempo estimado:** ~5 minutos (tentativa inicial de até 10 minutos).

## Contexto
Na Issue #3 criamos a **exclusão lógica**: excluir não apaga o registro, só
marca **quando** e **por quem** ele foi excluído. As consultas escondem os
excluídos automaticamente, a não ser que alguém peça `incluir_excluidos=True`.

Aqui você vai fazer a mesma ideia em miniatura, **sem Flask, sem banco e sem
importar nada de `app/`**. Cada computador é só um dicionário:

```python
{"nome": "PC-07", "excluido_em": None, "excluido_por": None}
```

`excluido_em` igual a `None` quer dizer que o computador está **ativo**.

## O que fazer
Abra `lixeira.py` e complete as duas funções:

1. `excluir(pc, autor, quando)`: **não apaga** o computador. Só preenche
   `pc["excluido_em"]` com `quando` e `pc["excluido_por"]` com `autor`.
2. `listar(pcs, incluir_excluidos=False)`: devolve uma **nova lista** com:
   - só os ativos, por padrão;
   - todos (ativos e excluídos), quando `incluir_excluidos=True`.

Os testes em `test_lixeira.py` já estão prontos. **Não altere os testes.**

## Como rodar os testes
```bash
docker compose exec app pytest desafios/issue-003 -v
```
Antes da sua solução, os testes falham (é esperado). Depois, todos devem passar.

## Dicas (use só se travar)
1. Para mudar um valor do dicionário: `pc["chave"] = valor`.
2. Para saber se está ativo: `pc["excluido_em"] is None`.
3. Monte a lista com um `for` e `.append(...)`. Se já conhece, pode usar
   *list comprehension*: `[pc for pc in pcs if ...]`.
4. Por que devolver uma **nova** lista em vez de remover itens de `pcs`?
   (Pense: o que é a exclusão lógica?)

## Regras
- Escreva sua solução **exclusivamente** em `desafios/issue-003/`.
- Não importe nem altere nada da pasta `app/`.
- **Salve o arquivo** antes de rodar os testes.
- Ao terminar, avise o agente para fazer o commit `learn(issue-003): concluir desafio prático`.
