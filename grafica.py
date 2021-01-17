
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
        return None
    
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
        return None
    
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
            self.num_nodos += 1
        else:
            print("El nodo", nodo, "ya existe.")
    
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
        else:
            print("La arista", etiqueta, "ya existe")

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
        else:
            print("La arista", etiqueta, "no existe")

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
            self.num_nodos -= 1
        else:
            print("El nodo", nodo, "no existe")
    
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
    
    """
        Este método obtiene el número de nodos de la gráfica

        Regresa
        -------
        El número de nodos de la gráfica
    """
    def obtener_numero_nodos(self):
        # Simplemente regresamos el valor del contador de nodos
        return self.num_nodos
    
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
        else:
            print("El nodo", nodo, "no existe")
    """
        Este método limpia la gráfica
    """
    def vaciar_grafica(self):
        self.__grafica = {}
        self.num_nodos = 0
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

    g.agregar_arista("1", "2", "v1")
    print(g)

    g.agregar_arista("1", "2", "v1")
    print(g)
