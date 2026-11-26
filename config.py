"""Configurações do GERLab, lidas de variáveis de ambiente (SPEC-01 §7)."""
import os


def _env_int(nome, padrao):
    return int(os.environ.get(nome, padrao))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CSRF global (Flask-WTF). O HTMX envia o token no cabeçalho X-CSRFToken.
    WTF_CSRF_ENABLED = True
    WTF_CSRF_HEADERS = ["X-CSRFToken"]

    # Parâmetros da SPEC-01 §7 (alteráveis por variável de ambiente)
    TOKEN_CONFIRMACAO_HORAS = _env_int("TOKEN_CONFIRMACAO_HORAS", 24)
    TOKEN_RECUPERACAO_HORAS = _env_int("TOKEN_RECUPERACAO_HORAS", 1)
    REENVIO_LINK_SEGUNDOS = _env_int("REENVIO_LINK_SEGUNDOS", 60)
    SENHA_MIN_CARACTERES = _env_int("SENHA_MIN_CARACTERES", 8)
    LOGIN_MAX_FALHAS = _env_int("LOGIN_MAX_FALHAS", 5)
    LOGIN_JANELA_MINUTOS = _env_int("LOGIN_JANELA_MINUTOS", 15)
    LOGIN_BLOQUEIO_MINUTOS = _env_int("LOGIN_BLOQUEIO_MINUTOS", 15)
    SESSAO_EXPIRA_HORAS = _env_int("SESSAO_EXPIRA_HORAS", 2)
    SALA_DIMENSAO_MAX_M = _env_int("SALA_DIMENSAO_MAX_M", 100)
    SALA_MAX_EQUIPAMENTOS = _env_int("SALA_MAX_EQUIPAMENTOS", 200)
    OCORRENCIA_MAX_CARACTERES = _env_int("OCORRENCIA_MAX_CARACTERES", 2000)
    OBSERVACAO_MAX_CARACTERES = _env_int("OBSERVACAO_MAX_CARACTERES", 5000)
    PARECER_MIN_CARACTERES = _env_int("PARECER_MIN_CARACTERES", 10)
    IMAGEM_MAX_MB = _env_int("IMAGEM_MAX_MB", 5)
    IMAGEM_FORMATOS = ("jpg", "jpeg", "png")
    PRIORIDADES = ("Baixa", "Média", "Alta")


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = os.environ.get("SECRET_KEY", "chave-apenas-para-testes")
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL")


class ProductionConfig(Config):
    SESSION_COOKIE_SECURE = True


config_por_nome = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
