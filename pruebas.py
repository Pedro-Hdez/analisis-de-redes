from digrafica import *

d = Digrafica()
d.leer_digrafica("digrafica.txt")

nodo1 = "a"
nodo2 = "g"

ruta_mas_corta = d.dikjstra(nodo1)

if ruta_mas_corta:
    if isinstance(ruta_mas_corta[0], list):
        print(f"RUTAS MÁS CORTAS DESDE EL NODO {nodo1}")
        for ruta in ruta_mas_corta:
            longitud_total = 0
            print(f"Al nodo el nodo{ruta[-1].destino.nombre}")
            for arco in ruta:
                longitud_total += arco.peso
                print(f"({arco.origen.nombre}, {arco.destino.nombre}, {arco.peso})")
            print("LONGITUD DE LA RUTA:", longitud_total)
            print("-------------------------")
    else:
        print(f"RUTA MÁS CORTA DESDE {nodo1} HASTA {nodo2}")
        longitud_total = 0
        for arco in ruta_mas_corta:
            longitud_total += arco.peso
            print(f"({arco.origen.nombre}, {arco.destino.nombre}, {arco.peso})")
        print("LONGITUD DE LA RUTA:", longitud_total)
    
