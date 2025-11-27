#ifndef GRAFODISPERSO_H
#define GRAFODISPERSO_H

#include "GrafoBase.h"
#include <vector>
#include <string>
#include <algorithm>
#include <iostream>

class GrafoDisperso : public GrafoBase {
private:
    int numNodos;
    int numAristas;

    // Estructura CSR (Compressed Sparse Row)
    // En grafos no ponderados, 'valores' podria omitirse si solo importa la conectividad,
    // pero lo mantendremos por compatibilidad con la definicion estandar o si se agregan pesos luego.
    // Para este caso, asumiremos peso 1, asi que podriamos optimizar no usandolo, 
    // pero el requerimiento menciona "3 vectores: valores, indices de columnas, punteros de fila".
    std::vector<int> valores; 
    std::vector<int> indices_columnas; // adj
    std::vector<int> punteros_fila;    // xadj

public:
    GrafoDisperso();
    ~GrafoDisperso();

    void cargarDatos(const std::string& archivo) override;
    std::pair<int, int> obtenerGrado() override;
    std::vector<std::pair<int, int>> BFS(int nodoInicio, int profundidadMax) override;
    std::vector<int> getVecinos(int nodo) override;

    int getNumNodos() const { return numNodos; }
    int getNumAristas() const { return numAristas; }
};

#endif // GRAFODISPERSO_H
