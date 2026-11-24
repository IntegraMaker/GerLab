# SPEC-04 — Dashboard e planta da sala

- **Status:** Aprovada pelo estudante em 2026-11-24
- **Fontes:** `spec.md` RF17, RF22, RF23, RNF02, RNF05, RNF08, §2.1; `casos-de-uso.md` UC05, UC06; protótipo telas "Dashboard", "Planta da sala" e "Celular"; entrevista P6, P9, P10.2–P10.4
- **Casos de uso:** UC05, UC06

## 1. Objetivo

Mostrar a situação de todas as salas e, em cada sala, a planta em escala com os equipamentos, seus status e detalhes.

## 2. Atores

Estudante, Servidor, Administrador (todos autenticados).

## 3. Requisitos funcionais

- **RF-022 — Dashboard:** um card por sala ativa com nome, bloco, total e contagem de equipamentos por status (cor, ícone e texto). Filtros por bloco e por status. Sem salas → estado vazio; para o Administrador, atalho "Nova sala".
  - [Decisão P10.2] No topo, totais gerais: salas ativas, operacionais, em manutenção e com falha (soma das contagens dos cards).
- **RF-023 — Planta interativa:** desenhada em escala (RNF-002), com zoom e pan por mouse, toque e teclado; popover em cada ícone com nome, categoria, localização/bancada, periféricos, status, última ocorrência visível e **apenas** as ações permitidas ao perfil. Ícones alcançáveis por Tab; Enter abre o popover; setas fazem pan; + e − fazem zoom.
  - [Decisão P10.4] Quando o equipamento está em Falha e tem solicitação PENDENTE, o popover mostra o rótulo informativo "Falha · aguardando triagem" (não é um status novo).
  - [Decisão P9] A planta mostra **somente equipamentos** (sem quadro, mesa ou porta).
  - Ao lado da planta: observações da sala e ocorrências recentes da sala [Fonte: protótipo].
- **RF-017 — Histórico do equipamento:** lista cronológica de mudanças de status, ocorrências, solicitações, chamados, movimentações (inclusive em salas anteriores) e edições; disponível a todos os autenticados para equipamentos ativos.

## 4. Requisitos não funcionais

- **RNF-002 — Proporção:** a planta respeita a razão largura/comprimento com erro ≤ 1%; posições em metros, independentes da tela; adapta-se a telas a partir de 360 px sem distorcer.
- **RNF-005 — Status:** Verde = "Operacional" + ícone de ok; Amarelo = "Em manutenção" + ícone de ferramenta; Vermelho = "Falha" + ícone ×, com forma quadrada na planta [Fonte: protótipo]. Ícones com `aria-label` "‹categoria› ‹nome›, ‹status›".
- **RNF-008 — Celular:** layout responsivo com barra inferior Início, Plantas, Avisos, Conta [Decisão P10.3]; toque no equipamento abre o painel; gesto de pinça para zoom.
- Implementação da planta em SVG com JavaScript próprio, sem biblioteca externa [Decisão P6].

## 5. Fluxos

- UC05: acessar → cards → filtrar → clicar ("Ver planta") → UC06. FA1: nenhuma sala.
- UC06: desenhar planta → ícones com status → zoom/pan → foco/toque → popover → ações. FA1: histórico; FA2: tela pequena; FA3: teclado.

## 6. Critérios de aceitação

- [ ] Sala de 12 × 8 m é desenhada com razão 1,5 (± 1%) em 360 px e em 1920 px de largura.
- [ ] Um equipamento em (6,0 m; 4,0 m) aparece no centro da planta em qualquer tamanho de tela.
- [ ] Nenhum status é indicado só pela cor.
- [ ] Estudante não vê ações de Servidor ou Administrador no popover.
- [ ] Todos os ícones são alcançáveis por Tab e o popover abre com Enter.
- [ ] Salas e equipamentos excluídos não aparecem no dashboard nem na planta.

## 7. Cenários de teste

1. Dashboard com 2 salas (uma com 1 equipamento Vermelho) → contagens e totais corretos; filtro "Falha" mostra só a sala com falha.
2. Dashboard sem salas para Administrador → estado vazio com atalho "Nova sala"; para Estudante, sem atalho.
3. Popover de equipamento Vermelho com solicitação pendente → rótulo "Falha · aguardando triagem".
4. Histórico de equipamento movido de sala → mostra a movimentação com as duas salas.

## 8. Dependências, dúvidas e pendências

- Depende de: SPEC-03. As ações do popover são habilitadas conforme cada SPEC posterior é implementada.
- [Decisão] O item de menu "Plantas das salas" do protótipo leva a uma lista de salas para abrir a planta (equivalente ao dashboard em formato de lista).
