import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations
import heapq

# Definir los 7 estados y sus conexiones con costos
estados = {
    "CDMX": 0,
    "EdoMex": 1,
    "Morelos": 2,
    "Puebla": 3,
    "Hidalgo": 4,
    "Queretaro": 5,
    "Tlaxcala": 6
}

# Lista de nombres de estados para fácil acceso
nombres_estados = list(estados.keys())

# Matriz de adyacencia con costos (inicializar con infinito)
n = len(estados)
INF = float('inf')
costos = [[INF] * n for _ in range(n)]

# Llenar conexiones
def agregar_conexion(estado1, estado2, costo):
    i, j = estados[estado1], estados[estado2]
    costos[i][j] = costo
    costos[j][i] = costo

# ==============================================
# NUEVO DISEÑO DE GRAFO - SIN CONEXIÓN DIRECTA ENTRE EDOMEX Y CDMX
# La única ruta de EdoMex a CDMX es pasando por Morelos
# ==============================================

# Conexiones principales (estructura de anillo con algunas diagonales)
agregar_conexion("CDMX", "Morelos", 85)        # CDMX conecta directo con Morelos
agregar_conexion("CDMX", "Puebla", 130)        # CDMX conecta directo con Puebla
agregar_conexion("Morelos", "EdoMex", 100)     # Morelos conecta con EdoMex
agregar_conexion("EdoMex", "Hidalgo", 110)     # EdoMex conecta con Hidalgo
agregar_conexion("EdoMex", "Queretaro", 210)   # EdoMex conecta con Queretaro
agregar_conexion("Morelos", "Puebla", 150)     # Morelos conecta con Puebla
agregar_conexion("Puebla", "Tlaxcala", 50)     # Puebla conecta con Tlaxcala
agregar_conexion("Tlaxcala", "Hidalgo", 110)   # Tlaxcala conecta con Hidalgo
agregar_conexion("Hidalgo", "Queretaro", 150)  # Hidalgo conecta con Queretaro

# IMPORTANTE: NO hay conexión directa entre EdoMex y CDMX
# Para ir de EdoMex a CDMX, la ruta es: EdoMex -> Morelos -> CDMX (costo: 100 + 85 = 185)

# Verificar que NO existe conexión directa EdoMex-CDMX
if costos[estados["EdoMex"]][estados["CDMX"]] == INF:
    print("✓ CONFIGURACIÓN CORRECTA: No hay conexión directa entre EdoMex y CDMX")
    print("  La única ruta de EdoMex a CDMX es: EdoMex -> Morelos -> CDMX (costo: 185)")
else:
    print("✗ ERROR: Aún existe conexión directa")

# Algoritmo de Dijkstra para encontrar la ruta más corta entre dos nodos
def dijkstra(origen, destino):
    """Encuentra la ruta más corta y su costo entre origen y destino"""
    distancias = [INF] * n
    distancias[origen] = 0
    padres = [-1] * n
    padres[origen] = origen
    pq = [(0, origen)]
    
    while pq:
        dist_actual, actual = heapq.heappop(pq)
        
        if dist_actual > distancias[actual]:
            continue
        
        if actual == destino:
            break
        
        for vecino in range(n):
            if costos[actual][vecino] != INF:
                nueva_dist = dist_actual + costos[actual][vecino]
                if nueva_dist < distancias[vecino]:
                    distancias[vecino] = nueva_dist
                    padres[vecino] = actual
                    heapq.heappush(pq, (nueva_dist, vecino))
    
    # Reconstruir la ruta
    if distancias[destino] == INF:
        return None, INF
    
    ruta = []
    actual = destino
    while actual != origen:
        ruta.append(actual)
        actual = padres[actual]
    ruta.append(origen)
    ruta.reverse()
    
    return ruta, distancias[destino]

# Función para calcular costo de un camino, usando rutas más cortas cuando no hay conexión directa
def costo_camino_con_alternativas_sin_repeticion(camino_indices):
    """Calcula el costo total de un camino, sin permitir repetición de estados en la ruta detallada"""
    costo_total = 0
    ruta_completa = []
    visitados_en_ruta = set()
    
    for i in range(len(camino_indices) - 1):
        origen = camino_indices[i]
        destino = camino_indices[i+1]
        
        # Si hay conexión directa, usarla
        if costos[origen][destino] != INF:
            costo_total += costos[origen][destino]
            if i == 0:
                if nombres_estados[origen] not in visitados_en_ruta:
                    ruta_completa.append(nombres_estados[origen])
                    visitados_en_ruta.add(nombres_estados[origen])
            if nombres_estados[destino] not in visitados_en_ruta:
                ruta_completa.append(nombres_estados[destino])
                visitados_en_ruta.add(nombres_estados[destino])
            else:
                return None, INF
        else:
            # Buscar ruta alternativa más corta (usando Dijkstra)
            ruta_alt, costo_alt = dijkstra(origen, destino)
            if ruta_alt is None:
                return None, INF
            costo_total += costo_alt
            # Agregar la ruta alternativa
            if i == 0:
                if nombres_estados[ruta_alt[0]] not in visitados_en_ruta:
                    ruta_completa.append(nombres_estados[ruta_alt[0]])
                    visitados_en_ruta.add(nombres_estados[ruta_alt[0]])
            for idx in range(1, len(ruta_alt)):
                estado_alt = nombres_estados[ruta_alt[idx]]
                if estado_alt in visitados_en_ruta:
                    return None, INF
                ruta_completa.append(estado_alt)
                visitados_en_ruta.add(estado_alt)
    
    return ruta_completa, costo_total

def costo_camino_con_alternativas_con_repeticion(camino_indices):
    """Calcula el costo total de un camino, permitiendo repetición de estados"""
    costo_total = 0
    ruta_completa = []
    
    for i in range(len(camino_indices) - 1):
        origen = camino_indices[i]
        destino = camino_indices[i+1]
        
        if costos[origen][destino] != INF:
            costo_total += costos[origen][destino]
            if i == 0:
                ruta_completa.append(nombres_estados[origen])
            ruta_completa.append(nombres_estados[destino])
        else:
            ruta_alt, costo_alt = dijkstra(origen, destino)
            if ruta_alt is None:
                return None, INF
            costo_total += costo_alt
            if i == 0:
                ruta_completa.append(nombres_estados[ruta_alt[0]])
            for idx in range(1, len(ruta_alt)):
                ruta_completa.append(nombres_estados[ruta_alt[idx]])
    
    return ruta_completa, costo_total

def mejor_camino_hamiltoniano(estados_seleccionados):
    indices_seleccionados = [estados[estado] for estado in estados_seleccionados]
    m = len(indices_seleccionados)
    
    if m == 0:
        return None, 0, None
    
    if m == 1:
        return indices_seleccionados, 0, [nombres_estados[indices_seleccionados[0]]]
    
    mejor_costo = INF
    mejor_ruta = None
    mejor_ruta_detallada = None
    
    for perm in permutations(indices_seleccionados):
        ruta_detallada, costo = costo_camino_con_alternativas_sin_repeticion(perm)
        if costo is not None and costo < mejor_costo:
            mejor_costo = costo
            mejor_ruta = perm
            mejor_ruta_detallada = ruta_detallada
    
    return mejor_ruta, mejor_costo, mejor_ruta_detallada

def recorrido_con_repeticion(estados_seleccionados):
    indices_seleccionados = [estados[estado] for estado in estados_seleccionados]
    m = len(indices_seleccionados)
    
    if m == 0:
        return None, 0, None
    
    if m == 1:
        idx = indices_seleccionados[0]
        mejor_costo = INF
        mejor_ruta = None
        mejor_ruta_detallada = None
        
        for vecino in range(n):
            if costos[idx][vecino] != INF:
                ruta = [idx, vecino, idx]
                ruta_detallada, costo = costo_camino_con_alternativas_con_repeticion(ruta)
                if costo is not None and costo < mejor_costo:
                    mejor_costo = costo
                    mejor_ruta = ruta
                    mejor_ruta_detallada = ruta_detallada
        return mejor_ruta, mejor_costo, mejor_ruta_detallada
    
    ruta_ham, costo_ham, ruta_det_ham = mejor_camino_hamiltoniano(estados_seleccionados)
    
    if costo_ham == INF:
        return None, INF, None
    
    ruta_repetida = list(ruta_ham) + [ruta_ham[0]]
    ruta_det_rep, costo_rep = costo_camino_con_alternativas_con_repeticion(ruta_repetida)
    
    mejor_costo_rep = costo_rep if costo_rep is not None else INF
    mejor_ruta_rep = ruta_repetida if costo_rep is not None else None
    mejor_ruta_det_rep = ruta_det_rep
    
    for i in range(len(ruta_ham)):
        for j in range(i + 1, len(ruta_ham)):
            if ruta_ham[i] == ruta_ham[j]:
                continue
            ruta_try = list(ruta_ham[:j+1]) + [ruta_ham[i]] + list(ruta_ham[j+1:])
            ruta_det_try, costo_try = costo_camino_con_alternativas_con_repeticion(ruta_try)
            if costo_try is not None and costo_try < mejor_costo_rep:
                mejor_costo_rep = costo_try
                mejor_ruta_rep = ruta_try
                mejor_ruta_det_rep = ruta_det_try
    
    return mejor_ruta_rep, mejor_costo_rep, mejor_ruta_det_rep

def mostrar_resultados(estados_sel, ruta_indices, costo, ruta_detallada, tipo_inciso):
    if ruta_indices is None or costo == INF or costo is None:
        print(f"\n--- {tipo_inciso} ---")
        print(f"No se encontró un recorrido válido para los estados: {', '.join(estados_sel)}")
        return None
    
    ruta_simplificada = [nombres_estados[i] for i in ruta_indices]
    
    print(f"\n--- {tipo_inciso} ---")
    print(f"Estados objetivo: {', '.join(estados_sel)}")
    print(f"\nRuta SIMPLIFICADA (solo estados objetivo):")
    print(f"{' -> '.join(ruta_simplificada)}")
    
    print(f"\nRuta DETALLADA (incluyendo escalas intermedias):")
    print(f"{' -> '.join(ruta_detallada)}")
    
    print(f"\nCosto total del recorrido: {costo}")
    print(f"Total de paradas (incluyendo escalas): {len(ruta_detallada)}")
    
    repeticiones = len(ruta_detallada) - len(set(ruta_detallada))
    if repeticiones > 0 and "sin repetir" in tipo_inciso.lower():
        print(f"\n⚠️ ADVERTENCIA: La ruta contiene {repeticiones} repeticiones de estados")
    elif repeticiones > 0:
        print(f"\n✓ La ruta contiene {repeticiones} repeticiones de estados (permitido para este inciso)")
    else:
        print(f"\n✓ No hay repeticiones de estados en la ruta")
    
    print("\n=== DESGLOSE DEL RECORRIDO DETALLADO ===")
    costo_acumulado = 0
    for i in range(len(ruta_detallada) - 1):
        origen = ruta_detallada[i]
        destino = ruta_detallada[i+1]
        costo_seg = costos[estados[origen]][estados[destino]]
        if costo_seg == INF:
            print(f"  {origen} -> {destino}: Usando ruta alternativa (incluida en detalles)")
        else:
            costo_acumulado += costo_seg
            print(f"  {origen} -> {destino}: {costo_seg} (Acumulado: {costo_acumulado})")
    
    return ruta_detallada

def dibujar_grafo_con_ruta_numerada(ruta_detallada=None, titulo="Grafo de Estados Mexicanos"):
    G = nx.Graph()
    
    # Agregar nodos
    for estado in estados:
        G.add_node(estado)
    
    # Agregar aristas con pesos
    for i in range(n):
        for j in range(i + 1, n):
            if costos[i][j] != INF:
                G.add_edge(nombres_estados[i], nombres_estados[j], weight=costos[i][j])
    
    # Posiciones fijas para mostrar claramente la estructura
    # Colocamos EdoMex y CDMX separados, con Morelos en medio
    pos = {
        "CDMX": (0, 1),
        "Morelos": (0, 0),
        "EdoMex": (0, -1),
        "Puebla": (2, 0.5),
        "Tlaxcala": (3, 0),
        "Hidalgo": (1, -1.5),
        "Queretaro": (-1, -1.5)
    }
    
    # Dibujar todos los nodos
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1500)
    
    # Dibujar todas las aristas (gris claro)
    nx.draw_networkx_edges(G, pos, edge_color='gray', width=1, alpha=0.3)
    
    # Dibujar etiquetas de pesos
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)
    
    # Si hay una ruta, dibujarla con números de orden
    if ruta_detallada and len(ruta_detallada) > 1:
        aristas_ruta = []
        for i in range(len(ruta_detallada) - 1):
            aristas_ruta.append((ruta_detallada[i], ruta_detallada[i+1]))
        
        nx.draw_networkx_edges(G, pos, edgelist=aristas_ruta, 
                               edge_color='red', width=3, style='solid')
        
        nx.draw_networkx_nodes(G, pos, nodelist=ruta_detallada, 
                               node_color='orange', node_size=1800)
        
        if len(ruta_detallada) > 0:
            nx.draw_networkx_nodes(G, pos, nodelist=[ruta_detallada[0]], 
                                   node_color='green', node_size=2000, 
                                   node_shape='s')
            nx.draw_networkx_nodes(G, pos, nodelist=[ruta_detallada[-1]], 
                                   node_color='red', node_size=2000,
                                   node_shape='d')
        
        for idx, nodo in enumerate(ruta_detallada):
            x, y = pos[nodo]
            plt.text(x, y + 0.15, f"{idx+1}", 
                    fontsize=10, fontweight='bold', ha='center', va='center',
                    bbox=dict(boxstyle="circle", facecolor='white', edgecolor='black', alpha=0.9))
    
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    
    plt.title(titulo, fontsize=14)
    plt.axis('off')
    
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='red', linewidth=3, label='Ruta del recorrido'),
        Patch(facecolor='orange', edgecolor='black', label='Estados visitados'),
        Patch(facecolor='green', edgecolor='black', label='Inicio'),
        Patch(facecolor='red', edgecolor='black', label='Fin'),
        Patch(facecolor='lightblue', edgecolor='black', label='Otros estados'),
        Patch(facecolor='white', edgecolor='black', label='Números = orden de visita')
    ]
    plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1))
    
    if ruta_detallada and len(ruta_detallada) > 1:
        ruta_texto = " → ".join([f"{i+1}.{n}" for i, n in enumerate(ruta_detallada)])
        plt.figtext(0.5, 0.02, f"Orden de visita: {ruta_texto}", 
                   wrap=True, horizontalalignment='center', fontsize=9,
                   bbox=dict(boxstyle="round", facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.show()

def menu_personalizado():
    print("\n" + "=" * 60)
    print("MODO PERSONALIZADO")
    print("=" * 60)
    
    print("\nEstados disponibles:")
    for i, estado in enumerate(nombres_estados, 1):
        print(f"  {i}. {estado}")
    
    print("\nIngrese los números de los estados que desea recorrer (separados por comas)")
    print("Ejemplo: 1,3,5")
    seleccion = input("Su selección: ").strip()
    
    try:
        indices = [int(x.strip()) - 1 for x in seleccion.split(',')]
        estados_sel = [nombres_estados[i] for i in indices if 0 <= i < len(nombres_estados)]
        if not estados_sel:
            print("Selección inválida. Se usarán todos los estados.")
            estados_sel = nombres_estados.copy()
    except:
        print("Formato inválido. Se usarán todos los estados.")
        estados_sel = nombres_estados.copy()
    
    print(f"\nEstados seleccionados: {', '.join(estados_sel)}")
    
    print("\n¿Qué tipo de recorrido desea?")
    print("  1. Sin repetir estados (recorrido único)")
    print("  2. Repitiendo al menos un estado")
    
    while True:
        tipo = input("Seleccione (1 o 2): ").strip()
        if tipo in ['1', '2']:
            break
        print("Opción inválida. Intente nuevamente.")
    
    return estados_sel, tipo

def ejecutar_inciso_a():
    print("\n" + "=" * 80)
    print("INCISO A: Recorrer los 7 estados SIN repetir")
    print("=" * 80)
    
    estados_completos = nombres_estados.copy()
    ruta_a, costo_a, ruta_det_a = mejor_camino_hamiltoniano(estados_completos)
    ruta_mostrar = mostrar_resultados(estados_completos, ruta_a, costo_a, ruta_det_a, "INCISO A - Sin repetir")
    
    ver_grafo = input("\n¿Desea ver el grafo con la ruta encontrada? (s/n): ").strip().lower()
    if ver_grafo == 's' and ruta_mostrar:
        dibujar_grafo_con_ruta_numerada(ruta_mostrar, "Inciso A - Ruta sin repetir (EdoMex→Morelos→CDMX obligatorio)")

def ejecutar_inciso_b():
    print("\n" + "=" * 80)
    print("INCISO B: Recorrer los 7 estados repitiendo al menos UNO")
    print("=" * 80)
    
    estados_completos = nombres_estados.copy()
    ruta_b, costo_b, ruta_det_b = recorrido_con_repeticion(estados_completos)
    ruta_mostrar = mostrar_resultados(estados_completos, ruta_b, costo_b, ruta_det_b, "INCISO B - Con repetición")
    
    ver_grafo = input("\n¿Desea ver el grafo con la ruta encontrada? (s/n): ").strip().lower()
    if ver_grafo == 's' and ruta_mostrar:
        dibujar_grafo_con_ruta_numerada(ruta_mostrar, "Inciso B - Ruta con repetición")

def ejecutar_personalizado():
    estados_sel, tipo = menu_personalizado()
    
    if tipo == '1':
        print("\n" + "=" * 80)
        print("MODO PERSONALIZADO - Sin repetir estados")
        print("=" * 80)
        ruta, costo, ruta_det = mejor_camino_hamiltoniano(estados_sel)
        ruta_mostrar = mostrar_resultados(estados_sel, ruta, costo, ruta_det, "PERSONALIZADO - Sin repetición")
    else:
        print("\n" + "=" * 80)
        print("MODO PERSONALIZADO - Repitiendo al menos un estado")
        print("=" * 80)
        ruta, costo, ruta_det = recorrido_con_repeticion(estados_sel)
        ruta_mostrar = mostrar_resultados(estados_sel, ruta, costo, ruta_det, "PERSONALIZADO - Con repetición")
    
    ver_grafo = input("\n¿Desea ver el grafo con la ruta encontrada? (s/n): ").strip().lower()
    if ver_grafo == 's' and ruta_mostrar:
        dibujar_grafo_con_ruta_numerada(ruta_mostrar, "Modo Personalizado - Ruta encontrada")

def main():
    print("=" * 80)
    print("PROGRAMA DE RECORRIDO DE ESTADOS MEXICANOS USANDO GRAFOS")
    print("=" * 80)
    
    # Mostrar información del nuevo diseño de grafo
    print("\n" + "=" * 60)
    print("NUEVA ESTRUCTURA DEL GRAFO:")
    print("=" * 60)
    print("✓ NO existe conexión directa entre EdoMex y CDMX")
    print("✓ La única ruta de EdoMex a CDMX es: EdoMex -> Morelos -> CDMX")
    print(f"  Costo: {costos[estados['EdoMex']][estados['Morelos']]} + {costos[estados['Morelos']][estados['CDMX']]} = 185")
    print("\nConexiones del grafo:")
    
    for i in range(n):
        for j in range(i + 1, n):
            if costos[i][j] != INF:
                print(f"  {nombres_estados[i]} <-> {nombres_estados[j]}: {costos[i][j]}")
    
    # Verificación adicional
    if costos[estados["EdoMex"]][estados["CDMX"]] == INF:
        print("\n✓ VERIFICADO: No hay conexión directa EdoMex-CDMX")
        ruta, costo = dijkstra(estados["EdoMex"], estados["CDMX"])
        if ruta:
            ruta_nombres = [nombres_estados[i] for i in ruta]
            print(f"  Ruta más corta EdoMex → CDMX: {' -> '.join(ruta_nombres)} (costo: {costo})")
    
    while True:
        print("\n" + "=" * 80)
        print("MENÚ PRINCIPAL")
        print("=" * 80)
        print("1. Inciso A - Recorrer TODOS los 7 estados SIN repetir")
        print("2. Inciso B - Recorrer TODOS los 7 estados repitiendo al menos UNO")
        print("3. Personalizado - Elegir qué estados y qué tipo de recorrido")
        print("4. Salir")
        print("-" * 80)
        
        opcion = input("Seleccione una opción (1-4): ").strip()
        
        if opcion == '1':
            ejecutar_inciso_a()
        elif opcion == '2':
            ejecutar_inciso_b()
        elif opcion == '3':
            ejecutar_personalizado()
        elif opcion == '4':
            print("\n¡Gracias por usar el programa! Hasta luego.")
            break
        else:
            print("\nOpción inválida. Por favor, seleccione 1, 2, 3 o 4.")
    
    ver_grafo_final = input("\n¿Desea ver el grafo general del sistema? (s/n): ").strip().lower()
    if ver_grafo_final == 's':
        dibujar_grafo_con_ruta_numerada(None, "Grafo General - Sin conexión directa EdoMex-CDMX")

if __name__ == "__main__":
    main()