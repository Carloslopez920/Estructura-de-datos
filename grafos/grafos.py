import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog, scrolledtext
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import json
import os
from datetime import datetime

class TDA_Grafo:
    """Implementación del TDA Grafo usando NetworkX"""
    
    def __init__(self, dirigido=False):
        if dirigido:
            self.grafo = nx.DiGraph()
        else:
            self.grafo = nx.Graph()
        self.dirigido = dirigido
        self.contador_vertices = 0
        self.contador_aristas = 0
        
    def numVertices(self):
        return self.grafo.number_of_nodes()
    
    def numAristas(self):
        return self.grafo.number_of_edges()
    
    def vertices(self):
        return list(self.grafo.nodes())
    
    def aristas(self):
        return list(self.grafo.edges())
    
    def grado(self, v):
        return self.grafo.degree(v)
    
    def verticesAdyacentes(self, v):
        return list(self.grafo.neighbors(v))
    
    def aristasIncidentes(self, v):
        return list(self.grafo.edges(v))
    
    def verticesFinales(self, e):
        return list(e)
    
    def opuesto(self, v, e):
        if v == e[0]:
            return e[1]
        elif v == e[1]:
            return e[0]
        return None
    
    def esAdyacente(self, v, w):
        return self.grafo.has_edge(v, w)
    
    def aristasDirigidas(self):
        if self.dirigido:
            return list(self.grafo.edges())
        return []
    
    def aristasNoDirigidas(self):
        if not self.dirigido:
            return list(self.grafo.edges())
        return []
    
    def gradoEntrada(self, v):
        if self.dirigido:
            return self.grafo.in_degree(v)
        return self.grafo.degree(v)
    
    def gradoSalida(self, v):
        if self.dirigido:
            return self.grafo.out_degree(v)
        return self.grafo.degree(v)
    
    def aristasIncidentesEntrada(self, v):
        if self.dirigido:
            return list(self.grafo.in_edges(v))
        return list(self.grafo.edges(v))
    
    def aristasIncidentesSalida(self, v):
        if self.dirigido:
            return list(self.grafo.out_edges(v))
        return list(self.grafo.edges(v))
    
    def verticesAdyacentesEntrada(self, v):
        if self.dirigido:
            return [u for u, _ in self.grafo.in_edges(v)]
        return list(self.grafo.neighbors(v))
    
    def verticesAdyacentesSalida(self, v):
        if self.dirigido:
            return [w for _, w in self.grafo.out_edges(v)]
        return list(self.grafo.neighbors(v))
    
    def destino(self, e):
        if self.dirigido:
            return e[1]
        return e[1] if len(e) > 1 else None
    
    def origen(self, e):
        if self.dirigido:
            return e[0]
        return e[0] if len(e) > 0 else None
    
    def esDirigida(self, e):
        return self.dirigido
    
    def insertaArista(self, v, w, o=None):
        if not self.dirigido:
            self.grafo.add_edge(v, w, weight=o if o else 1)
            self.contador_aristas += 1
            return (v, w)
        return None
    
    def insertaAristaDirigida(self, v, w, o=None):
        if self.dirigido:
            self.grafo.add_edge(v, w, weight=o if o else 1)
            self.contador_aristas += 1
            return (v, w)
        return None
    
    def insertaVertice(self, o=None):
        self.contador_vertices += 1
        nombre = o if o else f"v{self.contador_vertices}"
        self.grafo.add_node(nombre)
        return nombre
    
    def eliminaVertice(self, v):
        if v in self.grafo.nodes():
            self.grafo.remove_node(v)
            return True
        return False
    
    def eliminaArista(self, e):
        if e in self.grafo.edges():
            self.grafo.remove_edge(e[0], e[1])
            return True
        return False
    
    def convierteNoDirigida(self, e):
        if self.dirigido and e in self.grafo.edges():
            # Convertir a no dirigido requiere recrear el grafo
            return False
        return False
    
    def invierteDireccion(self, e):
        if self.dirigido and e in self.grafo.edges():
            u, v = e
            peso = self.grafo[u][v].get('weight', 1)
            self.grafo.remove_edge(u, v)
            self.grafo.add_edge(v, u, weight=peso)
            return True
        return False
    
    def asignaDireccionDesde(self, e, v):
        if not self.dirigido and e in self.grafo.edges():
            u, w = e
            if v == u:
                return True
            elif v == w:
                peso = self.grafo[u][w].get('weight', 1)
                self.grafo.remove_edge(u, w)
                self.grafo.add_edge(w, u, weight=peso)
                return True
        return False
    
    def asignaDireccionA(self, e, v):
        if not self.dirigido and e in self.grafo.edges():
            u, w = e
            if v == w:
                return True
            elif v == u:
                peso = self.grafo[u][w].get('weight', 1)
                self.grafo.remove_edge(u, w)
                self.grafo.add_edge(w, u, weight=peso)
                return True
        return False
    
    def tamano(self):
        return self.numVertices() + self.numAristas()
    
    def estaVacio(self):
        return self.numVertices() == 0
    
    def elementos(self):
        return list(self.grafo.nodes()) + list(self.grafo.edges())
    
    def posiciones(self):
        return list(self.grafo.nodes())
    
    def reemplazar(self, p, r):
        if p in self.grafo.nodes():
            nx.relabel_nodes(self.grafo, {p: r}, copy=False)
            return True
        return False
    
    def intercambiar(self, p, q):
        if p in self.grafo.nodes() and q in self.grafo.nodes():
            mapping = {p: 'temp', q: p, 'temp': q}
            nx.relabel_nodes(self.grafo, mapping, copy=False)
            return True
        return False
    
    def to_dict(self):
        """Convierte el grafo a diccionario para guardar"""
        return {
            'dirigido': self.dirigido,
            'vertices': list(self.grafo.nodes()),
            'aristas': [(u, v, self.grafo[u][v].get('weight', 1)) for u, v in self.grafo.edges()]
        }
    
    def from_dict(self, data):
        """Carga el grafo desde un diccionario"""
        self.__init__(dirigido=data['dirigido'])
        for vertice in data['vertices']:
            self.insertaVertice(vertice)
        for u, v, peso in data['aristas']:
            if self.dirigido:
                self.insertaAristaDirigida(u, v, peso)
            else:
                self.insertaArista(u, v, peso)


class GrafoVisualApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TDA Grafo - Visualizador Completo con Entrada de Datos")
        self.root.geometry("1400x900")
        
        # Grafo inicial (no dirigido por defecto)
        self.grafo = TDA_Grafo(dirigido=False)
        
        # Configurar la interfaz
        self.setup_ui()
        
        # Dibujar el grafo inicial
        self.dibujar_grafo()
    
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Panel izquierdo - Operaciones
        panel_ops = ttk.LabelFrame(main_frame, text="Operaciones del Grafo", width=350)
        panel_ops.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        panel_ops.pack_propagate(False)
        
        # Panel derecho - Visualización
        panel_vis = ttk.LabelFrame(main_frame, text="Visualización del Grafo")
        panel_vis.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Canvas para matplotlib
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=panel_vis)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Crear pestañas para organizar operaciones
        self.notebook = ttk.Notebook(panel_ops)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Pestaña 0: Entrada de Datos
        tab_entrada = ttk.Frame(self.notebook)
        self.notebook.add(tab_entrada, text="📥 Entrada Datos")
        self.crear_tab_entrada_datos(tab_entrada)
        
        # Pestaña 1: Información básica
        tab_info = ttk.Frame(self.notebook)
        self.notebook.add(tab_info, text="ℹ️ Información")
        self.crear_tab_informacion(tab_info)
        
        # Pestaña 2: Operaciones básicas
        tab_basicas = ttk.Frame(self.notebook)
        self.notebook.add(tab_basicas, text="🔷 Básicas")
        self.crear_tab_operaciones_basicas(tab_basicas)
        
        # Pestaña 3: Operaciones con aristas
        tab_aristas = ttk.Frame(self.notebook)
        self.notebook.add(tab_aristas, text="🔗 Aristas")
        self.crear_tab_operaciones_aristas(tab_aristas)
        
        # Pestaña 4: Operaciones dirigidas
        tab_dirigidas = ttk.Frame(self.notebook)
        self.notebook.add(tab_dirigidas, text="➡️ Dirigidas")
        self.crear_tab_operaciones_dirigidas(tab_dirigidas)
        
        # Pestaña 5: Operaciones posicionales
        tab_pos = ttk.Frame(self.notebook)
        self.notebook.add(tab_pos, text="📍 Posiciones")
        self.crear_tab_operaciones_posicionales(tab_pos)
        
        # Pestaña 6: Actualización
        tab_actualizar = ttk.Frame(self.notebook)
        self.notebook.add(tab_actualizar, text="🔄 Actualizar")
        self.crear_tab_operaciones_actualizar(tab_actualizar)
        
        # Panel inferior para resultados
        panel_resultados = ttk.LabelFrame(self.root, text="Resultados / Consola")
        panel_resultados.pack(fill=tk.X, padx=10, pady=5)
        
        self.text_resultados = scrolledtext.ScrolledText(panel_resultados, height=8, width=100)
        self.text_resultados.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configurar colores para la consola
        self.text_resultados.tag_config("info", foreground="blue")
        self.text_resultados.tag_config("success", foreground="green")
        self.text_resultados.tag_config("error", foreground="red")
        self.text_resultados.tag_config("warning", foreground="orange")
        
        # Frame para controles globales
        frame_controles = ttk.Frame(panel_ops)
        frame_controles.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(frame_controles, text="Tipo de grafo:").pack(side=tk.LEFT, padx=5)
        self.tipo_var = tk.StringVar(value="No dirigido")
        tipo_combo = ttk.Combobox(frame_controles, textvariable=self.tipo_var, 
                                   values=["No dirigido", "Dirigido"], 
                                   state="readonly", width=15)
        tipo_combo.pack(side=tk.LEFT, padx=5)
        tipo_combo.bind("<<ComboboxSelected>>", self.cambiar_tipo_grafo)
        
        ttk.Button(frame_controles, text="🔄 Refrescar", 
                  command=self.dibujar_grafo).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_controles, text="🗑️ Limpiar consola", 
                  command=self.limpiar_consola).pack(side=tk.LEFT, padx=5)
    
    def crear_tab_entrada_datos(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sección para creación manual
        frame_manual = ttk.LabelFrame(frame, text="Creación Manual")
        frame_manual.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(frame_manual, text="➕ Crear grafo vacío", 
                  command=self.crear_grafo_vacio).pack(pady=5)
        
        ttk.Button(frame_manual, text="📝 Crear grafo con wizard", 
                  command=self.wizard_crear_grafo).pack(pady=5)
        
        # Sección para carga de archivos
        frame_archivo = ttk.LabelFrame(frame, text="Cargar desde Archivo")
        frame_archivo.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(frame_archivo, text="📂 Cargar desde JSON", 
                  command=self.cargar_desde_json).pack(pady=5)
        
        ttk.Button(frame_archivo, text="📄 Cargar desde archivo de texto", 
                  command=self.cargar_desde_texto).pack(pady=5)
        
        # Sección para ejemplos
        frame_ejemplos = ttk.LabelFrame(frame, text="Ejemplos Predefinidos")
        frame_ejemplos.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(frame_ejemplos, text="🌟 Grafo simple (3 vértices)", 
                  command=self.ejemplo_grafo_simple).pack(pady=5)
        
        ttk.Button(frame_ejemplos, text="🔺 Grafo completo K4", 
                  command=self.ejemplo_grafo_completo).pack(pady=5)
        
        ttk.Button(frame_ejemplos, text="🔄 Grafo cíclico C5", 
                  command=self.ejemplo_grafo_ciclico).pack(pady=5)
        
        ttk.Button(frame_ejemplos, text="🌲 Árbol binario", 
                  command=self.ejemplo_arbol_binario).pack(pady=5)
        
        # Sección para exportar
        frame_exportar = ttk.LabelFrame(frame, text="Exportar")
        frame_exportar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(frame_exportar, text="💾 Guardar como JSON", 
                  command=self.guardar_como_json).pack(pady=5)
        
        ttk.Button(frame_exportar, text="📝 Exportar a texto", 
                  command=self.exportar_a_texto).pack(pady=5)
    
    def crear_tab_informacion(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Button(frame, text="📊 Mostrar Información Completa", 
                  command=self.mostrar_informacion_completa).pack(pady=5)
        ttk.Button(frame, text="📋 Listar Vértices", 
                  command=self.listar_vertices).pack(pady=5)
        ttk.Button(frame, text="🔗 Listar Aristas", 
                  command=self.listar_aristas).pack(pady=5)
        ttk.Button(frame, text="❓ ¿Está vacío?", 
                  command=self.mostrar_esta_vacio).pack(pady=5)
        ttk.Button(frame, text="📏 Tamaño total", 
                  command=self.mostrar_tamano).pack(pady=5)
        ttk.Button(frame, text="📈 Matriz de adyacencia", 
                  command=self.mostrar_matriz_adyacencia).pack(pady=5)
    
    def crear_tab_operaciones_basicas(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Button(frame, text="➕ Insertar Vértice", 
                  command=self.insertar_vertice).pack(pady=5)
        ttk.Button(frame, text="➖ Eliminar Vértice", 
                  command=self.eliminar_vertice).pack(pady=5)
        ttk.Button(frame, text="📊 Grado de un vértice", 
                  command=self.mostrar_grado).pack(pady=5)
        ttk.Button(frame, text="👥 Vértices adyacentes", 
                  command=self.mostrar_adyacentes).pack(pady=5)
        ttk.Button(frame, text="🔍 ¿Son adyacentes?", 
                  command=self.verificar_adyacencia).pack(pady=5)
    
    def crear_tab_operaciones_aristas(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Button(frame, text="➕ Insertar Arista", 
                  command=self.insertar_arista).pack(pady=5)
        ttk.Button(frame, text="➖ Eliminar Arista", 
                  command=self.eliminar_arista).pack(pady=5)
        ttk.Button(frame, text="📌 Aristas incidentes", 
                  command=self.mostrar_aristas_incidentes).pack(pady=5)
        ttk.Button(frame, text="🎯 Vértices finales", 
                  command=self.mostrar_vertices_finales).pack(pady=5)
        ttk.Button(frame, text="🔄 Vértice opuesto", 
                  command=self.mostrar_opuesto).pack(pady=5)
    
    def crear_tab_operaciones_dirigidas(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Button(frame, text="➡️ Mostrar aristas dirigidas", 
                  command=self.mostrar_aristas_dirigidas).pack(pady=5)
        ttk.Button(frame, text="🔀 Mostrar aristas no dirigidas", 
                  command=self.mostrar_aristas_nodirigidas).pack(pady=5)
        ttk.Button(frame, text="📥 Grado de entrada", 
                  command=self.mostrar_grado_entrada).pack(pady=5)
        ttk.Button(frame, text="📤 Grado de salida", 
                  command=self.mostrar_grado_salida).pack(pady=5)
        ttk.Button(frame, text="⬅️ Aristas incidentes entrada", 
                  command=self.mostrar_aristas_entrada).pack(pady=5)
        ttk.Button(frame, text="➡️ Aristas incidentes salida", 
                  command=self.mostrar_aristas_salida).pack(pady=5)
        ttk.Button(frame, text="📍 Origen de arista", 
                  command=self.mostrar_origen).pack(pady=5)
        ttk.Button(frame, text="🎯 Destino de arista", 
                  command=self.mostrar_destino).pack(pady=5)
    
    def crear_tab_operaciones_posicionales(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Button(frame, text="📦 Listar elementos", 
                  command=self.listar_elementos).pack(pady=5)
        ttk.Button(frame, text="📍 Listar posiciones", 
                  command=self.listar_posiciones).pack(pady=5)
        ttk.Button(frame, text="✏️ Reemplazar vértice", 
                  command=self.reemplazar_vertice).pack(pady=5)
        ttk.Button(frame, text="🔄 Intercambiar vértices", 
                  command=self.intercambiar_vertices).pack(pady=5)
    
    def crear_tab_operaciones_actualizar(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Button(frame, text="🔄 Convertir a no dirigida", 
                  command=self.convertir_no_dirigida).pack(pady=5)
        ttk.Button(frame, text="🔁 Invertir dirección", 
                  command=self.invertir_direccion).pack(pady=5)
        ttk.Button(frame, text="⬅️ Asignar dirección desde", 
                  command=self.asignar_desde).pack(pady=5)
        ttk.Button(frame, text="➡️ Asignar dirección hacia", 
                  command=self.asignar_hacia).pack(pady=5)
    
    def escribir_consola(self, mensaje, tipo="info"):
        """Escribe mensajes en la consola con formato"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.text_resultados.insert(tk.END, f"[{timestamp}] ", "info")
        self.text_resultados.insert(tk.END, f"{mensaje}\n", tipo)
        self.text_resultados.see(tk.END)
    
    def limpiar_consola(self):
        self.text_resultados.delete(1.0, tk.END)
        self.escribir_consola("Consola limpiada", "info")
    
    def mostrar_informacion_completa(self):
        info = f"""=== INFORMACIÓN COMPLETA DEL GRAFO ===
Tipo: {'Dirigido' if self.grafo.dirigido else 'No Dirigido'}
Número de vértices: {self.grafo.numVertices()}
Número de aristas: {self.grafo.numAristas()}
Tamaño total: {self.grafo.tamano()}
¿Está vacío?: {'Sí' if self.grafo.estaVacio() else 'No'}

Vértices: {', '.join(map(str, self.grafo.vertices())) if self.grafo.vertices() else 'Ninguno'}
Aristas: {', '.join([f'{u}→{v}' if self.grafo.dirigido else f'{u}-{v}' for u, v in self.grafo.aristas()]) if self.grafo.aristas() else 'Ninguna'}"""
        
        self.escribir_consola(info, "info")
        messagebox.showinfo("Información", info)
    
    def mostrar_matriz_adyacencia(self):
        if self.grafo.numVertices() == 0:
            self.escribir_consola("No hay vértices para mostrar matriz", "warning")
            return
        
        vertices = sorted(self.grafo.vertices())
        n = len(vertices)
        
        # Crear matriz
        matriz = [[0] * n for _ in range(n)]
        idx = {v: i for i, v in enumerate(vertices)}
        
        for u, v in self.grafo.aristas():
            matriz[idx[u]][idx[v]] = 1
            if not self.grafo.dirigido:
                matriz[idx[v]][idx[u]] = 1
        
        # Formatear matriz para mostrar
        resultado = "Matriz de Adyacencia:\n"
        resultado += "    " + "  ".join(vertices) + "\n"
        for i, v in enumerate(vertices):
            resultado += f"{v}: " + "  ".join(map(str, matriz[i])) + "\n"
        
        self.escribir_consola(resultado, "info")
        messagebox.showinfo("Matriz de Adyacencia", resultado)
    
    def crear_grafo_vacio(self):
        tipo = self.tipo_var.get()
        dirigido = (tipo == "Dirigido")
        self.grafo = TDA_Grafo(dirigido=dirigido)
        self.dibujar_grafo()
        self.escribir_consola(f"Grafo {tipo} vacío creado", "success")
        messagebox.showinfo("Éxito", f"Grafo {tipo} vacío creado")
    
    def wizard_crear_grafo(self):
        # Ventana de wizard
        wizard = tk.Toplevel(self.root)
        wizard.title("Wizard de Creación de Grafo")
        wizard.geometry("500x600")
        
        # Paso 1: Número de vértices
        ttk.Label(wizard, text="Paso 1: Número de vértices", font=("Arial", 12, "bold")).pack(pady=10)
        
        frame_vertices = ttk.Frame(wizard)
        frame_vertices.pack(pady=10)
        
        ttk.Label(frame_vertices, text="Número de vértices:").pack(side=tk.LEFT)
        num_vertices_var = tk.StringVar(value="3")
        num_vertices_spin = ttk.Spinbox(frame_vertices, from_=1, to=20, textvariable=num_vertices_var, width=5)
        num_vertices_spin.pack(side=tk.LEFT, padx=5)
        
        # Entrada de nombres de vértices
        frame_nombres = ttk.Frame(wizard)
        frame_nombres.pack(pady=10, fill=tk.BOTH, expand=True)
        
        ttk.Label(frame_nombres, text="Nombres de vértices:").pack()
        
        text_nombres = tk.Text(frame_nombres, height=5, width=40)
        text_nombres.pack(pady=5)
        text_nombres.insert(1.0, "A, B, C")
        
        # Paso 2: Aristas
        ttk.Label(wizard, text="Paso 2: Aristas (formato: A-B, B-C, ...)", font=("Arial", 12, "bold")).pack(pady=10)
        
        text_aristas = tk.Text(wizard, height=8, width=40)
        text_aristas.pack(pady=5)
        text_aristas.insert(1.0, "A-B\nA-C\nB-C")
        
        def crear_grafo_wizard():
            try:
                # Crear nuevo grafo
                tipo = self.tipo_var.get()
                dirigido = (tipo == "Dirigido")
                nuevo_grafo = TDA_Grafo(dirigido=dirigido)
                
                # Obtener vértices
                nombres_texto = text_nombres.get(1.0, tk.END).strip()
                vertices = [v.strip() for v in nombres_texto.replace(",", " ").split() if v.strip()]
                
                if not vertices:
                    num = int(num_vertices_var.get())
                    vertices = [f"v{i+1}" for i in range(num)]
                
                # Insertar vértices
                for v in vertices:
                    nuevo_grafo.insertaVertice(v)
                
                # Obtener aristas
                aristas_texto = text_aristas.get(1.0, tk.END).strip()
                lineas = aristas_texto.split('\n')
                
                for linea in lineas:
                    if '-' in linea:
                        partes = linea.split('-')
                        if len(partes) == 2:
                            u, v = partes[0].strip(), partes[1].strip()
                            if u in vertices and v in vertices:
                                if dirigido:
                                    nuevo_grafo.insertaAristaDirigida(u, v)
                                else:
                                    nuevo_grafo.insertaArista(u, v)
                
                self.grafo = nuevo_grafo
                self.dibujar_grafo()
                self.escribir_consola(f"Grafo creado con {len(vertices)} vértices y {self.grafo.numAristas()} aristas", "success")
                messagebox.showinfo("Éxito", "Grafo creado correctamente")
                wizard.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear grafo: {str(e)}")
        
        ttk.Button(wizard, text="Crear Grafo", command=crear_grafo_wizard).pack(pady=20)
    
    def cargar_desde_json(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo JSON",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
        )
        
        if archivo:
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.grafo.from_dict(data)
                self.dibujar_grafo()
                self.tipo_var.set("Dirigido" if data['dirigido'] else "No dirigido")
                self.escribir_consola(f"Grafo cargado desde {archivo}", "success")
                messagebox.showinfo("Éxito", f"Grafo cargado correctamente desde {archivo}")
            except Exception as e:
                self.escribir_consola(f"Error al cargar archivo: {str(e)}", "error")
                messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")
    
    def cargar_desde_texto(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de texto",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if archivo:
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    lineas = f.readlines()
                
                tipo = self.tipo_var.get()
                dirigido = (tipo == "Dirigido")
                nuevo_grafo = TDA_Grafo(dirigido=dirigido)
                
                vertices = []
                aristas = []
                
                for linea in lineas:
                    linea = linea.strip()
                    if not linea or linea.startswith('#'):
                        continue
                    
                    if '-' in linea:
                        aristas.append(linea)
                    else:
                        vertices.append(linea)
                
                # Insertar vértices
                for v in vertices:
                    nuevo_grafo.insertaVertice(v)
                
                # Insertar aristas
                for arista in aristas:
                    if '-' in arista:
                        u, v = arista.split('-')
                        u, v = u.strip(), v.strip()
                        if dirigido:
                            nuevo_grafo.insertaAristaDirigida(u, v)
                        else:
                            nuevo_grafo.insertaArista(u, v)
                
                self.grafo = nuevo_grafo
                self.dibujar_grafo()
                self.escribir_consola(f"Grafo cargado desde {archivo}", "success")
                messagebox.showinfo("Éxito", f"Grafo cargado correctamente desde {archivo}")
                
            except Exception as e:
                self.escribir_consola(f"Error al cargar archivo: {str(e)}", "error")
                messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")
    
    def guardar_como_json(self):
        if self.grafo.estaVacio():
            self.escribir_consola("El grafo está vacío, no se puede guardar", "warning")
            return
        
        archivo = filedialog.asksaveasfilename(
            title="Guardar como JSON",
            defaultextension=".json",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
        )
        
        if archivo:
            try:
                data = self.grafo.to_dict()
                with open(archivo, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                self.escribir_consola(f"Grafo guardado en {archivo}", "success")
                messagebox.showinfo("Éxito", f"Grafo guardado correctamente en {archivo}")
            except Exception as e:
                self.escribir_consola(f"Error al guardar: {str(e)}", "error")
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")
    
    def exportar_a_texto(self):
        if self.grafo.estaVacio():
            self.escribir_consola("El grafo está vacío, no se puede exportar", "warning")
            return
        
        archivo = filedialog.asksaveasfilename(
            title="Exportar a texto",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if archivo:
            try:
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(f"Tipo: {'Dirigido' if self.grafo.dirigido else 'No Dirigido'}\n")
                    f.write(f"Número de vértices: {self.grafo.numVertices()}\n")
                    f.write(f"Número de aristas: {self.grafo.numAristas()}\n\n")
                    
                    f.write("Vértices:\n")
                    for v in self.grafo.vertices():
                        f.write(f"  {v}\n")
                    
                    f.write("\nAristas:\n")
                    for u, v in self.grafo.aristas():
                        if self.grafo.dirigido:
                            f.write(f"  {u} -> {v}\n")
                        else:
                            f.write(f"  {u} - {v}\n")
                
                self.escribir_consola(f"Grafo exportado a {archivo}", "success")
                messagebox.showinfo("Éxito", f"Grafo exportado correctamente a {archivo}")
            except Exception as e:
                self.escribir_consola(f"Error al exportar: {str(e)}", "error")
                messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")
    
    def ejemplo_grafo_simple(self):
        tipo = self.tipo_var.get()
        dirigido = (tipo == "Dirigido")
        self.grafo = TDA_Grafo(dirigido=dirigido)
        
        self.grafo.insertaVertice("A")
        self.grafo.insertaVertice("B")
        self.grafo.insertaVertice("C")
        
        if dirigido:
            self.grafo.insertaAristaDirigida("A", "B")
            self.grafo.insertaAristaDirigida("B", "C")
            self.grafo.insertaAristaDirigida("C", "A")
        else:
            self.grafo.insertaArista("A", "B")
            self.grafo.insertaArista("B", "C")
            self.grafo.insertaArista("A", "C")
        
        self.dibujar_grafo()
        self.escribir_consola("Grafo simple de 3 vértices cargado", "success")
    
    def ejemplo_grafo_completo(self):
        tipo = self.tipo_var.get()
        dirigido = (tipo == "Dirigido")
        self.grafo = TDA_Grafo(dirigido=dirigido)
        
        vertices = ["A", "B", "C", "D"]
        for v in vertices:
            self.grafo.insertaVertice(v)
        
        # Grafo completo K4
        for i in range(len(vertices)):
            for j in range(i+1, len(vertices)):
                if dirigido:
                    self.grafo.insertaAristaDirigida(vertices[i], vertices[j])
                    self.grafo.insertaAristaDirigida(vertices[j], vertices[i])
                else:
                    self.grafo.insertaArista(vertices[i], vertices[j])
        
        self.dibujar_grafo()
        self.escribir_consola("Grafo completo K4 cargado", "success")
    
    def ejemplo_grafo_ciclico(self):
        tipo = self.tipo_var.get()
        dirigido = (tipo == "Dirigido")
        self.grafo = TDA_Grafo(dirigido=dirigido)
        
        vertices = ["v1", "v2", "v3", "v4", "v5"]
        for v in vertices:
            self.grafo.insertaVertice(v)
        
        # Ciclo C5
        for i in range(len(vertices)):
            j = (i + 1) % len(vertices)
            if dirigido:
                self.grafo.insertaAristaDirigida(vertices[i], vertices[j])
            else:
                self.grafo.insertaArista(vertices[i], vertices[j])
        
        self.dibujar_grafo()
        self.escribir_consola("Grafo cíclico C5 cargado", "success")
    
    def ejemplo_arbol_binario(self):
        tipo = self.tipo_var.get()
        dirigido = (tipo == "Dirigido")
        self.grafo = TDA_Grafo(dirigido=dirigido)
        
        # Árbol binario con 7 nodos
        vertices = ["Raíz", "Hijo_Izq", "Hijo_Der", "Nieto_II", "Nieto_ID", "Nieto_DI", "Nieto_DD"]
        for v in vertices:
            self.grafo.insertaVertice(v)
        
        aristas = [
            ("Raíz", "Hijo_Izq"), ("Raíz", "Hijo_Der"),
            ("Hijo_Izq", "Nieto_II"), ("Hijo_Izq", "Nieto_ID"),
            ("Hijo_Der", "Nieto_DI"), ("Hijo_Der", "Nieto_DD")
        ]
        
        for u, v in aristas:
            if dirigido:
                self.grafo.insertaAristaDirigida(u, v)
            else:
                self.grafo.insertaArista(u, v)
        
        self.dibujar_grafo()
        self.escribir_consola("Árbol binario cargado", "success")
    
    def cambiar_tipo_grafo(self, event=None):
        if self.grafo.estaVacio():
            tipo = self.tipo_var.get()
            dirigido = (tipo == "Dirigido")
            self.grafo = TDA_Grafo(dirigido=dirigido)
            self.dibujar_grafo()
            self.escribir_consola(f"Tipo de grafo cambiado a {tipo}", "info")
        else:
            respuesta = messagebox.askyesno("Confirmar", 
                "Cambiar el tipo de grafo eliminará el grafo actual. ¿Continuar?")
            if respuesta:
                tipo = self.tipo_var.get()
                dirigido = (tipo == "Dirigido")
                self.grafo = TDA_Grafo(dirigido=dirigido)
                self.dibujar_grafo()
                self.escribir_consola(f"Tipo de grafo cambiado a {tipo}", "info")
    
    def dibujar_grafo(self):
        self.ax.clear()
        
        G = self.grafo.grafo
        
        if len(G.nodes()) == 0:
            self.ax.text(0.5, 0.5, "Grafo vacío\nUse la pestaña 'Entrada Datos'\npara crear un grafo", 
                        horizontalalignment='center',
                        verticalalignment='center',
                        transform=self.ax.transAxes,
                        fontsize=12,
                        bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.5))
        else:
            pos = nx.spring_layout(G, k=2, iterations=50)
            
            nx.draw_networkx_nodes(G, pos, ax=self.ax, node_color='lightblue', 
                                   node_size=500, node_shape='o')
            
            if self.grafo.dirigido:
                nx.draw_networkx_edges(G, pos, ax=self.ax, edge_color='gray', 
                                       arrows=True, arrowsize=20, arrowstyle='->')
            else:
                nx.draw_networkx_edges(G, pos, ax=self.ax, edge_color='gray')
            
            nx.draw_networkx_labels(G, pos, ax=self.ax, font_size=12, font_weight='bold')
            
            labels = nx.get_edge_attributes(G, 'weight')
            if labels:
                nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=self.ax)
        
        self.ax.set_title(f"Grafo {'Dirigido' if self.grafo.dirigido else 'No Dirigido'}")
        self.ax.axis('off')
        self.canvas.draw()
    
    # Métodos para las operaciones (misma implementación que antes)
    def insertar_vertice(self):
        nombre = simpledialog.askstring("Insertar vértice", 
                                       "Nombre del vértice (dejar vacío para auto):")
        if nombre == "":
            nombre = None
        vertice = self.grafo.insertaVertice(nombre)
        self.dibujar_grafo()
        mensaje = f"Vértice '{vertice}' insertado"
        self.escribir_consola(mensaje, "success")
        messagebox.showinfo("Éxito", mensaje)
    
    def eliminar_vertice(self):
        vertices = self.grafo.vertices()
        if not vertices:
            self.escribir_consola("No hay vértices para eliminar", "warning")
            return
        
        vertice = simpledialog.askstring("Eliminar vértice", 
                                         f"Vértices disponibles: {vertices}\n¿Cuál eliminar?")
        if vertice and vertice in vertices:
            self.grafo.eliminaVertice(vertice)
            self.dibujar_grafo()
            mensaje = f"Vértice '{vertice}' eliminado"
            self.escribir_consola(mensaje, "success")
            messagebox.showinfo("Éxito", mensaje)
    
    def mostrar_grado(self):
        vertices = self.grafo.vertices()
        if not vertices:
            self.escribir_consola("No hay vértices", "warning")
            return
        
        vertice = simpledialog.askstring("Grado", 
                                         f"Vértices: {vertices}\n¿De qué vértice?")
        if vertice and vertice in vertices:
            grado = self.grafo.grado(vertice)
            mensaje = f"Grado de '{vertice}': {grado}"
            self.escribir_consola(mensaje, "info")
            messagebox.showinfo("Grado", mensaje)
    
    def mostrar_adyacentes(self):
        vertices = self.grafo.vertices()
        if not vertices:
            self.escribir_consola("No hay vértices", "warning")
            return
        
        vertice = simpledialog.askstring("Adyacentes", 
                                         f"Vértices: {vertices}\n¿De qué vértice?")
        if vertice and vertice in vertices:
            ady = self.grafo.verticesAdyacentes(vertice)
            if ady:
                mensaje = f"Vértices adyacentes a '{vertice}': {ady}"
            else:
                mensaje = f"'{vertice}' no tiene vértices adyacentes"
            self.escribir_consola(mensaje, "info")
            messagebox.showinfo("Adyacentes", mensaje)
    
    def verificar_adyacencia(self):
        vertices = self.grafo.vertices()
        if len(vertices) < 2:
            self.escribir_consola("Se necesitan al menos 2 vértices", "warning")
            return
        
        v = simpledialog.askstring("Adyacencia", f"Vértices: {vertices}\nPrimer vértice:")
        w = simpledialog.askstring("Adyacencia", "Segundo vértice:")
        
        if v and w and v in vertices and w in vertices:
            es_ady = self.grafo.esAdyacente(v, w)
            mensaje = f"{v} y {w} {'son' if es_ady else 'NO son'} adyacentes"
            self.escribir_consola(mensaje, "info")
            messagebox.showinfo("Resultado", mensaje)
    
    def insertar_arista(self):
        vertices = self.grafo.vertices()
        if len(vertices) < 2:
            self.escribir_consola("Se necesitan al menos 2 vértices", "warning")
            return
        
        u = simpledialog.askstring("Arista", f"Vértices: {vertices}\nVértice origen:")
        v = simpledialog.askstring("Arista", "Vértice destino:")
        
        if u and v and u in vertices and v in vertices:
            if self.grafo.dirigido:
                self.grafo.insertaAristaDirigida(u, v)
            else:
                self.grafo.insertaArista(u, v)
            self.dibujar_grafo()
            flecha = "→" if self.grafo.dirigido else "-"
            mensaje = f"Arista {u} {flecha} {v} insertada"
            self.escribir_consola(mensaje, "success")
            messagebox.showinfo("Éxito", mensaje)
    
    def eliminar_arista(self):
        aristas = self.grafo.aristas()
        if not aristas:
            self.escribir_consola("No hay aristas para eliminar", "warning")
            return
        
        aristas_str = [f"{u}-{v}" for u, v in aristas]
        arista_input = simpledialog.askstring("Eliminar arista", 
                                              f"Aristas: {aristas_str}\nEjemplo: u-v")
        
        if arista_input and '-' in arista_input:
            u, v = arista_input.split('-')
            if (u, v) in aristas or (v, u) in aristas:
                self.grafo.eliminaArista((u, v))
                self.dibujar_grafo()
                mensaje = f"Arista {u}-{v} eliminada"
                self.escribir_consola(mensaje, "success")
                messagebox.showinfo("Éxito", mensaje)
            else:
                self.escribir_consola("Arista no encontrada", "error")
    
    def mostrar_aristas_incidentes(self):
        vertices = self.grafo.vertices()
        if not vertices:
            self.escribir_consola("No hay vértices", "warning")
            return
        
        vertice = simpledialog.askstring("Aristas incidentes", 
                                         f"Vértices: {vertices}\n¿De qué vértice?")
        if vertice and vertice in vertices:
            aristas = self.grafo.aristasIncidentes(vertice)
            if aristas:
                aristas_str = [f"{u}-{v}" for u, v in aristas]
                mensaje = f"Aristas incidentes en '{vertice}': {aristas_str}"
            else:
                mensaje = f"'{vertice}' no tiene aristas incidentes"
            self.escribir_consola(mensaje, "info")
            messagebox.showinfo("Aristas incidentes", mensaje)
    
    def mostrar_vertices_finales(self):
        aristas = self.grafo.aristas()
        if not aristas:
            self.escribir_consola("No hay aristas", "warning")
            return
        
        aristas_str = [f"{u}-{v}" for u, v in aristas]
        arista_input = simpledialog.askstring("Vértices finales", 
                                              f"Aristas: {aristas_str}\nEjemplo: u-v")
        
        if arista_input and '-' in arista_input:
            u, v = arista_input.split('-')
            if (u, v) in aristas or (v, u) in aristas:
                finales = self.grafo.verticesFinales((u, v))
                mensaje = f"Vértices finales de {u}-{v}: {finales[0]} y {finales[1]}"
                self.escribir_consola(mensaje, "info")
                messagebox.showinfo("Vértices finales", mensaje)
    
    def mostrar_opuesto(self):
        vertices = self.grafo.vertices()
        aristas = self.grafo.aristas()
        
        if not vertices or not aristas:
            self.escribir_consola("Se necesitan vértices y aristas", "warning")
            return
        
        vertice = simpledialog.askstring("Vértice opuesto", f"Vértices: {vertices}\nVértice:")
        arista_input = simpledialog.askstring("Vértice opuesto", 
                                              f"Aristas: {[f'{u}-{v}' for u, v in aristas]}\nArista (ej: u-v):")
        
        if vertice and arista_input and '-' in arista_input:
            u, v = arista_input.split('-')
            if (u, v) in aristas or (v, u) in aristas:
                if vertice == u or vertice == v:
                    opuesto = self.grafo.opuesto(vertice, (u, v))
                    mensaje = f"El vértice opuesto a {vertice} en la arista {u}-{v} es: {opuesto}"
                    self.escribir_consola(mensaje, "info")
                    messagebox.showinfo("Vértice opuesto", mensaje)
                else:
                    self.escribir_consola("El vértice no pertenece a la arista", "error")
    
    def mostrar_aristas_dirigidas(self):
        aristas = self.grafo.aristasDirigidas()
        if aristas:
            aristas_str = [f"{u} → {v}" for u, v in aristas]
            mensaje = f"Aristas dirigidas: {', '.join(aristas_str)}"
            self.escribir_consola(mensaje, "info")
            messagebox.showinfo("Aristas dirigidas", mensaje)
        else:
            mensaje = "No hay aristas dirigidas"
            self.escribir_consola(mensaje, "info")
    
    def mostrar_aristas_nodirigidas(self):
        aristas = self.grafo.aristasNoDirigidas()
        if aristas:
            aristas_str = [f"{u} - {v}" for u, v in aristas]
            mensaje = f"Aristas no dirigidas: {', '.join(aristas_str)}"
            self.escribir_consola(mensaje, "info")
            messagebox.showinfo("Aristas no dirigidas", mensaje)
        else:
            mensaje = "No hay aristas no dirigidas"
            self.escribir_consola(mensaje, "info")
    
    def mostrar_grado_entrada(self):
        vertices = self.grafo.vertices()
        if not vertices:
            self.escribir_consola("No hay vértices", "warning")
            return
        
        vertice = simpledialog.askstring("Grado de entrada", 
                                         f"Vértices: {vertices}\n¿De qué vértice?")
        if vertice and vertice in vertices:
            grado = self.grafo.gradoEntrada(vertice)
            mensaje = f"Grado de entrada de '{vertice}': {grado}"
            self.escribir_consola(mensaje, "info")
            messagebox.showinfo("Grado de entrada", mensaje)
    
    def mostrar_grado_salida(self):
        vertices = self.grafo.vertices()
        if not vertices:
            self.escribir_consola("No hay vértices", "warning")
            return
        
        vertice = simpledialog.askstring("Grado de salida", 
                                         f"Vértices: {vertices}\n¿De qué vértice?")
        if vertice and vertice in vertices:
            grado = self.grafo.gradoSalida(vertice)
            mensaje = f"Grado de salida de '{vertice}': {grado}"
            self.escribir_consola(mensaje, "info")
            messagebox.showinfo("Grado de salida", mensaje)
    
    def mostrar_aristas_entrada(self):
        vertices = self.grafo.vertices()
        if not vertices:
            self.escribir_consola("No hay vértices", "warning")
            return
        
        vertice = simpledialog.askstring("Aristas de entrada", 
                                         f"Vértices: {vertices}\n¿De qué vértice?")
        if vertice and vertice in vertices:
            aristas = self.grafo.aristasIncidentesEntrada(vertice)
            if aristas:
                aristas_str = [f"{u} → {v}" for u, v in aristas]
                mensaje = f"Aristas de entrada a '{vertice}': {aristas_str}"
            else:
                mensaje = f"No hay aristas de entrada a '{vertice}'"
            self.escribir_consola(mensaje, "info")
            messagebox.showinfo("Aristas de entrada", mensaje)
    
    def mostrar_aristas_salida(self):
        vertices = self.grafo.vertices()
        if not vertices:
            self.escribir_consola("No hay vértices", "warning")
            return
        
        vertice = simpledialog.askstring("Aristas de salida", 
                                         f"Vértices: {vertices}\n¿De qué vértice?")
        if vertice and vertice in vertices:
            aristas = self.grafo.aristasIncidentesSalida(vertice)
            if aristas:
                aristas_str = [f"{u} → {v}" for u, v in aristas]
                mensaje = f"Aristas de salida de '{vertice}': {aristas_str}"
            else:
                mensaje = f"No hay aristas de salida de '{vertice}'"
            self.escribir_consola(mensaje, "info")
            messagebox.showinfo("Aristas de salida", mensaje)
    
    def mostrar_origen(self):
        aristas = self.grafo.aristas()
        if not aristas:
            self.escribir_consola("No hay aristas", "warning")
            return
        
        aristas_str = [f"{u}-{v}" for u, v in aristas]
        arista_input = simpledialog.askstring("Origen", 
                                              f"Aristas: {aristas_str}\nEjemplo: u-v")
        
        if arista_input and '-' in arista_input:
            u, v = arista_input.split('-')
            if (u, v) in aristas or (v, u) in aristas:
                origen = self.grafo.origen((u, v))
                mensaje = f"Origen de la arista {u}-{v}: {origen}"
                self.escribir_consola(mensaje, "info")
                messagebox.showinfo("Origen", mensaje)
    
    def mostrar_destino(self):
        aristas = self.grafo.aristas()
        if not aristas:
            self.escribir_consola("No hay aristas", "warning")
            return
        
        aristas_str = [f"{u}-{v}" for u, v in aristas]
        arista_input = simpledialog.askstring("Destino", 
                                              f"Aristas: {aristas_str}\nEjemplo: u-v")
        
        if arista_input and '-' in arista_input:
            u, v = arista_input.split('-')
            if (u, v) in aristas or (v, u) in aristas:
                destino = self.grafo.destino((u, v))
                mensaje = f"Destino de la arista {u}-{v}: {destino}"
                self.escribir_consola(mensaje, "info")
                messagebox.showinfo("Destino", mensaje)
    
    def listar_vertices(self):
        vertices = self.grafo.vertices()
        if vertices:
            mensaje = f"Vértices: {', '.join(map(str, vertices))}"
        else:
            mensaje = "No hay vértices en el grafo"
        self.escribir_consola(mensaje, "info")
        messagebox.showinfo("Vértices", mensaje)
    
    def listar_aristas(self):
        aristas = self.grafo.aristas()
        if aristas:
            aristas_str = [f"{u} → {v}" if self.grafo.dirigido else f"{u} - {v}" 
                          for u, v in aristas]
            mensaje = f"Aristas: {', '.join(aristas_str)}"
        else:
            mensaje = "No hay aristas en el grafo"
        self.escribir_consola(mensaje, "info")
        messagebox.showinfo("Aristas", mensaje)
    
    def mostrar_esta_vacio(self):
        vacio = self.grafo.estaVacio()
        mensaje = f"El grafo {'está' if vacio else 'no está'} vacío"
        self.escribir_consola(mensaje, "info")
        messagebox.showinfo("Estado", mensaje)
    
    def mostrar_tamano(self):
        tam = self.grafo.tamano()
        mensaje = f"Tamaño total (vértices + aristas): {tam}"
        self.escribir_consola(mensaje, "info")
        messagebox.showinfo("Tamaño", mensaje)
    
    def listar_elementos(self):
        elementos = self.grafo.elementos()
        elementos_str = []
        for e in elementos:
            if isinstance(e, tuple):
                elementos_str.append(f"{e[0]}-{e[1]}")
            else:
                elementos_str.append(str(e))
        mensaje = f"Elementos: {', '.join(elementos_str)}"
        self.escribir_consola(mensaje, "info")
        messagebox.showinfo("Elementos", mensaje)
    
    def listar_posiciones(self):
        posiciones = self.grafo.posiciones()
        mensaje = f"Posiciones (vértices): {', '.join(map(str, posiciones))}"
        self.escribir_consola(mensaje, "info")
        messagebox.showinfo("Posiciones", mensaje)
    
    def reemplazar_vertice(self):
        vertices = self.grafo.vertices()
        if not vertices:
            self.escribir_consola("No hay vértices", "warning")
            return
        
        p = simpledialog.askstring("Reemplazar", f"Vértices: {vertices}\nVértice a reemplazar:")
        if p and p in vertices:
            r = simpledialog.askstring("Reemplazar", "Nuevo nombre:")
            if r:
                self.grafo.reemplazar(p, r)
                self.dibujar_grafo()
                mensaje = f"Vértice '{p}' reemplazado por '{r}'"
                self.escribir_consola(mensaje, "success")
                messagebox.showinfo("Éxito", mensaje)
    
    def intercambiar_vertices(self):
        vertices = self.grafo.vertices()
        if len(vertices) < 2:
            self.escribir_consola("Se necesitan al menos 2 vértices", "warning")
            return
        
        p = simpledialog.askstring("Intercambiar", f"Vértices: {vertices}\nPrimer vértice:")
        q = simpledialog.askstring("Intercambiar", "Segundo vértice:")
        
        if p and q and p in vertices and q in vertices:
            self.grafo.intercambiar(p, q)
            self.dibujar_grafo()
            mensaje = f"Vértices '{p}' y '{q}' intercambiados"
            self.escribir_consola(mensaje, "success")
            messagebox.showinfo("Éxito", mensaje)
    
    def convertir_no_dirigida(self):
        if not self.grafo.dirigido:
            self.escribir_consola("El grafo ya es no dirigido", "info")
            return
        
        aristas = self.grafo.aristas()
        if not aristas:
            self.escribir_consola("No hay aristas para convertir", "warning")
            return
        
        aristas_str = [f"{u}-{v}" for u, v in aristas]
        arista_input = simpledialog.askstring("Convertir", 
                                              f"Aristas: {aristas_str}\nArista a convertir:")
        
        if arista_input and '-' in arista_input:
            u, v = arista_input.split('-')
            if (u, v) in aristas:
                self.grafo.convierteNoDirigida((u, v))
                self.dibujar_grafo()
                mensaje = f"Arista {u}-{v} convertida a no dirigida"
                self.escribir_consola(mensaje, "success")
                messagebox.showinfo("Éxito", mensaje)
    
    def invertir_direccion(self):
        if not self.grafo.dirigido:
            self.escribir_consola("Solo aplicable a grafos dirigidos", "warning")
            return
        
        aristas = self.grafo.aristas()
        if not aristas:
            self.escribir_consola("No hay aristas para invertir", "warning")
            return
        
        aristas_str = [f"{u}→{v}" for u, v in aristas]
        arista_input = simpledialog.askstring("Invertir dirección", 
                                              f"Aristas: {aristas_str}\nArista a invertir (u→v):")
        
        if arista_input and '→' in arista_input:
            u, v = arista_input.split('→')
            if (u, v) in aristas:
                self.grafo.invierteDireccion((u, v))
                self.dibujar_grafo()
                mensaje = f"Dirección de {u}→{v} invertida a {v}→{u}"
                self.escribir_consola(mensaje, "success")
                messagebox.showinfo("Éxito", mensaje)
    
    def asignar_desde(self):
        if self.grafo.dirigido:
            self.escribir_consola("Solo aplicable a grafos no dirigidos", "warning")
            return
        
        aristas = self.grafo.aristas()
        if not aristas:
            self.escribir_consola("No hay aristas", "warning")
            return
        
        aristas_str = [f"{u}-{v}" for u, v in aristas]
        arista_input = simpledialog.askstring("Asignar dirección desde", 
                                              f"Aristas: {aristas_str}\nArista:")
        vertice = simpledialog.askstring("Asignar dirección desde", "Vértice de origen:")
        
        if arista_input and vertice and '-' in arista_input:
            u, v = arista_input.split('-')
            if (u, v) in aristas and (vertice == u or vertice == v):
                self.grafo.asignaDireccionDesde((u, v), vertice)
                self.dibujar_grafo()
                mensaje = f"Arista {u}-{v} ahora dirigida desde {vertice}"
                self.escribir_consola(mensaje, "success")
                messagebox.showinfo("Éxito", mensaje)
    
    def asignar_hacia(self):
        if self.grafo.dirigido:
            self.escribir_consola("Solo aplicable a grafos no dirigidos", "warning")
            return
        
        aristas = self.grafo.aristas()
        if not aristas:
            self.escribir_consola("No hay aristas", "warning")
            return
        
        aristas_str = [f"{u}-{v}" for u, v in aristas]
        arista_input = simpledialog.askstring("Asignar dirección hacia", 
                                              f"Aristas: {aristas_str}\nArista:")
        vertice = simpledialog.askstring("Asignar dirección hacia", "Vértice de destino:")
        
        if arista_input and vertice and '-' in arista_input:
            u, v = arista_input.split('-')
            if (u, v) in aristas and (vertice == u or vertice == v):
                self.grafo.asignaDireccionA((u, v), vertice)
                self.dibujar_grafo()
                mensaje = f"Arista {u}-{v} ahora dirigida hacia {vertice}"
                self.escribir_consola(mensaje, "success")
                messagebox.showinfo("Éxito", mensaje)


def main():
    root = tk.Tk()
    app = GrafoVisualApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()