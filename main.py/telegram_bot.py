import requests

TOKEN = "8760572133:AAFCXcliDBJjkBMZ0OOILdGxaGWVjZwkBfE"
CHAT_ID = "6598225589"

def enviar_mensaje(texto):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    datos = {
        "chat_id": CHAT_ID,
        "text": texto
    }

    requests.post(url, data=datos)