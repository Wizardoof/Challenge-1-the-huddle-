"""FUNCIÓN dijkstra_costos(mapa, origen, destino):

    // 1. Inicialización
    //  distancias: Costo más bajo conocido hasta cada nodo (G-Score).
    //  predecesores: Para reconstruir la ruta.
    Inicializar todas las distancias a INFINITO.
    Distancia_a[origen] = 0.
    
    //  cola_prioridad: (costo_acumulado, coordenada)
    Insertar (0, origen) en la Cola_de_Prioridad (Min-Heap).
    
    // 2. Proceso de Búsqueda
    MIENTRAS Cola_de_Prioridad NO esté vacía:
        
        Extraer el nodo 'actual' con el MENOR costo_actual de la cola.
        
        SI 'actual' es igual a 'destino', ENTONCES:
            TERMINAR (Ruta encontrada).
            
        // Optimización: Evitar procesar rutas viejas o más caras.
        SI costo_actual > Distancia_a[actual], ENTONCES:
            CONTINUAR (Saltar esta iteración).

        // 3. Explorar Vecinos (Relajación)
        PARA cada 'vecino' de 'actual':
            
            SI 'vecino' NO es un muro Y es válido:
                
                // Cálculo de Costos
                costo_paso = OBTENER_COSTO_TERRENO(valor_celda[vecino]) // Ej: 1, 3, o 5
                costo_tentativo = costo_actual + costo_paso

                // Relajación: ¿Encontramos una ruta mejor?
                SI costo_tentativo < Distancia_a[vecino], ENTONCES:
                    
                    // Actualizar
                    Distancia_a[vecino] = costo_tentativo
                    Predecesor[vecino] = actual
                    
                    // Insertar/Actualizar la mejor ruta en la cola
                    Insertar (costo_tentativo, vecino) en Cola_de_Prioridad."""

import heapq 

# =================================================================
# CONSTANTES Y MODELO DE COSTOS (COMPLETADO)
# =================================================================
camino_libre = 0  # Costo 1
edificio = 1      # Costo Infinito
agua = 2          # Costo 3
bloqueo = 3       # Costo 5

# Variables globales de tamaño
filas = 0
columnas = 0

def obtener_costo_terreno(valor_celda):
    """Convierte el valor del mapa en el costo de movimiento."""
    if valor_celda == camino_libre: return 1
    if valor_celda == agua: return 3
    if valor_celda == bloqueo: return 5
    return float('inf')

def es_coodenada_valida(mapa, fila, columna):
    global filas, columnas
    es_dentro_limites = (0 <= fila < filas) and (0 <= columna < columnas)
    if not es_dentro_limites: return False
    return mapa[fila][columna] != edificio

# ... (Otras funciones auxiliares como crear_mapa_vacio, reconstruir_ruta, etc., están asumidas) ...

# =================================================================
# EJERCICIO: FUNCIÓN DIJKSTRA INCOMPLETA
# =================================================================

def dijkstra_costos_incompleto(mapa, origen, destino):
    global filas, columnas
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
    
    # Inicialización del G-Score (distancias) y predecesores
    distancias = { (r, c): float('inf') for r in range(filas) for c in range(columnas) }
    distancias[origen] = 0
    predecesores = { origen: None }
    
    # Cola de Prioridad: (costo_acumulado, coordenada)
    cola_prioridad = [(0, origen)]

    while cola_prioridad:
        costo_actual, actual = heapq.heappop(cola_prioridad)

        if actual == destino: 
            # Asumimos que la función de reconstrucción existe
            # return reconstruir_ruta(predecesores, origen, destino)
            break # Paramos para el ejercicio
        
        # Optimización: Si el costo actual extraído ya es mayor al registrado, ignorar.
        if costo_actual > distancias[actual]: 
            continue 

        for df, dc in direcciones:
            nf, nc = actual[0] + df, actual[1] + dc
            vecino = (nf, nc)
            
            if es_coodenada_valida(mapa, nf, nc):
                
                # 1. TODO: Calcula el costo de paso y el costo_tentativo
                costo_paso = obtener_costo_terreno(mapa[nf][nc])
                costo_tentativo = costo_actual + costo_paso

                # 2. TODO: Implementa la condición de Relajación
                if costo_tentativo < distancias[vecino]:
                    
                    # 3. TODO: Actualiza distancias, predecesores y la cola de prioridad
                    distancias[vecino] = costo_tentativo
                    predecesores[vecino] = actual
                    heapq.heappush(cola_prioridad, (costo_tentativo, vecino))
                    
    # return reconstruir_ruta(predecesores, origen, destino) # Si el destino fue alcanzado

# Ejemplo de uso:
# filas, columnas = 5, 5
# mapa_ejemplo = [[0, 2, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 0, 0], [0, 0, 3, 0, 0], [0, 0, 0, 0, 0]]
# dijkstra_costos_incompleto(mapa_ejemplo, (0, 0), (4, 4))