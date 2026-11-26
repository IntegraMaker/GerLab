def excluir(pc, autor, quando):
    pc["excluido_em"] = quando
    pc["excluido_por"] = autor


def listar(pcs, incluir_excluidos=False):
    if incluir_excluidos:
        return list(pcs)
    return [pc for pc in pcs if pc["excluido_em"] is None]