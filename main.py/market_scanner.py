import requests


def obtener_top_cripto():

    url = "https://api.binance.com/api/v3/ticker/24hr"

    try:

        data = requests.get(url).json()

        usdt_pairs = []

        for coin in data:

            if "USDT" in coin["symbol"]:

                usdt_pairs.append({
                    "symbol": coin["symbol"],
                    "volume": float(coin["quoteVolume"])
                })

        usdt_pairs.sort(key=lambda x: x["volume"], reverse=True)

        top = [coin["symbol"] for coin in usdt_pairs[:10]]

        return top

    except:

        return []