def stop_loss(precio_actual, precio_compra):

    if precio_actual < precio_compra * 0.98:
        return True

    return False