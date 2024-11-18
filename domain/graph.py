import graphviz

def graficar_afd(afd, nombre_archivo):
    dot = graphviz.Digraph(comment='AFD')

    # Añadir nodos
    for estado in afd['estados']:
        if estado in afd['estados_finales']:
            dot.node(estado, shape='doublecircle')
        else:
            dot.node(estado)

    # Añadir transiciones
    for transicion in afd['transiciones']:
        origen, simbolo, destino = transicion
        dot.edge(origen, destino, label=simbolo)

    # Guardar y renderizar el archivo
    dot.render(nombre_archivo, format='png', cleanup=True)

def graficar_afn(afn, nombre_archivo):
    dot = graphviz.Digraph(comment='AFN')

    # Añadir nodos
    for estado in afn['estados']:
        if estado in afn['estados_finales']:
            dot.node(estado, shape='doublecircle')
        else:
            dot.node(estado)

    # Añadir transiciones
    for transicion in afn['transiciones']:
        origen, simbolo, destino = transicion
        dot.edge(origen, destino, label=simbolo)

    # Guardar y renderizar el archivo
    dot.render(nombre_archivo, format='png', cleanup=True)