import time
import json

from datetime import datetime
from market_data import obtener_precio
from strategy import calcular_medias, señal_trading
from risk_manager import stop_loss
from trader import Trader
from logger import guardar_operacion
from telegram_bot import enviar_mensaje
from volume_filter import obtener_volumen, volumen_fuerte
from indicators import calcular_rsi
from market_scanner import obtener_top_cripto
from realtime_price import iniciar_socket

iniciar_socket("btcusdt")


# obtener criptos más activas
pares = obtener_top_cripto()

print("TOP MERCADOS:", pares)


# guardar historial de precios
precios = {}

for par in pares:
    precios[par] = []


bot = Trader()

print("🚀 BOT SCANNER INICIADO")

def guardar_operacion(tipo, precio):

    try:
        with open("operaciones.json", "r") as f:
            operaciones = json.load(f)
    except:
        operaciones = []

    nueva = {
        "tipo": tipo,
        "precio": precio,
        "hora": datetime.now().strftime("%H:%M:%S")
    }

    operaciones.append(nueva)

    with open("operaciones.json", "w") as f:
        json.dump(operaciones, f, indent=4)


# ejemplo de bot
while True:

    precio = 65000  # ejemplo

    decision = "comprar"  # ejemplo

    if decision == "comprar":
        print("Comprando en", precio)
        guardar_operacion("compra", precio)

    elif decision == "vender":
        print("Vendiendo en", precio)
        guardar_operacion("venta", precio)

    time.sleep(10)


while True:

    for par in pares:

        precio = obtener_precio(par)

        if precio is None:
            continue


        # filtro de volumen
        volumen = obtener_volumen(par)

        if not volumen_fuerte(volumen):
            print(par, "volumen bajo")
            continue


        precios[par].append(precio)

        if len(precios[par]) > 100:
            precios[par].pop(0)


        print("\n", par, "precio:", precio)
        print("Dinero:", bot.dinero)
        print("Portfolio:", bot.portfolio)


        if len(precios[par]) >= 15:

            media_corta, media_larga = calcular_medias(precios[par])

            señal = señal_trading(media_corta, media_larga)

            rsi = calcular_rsi(precios[par])

            print("RSI:", rsi)


            # COMPRA
            if (
                señal == "COMPRA"
                and rsi is not None
                and rsi < 30
                and bot.dinero > 0
            ):

                bot.comprar(par, precio)

                guardar_operacion(f"COMPRA {par}", precio)

                enviar_mensaje(
                    f"🟢 COMPRA {par}\nPrecio: {precio}\nRSI: {rsi}"
                )


            # VENTA
            elif (
                señal == "VENTA"
                and rsi is not None
                and rsi > 70
                and bot.portfolio[par] > 0
            ):

                bot.vender(par, precio)

                guardar_operacion(f"VENTA {par}", precio)

                enviar_mensaje(
                    f"🔴 VENTA {par}\nPrecio: {precio}\nRSI: {rsi}"
                )


            # STOP LOSS
            if par in bot.precio_compra:

                if (
                    bot.portfolio[par] > 0
                    and stop_loss(precio, bot.precio_compra[par])
                ):

                    bot.vender(par, precio)

                    guardar_operacion(f"STOPLOSS {par}", precio)

                    enviar_mensaje(
                        f"⚠️ STOP LOSS {par}\nPrecio: {precio}"
                    )


    time.sleep(5)