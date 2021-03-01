from grafica2 import *

g = Grafica()
g.leer_grafica("grafica.txt")

bosque_prim = g.algoritmo_prim()
bosque_kruskal = g.algoritmo_kruskal()

print("ALGORITMO DE PRIM")
for arbol in bosque_prim:
    for arista in arbol:
        print(arista.origen.nombre, arista.destino.nombre, arista.peso)
    print("--------------------------")


print("ALGORITMO DE KRUSKAL")
for arista in bosque_kruskal:
    print(arista.origen.nombre, arista.destino.nombre, arista.peso)