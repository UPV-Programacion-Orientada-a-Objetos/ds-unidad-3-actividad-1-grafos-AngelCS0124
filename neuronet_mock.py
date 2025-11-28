import collections
import time

class PyGrafo:
    def __init__(self):
        # Estructura CSR (Compressed Sparse Row) optimizada para memoria
        self.row_ptr = [0]  # Punteros de fila
        self.col_idx = []   # Índices de columna (destino)
        self.num_nodos_val = 0
        self.num_aristas_val = 0
        self.grado_cache = None  # Cache del grado máximo
        self.nodo_max_grado = None

    def cargar_datos(self, archivo: str):
        print(f"[Python Mock] Cargando dataset '{archivo}'...")
        start_time = time.time()
        try:
            # Primera pasada: contar aristas por nodo
            adj_temp = collections.defaultdict(list)
            max_id = 0
            count = 0
            
            with open(archivo, 'r', encoding='utf-8-sig') as f:  # utf-8-sig ignora el BOM
                for line in f:
                    if not line.strip() or line.startswith('#'):
                        continue
                    parts = line.split()
                    if len(parts) >= 2:
                        try:
                            u, v = int(parts[0]), int(parts[1])
                            adj_temp[u].append(v)
                            max_id = max(max_id, u, v)
                            count += 1
                        except ValueError:
                            continue  # Ignorar líneas mal formadas
            
            self.num_nodos_val = max_id + 1
            self.num_aristas_val = count
            
            # Construir estructura CSR
            self.row_ptr = [0]
            self.col_idx = []
            
            for i in range(self.num_nodos_val):
                if i in adj_temp:
                    # Eliminar duplicados y ordenar
                    vecinos = list(set(adj_temp[i]))
                    vecinos.sort()
                    self.col_idx.extend(vecinos)
                self.row_ptr.append(len(self.col_idx))
            
            # Limpiar cache
            self.grado_cache = None
            self.nodo_max_grado = None
            
            elapsed = time.time() - start_time
            print(f"[Python Mock] Carga completa. Nodos: {self.num_nodos_val} | Aristas: {self.num_aristas_val}")
            print(f"[Python Mock] Tiempo: {elapsed:.4f}s | Memoria CSR: ~{(len(self.col_idx) * 8 + len(self.row_ptr) * 8) / 1024 / 1024:.2f} MB")
        except Exception as e:
            print(f"Error cargando archivo: {e}")

    def obtener_grado(self):
        """Obtiene el nodo con mayor grado usando estructura CSR"""
        if self.grado_cache is not None:
            return (self.nodo_max_grado, self.grado_cache)
        
        max_grado = -1
        nodo_max = -1
        
        for u in range(self.num_nodos_val):
            grado = self.row_ptr[u + 1] - self.row_ptr[u]
            if grado > max_grado:
                max_grado = grado
                nodo_max = u
        
        # Cachear resultado
        self.grado_cache = max_grado
        self.nodo_max_grado = nodo_max
        
        return (nodo_max, max_grado)

    def bfs(self, nodo_inicio: int, profundidad_max: int):
        """BFS optimizado usando estructura CSR"""
        print(f"[Python Mock] Ejecutando BFS desde {nodo_inicio} prof {profundidad_max}...")
        start_time = time.time()
        
        if nodo_inicio < 0 or nodo_inicio >= self.num_nodos_val:
            print(f"[Python Mock] Nodo {nodo_inicio} no válido")
            return []
        
        visitados = set()
        cola = collections.deque([(nodo_inicio, 0)])
        visitados.add(nodo_inicio)
        aristas = []

        while cola:
            u, nivel = cola.popleft()
            if nivel >= profundidad_max:
                continue
            
            # Obtener vecinos desde CSR
            start_idx = self.row_ptr[u]
            end_idx = self.row_ptr[u + 1]
            
            for v in self.col_idx[start_idx:end_idx]:
                aristas.append((u, v))
                if v not in visitados:
                    visitados.add(v)
                    cola.append((v, nivel + 1))
        
        elapsed = time.time() - start_time
        print(f"[Python Mock] BFS completado. {len(aristas)} aristas encontradas en {elapsed:.4f}s")
        return aristas

    def get_vecinos(self, nodo: int):
        """Obtiene los vecinos de un nodo usando CSR"""
        if nodo < 0 or nodo >= self.num_nodos_val:
            return []
        start_idx = self.row_ptr[nodo]
        end_idx = self.row_ptr[nodo + 1]
        return self.col_idx[start_idx:end_idx]

    @property
    def num_nodos(self):
        return self.num_nodos_val

    @property
    def num_aristas(self):
        return self.num_aristas_val
