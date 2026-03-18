class Postre:
    def __init__(self, nombre, ingredientes=None):
        self.nombre = nombre
        self.ingredientes = ingredientes if ingredientes is not None else []

class GestionPostres:
    def __init__(self):
        self.POSTRES = []
    
    def normalizar_nombre(self, nombre):
        return nombre.lower().strip()
    
    def buscar_postre(self, nombre):
        nombre_normalizado = self.normalizar_nombre(nombre)
        for i, postre in enumerate(self.POSTRES):
            if self.normalizar_nombre(postre.nombre) == nombre_normalizado:
                return i, postre
        return None, None
    
    def ordenar_postres(self):
        self.POSTRES.sort(key=lambda x: self.normalizar_nombre(x.nombre))
    
    def imprimir_ingredientes(self, nombre_postre):
        indice, postre = self.buscar_postre(nombre_postre)
        print(f"\nIngredientes de {postre.nombre}:")
        for ing in postre.ingredientes:
            print(f"  - {ing}")
    
    def insertar_ingredientes(self, nombre_postre, nuevos_ingredientes):
        indice, postre = self.buscar_postre(nombre_postre)
        for ing in nuevos_ingredientes:
            postre.ingredientes.append(ing.strip())
        print(f"Ingredientes agregados a {postre.nombre}")
    
    def eliminar_ingrediente(self, nombre_postre, ingrediente_eliminar):
        indice, postre = self.buscar_postre(nombre_postre)
        for i, ing in enumerate(postre.ingredientes):
            if ing.lower() == ingrediente_eliminar.lower().strip():
                postre.ingredientes.pop(i)
                print(f"Ingrediente eliminado de {postre.nombre}")
                break
    
    def alta_postre(self, nombre, ingredientes=None):
        nuevo_postre = Postre(nombre.strip(), ingredientes if ingredientes else [])
        self.POSTRES.append(nuevo_postre)
        self.ordenar_postres()
        print(f"Postre {nombre} agregado")
    
    def baja_postre(self, nombre):
        indice, postre = self.buscar_postre(nombre)
        self.POSTRES.pop(indice)
        print(f"Postre {nombre} eliminado")
    
    def mostrar_todos(self):
        print("\nLISTA DE POSTRES:")
        for i, postre in enumerate(self.POSTRES, 1):
            print(f"{i}. {postre.nombre}")
            for ing in postre.ingredientes:
                print(f"     - {ing}")
    
    def eliminar_postres_repetidos(self):
        postres_vistos = {}
        indices_a_eliminar = []
        
        for i, postre in enumerate(self.POSTRES):
            nombre_normalizado = self.normalizar_nombre(postre.nombre)
            if nombre_normalizado in postres_vistos:
                indices_a_eliminar.append(i)
            else:
                postres_vistos[nombre_normalizado] = i
        
        for idx in sorted(indices_a_eliminar, reverse=True):
            self.POSTRES.pop(idx)
        
        print(f"Postres duplicados eliminados")
    
    def eliminar_ingredientes_repetidos_global(self):
        for postre in self.POSTRES:
            ingredientes_unicos = []
            for ing in postre.ingredientes:
                if ing.lower() not in [i.lower() for i in ingredientes_unicos]:
                    ingredientes_unicos.append(ing)
            postre.ingredientes = ingredientes_unicos
        print("Ingredientes repetidos eliminados")
    
    def limpieza_completa(self):
        self.eliminar_postres_repetidos()
        self.eliminar_ingredientes_repetidos_global()
        self.ordenar_postres()
        print("Limpieza completa realizada")

def main():
    sistema = GestionPostres()
    
    # Datos de ejemplo
    datos_ejemplo = [
        ("Pastel de Chocolate", ["harina", "huevos", "chocolate", "azucar", "mantequilla", "huevos"]),
        ("Flan", ["huevos", "leche", "azucar", "vainilla", "leche"]),
        ("pastel de chocolate", ["harina", "azucar", "chocolate"]),
        ("Helado", ["leche", "crema", "azucar", "vainilla"]),
        ("flan", ["huevos", "leche"]),
    ]
    
    for nombre, ingredientes in datos_ejemplo:
        sistema.alta_postre(nombre, ingredientes)
    
    while True:
        print("\n" + "="*30)
        print("MENÚ PRINCIPAL")
        print("="*30)
        print("1. Ver ingredientes")
        print("2. Insertar ingredientes")
        print("3. Eliminar ingrediente")
        print("4. Agregar postre")
        print("5. Eliminar postre")
        print("6. Mostrar todos")
        print("7. Eliminar postres duplicados")
        print("8. Eliminar ingredientes repetidos")
        print("9. Limpieza completa")
        print("10. Salir")
        
        opcion = input("\nOpción: ")
        
        if opcion == '1':
            nombre = input("Nombre del postre: ")
            sistema.imprimir_ingredientes(nombre)
        
        elif opcion == '2':
            nombre = input("Nombre del postre: ")
            ingredientes = input("Ingredientes (separados por coma): ").split(',')
            sistema.insertar_ingredientes(nombre, ingredientes)
        
        elif opcion == '3':
            nombre = input("Nombre del postre: ")
            ingrediente = input("Ingrediente a eliminar: ")
            sistema.eliminar_ingrediente(nombre, ingrediente)
        
        elif opcion == '4':
            nombre = input("Nombre del postre: ")
            ingredientes = input("Ingredientes (opcional, separados por coma): ").split(',')
            if ingredientes == ['']:
                sistema.alta_postre(nombre)
            else:
                sistema.alta_postre(nombre, ingredientes)
        
        elif opcion == '5':
            nombre = input("Nombre del postre: ")
            sistema.baja_postre(nombre)
        
        elif opcion == '6':
            sistema.mostrar_todos()
        
        elif opcion == '7':
            sistema.eliminar_postres_repetidos()
        
        elif opcion == '8':
            sistema.eliminar_ingredientes_repetidos_global()
        
        elif opcion == '9':
            sistema.limpieza_completa()
        
        elif opcion == '10':
            print("¡Hasta luego!")
            break

if __name__ == "__main__":
    main()