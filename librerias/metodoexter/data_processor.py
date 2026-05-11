# data_processor.py
import re
from datetime import datetime
from typing import List, Any, Callable, Tuple
from collections import Counter

class DataProcessor:
    """Clase para procesar y analizar datos según diferentes tipos"""
    
    TIPO_NUMEROS = "numeros"
    TIPO_PALABRAS = "palabras"
    TIPO_LINEAS = "lineas"
    TIPO_FECHAS = "fechas"
    TIPO_CARACTERES = "caracteres"
    TIPO_TODO = "todo"
    
    @staticmethod
    def get_tipos_disponibles() -> List[Tuple[str, str, str]]:
        """Obtener lista de tipos de datos disponibles con iconos y descripción"""
        return [
            ("🔢 Números", DataProcessor.TIPO_NUMEROS, "Extrae y ordena valores numéricos"),
            ("📝 Palabras", DataProcessor.TIPO_PALABRAS, "Extrae y ordena palabras alfabéticamente"),
            ("📄 Líneas", DataProcessor.TIPO_LINEAS, "Ordena líneas completas"),
            ("📅 Fechas", DataProcessor.TIPO_FECHAS, "Detecta y ordena fechas cronológicamente"),
            ("🔤 Caracteres", DataProcessor.TIPO_CARACTERES, "Ordena caracteres individuales"),
            ("🌐 Todo", DataProcessor.TIPO_TODO, "Procesa todo el texto completo")
        ]
    
    @staticmethod
    def process_by_type(content: str, data_type: str) -> List[Any]:
        """Procesar datos según el tipo seleccionado"""
        if data_type == DataProcessor.TIPO_NUMEROS:
            return DataProcessor._extract_numbers(content)
        elif data_type == DataProcessor.TIPO_PALABRAS:
            return DataProcessor._extract_words(content)
        elif data_type == DataProcessor.TIPO_LINEAS:
            return DataProcessor._extract_lines(content)
        elif data_type == DataProcessor.TIPO_FECHAS:
            return DataProcessor._extract_dates(content)
        elif data_type == DataProcessor.TIPO_CARACTERES:
            return DataProcessor._extract_characters(content)
        else:
            return DataProcessor._extract_all_elements(content)
    
    @staticmethod
    def _extract_numbers(content: str) -> List[Any]:
        """Extraer números enteros y flotantes"""
        numbers = re.findall(r'-?\d+(?:\.\d+)?', content)
        result = []
        for n in numbers:
            try:
                if '.' in n:
                    result.append(float(n))
                else:
                    result.append(int(n))
            except:
                pass
        return result
    
    @staticmethod
    def _extract_words(content: str) -> List[str]:
        """Extraer palabras (mínimo 2 caracteres)"""
        words = re.findall(r'\b[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ][a-zA-ZáéíóúüñÁÉÍÓÚÜÑ0-9]*\b', content)
        return [w.lower() for w in words if len(w) >= 2]
    
    @staticmethod
    def _extract_lines(content: str) -> List[str]:
        """Extraer líneas no vacías"""
        lines = content.split('\n')
        return [l.strip() for l in lines if l.strip()]
    
    @staticmethod
    def _extract_dates(content: str) -> List[Any]:
        """Extraer y convertir fechas"""
        date_patterns = [
            r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',
            r'\d{4}[/-]\d{1,2}[/-]\d{1,2}',
            r'\d{1,2}\s+(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+\d{4}',
            r'\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}'
        ]
        
        dates = []
        for pattern in date_patterns:
            found = re.findall(pattern, content, re.IGNORECASE)
            dates.extend(found)
        
        converted_dates = []
        for d in dates:
            try:
                for fmt in ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d', '%d/%m/%y', '%d-%m-%y']:
                    try:
                        date_obj = datetime.strptime(d, fmt)
                        converted_dates.append(date_obj)
                        break
                    except:
                        continue
                else:
                    converted_dates.append(d)
            except:
                converted_dates.append(d)
        
        return converted_dates
    
    @staticmethod
    def _extract_characters(content: str) -> List[str]:
        """Extraer caracteres individuales (excluyendo espacios)"""
        return [c for c in content if c.strip() and not c.isspace()]
    
    @staticmethod
    def _extract_all_elements(content: str) -> List[str]:
        """Extraer todos los elementos (separados por espacios, comas, etc.)"""
        return re.findall(r'[^\s,;:!?¡¿()\[\]{}/\\<>]+', content)
    
    @staticmethod
    def get_statistics(data: List[Any], data_type: str) -> dict:
        """Obtener estadísticas según el tipo de dato"""
        stats = {
            "total": len(data),
            "unicos": len(set(str(x) for x in data))
        }
        
        if data_type == DataProcessor.TIPO_NUMEROS and data:
            numeric_data = [x for x in data if isinstance(x, (int, float))]
            if numeric_data:
                stats.update({
                    "minimo": min(numeric_data),
                    "maximo": max(numeric_data),
                    "suma": sum(numeric_data),
                    "promedio": sum(numeric_data) / len(numeric_data)
                })
        
        elif data_type == DataProcessor.TIPO_PALABRAS and data:
            palabras = [str(x) for x in data]
            if palabras:
                stats.update({
                    "palabra_mas_larga": max(palabras, key=len),
                    "longitud_promedio": sum(len(p) for p in palabras) / len(palabras)
                })
        
        elif data_type == DataProcessor.TIPO_LINEAS and data:
            lineas = [str(x) for x in data]
            stats.update({
                "caracteres_totales": sum(len(l) for l in lineas),
                "linea_mas_larga": max(lineas, key=len) if lineas else ""
            })
        
        return stats
    
    @staticmethod
    def compare_archives(data1: List[Any], data2: List[Any], data_type: str) -> dict:
        """Comparar dos conjuntos de datos"""
        if data_type == DataProcessor.TIPO_NUMEROS:
            set1 = set(data1)
            set2 = set(data2)
        else:
            set1 = set(str(x) for x in data1)
            set2 = set(str(x) for x in data2)
        
        comunes = set1 & set2
        solo1 = set1 - set2
        solo2 = set2 - set1
        
        return {
            "archivo1": {
                "elementos": len(data1),
                "unicos": len(set1)
            },
            "archivo2": {
                "elementos": len(data2),
                "unicos": len(set2)
            },
            "comparacion": {
                "comunes": len(comunes),
                "solo_archivo1": len(solo1),
                "solo_archivo2": len(solo2),
                "similitud": (len(comunes) / max(len(set1), len(set2)) * 100) if max(len(set1), len(set2)) > 0 else 0,
                "valores_comunes": sorted(list(comunes))[:50],
                "valores_solo1": sorted(list(solo1))[:50],
                "valores_solo2": sorted(list(solo2))[:50]
            }
        }
    
    @staticmethod
    def compare_elements(a: Any, b: Any, data_type: str) -> int:
        """Comparar dos elementos según el tipo de dato"""
        if data_type == DataProcessor.TIPO_NUMEROS:
            if a < b:
                return -1
            elif a > b:
                return 1
            return 0
        elif data_type == DataProcessor.TIPO_FECHAS:
            if hasattr(a, '__lt__') and hasattr(b, '__lt__'):
                if a < b:
                    return -1
                elif a > b:
                    return 1
                return 0
        else:
            str_a = str(a).lower()
            str_b = str(b).lower()
            if str_a < str_b:
                return -1
            elif str_a > str_b:
                return 1
            return 0