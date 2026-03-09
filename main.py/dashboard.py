from flask import Flask, render_template, jsonify
import requests
import subprocess
import json

app = Flask(__name__)

bot_proceso = None

def calcular_ganancia():

    try:
        with open("operaciones.json") as f:
            operaciones = json.load(f)
    except:
        return 0

    ganancia = 0
    ultima_compra = None

    for op in operaciones:

        if op["tipo"] == "compra":
            ultima_compra = op["precio"]

        if op["tipo"] == "venta" and ultima_compra:
            ganancia += op["precio"] - ultima_compra
            ultima_compra = None

    return round(ganancia,2)


def obtener_precios():

    url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=50"

    data = requests.get(url).json()

    precios = []
    tiempos = []

    for vela in data:
        precios.append(float(vela[4]))
        tiempos.append(vela[0])

    return tiempos, precios


@app.route("/")
def home():

    tiempos, precios = obtener_precios()

    estado = bot_proceso is not None

    return render_template(
        "index.html",
        tiempos=tiempos,
        precios=precios,
        estado=estado
    )


@app.route("/data")
def data():

    tiempos, precios = obtener_precios()

    try:
        with open("operaciones.json") as f:
            operaciones = json.load(f)
    except:
        operaciones = []

    return jsonify({
        "tiempos": tiempos,
        "precios": precios,
        "operaciones": operaciones
    })


@app.route("/start")
def start_bot():

    global bot_proceso

    if bot_proceso is None:
        bot_proceso = subprocess.Popen(["python", "main.py"])

    return jsonify({"estado": "bot iniciado"})


@app.route("/stop")
def stop_bot():

    global bot_proceso

    if bot_proceso is not None:
        bot_proceso.terminate()
        bot_proceso = None

    return jsonify({"estado": "bot detenido"})


@app.route("/operaciones")
def operaciones():

    try:
        with open("operaciones.json") as f:
            data = json.load(f)
    except:
        data = []

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)

@app.route("/ganancia")
def ganancia():

    g = calcular_ganancia()

    return jsonify({
        "ganancia": g
    })
    