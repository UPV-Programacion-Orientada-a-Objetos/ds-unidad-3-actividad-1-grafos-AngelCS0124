import collections

class PyGrafo:
    def __init__(self):
        self.adj = collections.defaultdict(list)
        self.num_nodos_val = 0
        self.num_aristas_val = 0

    def cargar_datos(self, archivo: str):
        print(f"[Python Mock] Cargando dataset '{archivo}'...")
        try:
            with open(archivo, 'r') as f:
                max_id = 0
                count = 0
                for line in f:
                    if not line.strip() or line.startswith('#'):
                        continue
                    parts = line.split()
                    if len(parts) >= 2:
                        u, v = int(parts[0]), int(parts[1])
                        self.adj[u].append(v)
                        # Asumimos dirigido para coincidir con C++
                        max_id = max(max_id, u, v)
                        count += 1
                
                self.num_nodos_val = max_id + 1
                self.num_aristas_val = count
                print(f"[Python Mock] Carga completa. Nodos: {self.num_nodos_val} | Aristas: {self.num_aristas_val}")
        except Exception as e:
            print(f"Error cargando archivo: {e}")

    def obtener_grado(self):
        max_grado = -1
        nodo_max = -1
        for u in range(self.num_nodos_val):
            grado = len(self.adj[u])
            if grado > max_grado:
                max_grado = grado
                nodo_max = u
        return (nodo_max, max_grado)

    def bfs(self, nodo_inicio: int, profundidad_max: int):
        print(f"[Python Mock] Ejecutando BFS desde {nodo_inicio} prof {profundidad_max}...")
        visitados = set()
        cola = collections.deque([(nodo_inicio, 0)])
        visitados.add(nodo_inicio)
        aristas = []

        while cola:
            u, nivel = cola.popleft()
            if nivel >= profundidad_max:
                continue
            
            for v in self.adj[u]:
                aristas.append((u, v))
                if v not in visitados:
                    visitados.add(v)
                    cola.append((v, nivel + 1))
        
        return aristas

    def get_vecinos(self, nodo: int):
        return self.adj.get(nodo, [])

    @property
    def num_nodos(self):
        return self.num_nodos_val

    @property
    def num_aristas(self):
        return self.num_aristas_val
