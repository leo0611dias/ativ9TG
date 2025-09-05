class Grafo:
    def __init__(self):
        self.vertices = {}
        self.arestas = []
    
    def adicionar_vertice(self, vertice):
        if vertice not in self.vertices:
            self.vertices[vertice] = []
    
    def adicionar_aresta(self, u, v):
        if u != v:  
            if u in self.vertices and v in self.vertices:
                if v not in self.vertices[u]:
                    self.vertices[u].append(v)
                if u not in self.vertices[v]:
                    self.vertices[v].append(u)
                if (u, v) not in self.arestas and (v, u) not in self.arestas:
                    self.arestas.append((u, v))
                print(f"Aresta adicionada entre {u} e {v}")
    
    def get_vizinhos(self, vertice):
        return self.vertices.get(vertice, [])
    
    def get_vertices(self):
        return list(self.vertices.keys())
    
    def get_arestas(self):
        return self.arestas
    
    def eh_seguro(self, vertice, cor, cores_atribuidas):
        for vizinho in self.get_vizinhos(vertice):
            if cores_atribuidas.get(vizinho) == cor:
                return False
        return True
    
    def colorir_grafo_util(self, num_cores, cores_atribuidas, vertices_ordenados):
        if len(cores_atribuidas) == len(self.vertices):
            return True
        
        vertice_atual = None
        for v in vertices_ordenados:
            if v not in cores_atribuidas:
                vertice_atual = v
                break
        
        if vertice_atual is None:
            return True
        
        for cor in range(1, num_cores + 1):
            print(f"Tentando colorir a aula {vertice_atual} com a cor {cor}...")
            
            if self.eh_seguro(vertice_atual, cor, cores_atribuidas):
                cores_atribuidas[vertice_atual] = cor
                
                if self.colorir_grafo_util(num_cores, cores_atribuidas, vertices_ordenados):
                    return True
                
                cores_atribuidas.pop(vertice_atual)
        
        return False
    
    def colorir_grafo(self):
        # Ordenar vértices por grau (maior grau primeiro) - heurística
        vertices_ordenados = sorted(self.vertices.keys(), 
                                  key=lambda v: len(self.get_vizinhos(v)), 
                                  reverse=True)
        
        num_cores = 0
        cores_atribuidas = {}
        
        # Encontrar o número mínimo de cores
        while len(cores_atribuidas) < len(self.vertices):
            num_cores += 1
            cores_atribuidas = {}
            print(f"\nTentando colorir com {num_cores} cores:")
            
            if self.colorir_grafo_util(num_cores, cores_atribuidas, vertices_ordenados):
                break
        
        return num_cores, cores_atribuidas

if __name__ == '__main__':
    # Criar o grafo
    g = Grafo()
    
    # Adicionar vértices (aulas)
    aulas = ['M', 'A', 'C', 'F', 'G', 'P']
    for aula in aulas:
        g.adicionar_vertice(aula)
    
    # Adicionar arestas (conflitos entre aulas)
    g.adicionar_aresta("C", "F")
    g.adicionar_aresta("G", "A")
    g.adicionar_aresta("F", "A")
    g.adicionar_aresta("G", "F")
    g.adicionar_aresta("P", "A")
    g.adicionar_aresta("P", "F")
    g.adicionar_aresta("P", "G")
    
    # Mostrar conflitos
    print("\n" + "-" * 50)
    for vertice in g.get_vertices():
        vizinhos = g.get_vizinhos(vertice)
        if vizinhos:
            print(f"- Aula {vertice} tem conflito com: {', '.join(vizinhos)}")
    
    print("\n" + "=" * 50)
    numero_minimo_horarios, cores_atribuidas = g.colorir_grafo()
    
    print("\n" + "=" * 50)
    print(f"Número mínimo de horários necessários: {numero_minimo_horarios}")
    print("Cores atribuídas a cada aula:")
    for aula, cor in sorted(cores_atribuidas.items()):
        print(f"- Aula {aula}: Horário {cor}")
    
    print(f"\n{cores_atribuidas}")
