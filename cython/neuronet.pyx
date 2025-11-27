# distutils: language = c++

from libcpp.vector cimport vector
from libcpp.string cimport string
from libcpp.utility cimport pair
from neuronet_core cimport GrafoDisperso

cdef class PyGrafo:
    cdef GrafoDisperso* c_grafo  # Puntero a la instancia C++

    def __cinit__(self):
        self.c_grafo = new GrafoDisperso()

    def __dealloc__(self):
        del self.c_grafo

    def cargar_datos(self, archivo: str):
        # Convertir str python a string C++
        cdef string c_archivo = archivo.encode('utf-8')
        self.c_grafo.cargarDatos(c_archivo)

    def obtener_grado(self):
        cdef pair[int, int] resultado = self.c_grafo.obtenerGrado()
        return (resultado.first, resultado.second)

    def bfs(self, nodo_inicio: int, profundidad_max: int):
        cdef vector[pair[int, int]] resultado = self.c_grafo.BFS(nodo_inicio, profundidad_max)
        # Convertir vector de pairs a lista de tuplas de Python
        py_resultado = []
        for i in range(resultado.size()):
            py_resultado.append((resultado[i].first, resultado[i].second))
        return py_resultado

    def get_vecinos(self, nodo: int):
        cdef vector[int] resultado = self.c_grafo.getVecinos(nodo)
        return resultado

    @property
    def num_nodos(self):
        return self.c_grafo.getNumNodos()

    @property
    def num_aristas(self):
        return self.c_grafo.getNumAristas()
