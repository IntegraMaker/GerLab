# Microdesafio — Issue #2: descobrir o perfil pelo e-mail

**Tempo estimado:** ~5 minutos (tentativa inicial de até 10 minutos).

## Contexto
No `criar-admin`, conferimos se o domínio do e-mail é **exatamente** `ifpb.edu.br`,
separando o e-mail no `@`. Agora você vai usar a mesma ideia numa função
**independente**, sem Flask, sem banco e sem importar nada de `app/`.

## O que fazer
Abra `classificador.py` e complete a função `classificar_perfil(email)`:

| E-mail termina em | Deve devolver |
|---|---|
| `@academico.ifpb.edu.br` | `"ESTUDANTE"` |
| `@ifpb.edu.br` | `"SERVIDOR"` |
| qualquer outra coisa | `None` |

Regras extras:
- maiúsculas e minúsculas não importam (`ANA@IFPB.EDU.BR` é Servidor);
- e-mail sem nada antes do `@` (ex.: `@ifpb.edu.br`) devolve `None`;
- domínio "parecido" não vale (ex.: `ana@ifpb.edu.br.com` devolve `None`).

Os testes em `test_classificador.py` já estão prontos. **Não altere os testes.**

## Como rodar os testes
```bash
docker compose exec app pytest desafios/issue-002 -v
```
Antes da sua solução, os testes falham (é esperado). Depois, todos devem passar.

## Dicas (use só se travar)
1. `"texto".lower()` deixa tudo minúsculo.
2. `"ana@ifpb.edu.br".partition("@")` devolve `("ana", "@", "ifpb.edu.br")`.
3. Compare o domínio com `==`, não com `in` nem com `endswith` (por quê?).

## Regras
- Escreva sua solução **exclusivamente** em `desafios/issue-002/`.
- Não importe nem altere nada da pasta `app/`.
- Ao terminar, avise o agente para fazer o commit `learn(issue-002): concluir desafio prático`.
