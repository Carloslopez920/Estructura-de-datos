# ==================== LIBRERÍA DE ORDENAMIENTO INTERNO ====================
# archivo: ordenamiento_interno.py

import random
import time
from typing import List, Any, Callable


class OrdenamientoInterno:
    """Clase que contiene los algoritmos de ordenamiento interno"""
    
    def __init__(self):
        self.comparaciones = 0
        self.intercambios = 0
        self.pasos = []  # Para visualización
    
    def reiniciar_contadores(self):
        """Reinicia los contadores de comparaciones e intercambios"""
        self.comparaciones = 0
        self.intercambios = 0
        self.pasos = []
    
    def registrar_paso(self, arr: List[Any]):
        """Registra un paso del ordenamiento"""
        self.pasos.append(arr.copy())
    
    # ==================== BURBUJA ====================
    def burbuja(self, arr: List[Any], comparador: Callable = None) -> List[Any]:
        """
        Ordenamiento Burbuja
        Complejidad: O(n²)
        """
        self.reiniciar_contadores()
        datos = arr.copy()
        n = len(datos)
        
        if comparador is None:
            comparador = lambda a, b: (a > b) - (a < b)
        
        self.registrar_paso(datos)
        
        for i in range(n - 1):
            for j in range(n - 1 - i):
                self.comparaciones += 1
                if comparador(datos[j], datos[j + 1]) > 0:
                    datos[j], datos[j + 1] = datos[j + 1], datos[j]
                    self.intercambios += 1
                    self.registrar_paso(datos)
        
        return datos
    
    # ==================== INSERCIÓN ====================
    def insercion(self, arr: List[Any], comparador: Callable = None) -> List[Any]:
        """
        Ordenamiento por Inserción
        Complejidad: O(n²)
        """
        self.reiniciar_contadores()
        datos = arr.copy()
        
        if comparador is None:
            comparador = lambda a, b: (a > b) - (a < b)
        
        self.registrar_paso(datos)
        
        for i in range(1, len(datos)):
            clave = datos[i]
            j = i - 1
            
            while j >= 0:
                self.comparaciones += 1
                if comparador(datos[j], clave) > 0:
                    datos[j + 1] = datos[j]
                    self.intercambios += 1
                    j -= 1
                    self.registrar_paso(datos)
                else:
                    break
            
            datos[j + 1] = clave
            self.registrar_paso(datos)
        
        return datos
    
    # ==================== SELECCIÓN ====================
    def seleccion(self, arr: List[Any], comparador: Callable = None) -> List[Any]:
        """
        Ordenamiento por Selección
        Complejidad: O(n²)
        """
        self.reiniciar_contadores()
        datos = arr.copy()
        
        if comparador is None:
            comparador = lambda a, b: (a > b) - (a < b)
        
        self.registrar_paso(datos)
        
        for i in range(len(datos)):
            min_idx = i
            for j in range(i + 1, len(datos)):
                self.comparaciones += 1
                if comparador(datos[j], datos[min_idx]) < 0:
                    min_idx = j
            
            if min_idx != i:
                datos[i], datos[min_idx] = datos[min_idx], datos[i]
                self.intercambios += 1
                self.registrar_paso(datos)
        
        return datos
    
    # ==================== SHELL SORT ====================
    def shell_sort(self, arr: List[Any], comparador: Callable = None) -> List[Any]:
        """
        Ordenamiento Shell Sort
        Complejidad: O(n log² n) en promedio
        """
        self.reiniciar_contadores()
        datos = arr.copy()
        
        if comparador is None:
            comparador = lambda a, b: (a > b) - (a < b)
        
        gaps = [701, 301, 132, 57, 23, 10, 4, 1]
        self.registrar_paso(datos)
        
        for gap in gaps:
            if gap >= len(datos):
                continue
                
            for i in range(gap, len(datos)):
                temp = datos[i]
                j = i
                
                while j >= gap:
                    self.comparaciones += 1
                    if comparador(datos[j - gap], temp) > 0:
                        datos[j] = datos[j - gap]
                        self.intercambios += 1
                        j -= gap
                        self.registrar_paso(datos)
                    else:
                        break
                
                datos[j] = temp
                self.registrar_paso(datos)
        
        return datos
    
    # ==================== QUICK SORT ====================
    def _quick_sort_recursivo(self, datos: List[Any], inicio: int, fin: int, 
                               comparador: Callable) -> None:
        """Método recursivo interno para Quick Sort"""
        if inicio >= fin:
            return
        
        # Seleccionar pivote (mediana de tres)
        medio = (inicio + fin) // 2
        pivote = self._mediana_de_tres(datos, inicio, medio, fin, comparador)
        
        # Partición
        i = inicio
        j = fin
        
        while i <= j:
            while i <= fin:
                self.comparaciones += 1
                if comparador(datos[i], pivote) < 0:
                    i += 1
                else:
                    break
            
            while j >= inicio:
                self.comparaciones += 1
                if comparador(datos[j], pivote) > 0:
                    j -= 1
                else:
                    break
            
            if i <= j:
                datos[i], datos[j] = datos[j], datos[i]
                self.intercambios += 1
                self.registrar_paso(datos)
                i += 1
                j -= 1
        
        # Recursión
        self._quick_sort_recursivo(datos, inicio, j, comparador)
        self._quick_sort_recursivo(datos, i, fin, comparador)
    
    def _mediana_de_tres(self, datos: List[Any], a: int, b: int, c: int, 
                          comparador: Callable) -> Any:
        """Encuentra la mediana de tres elementos"""
        if comparador(datos[a], datos[b]) > 0:
            datos[a], datos[b] = datos[b], datos[a]
        if comparador(datos[a], datos[c]) > 0:
            datos[a], datos[c] = datos[c], datos[a]
        if comparador(datos[b], datos[c]) > 0:
            datos[b], datos[c] = datos[c], datos[b]
        return datos[b]
    
    def quick_sort(self, arr: List[Any], comparador: Callable = None) -> List[Any]:
        """
        Ordenamiento Quick Sort
        Complejidad: O(n log n) promedio, O(n²) peor caso
        """
        self.reiniciar_contadores()
        datos = arr.copy()
        
        if comparador is None:
            comparador = lambda a, b: (a > b) - (a < b)
        
        self.registrar_paso(datos)
        self._quick_sort_recursivo(datos, 0, len(datos) - 1, comparador)
        
        return datos
    
    # ==================== HEAP SORT ====================
    def _heapify(self, datos: List[Any], n: int, i: int, comparador: Callable) -> None:
        """Mantiene la propiedad de heap"""
        largest = i
        izquierda = 2 * i + 1
        derecha = 2 * i + 2
        
        if izquierda < n:
            self.comparaciones += 1
            if comparador(datos[izquierda], datos[largest]) > 0:
                largest = izquierda
        
        if derecha < n:
            self.comparaciones += 1
            if comparador(datos[derecha], datos[largest]) > 0:
                largest = derecha
        
        if largest != i:
            datos[i], datos[largest] = datos[largest], datos[i]
            self.intercambios += 1
            self.registrar_paso(datos)
            self._heapify(datos, n, largest, comparador)
    
    def heap_sort(self, arr: List[Any], comparador: Callable = None) -> List[Any]:
        """
        Ordenamiento Heap Sort
        Complejidad: O(n log n)
        """
        self.reiniciar_contadores()
        datos = arr.copy()
        
        if comparador is None:
            comparador = lambda a, b: (a > b) - (a < b)
        
        self.registrar_paso(datos)
        n = len(datos)
        
        # Construir heap
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(datos, n, i, comparador)
        
        # Extraer elementos del heap
        for i in range(n - 1, 0, -1):
            datos[0], datos[i] = datos[i], datos[0]
            self.intercambios += 1
            self.registrar_paso(datos)
            self._heapify(datos, i, 0, comparador)
        
        return datos
    
    # ==================== RADIX SORT ====================
    def radix_sort(self, arr: List[int]) -> List[int]:
        """
        Ordenamiento Radix Sort (solo para enteros)
        Complejidad: O(n * k) donde k es el número de dígitos
        """
        self.reiniciar_contadores()
        if not arr:
            return []
        
        datos = arr.copy()
        
        # Verificar que todos sean enteros
        if not all(isinstance(x, int) for x in datos):
            raise ValueError("Radix Sort solo funciona con números enteros")
        
        # Manejar números negativos
        negativos = [-x for x in datos if x < 0]
        positivos = [x for x in datos if x >= 0]
        
        if negativos:
            negativos_ordenados = self._radix_sort_positivos(negativos)
            negativos_ordenados = [-x for x in reversed(negativos_ordenados)]
        else:
            negativos_ordenados = []
        
        positivos_ordenados = self._radix_sort_positivos(positivos)
        
        resultado = negativos_ordenados + positivos_ordenados
        self.registrar_paso(resultado)
        
        return resultado
    
    def _radix_sort_positivos(self, arr: List[int]) -> List[int]:
        """Radix Sort para números positivos"""
        if not arr:
            return []
        
        datos = arr.copy()
        max_valor = max(datos)
        posicion = 1
        
        self.registrar_paso(datos)
        
        while max_valor // posicion > 0:
            # Counting sort por dígito
            conteo = [0] * 10
            salida = [0] * len(datos)
            
            for num in datos:
                digito = (num // posicion) % 10
                conteo[digito] += 1
                self.comparaciones += 1
            
            for i in range(1, 10):
                conteo[i] += conteo[i - 1]
            
            for i in range(len(datos) - 1, -1, -1):
                digito = (datos[i] // posicion) % 10
                salida[conteo[digito] - 1] = datos[i]
                conteo[digito] -= 1
                self.intercambios += 1
            
            datos = salida
            self.registrar_paso(datos)
            posicion *= 10
        
        return datos


# ==================== FUNCIONES DE UTILIDAD ====================

def generar_datos_aleatorios(cantidad: int = 20, min_val: int = 1, max_val: int = 100) -> List[int]:
    """Genera una lista de números aleatorios"""
    return [random.randint(min_val, max_val) for _ in range(cantidad)]


def generar_datos_ordenados(cantidad: int = 20) -> List[int]:
    """Genera una lista ordenada ascendentemente"""
    return list(range(1, cantidad + 1))


def generar_datos_inversos(cantidad: int = 20) -> List[int]:
    """Genera una lista ordenada descendentemente"""
    return list(range(cantidad, 0, -1))


def generar_datos_casi_ordenados(cantidad: int = 20, desorden: int = 2) -> List[int]:
    """Genera una lista casi ordenada"""
    datos = list(range(1, cantidad + 1))
    for _ in range(desorden):
        i, j = random.sample(range(cantidad), 2)
        datos[i], datos[j] = datos[j], datos[i]
    return datos


def verificar_ordenado(arr: List[Any]) -> bool:
    """Verifica si una lista está ordenada"""
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


def comparar_algoritmos(algoritmos: dict, datos: List[Any], nombre_datos: str = ""):
    """Compara múltiples algoritmos de ordenamiento"""
    print("\n" + "="*80)
    print(f"COMPARATIVA DE ALGORITMOS - {nombre_datos}")
    print(f"Datos: {len(datos)} elementos")
    print("="*80)
    
    resultados = []
    
    for nombre, (algoritmo, ordenamiento) in enumerate(algoritmos.items()):
        print(f"\nEjecutando {nombre}...")
        
        datos_copia = datos.copy()
        inicio = time.time()
        
        try:
            resultado = algoritmo(datos_copia)
            fin = time.time()
            tiempo = (fin - inicio) * 1000  # Convertir a milisegundos
            
            correcto = verificar_ordenado(resultado)
            
            resultados.append({
                "nombre": nombre,
                "tiempo_ms": tiempo,
                "comparaciones": ordenamiento.comparaciones,
                "intercambios": ordenamiento.intercambios,
                "correcto": correcto,
                "pasos": len(ordenamiento.pasos)
            })
            
            estado = "✓" if correcto else "✗"
            print(f"  {estado} Tiempo: {tiempo:.2f} ms | Comp: {ordenamiento.comparaciones} | Int: {ordenamiento.intercambios} | Pasos: {len(ordenamiento.pasos)}")
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    # Mostrar ranking
    print("\n" + "-"*80)
    print("RANKING DE VELOCIDAD:")
    print("-"*80)
    
    resultados_ordenados = sorted(resultados, key=lambda x: x["tiempo_ms"])
    
    for i, res in enumerate(resultados_ordenados, 1):
        print(f"  {i}. {res['nombre']:15} - {res['tiempo_ms']:.2f} ms (Comp: {res['comparaciones']}, Int: {res['intercambios']})")
    
    return resultados


if __name__ == "__main__":
    # Prueba rápida de la librería
    ordenador = OrdenamientoInterno()
    
    datos = generar_datos_aleatorios(15, 1, 50)
    print(f"Datos originales: {datos}")
    
    resultados = {
        "Burbuja": ordenador.burbuja(datos),
        "Inserción": ordenador.insercion(datos),
        "Selección": ordenador.seleccion(datos),
        "Shell Sort": ordenador.shell_sort(datos),
        "Quick Sort": ordenador.quick_sort(datos),
        "Heap Sort": ordenador.heap_sort(datos),
        "Radix Sort": ordenador.radix_sort(datos)
    }
    
    for nombre, resultado in resultados.items():
        print(f"{nombre}: {resultado}")