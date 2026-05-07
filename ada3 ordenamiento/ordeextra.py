import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
import threading
import random
import math
import os
import json
import csv
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

class OrdenamientoExternoSimultaneo:
    def __init__(self, root, datos_usuario=None, archivo_cargado=None):
        self.root = root
        self.root.title("Ordenamiento Externo - Mezcla Directa, Mezcla Equilibrada e Intercalación")
        self.root.geometry("1300x800")
        self.root.configure(bg="#2c3e50")
        
        # Datos proporcionados por el usuario o desde archivo
        self.datos_ejemplo = datos_usuario if datos_usuario else []
        self.archivo_actual = archivo_cargado
        self.ruta_archivo = None
        
        self.crear_widgets()
        if self.datos_ejemplo:
            self.mostrar_datos_iniciales()
    
    def crear_widgets(self):
        # Título principal
        titulo = tk.Label(self.root, text="COMPARACIÓN DE MÉTODOS DE ORDENAMIENTO EXTERNO", 
                         font=("Arial", 16, "bold"), bg="#2c3e50", fg="white", pady=10)
        titulo.pack(fill=tk.X)
        
        # Frame para controles de archivo
        frame_archivo = tk.Frame(self.root, bg="#34495e", pady=10)
        frame_archivo.pack(fill=tk.X, padx=10, pady=5)
        
        # Botones para manejo de archivos
        btn_frame = tk.Frame(frame_archivo, bg="#34495e")
        btn_frame.pack()
        
        btn_crear = tk.Button(btn_frame, text="📝 CREAR ARCHIVO", command=self.crear_archivo,
                             bg="#9b59b6", fg="white", font=("Arial", 10, "bold"),
                             width=15, cursor="hand2")
        btn_crear.pack(side=tk.LEFT, padx=5)
        
        btn_cargar = tk.Button(btn_frame, text="📂 CARGAR ARCHIVO", command=self.cargar_archivo,
                              bg="#3498db", fg="white", font=("Arial", 10, "bold"),
                              width=15, cursor="hand2")
        btn_cargar.pack(side=tk.LEFT, padx=5)
        
        btn_guardar = tk.Button(btn_frame, text="💾 GUARDAR RESULTADO", command=self.guardar_resultado,
                               bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                               width=15, cursor="hand2")
        btn_guardar.pack(side=tk.LEFT, padx=5)
        
        btn_nuevos = tk.Button(btn_frame, text="🔄 NUEVOS DATOS", command=self.nuevos_datos,
                              bg="#e67e22", fg="white", font=("Arial", 10, "bold"),
                              width=15, cursor="hand2")
        btn_nuevos.pack(side=tk.LEFT, padx=5)
        
        # Label para mostrar archivo actual
        self.lbl_archivo = tk.Label(frame_archivo, text="", bg="#34495e", fg="#bdc3c7", 
                                    font=("Arial", 9), pady=5)
        self.lbl_archivo.pack()
        
        # Subtítulo con los datos ingresados
        self.subtitulo = tk.Label(self.root, text="", font=("Arial", 9), 
                                 bg="#2c3e50", fg="#bdc3c7", pady=5)
        self.subtitulo.pack(fill=tk.X)
        
        # Mostrar cantidad de elementos
        self.lbl_cantidad = tk.Label(self.root, text="", font=("Arial", 10, "bold"), 
                                    bg="#2c3e50", fg="#f39c12")
        self.lbl_cantidad.pack(fill=tk.X)
        
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
        
        # Frame de control
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
    
    def crear_archivo(self):
        """Ventana para crear un nuevo archivo con datos"""
        ventana_crear = tk.Toplevel(self.root)
        ventana_crear.title("Crear Nuevo Archivo")
        ventana_crear.geometry("700x600")
        ventana_crear.configure(bg="#ecf0f1")
        
        tk.Label(ventana_crear, text="CREAR NUEVO ARCHIVO DE DATOS", 
                font=("Arial", 14, "bold"), bg="#2c3e50", fg="white", pady=10).pack(fill=tk.X)
        
        notebook = ttk.Notebook(ventana_crear)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestaña 1: Ingreso manual
        frame_manual = tk.Frame(notebook, bg="#ecf0f1")
        notebook.add(frame_manual, text="✏️ Ingreso Manual")
        
        tk.Label(frame_manual, text="Ingrese los números separados por comas o espacios:", 
                bg="#ecf0f1", font=("Arial", 10, "bold")).pack(pady=10)
        
        texto_datos = tk.Text(frame_manual, height=10, width=60, font=("Courier", 10))
        texto_datos.pack(pady=10, padx=10)
        
        tk.Label(frame_manual, text="Ejemplo: 45, 23, 89, 12, 67, 34, 90, 21", 
                bg="#ecf0f1", font=("Arial", 8), fg="#7f8c8d").pack()
        
        # Pestaña 2: Generación aleatoria
        frame_aleatorio = tk.Frame(notebook, bg="#ecf0f1")
        notebook.add(frame_aleatorio, text="🎲 Generación Aleatoria")
        
        tk.Label(frame_aleatorio, text="Parámetros de generación:", 
                bg="#ecf0f1", font=("Arial", 10, "bold")).pack(pady=10)
        
        frame_params = tk.Frame(frame_aleatorio, bg="#ecf0f1")
        frame_params.pack(pady=10)
        
        tk.Label(frame_params, text="Cantidad:", bg="#ecf0f1").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        entry_cantidad = tk.Entry(frame_params, width=15)
        entry_cantidad.insert(0, "20")
        entry_cantidad.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_params, text="Valor mínimo:", bg="#ecf0f1").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        entry_min = tk.Entry(frame_params, width=15)
        entry_min.insert(0, "1")
        entry_min.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame_params, text="Valor máximo:", bg="#ecf0f1").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        entry_max = tk.Entry(frame_params, width=15)
        entry_max.insert(0, "100")
        entry_max.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(frame_params, text="Tipo de datos:", bg="#ecf0f1").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        tipo_datos = ttk.Combobox(frame_params, values=["Uniforme", "Normal", "Sin repetición", "Ordenado", "Inverso"], width=13)
        tipo_datos.set("Uniforme")
        tipo_datos.grid(row=3, column=1, padx=5, pady=5)
        
        # Pestaña 3: Configuración de archivo
        frame_config = tk.Frame(notebook, bg="#ecf0f1")
        notebook.add(frame_config, text="⚙️ Configuración Archivo")
        
        tk.Label(frame_config, text="Formato del archivo:", 
                bg="#ecf0f1", font=("Arial", 10, "bold")).pack(pady=10)
        
        formato = tk.StringVar(value="txt")
        
        frame_formatos = tk.Frame(frame_config, bg="#ecf0f1")
        frame_formatos.pack(pady=10)
        
        tk.Radiobutton(frame_formatos, text="TXT (Texto plano)", variable=formato, value="txt",
                      bg="#ecf0f1").pack(anchor="w", padx=20, pady=2)
        tk.Radiobutton(frame_formatos, text="CSV (Valores separados por comas)", variable=formato, value="csv",
                      bg="#ecf0f1").pack(anchor="w", padx=20, pady=2)
        tk.Radiobutton(frame_formatos, text="JSON (Formato JSON)", variable=formato, value="json",
                      bg="#ecf0f1").pack(anchor="w", padx=20, pady=2)
        tk.Radiobutton(frame_formatos, text="XML (Formato XML)", variable=formato, value="xml",
                      bg="#ecf0f1").pack(anchor="w", padx=20, pady=2)
        
        tk.Label(frame_config, text="Nombre del archivo (sin extensión):", 
                bg="#ecf0f1", font=("Arial", 10)).pack(pady=10)
        entry_nombre = tk.Entry(frame_config, width=40)
        entry_nombre.insert(0, f"datos_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        entry_nombre.pack(pady=5)
        
        # Función para generar datos según el tipo
        def generar_datos():
            try:
                cantidad = int(entry_cantidad.get())
                minimo = int(entry_min.get())
                maximo = int(entry_max.get())
                tipo = tipo_datos.get()
                
                if cantidad < 1:
                    messagebox.showwarning("Advertencia", "La cantidad debe ser al menos 1.")
                    return None
                
                if minimo >= maximo:
                    messagebox.showwarning("Advertencia", "El mínimo debe ser menor que el máximo.")
                    return None
                
                if tipo == "Uniforme":
                    datos = [random.randint(minimo, maximo) for _ in range(cantidad)]
                elif tipo == "Normal":
                    media = (minimo + maximo) / 2
                    desviacion = (maximo - minimo) / 6
                    datos = []
                    for _ in range(cantidad):
                        valor = int(random.gauss(media, desviacion))
                        valor = max(minimo, min(maximo, valor))
                        datos.append(valor)
                elif tipo == "Sin repetición":
                    if cantidad > (maximo - minimo + 1):
                        messagebox.showwarning("Advertencia", f"No se pueden generar {cantidad} números únicos en el rango [{minimo}, {maximo}]")
                        return None
                    datos = random.sample(range(minimo, maximo + 1), cantidad)
                elif tipo == "Ordenado":
                    datos = list(range(minimo, minimo + cantidad))
                elif tipo == "Inverso":
                    datos = list(range(maximo, maximo - cantidad, -1))
                else:
                    datos = [random.randint(minimo, maximo) for _ in range(cantidad)]
                
                return datos
            except ValueError:
                messagebox.showwarning("Advertencia", "Ingrese valores numéricos válidos.")
                return None
        
        # Función para guardar el archivo
        def guardar_archivo():
            # Obtener datos
            pestaña_actual = notebook.index(notebook.select())
            
            if pestaña_actual == 0:  # Manual
                texto = texto_datos.get("1.0", tk.END).strip()
                if not texto:
                    messagebox.showwarning("Advertencia", "Ingrese algunos números.")
                    return
                import re
                numeros = re.findall(r'-?\d+', texto)
                if len(numeros) < 1:
                    messagebox.showwarning("Advertencia", "No se encontraron números válidos.")
                    return
                datos = [int(x) for x in numeros]
            else:  # Aleatorio
                datos = generar_datos()
                if datos is None:
                    return
            
            # Obtener configuración del archivo
            extension = formato.get()
            nombre_base = entry_nombre.get().strip()
            if not nombre_base:
                nombre_base = "datos"
            
            nombre_archivo = f"{nombre_base}.{extension}"
            
            # Seleccionar ubicación
            ruta = filedialog.asksaveasfilename(
                title="Guardar archivo",
                initialfile=nombre_archivo,
                defaultextension=f".{extension}",
                filetypes=[
                    (f"Archivos {extension.upper()}", f"*.{extension}"),
                    ("Todos los archivos", "*.*")
                ]
            )
            
            if not ruta:
                return
            
            try:
                # Guardar según formato
                if extension == 'txt':
                    with open(ruta, 'w', encoding='utf-8') as f:
                        f.write(" ".join(str(n) for n in datos))
                        f.write("\n")
                
                elif extension == 'csv':
                    with open(ruta, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(["Numero"] if len(datos) > 0 else [])
                        for num in datos:
                            writer.writerow([num])
                
                elif extension == 'json':
                    with open(ruta, 'w', encoding='utf-8') as f:
                        json.dump({
                            "metadata": {
                                "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "cantidad_elementos": len(datos),
                                "formato": "lista_numeros"
                            },
                            "datos": datos
                        }, f, indent=2, ensure_ascii=False)
                
                elif extension == 'xml':
                    root_xml = ET.Element("datos")
                    root_xml.set("fecha", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    root_xml.set("cantidad", str(len(datos)))
                    
                    for i, num in enumerate(datos):
                        elemento = ET.SubElement(root_xml, "numero")
                        elemento.set("indice", str(i+1))
                        elemento.text = str(num)
                    
                    tree = ET.ElementTree(root_xml)
                    tree.write(ruta, encoding='utf-8', xml_declaration=True)
                
                # Cargar los datos en el programa
                self.datos_ejemplo = datos
                self.ruta_archivo = ruta
                self.archivo_actual = os.path.basename(ruta)
                self.lbl_archivo.config(text=f"Archivo actual: {self.archivo_actual} (creado)")
                self.mostrar_datos_iniciales()
                
                messagebox.showinfo("Éxito", f"Archivo creado y cargado correctamente.\n"
                                           f"Ubicación: {ruta}\n"
                                           f"Elementos: {len(datos)}")
                ventana_crear.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")
        
        # Botones de acción
        frame_botones = tk.Frame(ventana_crear, bg="#ecf0f1", pady=20)
        frame_botones.pack()
        
        tk.Button(frame_botones, text="💾 CREAR Y GUARDAR ARCHIVO", command=guardar_archivo,
                 bg="#27ae60", fg="white", font=("Arial", 11, "bold"),
                 width=25, height=2, cursor="hand2").pack(pady=5)
        
        tk.Button(frame_botones, text="❌ CANCELAR", command=ventana_crear.destroy,
                 bg="#e74c3c", fg="white", font=("Arial", 10),
                 width=20, cursor="hand2").pack(pady=5)
    
    def cargar_archivo(self):
        """Cargar archivo de diferentes formatos"""
        formatos = [
            ("Todos los archivos soportados", "*.txt *.csv *.json *.xml *.dat *.numbers"),
            ("Archivos de texto", "*.txt"),
            ("Archivos CSV", "*.csv"),
            ("Archivos JSON", "*.json"),
            ("Archivos XML", "*.xml"),
            ("Archivos de datos", "*.dat"),
            ("Archivos de números", "*.numbers"),
            ("Todos los archivos", "*.*")
        ]
        
        ruta = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=formatos)
        
        if not ruta:
            return
        
        try:
            datos = self.leer_archivo(ruta)
            
            if datos and len(datos) > 0:
                self.datos_ejemplo = datos
                self.ruta_archivo = ruta
                self.archivo_actual = os.path.basename(ruta)
                self.lbl_archivo.config(text=f"Archivo actual: {self.archivo_actual}")
                self.mostrar_datos_iniciales()
                messagebox.showinfo("Éxito", f"Archivo cargado correctamente.\n{len(datos)} elementos encontrados.")
            else:
                messagebox.showwarning("Advertencia", "El archivo no contiene datos válidos.")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{str(e)}")
    
    def leer_archivo(self, ruta):
        """Leer diferentes formatos de archivo y extraer números"""
        extension = Path(ruta).suffix.lower()
        numeros = []
        
        try:
            if extension == '.txt':
                with open(ruta, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                    import re
                    numeros = [int(x) for x in re.findall(r'-?\d+', contenido)]
            
            elif extension == '.csv':
                with open(ruta, 'r', encoding='utf-8') as f:
                    lector = csv.reader(f)
                    for fila in lector:
                        for elem in fila:
                            try:
                                num = float(elem) if '.' in elem else int(elem)
                                numeros.append(int(num) if isinstance(num, float) else num)
                            except:
                                pass
            
            elif extension == '.json':
                with open(ruta, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Si el JSON tiene estructura con "datos", extraer de ahí
                    if isinstance(data, dict) and "datos" in data:
                        numeros = self.extraer_numeros_json(data["datos"])
                    else:
                        numeros = self.extraer_numeros_json(data)
            
            elif extension == '.xml':
                tree = ET.parse(ruta)
                root = tree.getroot()
                numeros = self.extraer_numeros_xml(root)
            
            elif extension == '.dat':
                with open(ruta, 'rb') as f:
                    contenido = f.read().decode('utf-8', errors='ignore')
                    import re
                    numeros = [int(x) for x in re.findall(r'-?\d+', contenido)]
            
            elif extension == '.numbers':
                with open(ruta, 'r', encoding='utf-8') as f:
                    lineas = f.readlines()
                    for linea in lineas:
                        try:
                            num = int(linea.strip())
                            numeros.append(num)
                        except:
                            pass
            
            else:
                with open(ruta, 'r', encoding='utf-8', errors='ignore') as f:
                    contenido = f.read()
                    import re
                    numeros = [int(x) for x in re.findall(r'-?\d+', contenido)]
            
            return numeros if len(numeros) >= 2 else None
            
        except Exception as e:
            raise Exception(f"Error leyendo archivo {extension}: {str(e)}")
    
    def extraer_numeros_json(self, obj, numeros=None):
        """Extraer números de estructuras JSON anidadas"""
        if numeros is None:
            numeros = []
        
        if isinstance(obj, dict):
            for valor in obj.values():
                self.extraer_numeros_json(valor, numeros)
        elif isinstance(obj, list):
            for elemento in obj:
                self.extraer_numeros_json(elemento, numeros)
        elif isinstance(obj, (int, float)):
            numeros.append(int(obj))
        
        return numeros
    
    def extraer_numeros_xml(self, elemento, numeros=None):
        """Extraer números de estructuras XML"""
        if numeros is None:
            numeros = []
        
        if elemento.text and elemento.text.strip():
            try:
                num = int(elemento.text.strip())
                numeros.append(num)
            except:
                pass
        
        for hijo in elemento:
            self.extraer_numeros_xml(hijo, numeros)
        
        return numeros
    
    def guardar_resultado(self):
        """Guardar los resultados ordenados en un archivo"""
        if not self.resultados:
            messagebox.showwarning("Advertencia", "Primero debe ejecutar el ordenamiento.")
            return
        
        formatos = [
            ("Archivo de texto", "*.txt"),
            ("Archivo CSV", "*.csv"),
            ("Archivo JSON", "*.json"),
            ("Archivo XML", "*.xml")
        ]
        
        ruta = filedialog.asksaveasfilename(
            title="Guardar resultados",
            defaultextension=".txt",
            filetypes=formatos
        )
        
        if not ruta:
            return
        
        try:
            extension = Path(ruta).suffix.lower()
            
            if extension == '.txt':
                with open(ruta, 'w', encoding='utf-8') as f:
                    f.write("="*60 + "\n")
                    f.write("RESULTADOS DE ORDENAMIENTO EXTERNO\n")
                    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("="*60 + "\n\n")
                    
                    for nombre, datos in self.resultados.items():
                        f.write(f"{nombre.upper()}\n")
                        f.write("-"*40 + "\n")
                        f.write(f"Datos ordenados: {datos['datos']}\n")
                        f.write(f"Comparaciones: {datos['comparaciones']}\n")
                        f.write(f"Tiempo: {datos['tiempo']:.2f} ms\n\n")
            
            elif extension == '.csv':
                with open(ruta, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Algoritmo', 'Datos Ordenados', 'Comparaciones', 'Tiempo (ms)'])
                    for nombre, datos in self.resultados.items():
                        writer.writerow([nombre, str(datos['datos']), datos['comparaciones'], f"{datos['tiempo']:.2f}"])
            
            elif extension == '.json':
                with open(ruta, 'w', encoding='utf-8') as f:
                    json.dump({
                        "metadata": {
                            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "datos_originales": self.datos_ejemplo,
                            "cantidad_elementos": len(self.datos_ejemplo)
                        },
                        "resultados": self.resultados
                    }, f, indent=2, ensure_ascii=False)
            
            elif extension == '.xml':
                root_xml = ET.Element("resultados_ordenamiento")
                root_xml.set("fecha", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                
                for nombre, datos in self.resultados.items():
                    algo_elem = ET.SubElement(root_xml, "algoritmo")
                    algo_elem.set("nombre", nombre)
                    
                    ET.SubElement(algo_elem, "datos_ordenados").text = str(datos['datos'])
                    ET.SubElement(algo_elem, "comparaciones").text = str(datos['comparaciones'])
                    ET.SubElement(algo_elem, "tiempo_ms").text = f"{datos['tiempo']:.2f}"
                
                tree = ET.ElementTree(root_xml)
                tree.write(ruta, encoding='utf-8', xml_declaration=True)
            
            messagebox.showinfo("Éxito", f"Resultados guardados en:\n{ruta}")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")
    
    def nuevos_datos(self):
        """Permitir ingresar nuevos datos desde terminal"""
        ventana_datos = tk.Toplevel(self.root)
        ventana_datos.title("Ingresar Nuevos Datos")
        ventana_datos.geometry("600x500")
        ventana_datos.configure(bg="#ecf0f1")
        
        tk.Label(ventana_datos, text="Ingresar Nuevos Datos", 
                font=("Arial", 14, "bold"), bg="#2c3e50", fg="white", pady=10).pack(fill=tk.X)
        
        frame_opciones = tk.Frame(ventana_datos, bg="#ecf0f1", pady=10)
        frame_opciones.pack()
        
        def cargar_manual():
            texto = entrada_texto.get("1.0", tk.END).strip()
            if texto:
                import re
                numeros = re.findall(r'-?\d+', texto)
                if len(numeros) >= 2:
                    self.datos_ejemplo = [int(x) for x in numeros]
                    self.ruta_archivo = None
                    self.archivo_actual = "Datos manuales"
                    self.lbl_archivo.config(text="Archivo actual: Datos manuales")
                    self.mostrar_datos_iniciales()
                    ventana_datos.destroy()
                    messagebox.showinfo("Éxito", f"{len(numeros)} números cargados correctamente.")
                else:
                    messagebox.showwarning("Advertencia", "Ingrese al menos 2 números.")
        
        def generar_aleatorios():
            try:
                cantidad = int(entry_cantidad.get())
                if cantidad < 2:
                    messagebox.showwarning("Advertencia", "La cantidad debe ser al menos 2.")
                    return
                
                minimo = int(entry_min.get())
                maximo = int(entry_max.get())
                
                if minimo >= maximo:
                    messagebox.showwarning("Advertencia", "El mínimo debe ser menor que el máximo.")
                    return
                
                self.datos_ejemplo = [random.randint(minimo, maximo) for _ in range(cantidad)]
                random.shuffle(self.datos_ejemplo)
                self.ruta_archivo = None
                self.archivo_actual = "Datos aleatorios"
                self.lbl_archivo.config(text="Archivo actual: Datos aleatorios")
                self.mostrar_datos_iniciales()
                ventana_datos.destroy()
                messagebox.showinfo("Éxito", f"{cantidad} números generados correctamente.")
                
            except ValueError:
                messagebox.showwarning("Advertencia", "Ingrese valores numéricos válidos.")
        
        notebook = ttk.Notebook(ventana_datos)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        frame_manual = tk.Frame(notebook, bg="#ecf0f1")
        notebook.add(frame_manual, text="Manual")
        
        tk.Label(frame_manual, text="Ingrese números separados por comas o espacios:", 
                bg="#ecf0f1", font=("Arial", 10)).pack(pady=10)
        
        entrada_texto = tk.Text(frame_manual, height=10, width=60, font=("Courier", 10))
        entrada_texto.pack(pady=10, padx=10)
        
        tk.Button(frame_manual, text="Cargar Datos", command=cargar_manual,
                 bg="#3498db", fg="white", font=("Arial", 10, "bold"),
                 width=20, cursor="hand2").pack(pady=10)
        
        frame_aleatorio = tk.Frame(notebook, bg="#ecf0f1")
        notebook.add(frame_aleatorio, text="Aleatorio")
        
        tk.Label(frame_aleatorio, text="Cantidad de números:", bg="#ecf0f1", font=("Arial", 10)).pack(pady=5)
        entry_cantidad = tk.Entry(frame_aleatorio, font=("Arial", 10), width=20)
        entry_cantidad.insert(0, "20")
        entry_cantidad.pack(pady=5)
        
        tk.Label(frame_aleatorio, text="Valor mínimo:", bg="#ecf0f1", font=("Arial", 10)).pack(pady=5)
        entry_min = tk.Entry(frame_aleatorio, font=("Arial", 10), width=20)
        entry_min.insert(0, "1")
        entry_min.pack(pady=5)
        
        tk.Label(frame_aleatorio, text="Valor máximo:", bg="#ecf0f1", font=("Arial", 10)).pack(pady=5)
        entry_max = tk.Entry(frame_aleatorio, font=("Arial", 10), width=20)
        entry_max.insert(0, "100")
        entry_max.pack(pady=5)
        
        tk.Button(frame_aleatorio, text="Generar Datos", command=generar_aleatorios,
                 bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                 width=20, cursor="hand2").pack(pady=20)
    
    def crear_panel_algoritmo(self, columna, titulo, color):
        frame = tk.LabelFrame(self.frame_principal, text=titulo, font=("Arial", 11, "bold"),
                             bg="#ecf0f1", fg=color, bd=2, relief=tk.RAISED)
        frame.grid(row=0, column=columna, padx=10, pady=10, sticky="nsew")
        
        canvas = tk.Canvas(frame, bg="white", height=300, highlightthickness=1)
        canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        label_datos = tk.Label(frame, text="", bg="#ecf0f1", font=("Courier", 8), wraplength=380)
        label_datos.pack(fill=tk.X, padx=5, pady=5)
        
        label_stats = tk.Label(frame, text="Comparaciones: 0 | Tiempo: 0 ms", 
                              bg="#ecf0f1", font=("Arial", 9), fg="#2c3e50")
        label_stats.pack(fill=tk.X, padx=5, pady=2)
        
        label_estado = tk.Label(frame, text="⚡ En espera", bg="#ecf0f1", font=("Arial", 9, "italic"), fg="#7f8c8d")
        label_estado.pack(fill=tk.X, padx=5, pady=2)
        
        frame.canvas = canvas
        frame.label_datos = label_datos
        frame.label_stats = label_stats
        frame.label_estado = label_estado
        frame.color = color
        
        return frame
    
    def mostrar_datos_iniciales(self):
        datos_str = str(self.datos_ejemplo)
        if len(datos_str) > 80:
            datos_str = datos_str[:77] + "..."
        self.subtitulo.config(text=f"Datos cargados: {datos_str}")
        self.lbl_cantidad.config(text=f"Total de elementos: {len(self.datos_ejemplo)}")
        
        for frame in [self.frame_mezcla_directa, self.frame_mezcla_equilibrada, self.frame_intercalacion]:
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
        
        bar_width = max(2, (width - 20) / n - 2)
        max_valor = max(datos) if datos else 1
        min_valor = min(datos) if datos else 0
        rango = max_valor - min_valor if max_valor != min_valor else 1
        
        total_width = n * (bar_width + 2)
        offset = max(5, (width - total_width) / 2)
        
        for i, valor in enumerate(datos):
            x0 = offset + i * (bar_width + 2)
            bar_height = ((valor - min_valor) / rango) * (height - 60)
            y0 = height - bar_height - 40
            y1 = height - 40
            
            intensidad = (valor - min_valor) / rango
            r = int(255 * (1 - intensidad))
            g = int(255 * intensidad)
            b = 100
            color = f"#{r:02x}{g:02x}{b:02x}"
            
            canvas.create_rectangle(x0, y0, x0 + bar_width, y1, fill=color, outline="#34495e", width=1)
            
            if bar_width >= 12 and n <= 30:
                canvas.create_text(x0 + bar_width/2, y1 - 5, text=str(valor), anchor="n", font=("Arial", 7))
            elif bar_width >= 8 and n <= 60:
                canvas.create_text(x0 + bar_width/2, y1 - 5, text=str(valor), anchor="n", font=("Arial", 6))
        
        canvas.update()
    
    def actualizar_visualizacion(self, frame, datos, mensaje, comparaciones, tiempo_ms):
        datos_str = str(datos)
        if len(datos_str) > 60:
            datos_str = datos_str[:57] + "..."
        frame.label_datos.config(text=f"Datos: {datos_str}")
        frame.label_stats.config(text=f"Comparaciones: {comparaciones} | Tiempo: {tiempo_ms:.0f} ms")
        frame.label_estado.config(text=mensaje)
        self.dibujar_barras(frame.canvas, datos, frame.color)
    
    def mezcla_directa(self, frame, datos_originales, resultados):
        inicio = time.time()
        datos = datos_originales.copy()
        paso = 1
        fase = 1
        comparaciones = 0
        
        self.actualizar_visualizacion(frame, datos, f"Fase {fase}: Inicio", comparaciones, 0)
        time.sleep(0.1)
        
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
            time.sleep(0.1)
            paso *= 2
        
        tiempo_ms = (time.time() - inicio) * 1000
        self.actualizar_visualizacion(frame, datos, "✅ COMPLETADO", comparaciones, tiempo_ms)
        resultados["mezcla_directa"] = {"datos": datos, "comparaciones": comparaciones, "tiempo": tiempo_ms}
        return datos
    
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
        time.sleep(0.1)
        
        comparaciones = [0]
        frame.label_estado.config(text="Mezclando niveles...")
        time.sleep(0.1)
        
        datos_ordenados = self.mezcla_equilibrada_recursiva(frame, datos_originales, 0, comparaciones)
        self.actualizar_visualizacion(frame, datos_ordenados, "Mezclando...", comparaciones[0], (time.time() - inicio) * 1000)
        time.sleep(0.1)
        
        tiempo_ms = (time.time() - inicio) * 1000
        self.actualizar_visualizacion(frame, datos_ordenados, "✅ COMPLETADO", comparaciones[0], tiempo_ms)
        resultados["mezcla_equilibrada"] = {"datos": datos_ordenados, "comparaciones": comparaciones[0], "tiempo": tiempo_ms}
        return datos_ordenados
    
    def intercalacion(self, frame, datos_originales, resultados):
        inicio = time.time()
        datos = datos_originales.copy()
        k = 2
        fase = 1
        comparaciones = 0
        
        self.actualizar_visualizacion(frame, datos, f"Fase {fase}: bloque tamaño 1", comparaciones, 0)
        time.sleep(0.1)
        
        while k <= len(datos):
            fase += 1
            for i in range(0, len(datos), k):
                sublista = datos[i:i + k]
                for j in range(1, len(sublista)):
                    for m in range(j):
                        comparaciones += 1
                sublista.sort()
                datos[i:i + k] = sublista
            
            self.actualizar_visualizacion(frame, datos, f"Fase {fase}: bloque tamaño {k}", comparaciones, (time.time() - inicio) * 1000)
            time.sleep(0.1)
            
            if k >= len(datos):
                break
            k *= 2
        
        if k > len(datos) and len(datos) > 2:
            datos.sort()
            self.actualizar_visualizacion(frame, datos, "Fase final: ordenando resto", comparaciones, (time.time() - inicio) * 1000)
            time.sleep(0.1)
        
        tiempo_ms = (time.time() - inicio) * 1000
        self.actualizar_visualizacion(frame, datos, "✅ COMPLETADO", comparaciones, tiempo_ms)
        resultados["intercalacion"] = {"datos": datos, "comparaciones": comparaciones, "tiempo": tiempo_ms}
        return datos
    
    def iniciar_ordenamiento_simultaneo(self):
        if self.ejecutando or not self.datos_ejemplo:
            if not self.datos_ejemplo:
                messagebox.showwarning("Advertencia", "Primero cargue, cree o ingrese datos.")
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
        
        if self.ruta_archivo:
            texto_resumen.insert(tk.END, f"Fuente: {self.archivo_actual}\n")
        
        texto_resumen.insert(tk.END, f"Cantidad de elementos: {len(self.datos_ejemplo)}\n")
        
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
        
        texto_resumen.config(state=tk.DISABLED)
        
        btn_frame = tk.Frame(resumen_win, bg="#ecf0f1", pady=10)
        btn_frame.pack()
        
        tk.Button(btn_frame, text="CERRAR", command=resumen_win.destroy, 
                 bg="#2c3e50", fg="white", font=("Arial", 10, "bold"), width=15).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = OrdenamientoExternoSimultaneo(root)
    
    messagebox.showinfo("Bienvenido", 
                       "PROGRAMA DE ORDENAMIENTO EXTERNO\n\n"
                       "NUEVA FUNCIONALIDAD: CREAR ARCHIVOS\n"
                       "• Botón 'CREAR ARCHIVO' - Crea nuevos archivos en múltiples formatos\n"
                       "• Formatos soportados: TXT, CSV, JSON, XML\n"
                       "• Puede ingresar datos manualmente o generarlos aleatoriamente\n"
                       "• Los archivos creados se cargan automáticamente\n\n"
                       "También puede:\n"
                       "• Cargar archivos existentes\n"
                       "• Guardar resultados ordenados\n"
                       "• Generar datos aleatorios\n"
                       "• Ingresar datos manualmente")
    
    root.mainloop()