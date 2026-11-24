# SPEC-08 — Notificações e e-mails

- **Status:** Aprovada pelo estudante em 2026-11-24
- **Fontes:** `spec.md` RF20, RF21, RN04; `casos-de-uso.md` UC07; protótipo (contador de notificações no cabeçalho, "Avisos" no celular); entrevista P4 (opção B), P5
- **Casos de uso:** UC07

## 1. Objetivo

Avisar os envolvidos dentro do sistema e enviar, em segundo plano, os e-mails de assuntos da conta.

## 2. Atores

Todos os perfis; Serviço de E-mail (secundário).

## 3. Regras de negócio

- **RN-004 — Canais:** e-mail **apenas** para confirmação de cadastro, recuperação de senha, aviso de tentativa de cadastro com e-mail existente e resultado da solicitação de perfil Administrador. Avisos sobre equipamentos, solicitações e chamados são **apenas dentro do sistema**.

## 4. Requisitos funcionais

- **RF-020 — Notificações dentro do sistema:**

  | Evento | Quem recebe |
  | :--- | :--- |
  | Falha reportada (T1) | Todos os Administradores |
  | Solicitação de chamado criada | Todos os Administradores |
  | Solicitação de chamado descartada | Solicitante |
  | Chamado aberto | Quem reportou a falha ou fez a solicitação; responsável |
  | Chamado assumido, resolvido, reaberto, cancelado ou fechado | Quem reportou a falha ou fez a solicitação; responsável |
  | Falso alarme desfeito (T2) | Quem reportou a falha |
  | Solicitação de perfil Administrador criada | Todos os Administradores |
  | Solicitação de perfil Administrador aprovada ou recusada | Solicitante (também por e-mail) |

  - Quem executou a ação não recebe aviso dela.
  - Cabeçalho com contador de não lidas; abrir um aviso leva ao item e o marca como lido; "marcar todas como lidas".
  - Item do aviso excluído → aviso continua na lista e o link mostra "item excluído".
- **RF-021 — Envio em segundo plano (adaptado pela decisão P4-B):**
  - **Notificações** são gravadas no PostgreSQL na mesma transação da ação que as gera (são linhas de banco, sem envio externo); a resposta ao usuário não espera nada além disso.
  - **E-mails** são gravados numa fila de saída no PostgreSQL e enviados por um processo separado (`flask enviar-emails`, serviço próprio no Docker Compose); a resposta ao usuário não espera o envio.
  - Falha de envio → até 3 tentativas; a falha final fica registrada.
  - Com o servidor de e-mail fora do ar, cadastro e recuperação continuam respondendo normalmente.
  - Envio via SMTP com a conta Gmail do projeto (decisão P5); endereço e senha de app apenas no `.env`. Em desenvolvimento e testes, o e-mail é escrito no log em vez de enviado.

## 5. Fluxos

- UC07: contador no cabeçalho → abrir lista → clicar no aviso → abre o item → marcado como lido. FA1 marcar todas; FA2 item excluído.

## 6. Critérios de aceitação

- [ ] Cada evento da tabela gera avisos exatamente para os destinatários indicados, exceto o autor da ação.
- [ ] O contador mostra apenas não lidas do usuário logado.
- [ ] Um usuário não consegue ler nem marcar avisos de outro (403/404).
- [ ] O cadastro responde com sucesso mesmo com o SMTP indisponível; o e-mail fica na fila.
- [ ] Um e-mail que falha três vezes é marcado como falha final e não é tentado de novo.
- [ ] Nenhuma notificação de chamado é enviada por e-mail.

## 7. Cenários de teste

1. Falha reportada por Administrador A → avisos para os demais Administradores, não para A.
2. SMTP simulado falhando sempre → após 3 tentativas, e-mail com estado de falha final.
3. "Marcar todas como lidas" → contador zerado apenas para o usuário atual.
4. Aviso de equipamento depois excluído → link mostra "item excluído" e marca como lido.

## 8. Dependências, dúvidas e pendências

- Depende de: SPEC-01, SPEC-02 (usuário).
- Pendência: senha de app do Gmail configurada localmente pelo estudante.
- [Decisão] O processo de envio verifica a fila a cada 10 segundos.
