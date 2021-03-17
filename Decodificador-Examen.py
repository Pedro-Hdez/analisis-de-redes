from grafica import *

# Secuencia para probar el algoritmo
secuencia = [2,1,5,5,7,4,1,5]

# Funcíon decodificador que recibe una lista se números como parametro (secuencia)
def Decodificador(secuencia):
    # Creamos una lista donde guardaremos la lista desde 1,....,n, la lista correspondiente a los vertices del árbol
    lista = []
    # Obtenemos el tamaño de la secuencia
    lens = len(secuencia)

    # Creamos una gráfica donde guardaremos el arbol
    arbol = Grafica()

    # Llenamos la lista con valores desde 1,....,n
    # Donde n es el tamaño de la secuencia + 2
    for x in range(lens+2):
        lista.append(x+1)

    #Iniciamos el ciclo desde 1 hasta n-2 (tamaño secuencia)
    for x in range(lens):
        # Creamos una copia de lista que nos servira como lista auxiliar
        lista2 = lista.copy()

        # Ciclo para encontrar el minimo en lista que no está en la secuencia
        while(True):
            # Buscamos el minimo en lista
            k = min(lista2)
            # Si k no está en la secuencia, nos quedamos con ese k y rompemos el while
            if k not in secuencia:
                break
            else:
                # Si k si está en la secuencia, lo sacamos de la lista auxiliar y buscamos otro k
                lista2.remove(k)

        # Agregamos la arista (Si,k) al arbol        
        arbol.agregar_arista_digrafica(k,secuencia[x])
        # Hacemos Si = None para ya no considerarlo en la secuencia
        secuencia[x]=None
        # Eliminamos k de la lista
        lista.remove(k)

    # Agregamos al árbol los 2 vertices faltantes
    arbol.agregar_arista_digrafica(lista[0],lista[1]) 
    # Regresamos el árbol
    return arbol

#Creamos una nueva gráfica donde guardaremos el arbol resultante para probar el algoritmo
arbolexp = Grafica()

#llamamos a la funcíon decodificador
arbolexp = Decodificador(secuencia)

#Imprimimos las aristas del arbol resultante
print("Aristas del arbol resultante: ")
arbolexp.imprimir_aristas()

