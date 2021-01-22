from grafica2 import Grafica
g = Grafica()
g.leer_grafica("grafica_bipartita.txt")
print("GRÁFICA")
print(g)
print("\n¿Es bipartita?")
v1, v2 = g.es_bipartita()

if v1:
    print("SÍ\n")
    print("V1")
    print (v1)
    print("V2")
    print (v2)
else:
    print("NO")
