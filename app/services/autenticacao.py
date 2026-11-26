"""Conferência de e-mail e senha no login (SPEC-02, UC03 FE1-FE4).

O serviço só responde "deu certo?" e, se não deu, "por quê?". Quem mostra a
mensagem na tela e quem abre a sessão é a rota.
"""
import enum

from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.models import Usuario
from app.services.limite_login import esta_bloqueado, registrar_tentativa


class ResultadoLogin(enum.Enum):
    OK = "OK"
    CREDENCIAIS_INVALIDAS = "CREDENCIAIS_INVALIDAS"   # FE1
    NAO_CONFIRMADA = "NAO_CONFIRMADA"                 # FE2
    DESATIVADA = "DESATIVADA"                         # FE3
    BLOQUEADO = "BLOQUEADO"                           # FE4 (Issue #5)


# Hash "de mentira" usado quando o e-mail não existe. Assim o login demora
# o mesmo tempo nos dois casos, e o tempo de resposta não denuncia quais
# e-mails estão cadastrados.
_HASH_FALSO = generate_password_hash("senha-que-nao-existe")


def autenticar(email, senha, ip, agora=None):
    """Devolve (ResultadoLogin, usuario ou None).

    Anota a tentativa no caderno da portaria (TentativaLogin), mas não faz
    commit: quem chama (a rota) confirma tudo de uma vez.
    `agora` só é passado nos testes ("relógio simulado").
    """
    email = (email or "").strip().lower()
    senha = senha or ""

    # FE4: de castigo, nem olhamos a senha — mesmo que ela esteja certa.
    # A tentativa não é anotada como falha, para o castigo não aumentar.
    if esta_bloqueado(email, ip, agora=agora):
        return ResultadoLogin.BLOQUEADO, None

    resultado, usuario = _conferir(email, senha)

    # Só "e-mail ou senha inválidos" conta como falha. Nos demais casos a
    # senha estava certa (é o próprio dono), então não conta para o bloqueio.
    falhou = resultado is ResultadoLogin.CREDENCIAIS_INVALIDAS
    registrar_tentativa(email, ip, sucesso=not falhou, agora=agora)
    return resultado, usuario


def _conferir(email, senha):
    """Confere e-mail e senha e explica o resultado (FE1-FE3)."""
    usuario = db.session.execute(
        db.select(Usuario).filter_by(email=email)
    ).scalar_one_or_none()

    if usuario is None:
        check_password_hash(_HASH_FALSO, senha)
        return ResultadoLogin.CREDENCIAIS_INVALIDAS, None

    if not usuario.verificar_senha(senha):
        # Senha errada: mesma resposta do e-mail inexistente (FE1),
        # mesmo que a conta esteja desativada ou sem confirmação.
        return ResultadoLogin.CREDENCIAIS_INVALIDAS, None

    # Daqui em diante a senha está certa: podemos explicar o motivo.
    if not usuario.ativo:
        return ResultadoLogin.DESATIVADA, usuario
    if not usuario.confirmado:
        return ResultadoLogin.NAO_CONFIRMADA, usuario
    return ResultadoLogin.OK, usuario
