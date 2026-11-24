# SPEC-01 — Fundamentos e regras transversais

- **Status:** Aprovada pelo estudante em 2026-11-24
- **Fontes:** `spec.md` §1, §3, §5, §6; `plan.md` §2; entrevista P2, P3, P4, P6
- **Convenção de IDs:** os identificadores preservam a numeração das fontes (RF01 → RF-001, RN01 → RN-001, RNF01 → RNF-001, UC01 → UC01). Números de itens fora do MVP ficam vagos.

## 1. Objetivo

Definir perfis, matriz de permissões, auditoria, exclusão lógica, validação no servidor e requisitos não funcionais comuns a todas as SPECs.

## 2. Atores

Estudante, Servidor, Administrador (herança: Administrador ⊃ Servidor ⊃ Estudante nas ações de visualização, ocorrência e falha; exceções na matriz).

## 3. Matriz de permissões do MVP

[Fonte: spec.md 1.3, sem as linhas fora do MVP] `X` = permitido; vazio = HTTP 403.

| Ação | Estudante | Servidor | Administrador |
| :--- | :---: | :---: | :---: |
| Visualizar dashboard, plantas, status e popovers | X | X | X |
| Consultar histórico de equipamento ativo | X | X | X |
| Ver e marcar como lidas as próprias notificações | X | X | X |
| Alterar a própria senha e encerrar a sessão | X | X | X |
| Registrar ocorrência (texto + foto) | X | X | X |
| Reportar falha (Verde → Vermelho) | X | X | X |
| Mover equipamentos e periféricos | | X | X |
| Editar observações da sala e do equipamento | | X | X |
| Solicitar chamado técnico | | X | |
| Solicitar perfil de Administrador | | X | |
| Criar, editar e excluir salas, equipamentos, periféricos e categorias | | | X |
| Acessar a fila; abrir, assumir, resolver, reabrir, cancelar e fechar chamados | | | X |
| Desfazer falso alarme; descartar solicitação; ocultar ocorrência | | | X |
| Consultar log de auditoria | | | X |
| Gerenciar usuários e decidir solicitações de Administrador | | | X |

**Fora do MVP:** editar equipamentos em lote; consultar e restaurar itens excluídos.

## 4. Regras de negócio

- **RN-001 — Auditoria:** geram registro imutável no log: mudança de status do equipamento; criação, edição, movimentação e exclusão de sala, equipamento, periférico e categoria; edição de observações (com versão anterior); criação e ocultação de ocorrência; criação e mudança de estado de solicitação e de chamado; ativação, desativação, mudança de perfil e decisão sobre solicitação de Administrador. *(Restauração fica fora do MVP.)*
- **RN-002 — Exclusão lógica:** sala, equipamento, periférico, categoria, ocorrência, solicitação e chamado nunca são apagados fisicamente; usuários são apenas desativados. Item excluído some das telas operacionais. Excluir sala exclui seus equipamentos e periféricos; excluir equipamento exclui seus periféricos. Logs, ocorrências e chamados ficam intactos. Solicitações pendentes são descartadas e chamados não fechados são cancelados com justificativa "item excluído" (detalhado na SPEC-07). Categoria só é excluída se nenhum item ativo a usa.
- **RN-003 — Validação no servidor:** toda ação é conferida no servidor contra a matriz (§3) e as tabelas de transição (SPEC-06, SPEC-07, SPEC-02). Perfil sem permissão → HTTP 403 sem alteração. Transição inválida para o estado atual (inclusive por concorrência) → HTTP 409 sem alteração, e a interface recarrega o estado.

## 5. Requisitos funcionais transversais

- **RF-016 — Log estruturado:** cada evento da RN-001 gera registro com autor, data e hora, entidade, ação, valor anterior e valor novo; não existe rota para editar ou apagar; o registro é gravado **na mesma transação** da alteração. (A tela de consulta está na SPEC-09.)

## 6. Requisitos não funcionais

- **RNF-001 — Escopo:** apenas mapeamento espacial e operacional; sem patrimônio, contabilidade, inventário de software, agenda ou reservas.
- **RNF-003 — Validação no servidor:** permissões, transições, formatos, tamanhos e limites validados no servidor; requisições forjadas recebem 400, 403 ou 409.
- **RNF-005 — Acessibilidade:** meta WCAG 2.1 AA; status nunca só por cor (sempre ícone/forma e texto); contraste 4,5:1 para texto e 3:1 para ícones; ações da planta acessíveis por teclado; controles com nome acessível.
- **RNF-006 — Privacidade (LGPD), parte do MVP:** dados tratados: nome, e-mail institucional e autoria; nome do autor visível a autenticados, e-mail só ao Administrador; fotos sem metadados; aviso de privacidade acessível no cadastro, no login e no rodapé; anonimização manual a pedido do titular (SPEC-09). *Anonimização automática após 2 anos: fora do MVP.*
- **RNF-007 — Limites:** no máximo 200 equipamentos ativos por sala; cadastro e movimentação que ultrapassem o limite são recusados. *Metas de tempo de resposta: registradas como objetivo, sem teste de carga no MVP.*
- **RNF-008 — Compatibilidade:** duas últimas versões estáveis de Chrome, Firefox, Edge e Safari; telas a partir de 360 px; toque para zoom, pan e ações.

## 7. Parâmetros

[Fonte: spec.md §6] Ficam em configuração, lidos de variáveis de ambiente com estes padrões:

| Item | Valor |
| :--- | :--- |
| Validade dos tokens | 24 h (confirmação) · 1 h (recuperação) |
| Reenvio de link | no máximo 1 por minuto |
| Política de senha | 8+ caracteres, letra e número, diferente do prefixo do e-mail |
| Bloqueio de login | 5 falhas em 15 min → 15 min |
| Expiração da sessão | 2 h sem atividade |
| Dimensão máxima da sala | 100 m |
| Equipamentos por sala | 200 |
| Tamanho de textos | 2.000 (ocorrência) · 5.000 (observação) |
| Parecer técnico | mínimo 10 caracteres |
| Imagem | JPG ou PNG, até 5 MB |
| Prioridades | Baixa, Média, Alta |

## 8. Critérios de aceitação

- [ ] Toda rota que altera dados verifica o perfil no servidor e responde 403 quando não permitido.
- [ ] Toda alteração listada na RN-001 cria exatamente um registro de log na mesma transação.
- [ ] Se a gravação do log falhar, a alteração também é desfeita.
- [ ] Itens com exclusão lógica não aparecem em consultas operacionais.
- [ ] Os parâmetros do §7 podem ser alterados por variável de ambiente sem mudar código.

## 9. Cenários de teste

1. Estudante envia requisição direta para criar sala → 403 e nenhuma sala criada.
2. Alteração auditável com falha forçada na gravação do log → nenhuma das duas gravações persiste.
3. Equipamento excluído logicamente não aparece na listagem da sala nem no dashboard, mas continua no banco.
4. Duas mudanças concorrentes sobre o mesmo item → a segunda recebe 409.

## 10. Dependências, dúvidas e pendências

- Dependências: nenhuma (base das demais SPECs).
- Pendência: local de implantação e HTTPS em produção.
