from digrafica import *

d = Digrafica()
d.leer_digrafica("digrafica.txt")

nodo1 = "a"
nodo2 = "e" 

normal = []
ruta_mas_corta = d.dikjstra_general(nodo1, nodo2)

if ruta_mas_corta:
    print(f"De {nodo1} hasta {nodo2}")
    print("SOLUCION TEMPORAL")
    for arco in ruta_mas_corta:
        print(f"({arco.origen.nombre}, {arco.destino.nombre}, {arco.peso})")
    print("--------------------")
    print("DIKJSTRA GENERAL")
    longitud_total = 0
    for arco in ruta_mas_corta:
        print(f"({arco.origen.nombre}, {arco.destino.nombre}, {arco.peso})")