#ifndef GRAFOBASE_H
#define GRAFOBASE_H

#include <vector>
#include <string>
#include <utility>

// Clase Abstracta (Interfaz)
class GrafoBase {
public:
    virtual ~GrafoBase() {}

    // Carga datos desde un archivo de texto (Edge List)
    virtual void cargarDatos(const std::string& archivo) = 0;

    // Retorna el ID del nodo con mayor grado y su grado
    virtual std::pair<int, int> obtenerGrado() = 0;

    // Realiza un BFS desde un nodo inicio hasta una profundidad maxima
    // Retorna un vector de pares (origen, destino) representando las aristas del subgrafo visitado
    virtual std::vector<std::pair<int, int>> BFS(int nodoInicio, int profundidadMax) = 0;

    // Obtiene los vecinos de un nodo
    virtual std::vector<int> getVecinos(int nodo) = 0;
};

#endif // GRAFOBASE_H
