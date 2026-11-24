# SPEC-05 — Layout da sala e observações

- **Status:** Aprovada pelo estudante em 2026-11-24
- **Fontes:** `spec.md` RF09, RF10, RF13; `casos-de-uso.md` UC10, UC11; `plan.md` (posição livre em grade de 0,5 m); protótipo tela "Planta" (botões "Editar layout", "Mover", "Editar observação")
- **Casos de uso:** UC10, UC11

## 1. Objetivo

Permitir que Servidores e Administradores reposicionem equipamentos (na sala ou entre salas), transfiram periféricos e editem observações formatadas.

## 2. Atores

Servidor, Administrador.

## 3. Requisitos funcionais

- **RF-009 — Posicionamento:** no modo "Editar layout", arrastar o ícone para a nova posição (mouse e toque). Posição gravada em metros e mantida ao recarregar e em qualquer tela. Soltar fora da sala ou sobre outro ícone → volta à posição anterior com aviso. Alternativa sem arrastar: setas do teclado ou formulário de coordenadas. Modo de edição não aparece para Estudante; requisição direta → 403.
- **RF-010 — Modificação de layout:** mover equipamento para qualquer sala ativa; leva periféricos, histórico, ocorrências e chamado não fechado. Na sala de destino o sistema propõe posição livre (primeira célula livre numa grade de 0,5 m [Fonte: plan.md]); sem espaço livre, o usuário escolhe. Salas excluídas ou no limite de 200 equipamentos não aparecem como destino. Transferir periférico entre equipamentos; o periférico passa à sala do novo equipamento. Log com sala e posição anteriores e novas.
- **RF-013 — Observações formatadas:** observações da sala e do equipamento aceitam negrito, itálico, listas e links (apenas `http`/`https`); qualquer outra marcação é removida antes de gravar (biblioteca nh3); até 5.000 caracteres; cada edição gera log com a versão anterior.

## 4. Fluxos

- UC10: ativar edição → arrastar → validar limites → gravar em metros + log → confirmar sem recarregar. FA1 mover para outra sala; FA2 transferir periférico; FA3 teclado/formulário; FE1 fora da sala/sobreposto; FE2 Estudante → 403; FE3 sala de destino no limite.
- UC11: "Editar observações" → editor → salvar → sanitizar + log. FA1 observação do equipamento; FE1 script removido; FE2 > 5.000 caracteres.

## 5. Critérios de aceitação

- [ ] Posição (x, y) fora de [0, largura] × [0, comprimento] é recusada pelo servidor.
- [ ] Posição sobre outro ícone é recusada pelo servidor.
- [ ] Mover equipamento para outra sala leva os periféricos e mantém o histórico e o chamado.
- [ ] `<script>` e links `javascript:` nas observações são removidos; negrito, itálico, listas e links `https` permanecem.
- [ ] Movimentação e edição de observação geram log com valores anterior e novo.
- [ ] O movimento pode ser feito apenas com o teclado.

## 6. Cenários de teste

1. Servidor move PC-01 para (3,5; 2,0) numa sala 12 × 8 → gravado e log criado.
2. Estudante envia POST de movimentação → 403, posição inalterada.
3. Mover para sala com 200 equipamentos → sala não aparece como destino e POST direto é recusado.
4. Observação com `<b>ok</b><script>x</script>` → grava `<b>ok</b>`.

## 7. Dependências, dúvidas e pendências

- Depende de: SPEC-03, SPEC-04.
- [Decisão] Sobreposição = distância < 0,5 m entre os centros dos ícones (coerente com a grade de 0,5 m).
- [Decisão] Editor de observações sem biblioteca externa: botões que inserem a marcação básica num `<textarea>` e prévia sanitizada no servidor via HTMX.
