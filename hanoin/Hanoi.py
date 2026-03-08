import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
from queue import Queue
import gc

class Pila:
    __slots__ = ['items', 'nombre']  
    
    def __init__(self, nombre):
        self.items = []
        self.nombre = nombre
    
    def esta_vacia(self):
        return len(self.items) == 0
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.esta_vacia():
            return self.items.pop()
        return None
    
    def peek(self):
        if not self.esta_vacia():
            return self.items[-1]
        return None

class TorreHanoiGrafico:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Torre de Hanoi")
        self.ventana.geometry("900x600")
        self.ventana.resizable(False, False)
        

        self.num_discos = 5
        self.velocidad = 200 
        self.movimientos = 0
        self.animando = False
        self.pausado = False
        self.movimiento_actual = 0
        self.tiempo_inicio = 0
        self.tiempo_total = 0
        self.calidad_grafica = "baja"  
        self.modo_ahorro = True
        
        self.colores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        
        self.cola_movimientos = Queue()
        self.cola_actualizaciones = Queue()
        
        self.crear_interfaz()
        self.inicializar_torres()
        
    def crear_interfaz(self):
        main_frame = ttk.Frame(self.ventana)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(main_frame, width=880, height=400, bg='white',
                                highlightthickness=0)
        self.canvas.pack(pady=5)
        
        frame_controles = ttk.Frame(main_frame)
        frame_controles.pack(fill=tk.X, padx=5, pady=5)
        
        estilo_boton = {'width': 8, 'height': 1, 'font': ('Arial', 9)}
        
        ttk.Label(frame_controles, text="Discos:").grid(row=0, column=0, padx=2)
        
        self.btn_5 = tk.Button(frame_controles, text="5", command=lambda: self.set_discos(5),
                               bg='#3498db', fg='white', **estilo_boton)
        self.btn_5.grid(row=0, column=1, padx=1)
        
        self.btn_10 = tk.Button(frame_controles, text="10", command=lambda: self.set_discos(10),
                                bg='#3498db', fg='white', **estilo_boton)
        self.btn_10.grid(row=0, column=2, padx=1)
        
        self.btn_30 = tk.Button(frame_controles, text="30", command=lambda: self.set_discos(30),
                                bg='#e67e22', fg='white', **estilo_boton)
        self.btn_30.grid(row=0, column=3, padx=1)
        
        self.btn_64 = tk.Button(frame_controles, text="64", command=lambda: self.set_discos(64),
                                bg='#e74c3c', fg='white', **estilo_boton)
        self.btn_64.grid(row=0, column=4, padx=1)
        
        ttk.Label(frame_controles, text="Personalizado:").grid(row=1, column=0, padx=2, pady=2)
        
        self.discos_var = tk.IntVar(value=5)
        self.discos_spinbox = tk.Spinbox(frame_controles, from_=1, to=64, width=5,
                                         textvariable=self.discos_var)
        self.discos_spinbox.grid(row=1, column=1, padx=1, pady=2)
        
        self.btn_aplicar = tk.Button(frame_controles, text="OK", command=self.aplicar_discos,
                                     bg='#2ecc71', fg='white', width=3)
        self.btn_aplicar.grid(row=1, column=2, padx=1, pady=2)
        
 
        self.btn_iniciar = tk.Button(frame_controles, text="▶ Iniciar", 
                                     command=self.iniciar_solucion,
                                     bg='#4CAF50', fg='white', width=10)
        self.btn_iniciar.grid(row=1, column=3, padx=2, pady=2)
        
        self.btn_pausa = tk.Button(frame_controles, text="⏸ Pausa", 
                                   command=self.pausar_animacion,
                                   bg='#2196F3', fg='white', width=10, state='disabled')
        self.btn_pausa.grid(row=1, column=4, padx=2, pady=2)
        
        self.btn_reiniciar = tk.Button(frame_controles, text="↺ Reiniciar", 
                                       command=self.reiniciar_juego,
                                       bg='#FF5722', fg='white', width=10)
        self.btn_reiniciar.grid(row=1, column=5, padx=2, pady=2)
        
        ttk.Label(frame_controles, text="Calidad gráfica:").grid(row=2, column=0, padx=2, pady=2)
        
        self.calidad_var = tk.StringVar(value="baja")
        calidad_combo = ttk.Combobox(frame_controles, textvariable=self.calidad_var,
                                     values=["baja", "media", "alta"], width=8, state='readonly')
        calidad_combo.grid(row=2, column=1, padx=1, pady=2)
        calidad_combo.bind('<<ComboboxSelected>>', self.cambiar_calidad)
        
        ttk.Label(frame_controles, text="Velocidad:").grid(row=2, column=2, padx=2, pady=2)
        
        self.velocidad_var = tk.IntVar(value=200)
        self.velocidad_scale = tk.Scale(frame_controles, from_=0, to=500, 
                                       orient=tk.HORIZONTAL, length=100,
                                       variable=self.velocidad_var, showvalue=0)
        self.velocidad_scale.grid(row=2, column=3, padx=1, pady=2)
        
        ttk.Label(frame_controles, text=f"{self.velocidad_var.get()}ms").grid(row=2, column=4, padx=1)
        
        self.ahorro_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame_controles, text="Modo ahorro", 
                       variable=self.ahorro_var).grid(row=2, column=5, padx=2)
        
        info_frame = ttk.Frame(main_frame, relief=tk.GROOVE)
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.movimientos_label = ttk.Label(info_frame, text="Mov: 0", font=('Arial', 10))
        self.movimientos_label.pack(side=tk.LEFT, padx=10)
        
        self.tiempo_label = ttk.Label(info_frame, text="Tiempo: 0.0s", font=('Arial', 10))
        self.tiempo_label.pack(side=tk.LEFT, padx=10)
        
        self.estimado_label = ttk.Label(info_frame, text="Total: 31 mov", font=('Arial', 9))
        self.estimado_label.pack(side=tk.LEFT, padx=10)
        
        self.text_frame = ttk.Frame(main_frame)
        self.text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(self.text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_area = tk.Text(self.text_frame, height=6, yscrollcommand=scrollbar.set,
                                 bg='black', fg='lime', font=('Courier', 9),
                                 wrap=tk.NONE, state='disabled')
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_area.yview)
        
        self.text_buffer = []  
        self.buffer_size = 100
        
        self.text_frame.pack_forget()
        
    def cambiar_calidad(self, event=None):
        """Cambia la calidad gráfica para mejorar rendimiento"""
        self.calidad_grafica = self.calidad_var.get()
        if self.num_discos <= 10:  
            self.inicializar_torres()
    
    def set_discos(self, num):
        """Establece número de discos con validación de rendimiento"""
        self.num_discos = num
        self.discos_var.set(num)
        
        if num > 15:
            self.calidad_var.set("baja")
            self.calidad_grafica = "baja"
        elif num > 8:
            self.calidad_var.set("media")
            self.calidad_grafica = "media"
        
        self.inicializar_torres()
        
        movimientos_totales = 2**num - 1
        self.estimado_label.config(text=f"Total: {self.formatear_numero(movimientos_totales)} mov")
    
    def formatear_numero(self, num):
        """Formatea números grandes de forma legible"""
        if num < 1000:
            return str(num)
        elif num < 1000000:
            return f"{num/1000:.1f}K"
        elif num < 1000000000:
            return f"{num/1000000:.1f}M"
        else:
            return f"{num/1000000000:.1f}B"
    
    def aplicar_discos(self):
        try:
            num = int(self.discos_var.get())
            if 1 <= num <= 64:
                self.set_discos(num)
        except ValueError:
            pass
    
    def inicializar_torres(self):
        self.canvas.delete("all")
        gc.collect()
        
        if self.calidad_grafica == "baja":

            self.canvas.create_rectangle(50, 360, 850, 375, fill='#8B4513', outline='')
            
            for x in [150, 450, 750]:
                self.canvas.create_rectangle(x, 180, x+10, 360, fill='#654321', outline='')
            
            self.canvas.create_text(155, 385, text="O", font=('Arial', 10))
            self.canvas.create_text(455, 385, text="A", font=('Arial', 10))
            self.canvas.create_text(755, 385, text="D", font=('Arial', 10))
        else:
            self.canvas.create_rectangle(50, 360, 850, 375, fill='#8B4513', outline='')
            for x in [150, 450, 750]:
                self.canvas.create_rectangle(x, 180, x+15, 360, fill='#654321', outline='')
            self.canvas.create_text(155, 385, text="Origen", font=('Arial', 9))
            self.canvas.create_text(455, 385, text="Auxiliar", font=('Arial', 9))
            self.canvas.create_text(755, 385, text="Destino", font=('Arial', 9))
        
        self.origen = Pila("Origen")
        self.auxiliar = Pila("Auxiliar")
        self.destino = Pila("Destino")
        self.movimientos = 0
        self.movimiento_actual = 0
        
        for i in range(self.num_discos, 0, -1):
            self.origen.push(i)
        
        if self.num_discos <= 12:
            self.dibujar_discos()
        elif self.num_discos <= 20:
            self.dibujar_discos_simplificado()
        else:
            self.canvas.create_text(450, 250, 
                                   text=f"{self.num_discos} discos", 
                                   font=('Arial', 14), fill='blue')
            self.canvas.create_text(450, 280, 
                                   text="Usar modo texto", 
                                   font=('Arial', 12), fill='red')
        
        self.actualizar_etiquetas()
    
    def dibujar_discos_simplificado(self):
        """Versión simplificada para muchos discos"""
        self.dibujar_torre_lineas(self.origen, 155, 350)
        self.dibujar_torre_lineas(self.auxiliar, 455, 350)
        self.dibujar_torre_lineas(self.destino, 755, 350)
    
    def dibujar_torre_lineas(self, pila, x, y_base):
        """Dibuja discos como líneas para ahorrar recursos"""
        altura = min(10, 200 // len(pila.items)) if pila.items else 0
        y = y_base
        
        for disco in pila.items:
            if self.calidad_grafica == "baja":
                self.canvas.create_line(x-20, y, x+20, y, fill='black', width=2)
            else:
                self.canvas.create_rectangle(x-20, y-altura, x+20, y, 
                                           fill=self.colores[disco % len(self.colores)],
                                           outline='')
            y -= altura
    
    def dibujar_discos(self):
        """Versión optimizada de dibujo"""
        if self.ahorro_var.get() and self.num_discos > 8:
            self.dibujar_discos_simplificado()
            return
            
        self.dibujar_torre_discos(self.origen, 155, 350)
        self.dibujar_torre_discos(self.auxiliar, 455, 350)
        self.dibujar_torre_discos(self.destino, 755, 350)
    
    def dibujar_torre_discos(self, pila, x_centro, y_base):
        if not pila.items:
            return
            
        altura = min(18, 250 // (self.num_discos + 2))
        y = y_base
        
        for disco in pila.items:
            ancho = 30 + disco * 2
            if self.calidad_grafica == "media":
                ancho = 30 + disco * 1.5
            
            x1 = x_centro - ancho // 2
            x2 = x_centro + ancho // 2
            y1 = y - altura
            y2 = y
            
            self.canvas.create_rectangle(x1, y1, x2, y2, 
                                       fill=self.colores[disco % len(self.colores)],
                                       outline='black', width=1)
            y -= altura
    
    def mover_disco(self, desde, hacia):
        """Versión optimizada de movimiento"""
        if desde.esta_vacia():
            return False
            
        disco = desde.peek()
        if not hacia.esta_vacia() and hacia.peek() < disco:
            return False
        
        desde.pop()
        hacia.push(disco)
        self.movimientos += 1
        
        if not self.ahorro_var.get() or self.movimientos % 5 == 0:
            self.actualizar_interfaz()
        
        if self.text_frame.winfo_ismapped():
            self.text_buffer.append(f"{self.movimientos}: D{disco} {desde.nombre[0]}→{hacia.nombre[0]}\n")
            if len(self.text_buffer) >= self.buffer_size:
                self.actualizar_texto()
        
        return True
    
    def actualizar_interfaz(self):
        """Actualización optimizada de la interfaz"""
        if self.canvas.winfo_ismapped() and self.num_discos <= 15:
            self.canvas.delete("all")
            self.dibujar_base_torres()
            self.dibujar_discos()
        
        if self.animando:
            tiempo = time.time() - self.tiempo_inicio
            self.tiempo_label.config(text=f"Tiempo: {tiempo:.1f}s")
        
        self.movimientos_label.config(text=f"Mov: {self.movimientos}")
        self.ventana.update_idletasks()  
    
    def actualizar_texto(self):
        """Actualiza el área de texto con buffer"""
        if not self.text_buffer:
            return
            
        self.text_area.config(state='normal')
        for linea in self.text_buffer:
            self.text_area.insert(tk.END, linea)
        self.text_area.see(tk.END)
        self.text_area.config(state='disabled')
        self.text_buffer = []
    
    def dibujar_base_torres(self):
        """Versión optimizada de dibujo base"""
        self.canvas.create_rectangle(50, 360, 850, 375, fill='#8B4513', outline='')
        
        for x in [150, 450, 750]:
            if self.calidad_grafica == "baja":
                self.canvas.create_line(x, 180, x, 360, fill='#654321', width=4)
            else:
                self.canvas.create_rectangle(x, 180, x+12, 360, fill='#654321', outline='')
    
    def iniciar_solucion(self):
        if self.animando:
            return
        
        self.num_discos = self.discos_var.get()
        
        usar_texto = self.num_discos > 15
        
        if usar_texto:
            self.canvas.pack_forget()
            self.text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        else:
            self.text_frame.pack_forget()
            self.canvas.pack(pady=5)
        
        self.inicializar_torres()
        
        self.animando = True
        self.pausado = False
        self.tiempo_inicio = time.time()
        self.movimientos = 0
        self.movimiento_actual = 0
        self.text_buffer = []
        
        self.btn_pausa.config(state='normal', text='⏸ Pausa')
        self.btn_iniciar.config(state='disabled')
        
        thread = threading.Thread(target=self.resolver_en_hilo)
        thread.daemon = True
        thread.start()
    
    def resolver_en_hilo(self):
        """Ejecuta la solución en un hilo separado"""
        self.resolver_recursivo(self.num_discos, self.origen, self.destino, self.auxiliar)
        self.ventana.after(0, self.finalizar_solucion)
    
    def resolver_recursivo(self, n, origen, destino, auxiliar):
        """Versión recursiva optimizada"""
        if n == 1:
            if not self.pausado and self.animando:
                self.mover_disco(origen, destino)
                # Control de velocidad
                if self.velocidad_var.get() > 0:
                    time.sleep(self.velocidad_var.get() / 1000.0)
        else:
            self.resolver_recursivo(n-1, origen, auxiliar, destino)
            if not self.pausado and self.animando:
                self.mover_disco(origen, destino)
                if self.velocidad_var.get() > 0:
                    time.sleep(self.velocidad_var.get() / 1000.0)
            self.resolver_recursivo(n-1, auxiliar, destino, origen)
    
    def finalizar_solucion(self):
        self.tiempo_total = time.time() - self.tiempo_inicio
        self.animando = False
        
        if self.text_buffer:
            self.actualizar_texto()
        
        self.btn_pausa.config(state='disabled', text='⏸ Pausa')
        self.btn_iniciar.config(state='normal')
        
        messagebox.showinfo("Completado", 
                           f"Movimientos: {self.movimientos:,}\n"
                           f"Tiempo: {self.tiempo_total:.2f}s")
    
    def pausar_animacion(self):
        if self.btn_pausa['text'] == '⏸ Pausa':
            self.btn_pausa.config(text='▶ Continuar')
            self.pausado = True
            if self.animando:
                self.tiempo_total += time.time() - self.tiempo_inicio
        else:
            self.btn_pausa.config(text='⏸ Pausa')
            self.pausado = False
            if self.animando:
                self.tiempo_inicio = time.time()
    
    def reiniciar_juego(self):
        self.animando = False
        self.pausado = False
        self.btn_pausa.config(state='disabled', text='⏸ Pausa')
        self.btn_iniciar.config(state='normal')
        self.canvas.pack(pady=5)
        self.text_frame.pack_forget()
        self.inicializar_torres()
        gc.collect()  # Forzar limpieza de memoria
    
    def actualizar_etiquetas(self):
        mov_totales = 2**self.num_discos - 1
        self.movimientos_label.config(text="Mov: 0")
        self.tiempo_label.config(text="Tiempo: 0.0s")
        self.estimado_label.config(text=f"Total: {self.formatear_numero(mov_totales)}")
    
    def ejecutar(self):
        self.ventana.mainloop()

if __name__ == "__main__":
    app = TorreHanoiGrafico()
    app.ejecutar()