# SPEC-03 — Salas, categorias e equipamentos

- **Status:** Aprovada pelo estudante em 2026-11-24
- **Issues:** [#13](https://github.com/IntegraMaker/GerLab/issues/13) P-013, [#14](https://github.com/IntegraMaker/GerLab/issues/14) P-014, [#15](https://github.com/IntegraMaker/GerLab/issues/15) P-015, [#16](https://github.com/IntegraMaker/GerLab/issues/16) P-016, [#37](https://github.com/IntegraMaker/GerLab/issues/37) P-037 — card no Project [GERLab — Desenvolvimento](https://github.com/users/lucascaetano222/projects/1)
- **Fontes:** `spec.md` RF06, RF07, RF08, RF11, RF12, RF28, RN02, RN05, RNF07; `casos-de-uso.md` UC13, UC14, UC23; `plan.md` (categorias iniciais, ícones); protótipo telas "Dashboard" e "Planta"; entrevista P7, P8
- **Casos de uso:** UC13, UC14, UC23

## 1. Objetivo

Permitir ao Administrador manter o cadastro de categorias, salas, equipamentos e periféricos, com exclusão lógica confirmada e upload de imagem seguro.

## 2. Atores

Administrador.

## 3. Requisitos funcionais

- **RF-028 — Manter categorias:** nome, tipo (EQUIPAMENTO ou PERIFERICO) e ícone escolhido numa biblioteca do sistema (Bootstrap Icons). Nome único entre categorias ativas. Categoria em uso por item ativo não é excluída; o sistema lista os itens. Conjunto inicial carregado na implantação: Computador, Notebook, Projetor, Impressora, Roteador (equipamento); Monitor, Teclado, Mouse (periférico) [Fonte: plan.md].
- **RF-006 — Cadastro de salas:** nome, bloco, largura e comprimento em metros, observações.
  - Dimensões numéricas, > 0 e ≤ 100 m, até duas casas decimais.
  - Nome único dentro do bloco entre salas ativas.
  - Reduzir dimensões deixando equipamento fora → recusado, listando os itens a reposicionar.
  - Sala nova gera planta vazia na proporção informada.
  - [Decisão P7] **Não há campo "código da sala"**; o texto "Sala C-104" do protótipo foi apenas demonstração.
- **RF-007 — Equipamentos e periféricos:** equipamento tem nome, categoria (tipo equipamento), descrição, observações, **localização/bancada** (texto opcional, até 100 caracteres, apenas informativo — [Decisão P8]), foto opcional e posição na planta. Periférico tem nome e categoria (tipo periférico) e está vinculado a exatamente um equipamento, na mesma sala dele, sem status próprio. Equipamento nasce Verde. Nome e categoria obrigatórios.
- **RF-008 — Ícones:** cada item é exibido com o ícone da sua categoria, sempre com o indicador de status; trocar a categoria troca o ícone; trocar o ícone da categoria atualiza todos os itens.
- **RF-011 — Exclusão com confirmação:** nenhum item é excluído sem confirmação; a confirmação lista o que será afetado (equipamentos e periféricos da sala, periféricos do equipamento, solicitações a descartar, chamados a cancelar). Desistir não altera nada. Exclusão lógica (RN-002).
- **RF-012 — Upload de imagens (RN-005):** apenas JPG ou PNG verificados pelo conteúdo; até 5 MB; uma foto por equipamento, ocorrência e solicitação; EXIF removido. > 5 MB → 413; outro formato → 400; mensagem informa limite e formatos; texto já digitado é mantido; o formulário avisa para não fotografar pessoas.

## 4. Regras e RNF

- RN-002 (exclusão lógica em cascata) — SPEC-01.
- RNF-007 — sala com 200 equipamentos ativos não aceita novo cadastro.
- As imagens ficam fora da pasta pública e são servidas por rota que exige autenticação [Fonte: plan.md].

## 5. Campos confirmados

| Entidade | Campos |
| :--- | :--- |
| Categoria | nome, tipo, ícone |
| Sala | nome, bloco, largura_m, comprimento_m, observações |
| Equipamento | sala, categoria, nome, descrição, observações, localização (opcional), foto, pos_x, pos_y (metros), status, status antes da exclusão |
| Periférico | equipamento, categoria, nome |

Todas as entidades acima têm marcação de exclusão lógica (quem excluiu, quando e identificador da exclusão em cascata).

## 6. Fluxos

- UC23: nova categoria; FA1 editar (troca de ícone propaga); FA2 excluir; FE1 nome repetido; FE2 em uso.
- UC13: nova sala; FA1 editar (posições em metros preservadas); FA2 excluir com confirmação e cascata; FE1 dimensões inválidas; FE2 redução que deixa itens fora; FE3 nome repetido no bloco.
- UC14: novo equipamento (nasce Verde, posicionado na planta); FA1 cadastrar periférico; FA2 editar; FA3 excluir; FE1 campos obrigatórios; FE2 sala no limite.

## 7. Critérios de aceitação

- [ ] Sala com dimensão 0, negativa, texto ou > 100 m é recusada.
- [ ] Duas salas ativas com o mesmo nome no mesmo bloco não são aceitas; em blocos diferentes, são.
- [ ] Equipamento só aceita categoria do tipo equipamento; periférico só do tipo periférico.
- [ ] Excluir sala exclui logicamente seus equipamentos e periféricos, após tela de confirmação.
- [ ] Categoria em uso não é excluída e os itens que a usam são listados.
- [ ] Arquivo PNG renomeado para `.jpg` é aceito; arquivo de texto renomeado para `.png` é recusado com 400; imagem gravada não contém EXIF.

## 8. Cenários de teste

1. Criar sala 12 × 8 m → planta vazia; editar para 5 × 5 com equipamento em (10, 6) → recusado listando o equipamento.
2. Criar equipamento numa sala com 200 equipamentos ativos → recusado.
3. Excluir categoria usada por um equipamento ativo → recusado com a lista.
4. Upload de 6 MB → 413 e texto do formulário mantido.
5. Trocar o ícone de "Computador" → todos os computadores exibem o novo ícone.

## 9. Dependências, dúvidas e pendências

- Depende de: SPEC-01, SPEC-02 (login e perfil).
- O cancelamento de chamados e o descarte de solicitações na exclusão dependem da SPEC-07; até lá, a exclusão trata apenas sala, equipamentos e periféricos.
- [Decisão 2026-11-24] Campo "localização/bancada": no máximo 100 caracteres.
