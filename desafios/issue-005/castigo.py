def esta_de_castigo(falhas, agora):
    if len(falhas) < 5:
        return False

    cinco_recentes = falhas[-5:]
    mais_antiga = cinco_recentes[0]
    mais_nova = cinco_recentes[-1]

    intervalo_curto = mais_nova - mais_antiga <= 15
    castigo_nao_terminou = agora < mais_nova + 15

    return intervalo_curto and castigo_nao_terminou