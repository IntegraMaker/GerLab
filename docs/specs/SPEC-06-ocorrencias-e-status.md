# SPEC-06 — Ocorrências e status do equipamento

- **Status:** Aprovada pelo estudante em 2026-11-24
- **Issues:** [#24](https://github.com/IntegraMaker/GerLab/issues/24) P-024, [#25](https://github.com/IntegraMaker/GerLab/issues/25) P-025, [#26](https://github.com/IntegraMaker/GerLab/issues/26) P-026, [#27](https://github.com/IntegraMaker/GerLab/issues/27) P-027, [#37](https://github.com/IntegraMaker/GerLab/issues/37) P-037 — card no Project [GERLab — Desenvolvimento](https://github.com/users/lucascaetano222/projects/1)
- **Fontes:** `spec.md` §2.1, §2.2, RF14, RF15, RF31, RN03, RN05; `casos-de-uso.md` UC08, UC09, UC21; protótipo telas "Planta", "Celular" e "Fila"
- **Casos de uso:** UC08, UC09, UC21

## 1. Objetivo

Controlar o status físico dos equipamentos por transições validadas e permitir o registro de ocorrências e reportes de falha.

## 2. Atores

Estudante, Servidor, Administrador.

## 3. Status e transições

| Status | Significado |
| :--- | :--- |
| VERDE — Operacional | Funcionando normalmente |
| AMARELO — Em manutenção | Existe chamado não fechado para o equipamento |
| VERMELHO — Falha | Quebrado ou inoperante, sem chamado em andamento |

| ID | De | Para | Quem | Condição | SPEC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T1 | Verde | Vermelho | Qualquer perfil | Reportar falha com descrição | SPEC-06 |
| T2 | Vermelho | Verde | Administrador | Falso alarme com justificativa | SPEC-06 |
| T3 | Vermelho | Amarelo | Administrador | Abrir chamado | SPEC-07 |
| T4 | Verde | Amarelo | Administrador | Abrir chamado preventivo | SPEC-07 |
| T5 | Amarelo | Verde | Administrador | Fechar chamado "consertado" | SPEC-07 |
| T6 | Amarelo | Vermelho | Administrador | Fechar chamado "sem conserto" | SPEC-07 |
| T7 | Amarelo | Status anterior à abertura | Administrador | Cancelar chamado | SPEC-07 |
| T8 | Qualquer | Excluído | Administrador | Exclusão lógica (se Amarelo, cancela o chamado antes e aplica T7) | SPEC-03/07 |

*T9 (restaurar) está fora do MVP.* Qualquer outra mudança → 409. Não mudam o status: registrar ocorrência, mover, editar observações, solicitar chamado, descartar solicitação, assumir, resolver e reabrir chamado. **Quem reportou a falha** é o autor da T1 mais recente.

## 4. Requisitos funcionais

- **RF-014 — Transição por perfil:** o status só muda pelas transições acima; Estudante e Servidor só fazem T1; transição fora da tabela ou sobre estado já alterado → 409; perfil sem permissão → 403; cada transição gera log e notificações (SPEC-08).
- **RF-015 — Ocorrências:** texto obrigatório (até 2.000 caracteres), foto opcional (RN-005) e periférico afetado opcional (um dos vinculados ao equipamento); pode ser registrada em qualquer status e não muda o status; mostra nome do autor e data (e-mail só ao Administrador). O Administrador oculta ocorrência imprópria ou com dado pessoal, com justificativa (exclusão lógica); ocorrências ocultas não contam como "última ocorrência".
- **RF-031 — Desfazer falso alarme:** Administrador devolve equipamento Vermelho a Verde (T2) com justificativa obrigatória no log; solicitação PENDENTE do equipamento continua na fila; quem reportou é notificado.
- **Reportar falha em equipamento Vermelho ou Amarelo** (UC09 FA2): não muda o status e grava como ocorrência; no popover, "Reportar falha" não aparece nesses status [Fonte: protótipo].

## 5. Fluxos

- UC08: popover → "Registrar ocorrência" → texto/periférico/foto → confirmar → grava + log + popover atualizado sem recarregar (HTMX). FE1 texto vazio ou longo; FE2 imagem inválida.
- UC09: popover → "Reportar falha" → descrição → valida permissão e estado → T1 + ocorrência + log → notifica Administradores → ícone Vermelho. FA2 já Vermelho/Amarelo; FE1 conflito → 409.
- UC21: popover ou fila → "Marcar como falso alarme" → justificativa → T2 + log → notifica quem reportou. FE1 justificativa vazia; FE2 não está mais Vermelho → 409.

## 6. Critérios de aceitação

- [ ] Todas as transições do §3 são aceitas apenas nas condições e perfis indicados; as demais retornam 409 ou 403.
- [ ] Concorrência sobre o mesmo equipamento (controle de versão) resulta em 409 para a segunda requisição.
- [ ] Ocorrência não altera o status.
- [ ] Reportar falha cria a ocorrência, aplica T1, grava log e notifica todos os Administradores (exceto quem executou).
- [ ] Ocorrência oculta não aparece para Estudante/Servidor e não é usada como "última ocorrência".

## 7. Cenários de teste

1. Estudante reporta falha em equipamento Verde → Vermelho, 1 ocorrência, 1 log de status, notificações aos Administradores.
2. Estudante reporta falha em equipamento Amarelo → status inalterado, ocorrência criada.
3. Servidor tenta falso alarme → 403.
4. Dois Administradores desfazem o mesmo falso alarme ao mesmo tempo → um 200 e um 409.
5. Ocorrência com 2.001 caracteres → recusada.

## 8. Dependências, dúvidas e pendências

- Depende de: SPEC-01, SPEC-03, SPEC-04, SPEC-08.
