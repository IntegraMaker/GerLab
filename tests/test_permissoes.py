"""Testes da matriz de permissões (Issue #6, Etapa 1) — SPEC-01 §3."""
import pytest

from app.domain.permissoes import MATRIZ, Acao, pode
from app.models import Perfil, Usuario

E, S, A = "E", "S", "A"

# A tabela da SPEC-01 §3 copiada como texto: X = permitido.
#                                      Estudante Servidor Administrador
TABELA_DA_SPEC = {
    Acao.VISUALIZAR:                 (E, S, A),
    Acao.CONSULTAR_HISTORICO:        (E, S, A),
    Acao.VER_PROPRIAS_NOTIFICACOES:  (E, S, A),
    Acao.GERENCIAR_PROPRIA_CONTA:    (E, S, A),
    Acao.REGISTRAR_OCORRENCIA:       (E, S, A),
    Acao.REPORTAR_FALHA:             (E, S, A),
    Acao.MOVER_EQUIPAMENTOS:         (S, A),
    Acao.EDITAR_OBSERVACOES:         (S, A),
    Acao.SOLICITAR_CHAMADO:          (S,),
    Acao.SOLICITAR_ADMINISTRADOR:    (S,),
    Acao.GERENCIAR_CADASTROS:        (A,),
    Acao.GERENCIAR_CHAMADOS:         (A,),
    Acao.MODERAR:                    (A,),
    Acao.CONSULTAR_AUDITORIA:        (A,),
    Acao.GERENCIAR_USUARIOS:         (A,),
}
LETRA = {Perfil.ESTUDANTE: E, Perfil.SERVIDOR: S, Perfil.ADMINISTRADOR: A}


def _usuario(perfil, ativo=True):
    # Não precisa de banco: só o objeto em memória.
    return Usuario(nome="Teste", email="t@ifpb.edu.br", perfil=perfil, ativo=ativo)


def test_matriz_tem_as_15_linhas_da_spec():
    assert set(MATRIZ) == set(Acao) == set(TABELA_DA_SPEC)
    assert len(Acao) == 15


@pytest.mark.parametrize("acao", list(Acao), ids=lambda a: a.name)
@pytest.mark.parametrize("perfil", list(Perfil), ids=lambda p: p.name)
def test_cada_celula_igual_a_spec(perfil, acao):
    esperado = LETRA[perfil] in TABELA_DA_SPEC[acao]
    assert pode(_usuario(perfil), acao) is esperado


def test_administrador_nao_solicita_chamado_nem_perfil():
    # A matriz não é uma "escada": estas duas ações são só do Servidor.
    admin = _usuario(Perfil.ADMINISTRADOR)
    assert pode(admin, Acao.SOLICITAR_CHAMADO) is False
    assert pode(admin, Acao.SOLICITAR_ADMINISTRADOR) is False
    assert pode(_usuario(Perfil.SERVIDOR), Acao.SOLICITAR_CHAMADO) is True


def test_sem_usuario_ou_conta_desativada_nao_pode_nada():
    assert pode(None, Acao.VISUALIZAR) is False
    assert pode(_usuario(Perfil.ADMINISTRADOR, ativo=False), Acao.VISUALIZAR) is False
