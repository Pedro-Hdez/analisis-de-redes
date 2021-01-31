from grafica2 import Grafica
from os import system, name
from grafica2 import Cola

def validar(num):
    try:
        int(num)
        return True
    except:
        return False
    

def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

g = Grafica()
g.leer_grafica("grafica.txt")
copia = Grafica()
seleccion = ""

while (seleccion != "17"):
    clear()
    print("Menu")
    print("1) Agregar arista")
    print("2) Agregar nodo")
    print("3) Eliminar nodo")
    print("4) Eliminar arista")
    print("5) Buscar nodo")
    print("6) Buscar arista")
    print("7) Obtener grado de un nodo")
    print("8) Obtener numero de nodos")
    print("9) Obtener numero de aristas")
    print("10) Vaciar un nodo")
    print("11) Vaciar grafica")
    print("12) Imprimir grafica")
    print("13) Copiar grafica")
    print("14) Ver copia de la grafica")
    print("15) Verificar si la grafica es bipartita")
    print("16) paseo euler")
    print("17) Salir")

    seleccion = input()
    if validar(seleccion):
        if (int(seleccion) < 1 or int(seleccion) > 17):
            input("Error. Opción inválida. Presione Enter para intentarlo de nuevo...")
        else:
            if (seleccion == "1"):
                error = True
                while(error):
                    naristas = input("Ingrese la cantidad de aristas que desea agregar: ")
                    if not (validar(naristas)):
                        input("Error. Ingrese un número. Presione enter para intentarlo de nuevo...")
                    else:
                        naristas = int(naristas)
                        error = False
                while (naristas >0):
                    nodo1 = input("Ingrese el nodo 1: ")
                    nodo2 = input("Ingrese el nodo 2: ")
                    etiqueta = input("Ingrese la etiqueta del arista: ")
                    if g.agregar_arista(nodo1, nodo2, etiqueta):
                        naristas = naristas - 1
                    else:
                        print(f"La arista ({nodo1}, {nodo2}, {etiqueta}) ya existe")
                input("\nAristas agregadas. Presione Enter para continuar...")

            if (seleccion == "2"):
                nodo = input("Ingrese el nombre del nodo: ")
                if g.agregar_nodo(nodo):
                    print("Nodo", nodo, "agregado")
                else:
                    print("El nodo", nodo, "ya existe")
                input("\nPresione Enter para continuar...")
                
                
            if (seleccion == "3"):
                nodo = input("Ingrese el nombre del nodo que desea eliminar: ")
                if g.eliminar_nodo(nodo):
                    print("Nodo", nodo, "eliminado")
                else:
                    print("El nodo", nodo, "no existe")
                
                input("\nPresione Enter para continuar...")
                
            if (seleccion == "4"):
                nodo1 = input("Nodo 1: ")
                nodo2 = input("Nodo 2: ")
                etiqueta = input("Etiqueta (Enter si desea omitirla): ")
                if etiqueta == "":
                    etiqueta = None

                if g.eliminar_arista(nodo1, nodo2, etiqueta):
                    print(f"Arista eliminada")
                else:
                    print(f"La arista no existe")
                
                input("\nPresione Enter para continuar...")
            
            if (seleccion == "5"):
                nodo = input("Ingrese el nombre del nodo: ")
                if g.buscar_nodo(nodo):
                    print("El nodo", nodo, "existe")
                else:
                    print("El nodo", nodo, "no existe")
                
                input("\nPresione Enter para continuar...")
                
            if (seleccion == "6"):
                nodo1 = input("Nodo 1: ")
                nodo2 = input("Nodo 2: ")
                etiqueta = input("Etiqueta (Enter si desea omitirla): ")
                if etiqueta == "":
                    etiqueta = None

                if (g.buscar_arista(nodo1, nodo2, etiqueta)):
                    print("La arista existe")
                else:
                    print("La arista no existe")
                
                input("\nPresione Enter para continuar...")
            
            if (seleccion == "7"):
                nodo = input("Ingrese el nombre del nodo: ")
                grado = g.obtener_grado(nodo)
                if type(grado) != bool:
                    print("El grado del nodo", nodo, "es:", grado)
                else:
                    print("El nodo", nodo, "no existe")
                        
                input("\nPresione Enter para continuar...")
                
            if (seleccion == "8"):
                print("La gráfica tiene", g.obtener_numero_nodos(), "nodos")
                input("\nPresione Enter para continuar...")
            
            if (seleccion == "9"):
                print("La gráfica tiene", g.obtener_numero_aristas(), "aristas")
                input("\nPresione Enter para continuar...")
                
            if (seleccion == "10"):
                nodo = input("Ingrese el nodo que desee vaciar: ")
                if g.vaciar_nodo(nodo):
                    print("El nodo", nodo, "se ha vaciado.")
                else:
                    print("El nodo", nodo, "no existe")
                        
                input("\nPresione Enter para continuar...")
                        
            if (seleccion == "11"):
                g.vaciar_grafica()
                print("La gráfica se ha vaciado.")
                input("\nPresione Enter para continuar...")
            
            if (seleccion == "12"):
                print(g)
                input("\nPresione Enter para continuar...")
            
            if (seleccion == "13"):
                copia = g.copiar()
                print("Gráfica copiada correctamente: ")
                print(copia)
                input("\nPresione Enter para continuar...")

            if (seleccion == "14"):
                print("Última copia guardada: ")
                print(copia)
                input("\nPresione Enter para continuar...")
                
            if (seleccion == "15"):         
                v1, v2 = g.es_bipartita()
                if v1:
                    print("\n")
                    print("La gráfica SÍ es bipartita :)")
                    print("Gráfica g: ")
                    print(g)
                    print("Conjuntos:")
                    print("V1")
                    print (v1)
                    print("V2")
                    print (v2)
                else:
                    print("Gráfica g: ")
                    print(g)
                    print("La gráfica NO es bipartita :(")

               
                input("\nPresione Enter para continuar...")

            if (seleccion == "16"):  
                
                paseo_euler = g.paseo_euler()
                if paseo_euler:
                    print("Se encontró el siguiente paseo de Euler:")
                    print(paseo_euler)
                else:
                    print("La gráfica no contiene paseos de Euler")
                
             
                input("\nPresione Enter para continuar...")
                

    else:
        input("Error. Ingrese un número entre 1 y 15. Presione Enter para intentarlo de nuevo...")   
