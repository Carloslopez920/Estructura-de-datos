class Nodo:
    """Clase Nodo que representa un elemento individual en la lista enlazada"""
    
    def __init__(self, datos):
        """
        Inicializa un nuevo nodo
        
        Args:
            datos: Los datos que se almacenarán en el nodo
        """
        self.datos = datos
        self.siguiente = None
    
    def __str__(self):
        """Representación en cadena del nodo"""
        return str(self.datos)


class MiListaEnlazada:
    """
    Una implementación personalizada de una Lista Enlazada Simple
    Soporta operaciones comunes como agregar, eliminar, buscar e iterar
    """
    
    def __init__(self):
        """Inicializa una lista enlazada vacía"""
        self.cabeza = None
        self._tamano = 0
    
    def agregar_al_inicio(self, datos):
        """
        Agrega un nuevo nodo al principio de la lista
        
        Args:
            datos: Los datos que se agregarán
        """
        nuevo_nodo = Nodo(datos)
        nuevo_nodo.siguiente = self.cabeza
        self.cabeza = nuevo_nodo
        self._tamano += 1
        print(f"✓ Elemento '{datos}' agregado al inicio correctamente")
    
    def agregar_al_final(self, datos):
        """
        Agrega un nuevo nodo al final de la lista
        
        Args:
            datos: Los datos que se agregarán
        """
        nuevo_nodo = Nodo(datos)
        
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        
        self._tamano += 1
        print(f"✓ Elemento '{datos}' agregado al final correctamente")
    
    def agregar_en(self, indice, datos):
        """
        Agrega un nuevo nodo en el índice especificado
        
        Args:
            indice: Posición donde insertar (base 0)
            datos: Los datos que se agregarán
            
        Returns:
            bool: True si se agregó correctamente, False en caso contrario
        """
        if indice < 0 or indice > self._tamano:
            print(f"✗ Error: Índice {indice} fuera de los límites (0-{self._tamano})")
            return False
        
        if indice == 0:
            self.agregar_al_inicio(datos)
        elif indice == self._tamano:
            self.agregar_al_final(datos)
        else:
            nuevo_nodo = Nodo(datos)
            actual = self.cabeza
            for _ in range(indice - 1):
                actual = actual.siguiente
            nuevo_nodo.siguiente = actual.siguiente
            actual.siguiente = nuevo_nodo
            self._tamano += 1
            print(f"✓ Elemento '{datos}' agregado en la posición {indice} correctamente")
        
        return True
    
    def eliminar_primero(self):
        """
        Elimina y devuelve el primer elemento de la lista
        
        Returns:
            Los datos eliminados o None si la lista está vacía
        """
        if self.esta_vacia():
            print("✗ Error: No se puede eliminar de una lista vacía")
            return None
        
        datos_eliminados = self.cabeza.datos
        self.cabeza = self.cabeza.siguiente
        self._tamano -= 1
        print(f"✓ Elemento '{datos_eliminados}' eliminado del inicio correctamente")
        return datos_eliminados
    
    def eliminar_ultimo(self):
        """
        Elimina y devuelve el último elemento de la lista
        
        Returns:
            Los datos eliminados o None si la lista está vacía
        """
        if self.esta_vacia():
            print("✗ Error: No se puede eliminar de una lista vacía")
            return None
        
        if self._tamano == 1:
            return self.eliminar_primero()
        
        actual = self.cabeza
        while actual.siguiente.siguiente:
            actual = actual.siguiente
        
        datos_eliminados = actual.siguiente.datos
        actual.siguiente = None
        self._tamano -= 1
        print(f"✓ Elemento '{datos_eliminados}' eliminado del final correctamente")
        return datos_eliminados
    
    def eliminar_en(self, indice):
        """
        Elimina y devuelve el elemento en el índice especificado
        
        Args:
            indice: Posición del elemento a eliminar (base 0)
        
        Returns:
            Los datos eliminados o None si el índice está fuera de límites
        """
        if indice < 0 or indice >= self._tamano:
            print(f"✗ Error: Índice {indice} fuera de los límites (0-{self._tamano-1})")
            return None
        
        if indice == 0:
            return self.eliminar_primero()
        
        actual = self.cabeza
        for _ in range(indice - 1):
            actual = actual.siguiente
        
        datos_eliminados = actual.siguiente.datos
        actual.siguiente = actual.siguiente.siguiente
        self._tamano -= 1
        print(f"✓ Elemento '{datos_eliminados}' eliminado de la posición {indice} correctamente")
        return datos_eliminados
    
    def eliminar_por_valor(self, valor):
        """
        Elimina la primera ocurrencia del valor especificado
        
        Args:
            valor: El valor a eliminar
        
        Returns:
            bool: True si el valor fue encontrado y eliminado, False en caso contrario
        """
        if self.esta_vacia():
            print("✗ Error: La lista está vacía")
            return False
        
        if self.cabeza.datos == valor:
            self.eliminar_primero()
            return True
        
        actual = self.cabeza
        while actual.siguiente:
            if actual.siguiente.datos == valor:
                actual.siguiente = actual.siguiente.siguiente
                self._tamano -= 1
                print(f"✓ Elemento '{valor}' eliminado correctamente")
                return True
            actual = actual.siguiente
        
        print(f"✗ Error: No se encontró el elemento '{valor}' en la lista")
        return False
    
    def modificar(self, indice, nuevo_valor):
        """
        Modifica el valor en el índice especificado
        
        Args:
            indice: Posición del elemento a modificar
            nuevo_valor: Nuevo valor para el elemento
        
        Returns:
            bool: True si se modificó correctamente, False en caso contrario
        """
        if indice < 0 or indice >= self._tamano:
            print(f"✗ Error: Índice {indice} fuera de los límites (0-{self._tamano-1})")
            return False
        
        actual = self.cabeza
        for _ in range(indice):
            actual = actual.siguiente
        
        valor_anterior = actual.datos
        actual.datos = nuevo_valor
        print(f"✓ Elemento en posición {indice} modificado: '{valor_anterior}' → '{nuevo_valor}'")
        return True
    
    def modificar_por_valor(self, valor_buscar, nuevo_valor):
        """
        Modifica la primera ocurrencia del valor especificado
        
        Args:
            valor_buscar: Valor a buscar
            nuevo_valor: Nuevo valor para reemplazar
        
        Returns:
            bool: True si se modificó correctamente, False en caso contrario
        """
        if self.esta_vacia():
            print("✗ Error: La lista está vacía")
            return False
        
        actual = self.cabeza
        indice = 0
        while actual:
            if actual.datos == valor_buscar:
                actual.datos = nuevo_valor
                print(f"✓ Elemento '{valor_buscar}' modificado a '{nuevo_valor}' en posición {indice}")
                return True
            actual = actual.siguiente
            indice += 1
        
        print(f"✗ Error: No se encontró el elemento '{valor_buscar}' en la lista")
        return False
    
    def obtener(self, indice):
        """
        Obtiene el elemento en el índice especificado sin eliminarlo
        
        Args:
            indice: Posición del elemento a obtener (base 0)
        
        Returns:
            Los datos en el índice especificado o None si no existe
        """
        if indice < 0 or indice >= self._tamano:
            print(f"✗ Error: Índice {indice} fuera de los límites (0-{self._tamano-1})")
            return None
        
        actual = self.cabeza
        for _ in range(indice):
            actual = actual.siguiente
        
        return actual.datos
    
    def indice_de(self, valor):
        """
        Encuentra el índice de la primera ocurrencia de un valor
        
        Args:
            valor: El valor a buscar
        
        Returns:
            int: El índice del valor, o -1 si no se encuentra
        """
        actual = self.cabeza
        indice = 0
        
        while actual:
            if actual.datos == valor:
                return indice
            actual = actual.siguiente
            indice += 1
        
        return -1
    
    def contiene(self, valor):
        """
        Verifica si la lista contiene un valor específico
        
        Args:
            valor: El valor a buscar
        
        Returns:
            bool: True si el valor existe, False en caso contrario
        """
        return self.indice_de(valor) != -1
    
    def esta_vacia(self):
        """
        Verifica si la lista está vacía
        
        Returns:
            bool: True si la lista está vacía, False en caso contrario
        """
        return self.cabeza is None
    
    def tamano(self):
        """
        Obtiene el número de elementos en la lista
        
        Returns:
            int: El tamaño de la lista
        """
        return self._tamano
    
    def limpiar(self):
        """Elimina todos los elementos de la lista"""
        self.cabeza = None
        self._tamano = 0
        print("✓ Lista limpiada completamente")
    
    def invertir(self):
        """
        Invierte la lista enlazada in-place
        """
        if self.esta_vacia():
            print("✗ Error: No se puede invertir una lista vacía")
            return
        
        anterior = None
        actual = self.cabeza
        
        while actual:
            siguiente_nodo = actual.siguiente
            actual.siguiente = anterior
            anterior = actual
            actual = siguiente_nodo
        
        self.cabeza = anterior
        print("✓ Lista invertida correctamente")
    
    def mostrar(self):
        """Muestra la lista de forma visual"""
        if self.esta_vacia():
            print("📋 Lista: [vacía]")
            return
        
        elementos = []
        actual = self.cabeza
        while actual:
            elementos.append(str(actual.datos))
            actual = actual.siguiente
        
        print("📋 Lista: " + " → ".join(elementos))
        print(f"   Tamaño: {self._tamano} elementos")
    
    def mostrar_detallada(self):
        """Muestra la lista con índices"""
        if self.esta_vacia():
            print("📋 Lista: [vacía]")
            return
        
        print("\n" + "="*50)
        print("LISTA DETALLADA")
        print("="*50)
        
        actual = self.cabeza
        indice = 0
        while actual:
            print(f"  Índice {indice}: {actual.datos}")
            actual = actual.siguiente
            indice += 1
        
        print(f"\nTotal: {self._tamano} elementos")
        print("="*50 + "\n")
    
    def a_lista(self):
        """
        Convierte la lista enlazada a una lista de Python
        
        Returns:
            list: Una lista de Python que contiene todos los elementos
        """
        resultado = []
        actual = self.cabeza
        while actual:
            resultado.append(actual.datos)
            actual = actual.siguiente
        return resultado
    
    def __len__(self):
        """Soporte para la función len()"""
        return self._tamano
    
    def __iter__(self):
        """Hace que la lista sea iterable"""
        self._iter_actual = self.cabeza
        return self
    
    def __next__(self):
        """Obtiene el siguiente elemento al iterar"""
        if self._iter_actual is None:
            raise StopIteration
        datos = self._iter_actual.datos
        self._iter_actual = self._iter_actual.siguiente
        return datos
    
    def __str__(self):
        """Representación en cadena de la lista enlazada"""
        if self.esta_vacia():
            return "MiListaEnlazada[]"
        
        elementos = []
        actual = self.cabeza
        while actual:
            elementos.append(str(actual.datos))
            actual = actual.siguiente
        
        return "MiListaEnlazada[" + " -> ".join(elementos) + "]"


class MenuInteractivo:
    """Clase para manejar la interfaz de usuario interactiva"""
    
    def __init__(self):
        """Inicializa el menú interactivo"""
        self.lista = MiListaEnlazada()
    
    def mostrar_menu(self):
        """Muestra el menú principal"""
        print("\n" + "="*50)
        print("   SISTEMA DE GESTIÓN DE LISTA ENLAZADA")
        print("="*50)
        print("1. Agregar elemento")
        print("2. Eliminar elemento")
        print("3. Modificar elemento")
        print("4. Buscar elemento")
        print("5. Ver lista")
        print("6. Invertir lista")
        print("7. Limpiar lista")
        print("8. Información detallada")
        print("9. Ejemplos de prueba")
        print("0. Salir")
        print("="*50)
    
    def submenu_agregar(self):
        """Submenú para agregar elementos"""
        while True:
            print("\n--- AGREGAR ELEMENTO ---")
            print("1. Agregar al inicio")
            print("2. Agregar al final")
            print("3. Agregar en posición específica")
            print("4. Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                valor = input("Ingrese el valor a agregar: ")
                self.lista.agregar_al_inicio(valor)
                self.lista.mostrar()
            elif opcion == "2":
                valor = input("Ingrese el valor a agregar: ")
                self.lista.agregar_al_final(valor)
                self.lista.mostrar()
            elif opcion == "3":
                try:
                    indice = int(input("Ingrese la posición (índice): "))
                    valor = input("Ingrese el valor a agregar: ")
                    self.lista.agregar_en(indice, valor)
                    self.lista.mostrar()
                except ValueError:
                    print("✗ Error: Ingrese un número válido")
            elif opcion == "4":
                break
            else:
                print("✗ Opción inválida")
    
    def submenu_eliminar(self):
        """Submenú para eliminar elementos"""
        if self.lista.esta_vacia():
            print("✗ La lista está vacía, no hay elementos para eliminar")
            return
        
        while True:
            print("\n--- ELIMINAR ELEMENTO ---")
            self.lista.mostrar()
            print("\n1. Eliminar primero")
            print("2. Eliminar último")
            print("3. Eliminar por posición")
            print("4. Eliminar por valor")
            print("5. Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                self.lista.eliminar_primero()
                self.lista.mostrar()
            elif opcion == "2":
                self.lista.eliminar_ultimo()
                self.lista.mostrar()
            elif opcion == "3":
                try:
                    indice = int(input("Ingrese la posición a eliminar: "))
                    self.lista.eliminar_en(indice)
                    self.lista.mostrar()
                except ValueError:
                    print("✗ Error: Ingrese un número válido")
            elif opcion == "4":
                valor = input("Ingrese el valor a eliminar: ")
                self.lista.eliminar_por_valor(valor)
                self.lista.mostrar()
            elif opcion == "5":
                break
            else:
                print("✗ Opción inválida")
    
    def submenu_modificar(self):
        """Submenú para modificar elementos"""
        if self.lista.esta_vacia():
            print("✗ La lista está vacía, no hay elementos para modificar")
            return
        
        while True:
            print("\n--- MODIFICAR ELEMENTO ---")
            self.lista.mostrar()
            print("\n1. Modificar por posición")
            print("2. Modificar por valor")
            print("3. Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                try:
                    indice = int(input("Ingrese la posición a modificar: "))
                    nuevo_valor = input("Ingrese el nuevo valor: ")
                    self.lista.modificar(indice, nuevo_valor)
                    self.lista.mostrar()
                except ValueError:
                    print("✗ Error: Ingrese un número válido")
            elif opcion == "2":
                valor_buscar = input("Ingrese el valor a buscar: ")
                nuevo_valor = input("Ingrese el nuevo valor: ")
                self.lista.modificar_por_valor(valor_buscar, nuevo_valor)
                self.lista.mostrar()
            elif opcion == "3":
                break
            else:
                print("✗ Opción inválida")
    
    def submenu_buscar(self):
        """Submenú para buscar elementos"""
        if self.lista.esta_vacia():
            print("✗ La lista está vacía")
            return
        
        while True:
            print("\n--- BUSCAR ELEMENTO ---")
            print("1. Buscar por valor (obtener índice)")
            print("2. Buscar por posición (obtener valor)")
            print("3. Verificar si existe un valor")
            print("4. Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                valor = input("Ingrese el valor a buscar: ")
                indice = self.lista.indice_de(valor)
                if indice != -1:
                    print(f"✓ Valor '{valor}' encontrado en el índice {indice}")
                else:
                    print(f"✗ Valor '{valor}' no encontrado")
            elif opcion == "2":
                try:
                    indice = int(input("Ingrese la posición: "))
                    valor = self.lista.obtener(indice)
                    if valor is not None:
                        print(f"✓ En la posición {indice} se encuentra: {valor}")
                except ValueError:
                    print("✗ Error: Ingrese un número válido")
            elif opcion == "3":
                valor = input("Ingrese el valor a verificar: ")
                if self.lista.contiene(valor):
                    print(f"✓ La lista contiene el valor '{valor}'")
                else:
                    print(f"✗ La lista NO contiene el valor '{valor}'")
            elif opcion == "4":
                break
            else:
                print("✗ Opción inválida")
    
    def ejecutar_ejemplos(self):
        """Ejecuta ejemplos de prueba"""
        print("\n--- EJECUTANDO EJEMPLOS DE PRUEBA ---")
        
        # Crear lista temporal con ejemplos
        lista_ejemplo = MiListaEnlazada()
        
        print("\n1. Agregando elementos...")
        lista_ejemplo.agregar_al_final("Manzana")
        lista_ejemplo.agregar_al_final("Banana")
        lista_ejemplo.agregar_al_final("Cereza")
        lista_ejemplo.agregar_al_inicio("Kiwi")
        lista_ejemplo.mostrar()
        
        print("\n2. Modificando elemento en índice 2...")
        lista_ejemplo.modificar(2, "Naranja")
        lista_ejemplo.mostrar()
        
        print("\n3. Eliminando elemento por valor 'Banana'...")
        lista_ejemplo.eliminar_por_valor("Banana")
        lista_ejemplo.mostrar()
        
        print("\n4. Invirtiendo lista...")
        lista_ejemplo.invertir()
        lista_ejemplo.mostrar()
        
        print("\n5. Buscando elemento 'Kiwi'...")
        indice = lista_ejemplo.indice_de("Kiwi")
        if indice != -1:
            print(f"✓ 'Kiwi' encontrado en índice {indice}")
        
        print("\n6. Convertir a lista de Python:")
        print(f"   {lista_ejemplo.a_lista()}")
        
        print("\n✓ Ejemplos completados")
        input("\nPresione Enter para continuar...")
    
    def ejecutar(self):
        """Ejecuta el programa principal"""
        print("\n" + "="*50)
        print("   BIENVENIDO AL SISTEMA DE LISTA ENLAZADA")
        print("="*50)
        
        while True:
            self.mostrar_menu()
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                self.submenu_agregar()
            elif opcion == "2":
                self.submenu_eliminar()
            elif opcion == "3":
                self.submenu_modificar()
            elif opcion == "4":
                self.submenu_buscar()
            elif opcion == "5":
                print("\n--- LISTA ACTUAL ---")
                self.lista.mostrar()
                input("\nPresione Enter para continuar...")
            elif opcion == "6":
                self.lista.invertir()
                self.lista.mostrar()
                input("\nPresione Enter para continuar...")
            elif opcion == "7":
                confirmar = input("¿Está seguro de limpiar toda la lista? (s/n): ")
                if confirmar.lower() == 's':
                    self.lista.limpiar()
                input("\nPresione Enter para continuar...")
            elif opcion == "8":
                self.lista.mostrar_detallada()
                input("Presione Enter para continuar...")
            elif opcion == "9":
                self.ejecutar_ejemplos()
            elif opcion == "0":
                print("\n¡Gracias por usar el sistema!")
                print("¡Hasta luego!")
                break
            else:
                print("✗ Opción inválida")
                input("Presione Enter para continuar...")


# Programa principal
if __name__ == "__main__":
    # Iniciar el programa interactivo
    app = MenuInteractivo()
    app.ejecutar()