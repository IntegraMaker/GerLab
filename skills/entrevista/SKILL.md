# Skill — Entrevista e formalização dos requisitos do GERLab

## Quando usar
No início do projeto, sempre que o estudante apresentar requisitos, telas, protótipo, fluxos, desenhos ou documentos ainda não formalizados; ou quando novas funcionalidades exigirem levantamento de requisitos.

## Objetivo
Transformar as **fontes reais fornecidas pelo estudante** em `docs/INTENT.md`, `docs/specs/SPEC-NN-*.md` e `docs/PLAN.md`, sem inventar funcionalidades. A entrevista complementa, mas não substitui, a inspeção dos materiais existentes.

## Etapa 1 — Inventário e leitura das fontes
- Localize e abra os arquivos do projeto, protótipo, capturas de telas e requisitos existentes.
- Enumere cada tela, fluxo e documento, com referência ao arquivo de origem.
- Para cada funcionalidade observada, registre: evidência, comportamento aparente, campos, ações, validações, navegação e incertezas.
- Diferencie **o que a tela mostra** de **como o sistema deveria funcionar**. Um botão visível não prova uma regra de negócio.
- Se o protótipo não estiver disponível, solicite o arquivo ou link; não finja tê-lo analisado.

## Etapa 2 — Entrevista progressiva
Pergunte apenas o necessário para eliminar ambiguidades que impactam requisitos ou arquitetura. Priorize perguntas sobre:
1. problema a resolver, usuários e resultado esperado;
2. funcionalidades indispensáveis e funcionalidades futuras;
3. significado dos campos, regras, estados e ações das telas;
4. fluxos alternativos, erros, permissões e restrições;
5. persistência, importação/exportação e integrações;
6. requisitos não funcionais: segurança, acessibilidade, dispositivos, desempenho e implantação;
7. necessidades técnicas específicas das telas (sem rediscutir a stack obrigatória do AGENTS.md).

Faça perguntas **em pequenos blocos**, preferencialmente uma decisão relevante por vez. Não faça questionários extensos sem necessidade. Sempre ofereça uma interpretação provisória e peça confirmação quando houver ambiguidade.

## Etapa 3 — Gerar INTENT
Crie `docs/INTENT.md` com:
- contexto e problema;
- público-alvo e papéis;
- objetivo e resultados esperados;
- escopo do MVP e exclusões;
- principais jornadas;
- critérios de sucesso;
- restrições, premissas e pendências;
- fontes consultadas.

Não trate ideias futuras como requisitos obrigatórios do MVP.

## Etapa 4 — Gerar SPECs
Divida em documentos temáticos pequenos, `docs/specs/SPEC-01-*.md`, etc. Cada SPEC deve conter:
- identificação, status (`Rascunho`, `Em validação`, `Aprovada`) e fontes;
- objetivo e atores;
- requisitos funcionais identificados (RF-NNN);
- regras de negócio (RN-NNN) e requisitos não funcionais aplicáveis;
- campos e entidades **somente quando confirmados**;
- fluxos principal, alternativos e de erro;
- critérios de aceitação verificáveis;
- pelo menos três cenários de teste relevantes;
- dependências, dúvidas e decisões pendentes.

Associe requisitos às telas/protótipo sempre que possível. Não copie detalhes visuais como regra de negócio sem confirmação.

## Etapa 5 — Verificar restrições técnicas
Consulte a stack obrigatória no `AGENTS.md`: Flask, Jinja2, HTMX, Bootstrap 5, PostgreSQL, SQLAlchemy, Flask-Migrate, pytest e Docker Compose. **Não criar `ARQUITETURA.md` e não perguntar qual stack escolher.** Identifique apenas necessidades específicas do protótipo (por exemplo, biblioteca para planta interativa, caso a funcionalidade exista nas fontes). Registre escolhas técnicas adicionais e suas justificativas em `docs/PLAN.md`; marque decisões pendentes sem inventá-las.

## Etapa 6 — Gerar PLAN
Crie `docs/PLAN.md` com:
- etapas incrementais do MVP;
- ordem por dependências;
- entregas demonstráveis;
- referência às SPECs;
- propostas de Issues pequenas, cada uma com objetivo, critérios de aceite e três testes;
- itens bloqueados por decisão pendente.

A primeira Issue técnica deve preparar o ambiente e a estrutura inicial da aplicação conforme a stack do `AGENTS.md`.

## Etapa 7 — Validação e publicação
1. Mostre ao estudante um resumo das decisões e pendências.
2. Solicite confirmação explícita das SPECs e do PLAN antes de marcá-las como aprovadas.
3. Após aprovação, aplique o processo do `AGENTS.md` para criar Issues reais, GitHub Project e cards vinculados.
4. Verifique que todas as Issues estão no Board e que a primeira está em `Ready`.
5. Só então inicie a implementação por Issue.

## Restrições
- Não inventar telas, fluxos, campos, perfis ou funcionalidades.
- Não considerar documentos aprovados sem confirmação.
- Não implementar durante a entrevista e formalização.
- Não declarar operações no GitHub concluídas sem verificação.
