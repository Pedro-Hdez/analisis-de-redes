from grafica import *

g = Grafica()
g.leer_grafica("grafica.txt")
bosque_prim = g.algoritmo_prim()
bosque_kruskal = g.algoritmo_kruskal()

print("ALGORITMO DE PRIM")
for arbol in bosque_prim:
    for arista in arbol:
        print(arista[0].nombre, arista[1].destino, arista[1].peso)
    print("--------------------------")


print("ALGORITMO DE KRUSKAL")
for arista in bosque_kruskal:
    print(arista[0].nombre, arista[1].destino, arista[1].peso)