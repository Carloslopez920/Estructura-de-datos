# insertion_sort.py
from typing import List
from sorting_base import VisualizadorBase

class InsertionSortVisual(VisualizadorBase):
    """Implementación del algoritmo de ordenamiento por Inserción con visualización"""
    
    def insertion_sort_visual(self, collection: List[int]) -> List[int]:
        """
        Ordenamiento por Inserción con registro de pasos
        
        Complejidad: O(n²) en el peor caso, O(n) en el mejor caso
        """
        self.limpiar_pasos()
        n = len(collection)
        
        if n <= 1:
            return collection
        
        self.registrar_paso(collection)
        
        for i in range(1, n):
            key = collection[i]
            j = i - 1
            
            # Mover elementos mayores que key una posición adelante
            while j >= 0 and collection[j] > key:
                collection[j + 1] = collection[j]
                j -= 1
                self.registrar_paso(collection)
            
            collection[j + 1] = key
            self.registrar_paso(collection)
        
        return collection

# Función de conveniencia
def insertion_sort(collection: List[int], visualizer: InsertionSortVisual = None) -> List[int]:
    """Wrapper para usar el algoritmo de inserción"""
    if visualizer is None:
        visualizer = InsertionSortVisual()
    return visualizer.insertion_sort_visual(collection)