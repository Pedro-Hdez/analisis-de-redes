import copy
import operator
import math
from estructuras_datos import *

class Arco:
    """
        Esta clase representa un arco. Tiene nodos de origen y destino, además de un peso
        y una etiqueta.
    """
    def __init__(self, origen, destino, peso=None, etiqueta=None):
        self.origen = origen
        self.destino = destino
        self.peso = peso
        self.etiqueta = etiqueta
#----------------------------------------------------------------

class Nodo:
    """
        Esta clase representa un nodo. Tiene un nombre, una etiqueta y 
        grados positivo y negativo.
    """
    def __init__(self, nombre, etiqueta=None):
        self.nombre = nombre
        self.etiqueta = etiqueta
        self.grado_positivo = 0
        self.grado_negativo = 0


#----------------------------------------------------------------
class Digrafica:
    """
        Esta clase representa una gráfica dirigia y sus operaciones.
    """
    def __init__(self):
        self.__digrafica = {} # Estructura donde se va a guardar la gráfica
        self.__num_nodos = 0 # Contador de nodos
        self.__num_arcos = 0 # Contador de arcos

    def buscar_nodo(self, nombre):
        """
            Este método busca un nodo en la gráfica.

            Parametros:
            ----------
            nodo: Nodo a buscar

            Regresa:
            -------
            True si el nodo se encuentra en la digráfica.
            None si el nodo no se encuentra en la digráfica. 
        """
        for nodo in self.__digrafica:
            if nodo.nombre == nombre:
                return nodo
        return False 

    def agregar_nodo(self, nombre):
        """
            Este método agrega un nodo a la digráfica.

            Parámetros
            ----------
            nodo: Nodo que se desea agregar

            Regresa
            -------
            False: Si el nodo a agregar ya existe
            True: Si el nodo a agregar no existía en la digráfica.

        """
        # Se busca el nodo en la gráfica, si ya existe, se regresa False
        if self.buscar_nodo(nombre):
            return False
        
        # Si el nuevo nodo no existe, entonces se crea y se le añade un diccionario
        # con dos listas vacías, la lista de nodos "entrantes" y la lista de nodos "salientes"
        nodo = Nodo(nombre, etiqueta=None)
        self.__digrafica[nodo] = {"entrantes":[], "salientes":[]}

        # El número de nodos en la digráfica se incrementa y se regresa True
        self.__num_nodos += 1
        return True

    def agregar_arco(self, a, b, peso=None):
        """
            Este método agrega un arco a la digráfica

            Parámetros
            ----------
            a: Nodo de origen.
            b: Nodo destino.
            peso: Peso del arco.
        """
        # Se agregan los nodos a y b (Esto porque le damos la opción al usuario de 
        # agregar arcos directamente sin la necesidad de que los nodos ya existan
        # en la digráfica)
        self.agregar_nodo(a)
        self.agregar_nodo(b)

        # Se obtienen los nodos a y b
        nodo_a = self.buscar_nodo(a)
        nodo_b = self.buscar_nodo(b)

        # Se construye el arco (a,b)
        arco = Arco(nodo_a, nodo_b, peso)

        # Se agrega el arco (a,b) a los salientes de a, y el grado positivo de a 
        # se incrementa en 1
        self.__digrafica[nodo_a]["salientes"].append(arco)
        nodo_a.grado_positivo += 1

        # Se agrega el arco (a,b) a los entrantes de b, y el grado negativo de b 
        # se incrementa en 1
        self.__digrafica[nodo_b]["entrantes"].append(arco)
        nodo_b.grado_negativo += 1

        # El contador de arcos se incrementa
        self.__num_arcos += 1
        
        return True

    def leer_digrafica(self, archivo):
        """
            Este método lee una digráfica desde un archivo

            Parámetros
            ----------
            archivo: Ruta del archivo de texto en donde se encuentra la información
                     de la digráfica de la siguiente manera y separado con Enters:
                     a -> Para agregar el nodo a
                     a,b -> Para agregar el arco (a,b)
                     a,b,5 -> Para agregar el arco (a,b) con peso 5
        """
        file1 = open(archivo, 'r') 
        Lines = file1.readlines() 

        for line in Lines:
            line = line.strip().split(",")
            length = len(line)
            if length == 1:
                self.agregar_nodo(line[0])
            elif length == 2:
                self.agregar_arco(line[0], line[1])
            elif length == 3:
                self.agregar_arco(line[0], line[1], float(line[2]))

    def buscar_arco(self, a, b, peso=None):
        """
            Este método busca un arco entre dos nodos

            Parámetros
            ----------
            a: Nodo de origen del arco a buscar.
            b: Nodo destino del arco a buscar.
            peso (None por default): Peso del arco a buscar 

            Regresa
            -------
            arco: Si existe, regresa el objeto de la clase Arco que tiene como origen al nodo a, 
                  como destino al nodo b y con peso = peso (en caso de que se haya proporcionado 
                  un peso).
            False: Si el arco no existe.
        """
        # Se busca el nodo de origen
        nodo_a = self.buscar_nodo(a)

        # Si el nodo de origen no existe, la arista buscada tampoco. Se regresa False
        if not nodo_a:
            return False
        
        # Si el nodo de origen sí existe, entonces se busca el arco en sus salientes
        for arco in self.__digrafica[nodo_a]["salientes"]:
            # Si no se ha especificado un peso, entonces solamente se compara el 
            # nombre del nodo destino
            if peso == None:
                if arco.destino.nombre == b:
                    return arco
            # Si el peso se ha especificado, entonces se compara el nombre del nodo 
            # destino y el peso del arco
            else:
                if arco.destino.nombre == b and arco.peso == peso:
                    return arco 
        
        # Si se recorrieron todos los salientes del nodo de origen y no se encontró
        # el arco buscado, entonces se regresa False
        return False
    
    def eliminar_arco(self, a, b, peso=None):
        """
            Este método elimina un arco de la digráfica

            Parámetros
            ----------
            a: Nodo de origen del arco
            b: Nodo destino del arco
            peso (None por default): peso del arco

            Regresa
            -------
            True: Si el arco pudo eliminarse (si existía)
            False: Si el arco no pudo eliminarse (si no existía)
        """    

        # Se busca el arco
        arco = self.buscar_arco(a, b, peso)

        # Si existe el arco, entonces se procede a elminarlo
        if arco:
            # El arco se elimina de los salientes del nodo de origen y el peso positivo
            # de éste se decrementa
            nodo_origen = arco.origen
            self.__digrafica[nodo_origen]["salientes"].remove(arco)
            nodo_origen.grado_positivo -= 1

            # El arco se elimina de los entrantes del nodo destino y el peso negativo
            # de éste se decrementa
            nodo_destino = arco.destino
            self.__digrafica[nodo_destino]["entrantes"].remove(arco)
            nodo_destino.grado_negativo -= 1

            # Se decrementa el número de arcos de la digráfica
            self.__num_arcos -= 1

            # Se regresa True para indicar que el arco se pudo eliminar
            return True
            
        # Si el arco no existe, entonces se regresa False
        return False

    def eliminar_nodo(self, nombre):
        """
            Este método elimina un nodo de la digráfica

            Parámetros
            ----------
            nombre: Nombre del nodo que se quiere eliminar

            Regresa
            -------
            True: Si el nodo pudo eliminarse (Sí existía)
            False: Si el nodo no pudo eliminarse (No existía)
        """
        # Si se encuentra el nodo, entonces se procede a eliminarlo
        nodo = self.buscar_nodo(nombre)

        # Para eliminar el nodo, primero necesitamos eliminar sus salientes y entrantes
        if nodo:
            # Se eliminan todos los arcos salientes
            while self.__digrafica[nodo]["salientes"]:
                arco = self.__digrafica[nodo]["salientes"][0]
                self.eliminar_arco(arco.origen.nombre, arco.destino.nombre)
            
            # Se eliminan todos los arcos entrantes
            while self.__digrafica[nodo]["entrantes"]:
                arco = self.__digrafica[nodo]["entrantes"][0]
                self.eliminar_arco(arco.origen.nombre, arco.destino.nombre)

            # Cuando todos los arcos incidentes en el nodo se hayan eliminado procedemos a 
            # eliminar el nodo de la digráfica y decrementamos el contador de nodos
            self.__digrafica.pop(nodo)
            self.__num_nodos -= 1

            return True
        else:
            return False
    
    def obtener_grado(self, nombre, tipo="positivo"):
        """
            Este método obtiene el grado positivo de un nodo de la gráfica

            Parámetros
            ----------
            nombre: Nombre del nodo al que se le va a calcular el grado
            tipo: Tipo del grado
                - "positivo" (por default) para el grado positivo
                - "negativo" para el grado negativo

            Regresa
            -------
            - El grado del nodo si éste existe en la digráfica
            - False si el nodo no solicitado no existe en la digráfica.
        """
        # Primero se busca el nodo
        nodo = self.buscar_nodo(nombre)
        # Si exist se regresa el tipo de grado especificado
        if nodo:
            return nodo.grado_negativo if tipo == "negativo" else nodo.grado_positivo
        
        # Si el nodo no existe regresa False
        return False
    
    def obtener_numero_nodos(self):
        """
            Este método obtiene el número de nodos de la gráfica

            Regresa
            -------
            El número de nodos de la gráfica
        """
        # Simplemente regresamos el valor del contador de nodos
        return self.__num_nodos
    
    def obtener_numero_arcos(self):
        """
            Este método obtiene el número de aristas de la gráfica

            Regresa
            -------
            El número de aristas de la gráfica
        """
        # Simplemente regresamos el valor del contador de aristas
        return self.__num_arcos
    
    def vaciar_nodo(self, nombre):
        """
            Este método elimina todos los arcos incidentes de un nodo

            Parámetros
            ----------
            nombre: Nombre del nodo que vamos a vaciar

            Regresa
            -------
            - True si el nodo pudo ser vaciado (si existía en la digráfica)
            - False si el nodo no pudo ser vaciado (si no existía en la digráfica)
        """
        # Si se encuentra el nodo, entonces se procede a vaciarlo
        nodo = self.buscar_nodo(nombre)

        if nodo:
            # Se eliminan todos los arcos salientes
            while self.__digrafica[nodo]["salientes"]:
                arco = self.__digrafica[nodo]["salientes"][0]
                self.eliminar_arco(arco.origen.nombre, arco.destino.nombre)
            
            # Se eliminan todos los arcos entrantes
            while self.__digrafica[nodo]["entrantes"]:
                arco = self.__digrafica[nodo]["entrantes"][0]
                self.eliminar_arco(arco.origen.nombre, arco.destino.nombre)
            
            # Se regresa True
            return True
        else:
            # Si el nodo no existe se regresa False
            return False

    def vaciar_grafica(self):
        """
            Este método limpia la gráfica
        """
        self.__digrafica = {}
        self.__num_nodos = 0
        self.__num_arcos = 0
    

    def copiar(self):
        """
            Este método realiza una copia de la gráfica

            Regresa
            -------
            Objeto de la clase Digráfica que representa la copia del objeto actual.
        """
        return copy.deepcopy(self)
    
    def __limpiar_etiquetas(self, tipo):
        """
            Este método limpia las etiquetas de los nodos y/o aristas de la gráfica

            Parámetros
            ----------

            tipo: Tipo del objeto del que deseamos eliminar las etiquetas
                - "nodos": Para limpiar las etiquetas de los nodos
                - "arcos": Para limpiar las etiquetas de los arcos
                - "todo": Para limpiar las etiquetas de todos los arcos y aristas
        """
        if tipo == "nodos":
            for nodo in self.__digrafica:
                nodo.etiqueta = None
        elif tipo == "aristas":
            for nodo in self.__digrafica:
                for arco in self.__digrafica[nodo]["entrantes"]:
                    arco.etiqueta = None
                for arco in self.__digrafica[nodo]["salientes"]:
                    arco.etiqueta = None
        elif tipo == "todo":
            for nodo in self.__digrafica:
                for arco in self.__digrafica[nodo]["entrantes"]:
                    arco.etiqueta = None
                for arco in self.__digrafica[nodo]["salientes"]:
                    arco.etiqueta = None
        else:
            raise ValueError(f"Error en el tipo dado ({tipo}). Valores aceptados: 'nodos', 'aristas', 'todos'")

    def __str__(self):
        """
            Este método imprime la digráfica
        """
        resultado = ""
        for nodo in self.__digrafica:
            resultado += f"Nodo: {nodo.nombre}\nEntrantes: "
            for arco in self.__digrafica[nodo]["entrantes"]:
                if arco.peso:
                    resultado += f"({arco.origen.nombre}, {arco.peso}), "
                else:
                    resultado += f"{arco.origen.nombre}, "

            resultado = resultado[:-2] + "\nSalientes: "

            for arco in self.__digrafica[nodo]["salientes"]:
                if arco.peso:
                    resultado += f"({arco.destino.nombre}, {arco.peso}), "
                else:
                    resultado += f"{arco.destino.nombre}, "
            
            resultado = resultado[:-2] + "\n\n"
        
        resultado = resultado[:-2]

        return resultado 
    

    def __recuperar_ruta(self, nodo_actual, nodo_inicial):
        # Comenzamos la recuperación de la ruta en el nodo actual
        ruta = []

        arista_antecesor = nodo_actual.etiqueta["antecesor"]
        # Recuperamos arcos mientras el nodo actual no sea el nodo inicial
        while arista_antecesor != nodo_inicial:
            # Tomamos el antecesor del nodo actual mediante su etiqueta
            #antecesor = nodo_actual.etiqueta["antecesor"]
            # Se busca el objeto Arco que va desde el antecesor hasta el nodo actual y 
            # se agrega al principio de la lista, así terminaremos con la ruta ya ordenada
            ruta.insert(0, arista_antecesor)
            # Se actualiza el nodo actual
            arista_antecesor = arista_antecesor.origen.etiqueta["antecesor"]
        # Una vez que alcancemos el nodo inicial en la recuperación de la ruta, ésta
        # se regresa
        return ruta


    def dikjstra(self, nodo_inicial, nodo_final=None):
        # Se obtienen los nodos inicial y final
        a = self.buscar_nodo(nodo_inicial)
        if not a:
            raise ValueError(f"Error. El nodo inicial {nodo_inicial} no existe en la digráfica")

        if nodo_final:
            z = self.buscar_nodo(nodo_final)
            if not z:
                raise ValueError(f"Error. El nodo final {nodo_final} no existe en la digráfica" )
        else:
            z = None

        # el nodo inicial se etiqueta como temporal, como antecesor de él mismo y con una longitud
        # de ruta de 0, además se agrega a la lista de nodos etiquetados temporalmente
        a.etiqueta = {"tipo_etiqueta":"temporal", "antecesor":a, "longitud_ruta":0}
        X = [a]

        # El algoritmo continúa hasta que se acaben los nodos etiquetados temporalmente
        # o encontremos la ruta más corta hasta el nodo final z
        while X:
            # Se obtiene el nodo en X con la longitud de ruta más pequeña
            x = min(X, key=lambda nodo: nodo.etiqueta["longitud_ruta"])

            # x se elimina del conjunto de vértices marcados temporalmente y se marca de forma
            # definitiva
            X.remove(x)
            x.etiqueta["tipo_etiqueta"] = "definitiva"

            # Si x = z recuperamos la ruta y la regresamos. En caso de no especificar el nodo final
            # el algoritmo va a continuar hasta agotar la lista de nodos etiquetados temporalmente
            # para encontrar la ruta más corta desde el nodo inicial hacia todos los demás.
            # En este último caso esta condición también nos sirve ya que z siempre será None y
            # x nunca será None por lo tanto, siempre x != z
            if x == z:
                return self.__recuperar_ruta(x, a)
            
            # Si x != z, entonces se iteran los salientes de x:
            for arco in self.__digrafica[x]["salientes"]:
                # Se toma el destino del arco actual
                v = arco.destino
                # Si no tiene etiqueta, entonces se marca como temporal, con antecesor = x y
                # longitud de L(x) + w(arco). Además, se agrega a la lista de nodos etiquetados
                # temporalmente
                if not v.etiqueta:
                    v.etiqueta = {"tipo_etiqueta":"temporal", "antecesor":arco, "longitud_ruta":x.etiqueta["longitud_ruta"] + arco.peso}
                    X.append(v)

                # Si v tiene etiqueta temporal, entonces se revisa si la ruta desde x es mejor que
                # la que ya tenía
                elif v.etiqueta["tipo_etiqueta"] == "temporal":
                    # Si la longitud de la ruta viniendo desde x mejora la etiqueta de v, entonces
                    # se actualiza esta longitud y su antecesor ahora será X.
                    if x.etiqueta["longitud_ruta"] + arco.peso < v.etiqueta["longitud_ruta"]:
                        v.etiqueta["longitud_ruta"] = x.etiqueta["longitud_ruta"] + arco.peso 
                        v.etiqueta["antecesor"] = arco
        
        # Si llegamos hasta este punto y el usuario había especificado un nodo final, entonces
        # significa que no existe una ruta desde el nodo inicial hasta el nodo final, por lo tanto
        # se regresa un None. En caso contrario, recuperamos las rutas desde el nodo inicial hacia
        # todos los demás
        if nodo_final:
            return None
        else:
            rutas = []
            for nodo in self.__digrafica:
                if nodo != a:
                    rutas =list(set().union(rutas,self.__recuperar_ruta(nodo, a)))
            return rutas


    def dikjstra_general(self, nodo_inicial, nodo_final=None):
        nodo_inicial = self.buscar_nodo(nodo_inicial)
        arboresencia = self.dikjstra( nodo_inicial.nombre, nodo_final)

        aristas_sin_usar = []
        
        for nodo in self.__digrafica:
            for arco in self.__digrafica[nodo]["salientes"]:
                if arco not in arboresencia:
                    aristas_sin_usar.append(arco)
           
      
        i = 0
        while i < len(aristas_sin_usar)-1:
                    
            a = aristas_sin_usar[i]
          
            # Comparamos la arista que no está con la de la arboresencia    
            
            if a.origen.etiqueta["longitud_ruta"] + a.peso < a.destino.etiqueta["longitud_ruta"]:
                print(a.origen.nombre, a.destino.nombre,a.origen.etiqueta["longitud_ruta"] + a.peso,a.destino.etiqueta["longitud_ruta"])
                aristas_sin_usar.remove(a)
                # si mejora la longitud, debemos checar que no se forme un ciclo negativo
                # checaremos que el nodo destino no sea ancestro del nodo origen
                # Comenzamos la recuperación de la ruta en el nodo actual

                arista_antecesor = a.origen.etiqueta["antecesor"]               

                if arista_antecesor == nodo_inicial:
                    return False

                while arista_antecesor != nodo_inicial:
                    if arista_antecesor.origen ==  a.destino :
                        return False
                    arista_antecesor = arista_antecesor.origen.etiqueta["antecesor"]
                    
                

                delta = a.origen.etiqueta["longitud_ruta"] + a.peso - a.destino.etiqueta["longitud_ruta"]
                arboresencia.remove(a.destino.etiqueta["antecesor"])
                aristas_sin_usar.append(a.destino.etiqueta["antecesor"])
                a.destino.etiqueta["antecesor"] = a
                arboresencia.append(a)
                visited = []
                print("dfs")
                self.dfs(a.destino,visited, arboresencia, delta)

                i = 0
            else:
                i+=1

       
        return arboresencia




    def dfs(self,  node,visited, arborescencia, delta):
        if node not in visited:
            visited.append(node) 
            node.etiqueta["longitud_ruta"] += delta
            for saliente in self.__digrafica[node]["salientes"]:   
               if saliente in arborescencia:  
                   saliente.destino.etiqueta["longitud_ruta"] += delta
                   print(node.nombre, saliente.destino.nombre,saliente.destino.etiqueta["longitud_ruta"], delta)
                   self.dfs(saliente.destino,visited,arborescencia,delta)    