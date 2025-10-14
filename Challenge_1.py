from collections import deque # solo lo uso para la reconstrucción de ruta.
import heapq # Módulo CLAVE: Implementa la cola de prioridad (Min-Heap) para Dijkstra.

# CONSTANTES DE TERRENO Y MODELO DE COSTOS

camino_libre = 0  # Costo 1
edificio = 1      # Costo Infinito (Muro, Intransitable)
agua = 2          # Costo 3 (Penalización por lentitud)
bloqueo = 3       # Costo 5 (La mayor penalización)

# Constantes de visualización
visual_libre=' . '
visual_obstaculo=' X ' 
visual_agua=' ~ '     
visual_bloqueo=' # '   
visual_ruta=' * '
visual_inicio=' I '
visual_final=' F '

filas = 0
columnas = 0


def crear_mapa_vacio(f, c):
    """Crea un mapa nuevo con caminos libres (0) del tamaño especificado."""
    mapa = [[camino_libre for _ in range(c)] for _ in range(f)]
    # Opcionalmente, puedes añadir un obstáculo inicial para probar el ruteo:
    if f > 5 and c > 5:
        mapa[f//2][c//2] = bloqueo # Bloqueo en el centro
    return mapa


def es_coodenada_valida(mapa,fila,columna):
    """Verifica límites y transibilidad. Solo Edificio (1) es muro."""
    es_dentro_limites = (0<= fila < filas) and (0<= columna < columnas)
    if not es_dentro_limites: return False
    
    valor = mapa[fila][columna]
    es_muro = valor == edificio 
    return not es_muro

def obtener_costo_terreno(valor_celda):
    """
    MODELADO DE COSTOS: Asigna la penalización real de moverse a esta celda.
    """
    if valor_celda == camino_libre: return 1
    if valor_celda == agua: return 3
    if valor_celda == bloqueo: return 5
    return float('inf')

def reconstruir_ruta(camino_padre,inicio,fin):
    """Genera la lista de coordenadas de la ruta a partir del diccionario de predecesores."""
    ruta = []
    actual = fin
    while actual is not None:
        ruta.append(actual)
        actual = camino_padre.get(actual)
    ruta_correcta = ruta[::-1]
    
    # Devuelve solo los puntos intermedios
    if len(ruta_correcta) > 2:
            return ruta_correcta[1:-1]
    else:
            return []

def visualizar_mapa(mapa,ruta= None,inicio= None,fin=None):
    """Imprime el mapa mostrando rutas y terrenos."""
    ruta_set= set(ruta) if ruta else set()
    ancho = columnas * 3+6 
    print ("\n" + "=" * ancho) 
    print( f"Mapa de la ciudad ({filas}x{columnas})")
    print ("=" * ancho)
    encabezado = "   " +"".join([f"{c:2d}" for c in range (columnas)])
    print(encabezado) 

    for r in range (filas):
        fila_str = f"{r:2d}|" 
        for c in range (columnas):
            coordenada = (r,c)
            valor = mapa [r][c]
            simbolo = visual_libre

            if coordenada == inicio: simbolo = visual_inicio
            elif coordenada == fin: simbolo = visual_final
            elif coordenada in ruta_set: simbolo = visual_ruta
            elif valor == edificio: simbolo = visual_obstaculo 
            elif valor == agua: simbolo = visual_agua      
            elif valor == bloqueo: simbolo = visual_bloqueo 

            fila_str += simbolo
        print(fila_str)
    print("=" * ancho + "\n")

def obtener_coordenadas(mapa,tipo):
    """Pide y valida las coordenadas de inicio/fin."""
    while True:
        try:
            entrada = input(f"Ingresa la coordenada de {tipo} (Fila, Columna): ")
            fila,columna = map(int,entrada.split(','))
            
            if 0 <= fila < filas and 0 <= columna < columnas and mapa[fila][columna] != edificio:
                print(f"Coodenada de {tipo} aceptada: ({fila},{columna})")
                return (fila,columna)
            else:
                 print(f" Error: El punto ({fila},{columna}) es un obstáculo (Edificio) o está fuera. Intenta de nuevo.")
        except ValueError:
            print(f" Error de entrada. Usa el formato 'Fila,Columna' (ej: 0,0) con números enteros.")

def agregar_obstaculo_dinamico(mapa):
    """Permite al usuario añadir edificios (1) en tiempo de ejecución."""
    print("\n--- Agregar obstaculo (X)---")
    while True:
        try:
            entrada = input("coordenada(Fila,Columna) para nuevo obstaculo (o'fin'):")
            if entrada.lower()=='fin': break
            fila,columna = map(int,entrada.split(','))
            if not (0 <= fila < filas and 0 <= columna < columnas):
                print(f"Error: La coordenada ({fila},{columna}) esta fuera del mapa")
                continue
            mapa[fila][columna] = edificio
            print(f"Obstaculo (X) agregado en ({fila},{columna})")
            visualizar_mapa(mapa)
        except (ValueError,IndexError):
            print("Error:Usa el formato 'Fila,Columna'(ej:0,0)")

# 2. ALGORITMO PRINCIPAL: DIJKSTRA

def dijkstra_costos(mapa, origen, destino):
    """
    DIJKSTRA: Encuentra la ruta con el menor COSTO TOTAL.
    Usa una cola de prioridad (heapq) y la función de costo variable.
    """
    filas, columnas = len(mapa), len(mapa[0])
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
    
    # distancias: g_score (costo real) desde el origen.
    distancias = { (r, c): float('inf') for r in range(filas) for c in range(columnas) }
    distancias[origen] = 0
    predecesores = { origen: None }
    
    # Cola de Prioridad: (costo_acumulado, coordenada)
    cola_prioridad = [(0, origen)]

    while cola_prioridad:
        costo_actual, actual = heapq.heappop(cola_prioridad) # Extrae el nodo con menor costo

        if actual == destino: 
            return reconstruir_ruta(predecesores, origen, destino)
        
        # Optimización: Si ya encontramos una ruta más corta, ignorar esta entrada.
        if costo_actual > distancias[actual]: 
            continue 

        for df, dc in direcciones:
            nf, nc = actual[0] + df, actual[1] + dc
            vecino = (nf, nc)
            
            if es_coodenada_valida(mapa, nf, nc):
                
                # Usa el costo variable del terreno para el movimiento.
                costo_paso = obtener_costo_terreno(mapa[nf][nc])
                costo_tentativo = costo_actual + costo_paso # Nuevo costo acumulado

                if costo_tentativo < distancias[vecino]:
                    # Relajación: Se encontró una ruta mejor.
                    distancias[vecino] = costo_tentativo
                    predecesores[vecino] = actual
                    heapq.heappush(cola_prioridad, (costo_tentativo, vecino))
                    
    return None 

# 3. FUNCIÓN PRINCIPAL DE EJECUCIÓN

def calculadora_rutas():
    # Asegura que las dimensiones del mapa sean globales.
    global filas, columnas 

    print("="*40)
    print("  Calculadora de Rutas con Costo (Dijkstra)  ")
    print("="*40)

    # Pedir el tamaño al usuario
    while True:
        try:
            filas_input = input("Ingrese número de FILAS (ej: 10): ")
            columnas_input = input("Ingrese número de COLUMNAS (ej: 10): ")
            filas = int(filas_input)
            columnas = int(columnas_input)
            if filas > 0 and columnas > 0:
                break
            print("El tamaño debe ser mayor a cero.")
        except ValueError:
            print("Por favor, ingrese un número entero.")

    # 1. Configuración del mapa.
    # Usamos la función con las dimensiones ingresadas.
    mapa_actual = crear_mapa_vacio(filas, columnas) 
    
    visualizar_mapa(mapa_actual)
    
    # 2. Obtención de obstáculos.
    opcion = input("Deseas agregar obstaculos dinamicamente (Edificio)?(s/n):").lower()
    if opcion == 's':
        agregar_obstaculo_dinamico(mapa_actual)

    # 3. Definición de Inicio y Fin.
    inicio = obtener_coordenadas(mapa_actual, "Inicio (I)") 
    fin = obtener_coordenadas(mapa_actual, "Destino (F)") 

    # 4. EJECUCIÓN DEL ALGORITMO DIJKSTRA
    print(f"\nBuscando ruta de {inicio} a {fin} usando Dijkstra...")
    ruta_dijkstra = dijkstra_costos(mapa_actual, inicio, fin)
    
    # LÓGICA PARA CALCULAR EL COSTO TOTAL
    def calcular_costo_total(ruta, mapa, inicio, fin):
        """Calcula el costo real de una ruta."""
        if ruta is None: return float('inf')
        puntos = [inicio] + ruta + [fin]
        costo = 0
        for r, c in puntos:
            costo += obtener_costo_terreno(mapa[r][c]) 
        return costo

    costo_dijkstra = calcular_costo_total(ruta_dijkstra, mapa_actual, inicio, fin)

    # 5. VISUALIZACIÓN DE RESULTADOS
    if ruta_dijkstra:
        print("\n--- RESULTADO DE DIJKSTRA (Costo Mínimo) ---")
        print(f"Ruta Encontrada: Longitud: {len(ruta_dijkstra)+2} pasos.")
        print(f"Costo Total de la Ruta: {costo_dijkstra} unidades de costo.")
        
        print("\n--- Visualizando Ruta Óptima ---")
        visualizar_mapa(mapa_actual, ruta_dijkstra, inicio, fin)
        
    else:
        print("\n============================================")
        print("Ruta imposible! No se pudo encontrar un camino")
        print("==============================================")

if __name__ == "__main__":
    calculadora_rutas()