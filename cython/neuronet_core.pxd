from libcpp.vector cimport vector
from libcpp.string cimport string
from libcpp.utility cimport pair

cdef extern from "../src/GrafoBase.h":
    pass

cdef extern from "../src/GrafoDisperso.h":
    cdef cppclass GrafoDisperso:
        GrafoDisperso() except +
        void cargarDatos(string archivo)
        pair[int, int] obtenerGrado()
        vector[pair[int, int]] BFS(int nodoInicio, int profundidadMax)
        vector[int] getVecinos(int nodo)
        int getNumNodos()
        int getNumAristas()
