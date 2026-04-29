import random
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from typing import List

# ==================== ALGORITMOS DE ORDENAMIENTO CON VISUALIZACION ====================

class VisualizadorOrdenamiento:
    def __init__(self):
        self.pasos = []
    
    def registrar_paso(self, arr: List[int]):
        """Registra un paso del ordenamiento"""
        self.pasos.append(arr.copy())
    
    def limpiar_pasos(self):
        """Limpia los pasos registrados"""
        self.pasos = []
    
    # SHELL SORT CON VISUALIZACION
    def shell_sort_visual(self, collection: List[int]) -> List[int]:
        """Shell Sort algorithm con registro de pasos"""
        self.limpiar_pasos()
        gaps = [701, 301, 132, 57, 23, 10, 4, 1]
        self.registrar_paso(collection)
        
        for gap in gaps:
            for i in range(gap, len(collection)):
                insert_value = collection[i]
                j = i
                while j >= gap and collection[j - gap] > insert_value:
                    collection[j] = collection[j - gap]
                    j -= gap
                    self.registrar_paso(collection)
                if j != i:
                    collection[j] = insert_value
                    self.registrar_paso(collection)
        
        return collection
    
    # QUICK SORT CON VISUALIZACION
    def quick_sort_visual(self, collection: List[int]) -> List[int]:
        """Quick Sort algorithm con registro de pasos"""
        if len(collection) < 2:
            return collection
        
        pivot_index = random.randrange(len(collection))
        pivot = collection.pop(pivot_index)
        self.registrar_paso(collection)
        
        lesser = [item for item in collection if item <= pivot]
        greater = [item for item in collection if item > pivot]
        
        lesser_sorted = self.quick_sort_visual(lesser)
        greater_sorted = self.quick_sort_visual(greater)
        
        result = [*lesser_sorted, pivot, *greater_sorted]
        self.registrar_paso(result)
        
        return result
    
    # RADIX SORT CON VISUALIZACION
    def radix_sort_visual(self, list_of_ints: List[int]) -> List[int]:
        """Radix Sort algorithm con registro de pasos"""
        self.limpiar_pasos()
        if not list_of_ints:
            return list_of_ints
        
        RADIX = 10
        placement = 1
        max_digit = max(list_of_ints)
        
        self.registrar_paso(list_of_ints)
        
        while placement <= max_digit:
            buckets: List[List[int]] = [[] for _ in range(RADIX)]
            
            for i in list_of_ints:
                tmp = int((i / placement) % RADIX)
                buckets[tmp].append(i)
            
            a = 0
            for b in range(RADIX):
                for i in buckets[b]:
                    list_of_ints[a] = i
                    a += 1
                    self.registrar_paso(list_of_ints)
            
            placement *= RADIX
        
        return list_of_ints
    
    # HEAP SORT CON VISUALIZACION
    def heapify_visual(self, unsorted: List[int], index: int, heap_size: int) -> None:
        """Heapify helper con registro de pasos"""
        largest = index
        left_index = 2 * index + 1
        right_index = 2 * index + 2
        
        if left_index < heap_size and unsorted[left_index] > unsorted[largest]:
            largest = left_index
        
        if right_index < heap_size and unsorted[right_index] > unsorted[largest]:
            largest = right_index
        
        if largest != index:
            unsorted[largest], unsorted[index] = unsorted[index], unsorted[largest]
            self.registrar_paso(unsorted)
            self.heapify_visual(unsorted, largest, heap_size)
    
    def heap_sort_visual(self, unsorted: List[int]) -> List[int]:
        """Heap Sort algorithm con registro de pasos"""
        self.limpiar_pasos()
        if not unsorted:
            return unsorted
        
        n = len(unsorted)
        
        for i in range(n // 2 - 1, -1, -1):
            self.heapify_visual(unsorted, i, n)
        
        for i in range(n - 1, 0, -1):
            unsorted[0], unsorted[i] = unsorted[i], unsorted[0]
            self.registrar_paso(unsorted)
            self.heapify_visual(unsorted, 0, i)
        
        return unsorted


# ==================== FUNCIONES DE VISUALIZACION ====================

def animar_ordenamiento(datos_originales: List[int], pasos: List[List[int]], titulo: str, interval: int = 200):
    """Crea una animacion del proceso de ordenamiento"""
    if not pasos:
        print("No hay pasos para animar")
        return
    
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.suptitle(titulo, fontsize=16, fontweight='bold')
    
    ax.set_xlabel('Posicion en el arreglo')
    ax.set_ylabel('Valor')
    ax.grid(True, alpha=0.3)
    
    # Crear barras iniciales
    bars = ax.bar(range(len(pasos[0])), pasos[0], color='steelblue', alpha=0.7)
    
    # Texto informativo
    info_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, 
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                       fontsize=10, fontweight='bold')
    
    def update(frame):
        # Limpiar texto anterior de barras
        for text in ax.texts:
            if text != info_text:
                text.remove()
        
        # Actualizar barras
        for bar, val in zip(bars, pasos[frame]):
            bar.set_height(val)
            
            # Cambiar color basado en el valor
            if val == max(pasos[frame]):
                bar.set_color('red')
            elif val == min(pasos[frame]):
                bar.set_color('green')
            else:
                bar.set_color('steelblue')
            
            # Agregar valor encima de la barra
            ax.text(bar.get_x() + bar.get_width()/2, val + 0.5, 
                   str(val), ha='center', va='bottom', fontsize=8)
        
        # Actualizar texto informativo
        progreso = (frame + 1) / len(pasos) * 100
        info_text.set_text(f'Paso: {frame + 1}/{len(pasos)}\n'
                          f'Progreso: {progreso:.1f}%\n'
                          f'Min: {min(pasos[frame])} | Max: {max(pasos[frame])}')
        
        ax.set_title(f'Proceso de ordenamiento - Paso {frame + 1} ({progreso:.1f}%)')
        
        return bars, info_text
    
    anim = animation.FuncAnimation(fig, update, frames=len(pasos), 
                                   interval=interval, repeat=False, blit=False)
    
    plt.tight_layout()
    plt.show()
    return anim


def visualizar_paso_a_paso(datos: List[int], pasos: List[List[int]], nombre_algoritmo: str, max_pasos_mostrar: int = 8):
    """Muestra una cuadricula del proceso de ordenamiento"""
    if not pasos:
        return
    
    # Seleccionar pasos a mostrar
    total_pasos = len(pasos)
    indices_pasos = []
    
    if total_pasos <= max_pasos_mostrar:
        indices_pasos = list(range(total_pasos))
    else:
        # Tomar pasos distribuidos
        step = total_pasos // max_pasos_mostrar
        for i in range(0, total_pasos, step):
            indices_pasos.append(i)
        if total_pasos - 1 not in indices_pasos:
            indices_pasos.append(total_pasos - 1)
    
    # Crear figura
    n_pasos = len(indices_pasos)
    filas = (n_pasos + 2) // 3
    fig, axes = plt.subplots(filas, 3, figsize=(15, 5 * filas))
    axes = axes.flatten() if n_pasos > 1 else [axes]
    
    fig.suptitle(f'{nombre_algoritmo} - Evolucion del ordenamiento', fontsize=14, fontweight='bold')
    
    for idx, paso_idx in enumerate(indices_pasos):
        ax = axes[idx]
        paso_data = pasos[paso_idx]
        
        # Crear grafico de barras
        colors = ['red' if val == max(paso_data) 
                 else 'green' if val == min(paso_data)
                 else 'steelblue' for val in paso_data]
        
        bars = ax.bar(range(len(paso_data)), paso_data, color=colors, alpha=0.7)
        ax.set_title(f'Paso {paso_idx + 1}/{total_pasos}')
        ax.set_xlabel('Posicion')
        ax.set_ylabel('Valor')
        ax.grid(True, alpha=0.3)
        
        # Agregar valores en las barras
        for bar, val in zip(bars, paso_data):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                   str(val), ha='center', va='bottom', fontsize=8)
    
    # Ocultar ejes extras
    for idx in range(len(indices_pasos), len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    plt.show()


# ==================== FUNCIONES DE UTILIDAD ====================

def generar_datos_aleatorios() -> List[int]:
    """Genera una lista de numeros aleatorios"""
    while True:
        try:
            cantidad = int(input("Cuantos numeros quieres generar? (max 30 para mejor visualizacion): "))
            if cantidad <= 0:
                print("Por favor, ingresa un numero positivo.")
                continue
            
            if cantidad > 30:
                print("Advertencia: Con mas de 30 elementos la animacion puede ser lenta.")
                continuar = input("Quieres continuar de todas formas? (s/n): ").strip().lower()
                if continuar != 's':
                    continue
            
            min_val = int(input("Valor minimo: "))
            max_val = int(input("Valor maximo: "))
            
            if min_val >= max_val:
                print("El valor minimo debe ser menor que el maximo.")
                continue
            
            datos = [random.randint(min_val, max_val) for _ in range(cantidad)]
            print(f"\nSe generaron {cantidad} numeros aleatorios entre {min_val} y {max_val}")
            return datos
        
        except ValueError:
            print("Por favor, ingresa numeros validos.")


def ingresar_datos_manual() -> List[int]:
    """Permite al usuario ingresar datos manualmente"""
    while True:
        entrada = input("\nIngresa los numeros separados por comas (max 15 numeros): ").strip()
        
        if not entrada:
            print("No ingresaste ningun dato.")
            continue
        
        try:
            datos = [int(item.strip()) for item in entrada.split(",")]
            if not datos:
                print("La lista esta vacia.")
                continue
            
            if len(datos) > 15:
                print("Advertencia: Con mas de 15 elementos la visualizacion puede ser densa.")
                continuar = input("Quieres continuar de todas formas? (s/n): ").strip().lower()
                if continuar != 's':
                    continue
            
            print(f"\nDatos ingresados: {datos}")
            return datos
        
        except ValueError:
            print("Error: Asegurate de ingresar solo numeros separados por comas.")


def mostrar_resultados_simples(original: List[int], ordenados: List[int], tiempo: float, nombre_algoritmo: str):
    """Muestra los resultados de manera textual simple"""
    print("\n" + "="*60)
    print(f"RESULTADOS - {nombre_algoritmo}")
    print("="*60)
    
    print(f"\nDATOS ORIGINALES ({len(original)} elementos):")
    if len(original) <= 20:
        print(f"   {original}")
    else:
        print(f"   {original[:10]} ... {original[-10:]}")
    
    print(f"\nDATOS ORDENADOS:")
    if len(ordenados) <= 20:
        print(f"   {ordenados}")
    else:
        print(f"   {ordenados[:10]} ... {ordenados[-10:]}")
    
    print(f"\nTIEMPO DE EJECUCION: {tiempo:.6f} segundos")
    print(f"TOTAL DE PASOS: {len(visualizador.pasos)}")
    
    # Verificar si esta correctamente ordenado
    esta_ordenado = ordenados == sorted(original)
    if esta_ordenado:
        print(f"\nVERIFICACION: El ordenamiento es CORRECTO")
    else:
        print(f"\nVERIFICACION: El ordenamiento es INCORRECTO")


# ==================== MENU PRINCIPAL ====================

visualizador = VisualizadorOrdenamiento()

def menu_principal():
    """Menu interactivo principal"""
    
    while True:
        print("\n" + "="*60)
        print("SISTEMA DE ORDENAMIENTO CON VISUALIZACION GRAFICA")
        print("="*60)
        print("1. Shell Sort")
        print("2. Quick Sort")
        print("3. Radix Sort")
        print("4. Heap Sort")
        print("5. Comparar TODOS los metodos")
        print("6. Salir")
        print("="*60)
        
        opcion = input("\nElige una opcion (1-6): ").strip()
        
        if opcion == "6":
            print("\nGracias por usar el programa. Hasta luego.")
            plt.close('all')
            break
        
        if opcion not in ["1", "2", "3", "4", "5"]:
            print("Opcion invalida. Por favor, elige una opcion del 1 al 6.")
            continue
        
        # Seleccionar metodo de entrada de datos
        print("\nComo quieres proporcionar los datos?")
        print("1. Generar numeros aleatorios")
        print("2. Ingresar manualmente")
        
        metodo_entrada = input("Elige una opcion (1-2): ").strip()
        
        if metodo_entrada == "1":
            datos_originales = generar_datos_aleatorios()
        elif metodo_entrada == "2":
            datos_originales = ingresar_datos_manual()
        else:
            print("Opcion invalida. Volviendo al menu principal...")
            continue
        
        if not datos_originales:
            continue
        
        if opcion == "1":  # Shell Sort
            datos_copia = datos_originales.copy()
            print(f"\nEjecutando Shell Sort...")
            inicio = time.time()
            resultado = visualizador.shell_sort_visual(datos_copia)
            fin = time.time()
            
            mostrar_resultados_simples(datos_originales, resultado, fin - inicio, "Shell Sort")
            
            print("\nOpciones de visualizacion:")
            print("1. Ver animacion completa")
            print("2. Ver proceso paso a paso")
            print("3. Ver ambas")
            
            visual_opcion = input("Elige una opcion (1-3): ").strip()
            
            if visual_opcion == "1":
                animar_ordenamiento(datos_originales, visualizador.pasos, "Shell Sort", interval=150)
            elif visual_opcion == "2":
                visualizar_paso_a_paso(datos_originales, visualizador.pasos, "Shell Sort")
            elif visual_opcion == "3":
                visualizar_paso_a_paso(datos_originales, visualizador.pasos, "Shell Sort")
                animar_ordenamiento(datos_originales, visualizador.pasos, "Shell Sort", interval=150)
        
        elif opcion == "2":  # Quick Sort
            print(f"\nEjecutando Quick Sort...")
            inicio = time.time()
            resultado = visualizador.quick_sort_visual(datos_originales.copy())
            fin = time.time()
            
            mostrar_resultados_simples(datos_originales, resultado, fin - inicio, "Quick Sort")
            
            print("\nOpciones de visualizacion:")
            print("1. Ver animacion completa")
            print("2. Ver proceso paso a paso")
            print("3. Ver ambas")
            
            visual_opcion = input("Elige una opcion (1-3): ").strip()
            
            if visual_opcion == "1":
                animar_ordenamiento(datos_originales, visualizador.pasos, "Quick Sort", interval=300)
            elif visual_opcion == "2":
                visualizar_paso_a_paso(datos_originales, visualizador.pasos, "Quick Sort")
            elif visual_opcion == "3":
                visualizar_paso_a_paso(datos_originales, visualizador.pasos, "Quick Sort")
                animar_ordenamiento(datos_originales, visualizador.pasos, "Quick Sort", interval=300)
        
        elif opcion == "3":  # Radix Sort
            datos_copia = datos_originales.copy()
            print(f"\nEjecutando Radix Sort...")
            inicio = time.time()
            resultado = visualizador.radix_sort_visual(datos_copia)
            fin = time.time()
            
            mostrar_resultados_simples(datos_originales, resultado, fin - inicio, "Radix Sort")
            
            print("\nOpciones de visualizacion:")
            print("1. Ver animacion completa")
            print("2. Ver proceso paso a paso")
            print("3. Ver ambas")
            
            visual_opcion = input("Elige una opcion (1-3): ").strip()
            
            if visual_opcion == "1":
                animar_ordenamiento(datos_originales, visualizador.pasos, "Radix Sort", interval=100)
            elif visual_opcion == "2":
                visualizar_paso_a_paso(datos_originales, visualizador.pasos, "Radix Sort")
            elif visual_opcion == "3":
                visualizar_paso_a_paso(datos_originales, visualizador.pasos, "Radix Sort")
                animar_ordenamiento(datos_originales, visualizador.pasos, "Radix Sort", interval=100)
        
        elif opcion == "4":  # Heap Sort
            datos_copia = datos_originales.copy()
            print(f"\nEjecutando Heap Sort...")
            inicio = time.time()
            resultado = visualizador.heap_sort_visual(datos_copia)
            fin = time.time()
            
            mostrar_resultados_simples(datos_originales, resultado, fin - inicio, "Heap Sort")
            
            print("\nOpciones de visualizacion:")
            print("1. Ver animacion completa")
            print("2. Ver proceso paso a paso")
            print("3. Ver ambas")
            
            visual_opcion = input("Elige una opcion (1-3): ").strip()
            
            if visual_opcion == "1":
                animar_ordenamiento(datos_originales, visualizador.pasos, "Heap Sort", interval=200)
            elif visual_opcion == "2":
                visualizar_paso_a_paso(datos_originales, visualizador.pasos, "Heap Sort")
            elif visual_opcion == "3":
                visualizar_paso_a_paso(datos_originales, visualizador.pasos, "Heap Sort")
                animar_ordenamiento(datos_originales, visualizador.pasos, "Heap Sort", interval=200)
        
        elif opcion == "5":  # Comparar todos
            print("\n" + "="*60)
            print("COMPARANDO LOS 4 METODOS")
            print("="*60)
            
            resultados = {}
            todos_los_pasos = {}
            
            algoritmos = {
                "Shell Sort": visualizador.shell_sort_visual,
                "Quick Sort": visualizador.quick_sort_visual,
                "Radix Sort": visualizador.radix_sort_visual,
                "Heap Sort": visualizador.heap_sort_visual
            }
            
            for nombre, algoritmo in algoritmos.items():
                datos_copia = datos_originales.copy()
                print(f"\nEjecutando {nombre}...")
                inicio = time.time()
                
                try:
                    resultado = algoritmo(datos_copia)
                    fin = time.time()
                    tiempo = fin - inicio
                    resultados[nombre] = {
                        "tiempo": tiempo,
                        "correcto": resultado == sorted(datos_originales),
                        "pasos": len(visualizador.pasos)
                    }
                    todos_los_pasos[nombre] = visualizador.pasos.copy()
                    print(f"   Completado en {tiempo:.6f} segundos - {len(visualizador.pasos)} pasos")
                except Exception as e:
                    print(f"   Error en {nombre}: {e}")
            
            # Mostrar comparativa
            print("\n" + "="*60)
            print("COMPARATIVA DE RENDIMIENTO")
            print("="*60)
            
            resultados_ordenados = sorted(resultados.items(), key=lambda x: x[1]["tiempo"])
            
            print(f"\nDatos originales ({len(datos_originales)} elementos)")
            
            print(f"\nRANKING DE VELOCIDAD:")
            for i, (nombre, datos) in enumerate(resultados_ordenados, 1):
                check = "CORRECTO" if datos['correcto'] else "ERROR"
                print(f"   {i}. {nombre:12} - {datos['tiempo']:.6f} segundos - {datos['pasos']} pasos [{check}]")
            
            # Preguntar que visualizar
            print("\nQue metodo quieres visualizar?")
            print("1. Shell Sort")
            print("2. Quick Sort")
            print("3. Radix Sort")
            print("4. Heap Sort")
            print("5. El mas rapido")
            print("6. Ninguno")
            
            ver_opcion = input("Elige una opcion (1-6): ").strip()
            
            if ver_opcion == "1":
                visualizar_paso_a_paso(datos_originales, todos_los_pasos["Shell Sort"], "Shell Sort")
                animar_ordenamiento(datos_originales, todos_los_pasos["Shell Sort"], "Shell Sort", interval=150)
            elif ver_opcion == "2":
                visualizar_paso_a_paso(datos_originales, todos_los_pasos["Quick Sort"], "Quick Sort")
                animar_ordenamiento(datos_originales, todos_los_pasos["Quick Sort"], "Quick Sort", interval=300)
            elif ver_opcion == "3":
                visualizar_paso_a_paso(datos_originales, todos_los_pasos["Radix Sort"], "Radix Sort")
                animar_ordenamiento(datos_originales, todos_los_pasos["Radix Sort"], "Radix Sort", interval=100)
            elif ver_opcion == "4":
                visualizar_paso_a_paso(datos_originales, todos_los_pasos["Heap Sort"], "Heap Sort")
                animar_ordenamiento(datos_originales, todos_los_pasos["Heap Sort"], "Heap Sort", interval=200)
            elif ver_opcion == "5":
                nombre_rapido = resultados_ordenados[0][0]
                print(f"\nVisualizando el metodo mas rapido: {nombre_rapido}")
                visualizar_paso_a_paso(datos_originales, todos_los_pasos[nombre_rapido], nombre_rapido)
                animar_ordenamiento(datos_originales, todos_los_pasos[nombre_rapido], nombre_rapido, interval=150)
        
        input("\nPresiona Enter para continuar...")


# ==================== VERIFICACION ====================

def verificar_dependencias():
    """Verifica si las librerias necesarias estan instaladas"""
    try:
        import matplotlib
        return True
    except ImportError:
        print("\n" + "="*60)
        print("ERROR: Falta matplotlib")
        print("="*60)
        print("\nPara usar las visualizaciones graficas, necesitas instalar:")
        print("   pip install matplotlib")
        print("\n" + "="*60)
        return False


# ==================== EJECUCION PRINCIPAL ====================

if __name__ == "__main__":
    print("="*60)
    print("BIENVENIDO AL SISTEMA DE ORDENAMIENTO CON VISUALIZACION")
    print("="*60)
    print("\nEste programa muestra GRAFICAMENTE como cada algoritmo")
    print("de ordenamiento va resolviendo el problema paso a paso.")
    print("\nCaracteristicas:")
    print("   - Animacion en tiempo real del proceso")
    print("   - Visualizacion paso a paso en cuadricula")
    print("   - Numeros mostrados encima de cada barra")
    print("   - Colores: Rojo=Maximo, Verde=Minimo, Azul=Intermedios")
    
    if not verificar_dependencias():
        exit(1)
    
    menu_principal()