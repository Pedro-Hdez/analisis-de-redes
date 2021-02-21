# Librería base de Python para interfaces de usuario
import tkinter as tk

# ----- Variables Globales -----

global canvas_w # Ancho del canvas
global canvas_h # Alto del canvas
global node_radius # Radio de los nodos
global root # Pantalla principal
global canvas # Canvas: En donde se dibujará la gráfica
global node_label # Etiqueta automática de los nodos
global canvas_pady # Margen superior del canvas
global root_size # Tamaño de la ventana principal
global canvas_bgcolor # Color de fondo del canvas
global min_node_separation # Minima separación que debe existir entre un nodo y otro
global drag_data # Información del objeto arrastrado
global mouse_state # Estado del mouse ("node", "vertex")

global nodes_button # Botón para la gestión de nodos
global vertex_button # Botón para la gestión de las aristas

global buttons_frame_padx
global buttons_frame_pady

global nodes_menu

global element_selected


"""
    Este método dibuja un nodo en la gráfica.
    El nodo se representará con un círculo y su etiqueta. Este círculo tendrá radio 'node_r' con 
    centro en la coordenada en donde el usuario dio click.
"""
def drawNode(event):
    # Se obtienen las coordenadas del evento (del click)
    if mouse_state != "node":
        return

    x = event.x
    y = event.y
    # Se imprimen las coordenadas del evento (para pruebas)
    print(x,y)
    # Se llama a la variable global 'node_label' para poder modificarla desde aquí
    global node_label
    # Se verifica si se puede dibujar el nodo (círculo) sin que se salga del canvas
    if x-node_r >= 0 and x+node_r <= canvas_w and y-node_r >= 0 and y+node_r <= canvas_h:
        # Se verifica que el nuevo nodo no se traslape con otro existente
        overlapped_items = canvas.find_overlapping(x-node_r-min_node_separation, 
                           y-node_r-min_node_separation, x+node_r+min_node_separation, 
                           y+node_r+min_node_separation)
        if not overlapped_items:
            # Se crea el nodo y con el argumento 'tags' se indica que es un objeto del tipo nodo y su etiqueta
            canvas.create_oval(x-node_r, y-node_r, x+node_r, y+node_r, fill=node_color,
                                tags=f"node {node_label}")
        # Se crea la etiqueta del nodo dentro de éste, con el argumento 'tags' también se indica que
        # es un objeto del tipo nodo y su etiqueta (esto porque también la etiqueta pertenece a dicho nodo)                      
            canvas.create_text(x,y, text=str(node_label), tags=f"node {node_label}")
            
            # Se actualiza la etiqueta del nodo
            node_label += 1

"""
    Este método detecta si hemos dado click derecho a algún elemento de la gráfica. Esto con el
    fin de desplegar un menú desde donde se podrá modificar el elemento seleccionado.
"""
def onObjectClick(event):
    global element_selected

    x, y = event.x, event.y
    # Se encuentra el item que ha sido seleccionado mediante un click. Para ello utilizamos el 
    # método 'find_overlapping' del objeto canvas. Se le dan las coordenadas de la esquina superior
    # izquierda y la esquina inferior derecha de un rectángulo. El método regresará el índice de
    # todos los objetos que el rectángulo dado llegue a tocar. En este caso le damos las coordenadas
    # de solo un punto para tener más precisión al momento de seleccionar elementos.
    item = canvas.find_overlapping(
           x, y, x, y)         
    
    # Si se seleccionó un item, entonces se obtienen sus etiquetas en forma de arreglo
    # para saber qué tipo de objeto es (nodo o arista) y además saber su nombre (en caso de que sea 
    # nodo) o su peso (en caso de que se trate de una arista)
    if item:     
        item_tag = canvas.itemcget(item, "tags").replace("current", "").strip()
        
        if not canvas.itemcget(item, "tags"):
        # Bloque de excepción en caso de que seleccionemos la nada
            try:
                item = canvas.find_overlapping(x-node_r, y-node_r, x+node_r, y+node_r)[1] 
                item_tag = canvas.itemcget(item, "tags").replace("current", "").strip()

            except:
                print("No se encontró elemento en la rebúsqueda")
                return

        element_selected = item

        if "node" in item_tag:
            nodes_menu.tk_popup(event.x_root, event.y_root)
        print("Elemento seleccionado:", item_tag)


"""
    Este método inicializa la información necesaria para poder arrastrar un objeto
"""
def drag_start(event):
    print("----- DRAG BEGIN -----")
    global drag_data # Se necesitará modificar el diccionario de drag_data
    # Se obtienen las coordenadas del click    
    x, y = event.x, event.y

    # Se identifica el elemento seleccionado con un overlapping sobre un solo punto
    # (por eso las coordenadas de las esquinas de la bounding box son iguales)
    selected_item = canvas.find_overlapping(
           x, y, x, y) 
    
    # Cuando seleccionamos exatamente la etiqueta de un nodo, la instrucción actual regresa una
    # etiqueta vacía, probablemente es un bug ya que en ese caso la etiqueta y el nodo están
    # exactamente en la misma posición y el programa no sabe qué etiqueta regresar. En este caso,
    # buscamos un objeto cercano hasta una distancia de r. El primero será la etiqueta, el segundo
    # el nodo, así que por eso tomamos el item[1]
    if not canvas.itemcget(selected_item, "tags"):
        # Bloque de excepción en caso de que seleccionemos la nada
        try:
            selected_item = canvas.find_overlapping(
                            x-node_r, y-node_r, x+node_r, y+node_r)[1] 
        except:
            return
        
    #    print("NO SE ENCONTRÓ PERO AHORA ES:", selected_item)
    # En esta lista se almacenarán todos los objetos de interés, o sea, los que vamos a arrastrar.
    # Se identificarán por sus etiquetas.
    interest_objects = []

    # Se obtiene la etiqueta del item que seleccionamos. Si contiene la palabra "current"
    # se elimina junto con todos los espacios posibles.
    original_tag = canvas.itemcget(selected_item, "tags").replace("current", "").strip()

    # Se iteran todos los items del canvas
    for item in canvas.find_all():
        # De la misma forma que encontramos la etiqueta del item seleccionado, ahora 
        # se tomará la del item en cuestión
        this_tag = canvas.itemcget(item, "tags").replace("current", "").strip()

        print(f"Etiqueta del original: {original_tag}")
        print(f"Etiqueta del actual original: {this_tag}")
        print(f"Las etiquetas son iguales? {this_tag in original_tag}")
        print("\n----------------------------------")

        # Si las etiquetas son iguales, entonces se agrega a la lista de items de interés.
        # Hasta este momento solo tnenemos Nodos y su Etiqueta, por lo tanto, cuando el 
        # arreglo de regiones de interés tenga longitud 2 (nodo y su etiqueta) se rompe el ciclo 
        if this_tag == original_tag:
            interest_objects.append(item)
            if len(interest_objects) == 2:
                break
    
    print(f"Items de interes: {interest_objects}")

    # Se actualiza el drag data con la información que recolectamos
    drag_data["item"] = interest_objects
    drag_data["x"] = x
    drag_data["y"] = y
    drag_data["secure_x"] = x
    drag_data["secure_y"] = y
 
"""
    Este método arrastra un conjunto de elementos de una posición a otra dentro del canvas
    siguiendo las restricciones de distancia mínima entre un nodo y otro diferente, además de 
    respetar el límite del canvas
"""
def drag(event):
    # Se toma la posición hasta donde se ha arrastrado el moude
    x, y = event.x, event.y

    # Se calcula hasta dónde se movió el mouse
    delta_x = x - drag_data["x"]
    delta_y = y - drag_data["y"]
    
    # Se mueve cada item de interés (almacenado en drag_data["item"]) desde la posición en donde
    # estaba, hacia la nueva delta_x y delta_y
    # Además, se agrega un bloque de excepción en caso de que hayamos seleccionado la nada
    # y por lo tanto los items a mover sean None
    try:
        for item in drag_data["item"]:
            canvas.move(item, delta_x, delta_y)
            # Se actualiza la posición del objeto arrastrado
            drag_data["x"] = x
            drag_data["y"] = y
    except:
        return

def drag_stop(event):
    """End drag of an object"""
    print("Stoping dragging")
    
    # Se toma la posición actual de los objetos arrastrados 
    x, y = drag_data["x"], drag_data["y"]

    # Se identifican todos los elementos que están sobrepuestos de acuerdo a los límites de los
    # objetos arrastrados
    overlapped_items = canvas.find_overlapping(x-node_r-min_node_separation, 
                           y-node_r-min_node_separation, x+node_r+min_node_separation, 
                           y+node_r+min_node_separation)
    
    overlapping = False # Bandera para indicar si existe un overlapping

    # Se toma la etiqueta de uno de los items arrastrados (recordemos que en drag_data["item"]
    # se guardan siempre 2 elementos y estos tienen la misma etiqueta)
    # Se agrega un bloque de excepción en caso de que hayamos seleccionado la nada para 
    # arrastrar y los items de interes sean nulos
    try:
        dragged_item = canvas.itemcget(drag_data["item"][0], "tags").replace("current", "").strip()
    except:
        return
    print("\n\n-----DRAG_STOP-----")
    print("Dragged item:", dragged_item, "\n")

    # Se revisan todos los elementos sobrepuestos 
    for overlapped in overlapped_items:
        # Se obtiene la etiqueta del item sobrepuesto actual
        overlapped_item = canvas.itemcget(overlapped, "tags").replace("current", "").strip()
        print("Overlapped item:", overlapped_item)

        # Si la etiqueta del objeto sobrepuesto es diferente a la del objeto arrastrado, etonces
        # hay overlapping y con uno es suficiente para no permitir que el elemento arrastrado se
        # quede en ese lugar
        if dragged_item != overlapped_item:
            print("*Overlapped with this")
            overlapping = True
            break
    
    out_of_bounds = False # Bandera para indicar si arrastramos el objeto fuera del canvas

    # Se revisa si la nueva posición es válida de acuerdo a los límites del canvas
    if x-node_r < 0 or x+node_r > canvas_w or y-node_r < 0 or y+node_r > canvas_h:
        print("Dragged out of canvas bounds")
        out_of_bounds = True

    # Si hay overlapping o se arrastró fuera del canvas, entonces todos los elementos que se 
    # movieron se regresan a su posición anterior (drag_data["secure_x"], drag_data["secure_y"])
    if overlapping or out_of_bounds:
        for item in drag_data["item"]:
            canvas.move(item, drag_data["secure_x"] - event.x, drag_data["secure_y"] - event.y)
    else:
        print("Not overlapping nor out of bounds")
    
    # Se resetea la información de arrastre
    drag_data["item"] = None
    drag_data["x"] = 0
    drag_data["y"] = 0
    drag_data["secure_x"] = 0
    drag_data["secure_y"] = 0
    
    print("Drag Stoped")
    print("\n\n-----")


def nodesButtonClick():
    global mouse_state
    if nodes_button["state"] != "disabled":
        mouse_state = "node"
        nodes_button["state"] = "disabled"
        vertex_button["state"] = "normal"

def vertexButtonClick():
    global mouse_state
    if vertex_button["state"] != "disabled":
        mouse_state = "vertex"
        vertex_button["state"] = "disabled"
        nodes_button["state"] = "normal"

def removeNode():
    global canvas
    item = element_selected
    item_tag = canvas.itemcget(item, "tags").replace("current", "").strip()
        
    if not item_tag:
    # Bloque de excepción en caso de que seleccionemos la nada
        try:
            item = canvas.find_overlapping(x-node_r, y-node_r, x+node_r, y+node_r)[1] 
            item_tag = canvas.itemcget(item, "tags"),replace("current", "").strip()

        except:
            print("No se encontró elemento a eliminar")
            return        

    print("Estoy en:", item_tag)

    elements_to_remove = []
    print("ANTES DE ELIMINAR", len(canvas.find_all()))
    for item2 in canvas.find_all():
        # De la misma forma que encontramos la etiqueta del item seleccionado, ahora 
        # se tomará la del item en cuestión
        this_tag_original = canvas.itemcget(item2, "tags")
        this_tag_short = this_tag_original.replace("current", "").strip()

        # Si las etiquetas son iguales, entonces se agrega a la lista de items de interés.
        # Hasta este momento solo tnenemos Nodos y su Etiqueta, por lo tanto, cuando el 
        # arreglo de regiones de interés tenga longitud 2 (nodo y su etiqueta) se rompe el ciclo 
        if this_tag_short == item_tag:
            elements_to_remove.append(item2)
            if len(elements_to_remove) == 2:
                break
    
    for element in elements_to_remove:
        canvas.delete(element)

    print("DESPUES DE ELIMINAR", len(canvas.find_all()))

root_w = 800
root_h = 800
# Inicialización de las variables globales
canvas_w = 700
canvas_h = 600
node_r = 25
node_label = 1
canvas_pady = 5
root_size = f"{root_w}x{root_h}"
node_color = "cyan"
canvas_bgcolor = "white"
min_node_separation = 30
drag_data = {"x":0, "y":0, "secure_x":0, "secure_y":0, "item":None}
mouse_state = ""


buttons_frame_padx = 50
buttons_frame_pady = 5

nodes_button_padx = 0
nodes_button_pady = 0
vertex_button_padx = 0
vertex_button_padx = 0

root = tk.Tk()
root.geometry(root_size)
buttons_frame = tk.LabelFrame(root, bd=0)
buttons_frame.pack(padx=buttons_frame_padx, pady=buttons_frame_pady)

canvas = tk.Canvas(root, width = canvas_w, height=canvas_h, bg="white")
canvas.pack(pady=canvas_pady)

nodes_button = tk.Button(buttons_frame, text="Gestionar nodos", command=nodesButtonClick)
nodes_button.pack(side=tk.LEFT, padx=10)

vertex_button = tk.Button(buttons_frame, text="Gestionar aristas", command=vertexButtonClick)
vertex_button.pack(side=tk.RIGHT, padx=10)

nodes_menu = tk.Menu(canvas, tearoff = 0)   
nodes_menu.add_command(label ="Eliminar nodo", command=removeNode) 
nodes_menu.add_command(label ="Renombrar nodo") 

element_selected = ""
elements_to_remove = []

canvas.bind("<Button 1>",drawNode)
canvas.bind("<Button 3>",onObjectClick)
canvas.bind("<ButtonPress-2>", drag_start)
canvas.bind("<ButtonRelease-2>", drag_stop)
canvas.bind("<B2-Motion>", drag)


root.mainloop()