'''FUNCIÓN dijkstra_costos_incompleto(tablero, origen, destino):

    // 1. Inicialización
    //   G-Score (Costo Acumulado): Diccionario para almacenar el mejor costo a cada nodo.
    Distancia_a[origen] = 0; todos los demás a INFINITO.
    Predecesores: Diccionario para almacenar el camino de retorno.
    
    //   Cola de Prioridad: (costo_acumulado, coordenada)
    Insertar (0, origen) en la Cola_de_Prioridad.
    
    // 2. Búsqueda
    MIENTRAS la Cola_de_Prioridad NO esté vacía:
        
        Extraer el nodo 'actual' con el MENOR costo_actual.
        
        SI costo_actual > Distancia_a[actual], ENTONCES:
            CONTINUAR (Ignorar ruta vieja).

        SI 'actual' es igual a 'destino', ENTONCES:
            TERMINAR y reconstruir ruta.

        // 3. Explorar Vecinos (Relajación)
        PARA cada 'vecino' en movimientos_validos(tablero, actual):
            
            costo_paso = OBTENER_COSTO_TERRENO(...) // Costo de moverse al vecino
            costo_tentativo = costo_actual + costo_paso

            // Relajación: ¿Hemos encontrado una ruta mejor?
            SI costo_tentativo < Distancia_a[vecino], ENTONCES:
                
                // Actualizar
                Actualizar Distancia_a[vecino] = costo_tentativo
                Actualizar Predecesores[vecino] = actual
                
                // Insertar la nueva prioridad en la cola
                Insertar (costo_tentativo, vecino) en Cola_de_Prioridad.'''

# =================================================================
# 4. FUNCIÓN DIJKSTRA (INCOMPLETA)
# =================================================================

def dijkstra_costos_incompleto(tablero, origen, destino):
    filas = len(tablero)
    columnas = len(tablero[0])
    
    # Inicialización de G-Score y Predecesores usando un diccionario (más limpio que la matriz)
    distancias = {} 
    predecesores = {}
    
    # Llenar diccionarios con valores iniciales
    for r in range(filas):
        for c in range(columnas):
            distancias[(r, c)] = float('inf')
            predecesores[(r, c)] = None

    distancias[origen] = 0
    
    # Cola de Prioridad: (costo, coordenada_tuple)
    cola_prioridad = [(0, origen)]

    while cola_prioridad:
        costo_actual, actual = heapq.heappop(cola_prioridad)

        if actual == destino:
            # 1. TODO: Retorna la ruta reconstruida al alcanzar el destino.
            return reconstruir_ruta(predecesores, origen, destino)

        if costo_actual > distancias[actual]: 
            continue 

        # Itera sobre los vecinos válidos que no son muros
        for vecino in movimientos_validos(tablero, actual):
            
            # 2. TODO: Calcula el costo de paso
            # El valor del mapa es el tipo de celda; obtener_costo_terreno da el costo real (1 o inf)
            costo_paso = obtener_costo_terreno(tablero[vecino[0]][vecino[1]])
            costo_tentativo = costo_actual + costo_paso

            # 3. TODO: Implementa la condición de Relajación
            if costo_tentativo < distancias[vecino]:
                
                # 4. TODO: Actualiza el G-Score y el camino (Predecesor)
                distancias[vecino] = costo_tentativo
                predecesores[vecino] = actual
                
                # 5. TODO: Inserta la nueva prioridad en la cola
                heapq.heappush(cola_prioridad, (costo_tentativo, vecino))
                
    return None # Retorna None si no se encuentra ruta