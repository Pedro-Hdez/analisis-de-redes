"""
    Este archivo contiene la implementación de la clase
    gráfica en su forma más simple. No maneja los nodos
    como clases con atributos
"""
import copy

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
        Este método lee una gráfica desde un archivo
    """
    def leer_grafica(self, archivo):
        file1 = open(archivo, 'r') 
        Lines = file1.readlines() 

        for line in Lines:
            line = line.strip().split(",")
            length = len(line)
            if length == 1:
                self.agregar_nodo(line[0])
            elif length == 2:
                self.agregar_arista(line[0], line[1])
            else:
                self.agregar_arista(line[0], line[1], line[2])
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
        else:
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
    def buscar_arista(self, a, b, etiqueta=None):
        for arista in self.__grafica[a]:
            if etiqueta == None:
                if arista.destino == b:
                    return True
            else:
                if arista.destino == b and arista.etiqueta == etiqueta:
                    return True
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
    def agregar_arista(self, a, b, etiqueta=None):
        self.agregar_nodo(a)
        self.__grafica[a].append( Arista(b, etiqueta) )

        # Se agrega el nodo b y después se agrega una arista hacia
        # a con la etiqueta a su lista
        self.agregar_nodo(b)
        self.__grafica[b].append( Arista(a, etiqueta) )

        # El contador de aristas se incrementa
        self.__num_aristas += 1

    """
        Este método elimina una arista de la gráfica
        Parámetros
        ----------
        etiqueta: Etiqueta de la arista
    """    
    def eliminar_arista(self, a, b, etiqueta=None):
        if self.buscar_arista(a, b):
            for i in range(len(self.__grafica[a])):
                if etiqueta == None:
                    if self.__grafica[a][i].destino == b:
                        arista1 = self.__grafica[a][i]
                        break
                else:
                    if self.__grafica[a][i].destino == b and self.__grafica[a][i].etiqueta == etiqueta:
                        arista1 = self.__grafica[a][i]
                        break
            
            for i in range(len(self.__grafica[b])):
                if etiqueta == None:
                    if self.__grafica[b][i].destino == a:
                        arista2 = self.__grafica[b][i]
                        break
                else:
                    if self.__grafica[b][i].destino == a and self.__grafica[b][i].etiqueta == etiqueta:
                        arista2 = self.__grafica[b][i]
                        break
            
            self.__grafica[a].remove(arista1)
            self.__grafica[b].remove(arista2)
            self.__num_aristas -= 1
            return True

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
                self.eliminar_arista(nodo, self.__grafica[nodo][0].destino)
    
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
                self.eliminar_arista(nodo, self.__grafica[nodo][0].destino)
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

    def copiar(self):
        return copy.copy(self)

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