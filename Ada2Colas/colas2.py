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
    
    def mostrar(self):
        if self.esta_vacia():
            return "Vacía"
        return " -> ".join(str(elem) for elem in self.elementos)

class SistemaAtencionSeguros:
    def __init__(self):
        # Diccionario para almacenar las colas por servicio
        self.colas_servicio = {}
        # Contadores para cada servicio (para generar números de atención)
        self.contadores = {}
        # Número total de servicios disponibles (podemos expandir según necesidad)
        self.servicios_disponibles = [1, 2, 3, 4, 5]
        
        # Inicializar colas y contadores para cada servicio
        for servicio in self.servicios_disponibles:
            self.colas_servicio[servicio] = Cola()
            self.contadores[servicio] = 0
    
    def generar_numero_atencion(self, servicio):
        """Genera un número de atención para el servicio especificado"""
        self.contadores[servicio] += 1
        return f"S{servicio}-{self.contadores[servicio]:03d}"
    
    def llegada_cliente(self, servicio):
        """
        Simula la llegada de un cliente
        Formato esperado: C seguido de número de servicio (ej: C1, C2, etc.)
        """
        try:
            servicio = int(servicio)
            
            # Validar que el servicio exista
            if servicio not in self.servicios_disponibles:
                print(f"Error: El servicio {servicio} no existe. Servicios disponibles: {self.servicios_disponibles}")
                return None
            
            # Generar número de atención
            num_atencion = self.generar_numero_atencion(servicio)
            
            # Agregar cliente a la cola correspondiente
            self.colas_servicio[servicio].encolar(num_atencion)
            
            print(f"✅ Cliente registrado - {num_atencion} en cola de servicio {servicio}")
            return num_atencion
            
        except ValueError:
            print("Error: Formato incorrecto. Use C seguido del número de servicio (ej: C1)")
            return None
    
    def atender_cliente(self, servicio):
        """
        Simula la atención de un cliente
        Formato esperado: A seguido de número de servicio (ej: A1, A2, etc.)
        """
        try:
            servicio = int(servicio)
            
            # Validar que el servicio exista
            if servicio not in self.servicios_disponibles:
                print(f"Error: El servicio {servicio} no existe. Servicios disponibles: {self.servicios_disponibles}")
                return None
            
            cola = self.colas_servicio[servicio]
            
            # Verificar si hay clientes en la cola
            if cola.esta_vacia():
                print(f"ℹ️ No hay clientes en espera para el servicio {servicio}")
                return None
            
            # Atender al siguiente cliente
            cliente_atendido = cola.desencolar()
            print(f"📢 Llamando a {cliente_atendido} para servicio {servicio}")
            
            return cliente_atendido
            
        except ValueError:
            print("Error: Formato incorrecto. Use A seguido del número de servicio (ej: A1)")
            return None
    
    def mostrar_estado_colas(self):
        """Muestra el estado actual de todas las colas"""
        print("\n" + "="*60)
        print("ESTADO ACTUAL DE LAS COLAS")
        print("="*60)
        
        for servicio in self.servicios_disponibles:
            cola = self.colas_servicio[servicio]
            print(f"Servicio {servicio}: {cola.tamano()} cliente(s) en espera")
            print(f"  Cola: {cola.mostrar()}")
            print("-"*40)
        
        print(f"Total clientes en espera: {self.total_clientes_espera()}")
        print("="*60)
    
    def total_clientes_espera(self):
        """Calcula el total de clientes en espera en todas las colas"""
        total = 0
        for servicio in self.servicios_disponibles:
            total += self.colas_servicio[servicio].tamano()
        return total
    
    def mostrar_ayuda(self):
        """Muestra las instrucciones de uso"""
        print("\n" + "="*60)
        print("SISTEMA DE ATENCIÓN - COMPAÑÍA DE SEGUROS")
        print("="*60)
        print("COMANDOS DISPONIBLES:")
        print("  C[servicio] - Registrar llegada de cliente (C1, C2, C3, C4, C5)")
        print("  A[servicio] - Atender siguiente cliente (A1, A2, A3, A4, A5)")
        print("  E           - Mostrar estado de las colas")
        print("  H           - Mostrar esta ayuda")
        print("  S           - Salir del sistema")
        print("="*60)

def main():
    # Crear el sistema de atención
    sistema = SistemaAtencionSeguros()
    
    # Mostrar ayuda inicial
    sistema.mostrar_ayuda()
    
    print("\nServicios disponibles:", sistema.servicios_disponibles)
    print("Ingrese un comando (C, A, E, H, S):")
    
    while True:
        try:
            # Solicitar comando al usuario
            comando = input("\n> ").strip().upper()
            
            if not comando:
                continue
            
            # Procesar comandos
            if comando == 'S':
                print("Gracias por usar el sistema. ¡Hasta luego!")
                break
                
            elif comando == 'E':
                sistema.mostrar_estado_colas()
                
            elif comando == 'H':
                sistema.mostrar_ayuda()
                
            elif comando[0] == 'C':
                # Formato: C[servicio]
                if len(comando) < 2:
                    print("Error: Debe especificar el servicio (ej: C1)")
                    continue
                
                servicio = comando[1:]
                sistema.llegada_cliente(servicio)
                
            elif comando[0] == 'A':
                # Formato: A[servicio]
                if len(comando) < 2:
                    print("Error: Debe especificar el servicio (ej: A1)")
                    continue
                
                servicio = comando[1:]
                sistema.atender_cliente(servicio)
                
            else:
                print(f"Comando '{comando}' no reconocido. Use H para ayuda.")
                
        except KeyboardInterrupt:
            print("\n\nOperación cancelada por el usuario.")
            break
        except Exception as e:
            print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()