# Microdesafio — Issue #4: a portaria dos crachás

**Tempo estimado:** ~5 minutos (tentativa inicial de até 10 minutos).

## Contexto
Na Issue #4, o cookie de sessão funciona como um **crachá com versão**:
`"7:1"` quer dizer *usuário 7, versão 1*. O banco guarda a **versão atual**
de cada usuário. Quando a pessoa clica em **Sair**, a versão sobe e todos os
crachás antigos param de valer.

Aqui você vai fazer a mesma ideia em miniatura, **sem Flask, sem banco e sem
importar nada de `app/`**. O "banco" é só um dicionário
`{id_do_usuario: versao_atual}`:

```python
versoes = {7: 1, 8: 3}
```

## O que fazer
Abra `portaria.py` e complete as duas funções:

1. `conferir_cracha(cracha, versoes)`: recebe um texto como `"7:1"`.
   - Se o usuário existe em `versoes` **e** a versão do crachá é igual à
     versão atual → devolve o **id** do usuário (o número `7`).
   - Em qualquer outro caso (versão antiga, usuário inexistente) → devolve `None`.
2. `sair(usuario_id, versoes)`: aumenta em 1 a versão atual desse usuário
   no dicionário (não precisa devolver nada).

Os testes em `test_portaria.py` já estão prontos. **Não altere os testes.**

## Como rodar os testes
```bash
docker compose exec app pytest desafios/issue-004 -v
```
Antes da sua solução, os testes falham (é esperado). Depois, todos devem passar.

## Dicas (use só se travar)
1. Para separar `"7:1"` em duas partes: `"7:1".split(":")` devolve `["7", "1"]`.
2. As partes vêm como **texto**. Para virar número: `int("7")`.
3. Para saber se uma chave existe no dicionário: `usuario_id in versoes`.
4. Para aumentar um valor: `versoes[usuario_id] += 1`.

## Regras
- Escreva sua solução **exclusivamente** em `desafios/issue-004/`.
- Não importe nem altere nada da pasta `app/`.
- **Salve o arquivo** antes de rodar os testes.
- Ao terminar, avise o agente para fazer o commit `learn(issue-004): concluir desafio prático`.
