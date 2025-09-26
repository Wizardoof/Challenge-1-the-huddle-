from collections import deque

#contantes de terreno
camino_libre=0  #transitado
edificio=1  #obstaculo1
agua=2  #obstaculo2
bloqueo=3  #bloqueadas temporalmente 

#constantes para visualizar
visual_libre='.'
visual_obstaculo='x'
visual_ruta='*'
visual_inicio='I'
visual_final='F'

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
    
    ancho = columnas * 3+6
    print ("\n" + "=" * ancho)
    print( f"mapa de la ciudad ({filas}x{columnas})")
    print ("=" * ancho)

    #imprime el encabezado de las columnas
    encabezado = "   " +"".join([f"{c:2d}" for c in range (columnas)])
    print(encabezado)
    #recorre cada celda
    for r in range (filas):
        fila_str = f"{r:2d}|"
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
                






    
