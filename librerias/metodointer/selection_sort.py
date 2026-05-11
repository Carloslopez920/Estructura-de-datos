# selection_sort.py
from typing import List
from sorting_base import VisualizadorBase

class SelectionSortVisual(VisualizadorBase):
    """Implementación del algoritmo de ordenamiento por Selección con visualización"""
    
    def selection_sort_visual(self, collection: List[int]) -> List[int]:
        """
        Ordenamiento por Selección con registro de pasos
        
        Complejidad: O(n²) en todos los casos
        """
        self.limpiar_pasos()
        n = len(collection)
        
        if n <= 1:
            return collection
        
        self.registrar_paso(collection)
        
        for i in range(n):
            # Encontrar el mínimo en la porción no ordenada
            min_idx = i
            
            for j in range(i + 1, n):
                if collection[j] < collection[min_idx]:
                    min_idx = j
            
            # Intercambiar si es necesario
            if min_idx != i:
                collection[i], collection[min_idx] = collection[min_idx], collection[i]
                self.registrar_paso(collection)
        
        return collection

# Función de conveniencia
def selection_sort(collection: List[int], visualizer: SelectionSortVisual = None) -> List[int]:
    """Wrapper para usar el algoritmo de selección"""
    if visualizer is None:
        visualizer = SelectionSortVisual()
    return visualizer.selection_sort_visual(collection)