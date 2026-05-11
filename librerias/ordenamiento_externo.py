# ==================== LIBRERÍA DE ORDENAMIENTO EXTERNO ====================
# archivo: ordenamiento_externo.py

import os
import tempfile
import shutil
from typing import List, Any, Callable, Optional
import time


class OrdenamientoExterno:
    """
    Clase que contiene los algoritmos de ordenamiento externo
    Estos algoritmos son útiles cuando los datos no caben en memoria RAM
    """
    
    def __init__(self):
        self.comparaciones = 0
        self.lecturas = 0
        self.escrituras = 0
        self.temp_files = []
        self.pasos = []  # Para registro de fases
    
    def reiniciar_contadores(self):
        """Reinicia los contadores de operaciones"""
        self.comparaciones = 0
        self.lecturas = 0
        self.escrituras = 0
        self.pasos = []
    
    def registrar_paso(self, descripcion: str, datos: List[Any] = None):
        """Registra un paso del ordenamiento externo"""
        self.pasos.append({
            "descripcion": descripcion,
            "datos": datos.copy() if datos else None,
            "comparaciones": self.comparaciones,
            "lecturas": self.lecturas,
            "escrituras": self.escrituras
        })
    
    def limpiar_temp_files(self):
        """Limpia los archivos temporales creados"""
        for archivo in self.temp_files:
            try:
                if os.path.exists(archivo):
                    os.remove(archivo)
            except:
                pass
        self.temp_files = []
    
    def _crear_archivo_temp(self, datos: List[Any], nombre_base: str = "temp") -> str:
        """Crea un archivo temporal con los datos"""
        fd, path = tempfile.mkstemp(suffix=".txt", prefix=f"{nombre_base}_")
        os.close(fd)
        
        with open(path, 'w', encoding='utf-8') as f:
            for elemento in datos:
                f.write(f"{elemento}\n")
                self.escrituras += 1
        
        self.temp_files.append(path)
        return path
    
    def _leer_archivo_temp(self, path: str) -> List[Any]:
        """Lee datos desde un archivo temporal"""
        datos = []
        with open(path, 'r', encoding='utf-8') as f:
            for linea in f:
                linea = linea.strip()
                if linea:
                    try:
                        # Intentar convertir a número
                        if '.' in linea:
                            datos.append(float(linea))
                        else:
                            datos.append(int(linea))
                    except ValueError:
                        datos.append(linea)
                self.lecturas += 1
        return datos
    
    def _escribir_bloque(self, archivo, bloque: List[Any]):
        """Escribe un bloque de datos en un archivo"""
        for elem in bloque:
            archivo.write(f"{elem}\n")
            self.escrituras += 1
    
    # ==================== INTERCALACIÓN (MERGE) ====================
    def intercalacion(self, arr1: List[Any], arr2: List[Any], 
                      comparador: Callable = None) -> List[Any]:
        """
        Intercalación (Merge) de dos listas ordenadas
        Complejidad: O(n + m)
        
        Este algoritmo combina dos listas ya ordenadas en una sola ordenada.
        Es la base de los otros algoritmos externos.
        """
        self.reiniciar_contadores()
        
        if comparador is None:
            comparador = lambda a, b: (a > b) - (a < b)
        
        resultado = []
        i = j = 0
        
        self.registrar_paso("Iniciando intercalación")
        
        while i < len(arr1) and j < len(arr2):
            self.comparaciones += 1
            if comparador(arr1[i], arr2[j]) <= 0:
                resultado.append(arr1[i])
                i += 1
            else:
                resultado.append(arr2[j])
                j += 1
            self.registrar_paso(f"Intercalando... i={i}, j={j}", resultado)
        
        # Agregar elementos restantes
        resultado.extend(arr1[i:])
        resultado.extend(arr2[j:])
        
        self.registrar_paso("Intercalación completada", resultado)
        
        return resultado
    
    def intercalacion_multiple(self, listas: List[List[Any]], 
                                comparador: Callable = None) -> List[Any]:
        """
        Intercalación múltiple (fusiona múltiples listas ordenadas)
        """
        if comparador is None:
            comparador = lambda a, b: (a > b) - (a < b)
        
        if not listas:
            return []
        
        if len(listas) == 1:
            return listas[0].copy()
        
        # Fusionar por pares
        while len(listas) > 1:
            nuevas_listas = []
            for i in range(0, len(listas), 2):
                if i + 1 < len(listas):
                    fusion = self.intercalacion(listas[i], listas[i + 1], comparador)
                    nuevas_listas.append(fusion)
                else:
                    nuevas_listas.append(listas[i])
            listas = nuevas_listas
        
        return listas[0]
    
    # ==================== MEZCLA DIRECTA ====================
    def mezcla_directa(self, datos: List[Any], 
                       tamano_bloque: int = 100,
                       comparador: Callable = None) -> List[Any]:
        """
        Mezcla Directa (Straight Merge Sort)
        
        Divide el archivo en bloques del tamaño de memoria disponible,
        ordena cada bloque internamente, y luego los fusiona.
        
        Args:
            datos: Lista de datos a ordenar
            tamano_bloque: Tamaño máximo de bloque que cabe en memoria
            comparador: Función de comparación
        
        Returns:
            Lista ordenada
        """
        self.reiniciar_contadores()
        
        if comparador is None:
            comparador = lambda a, b: (a > b) - (a < b)
        
        if len(datos) <= tamano_bloque:
            # Si cabe en memoria, ordenar internamente
            datos.sort(key=lambda x: x if isinstance(x, (int, float)) else str(x))
            return datos
        
        # FASE 1: Crear bloques ordenados
        bloques = []
        ordenador_interno = type('obj', (object,), {
            'comparaciones': 0,
            'intercambios': 0
        })()
        
        for i in range(0, len(datos), tamano_bloque):
            bloque = datos[i:i + tamano_bloque]
            # Ordenar bloque internamente (usando bubble sort simple para demostración)
            for j in range(len(bloque)):
                for k in range(len(bloque) - 1 - j):
                    self.comparaciones += 1
                    if comparador(bloque[k], bloque[k + 1]) > 0:
                        bloque[k], bloque[k + 1] = bloque[k + 1], bloque[k]
            bloques.append(bloque)
            self.registrar_paso(f"Bloque {len(bloques)} ordenado", bloque)
        
        # FASE 2: Fusionar bloques
        while len(bloques) > 1:
            nuevos_bloques = []
            for i in range(0, len(bloques), 2):
                if i + 1 < len(bloques):
                    fusion = self.intercalacion(bloques[i], bloques[i + 1], comparador)
                    nuevos_bloques.append(fusion)
                    self.registrar_paso(f"Fusionando bloques {i} y {i+1}", fusion[:20])
                else:
                    nuevos_bloques.append(bloques[i])
            bloques = nuevos_bloques
        
        resultado = bloques[0] if bloques else []
        self.registrar_paso("Mezcla Directa completada", resultado[:50])
        
        return resultado
    
    # ==================== MEZCLA EQUILIBRADA ====================
    def mezcla_equilibrada(self, datos: List[Any],
                           tamano_bloque: int = 100,
                           comparador: Callable = None) -> List[Any]:
        """
        Mezcla Equilibrada (Balanced Merge Sort)
        
        Utiliza múltiples archivos de trabajo (generalmente 4: f1, f2, f3, f4)
        para distribuir los bloques y fusionarlos de manera equilibrada.
        
        Simula el proceso usando archivos temporales.
        """
        self.reiniciar_contadores()
        
        if comparador is None:
            comparador = lambda a, b: (a > b) - (a < b)
        
        if len(datos) <= tamano_bloque:
            datos.sort(key=lambda x: x if isinstance(x, (int, float)) else str(x))
            return datos
        
        # Limpiar archivos temporales previos
        self.limpiar_temp_files()
        
        # FASE 1: Crear bloques ordenados iniciales
        bloques = []
        for i in range(0, len(datos), tamano_bloque):
            bloque = datos[i:i + tamano_bloque]
            bloque.sort(key=lambda x: x if isinstance(x, (int, float)) else str(x))
            bloques.append(bloque)
            self.registrar_paso(f"Bloque inicial {len(bloques)}", bloque[:10])
        
        # Simular archivos de trabajo
        archivos_trabajo = [[], []]  # f1, f2
        distribucion = 0
        
        # Distribuir bloques iniciales
        for i, bloque in enumerate(bloques):
            archivos_trabajo[i % 2].append(bloque)
        
        fase = 1
        while len(archivos_trabajo[0]) > 1 or len(archivos_trabajo[1]) > 1:
            nuevos_archivos = [[], []]
            
            # Fusionar bloques de archivos de trabajo
            for i in range(2):  # Para f1 y f2
                bloques_actual = archivos_trabajo[i]
                for j in range(0, len(bloques_actual), 2):
                    if j + 1 < len(bloques_actual):
                        fusion = self.intercalacion(bloques_actual[j], 
                                                     bloques_actual[j + 1], 
                                                     comparador)
                        nuevos_archivos[i // 2].append(fusion)  # Distribuir alternadamente
                        self.registrar_paso(f"Fase {fase}: Fusionando en archivo {i//2}", fusion[:10])
                    else:
                        nuevos_archivos[i // 2].append(bloques_actual[j])
            
            archivos_trabajo = nuevos_archivos
            fase += 1
        
        # El resultado está en uno de los archivos
        resultado = archivos_trabajo[0][0] if archivos_trabajo[0] else archivos_trabajo[1][0]
        
        self.limpiar_temp_files()
        self.registrar_paso("Mezcla Equilibrada completada", resultado[:50])
        
        return resultado
    
    # ==================== MEZCLA NATURAL ====================
    def mezcla_natural(self, datos: List[Any],
                       comparador: Callable = None) -> List[Any]:
        """
        Mezcla Natural (Natural Merge Sort)
        
        Aprovecha las secuencias ya ordenadas (runs) presentes en los datos
        en lugar de dividir en bloques de tamaño fijo.
        """
        self.reiniciar_contadores()
        
        if comparador is None:
            comparador = lambda a, b: (a > b) - (a < b)
        
        if len(datos) <= 1:
            return datos.copy()
        
        # Detectar runs (secuencias ordenadas)
        def encontrar_runs(arr):
            runs = []
            run_actual = [arr[0]]
            
            for i in range(1, len(arr)):
                self.comparaciones += 1
                if comparador(arr[i - 1], arr[i]) <= 0:
                    run_actual.append(arr[i])
                else:
                    runs.append(run_actual)
                    run_actual = [arr[i]]
            
            runs.append(run_actual)
            return runs
        
        runs = encontrar_runs(datos)
        self.registrar_paso(f"Runs encontrados: {len(runs)}", [len(r) for r in runs[:5]])
        
        # Fusionar runs hasta tener una sola
        while len(runs) > 1:
            nuevas_runs = []
            for i in range(0, len(runs), 2):
                if i + 1 < len(runs):
                    fusion = self.intercalacion(runs[i], runs[i + 1], comparador)
                    nuevas_runs.append(fusion)
                    self.registrar_paso(f"Fusionando runs {i} y {i+1}", fusion[:10])
                else:
                    nuevas_runs.append(runs[i])
            runs = nuevas_runs
        
        resultado = runs[0] if runs else []
        self.registrar_paso("Mezcla Natural completada", resultado[:50])
        
        return resultado
    
    # ==================== ORDENAMIENTO POR MEZCLA EN ARCHIVOS ====================
    def ordenar_archivo_grande(self, archivo_entrada: str, archivo_salida: str,
                                tamano_memoria: int = 1000,
                                tipo_dato: str = "numeros") -> bool:
        """
        Ordena un archivo grande que no cabe en memoria
        
        Args:
            archivo_entrada: Ruta del archivo a ordenar
            archivo_salida: Ruta donde guardar el resultado
            tamano_memoria: Cantidad máxima de elementos a cargar en memoria
            tipo_dato: "numeros" o "texto"
        
        Returns:
            True si la operación fue exitosa
        """
        self.reiniciar_contadores()
        self.limpiar_temp_files()
        
        try:
            # FASE 1: Leer el archivo en bloques, ordenar y escribir a archivos temporales
            archivos_temp = []
            
            with open(archivo_entrada, 'r', encoding='utf-8') as f:
                bloque = []
                for linea in f:
                    linea = linea.strip()
                    if linea:
                        if tipo_dato == "numeros":
                            try:
                                if '.' in linea:
                                    valor = float(linea)
                                else:
                                    valor = int(linea)
                            except:
                                valor = linea
                        else:
                            valor = linea
                        
                        bloque.append(valor)
                        self.lecturas += 1
                    
                    if len(bloque) >= tamano_memoria:
                        # Ordenar bloque
                        bloque.sort(key=lambda x: x if isinstance(x, (int, float)) else str(x))
                        # Guardar a archivo temporal
                        temp_path = self._crear_archivo_temp(bloque, "bloque")
                        archivos_temp.append(temp_path)
                        bloque = []
                
                # Procesar último bloque
                if bloque:
                    bloque.sort(key=lambda x: x if isinstance(x, (int, float)) else str(x))
                    temp_path = self._crear_archivo_temp(bloque, "bloque")
                    archivos_temp.append(temp_path)
            
            # FASE 2: Fusionar archivos temporales
            while len(archivos_temp) > 1:
                nuevos_temp = []
                for i in range(0, len(archivos_temp), 2):
                    if i + 1 < len(archivos_temp):
                        # Leer ambos archivos
                        datos1 = self._leer_archivo_temp(archivos_temp[i])
                        datos2 = self._leer_archivo_temp(archivos_temp[i + 1])
                        
                        # Fusionar
                        fusion = self.intercalacion(datos1, datos2)
                        
                        # Guardar a nuevo archivo temporal
                        temp_path = self._crear_archivo_temp(fusion, "fusion")
                        nuevos_temp.append(temp_path)
                        
                        # Eliminar archivos viejos
                        os.remove(archivos_temp[i])
                        os.remove(archivos_temp[i + 1])
                    else:
                        nuevos_temp.append(archivos_temp[i])
                
                archivos_temp = nuevos_temp
            
            # FASE 3: Escribir resultado final
            if archivos_temp:
                datos_ordenados = self._leer_archivo_temp(archivos_temp[0])
                
                with open(archivo_salida, 'w', encoding='utf-8') as f:
                    for elem in datos_ordenados:
                        f.write(f"{elem}\n")
                        self.escrituras += 1
                
                os.remove(archivos_temp[0])
            
            self.limpiar_temp_files()
            self.registrar_paso(f"Archivo ordenado guardado en {archivo_salida}")
            
            return True
            
        except Exception as e:
            print(f"Error en ordenar_archivo_grande: {e}")
            self.limpiar_temp_files()
            return False


# ==================== FUNCIONES DE UTILIDAD ====================

def generar_datos_prueba_externos(cantidad: int = 1000, archivo: str = "datos_prueba.txt"):
    """Genera un archivo de prueba con datos aleatorios"""
    import random
    
    with open(archivo, 'w', encoding='utf-8') as f:
        for _ in range(cantidad):
            f.write(f"{random.randint(1, 10000)}\n")
    
    print(f"Archivo de prueba generado: {archivo} ({cantidad} elementos)")


if __name__ == "__main__":
    # Prueba rápida de la librería
    ordenador_ext = OrdenamientoExterno()
    
    # Datos de prueba
    datos1 = [1, 3, 5, 7, 9]
    datos2 = [2, 4, 6, 8, 10]
    
    print("Intercalación:")
    resultado = ordenador_ext.intercalacion(datos1, datos2)
    print(f"  {datos1} + {datos2} = {resultado}")
    
    datos_desordenados = [64, 34, 25, 12, 22, 11, 90, 5, 77, 30]
    print(f"\nDatos desordenados: {datos_desordenados}")
    
    print("\nMezcla Directa (tamaño bloque=3):")
    resultado = ordenador_ext.mezcla_directa(datos_desordenados, tamano_bloque=3)
    print(f"  Resultado: {resultado}")
    
    print("\nMezcla Equilibrada (tamaño bloque=3):")
    resultado = ordenador_ext.mezcla_equilibrada(datos_desordenados, tamano_bloque=3)
    print(f"  Resultado: {resultado}")
    
    print("\nMezcla Natural:")
    resultado = ordenador_ext.mezcla_natural(datos_desordenados)
    print(f"  Resultado: {resultado}")