# PLAN — GERLab (MVP)

- **Status:** Aprovada pelo estudante em 2026-11-24
- **Base:** `docs/INTENT.md`, `docs/specs/SPEC-01` a `SPEC-09`, `AGENTS.md`
- **Rastreabilidade:** cada item P-NNN é uma Issue real em [IntegraMaker/GerLab](https://github.com/IntegraMaker/GerLab/issues) (coluna "Issue" da §5), adicionada como card vinculado no Project [GERLab — Desenvolvimento](https://github.com/users/lucascaetano222/projects/1) (visões Board e Tabela; colunas Backlog, Ready, In Progress, In Review, Done). A pasta do desafio usa o número da Issue (`desafios/issue-NNN/`).

## 1. Stack (AGENTS.md) e bibliotecas aprovadas

| Camada | Tecnologia | Origem |
| :--- | :--- | :--- |
| Backend | Python + Flask (blueprints, `create_app`) | AGENTS.md |
| Templates | Jinja2, sem SPA | AGENTS.md |
| Estilo | Bootstrap 5 + Bootstrap Icons | AGENTS.md; P6 |
| Interatividade | HTMX; JavaScript próprio apenas na planta (SVG: zoom, pan, arrastar, teclado) | AGENTS.md; P6 |
| Banco | PostgreSQL, SQLAlchemy, Flask-Migrate/Alembic | AGENTS.md |
| Testes | pytest (≥ 3 cenários por Issue), executados contra PostgreSQL | AGENTS.md |
| Ambiente | Docker Compose: `app`, `db` (PostgreSQL) e `mailer` (processo de envio de e-mails, mesma imagem da `app`) | AGENTS.md; P4-B |
| Sessão e login | Flask-Login | P6 |
| Formulários e CSRF | Flask-WTF (`CSRFProtect`; token em `<meta>` enviado pelo HTMX no cabeçalho `X-CSRFToken`) | P6 |
| Hash de senha | `werkzeug.security` | P6 |
| Sanitização HTML | nh3 | P6 |
| Imagens | Pillow | P6 |
| E-mail | `smtplib` (biblioteca padrão) com SMTP do Gmail do projeto | P5, P6 |

**Rejeitado na entrevista:** Redis, RQ, rq-scheduler, Flask-Limiter, Flask-Mail, argon2-cffi (decisões P4-B e P6).

## 2. Decisões técnicas

| Decisão | Justificativa | Status |
| :--- | :--- | :--- |
| Exclusão lógica com `deleted_at`, `deleted_by` e `exclusao_id` (mesmo id em toda a cascata) | RN-002; `exclusao_id` prepara a futura restauração sem custo extra. Não usar `is_active` (conflita com Flask-Login) | Fonte: plan.md |
| Consultas operacionais filtram `deleted_at IS NULL` por padrão | RN-002 | Fonte: plan.md |
| Coluna `versao` (optimistic locking) em Equipamento, Chamado e SolicitacaoChamado → 409 | RN-003 | Fonte: plan.md |
| Módulo único de transições (`app/domain/transicoes.py`) que valida e grava o log na mesma transação | RF-014, RF-016 | Fonte: plan.md |
| `Usuario.sessao_versao` incrementada ao desativar, redefinir ou trocar a senha | RF-004, RF-005, RF-027 | Fonte: plan.md |
| Sair (`POST /sair`, com CSRF) também incrementa `sessao_versao`: a sessão é invalidada no servidor e a pessoa sai de todos os aparelhos | RF-026 | Decisão (aprovada pelo estudante em 2026-11-26, Issue #4) |
| Até o dashboard (P-017), a página inicial `/` é a área logada provisória e exige login | RF-026; teste 3 da P-004 | Decisão (aprovada pelo estudante em 2026-11-26, Issue #4) |
| `TentativaLogin` guarda o e-mail **digitado** (sem FK), o IP (até 45 caracteres) e também os logins certos | RNF-004; P-005 | Decisão (aprovada pelo estudante em 2026-11-26, Issue #5) |
| Bloqueio: as 5 últimas falhas (por e-mail **ou** IP) dentro de 15 min bloqueiam até 15 min após a 5ª falha; login certo não zera a contagem | RNF-004; P-005 | Decisão (aprovada pelo estudante em 2026-11-26, Issue #5) |
| Só FE1 (e-mail ou senha inválidos) conta como falha; tentativas durante o bloqueio não são anotadas e não estendem o castigo; bloqueado não confere a senha | RNF-004; UC03 FE4; P-005 | Decisão (aprovada pelo estudante em 2026-11-26, Issue #5) |
| Matriz em `app/domain/permissoes.py`: uma `Acao` por linha da SPEC-01 §3, escrita linha por linha (não é hierarquia: solicitar chamado e solicitar perfil de Administrador são só do Servidor); regras finas (ex.: só o responsável resolve) ficam nas SPECs de cada tema | SPEC-01 §3; RN-003; P-006 | Decisão (aprovada pelo estudante em 2026-11-26, Issue #6) |
| `@exige(Acao.X)` nas rotas: não autenticado → login com `next`; sem permissão ou conta desativada → 403 sem executar a rota; helper `pode` nos templates só para esconder botões | RN-003; P-006 | Decisão (aprovada pelo estudante em 2026-11-26, Issue #6) |
| 409 via `ConflitoDeEstado` (camada domain) ou `abort(409)`; em HTMX, 403/409 viram fragmento na área `#avisos` (HX-Retarget) e o 409 traz botão "Recarregar" (sem recarga automática); `htmx-config` permite swap de 403/409 | RN-003; P-006 | Decisão (aprovada pelo estudante em 2026-11-26, Issue #6) |
| Tokens com `secrets.token_urlsafe`; banco guarda só SHA-256 | RF-004 | Fonte: plan.md |
| Imagens validadas e regravadas pelo Pillow sem EXIF, com nome aleatório, num volume fora de `static`, servidas por rota autenticada; `MAX_CONTENT_LENGTH` = 5 MB | RN-005, RF-012 | Fonte: plan.md |
| Notificações gravadas na mesma transação da ação | RF-020, RF-021; P4-B | Decisão |
| E-mails em tabela de saída (`EmailPendente`) processada por `flask enviar-emails` no serviço `mailer`, até 3 tentativas | RF-021; P4-B | Decisão |
| Em desenvolvimento e testes, o "envio" escreve o e-mail no log | P5 | Decisão |
| Limite de tentativas de login por tabela `TentativaLogin` (conta e IP, janela de 15 min) | RNF-004; P4-B | Decisão |
| Parâmetros da SPEC-01 §7 em `config.py`, lidos de variáveis de ambiente | SPEC-01 | Fonte: plan.md |
| Primeiro Administrador por `flask criar-admin` | spec.md 1.2 | Fonte: plan.md |
| Categorias iniciais por migração de dados | RF-028 | Fonte: plan.md |
| Posição livre: primeira célula livre numa grade de 0,5 m | RF-010 | Fonte: plan.md |
| Sobreposição = distância < 0,5 m entre centros | RF-009 | Decisão (aprovada em 2026-11-24) |
| Bootstrap, Bootstrap Icons e HTMX copiados para `static/vendor` (sem CDN), versões fixas | Reprodutibilidade e uso na rede do campus | Decisão (aprovada em 2026-11-24) |
| Python 3.12 na imagem Docker | Versão estável suportada pelas bibliotecas | Decisão (aprovada em 2026-11-24) |
| Segredos (SMTP, `SECRET_KEY`, senha do banco) só no `.env`; `.env.example` sem valores reais | AGENTS.md; P5 | Decisão |
| Servidor de produção, domínio e HTTPS | RNF-004 | **Pendente** |

## 3. Estrutura de código (criada na P-001)

```text
GERLab/
├── app/
│   ├── __init__.py        # create_app()
│   ├── extensions.py      # db, migrate, login_manager, csrf
│   ├── models/            # entidades SQLAlchemy
│   ├── domain/            # transições, auditoria, exclusão lógica (regras puras)
│   ├── services/          # casos de uso (orquestram modelos + domain)
│   ├── auth/  labs/  tickets/  admin/  notifications/   # blueprints (rotas)
│   ├── templates/         # Jinja2 (parciais HTMX em _partials/)
│   └── static/            # css, js da planta, vendor/
├── migrations/
├── tests/
├── config.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

## 4. Marcos

| Marco | Entrega demonstrável | Itens | SPECs |
| :--- | :--- | :--- | :--- |
| M0 — Ambiente | `docker compose up` sobe app e banco; testes rodam | P-001 | SPEC-01 |
| M1 — Fundamentos e contas | Cadastro, confirmação, login, recuperação, minha conta | P-002 a P-012 | SPEC-01, 02, 08 |
| M2 — Cadastros | Admin cria categorias, salas e equipamentos | P-013 a P-016 | SPEC-03 |
| M3 — Visualização | Dashboard e planta interativa | P-017 a P-020 | SPEC-04 |
| M4 — Layout | Mover equipamentos e editar observações | P-021 a P-023 | SPEC-05 |
| M5 — Status e ocorrências | Reportar falha, ocorrência, falso alarme | P-024 a P-027 | SPEC-06 |
| M6 — Chamados | Fluxo completo de solicitação e chamado | P-028 a P-033 | SPEC-07 |
| M7 — Administração | Usuários e auditoria | P-034 a P-035 | SPEC-09 |
| M8 — Validação | Acessibilidade, privacidade e validação final | P-036 a P-037 | SPEC-01, 04 |

## 5. Itens de trabalho (futuras Issues)

Cada Issue usará o modelo obrigatório do `AGENTS.md` (atividades, validação pedagógica e conclusão). Abaixo: objetivo, dependências, critérios principais e os três testes mínimos.

| ID | Issue | Título | SPEC | Depende de |
| :--- | :--- | :--- | :--- | :--- |
| P-001 | [#1](https://github.com/IntegraMaker/GerLab/issues/1) | Preparar ambiente e estrutura inicial | 01 | — |
| P-002 | [#2](https://github.com/IntegraMaker/GerLab/issues/2) | Modelo de usuário, hash de senha e `flask criar-admin` | 02 | 001 |
| P-003 | [#3](https://github.com/IntegraMaker/GerLab/issues/3) | Auditoria (LogEvento) e base da exclusão lógica | 01 | 002 |
| P-004 | [#4](https://github.com/IntegraMaker/GerLab/issues/4) | Login, logout e sessão | 02 | 002 |
| P-005 | [#5](https://github.com/IntegraMaker/GerLab/issues/5) | Limite de tentativas de login | 02 | 004 |
| P-006 | [#6](https://github.com/IntegraMaker/GerLab/issues/6) | Autorização por perfil e respostas 403/409 | 01 | 004 |
| P-007 | [#7](https://github.com/IntegraMaker/GerLab/issues/7) | Fila de e-mails e serviço de envio | 08 | 001 |
| P-008 | [#8](https://github.com/IntegraMaker/GerLab/issues/8) | Notificações no sistema | 08 | 006 |
| P-009 | [#9](https://github.com/IntegraMaker/GerLab/issues/9) | Cadastro por domínio e pedido de Administrador no cadastro | 02 | 003, 007 |
| P-010 | [#10](https://github.com/IntegraMaker/GerLab/issues/10) | Confirmação de conta e reenvio do link | 02 | 009, 008 |
| P-011 | [#11](https://github.com/IntegraMaker/GerLab/issues/11) | Recuperação de senha | 02 | 010 |
| P-012 | [#12](https://github.com/IntegraMaker/GerLab/issues/12) | Minha conta: alterar senha e solicitar perfil Administrador | 02 | 010 |
| P-013 | [#13](https://github.com/IntegraMaker/GerLab/issues/13) | Categorias e carga inicial | 03 | 003, 006 |
| P-014 | [#14](https://github.com/IntegraMaker/GerLab/issues/14) | Salas (criar, editar, excluir) | 03 | 013 |
| P-015 | [#15](https://github.com/IntegraMaker/GerLab/issues/15) | Serviço de upload de imagens | 03 | 006 |
| P-016 | [#16](https://github.com/IntegraMaker/GerLab/issues/16) | Equipamentos e periféricos | 03 | 014, 015 |
| P-017 | [#17](https://github.com/IntegraMaker/GerLab/issues/17) | Dashboard de laboratórios | 04 | 016 |
| P-018 | [#18](https://github.com/IntegraMaker/GerLab/issues/18) | Planta em escala e popover | 04 | 016 |
| P-019 | [#19](https://github.com/IntegraMaker/GerLab/issues/19) | Planta interativa: zoom, pan, teclado e toque | 04 | 018 |
| P-020 | [#20](https://github.com/IntegraMaker/GerLab/issues/20) | Histórico do equipamento | 04 | 018 |
| P-021 | [#21](https://github.com/IntegraMaker/GerLab/issues/21) | Mover equipamento na sala | 05 | 019 |
| P-022 | [#22](https://github.com/IntegraMaker/GerLab/issues/22) | Mover entre salas e transferir periférico | 05 | 021 |
| P-023 | [#23](https://github.com/IntegraMaker/GerLab/issues/23) | Observações formatadas | 05 | 018 |
| P-024 | [#24](https://github.com/IntegraMaker/GerLab/issues/24) | Motor de transições de status e concorrência | 06 | 016 |
| P-025 | [#25](https://github.com/IntegraMaker/GerLab/issues/25) | Registrar e ocultar ocorrência | 06 | 018, 015 |
| P-026 | [#26](https://github.com/IntegraMaker/GerLab/issues/26) | Reportar falha | 06 | 024, 025, 008 |
| P-027 | [#27](https://github.com/IntegraMaker/GerLab/issues/27) | Desfazer falso alarme | 06 | 026 |
| P-028 | [#28](https://github.com/IntegraMaker/GerLab/issues/28) | Solicitar chamado | 07 | 026 |
| P-029 | [#29](https://github.com/IntegraMaker/GerLab/issues/29) | Abrir chamado | 07 | 028 |
| P-030 | [#30](https://github.com/IntegraMaker/GerLab/issues/30) | Fila do Administrador e descarte de solicitação | 07 | 029 |
| P-031 | [#31](https://github.com/IntegraMaker/GerLab/issues/31) | Assumir, resolver, cancelar e tela do chamado | 07 | 030 |
| P-032 | [#32](https://github.com/IntegraMaker/GerLab/issues/32) | Fechar e reabrir chamado | 07 | 031 |
| P-033 | [#33](https://github.com/IntegraMaker/GerLab/issues/33) | Exclusão em cascata com solicitações e chamados | 07 | 032 |
| P-034 | [#34](https://github.com/IntegraMaker/GerLab/issues/34) | Gestão de usuários | 09 | 012, 031 |
| P-035 | [#35](https://github.com/IntegraMaker/GerLab/issues/35) | Consulta de auditoria | 09 | 003, 006 |
| P-036 | [#36](https://github.com/IntegraMaker/GerLab/issues/36) | Aviso de privacidade, acessibilidade e responsividade | 01, 04 | 033, 034 |
| P-037 | [#37](https://github.com/IntegraMaker/GerLab/issues/37) | Validação final do MVP | todas | 036, 035 |

### Detalhamento

**P-001 — Preparar ambiente e estrutura inicial** (SPEC-01)
- Objetivo: criar a estrutura da §3, `create_app`, `config.py`, Dockerfile, `docker-compose.yml` (app + db), Flask-Migrate inicializado, layout base Bootstrap 5 + HTMX + Bootstrap Icons, CSRF global, `.env.example`, README com instruções.
- Critérios: `docker compose up` sobe app e banco; `pytest` roda dentro do contêiner contra banco de teste; nenhum segredo versionado.
- Testes: (1) `create_app("testing")` cria a app com configuração de teste; (2) GET `/saude` retorna 200 e confirma conexão com o banco; (3) POST sem token CSRF retorna 400; (4) layout base contém `<meta name="csrf-token">` e carrega HTMX.

**P-002 — Usuário, hash e criar-admin** (SPEC-02)
- Objetivo: modelo `Usuario` e migração; hash com `werkzeug.security`; validador da política de senha; comando `flask criar-admin`.
- Testes: (1) senha gravada nunca é igual ao texto; (2) política recusa "abcdefgh", "12345678" e senha igual ao prefixo; (3) `criar-admin` cria Administrador ativo e confirmado e recusa e-mail fora de `@ifpb.edu.br`.

**P-003 — Auditoria e exclusão lógica** (SPEC-01)
- Objetivo: modelo `LogEvento` imutável; função de registro na mesma transação; mixin de exclusão lógica com filtro padrão.
- Testes: (1) registro de log contém autor, entidade, ação, valores anterior e novo; (2) falha no log desfaz a alteração (rollback); (3) entidade com `deleted_at` não aparece na consulta padrão e aparece na explícita.

**P-004 — Login, logout e sessão** (SPEC-02)
- Objetivo: tela de login (protótipo), Flask-Login, expiração de 2 h, cookie seguro, `sessao_versao`, mensagens UC03 FE1–FE3, logout.
- Testes: (1) credenciais inválidas → mensagem genérica idêntica para e-mail inexistente e senha errada; (2) conta não confirmada com senha correta → orientação de confirmação; (3) após logout, rota protegida redireciona ao login; (4) incrementar `sessao_versao` invalida sessão existente.

**P-005 — Limite de tentativas** (SPEC-02)
- Objetivo: tabela `TentativaLogin`; bloqueio por conta e por IP (5 em 15 min → 15 min).
- Testes: (1) 5 falhas → 6ª tentativa bloqueada mesmo com senha correta; (2) após 15 min (relógio simulado) volta a permitir; (3) falhas em contas diferentes do mesmo IP também bloqueiam.

**P-006 — Autorização por perfil** (SPEC-01)
- Objetivo: decorador/serviço de permissão a partir da matriz SPEC-01 §3; páginas de erro 403 e 409 (também em parciais HTMX).
- Testes: (1) Estudante em rota de Administrador → 403; (2) Administrador → 200; (3) não autenticado → redireciona ao login; (4) resposta 409 em requisição HTMX devolve fragmento de recarga.

**P-007 — Fila de e-mails** (SPEC-08)
- Objetivo: modelo `EmailPendente`; serviço `enfileirar_email`; comando `flask enviar-emails` com até 3 tentativas; serviço `mailer` no Compose; transporte SMTP (produção) e log (dev/teste).
- Testes: (1) enfileirar não chama o SMTP; (2) envio bem-sucedido marca como enviado; (3) três falhas → falha final, sem nova tentativa.

**P-008 — Notificações no sistema** (SPEC-08)
- Objetivo: modelo `Notificacao`; serviço de criação que exclui o autor; contador no cabeçalho (HTMX); lista; marcar uma/todas como lidas; aviso de item excluído.
- Testes: (1) autor da ação não recebe aviso; (2) usuário não acessa aviso de outro; (3) "marcar todas" zera só o contador do usuário.

**P-009 — Cadastro por domínio** (SPEC-02)
- Objetivo: tela de cadastro (protótipo), validação do prefixo, perfil pelo domínio, confirmação de senha, solicitação de Administrador registrada (ainda não na fila), e-mail de confirmação enfileirado, tratamento de e-mail existente.
- Testes: (1) `@academico` → Estudante, `@ifpb` → Servidor, campo `perfil` forjado ignorado; (2) prefixo com `@` → 400; (3) e-mail existente confirmado → mesma resposta, sem nova conta, e-mail de aviso enfileirado; (4) Estudante marcando "Solicitar Administrador" → solicitação não criada.

**P-010 — Confirmação de conta** (SPEC-02)
- Objetivo: modelo `Token`, rota de confirmação, reenvio limitado a 1/min, ativação da solicitação de Administrador após confirmar (com notificação).
- Testes: (1) token válido confirma e é invalidado; (2) token de 25 h → expirado com oferta de reenvio; (3) segundo reenvio em menos de 1 min → recusado; (4) confirmação com solicitação de Administrador → PENDENTE e Administradores notificados.

**P-011 — Recuperação de senha** (SPEC-02)
- Testes: (1) e-mail inexistente → mesma mensagem e nenhum e-mail enfileirado; (2) token de 1 h expirado → recusado; (3) redefinição encerra sessões antigas e invalida o token.

**P-012 — Minha conta** (SPEC-02)
- Testes: (1) senha atual errada → nada muda; (2) troca válida mantém a sessão atual e invalida as outras; (3) Servidor solicita Administrador → PENDENTE e Administradores notificados; segunda solicitação → 409; Estudante → 403.

**P-013 — Categorias** (SPEC-03)
- Testes: (1) nome duplicado entre ativas → recusado; (2) categoria em uso não é excluída e lista os itens; (3) migração cria as 8 categorias iniciais com tipo correto.

**P-014 — Salas** (SPEC-03)
- Testes: (1) dimensões 0, −1, "abc" e 100,01 recusadas; (2) nome repetido no mesmo bloco recusado, em outro bloco aceito; (3) exclusão exige confirmação e grava log; desistir não altera nada.

**P-015 — Upload de imagens** (SPEC-03)
- Testes: (1) PNG válido gravado sem EXIF e com nome aleatório; (2) arquivo de texto renomeado `.png` → 400; (3) 6 MB → 413; (4) rota de imagem sem login → redireciona ao login.

**P-016 — Equipamentos e periféricos** (SPEC-03)
- Objetivo: CRUD de equipamento (com localização/bancada) e periféricos; nasce Verde; limite de 200; exclusão lógica com cascata de periféricos e de sala → equipamentos.
- Testes: (1) equipamento com categoria do tipo periférico → recusado; (2) 201º equipamento na sala → recusado; (3) excluir sala exclui equipamentos e periféricos com o mesmo `exclusao_id`.

**P-017 — Dashboard** (SPEC-04)
- Testes: (1) contagens por status e totais corretos; (2) filtros por bloco e por status; (3) estado vazio com atalho só para Administrador.

**P-018 — Planta em escala e popover** (SPEC-04)
- Objetivo: SVG com `viewBox` em metros, ícones por categoria e status, popover via HTMX com ações por perfil, observações e ocorrências recentes ao lado.
- Testes: (1) `viewBox` reflete largura × comprimento da sala; (2) cada ícone tem `aria-label` com nome e status; (3) popover para Estudante não contém ações de Servidor/Administrador; (4) rótulo "Falha · aguardando triagem" quando aplicável.

**P-019 — Planta interativa** (SPEC-04)
- Objetivo: JS próprio para zoom (botões, roda, pinça, + e −), pan (arrastar, setas), "ajustar à tela", Tab/Enter.
- Testes (pytest + verificação de marcação; roteiro manual registrado): (1) template inclui controles com nome acessível; (2) ícones têm `tabindex` e ordem coerente; (3) roteiro manual em 360 px e desktop confirma proporção e navegação por teclado.

**P-020 — Histórico do equipamento** (SPEC-04)
- Testes: (1) eventos em ordem cronológica; (2) inclui movimentação entre salas; (3) equipamento excluído → 404 para não Administrador.

**P-021 — Mover na sala** (SPEC-05)
- Testes: (1) posição válida gravada em metros com log; (2) fora da sala ou sobreposta → recusada, posição mantida; (3) Estudante → 403; (4) formulário de coordenadas funciona sem JS.

**P-022 — Mover entre salas e transferir periférico** (SPEC-05)
- Testes: (1) equipamento leva periféricos e mantém chamado/histórico; (2) posição livre proposta não sobrepõe; (3) sala no limite ou excluída não é destino; (4) periférico transferido muda de sala.

**P-023 — Observações formatadas** (SPEC-05)
- Testes: (1) `<script>` e `javascript:` removidos; (2) > 5.000 caracteres recusado; (3) log guarda a versão anterior.

**P-024 — Motor de transições** (SPEC-06)
- Objetivo: tabela T1–T8, validação de perfil e estado, `versao` para concorrência, log na mesma transação.
- Testes: (1) cada transição válida aceita pelo perfil correto; (2) transição inexistente (ex.: Verde → Verde por falso alarme) → 409; (3) versão desatualizada → 409; (4) Estudante tentando T2 → 403.

**P-025 — Ocorrências** (SPEC-06)
- Testes: (1) ocorrência não muda status; (2) periférico de outro equipamento → recusado; (3) ocorrência oculta some para Estudante e não é "última ocorrência".

**P-026 — Reportar falha** (SPEC-06)
- Testes: (1) Verde → Vermelho, ocorrência, log e notificações; (2) em Amarelo → só ocorrência; (3) concorrência → 409.

**P-027 — Falso alarme** (SPEC-06)
- Testes: (1) Vermelho → Verde com justificativa e aviso a quem reportou; (2) justificativa vazia recusada; (3) solicitação PENDENTE continua na fila.

**P-028 — Solicitar chamado** (SPEC-07)
- Testes: (1) Servidor cria PENDENTE e Administradores notificados; (2) já existe pendente ou chamado → mostra existente; (3) Estudante e Administrador → 403.

**P-029 — Abrir chamado** (SPEC-07)
- Testes: (1) Vermelho → Amarelo e status anterior guardado; (2) solicitação PENDENTE vira CONVERTIDA; (3) segundo chamado não fechado → recusado; (4) chamado de sala não muda equipamentos.

**P-030 — Fila do Administrador** (SPEC-07)
- Testes: (1) três grupos com itens corretos e sem excluídos; (2) filtros e ordenação; (3) descartar exige justificativa e notifica o solicitante.

**P-031 — Assumir, resolver, cancelar e tela do chamado** (SPEC-07)
- Testes: (1) outro Administrador assume e vira responsável; (2) não responsável resolvendo → 403; nota vazia recusada; (3) cancelar devolve status anterior (T7).

**P-032 — Fechar e reabrir** (SPEC-07)
- Testes: (1) "consertado" → Verde; "sem conserto" → Vermelho; (2) parecer com 9 caracteres recusado; (3) reabrir mantém responsável e Amarelo.

**P-033 — Exclusão em cascata com chamados** (SPEC-07)
- Testes: (1) excluir equipamento Amarelo cancela chamado e guarda status anterior; (2) excluir sala descarta solicitações e cancela chamados dos itens; (3) tela de confirmação lista solicitações e chamados afetados.

**P-034 — Gestão de usuários** (SPEC-09)
- Testes: (1) RN-007 (si mesmo e último Administrador); (2) reatribuição obrigatória de chamados; (3) desativação encerra sessão e recusa solicitação pendente; (4) anonimização só de conta desativada.

**P-035 — Consulta de auditoria** (SPEC-09)
- Testes: (1) ordem decrescente; (2) filtros por entidade, autor, ação e período; (3) Servidor → 403.

**P-036 — Privacidade, acessibilidade e responsividade** (SPEC-01, SPEC-04)
- Objetivo: página de aviso de privacidade (cadastro, login, rodapé); revisão WCAG 2.1 AA (contraste, nomes acessíveis, foco); layout em 360 px com barra inferior.
- Testes: (1) aviso acessível por link no cadastro, login e rodapé; (2) todos os indicadores de status têm texto; (3) roteiro manual de teclado e 360 px registrado.

**P-037 — Validação final do MVP** (todas)
- Objetivo: teste de ponta a ponta das jornadas do INTENT §6, revisão do README, conferência dos critérios de aceite das SPECs.
- Testes: (1) jornada Estudante reporta falha → Administrador fecha chamado; (2) jornada de cadastro e confirmação até o dashboard; (3) instalação limpa com `docker compose up` seguindo apenas o README.

## 6. Itens bloqueados ou dependentes de decisão

| Item | Bloqueio |
| :--- | :--- |
| Envio real de e-mail (P-007 em produção) | Senha de app do Gmail configurada pelo estudante no `.env` |
| HTTPS e implantação | Servidor e domínio de produção não definidos |
| IP real no bloqueio de login (P-005) em produção | Atrás de proxy reverso, `request.remote_addr` é o IP do proxy: configurar `ProxyFix` na implantação. Risco registrado: computadores de um laboratório atrás do mesmo IP (NAT) podem ser bloqueados juntos; mudar a regra da SPEC exige a skill de alteração |

## 7. Fora do MVP (backlog futuro, sem Issue agora)

UC19 edição em lote; UC22 itens excluídos e restauração (T9); anonimização automática; RNF09 backup; testes de carga RNF07; elementos fixos da planta; busca global; "Minhas solicitações"; "Reenviar link" pelo Administrador.
