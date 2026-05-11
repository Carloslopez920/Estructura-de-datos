# main_completo.py
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from typing import List

# Importar librerías de ordenamiento
from sorting_base import VisualizadorBase
from bubble_sort import BubbleSortVisual
from insertion_sort import InsertionSortVisual
from selection_sort import SelectionSortVisual

# Importar el visualizador original
import sys
sys.path.append('.')
from estructuradedatos.librerias.metordenamiento import VisualizadorOrdenamiento, animar_ordenamiento, visualizar_paso_a_paso, generar_datos_aleatorios, ingresar_datos_manual

class VisualizadorCompleto:
    """Integrador de todos los algoritmos de ordenamiento"""
    
    def __init__(self):
        self.bubble_vis = BubbleSortVisual()
        self.insertion_vis = InsertionSortVisual()
        self.selection_vis = SelectionSortVisual()
        self.advanced_vis = VisualizadorOrdenamiento()
        
        # Diccionario de algoritmos
        self.algoritmos = {
            "Burbuja": self.bubble_vis.bubble_sort_visual,
            "Inserción": self.insertion_vis.insertion_sort_visual,
            "Selección": self.selection_vis.selection_sort_visual,
            "Shell": self.advanced_vis.shell_sort_visual,
            "Quick": self.advanced_vis.quick_sort_visual,
            "Radix": self.advanced_vis.radix_sort_visual,
            "Heap": self.advanced_vis.heap_sort_visual
        }
        
        self.visualizadores = {
            "Burbuja": self.bubble_vis,
            "Inserción": self.insertion_vis,
            "Selección": self.selection_vis,
            "Shell": self.advanced_vis,
            "Quick": self.advanced_vis,
            "Radix": self.advanced_vis,
            "Heap": self.advanced_vis
        }
    
    def ejecutar_algoritmo(self, nombre: str, datos: List[int]) -> tuple:
        """Ejecuta un algoritmo específico y retorna resultado y tiempo"""
        visualizador = self.visualizadores[nombre]
        algoritmo = self.algoritmos[nombre]
        
        import time
        inicio = time.time()
        resultado = algoritmo(datos.copy())
        fin = time.time()
        
        return resultado, fin - inicio, visualizador.pasos
    
    def comparar_todos(self, datos_originales: List[int]):
        """Compara todos los algoritmos disponibles"""
        print("\n" + "="*80)
        print("COMPARATIVA COMPLETA DE ALGORITMOS")
        print("="*80)
        
        resultados = {}
        
        for nombre in self.algoritmos.keys():
            print(f"\nEjecutando {nombre}...")
            try:
                resultado, tiempo, pasos = self.ejecutar_algoritmo(nombre, datos_originales)
                correcto = resultado == sorted(datos_originales)
                resultados[nombre] = {
                    "tiempo": tiempo,
                    "correcto": correcto,
                    "pasos": len(pasos)
                }
                print(f"   ✓ Completado en {tiempo:.6f} segundos - {len(pasos)} pasos")
            except Exception as e:
                print(f"   ✗ Error en {nombre}: {e}")
                resultados[nombre] = {
                    "tiempo": float('inf'),
                    "correcto": False,
                    "pasos": 0
                }
        
        # Mostrar ranking
        print("\n" + "="*80)
        print("RANKING DE VELOCIDAD")
        print("="*80)
        
        resultados_ordenados = sorted(resultados.items(), key=lambda x: x[1]["tiempo"])
        
        for i, (nombre, datos) in enumerate(resultados_ordenados, 1):
            check = "✓" if datos['correcto'] else "✗"
            tiempo_str = f"{datos['tiempo']:.6f}" if datos['tiempo'] != float('inf') else "ERROR"
            print(f"   {i}. {nombre:12} - {tiempo_str} segundos - {datos['pasos']} pasos [{check}]")
        
        return resultados


def menu_completo():
    """Menú integrado con todos los algoritmos"""
    visualizador_completo = VisualizadorCompleto()
    
    while True:
        print("\n" + "="*80)
        print("SISTEMA DE ORDENAMIENTO CON VISUALIZACIÓN - COMPLETO")
        print("="*80)
        print("\nALGORITMOS BÁSICOS:")
        print("   1. Ordenamiento Burbuja")
        print("   2. Ordenamiento por Inserción")
        print("   3. Ordenamiento por Selección")
        print("\nALGORITMOS AVANZADOS:")
        print("   4. Shell Sort")
        print("   5. Quick Sort")
        print("   6. Radix Sort")
        print("   7. Heap Sort")
        print("\nCOMPARATIVAS:")
        print("   8. Comparar TODOS los métodos (Básicos + Avanzados)")
        print("   9. Comparar solo métodos BÁSICOS")
        print("  10. Salir")
        print("="*80)
        
        opcion = input("\nElige una opción (1-10): ").strip()
        
        if opcion == "10":
            print("\nGracias por usar el programa. ¡Hasta luego!")
            plt.close('all')
            break
        
        if opcion not in [str(i) for i in range(1, 10)]:
            print("Opción inválida. Por favor, elige una opción del 1 al 10.")
            continue
        
        # Seleccionar método de entrada de datos
        print("\n¿Cómo quieres proporcionar los datos?")
        print("1. Generar números aleatorios")
        print("2. Ingresar manualmente")
        
        metodo_entrada = input("Elige una opción (1-2): ").strip()
        
        if metodo_entrada == "1":
            datos_originales = generar_datos_aleatorios()
        elif metodo_entrada == "2":
            datos_originales = ingresar_datos_manual()
        else:
            print("Opción inválida. Volviendo al menú principal...")
            continue
        
        if not datos_originales:
            continue
        
        # Mapeo de opciones a algoritmos
        opcion_algoritmo = {
            "1": "Burbuja",
            "2": "Inserción",
            "3": "Selección",
            "4": "Shell",
            "5": "Quick",
            "6": "Radix",
            "7": "Heap"
        }
        
        if opcion in opcion_algoritmo:
            nombre_algoritmo = opcion_algoritmo[opcion]
            print(f"\nEjecutando {nombre_algoritmo}...")
            
            resultado, tiempo, pasos = visualizador_completo.ejecutar_algoritmo(nombre_algoritmo, datos_originales)
            
            # Mostrar resultados
            print("\n" + "="*60)
            print(f"RESULTADOS - {nombre_algoritmo}")
            print("="*60)
            
            print(f"\nDATOS ORIGINALES ({len(datos_originales)} elementos):")
            if len(datos_originales) <= 20:
                print(f"   {datos_originales}")
            else:
                print(f"   {datos_originales[:10]} ... {datos_originales[-10:]}")
            
            print(f"\nDATOS ORDENADOS:")
            if len(resultado) <= 20:
                print(f"   {resultado}")
            else:
                print(f"   {resultado[:10]} ... {resultado[-10:]}")
            
            print(f"\nTIEMPO DE EJECUCIÓN: {tiempo:.6f} segundos")
            print(f"TOTAL DE PASOS: {len(pasos)}")
            
            # Verificar ordenamiento
            esta_ordenado = resultado == sorted(datos_originales)
            print(f"\nVERIFICACIÓN: {'✓ CORRECTO' if esta_ordenado else '✗ INCORRECTO'}")
            
            # Opciones de visualización
            print("\nOpciones de visualización:")
            print("1. Ver animación completa")
            print("2. Ver proceso paso a paso")
            print("3. Ver ambas")
            print("4. Omitir visualización")
            
            visual_opcion = input("Elige una opción (1-4): ").strip()
            
            if visual_opcion == "1":
                animar_ordenamiento(datos_originales, pasos, nombre_algoritmo, interval=150)
            elif visual_opcion == "2":
                visualizar_paso_a_paso(datos_originales, pasos, nombre_algoritmo)
            elif visual_opcion == "3":
                visualizar_paso_a_paso(datos_originales, pasos, nombre_algoritmo)
                animar_ordenamiento(datos_originales, pasos, nombre_algoritmo, interval=150)
        
        elif opcion == "8":  # Comparar todos
            print("\n" + "="*60)
            print("COMPARANDO TODOS LOS ALGORITMOS")
            print("="*60)
            visualizador_completo.comparar_todos(datos_originales)
            
            # Preguntar qué visualizar
            print("\n¿Qué método quieres visualizar?")
            print("1. Burbuja")
            print("2. Inserción")
            print("3. Selección")
            print("4. Shell")
            print("5. Quick")
            print("6. Radix")
            print("7. Heap")
            print("8. El más rápido")
            print("9. Ninguno")
            
            ver_opcion = input("Elige una opción (1-9): ").strip()
            
            if ver_opcion in [str(i) for i in range(1, 8)]:
                nombres = ["Burbuja", "Inserción", "Selección", "Shell", "Quick", "Radix", "Heap"]
                nombre = nombres[int(ver_opcion) - 1]
                resultado, tiempo, pasos = visualizador_completo.ejecutar_algoritmo(nombre, datos_originales)
                visualizar_paso_a_paso(datos_originales, pasos, nombre)
                animar_ordenamiento(datos_originales, pasos, nombre, interval=150)
            elif ver_opcion == "8":
                # Encontrar el más rápido
                resultados = visualizador_completo.comparar_todos(datos_originales)
                nombre_rapido = min(resultados.items(), key=lambda x: x[1]["tiempo"])[0]
                print(f"\nVisualizando el método más rápido: {nombre_rapido}")
                resultado, tiempo, pasos = visualizador_completo.ejecutar_algoritmo(nombre_rapido, datos_originales)
                visualizar_paso_a_paso(datos_originales, pasos, nombre_rapido)
                animar_ordenamiento(datos_originales, pasos, nombre_rapido, interval=150)
        
        elif opcion == "9":  # Comparar solo básicos
            print("\n" + "="*60)
            print("COMPARANDO MÉTODOS BÁSICOS")
            print("Burbuja vs Inserción vs Selección")
            print("="*60)
            
            basicos = ["Burbuja", "Inserción", "Selección"]
            resultados = {}
            
            for nombre in basicos:
                print(f"\nEjecutando {nombre}...")
                resultado, tiempo, pasos = visualizador_completo.ejecutar_algoritmo(nombre, datos_originales)
                correcto = resultado == sorted(datos_originales)
                resultados[nombre] = {
                    "tiempo": tiempo,
                    "correcto": correcto,
                    "pasos": len(pasos)
                }
                print(f"   ✓ Completado en {tiempo:.6f} segundos - {len(pasos)} pasos")
            
            print("\n" + "="*60)
            print("COMPARATIVA DE MÉTODOS BÁSICOS")
            print("="*60)
            
            resultados_ordenados = sorted(resultados.items(), key=lambda x: x[1]["tiempo"])
            
            for i, (nombre, datos) in enumerate(resultados_ordenados, 1):
                check = "✓" if datos['correcto'] else "✗"
                print(f"   {i}. {nombre:12} - {datos['tiempo']:.6f} segundos - {datos['pasos']} pasos [{check}]")
        
        input("\nPresiona Enter para continuar...")


# Archivo de demostración rápida
def demo_rapida():
    """Demostración rápida de todos los algoritmos"""
    print("\n" + "="*80)
    print("DEMOSTRACIÓN RÁPIDA")
    print("="*80)
    
    # Datos de prueba
    datos_prueba = [64, 34, 25, 12, 22, 11, 90]
    print(f"\nDatos originales: {datos_prueba}")
    
    visualizador = VisualizadorCompleto()
    
    print("\nEjecutando todos los algoritmos...")
    print("-" * 60)
    
    for nombre in visualizador.algoritmos.keys():
        resultado, tiempo, pasos = visualizador.ejecutar_algoritmo(nombre, datos_prueba)
        print(f"{nombre:12} → {resultado} (tiempo: {tiempo:.6f}s, pasos: {len(pasos)})")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    print("="*80)
    print("SISTEMA COMPLETO DE ORDENAMIENTO CON VISUALIZACIÓN")
    print("="*80)
    
    # Verificar dependencias
    try:
        import matplotlib
        print("✓ Matplotlib instalado correctamente")
    except ImportError:
        print("\n✗ ERROR: Falta matplotlib")
        print("  Instálalo con: pip install matplotlib")
        exit(1)
    
    print("\nOpciones:")
    print("1. Menú completo (todos los algoritmos)")
    print("2. Demostración rápida")
    
    opcion_inicial = input("\nElige una opción (1-2): ").strip()
    
    if opcion_inicial == "2":
        demo_rapida()
    else:
        menu_completo()
    