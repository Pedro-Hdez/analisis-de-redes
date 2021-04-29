from red import *
d = Red()
d.leer_red("red.txt")

visitados = []
fuentes = []
sumideros = []

fuentes.append('a')

sumideros.append('g')

flujo = d.costo_minimo(fuentes,sumideros,15)

d.imprimir_arcos()

print("")
print("flujo final de la red: ",flujo)

