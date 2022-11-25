class Vertice:
    def __init__(self, n) :
        self.nombre = n
        self.vecinos = list()
        self.distancia = 9999
        self.color = 'white'
        self.pred = -1
    def agregarVecino (self, v):
        if v not in self.vecinos:
            self.vecinos.append(v)
            self.vecinos.sort()

class Grafo:

    def __init__(self):
        self.vertices = {}
    
    def agregarVertice (self, vertice):
        if isinstance (vertice, Vertice) and vertice.nombre not in self.vertices:
            self.vertices [vertice.nombre] = vertice
            return True 
        else:
            return False
    
    def agregarArista (self, u, v):
        if u in self.vertices and v in self.vertices:
            for key, value in self.vertices.items():
                if key == u:
                    value.agregarVecino(v)
                #if key == v:
                #    value.agregarVecino (u)
            return True 
        else:
            return False

    def imprimeGrafo (self):
        for key in sorted(list(self.vertices.keys())) :
            print ("Vertice " + str(key) + " Sus vecinos son" + str(self.vertices[key].vecinos) + " Y su distancia es: " + str(self.vertices[key].distancia))

    def bfs (self, vert):
        
        vert.distancia = 0
        vert.color = 'gris'
        vert.pred=-1
        q=list()
        q.append (vert.nombre)
        
        while len (q) > 0:
            u = q.pop ()
            node_u = self.vertices [u]
            for v in node_u.vecinos:
                node_v = self.vertices [v]
                if node_v.color == 'white':
                    node_v.color='gris'
                    node_v.distancia=node_u.distancia + 1
                    node_v.pred=node_u.nombre
                    q.append(v)
            self.vertices[u].color='black'