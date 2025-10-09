from collections import deque
import heapq #necesario para Dijkstra y A*

#contantes de terreno
camino_libre = 0  #transitado costo 1 
edificio = 1  #obstaculo (Muro,costo infinito)
agua = 2  #Transitable (costo 3 )
bloqueo = 3  #Transitable (costo 5)

#constantes para visualizar
visual_libre=' . '
visual_obstaculo=' x '
visual_ruta=' * '
visual_inicio=' I '
visual_final=' F '

 #las variables de tamanho son globales se definen en la funcion principal
 
filas = 0
columnas = 0

def crear_mapa():

    mapa = [
#col 0  1  2  3  4  5  6  7  8  9
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # Fila 0
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0], # Fila 1 (Bloqueo de edificios)
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 0], # Fila 2
    [0, 1, 0, 2, 2, 2, 2, 0, 1, 0], # Fila 3 (Agua 2)
    [0, 0, 0, 2, 3, 3, 2, 0, 1, 0], # Fila 4 (Bloqueo 3)
    [0, 1, 1, 2, 3, 3, 2, 0, 0, 0], # Fila 5
    [0, 0, 0, 2, 2, 2, 2, 0, 1, 0], # Fila 6
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 0], # Fila 7
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0], # Fila 8
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Fila 9
    ]
    return mapa

def crear_mapa_vacio(filas,columnas):
    #crear un mapa [filas x columnas] lleno de caminos libres(0)
    #lista de comprension: crea 'filas' listas, cada una con 'columnas' ceros
    return [[camino_libre for _ in range(columnas)] for _ in range(filas)]
        

def visualizar_mapa(mapa,ruta= None,inicio= None,fin=None):
    #imprime el mapa mostrando obstaculos x, camino libre . y la ruta mas corta si se proporciona *

    # si se proporciona una ruta,la convierto a un 'set' para busqueda rapidas
    ruta_set= set(ruta) if ruta else set()
   #calculo del ancho para los bordes
    
    ancho = columnas * 3+6 #cada celda del mapa se imprime usando 3 caracteres por ej "==="
    print ("\n" + "=" * ancho) # +6 valor fijo para contar los caracteres fijos de la izquierda 
    # los digitos, los separadores(|)y los espacios para el encabezado
    # asegura que las lines de borde y el titulo del mapa(====) se alineen con los bordes 
    print( f"mapa de la ciudad ({filas}x{columnas})")
    print ("=" * ancho)

    #imprime el encabezado de las columnas
    encabezado = "   " +"".join([f"{c:2d}" for c in range (columnas)])
    print(encabezado) #*3+6, r:2d y c:2d se usan para darle al mapa un formato estetico y alineado
    #recorre cada celda
    for r in range (filas):
        fila_str = f"{r:2d}|" 
        #:2d el valor de un numero entero decimal(d) tiene al menos 2 caracteres(d)
        # si es 5 por ej se imprime con un espacio y 10 no se agrega el espacio
        for c in range (columnas):
            coordenada = (r,c)
            valor = mapa [r][c]
            simbolo = visual_libre

            #jerarquia de visualizacion: I/E/ruta > obstaculo > libre
            if coordenada == inicio:
                simbolo = visual_inicio
            elif coordenada == fin:
                simbolo = visual_final
            elif coordenada in ruta_set:
                simbolo = visual_ruta
            elif valor in [edificio,agua,bloqueo]:
                simbolo = visual_obstaculo

            fila_str += simbolo

        print(fila_str)
    print("=" * ancho + "\n")
                
def es_coodenada_valida(mapa,fila,columna):
    
    #verifica si una coodenada no es obstaculo esta dentro de los limites
    # 1ero verifica los limites usando las variables filas y columnas
    es_dentro_limites = (0<= fila < filas) and (0<= columna < columnas)
    if not es_dentro_limites:
        return False
    #2do verifica si es transitable
    valor = mapa[fila][columna]

    es_muro = valor == edificio
    #solo si es un edificio (1) es un muro,agua(2) y bloqueo(3) son validos 
    return not es_muro

def obtener_costo_terreno(valor_celda):#asigna un costo variable al movimiento segun el terreno
    if valor_celda == camino_libre:
        return 1 #el mas rapido
    if valor_celda == agua:
        return 3 #costo intermedio
    if valor_celda == bloqueo:
        return 5 # el mas costoso 
    #si llega aqui, es edificio(1), aunque es_coordenada_valida lo deberian haber detenido
    return float('inf')

def bfs_sin_costos(mapa,inicio,fin):
    #version BFS (ruta mas corta en pasos), ignora costos variables
    if inicio == fin: return []
    movimientos = [(-1,0),(1,0),(0,-1),(0,1)]
    cola = deque([inicio])
    camino_padre = {inicio:None}

    while cola:
        actual_fila,actual_columna = cola.popleft()
        for dr,dc in movimientos:
            vecino = (actual_fila + dr, actual_columna + dc)

            #usa es_coodenada_valida (excluye solo Edificio=1)
            if es_coodenada_valida(mapa,vecino[0],vecino[1]) and vecino not in camino_padre: camino_padre[vecino] = (actual_fila,actual_columna)
            if vecino == fin:
                return reconstruir_ruta(camino_padre,inicio,fin)
            cola.append(vecino)
    return None

def dijkstra_costos(mapa,origen,destino):
    #Ruta más corta en COSTO TOTAL (usa costos variables).
    filas, columnas = len(mapa), len(mapa[0])
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
    
    distancias = { (r, c): float('inf') for r in range(filas) for c in range(columnas) }
    distancias[origen] = 0
    predecesores = { origen: None }
    
    cola_prioridad = [(0, origen)] # (costo_acumulado, (fila, columna))

    while cola_prioridad:
        costo_actual, (fila, col) = heapq.heappop(cola_prioridad)

        if (fila, col) == destino:
            return reconstruir_ruta(predecesores, origen, destino)

        if costo_actual > distancias[(fila, col)]:
            continue

        for df, dc in direcciones:
            nf, nc = fila + df, col + dc
            vecino = (nf, nc)
            
            if es_coodenada_valida(mapa, nf, nc): # Solo excluye Edificio (1)
                
                # ✅ CLAVE: Usa el costo variable del terreno
                costo_paso = obtener_costo_terreno(mapa[nf][nc])
                costo_tentativo = costo_actual + costo_paso

                if costo_tentativo < distancias[vecino]:
                    distancias[vecino] = costo_tentativo
                    predecesores[vecino] = (fila, col)
                    heapq.heappush(cola_prioridad, (costo_tentativo, vecino))
                    
    return None 

def distancia_manhattan(p1, p2):
    #Heurística para A* (Distancia de Manhattan).
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def a_star(mapa, origen, destino):
    #ruta más corta en COSTO TOTAL (optimización de Dijkstra con heurística).
    filas, columnas = len(mapa), len(mapa[0])
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
    
    g_score = { (r, c): float('inf') for r in range(filas) for c in range(columnas) }
    g_score[origen] = 0
    predecesores = { origen: None }
    
    f_score = { celda: float('inf') for celda in g_score }
    f_score[origen] = distancia_manhattan(origen, destino)

    cola_prioridad = [(f_score[origen], origen)]

    while cola_prioridad:
        f_actual, (fila, col) = heapq.heappop(cola_prioridad)

        if (fila, col) == destino:
            return reconstruir_ruta(predecesores, origen, destino)

        g_actual = g_score[(fila, col)] 

        for df, dc in direcciones:
            nf, nc = fila + df, col + dc
            vecino = (nf, nc)

            if es_coodenada_valida(mapa, nf, nc): 
                
                costo_paso = obtener_costo_terreno(mapa[nf][nc])
                g_tentativo = g_actual + costo_paso 

                if g_tentativo < g_score[vecino]:
                    
                    predecesores[vecino] = (fila, col)
                    g_score[vecino] = g_tentativo
                    
                    h_score = distancia_manhattan(vecino, destino)
                    f_score[vecino] = g_tentativo + h_score
                    
                    heapq.heappush(cola_prioridad, (f_score[vecino], vecino))
                    
    return None


def obtener_coordenadas(mapa,tipo):
    #pide la coordenada al usuario y la valida repetidamente
    while True:
        try:
            entrada = input(f"ingresa la coordenada de {tipo}(fila,columna)")
#map (int,...) convierte ambos elementos del split en enteros 
            fila,columna = map(int,entrada.split(','))
            if es_coodenada_valida(mapa,fila,columna):
                print(f"Coodenada de {tipo} aceptada: ({fila},{columna})")
                return (fila,columna)
            else:
                 print(f" Error: El punto ({fila},{columna}) es un obstáculo o está fuera. Intenta de nuevo.")
        except ValueError:
            print(f" Error de entrada. Usa el formato 'Fila,Columna' (ej: 0,0) con números enteros.")


#funcion para agregar obstaculos dinamicamente 
def agregar_obstaculo_dinamico(mapa):
    #permite al usuario agregar obstaculos en el mapa cuando se ejecuta
    print("\n---Agregar obstaculo (X)---")
    print("El mapa se actualiza en memoria,")

    while True:
        try:
            entrada = input("coordenada(Fila,Columna) para nuevo obstaculo (o'fin'):")
            if entrada.lower()=='fin': break
            fila,columna = map(int,entrada.split(','))
            #verifico los limites 
            if not (0 <= fila < filas and 0 <= columna < columnas):
                print(f"Error: La coordenada ({fila},{columna}) esta fuera del mapa")
                continue
            # la linea importante : modifica la matriz en memoria 
            mapa[fila][columna] = edificio
            print(f"Obstaculo (X) agregado en ({fila},{columna})")
            visualizar_mapa(mapa)

        except (ValueError,IndexError):
            print("Error:Usa el formato 'Fila,Columna'(ej:0,0)")
    
    print("--- Configuracion de obstaculos terminada. ---\n")

def reconstruir_ruta(camino_padre,inicio,fin):
    #usa el diccionario camino_padre para retroceder desde 'fin' hasta 'inicio
    #y generar la lista de coodenadas que forman la ruta
    ruta = []
    actual = fin

    #retrocede hasta que llega a la celda cuyo padre es None o sea el 'inicio'
    while actual is not None:
        ruta.append(actual)
        actual = camino_padre.get(actual)

        #invertimos la lista para obtener inicio -> fin
    ruta_correcta = ruta[::-1]

        #devolvemos solo los puntos intermedios para visualizarlos con '*'
    if len(ruta_correcta) > 2:
            return ruta_correcta[1:-1]
    else:
            return []
        
def buscar_ruta_mas_corta(mapa,inicio,fin):
    #para la ruta mas corta usando BFS
    if inicio == fin:
        return []
    #movimientos : Arriba, Abajo,Izquierda,Derecha
    movimientos = [(-1,0),(1,0),(0,-1),(0,1)]

    #cola : Para celdas a visitar
    cola = deque([inicio])

    # camino padre: diccionario que rastrea de donde vino a cada celda
    camino_padre = {inicio:None}

    while cola:
        actual_fila, actual_columna = cola.popleft() #la celda mas antigua

        #explora los 4 vecinos
        for dr,dc in movimientos:
            vecino_fila,vecino_columna = actual_fila + dr, actual_columna + dc
            vecino = (vecino_fila,vecino_columna)

            #si el vecino es valido y no ha sido visitado:
            if es_coodenada_valida(mapa,vecino_fila,vecino_columna) and vecino not in camino_padre:
                camino_padre[vecino] = (actual_fila,actual_columna) #registra el camino
                # si se encontro el destino:
                if vecino == fin:
                    return reconstruir_ruta(camino_padre,inicio,fin)
                #agregamos a la cola para seguir explorando 
                cola.append(vecino)
                
    #si la cola se vacia y no hay ruta :            
    return None

def calculadora_rutas():
    #funcion principal que maneja la logica de eleccion del mapa y la ejecucion

    #Hago que las FILAS y COLUMNAS sean variables globales para modificarlas aqui
    # Esta variable debe ser global para ser modificada por la función
    global filas, columnas 

    print("="*35)
    print("      Calculadora de Rutas Avanzada      ")
    print("="*35)

    # Lógica de elección y creación del mapa (omito detalles por espacio)
    mapa_actual = crear_mapa()
    filas = len(mapa_actual)
    columnas = len(mapa_actual[0])
    
    visualizar_mapa(mapa_actual)
    
    # Opcional: Agregar obstáculos dinámicamente
    opcion = input("Deseas agregar obstaculos dinamicamente (Edificio)?(s/n):").lower()
    if opcion == 's':
        agregar_obstaculo_dinamico(mapa_actual)

    # Ejemplo de inicio y fin que fuerzan una elección de ruta (evitan los costosos)
    inicio = obtener_coordenadas(mapa_actual, "Inicio (I)") # Ej: (0,0)
    fin = obtener_coordenadas(mapa_actual, "Destino (F)") # Ej: (9,9)

    # EJECUCIÓN DE LOS ALGORITMOS
    print(f"\nBuscando ruta de {inicio} a {fin}...")
    
    # 1. BFS (Menor número de pasos)
    ruta_bfs = bfs_sin_costos(mapa_actual, inicio, fin)
    
    # 2. DIJKSTRA (Menor costo total, sin heurística)
    ruta_dijkstra = dijkstra_costos(mapa_actual, inicio, fin)
    
    # 3. A* (Menor costo total, con heurística - más rápido)
    ruta_a_star = a_star(mapa_actual, inicio, fin)

    # VISUALIZACIÓN DE RESULTADOS
    
    if ruta_dijkstra:
        print("\n--- COMPARATIVA DE RUTAS ---")
        
        # El costo se puede calcular sumando los costos de las celdas en la ruta
        # Calculamos el costo total para demostrar la diferencia:
        def calcular_costo_total(ruta, mapa, inicio, fin):
            costo = obtener_costo_terreno(mapa[inicio[0]][inicio[1]]) # Costo del inicio
            for r, c in ruta:
                costo += obtener_costo_terreno(mapa[r][c])
            costo += obtener_costo_terreno(mapa[fin[0]][fin[1]]) # Costo del final
            return costo

        costo_dijkstra = calcular_costo_total(ruta_dijkstra, mapa_actual, inicio, fin)
        costo_bfs = calcular_costo_total(ruta_bfs, mapa_actual, inicio, fin)

        print(f"Ruta BFS (Pasos): Longitud: {len(ruta_bfs)+2}, Costo Total: {costo_bfs}")
        print(f"Ruta DIJKSTRA (Costo): Longitud: {len(ruta_dijkstra)+2}, Costo Total: {costo_dijkstra}")
        
        print("\n--- Visualizando Ruta DIJKSTRA (Costo Mínimo) ---")
        visualizar_mapa(mapa_actual, ruta_dijkstra, inicio, fin)
        
    else:
        print("\n============================================")
        print("Ruta imposible! No se pudo encontrar un camino")
        print("==============================================")

# Punto de Entrada
if __name__ == "__main__":
    calculadora_rutas()





    
