from grafica import *

g = Grafica()
g.leer_grafica("grafica.txt")

arbol_minimo = g.algoritmo_kruskal()
print("Árbol de mínima expansión con Kruskal")
print(arbol_minimo)