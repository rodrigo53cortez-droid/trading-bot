class Trader:

    def __init__(self):

        self.dinero = 1000

        self.portfolio = {
            "BTCUSDT": 0,
            "ETHUSDT": 0,
            "BNBUSDT": 0,
            "SOLUSDT": 0,
            "XRPUSDT": 0,
            "ADAUSDT": 0
        }

        self.precio_compra = {}


    def comprar(self, par, precio):

        if self.dinero <= 0:
            return

        cantidad = self.dinero / precio

        self.portfolio[par] += cantidad

        self.precio_compra[par] = precio

        self.dinero = 0

        print(f"🟢 Comprado {par} a {precio}")


    def vender(self, par, precio):

        cantidad = self.portfolio[par]

        if cantidad <= 0:
            return

        self.dinero = cantidad * precio

        self.portfolio[par] = 0

        print(f"🔴 Vendido {par} a {precio}")