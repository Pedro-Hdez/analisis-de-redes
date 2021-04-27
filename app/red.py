import copy
import operator
import math
from typing import MappingView
from estructuras_datos import *
import sys
sys.setrecursionlimit(5000)

class Arco:
    """
        Esta clase representa un arco. Tiene nodos de origen y destino, además de una 
        capacidad mínima, un flujo y una capacidad.
    """
    def __init__(self, origen, destino, res_min=0, flujo=0, capacidad=0, costo=0, Id=None):
        self.origen = origen
        self.destino = destino
        self.res_min = res_min
        self.flujo = flujo
        self.capacidad = capacidad
        self.costo = 0
        self.Id = Id
#----------------------------------------------------------------

class Nodo:
    """
        Esta clase representa un nodo. Tiene un nombre, restricción mínima y máxima, etiqueta y 
        grados positivo y negativo.
    """
    def __init__(self, nombre, res_min=0, res_max=math.inf, Id=None):
        self.nombre = nombre
        self.res_min=res_min
        self.res_max=res_max
        self.etiqueta = None
        self.grado_positivo = 0
        self.grado_negativo = 0
        self.Id = Id

#----------------------------------------------------------------
class Red:
    """
        Esta clase representa una red de transporte y sus operaciones.
    """
    def __init__(self):
        self.__red = {} # Estructura donde se va a guardar la gráfica
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
        for nodo in self.__red:
            if nodo.nombre == nombre:
                return nodo
        return False 
    
    def agregar_nodo(self, nombre, res_min=0, res_max=math.inf, Id=None):
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
        nodo = self.buscar_nodo(nombre)
        if not nodo:
        
            # Si el nuevo nodo no existe, entonces se crea y se le añade un diccionario
            # con dos listas vacías, la lista de nodos "entrantes" y la lista de nodos "salientes"
            nodo = Nodo(nombre, float(res_min), float(res_max), Id=Id)
            self.__red[nodo] = {"entrantes":[], "salientes":[]}

            # El número de nodos en la digráfica se incrementa y se regresa True
            self.__num_nodos += 1
        return nodo
    
    def agregar_arco(self, a, b, res_min=0, flujo=0, capacidad=0, costo=0, Id=None):
        """
            Este método agrega un arco a la digráfica

            Parámetros
            ----------
            a: Nodo de origen.
            b: Nodo destino.
            res_min: restricción mínima del arco.
            flujo: Flujo del arco
            capacidad: Capacidad del arco
        """
        # Se agregan los nodos a y b (Esto porque le damos la opción al usuario de 
        # agregar arcos directamente sin la necesidad de que los nodos ya existan
        # en la digráfica)
        nodo_a = self.agregar_nodo(a)
        nodo_b = self.agregar_nodo(b)

        # Se construye el arco (a,b)
        arco = Arco(nodo_a, nodo_b, float(res_min), float(flujo), float(capacidad), float(costo), Id=Id)

        # Se agrega el arco (a,b) a los salientes de a, y el grado positivo de a 
        # se incrementa en 1
        self.__red[nodo_a]["salientes"].append(arco)
        nodo_a.grado_positivo += 1

        # Se agrega el arco (a,b) a los entrantes de b, y el grado negativo de b 
        # se incrementa en 1
        self.__red[nodo_b]["entrantes"].append(arco)
        nodo_b.grado_negativo += 1

        # El contador de arcos se incrementa
        self.__num_arcos += 1
        
        return True
    
    def leer_red(self, archivo):
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
            elif length == 3:
                self.agregar_nodo(line[0], float(line[1]), float(line[2]))
            elif length == 6:
                self.agregar_arco(line[0], line[1], float(line[2]), float(line[3]), float(line[4], float(line[5])))
    
    def buscar_arco(self, a, b, res_min=0, flujo=0, capacidad=0):
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
        
        for arco in self.__red[nodo_a]['salientes']:
            if arco.destino.nombre == b and arco.res_min == res_min and arco.flujo == flujo and arco.capacidad == capacidad:
                return arco
        
        # Si se recorrieron todos los salientes del nodo de origen y no se encontró
        # el arco buscado, entonces se regresa False
        return False
    
    def eliminar_arco(self, a=None, b=None, res_min=0, flujo=0, capacidad=0, obj_arco=None):
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
        if not obj_arco:
            arco = self.buscar_arco(a, b, res_min, flujo, capacidad)
        else:
            arco = obj_arco

        # Si existe el arco, entonces se procede a elminarlo
        if arco:
            # El arco se elimina de los salientes del nodo de origen y el peso positivo
            # de éste se decrementa
            nodo_origen = arco.origen
            self.__red[nodo_origen]["salientes"].remove(arco)
            nodo_origen.grado_positivo -= 1

            # El arco se elimina de los entrantes del nodo destino y el peso negativo
            # de éste se decrementa
            nodo_destino = arco.destino
            self.__red[nodo_destino]["entrantes"].remove(arco)
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
            self.vaciar_nodo(nodo.nombre)

            # Cuando todos los arcos incidentes en el nodo se hayan eliminado procedemos a 
            # eliminar el nodo de la digráfica y decrementamos el contador de nodos
            self.__red.pop(nodo)
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
            while self.__red[nodo]["salientes"]:
                arco = self.__red[nodo]["salientes"][0]
                self.eliminar_arco(obj_arco=arco)
            
            # Se eliminan todos los arcos entrantes
            while self.__red[nodo]["entrantes"]:
                arco = self.__red[nodo]["entrantes"][0]
                self.eliminar_arco(obj_arco=arco)
            
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
            for nodo in self.__red:
                nodo.etiqueta = None
        elif tipo == "aristas":
            for nodo in self.__red:
                for arco in self.__red[nodo]["entrantes"]:
                    arco.etiqueta = None
                for arco in self.__digrafica[nodo]["salientes"]:
                    arco.etiqueta = None
        elif tipo == "todo":
            for nodo in self.__red:
                for arco in self.__red[nodo]["entrantes"]:
                    arco.etiqueta = None
                for arco in self.__red[nodo]["salientes"]:
                    arco.etiqueta = None
        else:
            raise ValueError(f"Error en el tipo dado ({tipo}). Valores aceptados: 'nodos', 'aristas', 'todos'")

    def imprimir_arcos(self):
        for nodo in self.__red:
                for arco in self.__red[nodo]["salientes"]:
                    print("(",arco.origen.nombre,', ',arco.destino.nombre,', ',arco.res_min,', ',arco.flujo,', ',arco.capacidad,')')

    def fulkerson(self,fuente,sumidero):
            arcos_visitados = []
            cadena = []
           
            # buscamos cadenas aumentantes con busqueda a lo profundo
            self.dfs(fuente,fuente,sumidero,cadena,arcos_visitados)

            # ciclo donde actualizaremos el flujo de las cadenas aumentantes, mientras existan estas cadenas
            while True:
                flujo_cadena = math.inf

                # calculamos el flujo con el que actualizarmos el flujo de la cadena aumentante
                for arco in cadena:       
                    if(arco.etiqueta == "sentidoPropio"):
                         # caso donde el arco va en sentido propio
                        if((arco.capacidad - arco.flujo) < flujo_cadena):
                            flujo_cadena = arco.capacidad - arco.flujo
                    else:
                        # caso donde el arco va en sentido impropio
                        if(arco.etiqueta == "sentidoImpropio"):
                            if(arco.flujo <= flujo_cadena and arco.flujo > arco.res_min):
                                flujo_cadena = arco.flujo - arco.res_min
                
                # actualizamos el flujo de los arcos de la cadena aumentante
                for arco in cadena:
                    # caso donde el arco va en sentido propio, sumamos flujo
                    if(arco.etiqueta == "sentidoPropio"):
                        arco.flujo += flujo_cadena

                    # caso donde el arco va en sentido impropio, restamos flujo
                    if(arco.etiqueta == "sentidoImpropio"):
                        arco.flujo -= flujo_cadena
                   
                cadena= []
                arcos_visitados = []
                # reseteamos las etiquetas de los nodos
                for nodo in self.__red:
                    nodo.etiqueta = None
                # buscamos una nueva cadena aumentante
                self.dfs(fuente,fuente,sumidero,cadena,arcos_visitados)

                # si ya no hay cadenas aumentantes, nos detenemos
                if not cadena:
                    break

    def flujo_maximo(self,fuentes,sumideros):

        # revisaremos cuantos nodos fuentes y sumideros hay 
        # si hay mas de un sumireo o mas de un nodo fuente, crearemos un super fuente o un super sumidero
        if len(fuentes) > 1:
            self.agregar_nodo('A+')
            fuente = self.buscar_nodo('A+')
            for nodo in fuentes:
                self.agregar_arco(fuente.nombre, nodo,0,0,math.inf)

        if len(sumideros) > 1:
            self.agregar_nodo('Z-')
            sumidero = self.buscar_nodo('Z-')
            for nodo in sumideros:
                self.agregar_arco(nodo, sumidero.nombre,0,0,math.inf)

        # si solo hay un sumidero o un solo fuente, los definimos
        if(len(fuentes)==1 ):
            fuente = self.buscar_nodo(fuentes[0])
        if(len(sumideros)==1 ):
            sumidero = self.buscar_nodo(sumideros[0])

        # revisaremos el caso donde hay restricciones en uno o mas nodos
        nodos_ficticios = []
        lista_nodos = []
        # lista con los nodos originales de la lista
        for nodo in self.__red:
            lista_nodos.append(nodo)
        
      
        # iteramos los nodos para revisar si tienen restricciones
        for nodo in lista_nodos:
            if nodo.res_min > 0 or nodo.res_max != math.inf:
                # si el nodo tiene restricción, agregamos un nodo ficticio
                self.agregar_nodo(nodo.nombre+ '"')
                # metemos el nodo ficticio creado en una lista
                nodos_ficticios.append(nodo)

                # creamos una lista de los arcos salientes del nodo que tiene restricciones
                lista_arcos = []
                for arco in self.__red[nodo]["salientes"]:
                    lista_arcos.append(arco)

                # creamos un arco ficticio entre el nodo con restricciones y en nuevo nodo ficticio creado
                self.agregar_arco(nodo.nombre, nodo.nombre+ '"',nodo.res_min,0,nodo.res_max)

                for arco in lista_arcos:   
                    # los arcos salientes del nodo con restricciones ahora serán los arcos salientes del nuevo nodo ficticios           
                    self.agregar_arco(nodo.nombre+ '"', arco.destino.nombre,arco.res_min,arco.flujo,arco.capacidad)
                    # eliminamos momentaneamente los arcos salientes del nodo que tiene restricciones
                    self.eliminar_arco(nodo.nombre,arco.destino.nombre,arco.res_min,arco.flujo,arco.capacidad)

        # revisamos los arcos que tienen restriccion y los metemos a una lista
        arcos_con_restriccion = []            
        for nodo in self.__red:
            for arco in self.__red[nodo]["salientes"]:
                if(arco.res_min > 0):
                    arcos_con_restriccion.append(arco)

        # caso donde existen arcos con restriccion
        if(len(arcos_con_restriccion)> 0):
            # lista donde guardaremos las restricciones de los arcos con restriccion minima
            restricciones_minimas = []
           
            # para cada arco con restriccion, creamos un arco ficticio desde el origen de ese arco hacia un sumidero ficticio
            # tambien creamos un arco ficticio desde un fuente ficticio hacia el nodo destino del arco con restricción
            for arco in arcos_con_restriccion:
                restricciones_minimas.append(arco.res_min)
                # creamos los arcos ficticios para los arcos que tiene restricción
                self.agregar_arco(arco.origen.nombre, "SumideroFicticio",0,0,arco.res_min)
                self.agregar_arco("FuenteFicticio", arco.destino.nombre,0,0,arco.res_min)

                # actualizamos la capacidad y restricción minima del arco provisionalmente, para que todo los arcos tengan restricción minima de 0
                arco.capacidad = arco.capacidad - arco.res_min
                arco.res_min = 0
            
            # agreamos dos arcos ficticiones que conecten al nodo fuente y al nodo sumidero con capacidad infinita
            self.agregar_arco(fuente.nombre, sumidero.nombre,0,0,math.inf)
            self.agregar_arco(sumidero.nombre, fuente.nombre,0,0,math.inf)

            # guardamos los arcos ficticios en una lista para eliminarlos después
            arcos_fuente_sumidero = []
            arcos_fuente_sumidero.append(self.buscar_arco(fuente.nombre, sumidero.nombre,0,0,math.inf))
            arcos_fuente_sumidero.append(self.buscar_arco(sumidero.nombre, fuente.nombre,0,0,math.inf))
            
            # buscamos los nodos fuete y sumidero ficticios creados para el caso donde hay arcos con restricciones
            fuenteFicticio = self.buscar_nodo("FuenteFicticio")
            sumideroFicticio = self.buscar_nodo("SumideroFicticio")
            
            # aplicamos ford fulkerson a la red, con los nodos fuente y sumidero ficticios
            self.fulkerson(fuenteFicticio,sumideroFicticio)
        
            # regresamos a la normalidad los arcos que tenian reestriccion minima
            arcos_sumideroFicticio = []
            for arco in self.__red[sumideroFicticio]['entrantes']:
                arcos_sumideroFicticio.append(arco)
            for arco in arcos_con_restriccion:
                res_min = restricciones_minimas.pop(0)
                # recuperamos la restriccion y capacidad originales de los arcos
                arco.res_min = res_min
                arco.flujo += arcos_sumideroFicticio.pop(0).flujo
                arco.capacidad = arco.capacidad + res_min
            # eliminamos los nodos ficticios creados para el caso donde hay arcos con reestriccion minima
            self.eliminar_nodo(fuenteFicticio.nombre)
            self.eliminar_nodo(sumideroFicticio.nombre)
          

            
            for arco in arcos_fuente_sumidero:
                self.eliminar_arco(arco.origen.nombre,arco.destino.nombre,arco.res_min,arco.flujo,arco.capacidad)
            
        
       
        # aplicamos for fulkerson a la red
        self.fulkerson(fuente,sumidero)


        # regresamos los nodos con reestriccion particionados a la normalidad
        for nodo in nodos_ficticios:
            nodo_ficticio = self.buscar_nodo(nodo.nombre+ '"')
            lista_arcos_ficticios = []
            for arco in self.__red[nodo_ficticio]["salientes"]:
                lista_arcos_ficticios.append(arco)
            
            for arco in lista_arcos_ficticios:
                self.agregar_arco(nodo.nombre, arco.destino.nombre,arco.res_min,arco.flujo,arco.capacidad)
            self.eliminar_nodo(nodo.nombre+ '"')

        # eliminamos los nodos super fuente y super sumidero en caso de que fueran requeridos
        # para el caso donde hay mas de un sumidero o mas de una fuente        
        if(len(fuentes)>1):
            self.eliminar_nodo('A+')
        if(len(sumideros)>1):
            self.eliminar_nodo('Z-')


        # calculamos el flujo final que reciben los sumideros
        flujo_final = 0
        for nodo in sumideros:
            for arco in self.__red[self.buscar_nodo(nodo)]["entrantes"]:
                flujo_final += arco.flujo
            for arco in self.__red[self.buscar_nodo(nodo)]["salientes"]:
                flujo_final -= arco.flujo
        
        aristas = []
        for nodo in self.__red:
            for arista in self.__red[nodo]['entrantes']:
                if arista not in aristas:
                    aristas.append(arista)

        return flujo_final, aristas

    def dfs(self, node,fuente, sumidero, cadena,arcos_visitados):
        bool = False
        node.etiqueta == "marcado"
        for saliente in self.__red[node]["salientes"]: 
            if(saliente.flujo < saliente.capacidad and saliente not in arcos_visitados and saliente.destino.etiqueta != "marcado"): 
      
                bool = True
                arcos_visitados.append(saliente)
                cadena.append(saliente) 
                saliente.etiqueta = "sentidoPropio"
                if(saliente.destino == sumidero):

                    return cadena
                self.dfs(saliente.destino,fuente,sumidero,cadena,arcos_visitados)
                break

        if(bool == False):
            for entrante in self.__red[node]["entrantes"]: 
                if(entrante.flujo > 0 and entrante.flujo > entrante.res_min and entrante not in arcos_visitados and entrante.origen.etiqueta != "marcado"): 
                    bool = True
                    arcos_visitados.append(entrante)
                    cadena.append(entrante) 
                    entrante.etiqueta = "sentidoImpropio"
                    if(entrante.origen == sumidero):
                        return cadena
                    self.dfs(entrante.origen,fuente,sumidero,cadena,arcos_visitados)
                    break
        
        

        if(bool == False):     
            if(len(cadena)>=1):
                if(cadena[len(cadena)-1].etiqueta == "sentidoPropio"):      
                    nodo = cadena[len(cadena)-1].origen
                    cadena.pop(len(cadena)-1)
                    node.etiqueta = None
                    self.dfs(nodo,fuente,sumidero,cadena,arcos_visitados)
                    return None
                elif(cadena[len(cadena)-1].etiqueta == "sentidoImpropio"):
                    nodo = cadena[len(cadena)-1].destino
                    cadena.pop(len(cadena)-1)
                    node.etiqueta = None
                    self.dfs(nodo,fuente,sumidero,cadena,arcos_visitados)
                    return None
    def __str__(self):
        """
            Este método imprime la digráfica
        """
        resultado = ""
        for nodo in self.__red:
            resultado += f"Nodo: {nodo.nombre}, ({nodo.res_min},{nodo.res_max},{nodo.Id})\nEntrantes: "
            for arco in self.__red[nodo]["entrantes"]:
                resultado += f"({arco.origen.nombre}, {arco.res_min}, {arco.flujo}, {arco.capacidad}, {arco.costo}, {arco.Id}), "

            resultado = resultado[:-2] + "\nSalientes: "
            for arco in self.__red[nodo]["salientes"]:
                resultado += f"({arco.destino.nombre}, {arco.res_min}, {arco.flujo}, {arco.capacidad}, {arco.costo}, {arco.Id}), "
            
            resultado = resultado[:-2] + "\n\n"
        
        resultado = resultado[:-2]

        return resultado 
      
        

      
             
            
        