# external_sorting.py
import time
from typing import List, Any, Callable, Dict, Optional
from data_processor import DataProcessor

class ExternalSortingAlgorithms:
    """Implementación de algoritmos de ordenamiento externo"""
    
    def __init__(self, data_type: str = "numeros"):
        self.data_type = data_type
        self.comparator = lambda a, b: DataProcessor.compare_elements(a, b, data_type)
    
    def mezcla_directa(self, data: List[Any], callback: Optional[Callable] = None) -> Dict:
        """
        Algoritmo de Mezcla Directa (Direct Merge Sort)
        
        Complejidad: O(n log n)
        """
        inicio = time.time()
        datos = data.copy()
        paso = 1
        comparaciones = 0
        
        if callback:
            callback(datos, f"Inicio - tamaño bloque: {paso}", comparaciones, 0)
        
        while paso < len(datos):
            for i in range(0, len(datos), paso * 2):
                izquierda = datos[i:i + paso]
                derecha = datos[i + paso:i + paso * 2]
                mezclados = []
                a, b = 0, 0
                
                while a < len(izquierda) and b < len(derecha):
                    comparaciones += 1
                    if self.comparator(izquierda[a], derecha[b]) < 0:
                        mezclados.append(izquierda[a])
                        a += 1
                    else:
                        mezclados.append(derecha[b])
                        b += 1
                
                mezclados.extend(izquierda[a:])
                mezclados.extend(derecha[b:])
                datos[i:i + paso * 2] = mezclados
            
            paso *= 2
            
            if callback:
                callback(datos, f"Mezclando - tamaño bloque: {paso}", comparaciones, (time.time() - inicio) * 1000)
        
        tiempo_ms = (time.time() - inicio) * 1000
        
        return {
            "datos": datos,
            "comparaciones": comparaciones,
            "tiempo_ms": tiempo_ms,
            "nombre": "Mezcla Directa"
        }
    
    def mezcla_equilibrada(self, data: List[Any], callback: Optional[Callable] = None) -> Dict:
        """
        Algoritmo de Mezcla Equilibrada (Balanced Merge Sort)
        
        Complejidad: O(n log n)
        """
        inicio = time.time()
        comparaciones = [0]
        
        if callback:
            callback(data, "Dividiendo lista...", 0, 0)
        
        def merge_sort_recursive(arr: List[Any], depth: int = 0) -> List[Any]:
            if len(arr) <= 1:
                return arr
            
            mid = len(arr) // 2
            left = merge_sort_recursive(arr[:mid], depth + 1)
            right = merge_sort_recursive(arr[mid:], depth + 1)
            
            result = []
            i = j = 0
            while i < len(left) and j < len(right):
                comparaciones[0] += 1
                if self.comparator(left[i], right[j]) < 0:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            
            result.extend(left[i:])
            result.extend(right[j:])
            
            if callback and depth % 3 == 0:
                callback(result, f"Mezclando nivel {depth}...", comparaciones[0], (time.time() - inicio) * 1000)
            
            return result
        
        datos_ordenados = merge_sort_recursive(data)
        tiempo_ms = (time.time() - inicio) * 1000
        
        if callback:
            callback(datos_ordenados, "COMPLETADO", comparaciones[0], tiempo_ms)
        
        return {
            "datos": datos_ordenados,
            "comparaciones": comparaciones[0],
            "tiempo_ms": tiempo_ms,
            "nombre": "Mezcla Equilibrada"
        }
    
    def intercalacion(self, data: List[Any], callback: Optional[Callable] = None) -> Dict:
        """
        Algoritmo de Intercalación (Interpolation Sort / Block Sort)
        
        Complejidad: O(n log n) en promedio
        """
        inicio = time.time()
        datos = data.copy()
        k = 2
        comparaciones = 0
        
        if callback:
            callback(datos, f"Inicio - bloque tamaño: {k//2}", comparaciones, 0)
        
        while k <= len(datos):
            for i in range(0, len(datos), k):
                sublista = datos[i:i + k]
                # Ordenar la sublista
                sublista.sort(key=lambda x: str(x) if self.data_type != "numeros" else x)
                comparaciones += len(sublista) * (len(sublista) - 1) // 2
                datos[i:i + k] = sublista
            
            if callback:
                callback(datos, f"Intercalando - bloque tamaño: {k}", comparaciones, (time.time() - inicio) * 1000)
            
            if k >= len(datos):
                break
            k *= 2
        
        # Ordenamiento final si es necesario
        if k > len(datos) and len(datos) > 2:
            datos.sort(key=lambda x: str(x) if self.data_type != "numeros" else x)
            if callback:
                callback(datos, "Ordenando resto...", comparaciones, (time.time() - inicio) * 1000)
        
        tiempo_ms = (time.time() - inicio) * 1000
        
        if callback:
            callback(datos, "COMPLETADO", comparaciones, tiempo_ms)
        
        return {
            "datos": datos,
            "comparaciones": comparaciones,
            "tiempo_ms": tiempo_ms,
            "nombre": "Intercalación"
        }
    
    @staticmethod
    def get_algorithms_info() -> Dict[str, Dict]:
        """Obtener información de los algoritmos disponibles"""
        return {
            "mezcla_directa": {
                "nombre": "Mezcla Directa",
                "complejidad": "O(n log n)",
                "descripcion": "Divide la lista en bloques pequeños y los mezcla iterativamente",
                "color": "#9b59b6"
            },
            "mezcla_equilibrada": {
                "nombre": "Mezcla Equilibrada",
                "complejidad": "O(n log n)",
                "descripcion": "Divide recursivamente y mezcla de forma equilibrada",
                "color": "#e74c3c"
            },
            "intercalacion": {
                "nombre": "Intercalación",
                "complejidad": "O(n log n)",
                "descripcion": "Ordena bloques y los intercala progresivamente",
                "color": "#16a085"
            }
        }
    
    def execute_all(self, data: List[Any], callback: Optional[Callable] = None) -> Dict[str, Dict]:
        """Ejecutar todos los algoritmos y devolver resultados"""
        results = {}
        
        algorithms = [
            ("mezcla_directa", self.mezcla_directa),
            ("mezcla_equilibrada", self.mezcla_equilibrada),
            ("intercalacion", self.intercalacion)
        ]
        
        for name, algorithm in algorithms:
            results[name] = algorithm(data, callback)
        
        return results