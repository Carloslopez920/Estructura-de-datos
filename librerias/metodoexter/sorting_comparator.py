# sorting_comparator.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from pathlib import Path
from datetime import datetime
from typing import List, Any, Optional, Dict
import os

from file_utils import FileProcessor
from data_processor import DataProcessor
from external_sorting import ExternalSortingAlgorithms

class SortingComparatorApp:
    """Aplicación principal para comparación y ordenamiento de archivos"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Ordenamiento Externo - Comparador de Archivos")
        self.root.geometry("1400x900")
        self.root.configure(bg="#2c3e50")
        
        # Componentes
        self.file_processor = FileProcessor()
        self.data_processor = DataProcessor()
        
        # Estado de la aplicación
        self.data_type = DataProcessor.TIPO_NUMEROS
        self.data1: List[Any] = []
        self.data2: List[Any] = []
        self.raw_data1: str = ""
        self.raw_data2: str = ""
        self.file1_path: Optional[str] = None
        self.file2_path: Optional[str] = None
        self.file1_name: Optional[str] = None
        self.file2_name: Optional[str] = None
        self.combined_data: List[Any] = []
        self.results: Dict = {}
        
        # Hojas de Excel seleccionadas
        self.selected_sheets1: List[str] = []
        self.selected_sheets2: List[str] = []
        self.available_sheets1: List[str] = []
        self.available_sheets2: List[str] = []
        
        self.executing = False
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Crear todos los widgets de la interfaz"""
        # Título principal
        title = tk.Label(self.root, text="📊 COMPARADOR Y ORDENADOR DE ARCHIVOS", 
                        font=("Arial", 16, "bold"), bg="#2c3e50", fg="white", pady=10)
        title.pack(fill=tk.X)
        
        # Frame para tipo de dato
        self._create_data_type_frame()
        
        # Frame para archivos
        self._create_files_frame()
        
        # Botones de acción
        self._create_action_buttons()
        
        # Frame para visualización
        self._create_visualization_frame()
        
        # Frame para algoritmos
        self._create_algorithms_frame()
        
        # Barra de progreso
        self.progress = ttk.Progressbar(self.root, mode='indeterminate')
        self.progress.pack(fill=tk.X, padx=200, pady=5)
    
    def _create_data_type_frame(self):
        """Crear frame de selección de tipo de dato"""
        frame = tk.LabelFrame(self.root, text="📋 TIPO DE DATO A ANALIZAR", 
                             font=("Arial", 10, "bold"), bg="#34495e", fg="white", padx=10, pady=5)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.type_var = tk.StringVar(value=DataProcessor.TIPO_NUMEROS)
        
        for text, value, desc in self.data_processor.get_tipos_disponibles():
            rb = tk.Radiobutton(frame, text=text, variable=self.type_var, value=value,
                               bg="#34495e", fg="white", selectcolor="#2c3e50",
                               font=("Arial", 9), command=self._on_data_type_change)
            rb.pack(side=tk.LEFT, padx=10, pady=5)
    
    def _create_files_frame(self):
        """Crear frame para carga de archivos"""
        files_frame = tk.Frame(self.root, bg="#34495e", pady=10)
        files_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Archivo 1
        frame1 = tk.LabelFrame(files_frame, text="📁 ARCHIVO 1", font=("Arial", 10, "bold"),
                               bg="#ecf0f1", fg="#3498db", padx=10, pady=5)
        frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        btn1 = tk.Button(frame1, text="📂 CARGAR ARCHIVO 1", command=lambda: self._load_file(1),
                        bg="#3498db", fg="white", font=("Arial", 10, "bold"), cursor="hand2")
        btn1.pack(pady=5)
        
        self.file1_label = tk.Label(frame1, text="Ningún archivo cargado", 
                                    bg="#ecf0f1", fg="#7f8c8d", font=("Arial", 9))
        self.file1_label.pack(pady=5)
        
        self.sheets1_label = tk.Label(frame1, text="", bg="#ecf0f1", fg="#3498db", font=("Arial", 8, "italic"))
        self.sheets1_label.pack(pady=2)
        
        self.stats1_label = tk.Label(frame1, text="", bg="#ecf0f1", fg="#2c3e50", font=("Arial", 9))
        self.stats1_label.pack(pady=5)
        
        # Archivo 2
        frame2 = tk.LabelFrame(files_frame, text="📁 ARCHIVO 2", font=("Arial", 10, "bold"),
                               bg="#ecf0f1", fg="#e74c3c", padx=10, pady=5)
        frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        btn2 = tk.Button(frame2, text="📂 CARGAR ARCHIVO 2", command=lambda: self._load_file(2),
                        bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), cursor="hand2")
        btn2.pack(pady=5)
        
        self.file2_label = tk.Label(frame2, text="Ningún archivo cargado", 
                                    bg="#ecf0f1", fg="#7f8c8d", font=("Arial", 9))
        self.file2_label.pack(pady=5)
        
        self.sheets2_label = tk.Label(frame2, text="", bg="#ecf0f1", fg="#e74c3c", font=("Arial", 8, "italic"))
        self.sheets2_label.pack(pady=2)
        
        self.stats2_label = tk.Label(frame2, text="", bg="#ecf0f1", fg="#2c3e50", font=("Arial", 9))
        self.stats2_label.pack(pady=5)
    
    def _create_action_buttons(self):
        """Crear botones de acción"""
        btn_frame = tk.Frame(self.root, bg="#2c3e50", pady=10)
        btn_frame.pack(fill=tk.X)
        
        buttons = [
            ("🔍 COMPARAR ARCHIVOS", self._compare_files, "#9b59b6"),
            ("🔄 COMBINAR Y ORDENAR", self._combine_and_sort, "#f39c12"),
            ("💾 GUARDAR RESULTADO", self._save_result, "#27ae60")
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(btn_frame, text=text, command=command,
                           bg=color, fg="white", font=("Arial", 11, "bold"),
                           width=20, height=2, cursor="hand2")
            btn.pack(side=tk.LEFT, padx=10, expand=True)
        
        self.combine_info_label = tk.Label(self.root, text="", bg="#2c3e50", fg="#f39c12", 
                                           font=("Arial", 10, "bold"), pady=5)
        self.combine_info_label.pack(fill=tk.X)
    
    def _create_visualization_frame(self):
        """Crear frame para visualización de datos"""
        viz_frame = tk.LabelFrame(self.root, text="📊 VISTA PREVIA DE DATOS", 
                                  font=("Arial", 10, "bold"), bg="#2c3e50", fg="white")
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.data_text = tk.Text(viz_frame, font=("Courier", 9), wrap=tk.WORD,
                                 bg="#f8f9fa", height=10)
        scrollbar = tk.Scrollbar(viz_frame, orient="vertical", command=self.data_text.yview)
        self.data_text.configure(yscrollcommand=scrollbar.set)
        
        self.data_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _create_algorithms_frame(self):
        """Crear frame para los algoritmos"""
        algo_frame = tk.LabelFrame(self.root, text="⚡ ALGORITMOS DE ORDENAMIENTO", 
                                   font=("Arial", 10, "bold"), bg="#2c3e50", fg="white")
        algo_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Frame para los tres algoritmos
        algorithms_container = tk.Frame(algo_frame, bg="#2c3e50")
        algorithms_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        algorithms_container.columnconfigure(0, weight=1)
        algorithms_container.columnconfigure(1, weight=1)
        algorithms_container.columnconfigure(2, weight=1)
        
        self.algo_frames = {}
        algos_info = ExternalSortingAlgorithms.get_algorithms_info()
        
        for i, (key, info) in enumerate(algos_info.items()):
            frame = self._create_algorithm_panel(algorithms_container, i, info)
            self.algo_frames[key] = frame
    
    def _create_algorithm_panel(self, parent, column, info: Dict) -> tk.Frame:
        """Crear panel para un algoritmo"""
        frame = tk.LabelFrame(parent, text=info["nombre"], font=("Arial", 11, "bold"),
                             bg="#ecf0f1", fg=info["color"], bd=2, relief=tk.RAISED)
        frame.grid(row=0, column=column, padx=10, pady=10, sticky="nsew")
        
        # Canvas para visualización
        canvas = tk.Canvas(frame, bg="white", height=250, highlightthickness=1)
        canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Labels de información
        data_label = tk.Label(frame, text="", bg="#ecf0f1", font=("Courier", 8), wraplength=350)
        data_label.pack(fill=tk.X, padx=5, pady=2)
        
        stats_label = tk.Label(frame, text="Comparaciones: 0 | Tiempo: 0 ms", 
                              bg="#ecf0f1", font=("Arial", 9), fg="#2c3e50")
        stats_label.pack(fill=tk.X, padx=5, pady=2)
        
        status_label = tk.Label(frame, text="⚡ En espera", bg="#ecf0f1", 
                                font=("Arial", 9, "italic"), fg="#7f8c8d")
        status_label.pack(fill=tk.X, padx=5, pady=2)
        
        complexity_label = tk.Label(frame, text=f"Complejidad: {info['complejidad']}", 
                                   bg="#ecf0f1", font=("Arial", 8), fg="#7f8c8d")
        complexity_label.pack(fill=tk.X, padx=5, pady=2)
        
        return {
            "frame": frame,
            "canvas": canvas,
            "data_label": data_label,
            "stats_label": stats_label,
            "status_label": status_label
        }
    
    def _on_data_type_change(self):
        """Manejar cambio de tipo de dato"""
        self.data_type = self.type_var.get()
        
        # Recargar archivos si están cargados
        if self.file1_path:
            self._reload_file(1, self.file1_path)
        if self.file2_path:
            self._reload_file(2, self.file2_path)
        
        messagebox.showinfo("Tipo de dato", 
                           f"Modo cambiado a: {self.data_type.upper()}\n"
                           f"Los datos se procesarán según este tipo.")
    
    def _load_file(self, file_num: int):
        """Cargar un archivo"""
        formats = self.file_processor.get_supported_formats()
        filepath = filedialog.askopenfilename(title=f"Seleccionar Archivo {file_num}", filetypes=formats)
        
        if not filepath:
            return
        
        extension = Path(filepath).suffix.lower()
        
        # Manejar archivos Excel
        if extension in ['.xlsx', '.xls'] and FileProcessor.EXCEL_AVAILABLE:
            self._load_excel_file(file_num, filepath)
        else:
            self._load_regular_file(file_num, filepath)
    
    def _load_regular_file(self, file_num: int, filepath: str):
        """Cargar archivo regular (no Excel)"""
        try:
            raw_content = self.file_processor.read_file_raw(filepath)
            processed_data = self.data_processor.process_by_type(raw_content, self.data_type)
            
            if processed_data:
                if file_num == 1:
                    self.data1 = processed_data
                    self.raw_data1 = raw_content
                    self.file1_path = filepath
                    self.file1_name = os.path.basename(filepath)
                    self.file1_label.config(text=f"📄 {self.file1_name}")
                    self._update_stats_display(1, processed_data)
                else:
                    self.data2 = processed_data
                    self.raw_data2 = raw_content
                    self.file2_path = filepath
                    self.file2_name = os.path.basename(filepath)
                    self.file2_label.config(text=f"📄 {self.file2_name}")
                    self._update_stats_display(2, processed_data)
                
                self._update_data_preview()
                messagebox.showinfo("Éxito", f"Archivo {file_num} cargado.\n{len(processed_data)} elementos encontrados.")
            else:
                messagebox.showwarning("Advertencia", f"No se encontraron elementos del tipo '{self.data_type}' en el archivo.")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{str(e)}")
    
    def _load_excel_file(self, file_num: int, filepath: str):
        """Cargar archivo Excel con selección de hojas"""
        try:
            sheets = self.file_processor.get_excel_sheets(filepath)
            
            if file_num == 1:
                self.available_sheets1 = sheets
                self.file1_path = filepath
                self.file1_name = os.path.basename(filepath)
                self.file1_label.config(text=f"📄 {self.file1_name}")
                self._show_sheet_selector(1, filepath, sheets)
            else:
                self.available_sheets2 = sheets
                self.file2_path = filepath
                self.file2_name = os.path.basename(filepath)
                self.file2_label.config(text=f"📄 {self.file2_name}")
                self._show_sheet_selector(2, filepath, sheets)
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el Excel:\n{str(e)}")
    
    def _show_sheet_selector(self, file_num: int, filepath: str, sheets: List[str]):
        """Mostrar selector de hojas de Excel"""
        selector = tk.Toplevel(self.root)
        selector.title(f"Seleccionar Hojas - Archivo {file_num}")
        selector.geometry("500x400")
        selector.configure(bg="#ecf0f1")
        
        tk.Label(selector, text=f"SELECCIONAR HOJAS DE EXCEL", 
                font=("Arial", 12, "bold"), bg="#2c3e50", fg="white", pady=10).pack(fill=tk.X)
        
        tk.Label(selector, text=f"Archivo: {os.path.basename(filepath)}", 
                font=("Arial", 10), bg="#ecf0f1", pady=5).pack()
        
        # Frame con scroll para checkboxes
        frame = tk.Frame(selector, bg="#ecf0f1")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        canvas = tk.Canvas(frame, bg="#ecf0f1", highlightthickness=0)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg="#ecf0f1")
        
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        sheet_vars = {}
        for sheet in sheets:
            var = tk.BooleanVar(value=True)
            sheet_vars[sheet] = var
            cb = tk.Checkbutton(scrollable, text=sheet, variable=var,
                               bg="#ecf0f1", font=("Arial", 10), anchor="w")
            cb.pack(fill=tk.X, padx=10, pady=2)
        
        btn_frame = tk.Frame(selector, bg="#ecf0f1")
        btn_frame.pack(pady=10)
        
        def select_all():
            for var in sheet_vars.values():
                var.set(True)
        
        def select_none():
            for var in sheet_vars.values():
                var.set(False)
        
        tk.Button(btn_frame, text="Seleccionar Todas", command=select_all,
                 bg="#3498db", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Seleccionar Ninguna", command=select_none,
                 bg="#95a5a6", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        
        def accept():
            selected = [sheet for sheet, var in sheet_vars.items() if var.get()]
            if not selected:
                messagebox.showwarning("Advertencia", "Seleccione al menos una hoja.")
                return
            
            if file_num == 1:
                self.selected_sheets1 = selected
                self.sheets1_label.config(text=f"Hojas: {len(selected)} seleccionadas")
                self._process_excel_sheets(1, filepath, selected)
            else:
                self.selected_sheets2 = selected
                self.sheets2_label.config(text=f"Hojas: {len(selected)} seleccionadas")
                self._process_excel_sheets(2, filepath, selected)
            
            selector.destroy()
        
        tk.Button(selector, text="ACEPTAR", command=accept,
                 bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                 width=15, pady=5).pack(pady=10)
    
    def _process_excel_sheets(self, file_num: int, filepath: str, selected_sheets: List[str]):
        """Procesar las hojas seleccionadas de Excel"""
        try:
            raw_content, all_data = self.file_processor.process_excel_file(filepath, selected_sheets)
            processed_data = self.data_processor.process_by_type(raw_content, self.data_type)
            
            if file_num == 1:
                self.data1 = processed_data
                self.raw_data1 = raw_content
                self._update_stats_display(1, processed_data)
            else:
                self.data2 = processed_data
                self.raw_data2 = raw_content
                self._update_stats_display(2, processed_data)
            
            self._update_data_preview()
            messagebox.showinfo("Éxito", f"Excel procesado.\n{len(processed_data)} elementos extraídos de {len(selected_sheets)} hojas.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error procesando Excel:\n{str(e)}")
    
    def _reload_file(self, file_num: int, filepath: str):
        """Recargar archivo con nuevo tipo de dato"""
        extension = Path(filepath).suffix.lower()
        
        if extension in ['.xlsx', '.xls'] and FileProcessor.EXCEL_AVAILABLE:
            selected = self.selected_sheets1 if file_num == 1 else self.selected_sheets2
            if selected:
                self._process_excel_sheets(file_num, filepath, selected)
        else:
            self._load_regular_file(file_num, filepath)
    
    def _update_stats_display(self, file_num: int, data: List[Any]):
        """Actualizar visualización de estadísticas"""
        stats = self.data_processor.get_statistics(data, self.data_type)
        
        stats_text = f"Elementos: {stats['total']:,}"
        if stats.get('unicos'):
            stats_text += f"\nÚnicos: {stats['unicos']:,}"
        if stats.get('minimo') is not None:
            stats_text += f"\nMín: {stats['minimo']} | Máx: {stats['maximo']}"
        if stats.get('suma') is not None:
            stats_text += f"\nSuma: {stats['suma']:,}"
        
        if file_num == 1:
            self.stats1_label.config(text=stats_text)
        else:
            self.stats2_label.config(text=stats_text)
    
    def _update_data_preview(self):
        """Actualizar vista previa de datos"""
        self.data_text.delete(1.0, tk.END)
        
        if self.data1:
            self.data_text.insert(tk.END, f"📁 ARCHIVO 1: {self.file1_name}\n")
            self.data_text.insert(tk.END, f"{'='*50}\n")
            self._insert_data_preview(self.data1)
        
        if self.data2:
            self.data_text.insert(tk.END, f"\n📁 ARCHIVO 2: {self.file2_name}\n")
            self.data_text.insert(tk.END, f"{'='*50}\n")
            self._insert_data_preview(self.data2)
    
    def _insert_data_preview(self, data: List[Any], max_items: int = 100):
        """Insertar vista previa de datos"""
        if self.data_type == DataProcessor.TIPO_NUMEROS:
            items = [str(x) for x in data[:max_items]]
            line = ", ".join(items)
            self.data_text.insert(tk.END, line + "\n")
            if len(data) > max_items:
                self.data_text.insert(tk.END, f"... y {len(data)-max_items} elementos más\n")
        else:
            for i, item in enumerate(data[:max_items], 1):
                item_str = str(item)[:100]
                self.data_text.insert(tk.END, f"{i}. {item_str}\n")
            if len(data) > max_items:
                self.data_text.insert(tk.END, f"... y {len(data)-max_items} elementos más\n")
    
    def _compare_files(self):
        """Comparar los dos archivos cargados"""
        if not self.data1 or not self.data2:
            messagebox.showwarning("Advertencia", "Cargue ambos archivos primero.")
            return
        
        comparison = self.data_processor.compare_archives(self.data1, self.data2, self.data_type)
        
        # Mostrar resultados
        result_win = tk.Toplevel(self.root)
        result_win.title("Comparación de Archivos")
        result_win.geometry("800x700")
        result_win.configure(bg="#ecf0f1")
        
        tk.Label(result_win, text="COMPARACIÓN DE ARCHIVOS", 
                font=("Arial", 14, "bold"), bg="#2c3e50", fg="white", pady=10).pack(fill=tk.X)
        
        text_frame = tk.Frame(result_win, bg="#ecf0f1")
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text = tk.Text(text_frame, font=("Courier", 10), wrap=tk.WORD,
                      yscrollcommand=scrollbar.set, padx=15, pady=15)
        text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=text.yview)
        
        text.insert(tk.END, "="*70 + "\n")
        text.insert(tk.END, f"TIPO DE DATO: {self.data_type.upper()}\n")
        text.insert(tk.END, "="*70 + "\n\n")
        
        text.insert(tk.END, f"ARCHIVO 1: {self.file1_name}\n")
        text.insert(tk.END, f"  • Elementos: {comparison['archivo1']['elementos']:,}\n")
        text.insert(tk.END, f"  • Únicos: {comparison['archivo1']['unicos']:,}\n\n")
        
        text.insert(tk.END, f"ARCHIVO 2: {self.file2_name}\n")
        text.insert(tk.END, f"  • Elementos: {comparison['archivo2']['elementos']:,}\n")
        text.insert(tk.END, f"  • Únicos: {comparison['archivo2']['unicos']:,}\n\n")
        
        text.insert(tk.END, "="*70 + "\n")
        text.insert(tk.END, "COMPARACIÓN\n")
        text.insert(tk.END, "="*70 + "\n\n")
        
        comp = comparison['comparacion']
        text.insert(tk.END, f"📊 Elementos comunes: {comp['comunes']:,}\n")
        text.insert(tk.END, f"📊 Similitud: {comp['similitud']:.2f}%\n")
        text.insert(tk.END, f"🔴 Solo en Archivo 1: {comp['solo_archivo1']:,}\n")
        text.insert(tk.END, f"🔵 Solo en Archivo 2: {comp['solo_archivo2']:,}\n\n")
        
        if comp['comunes'] > 0:
            text.insert(tk.END, f"Elementos comunes (primeros 50):\n{comp['valores_comunes']}\n\n")
        if comp['solo_archivo1'] > 0:
            text.insert(tk.END, f"Solo en Archivo 1:\n{comp['valores_solo1']}\n\n")
        if comp['solo_archivo2'] > 0:
            text.insert(tk.END, f"Solo en Archivo 2:\n{comp['valores_solo2']}\n\n")
        
        text.config(state=tk.DISABLED)
        
        tk.Button(result_win, text="CERRAR", command=result_win.destroy,
                 bg="#2c3e50", fg="white", font=("Arial", 10, "bold"), width=15).pack(pady=10)
    
    def _combine_and_sort(self):
        """Combinar y ordenar los datos de ambos archivos"""
        if not self.data1 or not self.data2:
            messagebox.showwarning("Advertencia", "Cargue ambos archivos primero.")
            return
        
        # Combinar datos
        self.combined_data = self.data1 + self.data2
        
        # Ordenar según tipo
        if self.data_type == DataProcessor.TIPO_NUMEROS:
            self.combined_data = sorted(self.combined_data)
        else:
            self.combined_data = sorted(self.combined_data, key=str)
        
        self.combine_info_label.config(
            text=f"📊 COMBINACIÓN: {len(self.data1)} + {len(self.data2)} = {len(self.combined_data)} elementos totales"
        )
        
        # Iniciar ordenamiento
        self._start_sorting()
    
    def _start_sorting(self):
        """Iniciar los algoritmos de ordenamiento"""
        if self.executing or not self.combined_data:
            return
        
        self.executing = True
        self.progress.start()
        
        # Resetear UI
        for frame in self.algo_frames.values():
            frame["status_label"].config(text="🔄 En ejecución...")
            frame["stats_label"].config(text="Comparaciones: 0 | Tiempo: 0 ms")
            frame["canvas"].delete("all")
        
        # Ejecutar algoritmos en hilos separados
        sorter = ExternalSortingAlgorithms(self.data_type)
        
        threads = []
        for key, frame in self.algo_frames.items():
            algorithm = getattr(sorter, key)
            thread = threading.Thread(
                target=self._run_algorithm,
                args=(algorithm, self.combined_data, frame, key)
            )
            threads.append(thread)
            thread.start()
        
        self._monitor_threads(threads)
    
    def _run_algorithm(self, algorithm, data, frame, key):
        """Ejecutar un algoritmo y actualizar UI"""
        def callback(datos, mensaje, comparaciones, tiempo_ms):
            self._update_algorithm_display(frame, datos, mensaje, comparaciones, tiempo_ms)
        
        result = algorithm(data, callback)
        self.results[key] = result
    
    def _update_algorithm_display(self, frame, datos, mensaje, comparaciones, tiempo_ms):
        """Actualizar la visualización de un algoritmo"""
        frame["status_label"].config(text=mensaje)
        frame["stats_label"].config(text=f"Comparaciones: {comparaciones:,} | Tiempo: {tiempo_ms:.0f} ms")
        
        # Actualizar datos mostrados
        if self.data_type == DataProcessor.TIPO_NUMEROS:
            data_str = str(datos[:30]) if datos else "[]"
            if len(datos) > 30:
                data_str = data_str[:-1] + f", ... +{len(datos)-30} más]"
            frame["data_label"].config(text=f"Datos: {data_str}")
            
            # Dibujar barras
            self._draw_bars(frame["canvas"], datos)
        else:
            frame["data_label"].config(text=f"Datos: {len(datos)} elementos")
        
        frame["canvas"].update()
    
    def _draw_bars(self, canvas: tk.Canvas, datos: List[Any]):
        """Dibujar gráfico de barras para datos numéricos"""
        canvas.delete("all")
        
        if not datos or self.data_type != DataProcessor.TIPO_NUMEROS:
            canvas.create_text(200, 125, text="Visualización disponible solo\npara datos numéricos",
                              fill="gray", font=("Arial", 10))
            return
        
        width = canvas.winfo_width() if canvas.winfo_width() > 50 else 380
        height = canvas.winfo_height() if canvas.winfo_height() > 50 else 250
        
        n = min(len(datos), 100)
        if n == 0:
            return
        
        bar_width = max(2, (width - 20) / n - 2)
        max_valor = max(datos[:n])
        min_valor = min(datos[:n])
        rango = max_valor - min_valor if max_valor != min_valor else 1
        
        total_width = n * (bar_width + 2)
        offset = max(5, (width - total_width) / 2)
        
        for i, valor in enumerate(datos[:n]):
            x0 = offset + i * (bar_width + 2)
            bar_height = ((valor - min_valor) / rango) * (height - 50)
            y0 = height - bar_height - 30
            y1 = height - 30
            
            intensidad = (valor - min_valor) / rango
            r = int(255 * (1 - intensidad))
            g = int(255 * intensidad)
            color = f"#{r:02x}{g:02x}60"
            
            canvas.create_rectangle(x0, y0, x0 + bar_width, y1, fill=color, outline="#34495e", width=1)
            
            if bar_width >= 10 and n <= 40:
                canvas.create_text(x0 + bar_width/2, y1 - 5, text=str(valor), 
                                  anchor="n", font=("Arial", 7))
        
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    def _monitor_threads(self, threads):
        """Monitorear la finalización de los hilos"""
        if not any(t.is_alive() for t in threads):
            self.executing = False
            self.progress.stop()
            self._show_sorting_results()
        else:
            self.root.after(500, lambda: self._monitor_threads(threads))
    
    def _show_sorting_results(self):
        """Mostrar resultados del ordenamiento"""
        result_win = tk.Toplevel(self.root)
        result_win.title("Resultados - Ordenamiento")
        result_win.geometry("900x700")
        result_win.configure(bg="#ecf0f1")
        
        tk.Label(result_win, text="RESULTADOS DEL ORDENAMIENTO", 
                font=("Arial", 14, "bold"), bg="#2c3e50", fg="white", pady=10).pack(fill=tk.X)
        
        text_frame = tk.Frame(result_win, bg="#ecf0f1")
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text = tk.Text(text_frame, font=("Courier", 10), wrap=tk.WORD,
                      yscrollcommand=scrollbar.set, padx=15, pady=15)
        text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=text.yview)
        
        # Información general
        text.insert(tk.END, "="*70 + "\n")
        text.insert(tk.END, f"TIPO DE DATO: {self.data_type.upper()}\n")
        text.insert(tk.END, "="*70 + "\n\n")
        
        text.insert(tk.END, f"Archivo 1: {self.file1_name} ({len(self.data1)} elementos)\n")
        text.insert(tk.END, f"Archivo 2: {self.file2_name} ({len(self.data2)} elementos)\n")
        text.insert(tk.END, f"Total combinado: {len(self.combined_data)} elementos\n\n")
        
        text.insert(tk.END, "="*70 + "\n")
        text.insert(tk.END, "RENDIMIENTO DE ALGORITMOS\n")
        text.insert(tk.END, "="*70 + "\n\n")
        
        # Ordenar resultados por tiempo
        sorted_results = sorted(self.results.items(), key=lambda x: x[1]['tiempo_ms'])
        
        for i, (key, result) in enumerate(sorted_results, 1):
            text.insert(tk.END, f"{i}. {result['nombre']}\n")
            text.insert(tk.END, f"   • Comparaciones: {result['comparaciones']:,}\n")
            text.insert(tk.END, f"   • Tiempo: {result['tiempo_ms']:.2f} ms\n\n")
        
        # Mostrar primeros elementos ordenados
        if self.results:
            first_result = list(self.results.values())[0]
            text.insert(tk.END, "="*70 + "\n")
            text.insert(tk.END, "MUESTRA DEL RESULTADO ORDENADO\n")
            text.insert(tk.END, "="*70 + "\n\n")
            
            for i, elem in enumerate(first_result['datos'][:50], 1):
                text.insert(tk.END, f"{i}. {str(elem)[:100]}\n")
            
            if len(first_result['datos']) > 50:
                text.insert(tk.END, f"\n... y {len(first_result['datos'])-50} elementos más\n")
        
        text.config(state=tk.DISABLED)
        
        btn_frame = tk.Frame(result_win, bg="#ecf0f1", pady=10)
        btn_frame.pack()
        
        tk.Button(btn_frame, text="GUARDAR RESULTADO", command=self._save_result,
                 bg="#27ae60", fg="white", font=("Arial", 10, "bold"), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="CERRAR", command=result_win.destroy,
                 bg="#2c3e50", fg="white", font=("Arial", 10, "bold"), width=15).pack(side=tk.LEFT, padx=5)
    
    def _save_result(self):
        """Guardar el resultado combinado y ordenado"""
        if not self.results:
            messagebox.showwarning("Advertencia", "Primero combine y ordene los datos.")
            return
        
        filepath = filedialog.asksaveasfilename(
            title="Guardar resultado",
            defaultextension=".txt",
            filetypes=[
                ("Archivo de texto", "*.txt"),
                ("Archivo CSV", "*.csv"),
                ("Archivo JSON", "*.json"),
                ("Archivo HTML", "*.html"),
            ]
        )
        
        if not filepath:
            return
        
        try:
            first_result = list(self.results.values())[0]
            metadata = {
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "tipo_dato": self.data_type,
                "archivo1": self.file1_name,
                "archivo2": self.file2_name,
                "elementos_archivo1": len(self.data1),
                "elementos_archivo2": len(self.data2),
                "total_combinado": len(self.combined_data),
                "algoritmo_usado": first_result['nombre'],
                "comparaciones": first_result['comparaciones'],
                "tiempo_ms": f"{first_result['tiempo_ms']:.2f}"
            }
            
            self.file_processor.save_result(filepath, first_result['datos'], metadata)
            messagebox.showinfo("Éxito", f"Resultado guardado:\n{filepath}")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar:\n{str(e)}")


def main():
    """Función principal"""
    root = tk.Tk()
    app = SortingComparatorApp(root)
    
    # Mostrar mensaje de bienvenida
    messagebox.showinfo("Bienvenido", 
                       "📊 PROGRAMA DE COMPARACIÓN Y ORDENAMIENTO\n\n"
                       "FUNCIONALIDADES:\n"
                       "✓ Selección de tipo de dato (números, palabras, fechas, etc.)\n"
                       "✓ Carga de múltiples formatos (TXT, CSV, JSON, XML, Excel)\n"
                       "✓ Para archivos Excel: selección de hojas específicas\n"
                       "✓ Comparación entre dos archivos con estadísticas detalladas\n"
                       "✓ Combinación y ordenamiento con 3 algoritmos diferentes\n"
                       "✓ Visualización gráfica del proceso de ordenamiento\n"
                       "✓ Comparativa de rendimiento entre algoritmos\n"
                       "✓ Guardado de resultados en múltiples formatos\n\n"
                       "Instrucciones:\n"
                       "1. Seleccione el tipo de dato a analizar\n"
                       "2. Cargue Archivo 1 y Archivo 2\n"
                       "3. Use 'COMPARAR ARCHIVOS' para ver diferencias\n"
                       "4. Use 'COMBINAR Y ORDENAR' para ordenar los datos combinados\n"
                       "5. Guarde el resultado ordenado")
    
    root.mainloop()


if __name__ == "__main__":
    main()