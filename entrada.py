def pedir_numero(mensaje):                      # 1. nombre nuevo, y recibe "mensaje"
    while True:
        try:
            numero = float(input(mensaje))      # 2. pregunta lo que diga "mensaje"
            return numero                       # 3. "numero" en vez de "edad"
        except ValueError:
            print("Eso no es un número, prueba otra vez")