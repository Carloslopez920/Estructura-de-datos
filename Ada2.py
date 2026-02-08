import random
import time
import sys

# Opciones disponibles
OPCIONES_ALUMNOS = [500, 1000, 10000, 100000]
OPCIONES_MATERIAS = [3, 6, 10, 15]

# Valores iniciales (se establecerán según selección del usuario)
NUM_ALUMNOS = None
NUM_MATERIAS = None

# Nombres de las materias base
MATERIAS_DISPONIBLES = [
    "Matemáticas", "Física", "Química", "Biología", "Historia",
    "Literatura", "Inglés", "Francés", "Arte", "Música",
    "Educación Física", "Informática", "Filosofía", "Economía", "Geografía",
    "Dibujo Técnico", "Tecnología", "Psicología", "Sociología", "Química Orgánica"
]

def seleccionar_configuracion():
    """Menú para seleccionar la cantidad de alumnos y materias"""
    print("\n" + "╔" + "═"*70 + "╗")
    print("║" + " "*22 + "🎓 CONFIGURACIÓN DEL SISTEMA" + " "*21 + "║")
    print("╚" + "═"*70 + "╝")
    
    # Seleccionar cantidad de alumnos
    print("\n  📊 SELECCIONA LA CANTIDAD DE ALUMNOS:")
    for i, cantidad in enumerate(OPCIONES_ALUMNOS, 1):
        print(f"  [{i}] {cantidad:6,} alumnos")
    
    print("─"*72)
    
    while True:
        try:
            opcion = int(input("  Selecciona una opción (1-4): ").strip())
            if 1 <= opcion <= 4:
                num_alumnos = OPCIONES_ALUMNOS[opcion - 1]
                print(f"\n  ✅ Alumnos seleccionados: {num_alumnos:,}")
                break
            else:
                print("  ❌ Opción no válida. Intenta de nuevo.")
        except ValueError:
            print("  ❌ Ingresa un número válido.")
    
    print("\n  📚 SELECCIONA LA CANTIDAD DE MATERIAS:")
    for i, cantidad in enumerate(OPCIONES_MATERIAS, 1):
        print(f"  [{i}] {cantidad:2} materias")
    
    print("─"*72)
    
    while True:
        try:
            opcion = int(input("  Selecciona una opción (1-4): ").strip())
            if 1 <= opcion <= 4:
                num_materias = OPCIONES_MATERIAS[opcion - 1]
                print(f"\n  ✅ Materias seleccionadas: {num_materias}")
                break
            else:
                print("  ❌ Opción no válida. Intenta de nuevo.")
        except ValueError:
            print("  ❌ Ingresa un número válido.")
    
    total_calif = num_alumnos * num_materias
    print(f"\n  📈 CONFIGURACIÓN FINAL:")
    print(f"     • Alumnos: {num_alumnos:,}")
    print(f"     • Materias: {num_materias}")
    print(f"     • Total de calificaciones: {total_calif:,}")
    print(f"     • Tamaño aproximado en memoria: {(total_calif * 28) / (1024*1024):.2f} MB")
    
    return num_alumnos, num_materias

def generar_nombres_materias(num_materias):
    """Genera nombres de materias según la cantidad seleccionada"""
    if num_materias <= len(MATERIAS_DISPONIBLES):
        return MATERIAS_DISPONIBLES[:num_materias]
    else:
        # Si necesitamos más materias de las disponibles, generamos nombres genéricos
        materias = MATERIAS_DISPONIBLES.copy()
        for i in range(len(MATERIAS_DISPONIBLES), num_materias):
            materias.append(f"Materia {i+1}")
        return materias

def generar_matriz_calificaciones(num_alumnos, num_materias):
    """Genera la matriz de calificaciones según la configuración seleccionada"""
    nombres_materias = generar_nombres_materias(num_materias)
    
    print("\n" + "╔" + "═"*70 + "╗")
    print("║" + " "*12 + "🎓 SISTEMA DE CALIFICACIONES - CARGA MASIVA" + " "*13 + "║")
    print("╚" + "═"*70 + "╝")
    print(f"\n  📊 Configuración:")
    print(f"     • Alumnos (filas):   {num_alumnos:,}")
    print(f"     • Materias (columnas): {num_materias}")
    print(f"     • Total de calificaciones: {num_alumnos * num_materias:,}")
    print("\n  Materias asignadas:")
    for i, materia in enumerate(nombres_materias):
        print(f"     {i+1:2}. {materia}")
    
    print("\n  ⏳ Iniciando carga de datos...")
    print("─"*72)

    # MEDIR TIEMPO DE CREACIÓN DE LA MATRIZ
    tiempo_inicio = time.time()

    # Crear matriz: N alumnos (filas) x M materias (columnas)
    calificaciones = []

    progreso_anterior = -1
    total_alumnos = num_alumnos
    
    for i in range(total_alumnos):
        # Mostrar progreso según la cantidad de alumnos
        porcentaje = int((i / total_alumnos) * 100)
        
        # Mostrar progreso con diferente frecuencia según el tamaño
        if total_alumnos <= 1000:
            if porcentaje != progreso_anterior and porcentaje % 10 == 0:
                print(f"  Generando datos... {porcentaje:3d}% completado ({i}/{total_alumnos} alumnos)")
                progreso_anterior = porcentaje
        elif total_alumnos <= 10000:
            if porcentaje != progreso_anterior and porcentaje % 5 == 0:
                print(f"  Generando datos... {porcentaje:3d}% completado ({i:,}/{total_alumnos:,} alumnos)")
                progreso_anterior = porcentaje
        else:
            if porcentaje != progreso_anterior and porcentaje % 2 == 0:
                print(f"  Generando datos... {porcentaje:3d}% completado ({i:,}/{total_alumnos:,} alumnos)")
                progreso_anterior = porcentaje
        
        # Crear fila con N materias
        fila = [random.randint(1, 10) for _ in range(num_materias)]
        calificaciones.append(fila)

    tiempo_fin = time.time()
    tiempo_total = tiempo_fin - tiempo_inicio

    # Calcular tamaño en memoria (aproximado)
    tamaño_bytes = sys.getsizeof(calificaciones)
    
    # Aproximación más precisa basada en el tamaño real
    if total_alumnos <= 1000:
        for fila in calificaciones:
            tamaño_bytes += sys.getsizeof(fila)
            tamaño_bytes += sum(sys.getsizeof(item) for item in fila)
    else:
        muestra = min(100, total_alumnos)
        for fila in calificaciones[:muestra]:
            tamaño_bytes += sys.getsizeof(fila)
            tamaño_bytes += sum(sys.getsizeof(item) for item in fila)
        tamaño_bytes = tamaño_bytes * (total_alumnos / muestra)
    
    tamaño_mb = tamaño_bytes / (1024 * 1024)

    print("─"*72)
    print("\n" + "╔" + "═"*70 + "╗")
    print("║" + " "*23 + "✅ CARGA COMPLETADA" + " "*28 + "║")
    print("╚" + "═"*70 + "╝")

    print("\n📈 ESTADÍSTICAS DE RENDIMIENTO:")
    print("┌" + "─"*70 + "┐")
    print(f"│ Tiempo de carga total:         {tiempo_total:10.4f} segundos           │")
    print(f"│ Calificaciones generadas:      {num_alumnos * num_materias:10,} elementos         │")
    print(f"│ Velocidad de generación:       {(num_alumnos * num_materias)/tiempo_total:10,.0f} calif./segundo    │")
    print(f"│ Tamaño aproximado en memoria:  {tamaño_mb:10.2f} MB                  │")
    print(f"│ Estructura:                    {num_alumnos:,} filas × {num_materias} columnas    │")
    print("└" + "─"*70 + "┘")
    
    return calificaciones, nombres_materias

def visualizar_tabla_completa(calificaciones, nombres_materias):
    """Visualiza TODOS los alumnos"""
    num_alumnos = len(calificaciones)
    num_materias = len(nombres_materias)
    
    print("\n" + "="*(12 + 16*num_materias))
    print(f"TABLA COMPLETA DE CALIFICACIONES - {num_alumnos:,} ALUMNOS × {num_materias} MATERIAS")
    print("="*(12 + 16*num_materias))
    print("\n⏳ Generando visualización completa...")
    
    tiempo_inicio_viz = time.time()
    
    # Encabezado
    print("\n┌" + "─"*12 + "┬", end="")
    for i in range(num_materias):
        print("─"*15 + ("┬" if i < num_materias-1 else "┐"), end="")
    print()
    
    # Nombres de materias (truncados si son muy largos)
    print("│ ALUMNO #   │", end="")
    for materia in range(num_materias):
        nombre = nombres_materias[materia]
        if len(nombre) > 13:
            nombre = nombre[:11] + ".."
        print(f" {nombre:13} │", end="")
    print()
    
    # Línea separadora principal
    print("├" + "─"*12 + "┼", end="")
    for i in range(num_materias):
        print("─"*15 + ("┼" if i < num_materias-1 else "┤"), end="")
    print()
    
    # MOSTRAR TODOS LOS ALUMNOS
    for alumno in range(num_alumnos):
        # Mostrar progreso para matrices grandes
        if num_alumnos >= 5000:
            if alumno % 5000 == 0 and alumno > 0:
                porcentaje = (alumno / num_alumnos) * 100
                espacios = " " * (num_materias * 16 - 35)
                print(f"│ {'':10} │ Progreso: {porcentaje:5.1f}% ({alumno:,}/{num_alumnos:,}){espacios}│")
        
        # Datos del alumno
        print(f"│ {alumno:10} │", end="")
        for materia in range(num_materias):
            print(f" {calificaciones[alumno][materia]:2}/10          │", end="")
        print()
        
        # Línea separadora según el tamaño
        if alumno < num_alumnos - 1:
            if num_alumnos <= 100:
                print("├" + "─"*12 + "┼", end="")
                for i in range(num_materias):
                    print("─"*15 + ("┼" if i < num_materias-1 else "┤"), end="")
                print()
            elif num_alumnos <= 1000 and alumno % 100 == 99:
                print("├" + "─"*12 + "┼", end="")
                for i in range(num_materias):
                    print("─"*15 + ("┼" if i < num_materias-1 else "┤"), end="")
                print()
            elif alumno % 1000 == 999:
                print("├" + "─"*12 + "┼", end="")
                for i in range(num_materias):
                    print("─"*15 + ("┼" if i < num_materias-1 else "┤"), end="")
                print()
    
    # Línea final
    print("└" + "─"*12 + "┴", end="")
    for i in range(num_materias):
        print("─"*15 + ("┴" if i < num_materias-1 else "┘"), end="")
    print()
    
    tiempo_fin_viz = time.time()
    tiempo_viz = tiempo_fin_viz - tiempo_inicio_viz
    
    print("\n" + "="*(12 + 16*num_materias))
    print(f"✅ Visualización completa generada en {tiempo_viz:.2f} segundos")
    print(f"📊 Se mostraron {num_alumnos:,} alumnos × {num_materias} materias")
    print("="*(12 + 16*num_materias))

def visualizar_tabla_paginada(calificaciones, nombres_materias, alumnos_por_pagina=100):
    """Visualiza la tabla en páginas de N alumnos"""
    num_alumnos = len(calificaciones)
    num_materias = len(nombres_materias)
    total_paginas = (num_alumnos + alumnos_por_pagina - 1) // alumnos_por_pagina
    
    print(f"\n📄 VISUALIZACIÓN PAGINADA: {alumnos_por_pagina} alumnos por página")
    print(f"📊 Total de páginas: {total_paginas:,}")
    
    for pagina in range(total_paginas):
        inicio = pagina * alumnos_por_pagina
        fin = min((pagina + 1) * alumnos_por_pagina, num_alumnos)
        
        ancho_tabla = 12 + 16 * num_materias
        print("\n" + "="*ancho_tabla)
        print(f"PÁGINA {pagina + 1:,}/{total_paginas:,} - Alumnos {inicio:,} al {fin-1:,}")
        print("="*ancho_tabla)
        
        # Encabezado
        print("\n┌" + "─"*12 + "┬", end="")
        for i in range(num_materias):
            print("─"*15 + ("┬" if i < num_materias-1 else "┐"), end="")
        print()
        
        # Nombres de materias (truncados si son muy largos)
        print("│ ALUMNO #   │", end="")
        for materia in range(num_materias):
            nombre = nombres_materias[materia]
            if len(nombre) > 13:
                nombre = nombre[:11] + ".."
            print(f" {nombre:13} │", end="")
        print()
        
        # Línea separadora
        print("├" + "─"*12 + "┼", end="")
        for i in range(num_materias):
            print("─"*15 + ("┼" if i < num_materias-1 else "┤"), end="")
        print()
        
        # Datos de la página
        for alumno in range(inicio, fin):
            print(f"│ {alumno:10} │", end="")
            for materia in range(num_materias):
                print(f" {calificaciones[alumno][materia]:2}/10          │", end="")
            print()
            
            if alumno < fin - 1:
                print("├" + "─"*12 + "┼", end="")
                for i in range(num_materias):
                    print("─"*15 + ("┼" if i < num_materias-1 else "┤"), end="")
                print()
        
        # Línea final
        print("└" + "─"*12 + "┴", end="")
        for i in range(num_materias):
            print("─"*15 + ("┴" if i < num_materias-1 else "┘"), end="")
        print()
        
        # Pausa entre páginas (excepto en la última)
        if pagina < total_paginas - 1:
            respuesta = input(f"\n➡️  Presiona ENTER para siguiente página, 'q' para salir: ")
            if respuesta.lower() == 'q':
                print(f"\n⏸️  Visualización detenida en página {pagina + 1}/{total_paginas:,}")
                break

def visualizar_rango_alumnos(calificaciones, nombres_materias, inicio, fin):
    """Visualiza un rango específico de alumnos"""
    num_alumnos = len(calificaciones)
    num_materias = len(nombres_materias)
    
    if inicio < 0 or fin > num_alumnos or inicio >= fin:
        print(f"❌ ERROR: Rango inválido. Debe ser 0 <= inicio < fin <= {num_alumnos:,}")
        return
    
    ancho_tabla = 12 + 16 * num_materias
    print("\n" + "="*ancho_tabla)
    print(f"RANGO DE ALUMNOS: {inicio:,} al {fin-1:,} ({fin-inicio:,} alumnos)")
    print("="*ancho_tabla)
    
    # Encabezado
    print("\n┌" + "─"*12 + "┬", end="")
    for i in range(num_materias):
        print("─"*15 + ("┬" if i < num_materias-1 else "┐"), end="")
    print()
    
    # Nombres de materias (truncados si son muy largos)
    print("│ ALUMNO #   │", end="")
    for materia in range(num_materias):
        nombre = nombres_materias[materia]
        if len(nombre) > 13:
            nombre = nombre[:11] + ".."
        print(f" {nombre:13} │", end="")
    print()
    
    # Línea separadora
    print("├" + "─"*12 + "┼", end="")
    for i in range(num_materias):
        print("─"*15 + ("┼" if i < num_materias-1 else "┤"), end="")
    print()
    
    # Datos
    for alumno in range(inicio, fin):
        print(f"│ {alumno:10} │", end="")
        for materia in range(num_materias):
            print(f" {calificaciones[alumno][materia]:2}/10          │", end="")
        print()
        
        if alumno < fin - 1:
            print("├" + "─"*12 + "┼", end="")
            for i in range(num_materias):
                print("─"*15 + ("┼" if i < num_materias-1 else "┤"), end="")
            print()
    
    # Línea final
    print("└" + "─"*12 + "┴", end="")
    for i in range(num_materias):
        print("─"*15 + ("┴" if i < num_materias-1 else "┘"), end="")
    print()
    print("="*ancho_tabla)

def mostrar_estadisticas(calificaciones, nombres_materias):
    """Muestra estadísticas de las calificaciones"""
    num_alumnos = len(calificaciones)
    num_materias = len(nombres_materias)
    
    print("\n" + "╔" + "═"*70 + "╗")
    print("║" + " "*23 + "📊 ESTADÍSTICAS" + " "*32 + "║")
    print("╚" + "═"*70 + "╝")
    
    print(f"\n  📈 RESUMEN GENERAL:")
    print(f"     • Total de alumnos: {num_alumnos:,}")
    print(f"     • Total de materias: {num_materias}")
    print(f"     • Total de calificaciones: {num_alumnos * num_materias:,}")
    
    print("\n  📊 POR MATERIA:")
    print("  ┌──────────┬──────────┬──────────┬──────────┬──────────┐")
    print("  │ Materia  │  Promedio│   Máxima │   Mínima │ Aprobados│")
    print("  ├──────────┼──────────┼──────────┼──────────┼──────────┤")
    
    for materia_idx in range(num_materias):
        califs_materia = [calificaciones[alumno][materia_idx] for alumno in range(num_alumnos)]
        promedio = sum(califs_materia) / num_alumnos
        maxima = max(califs_materia)
        minima = min(califs_materia)
        aprobados = sum(1 for calif in califs_materia if calif >= 6)
        porcentaje_aprobados = (aprobados / num_alumnos) * 100
        
        nombre_materia = nombres_materias[materia_idx]
        if len(nombre_materia) > 10:
            nombre_materia = nombre_materia[:8] + ".."
        
        print(f"  │ {nombre_materia:8} │ {promedio:8.2f} │ {maxima:8} │ {minima:8} │ {porcentaje_aprobados:7.1f}% │")
    
    print("  └──────────┴──────────┴──────────┴──────────┴──────────┘")
    
    # Estadísticas generales
    todas_calificaciones = [calif for alumno in calificaciones for calif in alumno]
    promedio_general = sum(todas_calificaciones) / len(todas_calificaciones)
    aprobados_general = sum(1 for calif in todas_calificaciones if calif >= 6)
    porcentaje_aprobados_general = (aprobados_general / len(todas_calificaciones)) * 100
    
    print(f"\n  📈 ESTADÍSTICAS GENERALES:")
    print(f"     • Promedio general: {promedio_general:.2f}")
    print(f"     • Porcentaje de aprobados: {porcentaje_aprobados_general:.1f}%")
    print(f"     • Calificación más alta: {max(todas_calificaciones)}")
    print(f"     • Calificación más baja: {min(todas_calificaciones)}")

def menu_principal(calificaciones, nombres_materias):
    """Menú interactivo del sistema"""
    num_alumnos = len(calificaciones)
    num_materias = len(nombres_materias)
    
    while True:
        print("\n" + "╔" + "═"*70 + "╗")
        titulo = f"🎓 SISTEMA DE GESTIÓN - {num_alumnos:,} × {num_materias}"
        espacios = " " * (70 - len(titulo) - 2)
        print(f"║{titulo}{espacios}║")
        print("╚" + "═"*70 + "╝")
        print(f"\n  📊 Sistema: {num_alumnos:,} alumnos × {num_materias} materias")
        print(f"  💾 Total: {num_alumnos * num_materias:,} calificaciones en memoria")
        print("\n  OPCIONES PRINCIPALES:")
        print("  [1] 📋 Ver tabla de calificaciones")
        print("  [2] 📊 Ver estadísticas")
        print("  [3] ⚙️  Cambiar configuración (reinicia sistema)")
        print("  [4] 🚪 Salir")
        print("─"*72)
        
        opcion = input("  Selecciona una opción: ").strip()
        
        if opcion == "1":
            print("\n  📋 OPCIONES DE VISUALIZACIÓN:")
            print("  [A] Ver TODA la tabla completa" + (" ⚠️" if num_alumnos > 1000 else ""))
            print("  [B] Ver tabla paginada (100 alumnos por página)")
            if num_alumnos > 100:
                print("  [C] Ver tabla paginada (1,000 alumnos por página)")
            print("  [D] Ver rango específico de alumnos")
            print("  [E] Ver primeros 100 alumnos")
            if num_alumnos > 100:
                print("  [F] Ver últimos 100 alumnos")
            if num_alumnos >= 200:
                print("  [G] Ver alumnos del medio")
            print("  [H] Volver al menú principal")
            print("─"*72)
            
            sub_opcion = input("  Selecciona una opción: ").strip().upper()
            
            if sub_opcion == "A":
                if num_alumnos > 1000:
                    confirmacion = input(f"\n⚠️  Esto mostrará {num_alumnos:,} líneas. ¿Continuar? (s/n): ")
                    if confirmacion.lower() != 's':
                        print("❌ Visualización cancelada")
                        input("\nPresiona ENTER para continuar...")
                        continue
                visualizar_tabla_completa(calificaciones, nombres_materias)
                input("\nPresiona ENTER para continuar...")
                
            elif sub_opcion == "B":
                visualizar_tabla_paginada(calificaciones, nombres_materias, 100)
                
            elif sub_opcion == "C" and num_alumnos > 100:
                visualizar_tabla_paginada(calificaciones, nombres_materias, 1000)
                
            elif sub_opcion == "D":
                try:
                    inicio = int(input(f"  Desde qué alumno? (0-{num_alumnos-1:,}): "))
                    fin = int(input(f"  Hasta qué alumno? ({inicio+1}-{num_alumnos:,}): "))
                    visualizar_rango_alumnos(calificaciones, nombres_materias, inicio, fin)
                except ValueError:
                    print("❌ Error: Ingresa números válidos")
                input("\nPresiona ENTER para continuar...")
                
            elif sub_opcion == "E":
                visualizar_rango_alumnos(calificaciones, nombres_materias, 0, min(100, num_alumnos))
                input("\nPresiona ENTER para continuar...")
                
            elif sub_opcion == "F" and num_alumnos > 100:
                visualizar_rango_alumnos(calificaciones, nombres_materias, max(0, num_alumnos - 100), num_alumnos)
                input("\nPresiona ENTER para continuar...")
                
            elif sub_opcion == "G" and num_alumnos >= 200:
                mitad = num_alumnos // 2
                visualizar_rango_alumnos(calificaciones, nombres_materias, max(0, mitad - 100), min(num_alumnos, mitad + 100))
                input("\nPresiona ENTER para continuar...")
                
            elif sub_opcion == "H":
                continue
            else:
                print("❌ Opción no válida.")
                input("\nPresiona ENTER para continuar...")
            
        elif opcion == "2":
            mostrar_estadisticas(calificaciones, nombres_materias)
            input("\nPresiona ENTER para continuar...")
            
        elif opcion == "3":
            confirmacion = input("\n⚠️  Esto reiniciará el sistema y perderás los datos actuales. ¿Continuar? (s/n): ")
            if confirmacion.lower() == 's':
                return True  # Indicar que se debe reiniciar
            else:
                print("❌ Reinicio cancelado")
                input("\nPresiona ENTER para continuar...")
            
        elif opcion == "4":
            print("\n" + "╔" + "═"*70 + "╗")
            print("║" + " "*26 + "👋 ¡Hasta luego!" + " "*29 + "║")
            print("╚" + "═"*70 + "╝\n")
            return False  # Salir del programa
            
        else:
            print("❌ Opción no válida.")

# PROGRAMA PRINCIPAL
if __name__ == "__main__":
    print("\n" + "╔" + "═"*70 + "╗")
    print("║" + " "*20 + "🎓 SISTEMA DE GESTIÓN ACADÉMICA" + " "*19 + "║")
    print("║" + " "*15 + "SISTEMA MASIVO DE CALIFICACIONES" + " "*18 + "║")
    print("╚" + "═"*70 + "╝")
    
    reiniciar = True
    
    while reiniciar:
        # Seleccionar configuración
        NUM_ALUMNOS, NUM_MATERIAS = seleccionar_configuracion()
        
        # Generar matriz de calificaciones
        calificaciones, nombres_materias = generar_matriz_calificaciones(NUM_ALUMNOS, NUM_MATERIAS)
        
        # Mostrar primeros alumnos como ejemplo
        num_ejemplo = min(10, NUM_ALUMNOS)
        print("\n" + "─"*72)
        print(f"📝 VISTA PREVIA: Primeros {num_ejemplo} alumnos")
        print("─"*72)
        visualizar_rango_alumnos(calificaciones, nombres_materias, 0, num_ejemplo)
        
        input("\nPresiona ENTER para ir al menú principal...")
        
        # Ejecutar menú principal
        reiniciar = menu_principal(calificaciones, nombres_materias)