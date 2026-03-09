import requests

def obtener_volumen(par):

    url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={par}"

    try:
        data = requests.get(url).json()
        volumen = float(data["quoteVolume"])
        return volumen

    except:
        return None


def volumen_fuerte(volumen):

    if volumen is None:
        return False

    # mínimo 50 millones
    if volumen > 50000000:
        return True

    return False