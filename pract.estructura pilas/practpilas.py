import tkinter as tk
from tkinter import messagebox, ttk
import random
import time

class PilaVisual:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Pila (Stack) - Versión Avanzada")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
    
        self.pila = []
        self.max_elementos = 8 
        self.historial_operaciones = []
        
        self.colores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', 
                       '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F',
                       '#FF9F1C', '#2EC4B6']
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        titulo = tk.Label(main_frame, text="VISUALIZADOR DE PILA (LIFO)", 
                         font=('Arial', 20, 'bold'), bg='#f0f0f0', fg='#333')
        titulo.pack(pady=10)
        
        stats_frame = tk.Frame(main_frame, bg='#e0e0e0', relief='ridge', bd=2)
        stats_frame.pack(fill='x', pady=(0, 10))
        
        self.stats_text = tk.StringVar()
        self.stats_text.set("📊 Tamaño: 0 | Capacidad: 10 | Operaciones: 0")
        stats_label = tk.Label(stats_frame, textvariable=self.stats_text, 
                              font=('Arial', 11), bg='#e0e0e0', pady=5)
        stats_label.pack()
        
        content_frame = tk.Frame(main_frame, bg='#f0f0f0')
        content_frame.pack(expand=True, fill='both')
        
        left_frame = tk.Frame(content_frame, bg='#f0f0f0')
        left_frame.pack(side='left', expand=True, fill='both', padx=(0, 10))
        
        pila_container = tk.Frame(left_frame, bg='white', relief='solid', 
                                   borderwidth=2)
        pila_container.pack(expand=True, fill='both')
        
        self.canvas = tk.Canvas(pila_container, bg='white', height=450)
        self.canvas.pack(expand=True, fill='both', padx=10, pady=10)
        
        right_frame = tk.Frame(content_frame, bg='#f0f0f0', width=300)
        right_frame.pack(side='right', fill='both', padx=(10, 0))
        right_frame.pack_propagate(False)
        
        basic_frame = tk.LabelFrame(right_frame, text="🔧 Operaciones Básicas", 
                                   bg='#f0f0f0', font=('Arial', 11, 'bold'))
        basic_frame.pack(fill='x', pady=(0, 10))
        
        input_frame = tk.Frame(basic_frame, bg='#f0f0f0')
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Valor:", font=('Arial', 11), 
                bg='#f0f0f0').pack(side='left', padx=5)
        
        self.entry_valor = tk.Entry(input_frame, font=('Arial', 11), 
                                   width=15, justify='center')
        self.entry_valor.pack(side='left', padx=5)
        self.entry_valor.bind('<Return>', lambda e: self.push())
        
        btn_frame = tk.Frame(basic_frame, bg='#f0f0f0')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="PUSH", command=self.push,
                 bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'),
                 width=10, pady=5).grid(row=0, column=0, padx=5, pady=2)
        
        tk.Button(btn_frame, text="POP", command=self.pop,
                 bg='#f44336', fg='white', font=('Arial', 10, 'bold'),
                 width=10, pady=5).grid(row=0, column=1, padx=5, pady=2)
        
        tk.Button(btn_frame, text="PEEK", command=self.peek,
                 bg='#FF9800', fg='white', font=('Arial', 10, 'bold'),
                 width=10, pady=5).grid(row=1, column=0, padx=5, pady=2)
        
        tk.Button(btn_frame, text="IS EMPTY", command=self.is_empty,
                 bg='#9C27B0', fg='white', font=('Arial', 10, 'bold'),
                 width=10, pady=5).grid(row=1, column=1, padx=5, pady=2)
        
        advanced_frame = tk.LabelFrame(right_frame, text="🚀 Operaciones Avanzadas", 
                                     bg='#f0f0f0', font=('Arial', 11, 'bold'))
        advanced_frame.pack(fill='x', pady=(0, 10))
        
        adv_btn_frame = tk.Frame(advanced_frame, bg='#f0f0f0')
        adv_btn_frame.pack(pady=10)
        
        tk.Button(adv_btn_frame, text="🎲 Aleatorio Múltiple", 
                 command=self.push_multiple,
                 bg='#2196F3', fg='white', font=('Arial', 10),
                 width=15, pady=3).grid(row=0, column=0, padx=5, pady=2)
        
        tk.Button(adv_btn_frame, text="🔄 Invertir Pila", 
                 command=self.invertir_pila,
                 bg='#FF4081', fg='white', font=('Arial', 10),
                 width=15, pady=3).grid(row=0, column=1, padx=5, pady=2)
        
        tk.Button(adv_btn_frame, text="🔍 Buscar Elemento", 
                 command=self.buscar_elemento,
                 bg='#7C4DFF', fg='white', font=('Arial', 10),
                 width=15, pady=3).grid(row=1, column=0, padx=5, pady=2)
        
        tk.Button(adv_btn_frame, text="📋 Tamaño de Pila", 
                 command=self.mostrar_tamano,
                 bg='#00BCD4', fg='white', font=('Arial', 10),
                 width=15, pady=3).grid(row=1, column=1, padx=5, pady=2)
        
        control_frame = tk.LabelFrame(right_frame, text="⚙️ Control de Pila", 
                                     bg='#f0f0f0', font=('Arial', 11, 'bold'))
        control_frame.pack(fill='x', pady=(0, 10))
        
        control_btn_frame = tk.Frame(control_frame, bg='#f0f0f0')
        control_btn_frame.pack(pady=10)
        
        tk.Button(control_btn_frame, text="🧹 Vaciar Pila", 
                 command=self.vaciar,
                 bg='#F44336', fg='white', font=('Arial', 10, 'bold'),
                 width=15, pady=3).grid(row=0, column=0, padx=5, pady=2)
        
        tk.Button(control_btn_frame, text="💾 Guardar Estado", 
                 command=self.guardar_estado,
                 bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'),
                 width=15, pady=3).grid(row=0, column=1, padx=5, pady=2)
        
        tk.Button(control_btn_frame, text="📂 Cargar Estado", 
                 command=self.cargar_estado,
                 bg='#FF9800', fg='white', font=('Arial', 10, 'bold'),
                 width=15, pady=3).grid(row=1, column=0, padx=5, pady=2)
        
        tk.Button(control_btn_frame, text="📊 Ver Historial", 
                 command=self.ver_historial,
                 bg='#9C27B0', fg='white', font=('Arial', 10, 'bold'),
                 width=15, pady=3).grid(row=1, column=1, padx=5, pady=2)
        
        
        message_frame = tk.Frame(main_frame, bg='#f0f0f0', height=60)
        message_frame.pack(fill='x', pady=(10, 0))
        message_frame.pack_propagate(False)
        
        self.message_label = tk.Label(message_frame, text="", font=('Arial', 10),
                                     bg='#e8e8e8', fg='#333', wraplength=800,
                                     relief='sunken', padx=10, pady=5)
        self.message_label.pack(expand=True, fill='both')
        
        self.estado_label = tk.Label(main_frame, text="Pila vacía", 
                                    font=('Arial', 10, 'italic'),
                                    bg='#f0f0f0', fg='#666')
        self.estado_label.pack(pady=5)
        
        self.actualizar_visualizacion()
        
    def push(self):
        valor = self.entry_valor.get()
        
        if not valor:
            self.mostrar_mensaje("⚠️ Por favor, ingresa un valor.", 'warning')
            return
        
        if len(self.pila) >= self.max_elementos:
            self.mostrar_mensaje(f"❌ Pila llena (máximo {self.max_elementos} elementos)", 'error')
            return
        
        self.pila.append(valor)
        self.registrar_operacion(f"PUSH: {valor}")
        self.entry_valor.delete(0, tk.END)
        self.actualizar_visualizacion()
        self.mostrar_mensaje(f"✅ Push exitoso: '{valor}' agregado a la pila", 'success')
        
    def pop(self):
        if not self.pila:
            self.mostrar_mensaje("❌ No hay elementos para desapilar", 'error')
            return
        
        # Verificar si se ingresó un valor específico para eliminar
        valor_especifico = self.entry_valor.get().strip()
        
        if valor_especifico:  # Si hay un valor en el campo de entrada
            if valor_especifico in self.pila:
                if valor_especifico != self.pila[-1]:
                    # CASO ESPECIAL: Queremos eliminar un elemento que no es el tope
                    
                    # Encontrar la posición del elemento a eliminar
                    posicion = self.pila.index(valor_especifico)
                    elementos_encima = len(self.pila) - 1 - posicion
                    
                    self.mostrar_mensaje(f"🔄 Eliminando '{valor_especifico}' que está en posición {posicion} desde la base", 'info')
                    self.root.update()
                    time.sleep(0.5)
                    
                    # Guardar todos los elementos que están encima del que queremos eliminar
                    elementos_encima_lista = []
                    for i in range(elementos_encima):
                        elementos_encima_lista.append(self.pila.pop())
                        self.registrar_operacion(f"POP temporal {i+1}: {elementos_encima_lista[-1]}")
                        self.actualizar_visualizacion()
                        self.root.update()
                        time.sleep(0.5)
                    
                    # Ahora eliminamos el elemento deseado (que ahora está en el tope)
                    elemento_eliminado = self.pila.pop()
                    self.registrar_operacion(f"POP (elemento objetivo): {elemento_eliminado}")
                    self.actualizar_visualizacion()
                    self.root.update()
                    time.sleep(0.5)
                    
                    # Restauramos los elementos que estaban encima (en orden inverso)
                    for elemento in reversed(elementos_encima_lista):
                        if len(self.pila) < self.max_elementos:
                            self.pila.append(elemento)
                            self.registrar_operacion(f"PUSH restauración: {elemento}")
                            self.actualizar_visualizacion()
                            self.root.update()
                            time.sleep(0.5)
                        else:
                            self.mostrar_mensaje(f"⚠️ No se pudo restaurar '{elemento}' (pila llena)", 'warning')
                    
                    self.mostrar_mensaje(f"✅ Proceso completado: Se eliminó '{valor_especifico}' y se restauraron {elementos_encima} elementos", 'success')
                else:
                    # Si es el tope, proceder con pop normal
                    valor = self.pila.pop()
                    self.registrar_operacion(f"POP: {valor}")
                    self.entry_valor.delete(0, tk.END)
                    self.mostrar_mensaje(f"✅ Pop exitoso: '{valor}' removido de la pila", 'success')
            else:
                # Si el elemento no existe, agregarlo automáticamente y luego eliminarlo
                if len(self.pila) >= self.max_elementos:
                    self.mostrar_mensaje(f"❌ No hay espacio para agregar '{valor_especifico}'", 'error')
                    return
                
                # Agregar el elemento a la pila
                self.pila.append(valor_especifico)
                self.registrar_operacion(f"PUSH AUTO: {valor_especifico}")
                
                # Pequeña pausa para visualizar el elemento agregado
                self.actualizar_visualizacion()
                self.root.update()
                time.sleep(0.5)
                
                # Eliminar el elemento recién agregado
                valor = self.pila.pop()
                self.registrar_operacion(f"POP AUTO: {valor}")
                self.mostrar_mensaje(f"🔄 Elemento '{valor_especifico}' agregado y eliminado automáticamente", 'success')
                self.entry_valor.delete(0, tk.END)
        else:
            # Pop normal sin valor específico
            valor = self.pila.pop()
            self.registrar_operacion(f"POP: {valor}")
            self.mostrar_mensaje(f"✅ Pop exitoso: '{valor}' removido de la pila", 'success')
        
        self.actualizar_visualizacion()
        
    def peek(self):
        if not self.pila:
            self.mostrar_mensaje("📭 La pila está vacía", 'info')
        else:
            self.mostrar_mensaje(f"🔝 Elemento en el tope: '{self.pila[-1]}'", 'info')
            
    def is_empty(self):
        if not self.pila:
            self.mostrar_mensaje("✅ La pila está VACÍA", 'success')
        else:
            self.mostrar_mensaje(f"❌ La pila NO está vacía (tiene {len(self.pila)} elementos)", 'info')
    
    def push_multiple(self):
        """Agrega múltiples elementos aleatorios"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Push Múltiple")
        ventana.geometry("300x200")
        ventana.configure(bg='#f0f0f0')
        
        tk.Label(ventana, text="Número de elementos:", 
                bg='#f0f0f0').pack(pady=10)
        
        spinbox = tk.Spinbox(ventana, from_=1, to=5, width=10)
        spinbox.pack(pady=5)
        
        tk.Label(ventana, text="Tipo de datos:", 
                bg='#f0f0f0').pack(pady=5)
        
        tipo_var = tk.StringVar(value="numeros")
        tk.Radiobutton(ventana, text="Números", variable=tipo_var, 
                      value="numeros", bg='#f0f0f0').pack()
        tk.Radiobutton(ventana, text="Letras", variable=tipo_var, 
                      value="letras", bg='#f0f0f0').pack()
        tk.Radiobutton(ventana, text="Símbolos", variable=tipo_var, 
                      value="simbolos", bg='#f0f0f0').pack()
        
        def agregar():
            cantidad = int(spinbox.get())
            tipo = tipo_var.get()
            
            if len(self.pila) + cantidad > self.max_elementos:
                self.mostrar_mensaje(f"❌ No hay espacio para {cantidad} elementos", 'error')
                ventana.destroy()
                return
            
            for i in range(cantidad):
                if tipo == "numeros":
                    valor = str(random.randint(1, 100))
                elif tipo == "letras":
                    valor = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                else:
                    valor = random.choice(['★', '♦', '♣', '♥', '♠', '☀', '☁', '⚡'])
                
                self.pila.append(valor)
                self.registrar_operacion(f"PUSH MÚLTIPLE: {valor}")
            
            self.actualizar_visualizacion()
            self.mostrar_mensaje(f"✅ {cantidad} elementos agregados aleatoriamente", 'success')
            ventana.destroy()
        
        tk.Button(ventana, text="Agregar", command=agregar,
                 bg='#4CAF50', fg='white').pack(pady=10)
    
    def invertir_pila(self):
        """Invierte el orden de la pila"""
        if len(self.pila) < 2:
            self.mostrar_mensaje("❌ Se necesitan al menos 2 elementos para invertir", 'error')
            return
        
        self.pila.reverse()
        self.registrar_operacion("INVERTIR PILA")
        self.actualizar_visualizacion()
        self.mostrar_mensaje("🔄 Pila invertida exitosamente", 'success')
    
    def buscar_elemento(self):
        """Busca un elemento en la pila"""
        if not self.pila:
            self.mostrar_mensaje("📭 La pila está vacía", 'info')
            return
        
        ventana = tk.Toplevel(self.root)
        ventana.title("Buscar Elemento")
        ventana.geometry("300x150")
        ventana.configure(bg='#f0f0f0')
        
        tk.Label(ventana, text="Elemento a buscar:", 
                bg='#f0f0f0').pack(pady=10)
        
        entry = tk.Entry(ventana, font=('Arial', 11))
        entry.pack(pady=5)
        entry.focus()
        
        def buscar():
            elemento = entry.get()
            if elemento in self.pila:
                posiciones = [i for i, x in enumerate(self.pila) if x == elemento]
                desde_tope = [len(self.pila) - 1 - i for i in posiciones]
                
                mensaje = f"✅ '{elemento}' encontrado:\n"
                mensaje += f"• Posiciones desde base: {posiciones}\n"
                mensaje += f"• Posiciones desde tope: {desde_tope}"
                
                # Resaltar el elemento en la visualización
                self.resaltar_elemento(elemento)
            else:
                mensaje = f"❌ '{elemento}' no encontrado en la pila"
            
            self.mostrar_mensaje(mensaje, 'info')
            ventana.destroy()
        
        tk.Button(ventana, text="Buscar", command=buscar,
                 bg='#2196F3', fg='white').pack(pady=10)
    
    def resaltar_elemento(self, elemento):
        """Resalta visualmente un elemento en la pila"""
        self.actualizar_visualizacion()
        # Este método podría mejorarse para resaltar visualmente
        self.root.after(2000, self.actualizar_visualizacion)
    
    def mostrar_tamano(self):
        """Muestra información detallada del tamaño"""
        capacidad_restante = self.max_elementos - len(self.pila)
        porcentaje = (len(self.pila) / self.max_elementos) * 100
        
        mensaje = f"📊 INFORMACIÓN DE LA PILA:\n"
        mensaje += f"• Elementos actuales: {len(self.pila)}\n"
        mensaje += f"• Capacidad máxima: {self.max_elementos}\n"
        mensaje += f"• Espacio restante: {capacidad_restante}\n"
        mensaje += f"• Ocupación: {porcentaje:.1f}%\n"
        
        if self.pila:
            mensaje += f"• Elemento tope: '{self.pila[-1]}'\n"
            mensaje += f"• Elemento base: '{self.pila[0]}'"
        
        self.mostrar_mensaje(mensaje, 'info')
    
    def guardar_estado(self):
        """Guarda el estado actual de la pila"""
        import pickle
        try:
            with open('pila_guardada.pkl', 'wb') as f:
                pickle.dump(self.pila, f)
            self.registrar_operacion("GUARDAR ESTADO")
            self.mostrar_mensaje("💾 Estado guardado exitosamente", 'success')
        except Exception as e:
            self.mostrar_mensaje(f"❌ Error al guardar: {str(e)}", 'error')
    
    def cargar_estado(self):
        """Carga un estado previamente guardado"""
        import pickle
        import os
        
        if not os.path.exists('pila_guardada.pkl'):
            self.mostrar_mensaje("❌ No hay estado guardado", 'error')
            return
        
        try:
            with open('pila_guardada.pkl', 'rb') as f:
                pila_cargada = pickle.load(f)
            
            if len(pila_cargada) > self.max_elementos:
                self.mostrar_mensaje(f"❌ La pila guardada excede la capacidad máxima", 'error')
                return
            
            self.pila = pila_cargada
            self.registrar_operacion("CARGAR ESTADO")
            self.actualizar_visualizacion()
            self.mostrar_mensaje("📂 Estado cargado exitosamente", 'success')
        except Exception as e:
            self.mostrar_mensaje(f"❌ Error al cargar: {str(e)}", 'error')
    
    def ver_historial(self):
        """Muestra el historial de operaciones"""
        if not self.historial_operaciones:
            self.mostrar_mensaje("📋 No hay operaciones registradas", 'info')
            return
        
        ventana = tk.Toplevel(self.root)
        ventana.title("Historial de Operaciones")
        ventana.geometry("400x300")
        ventana.configure(bg='#f0f0f0')
        
        tk.Label(ventana, text="Últimas 20 operaciones:", 
                font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(pady=10)
        
        frame = tk.Frame(ventana)
        frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side='right', fill='y')
        
        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set,
                             font=('Courier', 10))
        listbox.pack(expand=True, fill='both')
        
        scrollbar.config(command=listbox.yview)
        
        for op in self.historial_operaciones[-20:]:
            listbox.insert(tk.END, op)
        
        tk.Button(ventana, text="Cerrar", command=ventana.destroy,
                 bg='#f44336', fg='white').pack(pady=10)
    
    def vaciar(self):
        if not self.pila:
            self.mostrar_mensaje("📭 La pila ya está vacía", 'info')
            return
        
        if messagebox.askyesno("Confirmar", "¿Estás seguro de vaciar la pila?"):
            self.pila.clear()
            self.registrar_operacion("VACIAR PILA")
            self.actualizar_visualizacion()
            self.mostrar_mensaje("🧹 Pila vaciada completamente", 'success')
    
    def registrar_operacion(self, operacion):
        """Registra una operación en el historial"""
        timestamp = time.strftime("%H:%M:%S")
        self.historial_operaciones.append(f"[{timestamp}] {operacion}")
        if len(self.historial_operaciones) > 100:
            self.historial_operaciones.pop(0)
    
    
    def mostrar_mensaje(self, mensaje, tipo='info'):
        """Muestra un mensaje en el panel inferior"""
        colores = {
            'info': '#e3f2fd',
            'success': '#e8f5e8',
            'warning': '#fff3e0',
            'error': '#ffebee'
        }
        
        self.message_label.config(text=mensaje, bg=colores.get(tipo, '#e8e8e8'))
        self.root.after(5000, lambda: self.message_label.config(bg='#e8e8e8', text=""))
    
    def actualizar_visualizacion(self):
        """Actualiza la representación visual de la pila con el tope en la parte superior"""
        self.canvas.delete("all")
        
        if not self.pila:
            # Mostrar mensaje de pila vacía
            self.canvas.create_text(self.canvas.winfo_width()//2 or 200, 
                                   200, text="PILA VACÍA", 
                                   font=('Arial', 20, 'bold'), fill='#ccc')
            self.estado_label.config(text="📭 Pila vacía - Total: 0 elementos")
            self.stats_text.set(f"📊 Tamaño: 0 | Capacidad: {self.max_elementos} | Operaciones: {len(self.historial_operaciones)}")
            return
        
        # Obtener dimensiones del canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1:  # Si el canvas no tiene tamaño todavía
            canvas_width = 400
            canvas_height = 450
        
        # Configuración de dimensiones de los elementos
        alto_elemento = 40
        ancho_elemento = 180
        x_centro = canvas_width // 2
        
        # Calcular la posición Y inicial para centrar verticalmente la pila
        total_alto = len(self.pila) * alto_elemento
        y_inicial = (canvas_height - total_alto) // 2
        
        # Dibujar cada elemento de la pila de ARRIBA a ABAJO
        # El tope (último elemento agregado) va en la parte superior
        for i, valor in enumerate(reversed(self.pila)):
            y_pos = y_inicial + (i * alto_elemento)
            color = self.colores[i % len(self.colores)]
            
            # Dibujar rectángulo del elemento
            self.canvas.create_rectangle(x_centro - ancho_elemento//2, 
                                        y_pos,
                                        x_centro + ancho_elemento//2, 
                                        y_pos + alto_elemento,
                                        fill=color, outline='#333', width=2)
            
            # Dibujar texto del valor
            self.canvas.create_text(x_centro, y_pos + alto_elemento//2,
                                   text=str(valor), 
                                   font=('Arial', 12, 'bold'), 
                                   fill='black')
            
            # Indicador del tope (primer elemento, arriba)
            if i == 0:
                self.canvas.create_text(x_centro - ancho_elemento//2 - 30, 
                                       y_pos + alto_elemento//2,
                                       text="TOPE →", 
                                       font=('Arial', 10, 'bold'), 
                                       fill='#f44336')
            
            # Indicador de la base (último elemento, abajo)
            if i == len(self.pila) - 1:
                self.canvas.create_text(x_centro - ancho_elemento//2 - 30, 
                                       y_pos + alto_elemento//2,
                                       text="BASE →", 
                                       font=('Arial', 10, 'bold'), 
                                       fill='#2196F3')
        
        # Dibujar línea superior (techo de la pila)
        self.canvas.create_line(x_centro - ancho_elemento//2 - 10, 
                                y_inicial - 5,
                                x_centro + ancho_elemento//2 + 10, 
                                y_inicial - 5,
                                fill='#333', width=3)
        
        # Dibujar línea inferior (base de la pila)
        y_base = y_inicial + (len(self.pila) * alto_elemento)
        self.canvas.create_line(x_centro - ancho_elemento//2 - 10, 
                                y_base + 5,
                                x_centro + ancho_elemento//2 + 10, 
                                y_base + 5,
                                fill='#333', width=3)
        
        # Actualizar etiquetas de estado
        self.estado_label.config(text=f"📊 Pila con {len(self.pila)} elementos - Tope: '{self.pila[-1]}' (arriba) - Base: '{self.pila[0]}' (abajo)")
        self.stats_text.set(f"📊 Tamaño: {len(self.pila)} | Capacidad: {self.max_elementos} | Operaciones: {len(self.historial_operaciones)}")


def main():
    root = tk.Tk()
    app = PilaVisual(root)
    root.mainloop()

if __name__ == "__main__":
    main()