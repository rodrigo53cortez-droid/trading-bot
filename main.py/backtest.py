import requests

from strategy import calcular_medias, señal_trading
from indicators import calcular_rsi


def obtener_datos(par="BTCUSDT", limite=500):

    url = f"https://api.binance.com/api/v3/klines?symbol={par}&interval=1h&limit={limite}"

    data = requests.get(url).json()

    precios = []

    for vela in data:
        cierre = float(vela[4])
        precios.append(cierre)

    return precios


def ejecutar_backtest():

    precios = obtener_datos()

    dinero = 1000
    btc = 0

    historial = []

    for i in range(20, len(precios)):

        ventana = precios[:i]

        precio = ventana[-1]

        media_corta, media_larga = calcular_medias(ventana)

        señal = señal_trading(media_corta, media_larga)

        rsi = calcular_rsi(ventana)

        # COMPRA
        if señal == "COMPRA" and rsi and rsi < 30 and dinero > 0:

            btc = dinero / precio
            dinero = 0

            print("COMPRA", precio)

        # VENTA
        elif señal == "VENTA" and rsi and rsi > 70 and btc > 0:

            dinero = btc * precio
            btc = 0

            print("VENTA", precio)

        valor_total = dinero + btc * precio

        historial.append(valor_total)

    print("RESULTADO FINAL:", historial[-1])


if __name__ == "__main__":
    ejecutar_backtest()