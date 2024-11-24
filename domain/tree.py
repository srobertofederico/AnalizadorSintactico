import pydot

# Define la clase TreeNode para representar un nodo en el árbol de derivación.
class TreeNode:
    def __init__(self, name):
        self.name = name  # El nombre del nodo.
        self.children = []  # Lista de hijos del nodo.

    # Método para agregar un hijo al nodo.
    def add_child(self, node):
        self.children.append(node)

    # Método para representar el nodo como una cadena.
    def __str__(self):
        return self.name

# Función para construir el árbol de derivación a partir de una estructura de árbol dada.
def build_tree(t):
    if isinstance(t, tuple):  # Si el nodo tiene hijos.
        # El primer elemento de la tupla es el nombre del nodo.
        node = TreeNode(str(t[0]))  # Convertir el nombre del nodo en cadena para evitar errores.

        # Los siguientes elementos de la tupla son los hijos.
        for child in t[1:]:
            # Llamar recursivamente para construir subárboles.
            node.add_child(build_tree(child))
        return node
    elif isinstance(t, list):  # Si es una lista, construir subárbol para cada elemento.
        node = TreeNode("list")
        for item in t:
            node.add_child(build_tree(item))
        return node
    else:  # Si el nodo es una hoja (valor individual).
        return TreeNode(str(t))  # Convertir en nodo hoja.

# Función para dibujar el árbol de derivación utilizando la biblioteca pydot.
def draw_tree(node, graph=None, parent=None):
    if graph is None:
        graph = pydot.Dot(graph_type='digraph')  # Crea un nuevo grafo si no se proporciona uno.

    current = pydot.Node(str(id(node)), label=node.name)  # Crea un nodo en el grafo con el nombre del nodo actual.
    graph.add_node(current)  # Añade el nodo al grafo.

    if parent:  # Si el nodo tiene un padre, agrega una arista del padre al nodo actual.
        graph.add_edge(pydot.Edge(parent, current))

    for child in node.children:  # Para cada hijo del nodo actual, dibuja recursivamente el subárbol.
        draw_tree(child, graph, current)

    return graph  # Devuelve el grafo completo del árbol de derivación.