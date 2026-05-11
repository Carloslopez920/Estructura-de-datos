# bubble_sort.py
from typing import List
from sorting_base import VisualizadorBase

class BubbleSortVisual(VisualizadorBase):
    """Implementación del algoritmo de ordenamiento Burbuja con visualización"""
    
    def bubble_sort_visual(self, collection: List[int]) -> List[int]:
        """
        Ordenamiento Burbuja con registro de pasos
        
        Complejidad: O(n²) en el peor caso, O(n) en el mejor caso
        """
        self.limpiar_pasos()
        n = len(collection)
        
        if n <= 1:
            return collection
        
        self.registrar_paso(collection)
        
        for i in range(n - 1):
            swapped = False
            
            for j in range(0, n - i - 1):
                if collection[j] > collection[j + 1]:
                    # Intercambiar elementos
                    collection[j], collection[j + 1] = collection[j + 1], collection[j]
                    swapped = True
                    self.registrar_paso(collection)
            
            # Si no hubo intercambios, el array ya está ordenado
            if not swapped:
                break
        
        return collection

# Función de conveniencia
def bubble_sort(collection: List[int], visualizer: BubbleSortVisual = None) -> List[int]:
    """Wrapper para usar el algoritmo de burbuja"""
    if visualizer is None:
        visualizer = BubbleSortVisual()
    return visualizer.bubble_sort_visual(collection)