import requests
from indicators import calcular_rsi


def obtener_datos(par="BTCUSDT", limite=500):

    url = f"https://api.binance.com/api/v3/klines?symbol={par}&interval=1h&limit={limite}"

    data = requests.get(url).json()

    precios = []

    for vela in data:
        precios.append(float(vela[4]))

    return precios


def media(lista, periodo):

    return sum(lista[-periodo:]) / periodo


def probar_estrategia(precios, corta, larga):

    dinero = 1000
    btc = 0

    for i in range(larga, len(precios)):

        ventana = precios[:i]

        precio = ventana[-1]

        media_corta = media(ventana, corta)
        media_larga = media(ventana, larga)

        rsi = calcular_rsi(ventana)

        if media_corta > media_larga and rsi and rsi < 30 and dinero > 0:

            btc = dinero / precio
            dinero = 0

        elif media_corta < media_larga and rsi and rsi > 70 and btc > 0:

            dinero = btc * precio
            btc = 0

    return dinero + btc * precios[-1]


def optimizar():

    precios = obtener_datos()

    mejor_resultado = 0
    mejor_config = None

    for corta in range(5, 20):

        for larga in range(20, 80):

            if corta >= larga:
                continue

            resultado = probar_estrategia(precios, corta, larga)

            if resultado > mejor_resultado:

                mejor_resultado = resultado
                mejor_config = (corta, larga)

                print("Nueva mejor estrategia:", mejor_config, mejor_resultado)

    print("\nMEJOR CONFIGURACIÓN:")
    print("Media corta:", mejor_config[0])
    print("Media larga:", mejor_config[1])
    print("Capital final:", mejor_resultado)


if __name__ == "__main__":
    optimizar()