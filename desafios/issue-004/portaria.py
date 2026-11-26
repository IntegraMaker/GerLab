def conferir_cracha(cracha, versoes):
    try:
        usuario_texto, versao_texto = cracha.split(":")
        usuario_id = int(usuario_texto)
        versao_cracha = int(versao_texto)
    except (AttributeError, ValueError):
        return None

    if usuario_id in versoes and versoes[usuario_id] == versao_cracha:
        return usuario_id
    return None


def sair(usuario_id, versoes):
    versoes[usuario_id] += 1