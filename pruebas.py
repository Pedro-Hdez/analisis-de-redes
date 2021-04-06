from digrafica import *

d = Digrafica()
d.leer_digrafica("digrafica.txt")

nodo1 = "a"
nodo2 = "e" 

matriz = d.floyd(nodo1)

if matriz[len(matriz)-1][0] == 'ciclo':
    print("Se encontró un ciclo negativo de longitud ",matriz[len(matriz)-1][1],' con los siguientes arcos: ')
    for arco in matriz:
        if(type(arco[0]) == Arco):
            print('(',arco[0].origen.nombre,', ',arco[0].destino.nombre,')',end="")
else: 
    if (matriz):
        d.imprimir_rutas_floyd(nodo1,matriz)
    else:
        print("Error")
