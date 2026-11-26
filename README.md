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

### Estrutura

- `app/` — aplicação Flask (`create_app` em `app/__init__.py`), com blueprints por área
  (`main`, `auth`, `labs`, `tickets`, `admin`, `notifications`), `models/`, `services/`, `domain/`,
  `templates/` e `static/` (Bootstrap 5, Bootstrap Icons e HTMX servidos localmente em `static/vendor/`).
- `config.py` — configurações lidas de variáveis de ambiente (SPEC-01 §7).
- `migrations/` — migrações do banco.
- `tests/` — testes pytest.
- `docs/` — INTENT, SPECs, PLAN e registro de alterações.
- `desafios/` — microdesafios de aprendizagem, um diretório por Issue.
