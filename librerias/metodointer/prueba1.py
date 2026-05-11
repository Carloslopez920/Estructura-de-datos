"""
EJEMPLO 1: Ingresa tus propios números y visualiza el ordenamiento con Quick Sort
"""

from metordenamiento import (
    VisualizadorOrdenamiento,
    animar_ordenamiento,
    visualizar_paso_a_paso
)

def ingresar_numeros_manual():
    """Función interactiva para ingresar números"""
    print("\n" + "="*60)
    print("📝 INGRESO DE DATOS MANUAL")
    print("="*60)
    
    while True:
        entrada = input("\nIngresa los números separados por comas (ej: 5,2,8,1,9): ").strip()
        
        if not entrada:
            print("❌ No ingresaste ningún dato. Intenta de nuevo.")
            continue
        
        try:
            # Convertir a lista de números
            numeros = []
            for item in entrada.split(","):
                item = item.strip()
                if '.' in item:
                    numeros.append(float(item))
                else:
                    numeros.append(int(item))
            
            if not numeros:
                print("❌ La lista está vacía. Intenta de nuevo.")
                continue
            
            if len(numeros) > 30:
                print(f"⚠️ Ingresaste {len(numeros)} números. Para mejor visualización se recomiendan máximo 30.")
                continuar = input("¿Quieres continuar de todas formas? (s/n): ").lower()
                if continuar != 's':
                    continue
            
            print(f"\n✅ Números ingresados: {numeros}")
            print(f"📊 Cantidad: {len(numeros)} números")
            print(f"📈 Rango: {min(numeros)} - {max(numeros)}")
            
            return numeros
        
        except ValueError:
            print("❌ Error: Asegúrate de ingresar solo números separados por comas.")
            print("   Ejemplo válido: 10, 25, 3, 48, 19")

def ingresar_datos_aleatorios():
    """Función interactiva para generar números aleatorios"""
    print("\n" + "="*60)
    print("🎲 GENERACIÓN DE NÚMEROS ALEATORIOS")
    print("="*60)
    
    import random
    
    while True:
        try:
            cantidad = int(input("\n¿Cuántos números quieres generar? ").strip())
            if cantidad <= 0:
                print("❌ La cantidad debe ser mayor a 0.")
                continue
            
            if cantidad > 30:
                print(f"⚠️ Generarás {cantidad} números. Para mejor visualización se recomiendan máximo 30.")
                continuar = input("¿Quieres continuar de todas formas? (s/n): ").lower()
                if continuar != 's':
                    continue
            
            min_val = int(input("Valor mínimo: ").strip())
            max_val = int(input("Valor máximo: ").strip())
            
            if min_val >= max_val:
                print("❌ El valor mínimo debe ser menor que el máximo.")
                continue
            
            numeros = [random.randint(min_val, max_val) for _ in range(cantidad)]
            print(f"\n✅ Números generados: {numeros}")
            print(f"📊 Cantidad: {len(numeros)} números")
            print(f"📈 Rango: {min(numeros)} - {max(numeros)}")
            
            return numeros
        
        except ValueError:
            print("❌ Por favor, ingresa números válidos.")

def elegir_algoritmo():
    """Menú para elegir el algoritmo de ordenamiento"""
    print("\n" + "="*60)
    print("🎯 SELECCIÓN DE ALGORITMO")
    print("="*60)
    print("1. Shell Sort")
    print("2. Quick Sort")
    print("3. Radix Sort")
    print("4. Heap Sort")
    
    while True:
        opcion = input("\nElige un algoritmo (1-4): ").strip()
        if opcion == "1":
            return "shell_sort_visual", "Shell Sort"
        elif opcion == "2":
            return "quick_sort_visual", "Quick Sort"
        elif opcion == "3":
            return "radix_sort_visual", "Radix Sort"
        elif opcion == "4":
            return "heap_sort_visual", "Heap Sort"
        else:
            print("❌ Opción inválida. Elige 1, 2, 3 o 4.")

def elegir_visualizacion():
    """Menú para elegir el tipo de visualización"""
    print("\n" + "="*60)
    print("🎬 TIPO DE VISUALIZACIÓN")
    print("="*60)
    print("1. Animación completa (movimiento paso a paso)")
    print("2. Cuadrícula estática (ver todos los pasos juntos)")
    print("3. Ambas")
    print("4. Solo resultados (sin visualización)")
    
    while True:
        opcion = input("\nElige una opción (1-4): ").strip()
        if opcion in ["1", "2", "3", "4"]:
            return opcion
        else:
            print("❌ Opción inválida. Elige 1, 2, 3 o 4.")

def ejecutar_ejemplo1():
    """Ejecuta el ejemplo interactivo completo"""
    print("\n" + "="*60)
    print("📚 LIBRERÍA DE ORDENAMIENTO - EJEMPLO INTERACTIVO 1")
    print("="*60)
    
    # Elegir origen de datos
    print("\n¿Cómo quieres proporcionar los datos?")
    print("1. Ingresar números manualmente")
    print("2. Generar números aleatorios")
    
    while True:
        opcion_datos = input("\nElige una opción (1-2): ").strip()
        if opcion_datos == "1":
            datos_originales = ingresar_numeros_manual()
            break
        elif opcion_datos == "2":
            datos_originales = ingresar_datos_aleatorios()
            break
        else:
            print("❌ Opción inválida. Elige 1 o 2.")
    
    # Elegir algoritmo
    nombre_algo, nombre_mostrar = elegir_algoritmo()
    
    # Crear visualizador
    visualizador = VisualizadorOrdenamiento()
    
    # Ejecutar según el algoritmo elegido
    print(f"\n🔄 Ejecutando {nombre_mostrar}...")
    
    datos_copia = datos_originales.copy()
    
    import time
    inicio = time.time()
    
    if nombre_algo == "shell_sort_visual":
        resultado = visualizador.shell_sort_visual(datos_copia)
    elif nombre_algo == "quick_sort_visual":
        resultado = visualizador.quick_sort_visual(datos_copia)
    elif nombre_algo == "radix_sort_visual":
        resultado = visualizador.radix_sort_visual(datos_copia)
    else:
        resultado = visualizador.heap_sort_visual(datos_copia)
    
    fin = time.time()
    tiempo = fin - inicio
    
    # Mostrar resultados
    print("\n" + "="*60)
    print(f"📊 RESULTADOS - {nombre_mostrar}")
    print("="*60)
    
    print(f"\n📥 Datos originales ({len(datos_originales)} elementos):")
    print(f"   {datos_originales}")
    
    print(f"\n📤 Datos ordenados:")
    print(f"   {resultado}")
    
    print(f"\n⏱️ Tiempo de ejecución: {tiempo:.6f} segundos")
    print(f"📝 Pasos registrados: {len(visualizador.pasos)}")
    
    # Verificar corrección
    es_correcto = resultado == sorted(datos_originales)
    print(f"\n✅ Verificación: {'CORRECTO' if es_correcto else 'INCORRECTO'}")
    
    # Visualización
    opcion_vis = elegir_visualizacion()
    
    if opcion_vis == "1":
        print("\n🎬 Mostrando animación...")
        animar_ordenamiento(datos_originales, visualizador.pasos, nombre_mostrar, interval=200)
    elif opcion_vis == "2":
        print("\n📸 Mostrando cuadrícula paso a paso...")
        visualizar_paso_a_paso(datos_originales, visualizador.pasos, nombre_mostrar)
    elif opcion_vis == "3":
        print("\n📸 Mostrando cuadrícula paso a paso...")
        visualizar_paso_a_paso(datos_originales, visualizador.pasos, nombre_mostrar)
        print("\n🎬 Mostrando animación...")
        animar_ordenamiento(datos_originales, visualizador.pasos, nombre_mostrar, interval=200)
    else:
        print("\n⏭️ Omitiendo visualización gráfica.")

if __name__ == "__main__":
    ejecutar_ejemplo1()