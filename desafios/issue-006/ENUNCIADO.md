# Microdesafio — Issue #6: 200, 403 ou 409?

**Tempo estimado:** ~5 minutos (tentativa inicial de até 10 minutos).

## Contexto
Na Issue #6, toda ação passa por duas conferências, **nesta ordem**:
1. **Quem é você?** Se o perfil não está na matriz → **403** (proibido).
2. **Em que estado está o item?** Se a ação não vale para o estado atual → **409** (conflito).
3. Passou nas duas → **200** (deu certo).

Aqui você vai fazer essa decisão em miniatura, **sem Flask, sem banco e sem
importar nada de `app/`**. O arquivo `decisao.py` já traz uma matriz pequena
(`MATRIZ`) e, para cada ação, os estados em que ela vale (`ESTADOS_VALIDOS`).

## O que fazer
Complete a função `decidir(perfil, acao, estado_atual)` em `decisao.py`.
Ela deve devolver o **número** `200`, `403` ou `409`.

Exemplos:
```python
decidir("ADMINISTRADOR", "DESFAZER_FALSO_ALARME", "VERMELHO")  # → 200
decidir("SERVIDOR", "DESFAZER_FALSO_ALARME", "VERMELHO")       # → 403 (perfil)
decidir("ADMINISTRADOR", "DESFAZER_FALSO_ALARME", "VERDE")     # → 409 (estado)
```

Os testes em `test_decisao.py` já estão prontos. **Não altere os testes.**

## Como rodar os testes
```bash
docker compose exec app pytest desafios/issue-006 -v
```
Antes da sua solução, os testes falham (é esperado). Depois, todos devem passar.

## Dicas (use só se travar)
1. Os perfis permitidos de uma ação: `MATRIZ[acao]`.
2. Para saber se algo está num conjunto: `perfil in MATRIZ[acao]` (ou `not in`).
3. Use `if` para cada conferência e `return` assim que souber a resposta.
4. A **ordem** importa: um Servidor que tenta desfazer falso alarme num PC
   Verde deve receber 403, e não 409. Por quê? (Pense: faz sentido contar
   a quem não tem permissão em que estado o item está?)

## Regras
- Escreva sua solução **exclusivamente** em `desafios/issue-006/`.
- Não importe nem altere nada da pasta `app/`.
- **Salve o arquivo** antes de rodar os testes.
- Ao terminar, avise o agente para fazer o commit `learn(issue-006): concluir desafio prático`.
