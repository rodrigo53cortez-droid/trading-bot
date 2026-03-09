def calcular_medias(precios):

    media_corta = sum(precios[-5:]) / 5
    media_larga = sum(precios[-10:]) / 10

    return media_corta, media_larga


def señal_trading(media_corta, media_larga):

    if media_corta > media_larga:
        return "COMPRA"

    elif media_corta < media_larga:
        return "VENTA"

    return "NADA"