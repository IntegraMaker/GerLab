# SPEC-09 — Gestão de usuários e auditoria

- **Status:** Aprovada pelo estudante em 2026-11-24
- **Issues:** [#34](https://github.com/IntegraMaker/GerLab/issues/34) P-034, [#35](https://github.com/IntegraMaker/GerLab/issues/35) P-035, [#37](https://github.com/IntegraMaker/GerLab/issues/37) P-037 — card no Project [GerLab](https://github.com/users/IntegraMaker/projects/9)
- **Fontes:** `spec.md` RF05, RF16, RN07, RNF06; `casos-de-uso.md` UC18, UC24; protótipo tela "Usuários"; entrevista P3, P10.7
- **Casos de uso:** UC18, UC24

## 1. Objetivo

Permitir ao Administrador gerir contas, perfis e pedidos de acesso administrativo, e consultar o log de auditoria.

## 2. Atores

Administrador.

## 3. Regras de negócio

- **RN-007 — Continuidade administrativa:** sempre existe ao menos um Administrador ativo; um Administrador não desativa nem rebaixa a si mesmo, nem o último Administrador ativo.

## 4. Requisitos funcionais

- **RF-005 — Gestão de usuários:**
  - Listar com nome, e-mail, perfil, situação (Ativa, Desativada, Não confirmada) e data de cadastro; pesquisar por nome ou e-mail; filtrar por perfil e situação; paginação [Fonte: protótipo].
  - Ativar e desativar contas; a desativação encerra as sessões do usuário e recusa automaticamente sua solicitação de Administrador pendente.
  - Rebaixar Administrador a Servidor.
  - Aprovar ou recusar (com justificativa) solicitações de perfil Administrador; o solicitante é avisado por e-mail e no sistema.
  - Desativar ou rebaixar Administrador responsável por chamados não fechados exige escolher antes um novo responsável entre os Administradores ativos.
  - Anonimizar conta desativada a pedido do titular: nome e e-mail substituídos por valores sem identificação; irreversível; a autoria passa a aparecer como "Usuário removido".
  - Toda alteração gera log.
  - [Decisão P10.7] Sem botão "Reenviar link" nesta tela no MVP.
- **RF-016 (consulta) — Log de auditoria:** lista do mais recente para o mais antigo com data e hora, autor, entidade, ação, valor anterior e valor novo; filtros por entidade, autor, ação e período; abrir um registro leva ao item correspondente (ativo; se excluído, indica "item excluído", pois a tela de excluídos está fora do MVP).

## 5. Fluxos

- UC18: painel → listar → pesquisar/filtrar → ativar/desativar. FA1 decidir solicitação; FA2 rebaixar; FA3 anonimizar; FE1 RN-007; FE2 reatribuição de chamados.
- UC24: "Auditoria" → listar → filtrar → abrir. FA1 filtro vazio; FE1 outro perfil → 403.

## 6. Critérios de aceitação

- [ ] O último Administrador ativo não pode ser desativado nem rebaixado; ninguém desativa ou rebaixa a si mesmo.
- [ ] Usuário desativado é redirecionado ao login na próxima requisição.
- [ ] Aprovar solicitação torna o usuário Administrador e enfileira e-mail ao solicitante.
- [ ] Recusar sem justificativa não é permitido.
- [ ] Anonimização só para conta desativada; log continua ligado ao mesmo usuário, exibido como "Usuário removido".
- [ ] O log de auditoria não tem rota de edição nem exclusão; Estudante e Servidor recebem 403.

## 7. Cenários de teste

1. Único Administrador tenta se rebaixar → bloqueado.
2. Desativar Administrador responsável por chamado ASSUMIDO sem indicar substituto → bloqueado com a lista de chamados; com substituto → chamado reatribuído, estado mantido.
3. Desativar usuário com solicitação de Administrador pendente → solicitação RECUSADA automaticamente.
4. Filtrar auditoria por autor e período → apenas os registros correspondentes, em ordem decrescente.

## 8. Dependências, dúvidas e pendências

- Depende de: SPEC-01, SPEC-02, SPEC-07 (reatribuição), SPEC-08.
