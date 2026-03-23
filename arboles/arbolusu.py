import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import math

# ------------------------------------------------------------
# Clase Nodo del Árbol Binario
# ------------------------------------------------------------
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None

# ------------------------------------------------------------
# Funciones de análisis del árbol (nodos, hojas, altura, etc)
# ------------------------------------------------------------
def contar_nodos(raiz):
    if raiz is None:
        return 0
    return 1 + contar_nodos(raiz.izq) + contar_nodos(raiz.der)

def contar_hojas(raiz):
    if raiz is None:
        return 0
    if raiz.izq is None and raiz.der is None:
        return 1
    return contar_hojas(raiz.izq) + contar_hojas(raiz.der)

def altura(raiz):
    if raiz is None:
        return -1
    return 1 + max(altura(raiz.izq), altura(raiz.der))

def es_completo(raiz):
    """
    Verifica si el árbol es COMPLETO:
    - Todos los niveles están completamente llenos excepto posiblemente el último
    - El último nivel tiene todos los nodos lo más a la izquierda posible
    """
    if raiz is None:
        return True
    
    def verificar_completo(nodo, indice, total_nodos):
        if nodo is None:
            return True
        if indice >= total_nodos:
            return False
        return (verificar_completo(nodo.izq, 2 * indice + 1, total_nodos) and
                verificar_completo(nodo.der, 2 * indice + 2, total_nodos))
    
    total = contar_nodos(raiz)
    return verificar_completo(raiz, 0, total)

def es_lleno(raiz):
    """Árbol lleno: todos los nodos tienen 0 o 2 hijos"""
    if raiz is None:
        return True
    if (raiz.izq is None and raiz.der is not None) or (raiz.izq is not None and raiz.der is None):
        return False
    return es_lleno(raiz.izq) and es_lleno(raiz.der)

def es_degenerado(raiz):
    """Cada nodo tiene máximo un hijo"""
    if raiz is None:
        return True
    if raiz.izq and raiz.der:
        return False
    return es_degenerado(raiz.izq) and es_degenerado(raiz.der)

def es_bst(raiz, min_val=float('-inf'), max_val=float('inf')):
    if raiz is None:
        return True
    if not (min_val < raiz.valor < max_val):
        return False
    return (es_bst(raiz.izq, min_val, raiz.valor) and
            es_bst(raiz.der, raiz.valor, max_val))

def es_equilibrado(raiz):
    """Verifica si el árbol está balanceado (diferencia de alturas <=1)"""
    if raiz is None:
        return True
    def altura_balance(nodo):
        if nodo is None:
            return 0
        izq_h = altura_balance(nodo.izq)
        der_h = altura_balance(nodo.der)
        if izq_h == -1 or der_h == -1 or abs(izq_h - der_h) > 1:
            return -1
        return 1 + max(izq_h, der_h)
    return altura_balance(raiz) != -1

def misma_forma(raiz1, raiz2):
    """Verifica si tienen la misma estructura"""
    if raiz1 is None and raiz2 is None:
        return True
    if raiz1 is None or raiz2 is None:
        return False
    return misma_forma(raiz1.izq, raiz2.izq) and misma_forma(raiz1.der, raiz2.der)

def arboles_equivalentes(raiz1, raiz2):
    """Misma estructura y mismos valores"""
    if raiz1 is None and raiz2 is None:
        return True
    if raiz1 is None or raiz2 is None:
        return False
    return (raiz1.valor == raiz2.valor and
            arboles_equivalentes(raiz1.izq, raiz2.izq) and
            arboles_equivalentes(raiz1.der, raiz2.der))

def obtener_tipo_arbol(raiz):
    """Determina todos los tipos que aplican al árbol"""
    tipos = []
    
    if raiz is None:
        return ["🌿 Árbol vacío"]
    
    if es_completo(raiz):
        tipos.append("✅ Completo")
    
    if es_lleno(raiz):
        tipos.append("🌟 Lleno")
    
    if es_degenerado(raiz):
        tipos.append("📉 Degenerado")
    
    if es_bst(raiz):
        tipos.append("🔍 BST (Búsqueda)")
    
    if es_equilibrado(raiz):
        tipos.append("⚖️ Equilibrado")
    
    # Si no tiene ninguna clasificación especial
    if not tipos:
        tipos.append("📝 Árbol binario estándar")
    
    return tipos

# ------------------------------------------------------------
# Generadores de árboles de ejemplo
# ------------------------------------------------------------
def arbol_vacio():
    return None

def generar_arbol_distinto():
    """Genera un árbol con forma sesgada aleatoria"""
    raiz = Nodo(random.randint(1, 100))
    if random.choice([True, False]):
        raiz.izq = Nodo(random.randint(1, 100))
        raiz.izq.izq = Nodo(random.randint(1, 100))
        if random.choice([True, False]):
            raiz.izq.der = Nodo(random.randint(1, 100))
    else:
        raiz.der = Nodo(random.randint(1, 100))
        raiz.der.der = Nodo(random.randint(1, 100))
        if random.choice([True, False]):
            raiz.der.izq = Nodo(random.randint(1, 100))
    return raiz

def generar_arbol_completo():
    """Genera un árbol COMPLETO válido"""
    total_nodos = random.randint(3, 15)
    
    def construir_completo(indice, nodos):
        if indice >= len(nodos):
            return None
        raiz = Nodo(nodos[indice])
        raiz.izq = construir_completo(2 * indice + 1, nodos)
        raiz.der = construir_completo(2 * indice + 2, nodos)
        return raiz
    
    valores = [random.randint(1, 99) for _ in range(total_nodos)]
    return construir_completo(0, valores)

def generar_arbol_lleno():
    """Genera un árbol LLENO válido"""
    altura_arbol = random.randint(2, 3)
    total_nodos = 2 ** (altura_arbol + 1) - 1
    valores = [random.randint(1, 99) for _ in range(total_nodos)]
    
    def construir_lleno(indice, altura_actual, altura_max):
        if altura_actual > altura_max:
            return None
        if indice >= len(valores):
            return None
        nodo = Nodo(valores[indice])
        if altura_actual < altura_max:
            nodo.izq = construir_lleno(2 * indice + 1, altura_actual + 1, altura_max)
            nodo.der = construir_lleno(2 * indice + 2, altura_actual + 1, altura_max)
        return nodo
    
    return construir_lleno(0, 0, altura_arbol)

def generar_arbol_degenerado():
    """Genera un árbol degenerado"""
    longitud = random.randint(3, 7)
    raiz = Nodo(random.randint(1, 100))
    actual = raiz
    direccion = random.choice(['izq', 'der'])
    for i in range(longitud - 1):
        nuevo = Nodo(random.randint(1, 100))
        if direccion == 'izq':
            actual.izq = nuevo
        else:
            actual.der = nuevo
        actual = nuevo
        if random.random() < 0.3 and i < longitud - 2:
            direccion = 'der' if direccion == 'izq' else 'izq'
    return raiz

def generar_arbol_busqueda():
    """Genera un BST válido"""
    valores = sorted(random.sample(range(1, 200), random.randint(5, 10)))
    
    def construir_bst(valores_lista):
        if not valores_lista:
            return None
        idx = random.randint(0, len(valores_lista) - 1)
        raiz = Nodo(valores_lista[idx])
        raiz.izq = construir_bst(valores_lista[:idx])
        raiz.der = construir_bst(valores_lista[idx+1:])
        return raiz
    
    return construir_bst(valores)

def generar_arbol_equilibrado():
    """Genera un árbol equilibrado"""
    num_nodos = random.randint(5, 12)
    valores = random.sample(range(1, 200), num_nodos)
    
    def construir_balanceado(arr):
        if not arr:
            return None
        medio = len(arr) // 2
        raiz = Nodo(arr[medio])
        raiz.izq = construir_balanceado(arr[:medio])
        raiz.der = construir_balanceado(arr[medio+1:])
        return raiz
    
    valores_ordenados = sorted(valores)
    return construir_balanceado(valores_ordenados)

# ------------------------------------------------------------
# Clase para el Canvas con scroll y dibujo de árbol
# ------------------------------------------------------------
class TreeVisualizer:
    def __init__(self, canvas_frame, width=800, height=550):
        self.canvas = tk.Canvas(canvas_frame, bg="#FDF5E6", width=width, height=height, highlightthickness=0)
        v_scroll = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        h_scroll = ttk.Scrollbar(canvas_frame, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        self.canvas.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")
        
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)
        
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.raiz_actual = None
        self.radio_nodo = 25
        self.espacio_v = 70
        self.nodo_seleccionado = None
        self.id_nodo_map = {}  # Mapa de IDs de canvas a nodos
        
    def on_canvas_configure(self, event):
        if self.raiz_actual is not None:
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def dibujar_arbol(self, raiz):
        self.canvas.delete("all")
        self.id_nodo_map.clear()
        
        if raiz is None:
            self.canvas.create_text(400, 250, text="🌲 Árbol vacío\n\nHaz clic en 'Agregar Nodo Raíz' para comenzar", 
                                    font=("Arial", 16, "italic"), fill="#888", justify="center")
            self.canvas.configure(scrollregion=(0,0,800,550))
            return
        
        profundidad = self.calcular_profundidad(raiz)
        total_hojas = contar_hojas(raiz)
        ancho_necesario = max(800, total_hojas * 70 + 100)
        alto_necesario = max(550, (profundidad + 1) * self.espacio_v + 80)
        
        self.canvas.configure(scrollregion=(-50, 0, ancho_necesario, alto_necesario))
        x_centro = ancho_necesario // 2
        self._dibujar_rec(raiz, x_centro, 50, ancho_necesario // 4, 0)
        
    def _dibujar_rec(self, nodo, x, y, offset_x, nivel):
        if nodo is None:
            return
        
        color_fill = "#FFE4B5"
        if nodo.izq is None and nodo.der is None:
            color_fill = "#C1F0C1"  # hojas verde claro
        
        # Resaltar nodo seleccionado
        outline_color = "#FF6B35" if self.nodo_seleccionado is nodo else "#5D3A1A"
        outline_width = 3 if self.nodo_seleccionado is nodo else 2
        
        oval_id = self.canvas.create_oval(x - self.radio_nodo, y - self.radio_nodo,
                                          x + self.radio_nodo, y + self.radio_nodo,
                                          fill=color_fill, outline=outline_color, width=outline_width)
        text_id = self.canvas.create_text(x, y, text=str(nodo.valor), font=("Helvetica", 12, "bold"), fill="#2C3E2F")
        
        # Guardar referencia del nodo para eventos de clic
        self.id_nodo_map[oval_id] = nodo
        self.id_nodo_map[text_id] = nodo
        
        # Agregar evento de clic
        self.canvas.tag_bind(oval_id, "<Button-1>", lambda e, n=nodo: self.seleccionar_nodo(n))
        self.canvas.tag_bind(text_id, "<Button-1>", lambda e, n=nodo: self.seleccionar_nodo(n))
        
        # Dibujar hijos
        if nodo.izq:
            x_izq = x - offset_x
            y_izq = y + self.espacio_v
            line_id = self.canvas.create_line(x, y + self.radio_nodo, x_izq, y_izq - self.radio_nodo, width=2, fill="#B87333")
            self._dibujar_rec(nodo.izq, x_izq, y_izq, offset_x // 2, nivel+1)
        if nodo.der:
            x_der = x + offset_x
            y_der = y + self.espacio_v
            line_id = self.canvas.create_line(x, y + self.radio_nodo, x_der, y_der - self.radio_nodo, width=2, fill="#B87333")
            self._dibujar_rec(nodo.der, x_der, y_der, offset_x // 2, nivel+1)
    
    def calcular_profundidad(self, raiz):
        if raiz is None:
            return 0
        return 1 + max(self.calcular_profundidad(raiz.izq), self.calcular_profundidad(raiz.der))
    
    def actualizar(self, raiz):
        self.raiz_actual = raiz
        self.dibujar_arbol(raiz)
    
    def seleccionar_nodo(self, nodo):
        self.nodo_seleccionado = nodo
        self.dibujar_arbol(self.raiz_actual)

# ------------------------------------------------------------
# Editor interactivo de árboles
# ------------------------------------------------------------
class EditorArbol:
    def __init__(self, visualizador, info_callback):
        self.visualizador = visualizador
        self.raiz = None
        self.actualizar_info = info_callback
        
    def agregar_nodo_raiz(self):
        """Agrega la raíz del árbol si está vacío"""
        if self.raiz is not None:
            messagebox.showwarning("Árbol no vacío", "El árbol ya tiene una raíz. Para agregar más nodos, selecciona un nodo padre.")
            return
        
        valor = simpledialog.askinteger("Agregar Raíz", "Ingrese el valor de la raíz:", minvalue=1, maxvalue=999)
        if valor is not None:
            self.raiz = Nodo(valor)
            self.actualizar()
            messagebox.showinfo("Éxito", f"Raíz con valor {valor} agregada correctamente")
    
    def agregar_nodo(self):
        """Agrega un nodo como hijo del nodo seleccionado"""
        if self.raiz is None:
            messagebox.showwarning("Árbol vacío", "Primero agrega la raíz usando 'Agregar Nodo Raíz'")
            return
        
        if self.visualizador.nodo_seleccionado is None:
            messagebox.showwarning("Selección requerida", 
                                   "Primero haz clic en un nodo para seleccionarlo como padre.\n\n"
                                   "Luego vuelve a hacer clic en 'Agregar Nodo'")
            return
        
        padre = self.visualizador.nodo_seleccionado
        valor = simpledialog.askinteger("Agregar Nodo", f"Ingrese el valor para el nuevo nodo (hijo de {padre.valor}):", 
                                        minvalue=1, maxvalue=999)
        if valor is None:
            return
        
        # Crear ventana de selección de dirección
        direccion_ventana = tk.Toplevel()
        direccion_ventana.title("Seleccionar dirección")
        direccion_ventana.geometry("300x150")
        direccion_ventana.transient(self.visualizador.canvas)
        direccion_ventana.grab_set()
        
        tk.Label(direccion_ventana, text=f"Agregar nodo {valor} como hijo de {padre.valor}", 
                 font=("Arial", 10, "bold")).pack(pady=10)
        tk.Label(direccion_ventana, text="¿En qué posición deseas agregarlo?").pack(pady=5)
        
        resultado = [None]
        
        def elegir_izquierdo():
            resultado[0] = 'izq'
            direccion_ventana.destroy()
        
        def elegir_derecho():
            resultado[0] = 'der'
            direccion_ventana.destroy()
        
        btn_frame = tk.Frame(direccion_ventana)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="⬅️ Hijo Izquierdo", command=elegir_izquierdo, 
                 bg="#4A7A5C", fg="white", padx=20, pady=5).pack(side="left", padx=10)
        tk.Button(btn_frame, text="➡️ Hijo Derecho", command=elegir_derecho,
                 bg="#4A7A5C", fg="white", padx=20, pady=5).pack(side="left", padx=10)
        
        self.visualizador.canvas.wait_window(direccion_ventana)
        
        direccion = resultado[0]
        if direccion is None:
            return
        
        # Verificar si ya existe un hijo en esa dirección
        if direccion == 'izq' and padre.izq is not None:
            messagebox.showwarning("Posición ocupada", f"El nodo {padre.valor} ya tiene un hijo izquierdo ({padre.izq.valor})")
            return
        elif direccion == 'der' and padre.der is not None:
            messagebox.showwarning("Posición ocupada", f"El nodo {padre.valor} ya tiene un hijo derecho ({padre.der.valor})")
            return
        
        # Agregar el nodo
        nuevo = Nodo(valor)
        if direccion == 'izq':
            padre.izq = nuevo
        else:
            padre.der = nuevo
        
        self.actualizar()
        messagebox.showinfo("Éxito", f"Nodo {valor} agregado como hijo {direccion} de {padre.valor}")
    
    def eliminar_nodo(self):
        """Elimina el nodo seleccionado"""
        if self.raiz is None:
            messagebox.showwarning("Árbol vacío", "No hay nodos para eliminar")
            return
        
        if self.visualizador.nodo_seleccionado is None:
            messagebox.showwarning("Selección requerida", "Primero haz clic en un nodo para seleccionarlo")
            return
        
        nodo_a_eliminar = self.visualizador.nodo_seleccionado
        
        # Confirmar eliminación
        if not messagebox.askyesno("Confirmar eliminación", 
                                   f"¿Estás seguro de eliminar el nodo {nodo_a_eliminar.valor} y todos sus subárboles?"):
            return
        
        # Buscar el padre del nodo
        padre = self.encontrar_padre(self.raiz, nodo_a_eliminar)
        
        if padre is None:
            # Es la raíz
            self.raiz = None
            self.visualizador.nodo_seleccionado = None
            self.actualizar()
            messagebox.showinfo("Éxito", "Árbol eliminado completamente")
        else:
            # Eliminar referencia del padre
            if padre.izq is nodo_a_eliminar:
                padre.izq = None
            elif padre.der is nodo_a_eliminar:
                padre.der = None
            self.visualizador.nodo_seleccionado = None
            self.actualizar()
            messagebox.showinfo("Éxito", f"Nodo {nodo_a_eliminar.valor} eliminado correctamente")
    
    def encontrar_padre(self, raiz, nodo_buscar):
        """Encuentra el padre de un nodo"""
        if raiz is None or raiz is nodo_buscar:
            return None
        if raiz.izq is nodo_buscar or raiz.der is nodo_buscar:
            return raiz
        padre = self.encontrar_padre(raiz.izq, nodo_buscar)
        if padre:
            return padre
        return self.encontrar_padre(raiz.der, nodo_buscar)
    
    def modificar_valor(self):
        """Modifica el valor del nodo seleccionado"""
        if self.raiz is None:
            messagebox.showwarning("Árbol vacío", "No hay nodos para modificar")
            return
        
        if self.visualizador.nodo_seleccionado is None:
            messagebox.showwarning("Selección requerida", "Primero haz clic en un nodo para seleccionarlo")
            return
        
        nodo = self.visualizador.nodo_seleccionado
        nuevo_valor = simpledialog.askinteger("Modificar Valor", 
                                              f"Valor actual: {nodo.valor}\nIngrese nuevo valor:",
                                              minvalue=1, maxvalue=999)
        if nuevo_valor is not None:
            nodo.valor = nuevo_valor
            self.actualizar()
            messagebox.showinfo("Éxito", f"Valor modificado a {nuevo_valor}")
    
    def cargar_ejemplo(self, generador, nombre):
        """Carga un árbol de ejemplo"""
        self.raiz = generador()
        self.visualizador.nodo_seleccionado = None
        self.actualizar()
        messagebox.showinfo("Ejemplo Cargado", f"Se ha cargado el árbol: {nombre}")
    
    def limpiar_arbol(self):
        """Limpia el árbol actual"""
        if self.raiz is not None:
            if messagebox.askyesno("Limpiar", "¿Eliminar todo el árbol? Se perderán los datos actuales"):
                self.raiz = None
                self.visualizador.nodo_seleccionado = None
                self.actualizar()
    
    def actualizar(self):
        """Actualiza la visualización y la información"""
        self.visualizador.actualizar(self.raiz)
        self.actualizar_info(self.raiz)

# ------------------------------------------------------------
# Ventana principal
# ------------------------------------------------------------
class AplicacionArboles:
    def __init__(self, root):
        self.root = root
        self.root.title("🌳 Creador y Clasificador de Árboles Binarios")
        self.root.geometry("1300x800")
        self.root.configure(bg="#1E2F2F")
        
        # Frame superior
        top_frame = tk.Frame(root, bg="#1E2F2F")
        top_frame.pack(fill="x", pady=(10,5))
        tk.Label(top_frame, text="🌳 CREADOR INTERACTIVO DE ÁRBOLES BINARIOS", 
                 font=("Segoe UI", 16, "bold"), fg="#F7F3E0", bg="#1E2F2F").pack()
        tk.Label(top_frame, text="Crea tu propio árbol | Haz clic en nodos para seleccionarlos | El programa te dirá qué tipo de árbol es", 
                 font=("Segoe UI", 10), fg="#CFE6CF", bg="#1E2F2F").pack()
        
        # Panel principal
        main_panel = tk.Frame(root, bg="#2C423F")
        main_panel.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Frame izquierdo (controles)
        left_frame = tk.Frame(main_panel, bg="#2C423F", width=340)
        left_frame.pack(side="left", fill="y", padx=(0,15))
        left_frame.pack_propagate(False)
        
        # Canvas derecho
        right_frame = tk.Frame(main_panel, bg="#2C423F")
        right_frame.pack(side="right", fill="both", expand=True)
        
        self.visualizador = TreeVisualizer(right_frame, width=900, height=650)
        self.editor = EditorArbol(self.visualizador, self.actualizar_info)
        
        # Área de botones con scroll
        botones_canvas = tk.Canvas(left_frame, bg="#2C423F", highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=botones_canvas.yview)
        scrollable_frame = tk.Frame(botones_canvas, bg="#2C423F")
        
        scrollable_frame.bind("<Configure>", lambda e: botones_canvas.configure(scrollregion=botones_canvas.bbox("all")))
        botones_canvas.create_window((0,0), window=scrollable_frame, anchor="nw")
        botones_canvas.configure(yscrollcommand=scrollbar.set)
        
        botones_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Sección de edición
        tk.Label(scrollable_frame, text="✏️ EDITOR DE ÁRBOL", font=("Arial", 12, "bold"), 
                 bg="#2C423F", fg="#FFD966").pack(pady=(10,5))
        
        btn_agregar_raiz = tk.Button(scrollable_frame, text="🌱 Agregar Nodo Raíz", font=("Consolas", 10),
                                     bg="#4A7A5C", fg="white", activebackground="#6A9C7A",
                                     command=self.editor.agregar_nodo_raiz)
        btn_agregar_raiz.pack(pady=5, padx=10, fill="x")
        
        btn_agregar = tk.Button(scrollable_frame, text="➕ Agregar Nodo (hijo del seleccionado)", font=("Consolas", 10),
                                bg="#568EA6", fg="white", activebackground="#78AEC6",
                                command=self.editor.agregar_nodo)
        btn_agregar.pack(pady=5, padx=10, fill="x")
        
        btn_modificar = tk.Button(scrollable_frame, text="✏️ Modificar Valor del Nodo", font=("Consolas", 10),
                                  bg="#4A7A5C", fg="white", activebackground="#6A9C7A",
                                  command=self.editor.modificar_valor)
        btn_modificar.pack(pady=5, padx=10, fill="x")
        
        btn_eliminar = tk.Button(scrollable_frame, text="❌ Eliminar Nodo Seleccionado", font=("Consolas", 10),
                                 bg="#A5554A", fg="white", activebackground="#C5756A",
                                 command=self.editor.eliminar_nodo)
        btn_eliminar.pack(pady=5, padx=10, fill="x")
        
        btn_limpiar = tk.Button(scrollable_frame, text="🗑️ Limpiar Todo", font=("Consolas", 10),
                                bg="#8B6B4D", fg="white", activebackground="#AB8B6D",
                                command=self.editor.limpiar_arbol)
        btn_limpiar.pack(pady=5, padx=10, fill="x")
        
        # Separador
        tk.Frame(scrollable_frame, height=2, bg="#5D7A6E").pack(fill="x", pady=10)
        
        # Sección de ejemplos
        tk.Label(scrollable_frame, text="📚 ÁRBOLES DE EJEMPLO", font=("Arial", 12, "bold"), 
                 bg="#2C423F", fg="#FFD966").pack(pady=(5,5))
        
        ejemplos = [
            ("✅ Completo", generar_arbol_completo),
            ("🌟 Lleno", generar_arbol_lleno),
            ("📉 Degenerado", generar_arbol_degenerado),
            ("🔍 BST", generar_arbol_busqueda),
            ("⚖️ Equilibrado", generar_arbol_equilibrado),
            ("🔀 Distinto (forma única)", generar_arbol_distinto),
            ("🌿 Vacío", arbol_vacio)
        ]
        
        for nombre, generador in ejemplos:
            btn = tk.Button(scrollable_frame, text=nombre, font=("Consolas", 9),
                           bg="#3D5A5C", fg="white", activebackground="#E9C46A",
                           command=lambda g=generador, n=nombre: self.editor.cargar_ejemplo(g, n))
            btn.pack(pady=3, padx=10, fill="x")
        
        # Separador
        tk.Frame(scrollable_frame, height=2, bg="#5D7A6E").pack(fill="x", pady=10)
        
        # Área de información del árbol
        tk.Label(scrollable_frame, text="📊 CLASIFICACIÓN DEL ÁRBOL", font=("Arial", 11, "bold"), 
                 bg="#2C423F", fg="#FFD966").pack(pady=(5,5))
        
        self.info_text = tk.Text(scrollable_frame, height=16, width=34, bg="#FEFAE0", fg="#2D3E2B", 
                                  font=("Courier", 10), wrap="word", relief="solid", bd=1)
        self.info_text.pack(pady=5, padx=10, fill="both")
        self.info_text.config(state="disabled")
        
        # Instrucciones
        tk.Label(scrollable_frame, text="💡 INSTRUCCIONES", font=("Arial", 10, "bold"), 
                 bg="#2C423F", fg="#FFD966").pack(pady=(10,2))
        instrucciones = """1. Haz clic en 'Agregar Nodo Raíz' para comenzar
2. Selecciona un nodo haciendo clic en él
3. Usa 'Agregar Nodo' para agregar hijos
   - Elige si será izquierdo o derecho
4. Los nodos hoja se muestran en VERDE
5. El programa clasifica automáticamente
   el árbol según su estructura"""
        
        tk.Label(scrollable_frame, text=instrucciones, font=("Arial", 8), 
                 bg="#2C423F", fg="#CFE6CF", justify="left").pack(pady=(0,10), padx=10)
        
        # Inicializar con árbol vacío
        self.editor.actualizar()
    
    def actualizar_info(self, raiz):
        """Actualiza la información y clasificación del árbol"""
        tipos = obtener_tipo_arbol(raiz)
        
        total_nodos = contar_nodos(raiz)
        total_hojas = contar_hojas(raiz)
        alt = altura(raiz)
        
        # Crear texto de tipos
        tipos_texto = "\n".join([f"  {t}" for t in tipos])
        
        info = f"""📊 ESTADÍSTICAS
━━━━━━━━━━━━━━━━━━━━━
📦 Total Nodos: {total_nodos}
🍃 Total Hojas: {total_hojas}
📏 Altura: {alt}

🏷️ CLASIFICACIÓN:
{tipos_texto}

━━━━━━━━━━━━━━━━━━━━━
💡 Los tipos NO son mutuamente
excluyentes. Un árbol puede
pertenecer a varias categorías.
"""
        
        # Si hay un nodo seleccionado, mostrar información adicional
        if self.visualizador.nodo_seleccionado:
            nodo = self.visualizador.nodo_seleccionado
            info += f"\n✨ NODO SELECCIONADO:\n   Valor: {nodo.valor}"
            if nodo.izq:
                info += f"\n   Hijo izquierdo: {nodo.izq.valor}"
            else:
                info += f"\n   Hijo izquierdo: (vacío)"
            if nodo.der:
                info += f"\n   Hijo derecho: {nodo.der.valor}"
            else:
                info += f"\n   Hijo derecho: (vacío)"
        
        # Si es BST, mostrar propiedad
        if raiz and es_bst(raiz):
            info += "\n\n🔍 ¡Es un Árbol Binario de Búsqueda!\n   (izq < raíz < der)"
        
        # Si es equilibrado
        if raiz and es_equilibrado(raiz):
            info += "\n⚖️ Árbol equilibrado: diferencia\n   de altura entre subárboles ≤ 1"
        
        self.info_text.config(state="normal")
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, info)
        self.info_text.config(state="disabled")

# ------------------------------------------------------------
# Ejecutar aplicación
# ------------------------------------------------------------
if __name__ == "__main__":
    random.seed()
    root = tk.Tk()
    app = AplicacionArboles(root)
    root.mainloop()