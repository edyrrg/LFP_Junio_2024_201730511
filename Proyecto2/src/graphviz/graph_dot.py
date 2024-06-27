import graphviz


class GraphDot:
    def __init__(self, title="Árbol de Derivación"):
        self.graph = graphviz.Digraph(name=title, format='pdf')
        self.graph.attr(label=title)

    def create_node(self, identifier, node):
        self.graph.node(identifier, node)

    def create_connection(self, prev, post):
        self.graph.edge(prev, post)

    def render_graph(self, file_name, ruta="./assets/"):
        self.graph.render(filename=file_name, directory=ruta)
