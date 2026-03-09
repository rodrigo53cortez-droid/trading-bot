import json
import websocket

precios = {}

def on_message(ws, message):

    data = json.loads(message)

    simbolo = data["s"]
    precio = float(data["c"])

    precios[simbolo] = precio

    print(simbolo, precio)


def iniciar_socket(par):

    socket = f"wss://stream.binance.com:9443/ws/{par.lower()}@ticker"

    ws = websocket.WebSocketApp(
        socket,
        on_message=on_message
    )

    ws.run_forever()