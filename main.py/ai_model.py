import requests
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def obtener_datos(par="BTCUSDT", limite=1000):

    url = f"https://api.binance.com/api/v3/klines?symbol={par}&interval=1h&limit={limite}"

    data = requests.get(url).json()

    precios = []

    for vela in data:
        precios.append(float(vela[4]))

    return precios


def crear_dataset(precios):

    datos = []

    for i in range(10, len(precios)-1):

        precio = precios[i]

        media_corta = sum(precios[i-5:i]) / 5
        media_larga = sum(precios[i-10:i]) / 10

        cambio = precios[i] - precios[i-1]

        futuro = 1 if precios[i+1] > precios[i] else 0

        datos.append([
            precio,
            media_corta,
            media_larga,
            cambio,
            futuro
        ])

    df = pd.DataFrame(datos, columns=[
        "precio",
        "media_corta",
        "media_larga",
        "cambio",
        "target"
    ])

    return df


def entrenar_modelo():

    precios = obtener_datos()

    df = crear_dataset(precios)

    X = df[["precio", "media_corta", "media_larga", "cambio"]]
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2
    )

    modelo = RandomForestClassifier()

    modelo.fit(X_train, y_train)

    pred = modelo.predict(X_test)

    precision = accuracy_score(y_test, pred)

    print("Precisión del modelo:", precision)

    return modelo


if __name__ == "__main__":

    entrenar_modelo()