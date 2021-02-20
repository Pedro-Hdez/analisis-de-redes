"""
    Este archivo implementa los nodos como una clase con
    atributos.
    Se le hicieron las modificaciones correspondientes a 
    la clase 'Grafica' para que maneje los nodos de esta
    nueva forma
"""

import copy
import operator

class Arista:
    """
        Esta clase representa una arista. Tiene un nodo destino
        y una etiqueta. De esta forma es más fácil agregar otros
        atributos, por ejemplo, un peso.
    """
    def __init__(self, destino, peso, etiqueta):
        self.destino = destino
        self.etiqueta = etiqueta
        self.peso = peso

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
        self.__heap = {}

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
    def agregar_arista(self, a, b, etiqueta=None, peso=None):
        self.agregar_nodo(a)
        nodo_nuevo = self.buscar_nodo(a)
        self.__grafica[nodo_nuevo].append( Arista(b, etiqueta, peso) )

        # Se agrega el nodo b y después se agrega una arista hacia
        # a con la etiqueta a su lista
        self.agregar_nodo(b)
        nodo_nuevo = self.buscar_nodo(b)
        self.__grafica[nodo_nuevo].append( Arista(a, etiqueta, peso) )

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
            elif length == 3:
                self.agregar_arista(line[0], line[1], line[2])
            else:
              	self.agregar_arista(line[0], line[1], line[2], line[4])
                

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
    def buscar_arista(self, a, b, etiqueta=None, peso=None):
        if not self.buscar_nodo(a) or not self.buscar_nodo(b):
            return False
          
        for arista in self.__grafica[self.buscar_nodo(a)]:
            if etiqueta == None:
                if arista.destino == b and arista.peso == peso:
                    return True
            elif peso == None:
              	if arista.destino == b and arista.etiqueta == etiqueta:
                	return True
            elif not etiqueta and not peso:
                if arista.destino == b:
                    return True
            else:
              	if arista.destion == b and arista.destino == etiqueta and arista.peso == peso:
                  	return True
              	
        return False
    
    """
        Este método elimina una arista de la gráfica

        Parámetros
        ----------
        etiqueta: Etiqueta de la arista
    """    
    def eliminar_arista(self, a, b, etiqueta=None, peso=None):
        if self.buscar_arista(a, b, etiqueta):
            nodo_a = self.buscar_nodo(a)
            nodo_b = self.buscar_nodo(b)
            
            for i in range(len(self.__grafica[nodo_a])):
                if etiqueta == None:
                    if self.__grafica[nodo_a][i].destino == b and self.__grafica[nodo_a][i].peso == peso:
                        arista1 = self.__grafica[nodo_a][i]
                        break
                elif peso == None:
                    if self.__grafica[nodo_a][i].destino == b and self.__grafica[nodo_a][i].etiqueta == etiqueta:
                        arista1 = self.__grafica[nodo_a][i]
                        break
                elif not etiqueta and not peso:
                    if self.__grafica[nodo_a][i].destino == b:
                        arista1 = self.__grafica[nodo_a][i]
                        break
                else:
                    if self.__grafica[nodo_a][i].destino == b and self.__grafica[nodo_a][i].peso == peso and self.__grafica[nodo_a][i].etiqueta == etiqueta:
                        arista1 = self.__grafica[nodo_a][i]
                        break
            
            for i in range(len(self.__grafica[nodo_b])):
                if etiqueta == None:
                    if self.__grafica[nodo_b][i].destino == a and self.__grafica[nodo_b][i].peso == peso:
                        arista2 = self.__grafica[nodo_b][i]
                        break
                    elif peso == None:
                        if self.__grafica[nodo_b][i].destino == a and self.__grafica[nodo_b][i].etiqueta == etiqueta:
                            arista2 = self.__grafica[nodo_b][i]
                            break
                    elif not etiqueta and not peso:
                        if self.__grafica[nodo_b][i].destino == a:
                            arista2 = self.__grafica[nodo_b][i]
                            break
                    else:
                        if self.__grafica[nodo_b][i].destino == a and self.__grafica[nodo_b][i].peso == peso and self.__grafica[nodo_b][i].etiqueta == etiqueta:
                            arista = self.__grafica[nodo_b][i]
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
            for arista in self.__grafica[nodo]:
                arista.etiqueta = None
    
    def __buscar_particiones(self, nodos):
        for nodo_inicial in nodos:
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
                        self.__limpiar_etiquetas()
                        return None, None
        
        # Si se lograron etiquetar todos los nodos de la gráfica sin conflicto, 
        # entonces la gráfica es bipartita y se regresan las particiones
        self.__limpiar_etiquetas()
        return [n.nombre for n in self.__grafica if n.etiqueta == 1], [n.nombre for n in self.__grafica if n.etiqueta == 2]

    def es_bipartita(self):
        # Se obtienen todos los nodos de la gráfica. Servirá para reordenar los nodos
        # y así comenzar con uno diferente cada vez
        nodos = [n for n in self.__grafica]

        # El proceso de etiquetado se repetirá, de ser necesario, tantas veces como
        # nodos tengamos en la gráfica
        for _ in range(len(nodos)):
            # Se buscan las particiones
            particion1, particion2 = self.__buscar_particiones(nodos)
            # Si existen las particiones, entonces se regresan
            if particion1:
                return particion1, particion2
            # Si no existen las particiones, entonces se reordena la lista de nodos.
            # Movemos el último elemento hasta el inicio para así tomar un nuevo nodo inicial
            # al momento de etiquetar
            nodos.insert(0, nodos.pop())
        
        # Si al final probamos el etiquetado iniciando con todos y cada uno de los nodos y siempre
        # falló, entonces la gráfica no es bipartita
        return None, None
    
    def diccionario(self):
    	return self.__grafica
    
    def es_conexa(self):
        """
            Este método hace una búsqueda a lo profundo en cada nodo
            para saber si la gráfica es conexa
        """

        # Algoritmo de búsqueda
        visitados = []
        pila = Pila()
        pila.apilar(list(self.__grafica.items())[0][0].nombre)
        while not pila.es_vacia():
            nodo_actual = pila.desapilar()
            for arista in self.__grafica[self.buscar_nodo(nodo_actual)]:
                nodo_adyacente = arista.destino
                if nodo_adyacente not in visitados:
                    pila.apilar(nodo_adyacente)
            if nodo_actual not in visitados:
                visitados.append(nodo_actual)

        # Si la gráfica es conexa, entonces todos los nodos deberían
        # estar presentes en la lista de visitados
        for nodo in self.__grafica:
            if nodo.nombre not in visitados:
                return False
        return True
    
    def paseo_euler(self):
        if not self.es_conexa():
            return False

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
    
    """
        Este método verifica si todos los nodos de la gráfica ya se encuentran 
        marcados
    """
    def __todos_nodos_marcados(self):
        for nodo in self.__grafica:
            if nodo.etiqueta == None:
                return False
        return True
    
    """
        Esta función ejecuta una búsqueda a profundidad en la gráfica para encontrar árboles de
        expansión.

        Regresa
        -------

        bosque: lista de listas. Cada lista corresponde al árbol de expansión
                de una componente de la gráfica. Cada arista de los árboles
                de expansión se representan con una tupla.
    """
    def busqueda_a_profundidad(self):
        # Lista en donde se almacenarán los árboles de expansión para cada
        # componente de la gráfica
        bosque = [] 

        # Lista de los nodos que no han sido etiquetados por el algoritmo
        nodos_sin_etiqueta = [nodo for nodo in self.__grafica if not nodo.etiqueta]

        # Etiqueta para identificar el árbol de expansión de la componente en cuestión
        etiqueta_actual = 1

        # Mientras existan nodos sin etiquetar se efectuará el algoritmo de 
        # búsqueda
        while nodos_sin_etiqueta:

            # ----- ALGORITMO DE BÚSQUEDA A PROFUNDIDAD -----
            
            # Pila auxiliar del algoritmo
            pila = Pila()

            # Se toma el primer vértice y se etiqueta
            v = nodos_sin_etiqueta[0]
            v.etiqueta = etiqueta_actual

            # Mientras falte algún nodo por etiquetar en la gráfica se continúa            
            while not self.__todos_nodos_marcados():
                # Se buscan las aristas de v sin marcar
                aristas_validas = [a for a in self.__grafica[v] if not self.buscar_nodo(a.destino).etiqueta]
                
                # Si existen aristas válidas, entonces se marca la arista y el otro
                # extremo; además se apila v y se hace v = w. Luego, se repite el algoritmo
                # hasta este punto
                if aristas_validas:
                    arista = aristas_validas[0]
                    w = self.buscar_nodo(arista.destino)

                    arista.etiqueta = etiqueta_actual
                    w.etiqueta = etiqueta_actual
                    pila.apilar(v)
                    v = w
                    continue
                
                # Si no existen aristas válidas y la pila tiene elementos, entonces
                # se desapila un elemento y se repite el algoritmo hasta este punto
                if not pila.es_vacia():
                    v = pila.desapilar()
                # Si la pila ya está vacía, continuar con la siguiente parte del algoritmo
                else:
                    break
            
            # Si quedaron vértices sin marcar, la gráfica no es conexa, de lo contrario,
            # las aristas marcadas corresponden al árbol de expansión 

            # Se forma el árbol de expansión de la componente en cuestión
            # buscando todas las aristas que tengan la etiqueta actual
            arbol_expansion = []
            for nodo in self.__grafica:
                for arista in self.__grafica[nodo]:
                    if arista.etiqueta == etiqueta_actual:
                        arbol_expansion.append((nodo.nombre, arista.destino))
            
            # Si el arbol de expansion contiene aristas, entonces se ordenan
            if arbol_expansion:
                arbol_expansion.sort(key=lambda x:x[0])
            # Si el árbol de expansión no contiene aristas, significa que la componente
            # actual está formada de un solo vértice, así que éste se agrega al árbol
            else:
                arbol_expansion.append(nodos_sin_etiqueta[0].nombre)
            # Se añade el árbol de expansión de la componente en cuestión a nuestro
            # bosque
            bosque.append(arbol_expansion)

            # Se actualiza la lista de nodos sin etiqueta y la etiqueta actual
            nodos_sin_etiqueta = [n for n in self.__grafica if not n.etiqueta]
            etiqueta_actual += 1
        
        # Al final, después de que todos los nodos de la gráfica están etiquetados,
        # se regresa el bosque que se encontró
        self.__limpiar_etiquetas()
        return bosque


    """
        Esta función ejecuta una búsqueda a lo ancho en la gráfica para encontrar árboles de
        expansión.

        Regresa
        -------

        bosque: lista de listas. Cada lista corresponde al árbol de expansión
                de una componente de la gráfica. Cada arista de los árboles
                de expansión se representan con una tupla.
    """
    def busqueda_a_lo_ancho(self):
        # Lista en donde se almacenarán los árboles de expansión para cada
        # componente de la gráfica
        bosque = [] 

        # Lista de los nodos que no han sido etiquetados por el algoritmo
        nodos_sin_etiqueta = [nodo for nodo in self.__grafica if not nodo.etiqueta]

        # Etiqueta para identificar el árbol de expansión de la componente en cuestión
        etiqueta_actual = 1

        # Mientras existan nodos sin etiquetar se efectuará el algoritmo de 
        # búsqueda
        while nodos_sin_etiqueta:

            # ----- ALGORITMO DE BÚSQUEDA A LO ANCHO -----

            # Cola auxiliar del algoritmo
            cola = Cola()

            # Se elige un vértice no etiquetado, se etiqueta y se encola
            v = nodos_sin_etiqueta[0]
            v.etiqueta = etiqueta_actual
            cola.encolar(v)

            # El algoritmo continúa mientras la cola no esté vacía y 
            # haya vértices sin marcar
            while not cola.es_vacia() and not self.__todos_nodos_marcados():
                # Se desencola un vértice t
                t = cola.desencolar()

                # Se marcan todas las aristas de t tal que su otro extremo w
                # no esté marcado; además, se encola a w
                for arista in self.__grafica[t]:
                    w = self.buscar_nodo(arista.destino)
                    if not w.etiqueta:
                        arista.etiqueta = etiqueta_actual
                        w.etiqueta = etiqueta_actual
                        cola.encolar(w)
            
            # Si quedaron vértices sin marcar, la gráfica no es conexa, de lo contrario,
            # las aristas marcadas corresponden al árbol de expansión 

            # Se forma el árbol de expansión de la componente en cuestión
            # buscando todas las aristas que tengan la etiqueta actual
            arbol_expansion = []
            for nodo in self.__grafica:
                for arista in self.__grafica[nodo]:
                    if arista.etiqueta == etiqueta_actual:
                        arbol_expansion.append((nodo.nombre, arista.destino))
            
            # Si el arbol de expansion contiene aristas, entonces se ordenan
            if arbol_expansion:
                arbol_expansion.sort(key=lambda x:x[0])
            # Si el árbol de expansión no contiene aristas, significa que la componente
            # actual está formada de un solo vértice, así que éste se agrega al árbol
            else:
                arbol_expansion.append(nodos_sin_etiqueta[0].nombre)
            # Se añade el árbol de expansión de la componente en cuestión a nuestro
            # bosque
            bosque.append(arbol_expansion)

            # Se actualiza la lista de nodos sin etiqueta y la etiqueta actual
            nodos_sin_etiqueta = [n for n in self.__grafica if not n.etiqueta]
            etiqueta_actual += 1
        
        # Al final, después de que todos los nodos de la gráfica están etiquetados,
        # se regresa el bosque que se encontró
        self.__limpiar_etiquetas()
        return bosque
    

    def __busqueda(self, v):
        if (v == self.__heap[v]):
            return v
        return self.__busqueda(self.__heap[v])
    
    def __union(self, u, v):
        self.__heap[self.__busqueda(u)] = self.__busqueda(v)

    def algoritmo_kruskal(self):
    	# Introducir todas las aristas a una lista
        aristas = []
        for nodo in self.__grafica:
            for arista in self.__grafica[nodo]:
                a = (nodo.nombre, arista.destino, float(arista.peso)) 
                if a not in aristas:
                    aristas.append((arista.destino, nodo.nombre, float(arista.peso)))
        
        # Ordenar las aristas de mayor a menor de acuerdo a su peso
        aristas.sort(key=lambda a:a[2], reverse=True)
        print("ARISTAS")
        for arista in aristas:
          	print(arista)

        # Crear el heap e inicializarlo
        self.__heap = {}
        for nodo in self.__grafica:
            self.__heap[nodo.nombre] = nodo.nombre
        
        print("HEAP")
        print(self.__heap)

        # Hacer el algoritmo
        arbol = []
        nodos_sin_etiqueta = [nodo.nombre for nodo in self.__grafica]
        print("NODOS SIN ETIQUETA INICIALES")
        print(nodos_sin_etiqueta)
        while (len(arbol) < len(self.__grafica)) and nodos_sin_etiqueta:
            print("HEAP")
            print(self.__heap)
            arista = aristas.pop()
            if not self.__heap[arista[0]] == self.__heap[arista[1]]:
                arbol.append(arista)

                try:
                    nodos_sin_etiqueta.remove(arista[0])
                except:
                    pass
                try:
                    nodos_sin_etiqueta.remove(arista[1])
                except:
                    pass
                
                self.__union(arista[0], arista[1])

        print("ARBOL DE MINIMA EXPANSION") 
        print(arbol)

        print("NODOS SIN ETIQUETA")
        print(nodos_sin_etiqueta)


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