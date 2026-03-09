import requests

def obtener_precio(par):

    url = f"https://api.binance.com/api/v3/ticker/price?symbol={par}"

    try:

        respuesta = requests.get(url, timeout=10)
        data = respuesta.json()

        return float(data["price"])

    except Exception as e:

        print("⚠️ Error conectando con Binance:", e)
        return None