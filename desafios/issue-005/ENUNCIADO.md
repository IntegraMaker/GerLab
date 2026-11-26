# Microdesafio — Issue #5: o castigo da portaria

**Tempo estimado:** ~5 minutos (tentativa inicial de até 10 minutos).

## Contexto
Na Issue #5, o porteiro olha o caderno de tentativas e decide se a pessoa
está **de castigo**: 5 falhas em até 15 minutos bloqueiam por 15 minutos,
contados a partir da **5ª falha** (a mais recente).

Aqui você vai fazer a mesma regra em miniatura, **sem Flask, sem banco e
sem importar nada de `app/`**. Em vez de datas, usamos **números de minutos**
(o nosso "relógio simulado"):

```python
falhas = [0, 1, 2, 3, 4]   # minutos em que a pessoa errou a senha
agora = 18                  # que horas são, em minutos
```

## O que fazer
Abra `castigo.py` e complete a função `esta_de_castigo(falhas, agora)`:

- Se houver **menos de 5** falhas → `False`.
- Pegue as **5 falhas mais recentes** (as 5 últimas da lista; ela já vem em ordem).
- Está de castigo (`True`) se as **duas** coisas forem verdade:
  1. entre a mais antiga e a mais nova dessas 5 passaram **15 minutos ou menos**;
  2. `agora` é **menor** que `mais_nova + 15`.
- Senão → `False`.

Os testes em `test_castigo.py` já estão prontos. **Não altere os testes.**

## Como rodar os testes
```bash
docker compose exec app pytest desafios/issue-005 -v
```
Antes da sua solução, alguns testes falham (é esperado). Depois, todos devem passar.

## Dicas (use só se travar)
1. Tamanho da lista: `len(falhas)`.
2. As 5 últimas: `falhas[-5:]`.
3. A mais antiga dessas 5 é a primeira: `ultimas[0]`; a mais nova é a última: `ultimas[-1]`.
4. Para juntar duas condições: `condicao1 and condicao2`.

## Regras
- Escreva sua solução **exclusivamente** em `desafios/issue-005/`.
- Não importe nem altere nada da pasta `app/`.
- **Salve o arquivo** antes de rodar os testes.
- Ao terminar, avise o agente para fazer o commit `learn(issue-005): concluir desafio prático`.
