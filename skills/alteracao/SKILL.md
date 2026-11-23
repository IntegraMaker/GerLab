# Skill — Gestão de alterações do GERLab

## Quando usar
Quando o estudante, professor ou interessado solicitar mudanças após a aprovação de INTENT, SPECs ou PLAN: novas funcionalidades, ajustes de telas, regras, campos, permissões, fluxos ou tecnologias.

## Procedimento
1. **Registrar o pedido:** capture a solicitação original e identifique o solicitante. Se ambígua, pergunte antes de interpretá-la.
2. **Comparar com o aprovado:** leia as SPECs, o INTENT, o `AGENTS.md`, o PLAN e as Issues afetadas. Diferencie correção de defeito de alteração de requisito.
3. **Analisar impactos:** requisitos, telas, dados, migrações, permissões, segurança, testes, dependências, prazo e Issues.
4. **Propor decisão:** apresente o comportamento atual, a mudança proposta, opções relevantes, riscos e recomendação técnica. Não execute mudanças de escopo sem aprovação explícita do responsável definido para o projeto.
5. **Registrar:** após aprovação, crie `ALT-NNN` em `docs/REGISTRO_DE_ALTERACOES.md`, com data, solicitante, justificativa, aprovador, decisão, SPECs/Issues afetadas e plano de validação. Se um dado não estiver disponível, marque `Pendente`.
6. **Atualizar documentação:** altere SPECs, INTENT e PLAN conforme necessário, preservando rastreabilidade e histórico.
7. **Sincronizar GitHub:** atualize ou crie Issues, dependências e cards no Project. Evite duplicações e confirme operações remotas.
8. **Implementar:** somente após aprovação e atualização da documentação; siga as regras de testes, aprendizagem e commits do `AGENTS.md`.

## Modelo de registro
```markdown
## ALT-NNN — Título
- Data:
- Solicitante:
- Aprovador:
- Status: Proposta | Aprovada | Rejeitada | Implementada

### Solicitação original
...
### Justificativa
...
### Comportamento anterior
...
### Decisão aprovada
...
### Impactos
- SPECs:
- Decisões técnicas/stack:
- Dados e permissões:
- Issues e cards:
- Testes:
### Validação
...
```

## Regras
- Não tratar sugestão do agente como requisito aprovado.
- Não alterar silenciosamente SPECs aprovadas.
- Não remover funcionalidades sem autorização.
- Não alterar a stack sem aprovação explícita e atualização do `AGENTS.md`, do PLAN e do registro de alterações.
- Não publicar segredos ou dados reais.
- Não afirmar que uma Issue/card foi atualizada sem confirmação do GitHub.
