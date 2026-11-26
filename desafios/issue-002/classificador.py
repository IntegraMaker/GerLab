def classificar_perfil(email):
    email = email.lower()

    parte, separador, dominio = email.partition("@")

    if not parte or not separador:
        return None

    if dominio == "academico.ifpb.edu.br":
        return "ESTUDANTE"

    if dominio == "ifpb.edu.br":
        return "SERVIDOR"

    return None