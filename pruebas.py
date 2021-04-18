from red import *
d = Red()
d.leer_red("digrafica.txt")

visitados = []
fuentes = []
sumideros = []

fuentes.append('a')
fuentes.append('c')
sumideros.append('e')
sumideros.append('f')

flujo = d.flujo_maximo(fuentes,sumideros)

d.imprimir_arcos()

print("")
print("flujo final de la red: ",flujo)

