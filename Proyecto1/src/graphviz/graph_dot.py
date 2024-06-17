import graphviz


class GraphDot:
    def __init__(self, title, filepath, nodos, conexiones):
        self.graph = graphviz.Digraph(name=title, filename=filepath, format='png')
        self.nodos = nodos
        self.conexiones = conexiones
        self.create_nodos()
        self.create_conexiones()
        self.graph.attr(label=title)
        self.graph.render()

    def create_nodos(self):
        for i in range(0, len(self.nodos), 2):
            if i+1 < len(self.nodos):
                self.graph.node(self.nodos[i], self.nodos[i+1])

    def create_conexiones(self):
        for i in range(0, len(self.conexiones), 2):
            if i+1 < len(self.conexiones):
                self.graph.edge(self.conexiones[i], self.conexiones[i+1])
