class Pila:
    def __init__(self, nombre):
        self.items = []
        self.nombre = nombre
    
    def esta_vacia(self):
        return len(self.items) == 0
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.esta_vacia():
            return self.items.pop()
        return None
    
    def top(self):
        if not self.esta_vacia():
            return self.items[-1]
        return None
    
    def __str__(self):
        return f"Torre {self.nombre}: {self.items}"


class TorresDeHanoi:
    def __init__(self, num_discos):
        self.num_discos = num_discos
        self.torre_origen = Pila('A')  
        self.torre_auxiliar = Pila('B')  
        self.torre_destino = Pila('C')  
        self.movimientos = 0
        
        for i in range(num_discos, 0, -1):
            self.torre_origen.push(i)
    
    def mover_disco(self, origen, destino):
        """Mueve un disco de una torre a otra"""
        disco = origen.pop()
        destino.push(disco)
        self.movimientos += 1
        print(f"Movimiento {self.movimientos}: Mover disco {disco} de Torre {origen.nombre} a Torre {destino.nombre}")
        self.mostrar_torres()
    
    def mostrar_torres(self):
        """Muestra el estado actual de las torres"""
        print(self.torre_origen)
        print(self.torre_auxiliar)
        print(self.torre_destino)
        print("-" * 40)
    
    def resolver_hanoi(self, n, origen, destino, auxiliar):
        """
        Resuelve las Torres de Hanoi recursivamente
        n: número de discos a mover
        origen: torre de origen
        destino: torre de destino
        auxiliar: torre auxiliar
        """
        if n == 1:
            # Caso base: mover un solo disco
            self.mover_disco(origen, destino)
        else:
            # Paso 1: Mover n-1 discos de origen a auxiliar
            self.resolver_hanoi(n - 1, origen, auxiliar, destino)
            
            # Paso 2: Mover el disco más grande de origen a destino
            self.mover_disco(origen, destino)
            
            # Paso 3: Mover n-1 discos de auxiliar a destino
            self.resolver_hanoi(n - 1, auxiliar, destino, origen)
    
    def jugar(self):
        """Inicia el juego de las Torres de Hanoi"""
        print(f"\n=== TORRES DE HANOI - {self.num_discos} DISCOS ===")
        print("Estado inicial:")
        self.mostrar_torres()
        
        # Resolver el puzzle
        self.resolver_hanoi(self.num_discos, self.torre_origen, self.torre_destino, self.torre_auxiliar)
        
        print(f"\n¡Juego completado en {self.movimientos} movimientos!")
        print(f"Número mínimo teórico: {2**self.num_discos - 1} movimientos")


# Versión interactiva para que el usuario pueda jugar
class TorresDeHanoiInteractivo:
    def __init__(self, num_discos):
        self.num_discos = num_discos
        self.torre_origen = Pila('A')
        self.torre_auxiliar = Pila('B')
        self.torre_destino = Pila('C')
        self.movimientos = 0
        
        # Inicializar la torre de origen con los discos
        for i in range(num_discos, 0, -1):
            self.torre_origen.push(i)
    
    def obtener_torre(self, letra):
        """Obtiene la torre correspondiente a la letra"""
        if letra.upper() == 'A':
            return self.torre_origen
        elif letra.upper() == 'B':
            return self.torre_auxiliar
        elif letra.upper() == 'C':
            return self.torre_destino
        return None
    
    def movimiento_valido(self, origen, destino):
        """Verifica si un movimiento es válido"""
        if origen.esta_vacia():
            print("❌ La torre de origen está vacía")
            return False
        
        if not destino.esta_vacia() and origen.top() > destino.top():
            print(f"❌ No se puede colocar un disco {origen.top()} sobre uno más pequeño {destino.top()}")
            return False
        
        return True
    
    def juego_completado(self):
        """Verifica si el juego está completado"""
        return len(self.torre_destino.items) == self.num_discos
    
    def mostrar_torres(self):
        """Muestra el estado actual de las torres"""
        print(self.torre_origen)
        print(self.torre_auxiliar)
        print(self.torre_destino)
        print("-" * 40)


# Programa principal
if __name__ == "__main__":
    print("=== TORRES DE HANOI ===")
    print("1. Ver solución automática (3 discos)")
    
    opcion = input("Elige una opción (1): ").strip()
    
    if opcion == "1":
        # Solución automática para 3 discos
        juego = TorresDeHanoi(3)
        juego.jugar()
    elif opcion == '3':
        print("\n¡Hasta luego!")
                
    else:
     print("\n❌ Opción no válida. Intente nuevamente.")
            
    input("\nPresione Enter para continuar...")
