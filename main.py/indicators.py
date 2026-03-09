def calcular_rsi(precios, periodo=14):

    if len(precios) < periodo + 1:
        return None

    ganancias = []
    perdidas = []

    for i in range(-periodo, 0):

        cambio = precios[i] - precios[i-1]

        if cambio > 0:
            ganancias.append(cambio)
            perdidas.append(0)
        else:
            ganancias.append(0)
            perdidas.append(abs(cambio))

    promedio_ganancia = sum(ganancias) / periodo
    promedio_perdida = sum(perdidas) / periodo

    if promedio_perdida == 0:
        return 100

    rs = promedio_ganancia / promedio_perdida

    rsi = 100 - (100 / (1 + rs))

    return rsi