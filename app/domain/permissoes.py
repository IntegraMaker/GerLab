"""Matriz de permissões do MVP (SPEC-01 §3, RN-003; Issue #6).

Cada ação da tabela da SPEC vira um item de `Acao`, e `MATRIZ` diz quais
perfis podem fazê-la. Quem não está na linha recebe HTTP 403.

Não é uma "escada" (Administrador pode tudo): duas ações são só do
Servidor — solicitar chamado técnico e solicitar perfil de Administrador.
Por isso a tabela é escrita linha por linha, igual à SPEC.
"""
import enum

from app.models.usuario import Perfil

E, S, A = Perfil.ESTUDANTE, Perfil.SERVIDOR, Perfil.ADMINISTRADOR
TODOS = frozenset({E, S, A})


class Acao(enum.Enum):
    """As linhas da matriz da SPEC-01 §3, na mesma ordem."""
    VISUALIZAR = "Visualizar dashboard, plantas, status e popovers"
    CONSULTAR_HISTORICO = "Consultar histórico de equipamento ativo"
    VER_PROPRIAS_NOTIFICACOES = "Ver e marcar como lidas as próprias notificações"
    GERENCIAR_PROPRIA_CONTA = "Alterar a própria senha e encerrar a sessão"
    REGISTRAR_OCORRENCIA = "Registrar ocorrência (texto + foto)"
    REPORTAR_FALHA = "Reportar falha (Verde → Vermelho)"
    MOVER_EQUIPAMENTOS = "Mover equipamentos e periféricos"
    EDITAR_OBSERVACOES = "Editar observações da sala e do equipamento"
    SOLICITAR_CHAMADO = "Solicitar chamado técnico"
    SOLICITAR_ADMINISTRADOR = "Solicitar perfil de Administrador"
    GERENCIAR_CADASTROS = "Criar, editar e excluir salas, equipamentos, periféricos e categorias"
    GERENCIAR_CHAMADOS = "Acessar a fila; abrir, assumir, resolver, reabrir, cancelar e fechar chamados"
    MODERAR = "Desfazer falso alarme; descartar solicitação; ocultar ocorrência"
    CONSULTAR_AUDITORIA = "Consultar log de auditoria"
    GERENCIAR_USUARIOS = "Gerenciar usuários e decidir solicitações de Administrador"


MATRIZ = {
    Acao.VISUALIZAR: TODOS,
    Acao.CONSULTAR_HISTORICO: TODOS,
    Acao.VER_PROPRIAS_NOTIFICACOES: TODOS,
    Acao.GERENCIAR_PROPRIA_CONTA: TODOS,
    Acao.REGISTRAR_OCORRENCIA: TODOS,
    Acao.REPORTAR_FALHA: TODOS,
    Acao.MOVER_EQUIPAMENTOS: frozenset({S, A}),
    Acao.EDITAR_OBSERVACOES: frozenset({S, A}),
    Acao.SOLICITAR_CHAMADO: frozenset({S}),          # só Servidor
    Acao.SOLICITAR_ADMINISTRADOR: frozenset({S}),    # só Servidor
    Acao.GERENCIAR_CADASTROS: frozenset({A}),
    Acao.GERENCIAR_CHAMADOS: frozenset({A}),
    Acao.MODERAR: frozenset({A}),
    Acao.CONSULTAR_AUDITORIA: frozenset({A}),
    Acao.GERENCIAR_USUARIOS: frozenset({A}),
}


def pode(usuario, acao):
    """True se o usuário pode fazer a ação.

    Quem não entrou (sem perfil) ou está com a conta desativada não pode nada.
    """
    perfil = getattr(usuario, "perfil", None)
    if perfil is None or not getattr(usuario, "ativo", False):
        return False
    return perfil in MATRIZ[acao]
