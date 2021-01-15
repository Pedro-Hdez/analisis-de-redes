
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
        self.grafica = {} # Estructura donde se va a guardar la gráfica
        self.num_nodos = 0 # Contador de nodos
        self.num_aristas = 0 # Contador de aristas
    
    """
        Este método busca un nodo en la gráfica.

        Parametros:
        nodo: Nodo a buscar

        Regresa:
        True si el nodo se encuentra en la gráfica.
        None si el nodo no se encuentra en la gráfica. 
    """
    def buscar_nodo(self, nodo):
        if nodo in self.grafica:
            return True
        return None
    
    """
        Este método busca una arista. En caso de que un nodo
        tenga varias aristas sin etiqueta hacia otro mismo nodo,
        entonces únicamente se va a eliminar la primer ocurrencia.

        Parámetros
        ----------
        a: Nodo 1 de la arista a buscar
        b: Nodo 2 de la arista a buscar
        etiqueta: Etiqueta de la arista (None por default)

        Regresa
        -------
        Si se encuentra la arista, regresa arista1, arista2:
            - arista1: Arista dentro de la lista del nodo a
            - arista2: Arista dentro de la lista del nodo b
        
        Si no se encuentra la arista, regresa None, None
    """
    def buscar_arista(self, a, b, etiqueta=None):
        # Variables donde se guardarán los resultados a regresar
        arista1 = None
        arista2 = None

        # Se busca la arista solicitada dentro de la lista del nodo a
        for arista in self.grafica[a]:

            if arista.destino == b and arista.etiqueta == etiqueta:
                arista1 = arista
                break

        # Se busca la arista solicitada dentro de la lista del nodo b
        for arista in self.grafica[b]:
            if arista.destino == a and arista.etiqueta == etiqueta:
                arista2 = arista
                break
        
        # Si se encuentra la arista, entonces se regresan
        if arista1 and arista2:
            return arista1, arista2
        
        # Si no se encontró la arista, entonces se regresa None
        return None, None
    
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
            self.grafica[nodo] = []
            self.num_nodos += 1
    
    """
        Este método agrega una arista a la gráfica

        Parámetros
        ----------
        a: Nodo 1 de la arista.
        b: Nodo 2 de la arista.
        etiqueta: Etiqueta de la arista. None por default.
    """
    def agregar_arista(self, a, b, etiqueta=None):
        # Se agrega el nodo a y después se agrega una arista hacia
        # b con la etiqueta a su lista
        self.agregar_nodo(a)
        self.grafica[a].append( Arista(b, etiqueta) )

        # Se agrega el nodo b y después se agrega una arista hacia
        # a con la etiqueta a su lista
        self.agregar_nodo(b)
        self.grafica[b].append( Arista(a, etiqueta) )

        # El contador de aristas se incrementa
        self.num_aristas += 1

    """
        Este método elimina una arista de la gráfica

        Parámetros
        ----------
        a: Nodo 1 de la arista
        b: Nodo 2 de la arista
        etiqueta: Etiqueta de la arista. None por default
        unSentido: True para eliminar la arista de a y b
                   False para eliminar la arista únicamente de a
    """    
    def eliminar_arista(self, a, b, etiqueta=None, unSentido=False):
        # Primero se busca la arista que se quiere eliminar
        arista1, arista2 = self.buscar_arista(a, b, etiqueta=etiqueta)

        # Si existe, entonces se procede a eliminar
        if arista1 and arista2:
            # Primero se elimina de la lista de aristas de a y el
            # contador de aristas se decrementa
            self.grafica[a].remove(arista1)
            self.num_aristas -= 1
            
            # Si unSentido = True, entonces la arista también se elimina
            # de la lista de b
            if not unSentido:
                self.grafica[b].remove(arista2)
    
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
            for arista in self.grafica[nodo]:
                self.eliminar_arista(arista.destino, nodo, etiqueta=arista.etiqueta, unSentido=True)
    
            # Cuando todas las aristas del nodo se hayan eliminado procedemos a 
            # eliminar el nodo de la gráfica y decrementamos el contador de nodos
            _ = self.grafica.pop(nodo)
            self.num_nodos -= 1
    
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
            return len(self.grafica[nodo])
    
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
        return self.num_aristas
    
    """
        Este método elimina todas las aristas de un nodo

        Parámetros
        ----------
        nodo: Nodo del cuál vamos a eliminar las aristas
    """
    def vaciar_nodo(self, nodo):
        # Se elimina cada arista en ambos sentidos
        while self.grafica[nodo]:
            self.eliminar_arista(nodo,
                                 self.grafica[nodo][0].destino,
                                 self.grafica[nodo][0].etiqueta)
    """
        Este método limpia la gráfica
    """
    def vaciar_grafica(self):
        self.grafica = {}
        self.num_nodos = 0
        self.num_aristas = 0
    
    """
        Este método imprime la gráfica en forma de lista.
        Primero aparecerán todos los nodos, después, todas
        las aristas
    """
    def __str__(self):
        resultado = []
        for nodo in self.grafica:
            resultado.append(nodo)
            for arista in self.grafica[nodo]:
                a = (arista.etiqueta, nodo, arista.destino)
                if not (arista.etiqueta, arista.destino, nodo) in resultado:
                    resultado.append(a)
        
        resultado = sorted(resultado, key=len)
        return str(resultado)



if __name__ == "__main__":
    g = Grafica()
    g.agregar_nodo("a")
    g.agregar_nodo("b")
    g.agregar_nodo("c")

    g.agregar_arista("a", "b", "v1")
    g.agregar_arista("a", "b", "v2")
    g.agregar_arista("a", "b", "v3")
    print(g)

    g.eliminar_nodo("a")
    print(g)