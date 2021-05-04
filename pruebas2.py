from red import *
d = Red()
d.leer_red("red.txt")

visitados = []
fuentes = []
sumideros = []

fuentes.append('a')
fuentes.append('b')
sumideros.append('g')

flujo = d.costo_minimo_rutas_cortas(fuentes,sumideros,15)

d.imprimir_arcos()

print("")
print("costo final de la red: ",flujo)        



