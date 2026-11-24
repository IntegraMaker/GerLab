# INTENT — GERLab

- **Status:** Aprovada pelo estudante em 2026-11-24
- **Instituição:** IFPB – Campus Sousa
- **Última atualização:** 2026-11-24

> Legenda de rastreabilidade: **[Fonte]** fato encontrado nas fontes; **[Decisão]** decisão confirmada pelo estudante na entrevista; **[Hipótese]** interpretação ainda não confirmada; **[Recomendação]** sugestão do agente.

## 1. Contexto e problema

[Fonte: intent.md] Hoje não existe uma visão única de **onde está cada equipamento** nos laboratórios nem de **quais estão com defeito**. As falhas são percebidas por quem usa a sala, mas o aviso chega à equipe responsável de forma informal (conversa, mensagem, papel), sem registro, sem histórico e sem acompanhamento até o conserto.

[Decisão] O sistema chama-se **GERLab** (o nome "LabSpace", usado no protótipo e nos documentos de origem, é o nome anterior) e atende o **IFPB – Campus Sousa**.

## 2. Público-alvo e papéis

[Fonte: spec.md 1.1; intent.md]

| Papel | Como obtém o perfil | Necessidade principal |
| :--- | :--- | :--- |
| Estudante | Cadastro com e-mail `@academico.ifpb.edu.br` | Saber se a sala e a máquina estão funcionando; avisar quando algo quebra |
| Servidor | Cadastro com e-mail `@ifpb.edu.br` | Organizar a sala (posição, observações) e pedir intervenção técnica |
| Administrador | Servidor com solicitação aprovada; o primeiro é criado na implantação | Triar problemas numa fila, conduzir chamados até o fechamento e gerir salas, equipamentos e usuários |

[Decisão] Os domínios de e-mail permanecem `@ifpb.edu.br` e `@academico.ifpb.edu.br`.

## 3. Objetivo e resultados esperados

[Fonte: intent.md] Oferecer uma **planta baixa interativa** de cada laboratório, em escala real, em que cada equipamento aparece com seu status (Operacional, Em manutenção, Falha — sempre com cor, ícone e texto), e um **fluxo de chamados** rastreável do reporte ao fechamento.

## 4. Escopo do MVP

[Decisão] O foco são os **laboratórios de informática**. A sala não tem campo de "tipo de laboratório"; nada impede cadastrar outras salas, mas isso não orienta requisitos do MVP.

[Decisão] Casos de uso incluídos no MVP (numeração de `casos-de-uso.md`):

| Tema | Casos de uso | SPEC |
| :--- | :--- | :--- |
| Contas e autenticação | UC01, UC02, UC03, UC04, UC20 | SPEC-02 |
| Salas, categorias e equipamentos | UC13, UC14, UC23 | SPEC-03 |
| Dashboard e planta | UC05, UC06 | SPEC-04 |
| Layout e observações | UC10, UC11 | SPEC-05 |
| Ocorrências e status | UC08, UC09, UC21 | SPEC-06 |
| Solicitações e chamados | UC12, UC15, UC16, UC17 | SPEC-07 |
| Notificações e e-mails | UC07 | SPEC-08 |
| Usuários e auditoria | UC18, UC24 | SPEC-09 |
| Regras transversais (perfis, auditoria, exclusão lógica, autorização, RNF) | — | SPEC-01 |

## 5. Exclusões

**Fora do MVP, possíveis evoluções futuras** [Decisão]:
- UC19 — Edição de equipamentos em lote (RF24).
- UC22 — Consulta e restauração de itens excluídos (RF29, RF30, transição T9). A **exclusão lógica continua no MVP**.
- Anonimização automática após 2 anos de conta desativada (RNF06). A anonimização manual a pedido do titular (UC18 FA3) permanece.
- Backup e disponibilidade (RNF09).
- Testes de carga do RNF07 (os limites funcionais, como 200 equipamentos por sala, permanecem).
- Elementos fixos da planta (quadro, mesa do professor, porta) mostrados no protótipo.
- Busca global "Buscar sala ou equipamento", tela "Minhas solicitações" e botão "Reenviar link" na gestão de usuários, mostrados no protótipo.

**Fora do escopo do sistema** [Fonte: intent.md, RNF01; Decisão]:
- Agenda e reserva de laboratórios.
- Inventário de software instalado.
- Controle patrimonial ou contábil (tombamento, valor, depreciação).
- Avisos de chamado por e-mail, SMS ou aplicativos de mensagem (avisos só dentro do sistema; e-mail só para assuntos da conta).

## 6. Principais jornadas

1. **Estudante reporta falha:** entra → dashboard → planta da sala → toca no equipamento → "Reportar falha" → equipamento fica em Falha e os Administradores são avisados.
2. **Servidor organiza a sala:** abre a planta → "Editar layout" → move equipamentos → edita observações → solicita chamado para um problema.
3. **Administrador trata o problema:** abre a fila → abre chamado (equipamento em manutenção) → assume → resolve com nota técnica → valida no laboratório e fecha com parecer (equipamento volta a Operacional ou Falha).
4. **Administrador gere o cadastro:** cria categorias, salas e equipamentos; aprova pedidos de perfil Administrador; consulta a auditoria.

## 7. Critérios de sucesso

[Fonte: intent.md]
- Qualquer usuário reporta uma falha em poucos cliques, direto no ícone do equipamento.
- O Administrador vê todas as pendências numa única fila, sem depender de avisos informais.
- Todo equipamento tem histórico completo (status, ocorrências, chamados, mudanças de sala), preservado após exclusão lógica.
- O status de cada sala é consultado no dashboard sem ir ao laboratório.
- O sistema é utilizável por pessoas com daltonismo ou que navegam só pelo teclado.

## 8. Restrições, premissas e pendências

- **Stack obrigatória** [AGENTS.md]: Python + Flask, Jinja2, Bootstrap 5, HTMX (JS próprio só na planta), PostgreSQL com SQLAlchemy e Flask-Migrate, pytest, Docker Compose.
- **Sem Redis/RQ** [Decisão P4-B]: processamento em segundo plano usa apenas o PostgreSQL (ver PLAN).
- **E-mail** [Decisão P5]: conta Gmail do projeto informada pelo estudante, via SMTP com senha de app. Endereço e senha ficam somente no `.env` (fora do repositório).
- **Pendências:**
  - Local de implantação em produção (servidor, domínio e HTTPS).
  - Senha de app do Gmail (o estudante configura localmente).

## 9. Fontes consultadas

| Fonte | Caminho |
| :--- | :--- |
| Especificação de origem | `Documents/ifpb_labspace/docs/spec.md` |
| Casos de uso | `Documents/ifpb_labspace/docs/casos-de-uso.md` |
| Intent de origem | `Documents/ifpb_labspace/docs/intent.md` |
| Plan de origem | `Documents/ifpb_labspace/docs/plan.md` |
| Protótipo de telas | `Documents/Protótipo de telas – LabSpace IFPB.html` (8 telas estáticas) |
| Entrevista | Respostas do estudante às perguntas P1–P10 (2026-11-24) |
