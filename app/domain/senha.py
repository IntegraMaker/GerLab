"""Política de senha (SPEC-02 RNF-004) — regra pura, sem banco nem Flask.

A senha precisa ter pelo menos `minimo` caracteres, ao menos uma letra e
um número, e ser diferente do prefixo do e-mail (sem diferenciar maiúsculas).
"""


def problemas_da_senha(senha, prefixo_email, minimo=8):
    """Devolve a lista de requisitos não atendidos (lista vazia = senha válida)."""
    problemas = []
    if len(senha) < minimo:
        problemas.append(f"A senha deve ter pelo menos {minimo} caracteres.")
    if not any(c.isalpha() for c in senha):
        problemas.append("A senha deve conter pelo menos uma letra.")
    if not any(c.isdigit() for c in senha):
        problemas.append("A senha deve conter pelo menos um número.")
    if prefixo_email and senha.lower() == prefixo_email.lower():
        problemas.append("A senha não pode ser igual à parte do e-mail antes do @.")
    return problemas
