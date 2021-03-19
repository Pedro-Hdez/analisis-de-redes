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
                self.agregar_arco(line[0], line[1], line[2])

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