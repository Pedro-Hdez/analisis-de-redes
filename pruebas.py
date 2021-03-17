from grafica import *



#Creamos una nueva gráfica donde guardaremos el arbol resultante para probar el algoritmo
g = Grafica()
g.leer_digrafica("grafica.txt")
caminos = []
caminos = g.dijkstra("a","z")
if(caminos):
    for nodo in caminos:
        print(nodo[0].destino.nombre,": ",nodo[0].origen.nombre,nodo[1])
else:
    print("no hay arborecencia")