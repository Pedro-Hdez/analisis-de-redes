"""
    Este archivo implementa los nodos como una clase con
    atributos.
    Se le hicieron las modificaciones correspondientes a 
    la clase 'Grafica' para que maneje los nodos de esta
    nueva forma
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

class Nodo:
    """
        Esta clase representa un nodo. Tiene un nombre y una etiqueta que
        siempre será None por defecto.
    """
    def __init__(self, nombre, etiqueta=None):
        self.nombre = nombre
        self.etiqueta = etiqueta

#----------------------------------------------------------------
class Cola:
    """ Representa a una cola, con operaciones de encolar y desencolar.
        El primero en ser encolado es también el primero en ser desencolado.
    """

    def __init__(self):
        """ Crea una cola vacía. """
        # La cola vacía se representa por una lista vacía
        self.items=[]

    def imprimir_cola(self):
        for i in range(len(self.items)):
            print(self.items[i])

    def encolar(self, x):
        """ Agrega el elemento x como último de la cola. """
        self.items.append(x)
    def es_vacia(self):
        """ Devuelve True si la cola esta vacía, False si no."""
        return self.items == []
      
    def desencolar(self):
        """ Elimina el primer elemento de la cola y devuelve su
        valor. Si la cola está vacía, levanta ValueError. """
        try:
            return self.items.pop(0)
        except:
            raise ValueError("La cola está vacía")
        

#----------------------------------------------------------------
class Pila:
    """ Representa una pila con operaciones de apilar, desapilar y
        verificar si está vacía. """

    def __init__(self):
        """ Crea una pila vacía. """
        # La pila vacía se representa con una lista vacía
        self.items=[]
        
    def apilar(self, x):
        """ Agrega el elemento x a la pila. """
        # Apilar es agregar al final de la lista.
        self.items.append(x)

    def es_vacia(self):
    	return self.items == []

    def desapilar(self):
        """ Elimina el primer elemento de la cola y devuelve su
        valor. Si la cola está vacía, levanta ValueError. """
        try:
            return self.items.pop()
        except:
            raise ValueError("La cola está vacía")
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
    def buscar_nodo(self, nombre):
        for nodo in self.__grafica:
            if nodo.nombre == nombre:
                return nodo
        return False 

    """
        Este método agrega un nodo a la gráfica.

        Parámetros
        ----------
        nodo: Nodo que se desea agregar

    """
    def agregar_nodo(self, nombre):
        # Se busca el nodo en la gráfica, si no está, entonces
        # se agrega y el contador de nodos se incrementa
        if self.buscar_nodo(nombre):
            return False
        self.__grafica[Nodo(nombre, None)] = []
        self.__num_nodos += 1
        return True

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
        nodo_nuevo = self.buscar_nodo(a)
        self.__grafica[nodo_nuevo].append( Arista(b, etiqueta) )

        # Se agrega el nodo b y después se agrega una arista hacia
        # a con la etiqueta a su lista
        self.agregar_nodo(b)
        nodo_nuevo = self.buscar_nodo(b)
        self.__grafica[nodo_nuevo].append( Arista(a, etiqueta) )

        # El contador de aristas se incrementa
        self.__num_aristas += 1

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
        if not self.buscar_nodo(a) or not self.buscar_nodo(a):
            return False

        for arista in self.__grafica[self.buscar_nodo(a)]:
            if etiqueta == None:
                if arista.destino == b:
                    return True
            else:
                if arista.destino == b and arista.etiqueta == etiqueta:
                    return True
        return False
    
    """
        Este método elimina una arista de la gráfica

        Parámetros
        ----------
        etiqueta: Etiqueta de la arista
    """    
    def eliminar_arista(self, a, b, etiqueta=None):
        if self.buscar_arista(a, b, etiqueta):
            nodo_a = self.buscar_nodo(a)
            nodo_b = self.buscar_nodo(b)

            for i in range(len(self.__grafica[nodo_a])):
                if etiqueta == None:
                    if self.__grafica[nodo_a][i].destino == b:
                        arista1 = self.__grafica[nodo_a][i]
                        break
                else:
                    if self.__grafica[nodo_a][i].destino == b and self.__grafica[nodo_a][i].etiqueta == etiqueta:
                        arista1 = self.__grafica[nodo_a][i]
                        break
            
            for i in range(len(self.__grafica[nodo_b])):
                if etiqueta == None:
                    if self.__grafica[nodo_b][i].destino == a:
                        arista2 = self.__grafica[nodo_b][i]
                        break
                else:
                    if self.__grafica[nodo_b][i].destino == a and self.__grafica[nodo_b][i].etiqueta == etiqueta:
                        arista2 = self.__grafica[nodo_b][i]
                        break
            
            self.__grafica[nodo_a].remove(arista1)
            self.__grafica[nodo_b].remove(arista2)
            self.__num_aristas -= 1
            return True

        return False

    """
        Este método elimina un nodo de la gráfica

        Parámetros
        ----------
        nodo: Nodo que se quiere eliminar
    """
    def eliminar_nodo(self, nombre):
        # Si se encuentra el nodo, entonces se procede a eliminarlo
        nodo = self.buscar_nodo(nombre)
        if nodo:
            # Antes de eliminar el nodo debemos eliminar todas las aristas que
            # inciden en él. Lo hacemos con el método eliminar_arista() y usamos
            # la bandera unSentido=True porque no se necesita borrar la arista del nodo que
            # vamos a eliminar.
            while self.__grafica[nodo]:
                self.eliminar_arista(nombre, self.__grafica[nodo][0].destino)
    
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
    def obtener_grado(self, nombre):
        # Primero se busca el nodo
        nodo = self.buscar_nodo(nombre)
        if nodo:
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
    def vaciar_nodo(self, nombre):
        # Se elimina cada arista en ambos sentidos
        nodo = self.buscar_nodo(nombre)
        if nodo:
            while self.__grafica[nodo]:
                self.eliminar_arista(nombre, self.__grafica[nodo][0].destino)
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
        return copy.deepcopy(self)
    
    def __limpiar_etiquetas(self):
        for nodo in self.__grafica:
            nodo.etiqueta = None

    def es_bipartita(self):
        # Se iteran todos los nodos de la gráfica
        for nodo_inicial in self.__grafica:
            # Se el nodo inicial no tiene etiqueta, entonces se
            # agrega directamente a la partición 1
            if not nodo_inicial.etiqueta:
                nodo_inicial.etiqueta = 1
            
            # Se iteran todos los nodos adyacentes al nodo inicial
            for arista in self.__grafica[nodo_inicial]:
                nodo_adyacente = self.buscar_nodo(arista.destino)
                # Si el nodo adyacente no tiene etiqueta, entonces
                # se agrega a la partición contraria del nodo inicial
                if not nodo_adyacente.etiqueta:
                    if nodo_inicial.etiqueta == 1:
                        nodo_adyacente.etiqueta = 2
                    else:
                        nodo_adyacente.etiqueta = 1
                else:
                    # Si el nodo adyacente sí tiene etiqueta, entonces 
                    # se revisa que no sea igual a la etiqueta del nodo inicial.
                    # en ese caso, la gráfica no es bipartita.
                    if nodo_adyacente.etiqueta != nodo_inicial.etiqueta:
                        continue
                    else:
                        return None, None
        
        # Si se lograron etiquetar todos los nodos de la gráfica sin conflicto, 
        # entonces la gráfica es bipartita y se regresan las particiones
        return [n.nombre for n in self.__grafica if n.etiqueta == 1], [n.nombre for n in self.__grafica if n.etiqueta == 2]
	
    def diccionario(self):
    	return self.__grafica
    
    def paseo_euler(self):
        nodos_iniciales = []
        copia = self.copiar().diccionario()
        
        
        # Se cuentan los nodos con grado impar
        for nodo in self.__grafica:
            if len(self.__grafica[nodo]) % 2 != 0:
                nodos_iniciales.append(nodo)
                
        if len(nodos_iniciales) > 0 and len(nodos_iniciales) != 2:
        	return False
        
        # Cola y pila del algoritmo
        cola = Cola()
        pila = Pila()
        
        # Si existen nodos iniciales, los tomamos (Paseo abierto desde vp a vc)
        if nodos_iniciales:
            vp = nodos_iniciales[0]
            vc = nodos_iniciales[1]
        else:
            vp = vc = list(self.__grafica.items())[0][0]
        
        # Si no, tomamos por default el primer nodo (Paseo cerrado)

        cola.encolar(vc)
        pila.apilar(vp)
        
        while(self.obtener_grado(vp.nombre)>0 and self.obtener_grado(vc.nombre)>0):

            # Se iteran todos los nodos adyacentes al nodo inicial
            for arista in self.__grafica[vc]:
                nodo_adyacente = self.buscar_nodo(arista.destino)
                if(self.obtener_grado(nodo_adyacente.nombre)>1):
                    self.eliminar_arista(vc.nombre,nodo_adyacente.nombre,arista.etiqueta)
                    vc = nodo_adyacente
                    cola.encolar(vc)
                    break
            if(self.obtener_grado(vp.nombre)==1):
                arista_adyacente = self.__grafica[vp][0]
                self.eliminar_arista(vp.nombre,arista_adyacente.destino,arista_adyacente.etiqueta)
                vp = self.buscar_nodo(arista_adyacente.destino)
                pila.apilar(vp)

        
        pila.desapilar()
        paseo = []
        while(not cola.es_vacia()):
            paseo.append(cola.desencolar().nombre)
         
        while not pila.es_vacia():
            paseo.append(pila.desapilar().nombre)
         
        self.__grafica = copia
        return paseo
        

        
       
    def __str__(self):
        resultado = []
        for nodo in self.__grafica:
            resultado.append(nodo.nombre)
            for arista in self.__grafica[nodo]:
                a = (arista.etiqueta, nodo.nombre, arista.destino)
                if not (arista.etiqueta, arista.destino, nodo.nombre) in resultado:
                    resultado.append(a)
        
        resultado = sorted(resultado, key=len)
        return str(resultado)