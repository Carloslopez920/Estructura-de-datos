import numpy as np
import pandas as pd
from datetime import datetime
import os

class SistemaVentas:
    def __init__(self):
        self.matriz = None
        self.departamentos = []
        self.meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                     "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        self.n_departamentos = 0
        
    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_titulo(self, titulo):
        """Muestra un título formateado"""
        print("\n" + "=" * 60)
        print(f"{titulo:^60}")
        print("=" * 60)
    
    def crear_matriz(self):
        """Crea una nueva matriz de ventas"""
        self.limpiar_pantalla()
        self.mostrar_titulo("CREAR NUEVA MATRIZ DE VENTAS")
        
        # Solicitar cantidad de departamentos
        while True:
            try:
                self.n_departamentos = int(input("\nIngrese el número de departamentos: "))
                if self.n_departamentos > 0:
                    break
                else:
                    print("❌ Por favor ingrese un número positivo.")
            except ValueError:
                print("❌ Por favor ingrese un número válido.")
        
        # Solicitar nombres de departamentos
        self.departamentos = []
        print("\nIngrese los nombres de los departamentos:")
        for i in range(self.n_departamentos):
            while True:
                nombre = input(f"Departamento {i+1}: ").strip()
                if nombre:
                    self.departamentos.append(nombre)
                    break
                else:
                    print("❌ El nombre no puede estar vacío.")
        
        # Crear matriz inicial con ceros
        self.matriz = np.zeros((self.n_departamentos, 12), dtype=float)
        
        print(f"\n✅ Matriz creada: {self.n_departamentos} departamentos x 12 meses")
        input("\nPresione Enter para continuar...")
    
    def ingresar_datos(self):
        """Ingresa o modifica datos en la matriz"""
        if self.matriz is None:
            print("❌ Primero debe crear una matriz.")
            input("\nPresione Enter para continuar...")
            return
        
        self.limpiar_pantalla()
        self.mostrar_titulo("INGRESAR/MODIFICAR DATOS DE VENTAS")
        
        # Mostrar departamentos
        print("\n📋 Departamentos disponibles:")
        for i, depto in enumerate(self.departamentos):
            print(f"{i+1}. {depto}")
        
        # Seleccionar departamento
        while True:
            try:
                depto_idx = int(input(f"\nSeleccione departamento (1-{self.n_departamentos}): ")) - 1
                if 0 <= depto_idx < self.n_departamentos:
                    break
                else:
                    print(f"❌ Seleccione entre 1 y {self.n_departamentos}")
            except ValueError:
                print("❌ Ingrese un número válido.")
        
        # Mostrar meses
        print("\n📅 Meses disponibles:")
        for i, mes in enumerate(self.meses):
            print(f"{i+1}. {mes}: ${self.matriz[depto_idx, i]:,.2f}")
        
        # Seleccionar mes
        while True:
            try:
                mes_idx = int(input(f"\nSeleccione mes (1-12): ")) - 1
                if 0 <= mes_idx < 12:
                    break
                else:
                    print("❌ Seleccione entre 1 y 12")
            except ValueError:
                print("❌ Ingrese un número válido.")
        
        # Ingresar nuevo valor
        print(f"\n📊 Editando: {self.departamentos[depto_idx]} - {self.meses[mes_idx]}")
        print(f"Valor actual: ${self.matriz[depto_idx, mes_idx]:,.2f}")
        
        while True:
            try:
                nuevo_valor = float(input("Nuevo valor de ventas: $"))
                if nuevo_valor >= 0:
                    self.matriz[depto_idx, mes_idx] = nuevo_valor
                    print(f"✅ Valor actualizado: ${nuevo_valor:,.2f}")
                    break
                else:
                    print("❌ El valor no puede ser negativo.")
            except ValueError:
                print("❌ Ingrese un número válido.")
        
        input("\nPresione Enter para continuar...")
    
    def buscar_elemento(self):
        """Busca un elemento en la matriz por valor o departamento"""
        if self.matriz is None:
            print("❌ Primero debe crear una matriz.")
            input("\nPresione Enter para continuar...")
            return
        
        self.limpiar_pantalla()
        self.mostrar_titulo("BUSCAR ELEMENTO")
        
        print("\n🔍 Opciones de búsqueda:")
        print("1. Buscar por valor específico")
        print("2. Buscar por rango de valores")
        print("3. Buscar por departamento")
        print("4. Buscar por mes")
        
        while True:
            try:
                opcion = int(input("\nSeleccione opción (1-4): "))
                if 1 <= opcion <= 4:
                    break
                else:
                    print("❌ Seleccione entre 1 y 4")
            except ValueError:
                print("❌ Ingrese un número válido.")
        
        resultados = []
        
        if opcion == 1:  # Buscar por valor
            try:
                valor = float(input("\nIngrese el valor a buscar: $"))
                for i in range(self.n_departamentos):
                    for j in range(12):
                        if self.matriz[i, j] == valor:
                            resultados.append((i, j, valor))
            except ValueError:
                print("❌ Valor inválido")
                
        elif opcion == 2:  # Buscar por rango
            try:
                min_val = float(input("Valor mínimo: $"))
                max_val = float(input("Valor máximo: $"))
                
                for i in range(self.n_departamentos):
                    for j in range(12):
                        if min_val <= self.matriz[i, j] <= max_val:
                            resultados.append((i, j, self.matriz[i, j]))
            except ValueError:
                print("❌ Valores inválidos")
                
        elif opcion == 3:  # Buscar por departamento
            print("\nDepartamentos disponibles:")
            for idx, depto in enumerate(self.departamentos):
                print(f"{idx+1}. {depto}")
            
            try:
                depto_idx = int(input("\nSeleccione departamento: ")) - 1
                if 0 <= depto_idx < self.n_departamentos:
                    for j in range(12):
                        resultados.append((depto_idx, j, self.matriz[depto_idx, j]))
                else:
                    print("❌ Departamento inválido")
            except ValueError:
                print("❌ Ingrese un número válido")
                
        elif opcion == 4:  # Buscar por mes
            print("\nMeses disponibles:")
            for idx, mes in enumerate(self.meses):
                print(f"{idx+1}. {mes}")
            
            try:
                mes_idx = int(input("\nSeleccione mes: ")) - 1
                if 0 <= mes_idx < 12:
                    for i in range(self.n_departamentos):
                        resultados.append((i, mes_idx, self.matriz[i, mes_idx]))
                else:
                    print("❌ Mes inválido")
            except ValueError:
                print("❌ Ingrese un número válido")
        
        # Mostrar resultados
        if resultados:
            print(f"\n📊 Se encontraron {len(resultados)} resultado(s):")
            print("-" * 60)
            print(f"{'Departamento':<20} {'Mes':<15} {'Valor':<15}")
            print("-" * 60)
            
            for i, j, valor in resultados:
                print(f"{self.departamentos[i]:<20} {self.meses[j]:<15} ${valor:,.2f}")
        else:
            print("\n🔍 No se encontraron resultados.")
        
        input("\nPresione Enter para continuar...")
    
    def eliminar_elemento(self):
        """Elimina (pone en cero) un elemento específico"""
        if self.matriz is None:
            print("❌ Primero debe crear una matriz.")
            input("\nPresione Enter para continuar...")
            return
        
        self.limpiar_pantalla()
        self.mostrar_titulo("ELIMINAR ELEMENTO")
        
        # Mostrar matriz actual
        self.mostrar_matriz_simple()
        
        print("\n⚠️  La eliminación pondrá el valor en $0.00")
        
        # Seleccionar departamento
        while True:
            try:
                depto_idx = int(input(f"\nSeleccione departamento (1-{self.n_departamentos}): ")) - 1
                if 0 <= depto_idx < self.n_departamentos:
                    break
                else:
                    print(f"❌ Seleccione entre 1 y {self.n_departamentos}")
            except ValueError:
                print("❌ Ingrese un número válido.")
        
        # Seleccionar mes
        while True:
            try:
                mes_idx = int(input(f"Seleccione mes (1-12): ")) - 1
                if 0 <= mes_idx < 12:
                    break
                else:
                    print("❌ Seleccione entre 1 y 12")
            except ValueError:
                print("❌ Ingrese un número válido.")
        
        # Confirmar eliminación
        print(f"\n📊 Elemento seleccionado:")
        print(f"Departamento: {self.departamentos[depto_idx]}")
        print(f"Mes: {self.meses[mes_idx]}")
        print(f"Valor actual: ${self.matriz[depto_idx, mes_idx]:,.2f}")
        
        confirmar = input("\n¿Está seguro de eliminar este valor? (s/n): ").lower()
        
        if confirmar == 's':
            valor_anterior = self.matriz[depto_idx, mes_idx]
            self.matriz[depto_idx, mes_idx] = 0.0
            print(f"✅ Valor eliminado (${valor_anterior:,.2f} → $0.00)")
        else:
            print("❌ Eliminación cancelada")
        
        input("\nPresione Enter para continuar...")
    
    def mostrar_matriz_simple(self):
        """Muestra la matriz en formato simple"""
        if self.matriz is None:
            print("❌ No hay matriz creada.")
            return
        
        print("\n" + "-" * 80)
        print(f"{'MATRIZ DE VENTAS':^80}")
        print("-" * 80)
        
        # Encabezado de meses
        print(f"{'Departamento':<20}", end="")
        for mes in self.meses:
            print(f"{mes[:5]:>8}", end="")
        print(f"{'Total':>10}")
        print("-" * 80)
        
        # Filas de departamentos
        for i in range(self.n_departamentos):
            print(f"{self.departamentos[i]:<20}", end="")
            total_depto = 0
            for j in range(12):
                print(f"{self.matriz[i, j]:8,.0f}", end="")
                total_depto += self.matriz[i, j]
            print(f"{total_depto:10,.0f}")
        
        # Totales por mes
        print("-" * 80)
        print(f"{'Total Mes':<20}", end="")
        for j in range(12):
            total_mes = np.sum(self.matriz[:, j])
            print(f"{total_mes:8,.0f}", end="")
        
        total_general = np.sum(self.matriz)
        print(f"{total_general:10,.0f}")
        print("-" * 80)
    
    def mostrar_matriz_completa(self):
        """Muestra la matriz con todos los detalles"""
        if self.matriz is None:
            print("❌ Primero debe crear una matriz.")
            input("\nPresione Enter para continuar...")
            return
        
        self.limpiar_pantalla()
        self.mostrar_titulo("MATRIZ COMPLETA DE VENTAS")
        
        # Crear DataFrame para mejor visualización
        df = pd.DataFrame(self.matriz, 
                         index=self.departamentos, 
                         columns=self.meses)
        
        # Agregar total anual por departamento
        df['Total Anual'] = df.sum(axis=1)
        
        # Agregar total mensual
        df.loc['Total Mensual'] = df.sum(axis=0)
        df.loc['Total Mensual', 'Total Anual'] = df['Total Anual'].sum()
        
        # Mostrar DataFrame
        pd.set_option('display.float_format', '{:,.2f}'.format)
        pd.set_option('display.width', None)
        pd.set_option('display.max_columns', None)
        
        print("\n" + df.to_string())
        
        # Estadísticas adicionales
        print("\n" + "=" * 60)
        print("ESTADÍSTICAS GENERALES")
        print("=" * 60)
        
        if self.n_departamentos > 0:
            # Promedios
            promedio_general = np.mean(self.matriz)
            print(f"\n📈 Promedio general de ventas: ${promedio_general:,.2f}")
            
            # Mejor departamento
            totales_depto = np.sum(self.matriz, axis=1)
            mejor_depto_idx = np.argmax(totales_depto)
            peor_depto_idx = np.argmin(totales_depto)
            
            print(f"\n🏆 Mejor departamento: {self.departamentos[mejor_depto_idx]}")
            print(f"   Total anual: ${totales_depto[mejor_depto_idx]:,.2f}")
            
            print(f"\n📉 Peor departamento: {self.departamentos[peor_depto_idx]}")
            print(f"   Total anual: ${totales_depto[peor_depto_idx]:,.2f}")
            
            # Mejor mes global
            totales_mes = np.sum(self.matriz, axis=0)
            mejor_mes_idx = np.argmax(totales_mes)
            peor_mes_idx = np.argmin(totales_mes)
            
            print(f"\n📊 Mejor mes: {self.meses[mejor_mes_idx]}")
            print(f"   Ventas totales: ${totales_mes[mejor_mes_idx]:,.2f}")
            
            print(f"\n📊 Peor mes: {self.meses[peor_mes_idx]}")
            print(f"   Ventas totales: ${totales_mes[peor_mes_idx]:,.2f}")
        
        input("\nPresione Enter para continuar...")
    
    def generar_datos_aleatorios(self):
        """Genera datos aleatorios para la matriz"""
        if self.matriz is None:
            print("❌ Primero debe crear una matriz.")
            input("\nPresione Enter para continuar...")
            return
        
        self.limpiar_pantalla()
        self.mostrar_titulo("GENERAR DATOS ALEATORIOS")
        
        print("\n⚠️  Esto sobrescribirá todos los datos actuales")
        confirmar = input("¿Continuar? (s/n): ").lower()
        
        if confirmar == 's':
            for i in range(self.n_departamentos):
                for j in range(12):
                    # Generar valores entre 1000 y 50000
                    self.matriz[i, j] = round(np.random.uniform(1000, 50000), 2)
            print("✅ Datos aleatorios generados exitosamente")
        else:
            print("❌ Operación cancelada")
        
        input("\nPresione Enter para continuar...")
    
    def exportar_excel(self):
        """Exporta la matriz a Excel"""
        if self.matriz is None:
            print("❌ Primero debe crear una matriz.")
            input("\nPresione Enter para continuar...")
            return
        
        try:
            # Crear DataFrame
            df = pd.DataFrame(self.matriz, 
                            index=self.departamentos, 
                            columns=self.meses)
            
            # Agregar totales
            df['Total Anual'] = df.sum(axis=1)
            df.loc['Total Mensual'] = df.sum(axis=0)
            
            # Nombre de archivo con fecha
            fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
            archivo_excel = f"ventas_{fecha}.xlsx"
            archivo_csv = f"ventas_{fecha}.csv"
            
            # Exportar
            df.to_excel(archivo_excel, sheet_name='Ventas')
            df.to_csv(archivo_csv)
            
            print(f"\n✅ Exportación exitosa:")
            print(f"📁 Excel: {archivo_excel}")
            print(f"📁 CSV: {archivo_csv}")
            
        except Exception as e:
            print(f"❌ Error al exportar: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def mostrar_menu(self):
        """Muestra el menú principal"""
        self.limpiar_pantalla()
        self.mostrar_titulo("SISTEMA DE GESTIÓN DE VENTAS")
        
        print(f"\n📊 Estado actual: ", end="")
        if self.matriz is not None:
            print(f"{self.n_departamentos} departamentos cargados")
        else:
            print("Sin matriz creada")
        
        print("\n" + "═" * 40)
        print("📋 MENÚ PRINCIPAL")
        print("═" * 40)
        print("1. Crear nueva matriz")
        print("2. Ingresar/Modificar datos")
        print("3. Buscar elemento")
        print("4. Eliminar elemento")
        print("5. Ver matriz completa")
        print("6. Ver resumen simple")
        print("7. Generar datos aleatorios")
        print("8. Exportar a Excel/CSV")
        print("0. Salir")
        print("═" * 40)
    
    def ejecutar(self):
        """Ejecuta el sistema principal"""
        while True:
            self.mostrar_menu()
            
            try:
                opcion = int(input("\nSeleccione una opción: "))
                
                if opcion == 0:
                    print("\n👋 ¡Gracias por usar el sistema!")
                    break
                
                elif opcion == 1:
                    self.crear_matriz()
                elif opcion == 2:
                    self.ingresar_datos()
                elif opcion == 3:
                    self.buscar_elemento()
                elif opcion == 4:
                    self.eliminar_elemento()
                elif opcion == 5:
                    self.mostrar_matriz_completa()
                elif opcion == 6:
                    self.limpiar_pantalla()
                    self.mostrar_titulo("RESUMEN SIMPLE")
                    self.mostrar_matriz_simple()
                    input("\nPresione Enter para continuar...")
                elif opcion == 7:
                    self.generar_datos_aleatorios()
                elif opcion == 8:
                    self.exportar_excel()
                else:
                    print("❌ Opción no válida. Intente nuevamente.")
                    input("\nPresione Enter para continuar...")
                    
            except ValueError:
                print("❌ Ingrese un número válido.")
                input("\nPresione Enter para continuar...")
            except KeyboardInterrupt:
                print("\n\n⚠️  Operación cancelada por el usuario")
                input("\nPresione Enter para continuar...")

# Versión simplificada si prefieres algo más básico
def sistema_simplificado():
    """Versión simplificada del sistema"""
    
    def crear_matriz_simple():
        n = int(input("Número de departamentos: "))
        departamentos = [input(f"Nombre departamento {i+1}: ") for i in range(n)]
        
        meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", 
                "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        
        matriz = np.zeros((n, 12))
        
        # Llenar datos
        for i in range(n):
            print(f"\n📊 {departamentos[i]}:")
            for j in range(12):
                while True:
                    try:
                        valor = float(input(f"  {meses[j]}: $"))
                        matriz[i, j] = valor
                        break
                    except:
                        print("Valor inválido")
        
        return matriz, departamentos, meses
    
    print("\n" + "=" * 50)
    print("SISTEMA SIMPLIFICADO DE VENTAS")
    print("=" * 50)
    
    matriz, deptos, meses = crear_matriz_simple()
    
    while True:
        print("\nOpciones:")
        print("1. Ver matriz")
        print("2. Modificar valor")
        print("3. Buscar")
        print("4. Eliminar valor")
        print("5. Salir")
        
        op = input("Seleccione: ")
        
        if op == '1':
            # Mostrar matriz
            print("\nMatriz de ventas:")
            for i in range(len(deptos)):
                print(f"\n{deptos[i]}:")
                for j in range(12):
                    print(f"  {meses[j]}: ${matriz[i, j]:,.2f}")
        
        elif op == '2':
            # Modificar
            print("\nDepartamentos:")
            for idx, d in enumerate(deptos):
                print(f"{idx+1}. {d}")
            
            d_idx = int(input("Departamento: ")) - 1
            m_idx = int(input("Mes (1-12): ")) - 1
            nuevo = float(input("Nuevo valor: $"))
            matriz[d_idx, m_idx] = nuevo
            print("✅ Actualizado")
        
        elif op == '3':
            # Buscar
            valor = float(input("Valor a buscar: $"))
            print(f"\nResultados para ${valor}:")
            for i in range(len(deptos)):
                for j in range(12):
                    if matriz[i, j] == valor:
                        print(f"  {deptos[i]} - {meses[j]}")
        
        elif op == '4':
            # Eliminar (poner en cero)
            d_idx = int(input("Departamento: ")) - 1
            m_idx = int(input("Mes (1-12): ")) - 1
            matriz[d_idx, m_idx] = 0
            print("✅ Eliminado (valor en $0)")
        
        elif op == '5':
            print("¡Adiós!")
            break

# Programa principal
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("SISTEMA DE GESTIÓN DE VENTAS POR DEPARTAMENTOS")
    print("=" * 60)
    print("Desarrollado para Ingeniería de Sistemas")
    print("Versión 2.0 - Con CRUD completo\n")
    
    print("Seleccione el modo:")
    print("1. Sistema completo con interfaz mejorada")
    print("2. Versión simplificada")
    
    try:
        modo = input("Opción (1-2): ").strip()
        
        if modo == '1':
            sistema = SistemaVentas()
            sistema.ejecutar()
        elif modo == '2':
            sistema_simplificado()
        else:
            print("Opción inválida. Usando sistema completo...")
            sistema = SistemaVentas()
            sistema.ejecutar()
            
    except KeyboardInterrupt:
        print("\n\nPrograma terminado por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")