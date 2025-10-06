from collections import deque

#contantes de terreno
camino_libre = 0  #transitado
edificio = 1  #obstaculo1
agua = 2  #obstaculo2
bloqueo = 3  #bloqueadas temporalmente 

#constantes para visualizar
visual_libre=' . '
visual_obstaculo=' x '
visual_ruta=' * '
visual_inicio=' I '
visual_final=' F '

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
        
 #las variables de tamanho son globales se definen en la funcion principal
 
filas = 0
columnas = 0


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
    es_obstaculo = valor in [edificio,agua,bloqueo]
    #solo es valida si NO es obstaculo
    return not es_obstaculo

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
    global filas,columnas

    print("=================================")
    print(       "Calculadora de Rutas"      )
    print("=================================")

    #configuracion del mapa 
    while True:
        #uso .srip() para quitar espacios en blanco innecesarios
        #Y [0] para tomar solo el primer caracter que ingreso el usuario
        entrada = input("¿Usar mapa por Defecto 10x10 (d) o Crear uno nuevo (c)? [d/c]: ")

        if entrada: #asegura que el usuario no solo presione Enter 
            eleccion = entrada.strip().lower()[0] #toma el primer caracter en minuscula
            if eleccion in ['d','c']:
                break

        print("Opcion invalida ingresa solo 'd' o 'c'")

    if eleccion == 'c':
        print("\n--- Creacion de Mapa Personalizado ---")
        while True:
            try:
                f = int (input("Ingresa el numero de filas "))
                c = int (input("Ingresa el numero de columnas"))
                if f <= 1 or c <= 1:
                    print("El mapa debe tener al menos 2x2")
                    continue
                break
            except ValueError:
                print("Error: Por favor, ingresa numeros enteros positivos")

        mapa_actual = crear_mapa_vacio(f,c)

    else:
            #opcion 'd' por defecto 
        mapa_actual = crear_mapa()

            #Ajuste de las variables de tamanho globales 
    filas = len(mapa_actual)
    columnas = len(mapa_actual[0])
            
            #Confuguracion dinamica 
    visualizar_mapa(mapa_actual)
            
            #Si eligio mapa personalizado, forzamos la opcion de agregar obstaculos
    if eleccion == 'c':
        print("El mapa esta vacio. Agrega obstaculos o prueba tu ruta")
        agregar_obstaculo_dinamico(mapa_actual)
    else:
        opcion = input("Deseas agregar obstaculos dinamicamente al mapa por defecto?(s/n):").lower()
        if opcion == 's':
            agregar_obstaculo_dinamico(mapa_actual)

                #Obtener coordenadas 
    print(f"Mapa activo: {filas} filas x {columnas} columnas")
                
    inicio = obtener_coordenadas(mapa_actual,"Inicio (I)")
    fin = obtener_coordenadas(mapa_actual, "Destino (F)")

                #Ejecutar BFS
    print(f"\n Buscando ruta de {inicio} a {fin}...") 
    ruta_encontrada = buscar_ruta_mas_corta(mapa_actual,inicio,fin)

                #Mostrar el resultado 
    if ruta_encontrada is None:
        print("\n============================================")
        print("Ruta imposible! No se pudo encontrar un camino")
        print("==============================================")
    else:
        print(f"\nRuta encontrada! Longitud: {len(ruta_encontrada)+2} pasos")
        visualizar_mapa(mapa_actual,ruta_encontrada,inicio,fin)

#punto de Entrada 

if __name__ == "__main__":
    calculadora_rutas()






    
