from digrafica import *

d = Digrafica()
d.leer_digrafica("digrafica.txt")

nodo1 = "a"
nodo2 = "e" 

normal = []
ruta_mas_corta = d.dikjstra_general(nodo1)

if ruta_mas_corta:
    if ruta_mas_corta[0]=='ciclo':
        ruta_mas_corta.pop(0)
        longitud_ciclo = ruta_mas_corta.pop(len(ruta_mas_corta)-1)
        print("Se encontró un ciclo de longitud ",longitud_ciclo, " con los aristas: ")
        for arco in ruta_mas_corta:
            print("(",arco.origen.nombre,",",arco.destino.nombre,") ")
    else:    
        print(f"De {nodo1} hasta {nodo2}")
        print("SOLUCION TEMPORAL")
        for arco in ruta_mas_corta:
            print(f"({arco.origen.nombre}, {arco.destino.nombre}, {arco.peso})")
        print("--------------------")
        print("DIKJSTRA GENERAL")
        longitud_total = 0
        for arco in ruta_mas_corta:
            print(f"({arco.origen.nombre}, {arco.destino.nombre}, {arco.peso})")