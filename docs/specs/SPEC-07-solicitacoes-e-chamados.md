# SPEC-07 — Solicitações e chamados técnicos

- **Status:** Aprovada pelo estudante em 2026-11-24
- **Fontes:** `spec.md` §2.3, §2.4, RF18, RF19, RF25, RF32, RN02, RN06; `casos-de-uso.md` UC12, UC15, UC16, UC17, UC13 FA2, UC14 FA3; protótipo telas "Fila de chamados" e "Chamado"
- **Casos de uso:** UC12, UC15, UC16, UC17

## 1. Objetivo

Permitir que Servidores solicitem intervenção e que Administradores triem, abram, conduzam, validem e fechem chamados, com rastreabilidade completa.

## 2. Atores

Servidor (solicita), Administrador (tria e conduz).

## 3. Ciclos de vida

**Solicitação de chamado:**

| De | Para | Quem | Condição |
| :--- | :--- | :--- | :--- |
| — | PENDENTE | Servidor | Item ativo sem solicitação pendente nem chamado não fechado (RN-006) |
| PENDENTE | CONVERTIDA | Administrador | Abrir chamado para o item, a partir da solicitação ou direto |
| PENDENTE | DESCARTADA | Administrador | Justificativa obrigatória |
| PENDENTE | DESCARTADA | Sistema | Equipamento ou sala excluído |

**Chamado:**

| De | Para | Quem | Condição |
| :--- | :--- | :--- | :--- |
| — | ABERTO | Administrador | RN-006; descrição técnica, prioridade e responsável obrigatórios |
| ABERTO ou REABERTO | ASSUMIDO | Administrador | Quem assume passa a ser o responsável |
| ASSUMIDO | RESOLVIDO | Administrador responsável | Nota técnica obrigatória |
| RESOLVIDO | FECHADO | Administrador | Parecer (≥ 10 caracteres) e resultado ("consertado" ou "sem conserto") |
| RESOLVIDO | REABERTO | Administrador | Motivo obrigatório; mantém o responsável |
| ABERTO, ASSUMIDO ou REABERTO | CANCELADO | Administrador | Justificativa obrigatória |
| ABERTO, ASSUMIDO, RESOLVIDO ou REABERTO | CANCELADO | Sistema | Item excluído |

FECHADO e CANCELADO são finais. Chamado de **sala** (problema estrutural) não muda status de equipamento.

## 4. Regras de negócio

- **RN-006 — Um tratamento por item:** cada equipamento (ou sala) tem no máximo uma solicitação PENDENTE e um chamado não fechado; nova tentativa mostra o existente e oferece registrar ocorrência.
- **RN-002 (complemento):** ao excluir equipamento ou sala, solicitações pendentes são descartadas e chamados não fechados cancelados com justificativa "item excluído"; equipamento Amarelo volta ao status anterior ao chamado antes da exclusão (T8).

## 5. Requisitos funcionais

- **RF-025 — Solicitar chamado (Servidor):** para equipamento ou sala; descrição obrigatória e foto opcional; nasce PENDENTE; não muda status; o Servidor acompanha pelas notificações e pela página do item.
- **RF-032 — Ciclo do chamado:** abrir (descrição técnica, prioridade Baixa/Média/Alta, responsável entre Administradores ativos); solicitação PENDENTE do item passa a CONVERTIDA; equipamento vai a Amarelo (T3/T4) guardando o status anterior; assumir (por qualquer Administrador, que vira responsável); resolver (só o responsável, nota obrigatória); reabrir (motivo); cancelar (justificativa, T7). Cada mudança gera log e notificações.
- **RF-019 — Encerramento formal:** só chamado RESOLVIDO fecha; "consertado" → T5; "sem conserto" → T6; chamado de sala fecha sem mudar status.
- **RF-018 — Fila do Administrador:** tela única com três grupos — solicitações PENDENTES, equipamentos em Vermelho (sem chamado) e chamados não fechados; cada linha com sala, item, estado, prioridade, responsável e idade; filtros por sala, grupo, estado e prioridade; ordenação por idade e prioridade; itens excluídos não aparecem.
- **Tela do chamado** [Fonte: protótipo]: número, item, estado, prioridade, etapas (Aberto → Assumido → Resolvido → Fechado), descrição técnica, responsável, reportado por, origem (reporte de falha ou solicitação), linha do tempo e formulário da próxima ação; atalhos para a planta e para o histórico do equipamento.

## 6. Fluxos

- UC12: popover ou página da sala → "Solicitar chamado" → descrição/foto → RN-006 → PENDENTE → notifica Administradores. FA1 problema estrutural; FE1 já existe; FE2 Estudante → 403.
- UC15: popover ou fila → "Abrir chamado" → dados → ABERTO → Amarelo → notifica. FA1 preventivo; FA2 sala; FE1 já existe; FE2 concorrência → 409.
- UC16: fila → filtrar → assumir → resolver. FA1 descartar solicitação; FA2 equipamento em Vermelho (abrir ou falso alarme); FA3 cancelar; FE1 assumido por outro → 409; FE2 nota vazia; FE3 não responsável → 403.
- UC17: chamado RESOLVIDO → fechar com parecer e resultado. FA1 sem conserto; FA2 reabrir; FA3 chamado de sala; FE1 parecer curto.

## 7. Critérios de aceitação

- [ ] Não é possível ter duas solicitações pendentes ou dois chamados não fechados para o mesmo item.
- [ ] Abrir chamado converte a solicitação pendente, mesmo aberto pelo popover.
- [ ] Apenas o responsável resolve; qualquer Administrador assume.
- [ ] Cancelar devolve o equipamento ao status anterior à abertura.
- [ ] Fechar só a partir de RESOLVIDO, com parecer ≥ 10 caracteres.
- [ ] Excluir equipamento com chamado ASSUMIDO cancela o chamado, aplica T7 e só então exclui.
- [ ] A fila não mostra itens excluídos.

## 8. Cenários de teste

1. Servidor solicita chamado para PC-07 já com solicitação pendente → mostra a existente, nenhuma nova.
2. Administrador abre chamado para equipamento Vermelho com solicitação pendente → chamado ABERTO, solicitação CONVERTIDA, equipamento Amarelo com status anterior Vermelho.
3. Administrador não responsável tenta resolver → 403.
4. Fechar com resultado "sem conserto" → equipamento Vermelho.
5. Cancelar chamado preventivo → equipamento volta a Verde.
6. Excluir sala com chamado aberto → chamado CANCELADO "item excluído".

## 9. Dependências, dúvidas e pendências

- Depende de: SPEC-03, SPEC-06, SPEC-08.
