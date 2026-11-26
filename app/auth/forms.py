"""Formulários do blueprint auth (o Flask-WTF já inclui o token CSRF)."""
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField
from wtforms.validators import DataRequired, Length


class FormularioEntrar(FlaskForm):
    email = EmailField(
        "E-mail institucional",
        validators=[DataRequired("Informe o e-mail."), Length(max=254)],
    )
    senha = PasswordField(
        "Senha",
        validators=[DataRequired("Informe a senha.")],
    )
