from red import *
d = Red()
d.leer_red("red.txt")

visitados = []
fuentes = []
sumideros = []

fuentes.append('a')

sumideros.append('g')

costo = d.costo_minimo_ciclos_negativos(fuentes,sumideros,15)

d.imprimir_arcos()

print("")
print("Costo final: ",costo)

