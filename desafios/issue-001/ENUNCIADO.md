# Microdesafio — Issue #1: sua primeira rota Flask com teste

**Tempo estimado:** ~5 minutos (tentativa inicial de até 10 minutos).

## Contexto
Na Issue #1 criamos a rota `/saude`, que responde um JSON, e testes pytest que
verificam essa resposta. Agora é a sua vez de fazer algo parecido, numa
mini-aplicação **independente**. Ela não usa o GERLab nem o banco de dados.

## O que fazer
Abra `mini_app.py`. Já existe uma rota de exemplo, `/ola`. Crie **uma nova rota**:

- endereço: `/ping`
- aceita **somente GET**
- responde o JSON `{"resposta": "pong"}` com status **200**

Os testes em `test_mini_app.py` já estão prontos. **Não altere os testes.**
Seu objetivo é fazer os 3 testes passarem.

## Como rodar os testes
Com os contêineres ligados (`docker compose up -d`):

```bash
docker compose exec app pytest desafios/issue-001 -v
```

Antes da sua solução, 2 testes falham (é esperado). Depois, os 3 devem passar.

## Dicas (use só se travar)
1. Compare com a rota `/saude` em `app/main/routes.py`: o que ela usa para responder JSON?
2. `@app.get(...)` já faz a rota aceitar apenas GET.
3. Lembre de importar o que você usar, no topo do arquivo.

## Regras
- Escreva sua solução **exclusivamente** em `desafios/issue-001/`.
- Não importe nem altere nada da pasta `app/`.
- Ao terminar, avise o agente para fazer o commit `learn(issue-001): concluir desafio prático`.
