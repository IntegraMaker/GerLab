# GerLab
Projeto de pesquisa e inovação tecnológica do IFSertãoPB – Campus Sousa, voltado ao desenvolvimento de um sistema web para gestão e visualização espacial dos laboratórios de informática, facilitando o gerenciamento de ambientes, equipamentos, recursos e infraestrutura, além de apoiar a organização e o planejamento das atividades institucionais.

## GERLab — pacote de orientação

Inclui `AGENTS.md`, duas skills e `PROMPT_INICIAL.md`. Coloque os arquivos no repositório preservando os caminhos. A stack está fixada no AGENTS; não há `ARQUITETURA.md`. O estudante deve fornecer protótipo e telas ao iniciar a entrevista.

## Como executar (desenvolvimento)

Pré-requisitos: Docker Desktop (com WSL 2 no Windows) e Git.

1. Crie o arquivo de ambiente a partir do modelo e troque `SECRET_KEY` e `POSTGRES_PASSWORD`:
   ```bash
   cp .env.example .env
   ```
   O `.env` é ignorado pelo Git — nunca o versione.
2. Suba a aplicação e o banco:
   ```bash
   docker compose up -d --build
   ```
3. Acesse <http://localhost:5000>. A verificação de saúde fica em <http://localhost:5000/saude>
   (`{"status": "ok", "banco": "ok"}` quando o PostgreSQL está acessível; 503 caso contrário).
4. Para parar: `docker compose down` (os dados do banco ficam no volume `dados_db`).

### Testes

Os testes rodam **dentro do contêiner** `app`, contra o banco separado `gerlab_test`
(criado automaticamente por `docker/criar-banco-teste.sh` na primeira inicialização do volume):

```bash
docker compose exec app pytest
```

Se o volume do banco foi criado antes desse script existir, recrie-o (apaga os dados locais):
`docker compose down -v && docker compose up -d --build`.

### Migrações (Flask-Migrate/Alembic)

```bash
docker compose exec app flask --app wsgi db migrate -m "descrição"
docker compose exec app flask --app wsgi db upgrade
```

### Primeiro Administrador

Depois de aplicar as migrações (`flask --app wsgi db upgrade`), crie o primeiro Administrador.
O e-mail deve ser de Servidor (`@ifpb.edu.br`) e a senha segue a política (mínimo de 8 caracteres,
com letra e número, diferente da parte antes do @). A senha é pedida duas vezes, sem aparecer na tela:

```bash
docker compose exec app flask --app wsgi criar-admin
```

### Entrar e sair

Com a aplicação rodando, abra <http://localhost:5000/entrar> e entre com uma conta
confirmada e ativa (por exemplo, o Administrador criado acima). A página inicial `/`
exige login. A sessão expira após 2 horas sem atividade (`SESSAO_EXPIRA_HORAS`).
O botão **Sair** encerra a sessão em todos os aparelhos da pessoa.

Depois de 5 logins errados em 15 minutos, para o mesmo e-mail ou o mesmo IP, novas
tentativas ficam bloqueadas por 15 minutos, mesmo com a senha certa
(`LOGIN_MAX_FALHAS`, `LOGIN_JANELA_MINUTOS`, `LOGIN_BLOQUEIO_MINUTOS`). As tentativas ficam
anotadas na tabela `tentativa_login`.

> Depois de alterar templates, reinicie a aplicação: `docker compose restart app`.

### Notificações (avisos dentro do sistema)

Os avisos ficam na tabela `notificacao` e são criados por `notificar(...)`
(`app/services/notificacoes.py`), que nunca avisa o autor da ação. O sino no cabeçalho mostra
as não lidas e se atualiza sozinho a cada 60 segundos (HTMX). Em <http://localhost:5000/avisos>
cada pessoa vê só os próprios avisos, abre um (marca como lido e leva ao item; se o item foi
excluído, mostra "item excluído") ou marca todos como lidos.

### E-mails (fila e carteiro)

O sistema nunca espera um e-mail sair: ele grava a mensagem na tabela `email_pendente`
e o serviço `mailer` (`flask enviar-emails`) entrega a cada 10 segundos
(`EMAIL_INTERVALO_SEGUNDOS`), com até 3 tentativas (`EMAIL_MAX_TENTATIVAS`); depois disso
o e-mail fica como `FALHA`. Em desenvolvimento (`EMAIL_TRANSPORTE=log`) o e-mail só aparece no log:

```bash
docker compose logs -f mailer
```

Para uma única volta manual: `docker compose exec app flask --app wsgi enviar-emails --uma-vez`.
Em produção, use `EMAIL_TRANSPORTE=smtp` e preencha `SMTP_USUARIO`, `SMTP_SENHA` (senha de app
do Gmail) e `EMAIL_REMETENTE` apenas no `.env`.

### Permissões (403 e 409)

As permissões seguem a matriz da SPEC-01 §3, escrita em `app/domain/permissoes.py`.
Para proteger uma rota, use o decorador `@exige(Acao.X)` (`app/auth/decoradores.py`):
quem não entrou vai para o login; quem não tem permissão recebe **403** e nada é alterado.
Uma regra que descobre que o estado já mudou levanta `ConflitoDeEstado`
(`app/domain/erros.py`), que vira **409**. Em pedidos HTMX, os avisos de 403 e 409
aparecem na área `#avisos` do layout; o aviso de 409 tem o botão **Recarregar**.

### Estrutura

- `app/` — aplicação Flask (`create_app` em `app/__init__.py`), com blueprints por área
  (`main`, `auth`, `labs`, `tickets`, `admin`, `notifications`), `models/`, `services/`, `domain/`,
  `templates/` e `static/` (Bootstrap 5, Bootstrap Icons e HTMX servidos localmente em `static/vendor/`).
- `config.py` — configurações lidas de variáveis de ambiente (SPEC-01 §7).
- `migrations/` — migrações do banco.
- `tests/` — testes pytest.
- `docs/` — INTENT, SPECs, PLAN e registro de alterações.
- `desafios/` — microdesafios de aprendizagem, um diretório por Issue.
