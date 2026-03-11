class Cola:
    def __init__(self):
        self.elementos = []
    
    def encolar(self, elemento):
        self.elementos.append(elemento)
    
    def desencolar(self):
        if not self.esta_vacia():
            return self.elementos.pop(0)
        return None
    
    def esta_vacia(self):
        return len(self.elementos) == 0
    
    def ver_primero(self):
        if not self.esta_vacia():
            return self.elementos[0]
        return None
    
    def tamano(self):
        return len(self.elementos)
    
    def mostrar(self, nombre):
        """Muestra el contenido de la cola de forma legible"""
        print(f"{nombre}: ", end="")
        if self.esta_vacia():
            print("Vacía")
        else:
            print(" -> ".join(str(elem) for elem in self.elementos))

def sumar_colas(cola_a, cola_b):
    """
    Recibe dos colas con números enteros y devuelve una nueva cola
    con la suma de sus elementos uno a uno.
    """
    cola_resultado = Cola()
    
    # Creamos copias de las colas originales para no modificarlas
    copia_a = Cola()
    copia_b = Cola()
    
    # Hacemos copias de las colas originales
    while not cola_a.esta_vacia():
        elemento = cola_a.desencolar()
        copia_a.encolar(elemento)
    
    while not cola_b.esta_vacia():
        elemento = cola_b.desencolar()
        copia_b.encolar(elemento)
    
    # Sumamos elementos mientras ambas colas tengan elementos
    while not copia_a.esta_vacia() and not copia_b.esta_vacia():
        suma = copia_a.desencolar() + copia_b.desencolar()
        cola_resultado.encolar(suma)
    
    # Si una cola tiene más elementos que la otra, los agregamos tal cual
    while not copia_a.esta_vacia():
        cola_resultado.encolar(copia_a.desencolar())
    
    while not copia_b.esta_vacia():
        cola_resultado.encolar(copia_b.desencolar())
    
    return cola_resultado

def llenar_colas_manual(cola_a, cola_b, tamaño):
    """Permite al usuario llenar las colas manualmente"""
    print(f"\n--- LLENADO MANUAL DE COLAS ---")
    print(f"Las colas tendrán {tamaño} elementos cada una")
    
    print(f"\nLlenando Cola A:")
    for i in range(tamaño):
        while True:
            try:
                valor = int(input(f"Ingrese el elemento {i+1} para Cola A: "))
                cola_a.encolar(valor)
                break
            except ValueError:
                print("Error: Ingrese un número entero válido")
    
    print(f"\nLlenando Cola B:")
    for i in range(tamaño):
        while True:
            try:
                valor = int(input(f"Ingrese el elemento {i+1} para Cola B: "))
                cola_b.encolar(valor)
                break
            except ValueError:
                print("Error: Ingrese un número entero válido")

def llenar_colas_automatico(cola_a, cola_b, tamaño):
    """Llena las colas automáticamente con números aleatorios"""
    import random
    
    print(f"\n--- LLENADO AUTOMÁTICO DE COLAS ---")
    print(f"Generando {tamaño} elementos aleatorios para cada cola...")
    
    for i in range(tamaño):
        cola_a.encolar(random.randint(1, 20))
        cola_b.encolar(random.randint(1, 20))

def main():
    print("=" * 50)
    print("PROGRAMA PARA SUMAR DOS COLAS")
    print("=" * 50)
    
    # Solicitar tamaño de las colas
    while True:
        try:
            tamaño = int(input("\n¿De qué tamaño desea las colas? (1-15): "))
            if 1 <= tamaño <= 15:
                break
            else:
                print("Error: El tamaño debe estar entre 1 y 15")
        except ValueError:
            print("Error: Ingrese un número válido")
    
    # Solicitar método de llenado
    print("\n--- MÉTODO DE LLENADO ---")
    print("1. Llenado manual (usted ingresa los números)")
    print("2. Llenado automático (números aleatorios)")
    
    while True:
        try:
            opcion = int(input("Seleccione una opción (1-2): "))
            if opcion in [1, 2]:
                break
            else:
                print("Error: Seleccione 1 o 2")
        except ValueError:
            print("Error: Ingrese un número válido")
    
    # Crear las colas
    cola_a = Cola()
    cola_b = Cola()
    
    # Llenar las colas según la opción elegida
    if opcion == 1:
        llenar_colas_manual(cola_a, cola_b, tamaño)
    else:
        llenar_colas_automatico(cola_a, cola_b, tamaño)
    
    # Mostrar las colas originales
    print("\n" + "=" * 50)
    print("COLAS ORIGINALES")
    print("=" * 50)
    cola_a.mostrar("Cola A")
    cola_b.mostrar("Cola B")
    
    # Sumar las colas (creando copias para no perder las originales)
    # Hacemos copias de las colas originales para la suma
    copia_a = Cola()
    copia_b = Cola()
    
    # Copiamos los elementos
    elementos_a = []
    elementos_b = []
    
    while not cola_a.esta_vacia():
        elem = cola_a.desencolar()
        elementos_a.append(elem)
        copia_a.encolar(elem)
    
    while not cola_b.esta_vacia():
        elem = cola_b.desencolar()
        elementos_b.append(elem)
        copia_b.encolar(elem)
    
    # Restauramos las colas originales
    for elem in elementos_a:
        cola_a.encolar(elem)
    
    for elem in elementos_b:
        cola_b.encolar(elem)
    
    # Realizamos la suma con las copias
    cola_resultado = sumar_colas(copia_a, copia_b)
    
    # Mostrar el resultado
    print("\n" + "=" * 50)
    print("RESULTADO DE LA SUMA")
    print("=" * 50)
    cola_resultado.mostrar("Cola Resultado")
    
    # Mostrar tabla comparativa
    print("\n" + "=" * 50)
    print("TABLA COMPARATIVA")
    print("=" * 50)
    print("Posición | Cola A | Cola B | Resultado")
    print("-" * 40)
    
    # Restauramos las colas para la tabla
    elementos_a = []
    elementos_b = []
    
    while not cola_a.esta_vacia():
        elementos_a.append(cola_a.desencolar())
    while not cola_b.esta_vacia():
        elementos_b.append(cola_b.desencolar())
    
    elementos_resultado = []
    while not cola_resultado.esta_vacia():
        elementos_resultado.append(cola_resultado.desencolar())
    
    for i in range(tamaño):
        a = elementos_a[i] if i < len(elementos_a) else "-"
        b = elementos_b[i] if i < len(elementos_b) else "-"
        r = elementos_resultado[i] if i < len(elementos_resultado) else "-"
        print(f"    {i+1}     |  {a:3}  |  {b:3}  |    {r:3}")
    
    print("\n¡Programa finalizado!")

if __name__ == "__main__":
    main()