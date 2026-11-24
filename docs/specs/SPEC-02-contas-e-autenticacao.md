# SPEC-02 — Contas e autenticação

- **Status:** Aprovada pelo estudante em 2026-11-24
- **Fontes:** `spec.md` §1.2, §2.5, RF01–RF04, RF26, RF27, RNF04; `casos-de-uso.md` UC01–UC04, UC20; protótipo telas "Login" e "Cadastro"; entrevista P1, P10.1
- **Casos de uso:** UC01, UC02, UC03, UC04, UC20

## 1. Objetivo

Permitir que pessoas com e-mail institucional do IFPB criem conta, confirmem, entrem, recuperem e alterem a senha, encerrem a sessão e (Servidores) solicitem o perfil de Administrador.

## 2. Atores

Visitante, Estudante, Servidor, Serviço de E-mail (secundário).

## 3. Requisitos funcionais

- **RF-001 — Cadastro por domínio:** o usuário escolhe o domínio (`@academico.ifpb.edu.br` ou `@ifpb.edu.br`) e informa nome completo, prefixo do e-mail, senha e confirmação da senha.
  - Prefixo com `@` ou e-mail completo → HTTP 400, mensagem "informe só a parte antes do @".
  - Senha fora da política → recusada com os requisitos; demais campos mantidos.
  - Senhas diferentes → recusada; demais campos mantidos. *[Decisão P10.1 — campo visto no protótipo]*
  - E-mail já cadastrado → mesma mensagem de sucesso, sem criar conta; se a conta existente está confirmada, envia aviso com link de recuperação; se não, reenvia a confirmação.
  - A conta nasce **não confirmada**.
- **RF-002 — Classificação automática:** `@academico` → Estudante; `@ifpb` → Servidor; qualquer campo de perfil enviado é ignorado.
- **RF-003 — Solicitação de perfil Administrador:** um Servidor pede no cadastro (caixa "Solicitar perfil de Administrador") ou em "Minha conta". Cria solicitação PENDENTE e notifica todos os Administradores; se feita no cadastro, só entra na fila após a confirmação da conta. Estudante → 403. No máximo uma pendente por usuário. Enquanto pendente, o usuário atua como Servidor. Resultado comunicado por e-mail e no sistema.
- **RF-004 — Confirmação e recuperação:** token de confirmação vale 24 h; de recuperação, 1 h. Tokens de uso único, guardados só como hash; gerar novo invalida o anterior do mesmo tipo. Reenvio no máximo 1 por minuto. A recuperação mostra sempre a mesma mensagem. Redefinir a senha encerra todas as sessões. Token expirado → oferece reenviar; inválido ou usado → erro sem alterar a conta.
- **RF-026 — Encerrar sessão:** a sessão é invalidada no servidor.
- **RF-027 — Alterar a própria senha:** exige senha atual; nova senha na política, digitada duas vezes; as outras sessões são encerradas.

## 4. Regras e requisitos não funcionais

- **RNF-004 — Segurança:**
  - Política de senha: ≥ 8 caracteres, com letra e número, diferente do prefixo do e-mail.
  - Senhas com hash adaptativo e sal (`werkzeug.security`, decisão P6).
  - CSRF em todo formulário e em toda requisição HTMX que altera dados.
  - 5 logins falhos em 15 minutos para a mesma conta **ou** o mesmo IP bloqueiam por 15 minutos, com mensagem genérica.
  - Sessão expira após 2 h sem atividade; cookie `HttpOnly`, `Secure` (em produção) e `SameSite=Lax`.
  - Mensagens de erro não revelam se o e-mail existe.
- **Ciclo da solicitação de Administrador** [spec.md 2.5]: PENDENTE → APROVADA (perfil vira Administrador) ou RECUSADA (justificativa obrigatória). A pendente de um usuário desativado é recusada automaticamente. A decisão está na SPEC-09.
- **Primeiro Administrador** [spec.md 1.2; plan.md]: criado na implantação pelo comando `flask criar-admin`.

## 5. Campos confirmados

| Entidade | Campos |
| :--- | :--- |
| Usuário | nome, e-mail, senha (hash), perfil (ESTUDANTE, SERVIDOR, ADMINISTRADOR), ativo, confirmado, data de cadastro |
| Token | usuário, tipo (CONFIRMACAO, RECUPERACAO), hash do token, expira em, usado em |
| Solicitação de Administrador | usuário, estado, justificativa, decidido por, decidido em |

## 6. Fluxos

- **Principal (UC01→UC02→UC03):** cadastro → e-mail de confirmação enfileirado → clique no link → conta confirmada → login → dashboard.
- **Alternativos:** UC01 FA1 (pedido de Administrador no cadastro); UC04 (recuperação); UC20 FA1 (pedido em "Minha conta"); UC20 FA2 (sair).
- **Erros:** UC01 FE1–FE3; UC02 FE1–FE2; UC03 FE1 (credenciais inválidas, mensagem genérica), FE2 (não confirmada, oferece reenvio), FE3 (desativada, orienta procurar a coordenação), FE4 (bloqueio por tentativas); UC04 FE1–FE2; UC20 FE1–FE3.

## 7. Critérios de aceitação

- [ ] Cadastro com `@academico` cria Estudante e com `@ifpb` cria Servidor, ignorando qualquer campo de perfil enviado.
- [ ] Conta não confirmada não consegue entrar; após confirmar, consegue.
- [ ] Token expirado, usado ou inválido não altera a conta.
- [ ] Mensagens de cadastro, login e recuperação não revelam a existência do e-mail.
- [ ] A 6ª tentativa falha em 15 minutos é bloqueada mesmo com senha correta.
- [ ] Trocar ou redefinir a senha invalida as outras sessões.
- [ ] Estudante não vê nem consegue usar "Solicitar perfil de Administrador" (403).

## 8. Cenários de teste

1. Cadastro com prefixo `joao@ifpb.edu.br` → 400 com a mensagem do RF-001.
2. Cadastro com e-mail já confirmado → mesma resposta de sucesso, nenhuma conta nova, e-mail de aviso enfileirado.
3. Confirmação com token de 25 horas → recusada e oferta de reenvio.
4. Login de conta desativada com senha correta → bloqueado com orientação.
5. Recuperação de senha → sessões antigas deixam de ser aceitas.
6. Servidor com solicitação pendente tenta outra → 409.

## 9. Dependências, dúvidas e pendências

- Depende de: SPEC-01 (auditoria, autorização), SPEC-08 (fila de e-mails e notificações).
- Pendência: senha de app da conta Gmail do projeto (configurada só no `.env`).
