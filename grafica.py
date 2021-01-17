from os import system, name

# define our clear function 

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

class Arista:
    """
        Esta clase representa una arista. Tiene un nodo destino
        y una etiqueta. De esta forma es más fácil agregar otros
        atributos, por ejemplo, un peso.
    """
    def __init__(self, destino, etiqueta):
        self.destino = destino
        self.etiqueta = etiqueta

#----------------------------------------------------------------

class Grafica:
    """
        Esta clase representa una gráfica y sus operaciones.
    """
    def __init__(self):
        self.__grafica = {} # Estructura donde se va a guardar la gráfica
        self.__num_nodos = 0 # Contador de nodos
        self.__num_aristas = 0 # Contador de aristas
    
    """
        Este método busca un nodo en la gráfica.

        Parametros:
        nodo: Nodo a buscar

        Regresa:
        True si el nodo se encuentra en la gráfica.
        None si el nodo no se encuentra en la gráfica. 
    """
    def buscar_nodo(self, nodo):
        if nodo in self.__grafica:
            return True
        return False
    
    """
        Este método busca una arista. En caso de que un nodo
        tenga varias aristas sin etiqueta hacia otro mismo nodo,
        entonces únicamente se va a eliminar la primer ocurrencia.

        Parámetros
        ----------
        etiqueta: Etiqueta de la arista a buscar

        Regresa
        -------
        Si se encuentra la arista, regresa el nodo en donde se encontró
        Si no se encuentra, entonces regresa None
        
        Si no se encuentra la arista, regresa None, None
    """
    def buscar_arista(self, etiqueta):
        for nodo in self.__grafica:
            for arista in self.__grafica[nodo]:
                if arista.etiqueta == etiqueta:
                    return nodo
        return False
    
    """
        Este método agrega un nodo a la gráfica.

        Parámetros
        ----------
        nodo: Nodo que se desea agregar

    """
    def agregar_nodo(self, nodo):
        # Se busca el nodo en la gráfica, si no está, entonces
        # se agrega y el contador de nodos se incrementa
        if not self.buscar_nodo(nodo):
            self.__grafica[nodo] = []
            self.__num_nodos += 1
            return True
        else:
            return False
    
    """
        Este método agrega una arista a la gráfica

        Parámetros
        ----------
        a: Nodo 1 de la arista.
        b: Nodo 2 de la arista.
        etiqueta: Etiqueta de la arista.
    """
    def agregar_arista(self, a, b, etiqueta):
        # Se agrega el nodo a y después se agrega una arista hacia
        # b con la etiqueta a su lista
        if not self.buscar_arista(etiqueta):
            self.agregar_nodo(a)
            self.__grafica[a].append( Arista(b, etiqueta) )

            # Se agrega el nodo b y después se agrega una arista hacia
            # a con la etiqueta a su lista
            self.agregar_nodo(b)
            self.__grafica[b].append( Arista(a, etiqueta) )

            # El contador de aristas se incrementa
            self.__num_aristas += 1
            
            return True
        else:
            return False

    """
        Este método elimina una arista de la gráfica

        Parámetros
        ----------
        etiqueta: Etiqueta de la arista
    """    
    def eliminar_arista(self, etiqueta):
        # Primero, se busca la arista.
        nodo1 = self.buscar_arista(etiqueta)
        # Si se encontró entonces se pasa a eliminarla de ambos vértices
        if nodo1:
            # Se busca en el nodo1
            for i in range(len(self.__grafica[nodo1])):
                if self.__grafica[nodo1][i].etiqueta == etiqueta:
                    # Se guarda la arista y el otro nodo en el que
                    # incide
                    arista = self.__grafica[nodo1][i]
                    nodo2 = self.__grafica[nodo1][i].destino
                    break
            
            # La arista se elimina del nodo1
            self.__grafica[nodo1].remove(arista)

            # Se busca en el nodo2
            for i in range(len(self.__grafica[nodo2])):
                if self.__grafica[nodo2][i].etiqueta == etiqueta:
                    # Se guarda la arista
                    arista = self.__grafica[nodo2][i]
                    break

            # La arista se elimina del nodo2
            self.__grafica[nodo2].remove(arista)
            
            # Se decrementa el contador de aristas
            self.__num_aristas -= 1
            return True
        else:
            return False

    """
        Este método elimina un nodo de la gráfica

        Parámetros
        ----------
        nodo: Nodo que se quiere eliminar
    """
    def eliminar_nodo(self, nodo):
        # Si se encuentra el nodo, entonces se procede a eliminarlo
        if self.buscar_nodo(nodo):
            # Antes de eliminar el nodo debemos eliminar todas las aristas que
            # inciden en él. Lo hacemos con el método eliminar_arista() y usamos
            # la bandera unSentido=True porque no se necesita borrar la arista del nodo que
            # vamos a eliminar.
            while self.__grafica[nodo]:
                self.eliminar_arista(self.__grafica[nodo][0].etiqueta)
    
            # Cuando todas las aristas del nodo se hayan eliminado procedemos a 
            # eliminar el nodo de la gráfica y decrementamos el contador de nodos
            self.__grafica.pop(nodo)
            self.__num_nodos -= 1
            return True
        else:
            return False
    
    """
        Este método obtiene el grado de un nodo de la gráfica

        Parámetros
        ----------
        nodo: Nodo al que se le va a calcular el grado

        Regresa
        -------
        El grado del nodo
    """
    def obtener_grado(self, nodo):
        # Primero se busca el nodo
        if self.buscar_nodo(nodo):
            # El grado se calcula con la longitud de su lista de aristas
            return len(self.__grafica[nodo])
        return False
    
    """
        Este método obtiene el número de nodos de la gráfica

        Regresa
        -------
        El número de nodos de la gráfica
    """
    def obtener_numero_nodos(self):
        # Simplemente regresamos el valor del contador de nodos
        return self.__num_nodos
    
    """
        Este método obtiene el número de aristas de la gráfica

        Regresa
        -------
        El número de aristas de la gráfica
    """
    def obtener_numero_aristas(self):
        # Simplemente regresamos el valor del contador de aristas
        return self.__num_aristas
    
    """
        Este método elimina todas las aristas de un nodo

        Parámetros
        ----------
        nodo: Nodo del cuál vamos a eliminar las aristas
    """
    def vaciar_nodo(self, nodo):
        # Se elimina cada arista en ambos sentidos
        if self.buscar_nodo(nodo):
            while self.__grafica[nodo]:
                self.eliminar_arista(self.__grafica[nodo][0].etiqueta)
            return True
        else:
            return False
    """
        Este método limpia la gráfica
    """
    def vaciar_grafica(self):
        self.__grafica = {}
        self.__num_nodos = 0
        self.__num_aristas = 0
    
    """
        Este método imprime la gráfica en forma de lista.
        Primero aparecerán todos los nodos, después, todas
        las aristas
    """
    def __str__(self):
        resultado = []
        for nodo in self.__grafica:
            resultado.append(nodo)
            for arista in self.__grafica[nodo]:
                a = (arista.etiqueta, nodo, arista.destino)
                if not (arista.etiqueta, arista.destino, nodo) in resultado:
                    resultado.append(a)
        
        resultado = sorted(resultado, key=len)
        return str(resultado)



if __name__ == "__main__":
    g = Grafica()
    seleccion = ""

    while (seleccion != "13"):
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
        print("13) Salir")

        seleccion = input()
        if validar(seleccion):
            if (int(seleccion) < 1 or int(seleccion) > 13):
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
                    arista = input("Ingrese el nombre del arista que desea eliminar: ")
                    if g.eliminar_arista(arista):
                        print("Arista", arista, "eliminado")
                    else:
                        print("La arista", arista, "no existe")
                    
                    input("\nPresione Enter para continuar...")
                
                if (seleccion == "5"):
                    nodo = input("Ingrese el nombre del nodo: ")
                    if g.buscar_nodo(nodo):
                        print("El nodo", nodo, "existe")
                    else:
                        print("El nodo", nodo, "no existe")
                    
                    input("\nPresione Enter para continuar...")
                    
                if (seleccion == "6"):
                    etiqueta = input("Ingrese la etiqueta de la arista: ")
                    if (g.buscar_arista(etiqueta)):
                        print("La arista", etiqueta, "existe")
                    else:
                        print("La arista", etiqueta, "no existe")
                    
                    input("\nPresione Enter para continuar...")
                
                if (seleccion == "7"):
                    nodo = input("Ingrese el nombre del nodo: ")
                    grado = g.obtener_grado(nodo)
                    if grado:
                        print("El grado del nodo", nodo, "es:", grado)
                    else:
                        print("El nodo", nodo, "no existe")
                            
                    input("\nPresione Enter para continuar...")
                    
                if (seleccion == "8"):
                    print("La grafica tiene", g.obtener_numero_nodos(), "nodos")
                    input("\nPresione Enter para continuar...")
                
                if (seleccion == "9"):
                    print("La grafica tiene", g.obtener_numero_aristas(), "aristas")
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
                    print("La grafica se ha vaciado.")
                    input("\nPresione Enter para continuar...")
                
                if (seleccion == "12"):
                    print(g)
                    input("\nPresione Enter para continuar...")

        else:
            input("Error. Ingrese un número entre 1 y 13. Presione Enter para intentarlo de nuevo...")    