import time

def medir_tiempo_ejecucion(func, n, nombre=""):
    """
    Mide el tiempo de ejecución de una función
    """
    inicio = time.perf_counter()
    resultado = func(n)
    fin = time.perf_counter()
    tiempo = fin - inicio
    
    print(f"{nombre}:")
    print(f"  Resultado F({n}) = {resultado}")
    print(f"  Tiempo: {tiempo:.10f} segundos")
    print(f"  Tiempo: {tiempo*1000:.6f} milisegundos")
    print(f"  Tiempo: {tiempo*1000000:.2f} microsegundos")
    print()
    
    return resultado, tiempo

def fibonacci_iterativo(n):
    """
    Versión iterativa - Eficiente O(n)
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def fibonacci_recursivo(n):
    """
    Versión recursiva - Ineficiente O(2^n)
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci_recursivo(n-1) + fibonacci_recursivo(n-2)

def estimar_tiempo_recursivo(n):
    """
    Estima el tiempo aproximado para el método recursivo basado en experiencias previas
    """
    if n <= 30:
        return "menos de 1 segundo"
    elif n <= 35:
        return "aproximadamente 0.5-1 segundo"
    elif n <= 40:
        return "aproximadamente 5-10 segundos"
    elif n <= 45:
        return "aproximadamente 1-2 minutos"
    elif n <= 50:
        return "aproximadamente 10-15 minutos"
    else:
        return f"potencialmente horas (2^{n-30} veces más que n=30)"

def comparar_metodos(n):
    """
    Compara los tiempos de ejecución entre método iterativo y recursivo
    """
    print("=" * 70)
    print(f"COMPARACIÓN DIRECTA: FIBONACCI({n})")
    print("=" * 70)
    
    # Método iterativo (siempre se ejecuta)
    resultado_iter, tiempo_iter = medir_tiempo_ejecucion(fibonacci_iterativo, n, "🔵 MÉTODO ITERATIVO")
    
    # Método recursivo con advertencia y opción de elegir
    ejecutar_recursivo = True
    
    if n > 35:
        print("\n" + "!" * 70)
        print("⚠️  ADVERTENCIA: MÉTODO RECURSIVO PARA VALOR GRANDE ⚠️")
        print("!" * 70)
        print(f"Has solicitado calcular Fibonacci({n}) de forma RECURSIVA.")
        print(f"📊 ESTIMACIÓN DE TIEMPO: {estimar_tiempo_recursivo(n)}")
        print("\nConsecuencias:")
        print("  • Tu computadora podría ralentizarse significativamente")
        print("  • El programa podría tardar mucho tiempo en responder")
        
        respuesta = input("\n¿Estás SEGURO de que quieres continuar? (s/n): ")
        if respuesta.lower() != 's':
            ejecutar_recursivo = False
            print("\n🔴 MÉTODO RECURSIVO: Cancelado por el usuario")
    
    if ejecutar_recursivo:
        try:
            resultado_rec, tiempo_rec = medir_tiempo_ejecucion(fibonacci_recursivo, n, "🔴 MÉTODO RECURSIVO")
            
            # Calcular diferencias
            diferencia = tiempo_rec / tiempo_iter
            print(f"\n📊 ANÁLISIS COMPARATIVO:")
            print(f"   El método recursivo es {diferencia:.2f} veces más lento que el iterativo")
            
            if tiempo_rec > 5:
                print(f"   ⏱️  Tiempo total de espera: {tiempo_rec:.2f} segundos")
        except RecursionError:
            print(f"\n❌ ERROR: Límite de recursión excedido para n={n}")
            print("   Python tiene un límite de profundidad de recursión")
            print("   Para valores muy grandes, el método recursivo no es viable")
    else:
        print("\n💡 Puedes probar con un valor más pequeño para ver la diferencia")

def probar_rango_valores(inicio, fin, paso=1):
    """
    Prueba ambos métodos con un rango de valores
    """
    print("\n" + "=" * 100)
    print("PRUEBA DE RENDIMIENTO PARA MÚLTIPLES VALORES")
    print("=" * 100)
    print(f"{'n':<5} {'Iterativo (s)':<20} {'Recursivo (s)':<20} {'Diferencia':<15} {'Estado':<15}")
    print("-" * 100)
    
    for n in range(inicio, fin + 1, paso):
        # Tiempo iterativo
        inicio_iter = time.perf_counter()
        fibonacci_iterativo(n)
        tiempo_iter = time.perf_counter() - inicio_iter
        
        # Tiempo recursivo con advertencia para cada valor
        if n <= 35:
            try:
                inicio_rec = time.perf_counter()
                fibonacci_recursivo(n)
                tiempo_rec = time.perf_counter() - inicio_rec
                diferencia = f"{tiempo_rec/tiempo_iter:.1f}x"
                estado = "✅ OK"
                tiempo_rec_str = f"{tiempo_rec:.10f}"
            except RecursionError:
                tiempo_rec_str = "ERROR"
                diferencia = "N/A"
                estado = "❌ Recursión"
        else:
            tiempo_rec_str = "No ejecutado"
            diferencia = "N/A"
            estado = "⚠️  >35"
        
        print(f"{n:<5} {tiempo_iter:.10f}  {tiempo_rec_str:<20} {diferencia:<15} {estado:<15}")

def mostrar_advertencias_detalladas():
    """
    Muestra información detallada sobre los riesgos de recursión para valores grandes
    """
    print("\n" + "=" * 70)
    print("📋 INFORMACIÓN DETALLADA SOBRE RECURSIÓN")
    print("=" * 70)
    print("\n🔴 LÍMITES DEL MÉTODO RECURSIVO:")
    print("   • n ≤ 35:  Seguro y rápido (< 1 segundo)")
    print("   • 35 < n ≤ 40:  Lento pero manejable (5-30 segundos)")
    print("   • 40 < n ≤ 45:  Muy lento (minutos)")
    print("   • n > 45:  Extremadamente lento (horas o días)")
    
    print("\n⚙️  FACTORES TÉCNICOS:")
    print("   • Límite de recursión de Python: ~1000 llamadas")
    print(f"   • Para n=50, se necesitan aproximadamente 2^50 llamadas")
    print("   • La memoria se agotará antes de completar el cálculo")
    

def main():
    """
    Función principal del programa
    """
    print("🔬 ANALIZADOR DE TIEMPOS - FIBONACCI")
    print("Comparación: Iterativo vs Recursivo (con opción de riesgo)")
    
    while True:
        print("\n" + "=" * 50)
        print("MENÚ DE OPCIONES:")
        print("1. Comparar un valor específico")
        print("2. Probar un rango de valores (solo recursivo seguro)")
        print("3. Información sobre límites de recursión")
        print("4. Salir")
        
        opcion = input("\nSelecciona una opción (1-4): ")
        
        if opcion == "4":
            print("¡Hasta luego!")
            break
            
        elif opcion == "1":
            try:
                n = int(input("Ingresa el valor de n para Fibonacci: "))
                if n < 0:
                    print("❌ Error: n debe ser un número no negativo")
                    continue
                    
                comparar_metodos(n)
                
            except ValueError:
                print("❌ Error: Ingresa un número válido")
            except KeyboardInterrupt:
                print("\n\n⚠️  Ejecución interrumpida por el usuario")
                
        elif opcion == "2":
            try:
                inicio = int(input("Valor inicial de n: "))
                fin = int(input("Valor final de n: "))
                
                if inicio < 0 or fin < 0 or inicio > fin:
                    print("❌ Error: Rango no válido")
                    continue
                    
                if fin > 35:
                    print("\n⚠️  Nota: Solo se ejecutará recursivo para n ≤ 35")
                    print("   Para valores mayores, se mostrará como 'No ejecutado'")
                    
                probar_rango_valores(inicio, fin)
                
            except ValueError:
                print("❌ Error: Ingresa números válidos")
                
        elif opcion == "3":
            mostrar_advertencias_detalladas()

# Ejemplo de uso rápido
if __name__ == "__main__":
    # Prueba rápida opcional
    print("🔬 PROGRAMA DE COMPARACIÓN FIBONACCI")
    print("Este programa te permite ejecutar el método recursivo")
    print("incluso para valores grandes, bajo tu propia responsabilidad.\n")
    
    main()