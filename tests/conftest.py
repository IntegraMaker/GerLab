"""Fixtures compartilhadas pelos testes do GERLab.

Os testes usam create_app("testing"), que aponta para o banco separado
definido em TEST_DATABASE_URL (gerlab_test) — nunca o banco de desenvolvimento.
"""
import os

import pytest

from app import create_app
from app.extensions import db


@pytest.fixture
def app():
    if not os.environ.get("TEST_DATABASE_URL"):
        pytest.fail("TEST_DATABASE_URL não definida: rode o pytest dentro do contêiner app.")
    app = create_app("testing")
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def banco(app):
    """Cria as tabelas no gerlab_test antes do teste e apaga tudo depois."""
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()
