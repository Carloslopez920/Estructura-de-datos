import tkinter as tk
from tkinter import ttk
import time
import threading
import random
import math

class OrdenamientoExternoSimultaneo:
    def __init__(self, root, datos_usuario):
        self.root = root
        self.root.title("Ordenamiento Externo - Mezcla Directa, Mezcla Equilibrada e Intercalacion (Ejecución Simultánea)")
        self.root.geometry("1300x750")
        self.root.configure(bg="#2c3e50")
        
        # Datos proporcionados por el usuario
        self.datos_ejemplo = datos_usuario
        
        self.crear_widgets()
        self.mostrar_datos_iniciales()
    
    def crear_widgets(self):
        # Título principal
        titulo = tk.Label(self.root, text="COMPARACIÓN DE MÉTODOS DE ORDENAMIENTO EXTERNO", 
                         font=("Arial", 16, "bold"), bg="#2c3e50", fg="white", pady=15)
        titulo.pack(fill=tk.X)
        
        # Subtítulo con los datos ingresados (truncado si es muy largo)
        datos_str = str(self.datos_ejemplo)
        if len(datos_str) > 80:
            datos_str = datos_str[:77] + "..."
        subtitulo = tk.Label(self.root, text=f"Datos ingresados: {datos_str}", 
                            font=("Arial", 9), bg="#2c3e50", fg="#bdc3c7", pady=5)
        subtitulo.pack(fill=tk.X)
        
        # Mostrar cantidad de elementos
        lbl_cantidad = tk.Label(self.root, text=f"Total de elementos: {len(self.datos_ejemplo)}", 
                               font=("Arial", 10, "bold"), bg="#2c3e50", fg="#f39c12")
        lbl_cantidad.pack(fill=tk.X)
        
        # Frame para los tres algoritmos
        self.frame_principal = tk.Frame(self.root, bg="#2c3e50")
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Configurar tres columnas iguales
        self.frame_principal.columnconfigure(0, weight=1)
        self.frame_principal.columnconfigure(1, weight=1)
        self.frame_principal.columnconfigure(2, weight=1)
        
        # Algoritmo 1: Mezcla Directa
        self.frame_mezcla_directa = self.crear_panel_algoritmo(0, "MEZCLA DIRECTA", "#9b59b6")
        
        # Algoritmo 2: Mezcla Equilibrada
        self.frame_mezcla_equilibrada = self.crear_panel_algoritmo(1, "MEZCLA EQUILIBRADA", "#e74c3c")
        
        # Algoritmo 3: Intercalación
        self.frame_intercalacion = self.crear_panel_algoritmo(2, "INTERCALACIÓN", "#16a085")
        
        # Frame de control (solo un botón)
        frame_control = tk.Frame(self.root, bg="#2c3e50", pady=15)
        frame_control.pack(fill=tk.X)
        
        self.btn_iniciar = tk.Button(frame_control, text="▶ INICIAR ORDENAMIENTO SIMULTÁNEO", 
                                     command=self.iniciar_ordenamiento_simultaneo,
                                     bg="#f39c12", fg="white", font=("Arial", 12, "bold"),
                                     width=35, height=2, cursor="hand2")
        self.btn_iniciar.pack()
        
        # Barra de progreso general
        self.progress = ttk.Progressbar(frame_control, mode='indeterminate')
        self.progress.pack(fill=tk.X, padx=200, pady=5)
        
        # Estado de ejecución
        self.ejecutando = False
        
        # Almacenar resultados
        self.resultados = {}
    
    def crear_panel_algoritmo(self, columna, titulo, color):
        frame = tk.LabelFrame(self.frame_principal, text=titulo, font=("Arial", 11, "bold"),
                             bg="#ecf0f1", fg=color, bd=2, relief=tk.RAISED)
        frame.grid(row=0, column=columna, padx=10, pady=10, sticky="nsew")
        
        # Canvas para dibujar barras
        canvas = tk.Canvas(frame, bg="white", height=300, highlightthickness=1)
        canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame para scroll horizontal si hay muchos datos
        self.configurar_scroll_canvas(canvas)
        
        # Label para mostrar datos (truncado si es muy largo)
        label_datos = tk.Label(frame, text="", bg="#ecf0f1", font=("Courier", 8), wraplength=380)
        label_datos.pack(fill=tk.X, padx=5, pady=5)
        
        # Label para estadísticas
        label_stats = tk.Label(frame, text="Comparaciones: 0 | Tiempo: 0 ms", 
                              bg="#ecf0f1", font=("Arial", 9), fg="#2c3e50")
        label_stats.pack(fill=tk.X, padx=5, pady=2)
        
        # Label para estado
        label_estado = tk.Label(frame, text="⚡ En espera", bg="#ecf0f1", font=("Arial", 9, "italic"), fg="#7f8c8d")
        label_estado.pack(fill=tk.X, padx=5, pady=2)
        
        # Guardar referencias
        frame.canvas = canvas
        frame.label_datos = label_datos
        frame.label_stats = label_stats
        frame.label_estado = label_estado
        frame.color = color
        
        return frame
    
    def configurar_scroll_canvas(self, canvas):
        """Configurar canvas para soportar scroll horizontal si es necesario"""
        # Crear frame interno dentro del canvas
        inner_frame = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        inner_frame.bind("<Configure>", on_configure)
        canvas.inner_frame = inner_frame
        canvas.original_width = canvas.winfo_width
    
    def mostrar_datos_iniciales(self):
        for frame in [self.frame_mezcla_directa, self.frame_mezcla_equilibrada, self.frame_intercalacion]:
            datos_str = str(self.datos_ejemplo)
            if len(datos_str) > 60:
                datos_str = datos_str[:57] + "..."
            frame.label_datos.config(text=f"Datos: {datos_str}")
            self.dibujar_barras(frame.canvas, self.datos_ejemplo, frame.color)
    
    def dibujar_barras(self, canvas, datos, color_base):
        canvas.delete("all")
        if not datos:
            return
        
        width = canvas.winfo_width() if canvas.winfo_width() > 50 else 380
        height = canvas.winfo_height() if canvas.winfo_height() > 50 else 300
        
        n = len(datos)
        if n == 0:
            return
        
        # Calcular ancho de cada barra basado en la cantidad de datos
        # Para muchos datos, las barras serán más delgadas
        bar_width = max(2, (width - 20) / n - 2)
        
        max_valor = max(datos) if datos else 1
        min_valor = min(datos) if datos else 0
        rango = max_valor - min_valor if max_valor != min_valor else 1
        
        # Calcular offset para centrar
        total_width = n * (bar_width + 2)
        offset = max(5, (width - total_width) / 2)
        
        for i, valor in enumerate(datos):
            x0 = offset + i * (bar_width + 2)
            bar_height = ((valor - min_valor) / rango) * (height - 60)
            y0 = height - bar_height - 40
            y1 = height - 40
            
            # Color según valor
            intensidad = (valor - min_valor) / rango
            r = int(255 * (1 - intensidad))
            g = int(255 * intensidad)
            b = 100
            color = f"#{r:02x}{g:02x}{b:02x}"
            
            canvas.create_rectangle(x0, y0, x0 + bar_width, y1, fill=color, outline="#34495e", width=1)
            
            # Mostrar solo los valores si hay espacio suficiente
            if bar_width >= 12 and n <= 30:
                canvas.create_text(x0 + bar_width/2, y1 - 5, text=str(valor), anchor="n", font=("Arial", 7))
            elif bar_width >= 8 and n <= 60:
                canvas.create_text(x0 + bar_width/2, y1 - 5, text=str(valor), anchor="n", font=("Arial", 6))
        
        canvas.update()
    
    def actualizar_visualizacion(self, frame, datos, mensaje, comparaciones, tiempo_ms):
        # Truncar visualización de datos si es muy larga
        datos_str = str(datos)
        if len(datos_str) > 60:
            datos_str = datos_str[:57] + "..."
        frame.label_datos.config(text=f"Datos: {datos_str}")
        frame.label_stats.config(text=f"Comparaciones: {comparaciones} | Tiempo: {tiempo_ms:.0f} ms")
        frame.label_estado.config(text=mensaje)
        self.dibujar_barras(frame.canvas, datos, frame.color)
    
    # ALGORITMO 1: MEZCLA DIRECTA
    def mezcla_directa(self, frame, datos_originales, resultados):
        inicio = time.time()
        datos = datos_originales.copy()
        paso = 1
        fase = 1
        comparaciones = 0
        
        self.actualizar_visualizacion(frame, datos, f"Fase {fase}: Inicio", comparaciones, 0)
        time.sleep(0.2)
        
        while paso < len(datos):
            fase += 1
            for i in range(0, len(datos), paso * 2):
                izquierda = datos[i:i + paso]
                derecha = datos[i + paso:i + paso * 2]
                mezclados = []
                a, b = 0, 0
                while a < len(izquierda) and b < len(derecha):
                    comparaciones += 1
                    if izquierda[a] < derecha[b]:
                        mezclados.append(izquierda[a])
                        a += 1
                    else:
                        mezclados.append(derecha[b])
                        b += 1
                mezclados.extend(izquierda[a:])
                mezclados.extend(derecha[b:])
                datos[i:i + paso * 2] = mezclados
            
            self.actualizar_visualizacion(frame, datos, f"Fase {fase}: bloque tamaño {paso * 2}", comparaciones, (time.time() - inicio) * 1000)
            time.sleep(0.2)
            paso *= 2
        
        tiempo_ms = (time.time() - inicio) * 1000
        self.actualizar_visualizacion(frame, datos, "✅ COMPLETADO", comparaciones, tiempo_ms)
        resultados["mezcla_directa"] = {"datos": datos, "comparaciones": comparaciones, "tiempo": tiempo_ms}
        return datos
    
    # ALGORITMO 2: MEZCLA EQUILIBRADA
    def mezcla_equilibrada_recursiva(self, frame, datos, profundidad=0, comparaciones=[0]):
        if len(datos) <= 1:
            return datos
        
        medio = len(datos) // 2
        izquierda = self.mezcla_equilibrada_recursiva(frame, datos[:medio], profundidad + 1, comparaciones)
        derecha = self.mezcla_equilibrada_recursiva(frame, datos[medio:], profundidad + 1, comparaciones)
        
        resultado = []
        i = j = 0
        while i < len(izquierda) and j < len(derecha):
            comparaciones[0] += 1
            if izquierda[i] < derecha[j]:
                resultado.append(izquierda[i])
                i += 1
            else:
                resultado.append(derecha[j])
                j += 1
        resultado.extend(izquierda[i:])
        resultado.extend(derecha[j:])
        
        return resultado
    
    def mezcla_equilibrada(self, frame, datos_originales, resultados):
        inicio = time.time()
        frame.label_estado.config(text="Dividiendo lista...")
        time.sleep(0.2)
        
        comparaciones = [0]
        frame.label_estado.config(text="Mezclando niveles...")
        time.sleep(0.2)
        
        datos_ordenados = self.mezcla_equilibrada_recursiva(frame, datos_originales, 0, comparaciones)
        self.actualizar_visualizacion(frame, datos_ordenados, "Mezclando...", comparaciones[0], (time.time() - inicio) * 1000)
        time.sleep(0.2)
        
        tiempo_ms = (time.time() - inicio) * 1000
        self.actualizar_visualizacion(frame, datos_ordenados, "✅ COMPLETADO", comparaciones[0], tiempo_ms)
        resultados["mezcla_equilibrada"] = {"datos": datos_ordenados, "comparaciones": comparaciones[0], "tiempo": tiempo_ms}
        return datos_ordenados
    
    # ALGORITMO 3: INTERCALACIÓN
    def intercalacion(self, frame, datos_originales, resultados):
        inicio = time.time()
        datos = datos_originales.copy()
        k = 2
        fase = 1
        comparaciones = 0
        
        self.actualizar_visualizacion(frame, datos, f"Fase {fase}: bloque tamaño 1", comparaciones, 0)
        time.sleep(0.2)
        
        while k <= len(datos):
            fase += 1
            for i in range(0, len(datos), k):
                sublista = datos[i:i + k]
                # Contar comparaciones del sort interno
                for j in range(1, len(sublista)):
                    for m in range(j):
                        comparaciones += 1
                sublista.sort()
                datos[i:i + k] = sublista
            
            self.actualizar_visualizacion(frame, datos, f"Fase {fase}: bloque tamaño {k}", comparaciones, (time.time() - inicio) * 1000)
            time.sleep(0.2)
            
            if k >= len(datos):
                break
            k *= 2
        
        if k > len(datos) and len(datos) > 2:
            datos.sort()
            self.actualizar_visualizacion(frame, datos, "Fase final: ordenando resto", comparaciones, (time.time() - inicio) * 1000)
            time.sleep(0.2)
        
        tiempo_ms = (time.time() - inicio) * 1000
        self.actualizar_visualizacion(frame, datos, "✅ COMPLETADO", comparaciones, tiempo_ms)
        resultados["intercalacion"] = {"datos": datos, "comparaciones": comparaciones, "tiempo": tiempo_ms}
        return datos
    
    def iniciar_ordenamiento_simultaneo(self):
        if self.ejecutando:
            return
        
        self.ejecutando = True
        self.btn_iniciar.config(state=tk.DISABLED, text="⏳ ORDENANDO...")
        self.progress.start()
        
        self.resultados = {}
        
        for frame in [self.frame_mezcla_directa, self.frame_mezcla_equilibrada, self.frame_intercalacion]:
            frame.label_estado.config(text="🔄 En ejecución...")
            frame.label_stats.config(text="Comparaciones: 0 | Tiempo: 0 ms")
        
        hilo1 = threading.Thread(target=self.mezcla_directa, args=(self.frame_mezcla_directa, self.datos_ejemplo, self.resultados))
        hilo2 = threading.Thread(target=self.mezcla_equilibrada, args=(self.frame_mezcla_equilibrada, self.datos_ejemplo, self.resultados))
        hilo3 = threading.Thread(target=self.intercalacion, args=(self.frame_intercalacion, self.datos_ejemplo, self.resultados))
        
        hilo1.start()
        hilo2.start()
        hilo3.start()
        
        self.monitor_hilos(hilo1, hilo2, hilo3)
    
    def monitor_hilos(self, hilo1, hilo2, hilo3):
        if not (hilo1.is_alive() or hilo2.is_alive() or hilo3.is_alive()):
            self.ejecutando = False
            self.progress.stop()
            self.btn_iniciar.config(state=tk.NORMAL, text="▶ INICIAR ORDENAMIENTO SIMULTÁNEO")
            self.mostrar_resumen()
        else:
            self.root.after(500, lambda: self.monitor_hilos(hilo1, hilo2, hilo3))
    
    def mostrar_resumen(self):
        resumen_win = tk.Toplevel(self.root)
        resumen_win.title("Resumen de Ordenamiento Externo")
        resumen_win.geometry("750x600")
        resumen_win.configure(bg="#ecf0f1")
        
        tk.Label(resumen_win, text="RESUMEN COMPARATIVO DE ALGORITMOS", 
                font=("Arial", 14, "bold"), bg="#2c3e50", fg="white", pady=10).pack(fill=tk.X)
        
        # Frame con scroll para el texto
        text_frame = tk.Frame(resumen_win, bg="#ecf0f1")
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        texto_resumen = tk.Text(text_frame, font=("Courier", 10), wrap=tk.WORD, 
                                yscrollcommand=scrollbar.set, padx=15, pady=15)
        texto_resumen.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=texto_resumen.yview)
        
        texto_resumen.insert(tk.END, "="*70 + "\n")
        texto_resumen.insert(tk.END, "DATOS ORIGINALES\n")
        texto_resumen.insert(tk.END, "="*70 + "\n")
        texto_resumen.insert(tk.END, f"Cantidad de elementos: {len(self.datos_ejemplo)}\n")
        
        # Mostrar primeros 30 y últimos 5 si son muchos
        if len(self.datos_ejemplo) > 35:
            primeros = self.datos_ejemplo[:30]
            ultimos = self.datos_ejemplo[-5:]
            texto_resumen.insert(tk.END, f"Lista: {primeros} ... {ultimos}\n")
            texto_resumen.insert(tk.END, f"(Mostrando 30 primeros y 5 últimos de {len(self.datos_ejemplo)} totales)\n\n")
        else:
            texto_resumen.insert(tk.END, f"Lista: {self.datos_ejemplo}\n\n")
        
        algoritmos = [
            ("MEZCLA DIRECTA", self.resultados.get("mezcla_directa", {}), "#9b59b6"),
            ("MEZCLA EQUILIBRADA", self.resultados.get("mezcla_equilibrada", {}), "#e74c3c"),
            ("INTERCALACIÓN", self.resultados.get("intercalacion", {}), "#16a085")
        ]
        
        for nombre, res, color in algoritmos:
            if res:
                texto_resumen.insert(tk.END, "="*70 + "\n")
                texto_resumen.insert(tk.END, f"{nombre}\n")
                texto_resumen.insert(tk.END, "="*70 + "\n")
                
                # Mostrar resultado truncado si es largo
                datos_ordenados = res['datos']
                if len(datos_ordenados) > 35:
                    primeros = datos_ordenados[:30]
                    ultimos = datos_ordenados[-5:]
                    texto_resumen.insert(tk.END, f"Resultado ordenado: {primeros} ... {ultimos}\n")
                    texto_resumen.insert(tk.END, f"Verificación: {'✓ Ordenado' if datos_ordenados == sorted(datos_ordenados) else '✗ Error'}\n")
                else:
                    texto_resumen.insert(tk.END, f"Resultado ordenado: {datos_ordenados}\n")
                
                texto_resumen.insert(tk.END, f"Comparaciones realizadas: {res['comparaciones']:,}\n")
                texto_resumen.insert(tk.END, f"Tiempo de ejecución: {res['tiempo']:.2f} ms\n\n")
        
        texto_resumen.insert(tk.END, "="*70 + "\n")
        texto_resumen.insert(tk.END, "CUADRO COMPARATIVO\n")
        texto_resumen.insert(tk.END, "="*70 + "\n")
        texto_resumen.insert(tk.END, "┌────────────────────┬──────────────┬──────────────┬────────────────┐\n")
        texto_resumen.insert(tk.END, "│ Algoritmo          │ Comparaciones │ Tiempo (ms)  │ Eficiencia     │\n")
        texto_resumen.insert(tk.END, "├────────────────────┼──────────────┼──────────────┼────────────────┤\n")
        
        for nombre, res, _ in algoritmos:
            if res:
                eficiencia = "Baja" if res['comparaciones'] > len(self.datos_ejemplo) * math.log2(len(self.datos_ejemplo)) * 1.5 else "Normal"
                texto_resumen.insert(tk.END, f"│ {nombre:<18} │ {res['comparaciones']:>12,} │ {res['tiempo']:>12.2f} │ {eficiencia:<14} │\n")
        
        texto_resumen.insert(tk.END, "└────────────────────┴──────────────┴──────────────┴────────────────┘\n\n")
        
        texto_resumen.insert(tk.END, "="*70 + "\n")
        texto_resumen.insert(tk.END, "ANÁLISIS DE RESULTADOS\n")
        texto_resumen.insert(tk.END, "="*70 + "\n")
        
        mejor_tiempo = min((res.get('tiempo', float('inf')) for _, res, _ in algoritmos if res), default=0)
        mejor_comparaciones = min((res.get('comparaciones', float('inf')) for _, res, _ in algoritmos if res), default=0)
        
        ganador_tiempo = next((nombre for nombre, res, _ in algoritmos if res and res.get('tiempo') == mejor_tiempo), "N/A")
        ganador_comparaciones = next((nombre for nombre, res, _ in algoritmos if res and res.get('comparaciones') == mejor_comparaciones), "N/A")
        
        texto_resumen.insert(tk.END, f"✓ Algoritmo más rápido: {ganador_tiempo} ({mejor_tiempo:.2f} ms)\n")
        texto_resumen.insert(tk.END, f"✓ Algoritmo con menos comparaciones: {ganador_comparaciones} ({mejor_comparaciones:,} comparaciones)\n\n")
        
        mezcla_d = self.resultados.get("mezcla_directa", {})
        mezcla_e = self.resultados.get("mezcla_equilibrada", {})
        inter = self.resultados.get("intercalacion", {})
        
        if mezcla_d and mezcla_e and inter:
            texto_resumen.insert(tk.END, "Análisis detallado:\n")
            texto_resumen.insert(tk.END, f"- Mezcla Directa vs Mezcla Equilibrada: Diferencia de tiempo = {abs(mezcla_d['tiempo'] - mezcla_e['tiempo']):.2f} ms\n")
            texto_resumen.insert(tk.END, f"- Mezcla Directa vs Intercalación: Diferencia de comparaciones = {abs(mezcla_d['comparaciones'] - inter['comparaciones']):,}\n")
            texto_resumen.insert(tk.END, f"- La Intercalación resultó {'más' if inter['tiempo'] > mezcla_d['tiempo'] else 'menos'} lenta que Mezcla Directa\n")
            texto_resumen.insert(tk.END, f"- Complejidad teórica O(n log n) con n={len(self.datos_ejemplo)}: ~{len(self.datos_ejemplo) * math.log2(len(self.datos_ejemplo)):.0f} comparaciones esperadas\n")
        
        texto_resumen.config(state=tk.DISABLED)
        
        btn_frame = tk.Frame(resumen_win, bg="#ecf0f1", pady=10)
        btn_frame.pack()
        
        tk.Button(btn_frame, text="CERRAR", command=resumen_win.destroy, 
                 bg="#2c3e50", fg="white", font=("Arial", 10, "bold"), width=15).pack()

# ================ PARTE DE ENTRADA POR TERMINAL (SIN LÍMITE DE 30) ================

def obtener_datos_de_terminal():
    print("\n" + "="*60)
    print("   ORDENAMIENTO EXTERNO - MEZCLA DIRECTA, MEZCLA EQUILIBRADA E INTERCALACIÓN")
    print("="*60)
    print("\nPor favor, ingrese los números que desea ordenar.")
    print("NOTA: El programa puede manejar hasta 100+ números, pero la visualización")
    print("      se adaptará automáticamente (las barras se volverán más delgadas).\n")
    
    while True:
        try:
            opcion = input("¿Cómo desea ingresar los datos?\n1 - Escribir números manualmente\n2 - Generar números aleatorios\nOpción (1/2): ")
            
            if opcion == "1":
                entrada = input("\nIngrese los números separados por coma o espacio: ")
                import re
                numeros = re.findall(r'-?\d+', entrada)
                if len(numeros) < 2:
                    print("Error: Debe ingresar al menos 2 números. Intente nuevamente.\n")
                    continue
                if len(numeros) > 200:
                    confirmar = input(f"Advertencia: Ingresó {len(numeros)} números. ¿Continuar? (s/n): ")
                    if confirmar.lower() != 's':
                        continue
                datos = [int(x) for x in numeros]
                print(f"\n✓ Datos cargados: {len(datos)} elementos")
                print(f"✓ Primeros 10: {datos[:10]}{'...' if len(datos) > 10 else ''}")
                return datos
            
            elif opcion == "2":
                while True:
                    try:
                        cantidad = int(input("\n¿Cuántos números desea generar? (2-100, o más escribiendo otro número): "))
                        if cantidad < 2:
                            print("La cantidad debe ser al menos 2. Intente nuevamente.")
                            continue
                        
                        if cantidad > 100:
                            confirmar = input(f"Advertencia: Generará {cantidad} números. La visualización puede ser lenta. ¿Continuar? (s/n): ")
                            if confirmar.lower() != 's':
                                continue
                        
                        minimo = int(input("Valor mínimo: "))
                        maximo = int(input("Valor máximo: "))
                        
                        if minimo >= maximo:
                            print("El mínimo debe ser menor que el máximo. Intente nuevamente.")
                            continue
                        
                        print("\nTipos de generación:")
                        print("  uniforme    - Números aleatorios uniformemente distribuidos")
                        print("  normal      - Distribución normal (campana de Gauss)")
                        print("  sin_repetir - Números únicos sin repetición")
                        print("  inverso     - Secuencia descendente")
                        print("  casi        - Casi ordenado (pocos intercambios)")
                        tipo = input("Tipo de generación: ").lower()
                        
                        if tipo == "uniforme":
                            datos = [random.randint(minimo, maximo) for _ in range(cantidad)]
                        elif tipo == "normal":
                            media = (minimo + maximo) / 2
                            desviacion = (maximo - minimo) / 6
                            datos = []
                            for _ in range(cantidad):
                                valor = int(random.gauss(media, desviacion))
                                valor = max(minimo, min(maximo, valor))
                                datos.append(valor)
                        elif tipo == "sin_repetir":
                            if cantidad > (maximo - minimo + 1):
                                print(f"No se pueden generar {cantidad} números únicos en el rango [{minimo}, {maximo}]")
                                continue
                            datos = random.sample(range(minimo, maximo + 1), cantidad)
                        elif tipo == "inverso":
                            datos = list(range(maximo, maximo - cantidad, -1))
                            while len(datos) < cantidad:
                                datos.append(minimo)
                            datos = datos[:cantidad]
                        elif tipo == "casi":
                            datos = list(range(minimo, minimo + cantidad))
                            intercambios = max(1, cantidad // 20)
                            for _ in range(intercambios):
                                i, j = random.sample(range(cantidad), 2)
                                datos[i], datos[j] = datos[j], datos[i]
                        else:
                            print("Tipo no reconocido, usando uniforme")
                            datos = [random.randint(minimo, maximo) for _ in range(cantidad)]
                        
                        # Mezclar un poco si no es inverso o casi
                        if tipo not in ["inverso", "casi"]:
                            random.shuffle(datos)
                        
                        print(f"\n✓ Datos generados: {len(datos)} elementos")
                        print(f"✓ Primeros 10: {datos[:10]}{'...' if len(datos) > 10 else ''}")
                        print(f"✓ Rango: [{min(datos)}, {max(datos)}]")
                        return datos
                    
                    except ValueError:
                        print("Error: Ingrese valores numéricos válidos.\n")
            
            else:
                print("Opción inválida. Ingrese 1 o 2.\n")
        
        except KeyboardInterrupt:
            print("\n\nPrograma cancelado por el usuario.")
            exit()
        except Exception as e:
            print(f"Error: {e}. Intente nuevamente.\n")

if __name__ == "__main__":
    datos_usuario = obtener_datos_de_terminal()
    
    print("\n" + "="*60)
    print("Iniciando interfaz gráfica...")
    print(f"Cantidad de elementos a ordenar: {len(datos_usuario)}")
    print("Los tres algoritmos se ejecutarán simultáneamente.")
    print("Presione el botón 'INICIAR ORDENAMIENTO SIMULTÁNEO' para comenzar.")
    print("="*60 + "\n")
    
    root = tk.Tk()
    app = OrdenamientoExternoSimultaneo(root, datos_usuario)
    root.mainloop()
