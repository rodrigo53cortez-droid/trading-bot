from datetime import datetime

def guardar_operacion(tipo, precio):

    with open("trading_log.txt", "a") as archivo:

        tiempo = datetime.now()

        archivo.write(f"{tiempo} {tipo} {precio}\n")