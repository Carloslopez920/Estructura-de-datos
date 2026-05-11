# sorting_base.py
from typing import List, Callable
import time

class VisualizadorBase:
    """Clase base para visualización de ordenamiento"""
    
    def __init__(self):
        self.pasos = []
    
    def registrar_paso(self, arr: List[int]):
        """Registra un paso del ordenamiento"""
        self.pasos.append(arr.copy())
    
    def limpiar_pasos(self):
        """Limpia los pasos registrados"""
        self.pasos = []
    
    def medir_tiempo(self, algoritmo: Callable, datos: List[int]) -> tuple:
        """Mide el tiempo de ejecución de un algoritmo"""
        self.limpiar_pasos()
        inicio = time.time()
        resultado = algoritmo(datos.copy())
        fin = time.time()
        return resultado, fin - inicio