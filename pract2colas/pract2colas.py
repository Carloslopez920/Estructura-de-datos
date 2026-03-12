class Node:
    """Clase que representa un nodo en la lista enlazada"""
    def __init__(self, info):
        self.info = info 
        self.next = None  


class Order:
    """Clase que representa un pedido"""
    def __init__(self, qty, customer):
        self.customer = customer
        self.qty = qty
    
    def get_qty(self):
        return self.qty
    
    def get_customer(self):
        return self.customer
    
    def print(self):
        print(f"    Customer: {self.get_customer()}")
        print(f"    Quantity: {self.get_qty()}")
        print("---")


class Queue:
    """Implementación de una cola FIFO usando lista enlazada"""
    def __init__(self):
        self.top = None  # Apunta al primer elemento (por donde se extrae)
        self.tail = None  # Apunta al último elemento (por donde se inserta)
        self._size = 0  # Número de elementos en la cola
        self.temp_storage = []  # Memoria temporal para guardar elementos
    
    def size(self):
        """Retorna el número de elementos en la cola"""
        return self._size
    
    def is_empty(self):
        """Verifica si la cola está vacía"""
        return self._size == 0
    
    def front(self):
        """Retorna el primer elemento sin eliminarlo. Retorna None si está vacía"""
        if self.is_empty():
            return None
        return self.top.info
    
    def enqueue(self, info):
        """Añade un nuevo elemento al final de la cola"""
        new_node = Node(info)
        
        if self.is_empty():
            # Si la cola está vacía, el nuevo nodo es tanto top como tail
            self.top = new_node
            self.tail = new_node
        else:
            # Enlazamos el nuevo nodo al final y actualizamos tail
            self.tail.next = new_node
            self.tail = new_node
        
        self._size += 1
        print(f"✅ Pedido añadido correctamente. Tamaño actual: {self._size}")
    
    def dequeue(self):
        """Retorna y elimina el primer elemento. Retorna None si está vacía"""
        if self.is_empty():
            print("❌ No hay pedidos para eliminar. La cola está vacía.")
            return None
        
        # Guardamos la información del primer nodo
        info = self.top.info
        
        # Actualizamos top al siguiente nodo
        self.top = self.top.next
        
        # Si la cola quedó vacía, tail también debe ser None
        if self.top is None:
            self.tail = None
        
        self._size -= 1
        print(f"✅ Primer pedido eliminado correctamente. Tamaño actual: {self._size}")
        return info
    
    def remove_specific(self, position):
        """
        Elimina un pedido en una posición específica
        Guarda los elementos anteriores en memoria temporal y los reincorpora
        """
        if self.is_empty():
            print("❌ La cola está vacía. No hay pedidos para eliminar.")
            return None
        
        if position < 1 or position > self._size:
            print(f"❌ Posición no válida. La cola tiene {self._size} pedido(s).")
            return None
        
        print(f"\n🔄 Eliminando pedido en posición {position}...")
        
        # Limpiar memoria temporal anterior
        self.temp_storage = []
        
        # Guardar elementos anteriores al que queremos eliminar
        for i in range(1, position):
            if not self.is_empty():
                pedido = self.dequeue()
                if pedido:
                    self.temp_storage.append(pedido)
                    print(f"   📦 Guardando pedido #{i} en memoria temporal")
        
        # Eliminar el pedido en la posición deseada
        print(f"   🗑️ Eliminando pedido #{position}...")
        removed_pedido = self.dequeue() if not self.is_empty() else None
        
        # Reincorporar los elementos de la memoria temporal
        if self.temp_storage:
            print(f"   🔄 Reincorporando {len(self.temp_storage)} pedido(s) desde memoria temporal")
            for pedido in self.temp_storage:
                self.enqueue(pedido)
        
        # Limpiar memoria temporal después de reincorporar
        self.temp_storage = []
        
        if removed_pedido:
            print(f"✅ Pedido en posición {position} eliminado correctamente")
        
        return removed_pedido
    
    def print_info(self):
        """Muestra el contenido completo de la cola"""
        print("\n" + "="*50)
        print("******** QUEUE DUMP ********")
        print(f"Size: {self._size}")
        
        if not self.is_empty():
            node = self.top
            element_num = 1
            
            while node is not None:
                print(f"** Element {element_num}")
                node.info.print()
                node = node.next
                element_num += 1
        else:
            print("La cola está vacía")
        
        print("******************************")
        print("="*50 + "\n")


class TestQueue:
    """Clase para probar la implementación de la cola con interacción del usuario"""
    
    @staticmethod
    def confirmar_accion(mensaje):
        """Pregunta al usuario si quiere continuar con una acción"""
        while True:
            respuesta = input(f"\n¿{mensaje}? (s/n): ").strip().lower()
            if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
                return True
            elif respuesta in ['n', 'no', 'nope']:
                return False
            else:
                print("❌ Respuesta no válida. Por favor ingrese 's' para sí o 'n' para no.")
    
    @staticmethod
    def leer_entero_con_cancelar(mensaje, min_valor=1, max_valor=None):
        """
        Lee un entero del usuario con opción a cancelar
        Retorna el valor o None si se cancela
        """
        while True:
            entrada = input(mensaje).strip()
            
            # Verificar si quiere cancelar
            if entrada.lower() in ['cancelar', 'c', 'salir', 'exit', 'q']:
                print("⏸️ Operación cancelada.")
                return None
            
            try:
                valor = int(entrada)
                if valor < min_valor:
                    print(f"❌ El valor debe ser mayor o igual a {min_valor}.")
                    continue
                if max_valor and valor > max_valor:
                    print(f"❌ El valor debe ser menor o igual a {max_valor}.")
                    continue
                return valor
            except ValueError:
                print("❌ Por favor, ingrese un número válido o 'cancelar' para salir.")
    
    @staticmethod
    def leer_texto_con_cancelar(mensaje, permitir_vacio=False):
        """
        Lee texto del usuario con opción a cancelar
        Retorna el texto o None si se cancela
        """
        while True:
            texto = input(mensaje).strip()
            
            # Verificar si quiere cancelar
            if texto.lower() in ['cancelar', 'c', 'salir', 'exit', 'q']:
                print("⏸️ Operación cancelada.")
                return None
            
            if not permitir_vacio and not texto:
                print("❌ El texto no puede estar vacío. Ingrese 'cancelar' para salir.")
                continue
            
            return texto
    
    @staticmethod
    def crear_pedido():
        """Solicita al usuario los datos para crear un nuevo pedido con opción a cancelar"""
        print("\n--- Crear nuevo pedido (escriba 'cancelar' para salir) ---")
        
        # Leer cantidad
        qty = TestQueue.leer_entero_con_cancelar("Cantidad de producto (mayor a 0): ", min_valor=1)
        if qty is None:
            return None
        
        # Leer cliente
        customer = TestQueue.leer_texto_con_cancelar("Nombre del cliente: ")
        if customer is None:
            return None
        
        return Order(qty, customer)
    
    @staticmethod
    def mostrar_menu():
        """Muestra el menú de opciones"""
        print("\n" + "="*50)
        print("MENÚ DE OPCIONES - COLA DE PEDIDOS")
        print("="*50)
        print("1. Agregar pedidos (ingresar múltiples)")
        print("2. Ver primer pedido (front)")
        print("3. Eliminar primer pedido (dequeue)")
        print("4. Eliminar pedido específico (con memoria temporal)")
        print("5. Mostrar todos los pedidos")
        print("6. Ver tamaño de la cola")
        print("7. Salir")
        print("="*50)
        print("En cualquier momento puede escribir 'cancelar' para volver al menú")
        print("="*50)
    
    @staticmethod
    def agregar_pedidos(queue):
        """Permite al usuario agregar múltiples pedidos con opción a cancelar"""
        print("\n--- Agregar pedidos (escriba 'cancelar' para salir) ---")
        
        # Preguntar si realmente quiere agregar pedidos
        if not TestQueue.confirmar_accion("Desea agregar pedidos"):
            print("⏸️ Operación cancelada.")
            return
        
        # Leer número de pedidos
        num_pedidos = TestQueue.leer_entero_con_cancelar("¿Cuántos pedidos desea ingresar? ", min_valor=1)
        if num_pedidos is None:
            return
        
        pedidos_agregados = 0
        for i in range(num_pedidos):
            print(f"\n--- Pedido #{i+1} ---")
            pedido = TestQueue.crear_pedido()
            
            if pedido is None:
                # Preguntar si quiere continuar con los siguientes pedidos
                print(f"\n⚠️ Se canceló la creación del pedido #{i+1}.")
                if not TestQueue.confirmar_accion("Desea continuar con los siguientes pedidos"):
                    break
                continue
            
            queue.enqueue(pedido)
            pedidos_agregados += 1
        
        if pedidos_agregados > 0:
            print(f"\n✅ {pedidos_agregados} pedido(s) agregado(s) correctamente.")
            if TestQueue.confirmar_accion("Desea ver el estado actual de la cola"):
                queue.print_info()
        else:
            print("\n⚠️ No se agregó ningún pedido.")
    
    @staticmethod
    def ver_primer_pedido(queue):
        """Muestra el primer pedido con opción a cancelar"""
        print("\n--- Ver primer pedido ---")
        
        if not TestQueue.confirmar_accion("Desea ver el primer pedido"):
            print("⏸️ Operación cancelada.")
            return
        
        pedido = queue.front()
        if pedido:
            print("Primer pedido (sin eliminar):")
            pedido.print()
        else:
            print("La cola está vacía. No hay pedidos para mostrar.")
    
    @staticmethod
    def eliminar_primer_pedido(queue):
        """Elimina el primer pedido con opción a cancelar"""
        print("\n--- Eliminar primer pedido ---")
        
        if queue.is_empty():
            print("❌ La cola está vacía. No hay pedidos para eliminar.")
            return
        
        # Mostrar el pedido que se va a eliminar
        pedido = queue.front()
        print("Pedido que será eliminado:")
        pedido.print()
        
        if not TestQueue.confirmar_accion("Confirma la eliminación"):
            print("⏸️ Operación cancelada.")
            return
        
        pedido_eliminado = queue.dequeue()
        if pedido_eliminado:
            print("✅ Pedido eliminado correctamente.")
            if TestQueue.confirmar_accion("Desea ver el estado actual de la cola"):
                queue.print_info()
    
    @staticmethod
    def eliminar_pedido_especifico(queue):
        """Permite al usuario eliminar un pedido en una posición específica con opción a cancelar"""
        print("\n--- Eliminar pedido específico ---")
        
        if queue.is_empty():
            print("❌ La cola está vacía. No hay pedidos para eliminar.")
            return
        
        # Mostrar estado actual
        queue.print_info()
        
        if not TestQueue.confirmar_accion("Desea eliminar un pedido específico"):
            print("⏸️ Operación cancelada.")
            return
        
        # Leer posición
        posicion = TestQueue.leer_entero_con_cancelar(
            f"¿Qué posición desea eliminar? (1-{queue.size()}): ",
            min_valor=1,
            max_valor=queue.size()
        )
        
        if posicion is None:
            return
        
        # Confirmar eliminación
        # Para mostrar qué pedido se va a eliminar, necesitamos acceder a él
        node = queue.top
        for i in range(1, posicion):
            node = node.next
        
        print(f"\nPedido en posición {posicion} que será eliminado:")
        node.info.print()
        
        if not TestQueue.confirmar_accion("Confirma la eliminación"):
            print("⏸️ Operación cancelada.")
            return
        
        pedido_eliminado = queue.remove_specific(posicion)
        
        if pedido_eliminado:
            print("\n✅ Pedido eliminado correctamente.")
            if TestQueue.confirmar_accion("Desea ver el estado final de la cola"):
                queue.print_info()
    
    @staticmethod
    def mostrar_todos_pedidos(queue):
        """Muestra todos los pedidos con opción a cancelar"""
        print("\n--- Mostrar todos los pedidos ---")
        
        if not TestQueue.confirmar_accion("Desea ver todos los pedidos"):
            print("⏸️ Operación cancelada.")
            return
        
        queue.print_info()
    
    @staticmethod
    def ver_tamano_cola(queue):
        """Muestra el tamaño de la cola con opción a cancelar"""
        print("\n--- Ver tamaño de la cola ---")
        
        if not TestQueue.confirmar_accion("Desea ver el tamaño de la cola"):
            print("⏸️ Operación cancelada.")
            return
        
        print(f"\n📊 Tamaño actual de la cola: {queue.size()} pedido(s)")
    
    @staticmethod
    def main():
        """Método principal con menú interactivo"""
        queue = Queue()
        
        print("="*60)
        print("BIENVENIDO AL SISTEMA DE GESTIÓN DE PEDIDOS")
        print("="*60)
        print("🌟 CARACTERÍSTICAS:")
        print("  • Puede CANCELAR cualquier operación escribiendo 'cancelar'")
        print("  • Eliminación de pedidos específicos")
        print("  • Confirmación antes de acciones importantes")
        print("="*60)
        
        while True:
            TestQueue.mostrar_menu()
            opcion = input("Seleccione una opción (1-7): ").strip()
            
            if opcion == "1":
                # Agregar pedidos
                TestQueue.agregar_pedidos(queue)
                
            elif opcion == "2":
                # Ver primer pedido (front)
                TestQueue.ver_primer_pedido(queue)
                
            elif opcion == "3":
                # Eliminar primer pedido (dequeue)
                TestQueue.eliminar_primer_pedido(queue)
                
            elif opcion == "4":
                # Eliminar pedido específico
                TestQueue.eliminar_pedido_especifico(queue)
                
            elif opcion == "5":
                # Mostrar todos los pedidos
                TestQueue.mostrar_todos_pedidos(queue)
                
            elif opcion == "6":
                # Ver tamaño de la cola
                TestQueue.ver_tamano_cola(queue)
                
            elif opcion == "7":
                # Salir
                if TestQueue.confirmar_accion("Está seguro que desea salir"):
                    print("\n👋 ¡Gracias por usar el sistema! Hasta luego.")
                    break
                
            else:
                print("❌ Opción no válida. Por favor, seleccione una opción del 1 al 7.")
            
            input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    # Iniciar directamente el modo interactivo
    TestQueue.main()