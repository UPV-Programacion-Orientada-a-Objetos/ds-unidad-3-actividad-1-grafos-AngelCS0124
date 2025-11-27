#include "GrafoDisperso.h"
#include <fstream>
#include <sstream>
#include <iostream>
#include <queue>
#include <set>
#include <algorithm>
#include <map>

GrafoDisperso::GrafoDisperso() : numNodos(0), numAristas(0) {}

GrafoDisperso::~GrafoDisperso() {}

void GrafoDisperso::cargarDatos(const std::string& archivo) {
    std::cout << "[C++ Core] Cargando dataset '" << archivo << "'..." << std::endl;
    std::ifstream file(archivo);
    if (!file.is_open()) {
        std::cerr << "Error al abrir el archivo: " << archivo << std::endl;
        return;
    }

    // Primero leemos todas las aristas para saber cuantos nodos hay y construir la lista de adyacencia temporal
    // Usamos un map de vectores para facilitar la construccion inicial antes de pasar a CSR
    // Nota: Para grafos MUY masivos, esto podria consumir mucha RAM temporalmente. 
    // Una optimizacion seria leer dos veces: una para contar nodos/grados y reservar memoria, otra para llenar.
    // Por simplicidad y dado el limite de 500k nodos, usaremos una lista de adyacencia temporal.
    
    // Asumimos nodos numerados de 0 a N-1 o IDs arbitrarios. 
    // Si son IDs arbitrarios grandes, necesitariamos un mapeo. 
    // Los datasets de SNAP suelen ser IDs enteros. Asumiremos que podemos normalizarlos o que son densos.
    // Para seguridad, usaremos un mapeo si los IDs son muy dispersos, pero para eficiencia asumiremos
    // que max_id define el tamano.
    
    int u, v;
    int max_id = 0;
    std::vector<std::pair<int, int>> aristas_temp;
    
    std::string line;
    while (std::getline(file, line)) {
        if (line.empty() || line[0] == '#') continue;
        std::stringstream ss(line);
        if (ss >> u >> v) {
            aristas_temp.push_back({u, v});
            if (u > max_id) max_id = u;
            if (v > max_id) max_id = v;
        }
    }
    file.close();

    numNodos = max_id + 1;
    numAristas = aristas_temp.size();

    // Convertir a CSR
    // 1. Calcular grados para row_ptr
    punteros_fila.assign(numNodos + 1, 0);
    std::vector<std::vector<int>> adj_temp(numNodos);

    // Grafo no dirigido? El enunciado dice "Diferencia entre grafos dirigidos y no dirigidos".
    // SNAP web-Google es dirigido. Asumiremos dirigido segun el input.
    // Si fuera no dirigido, agregariamos tambien v->u.
    // Vamos a asumir DIRIGIDO para web-Google, pero permitiremos configurar si es necesario.
    // Por ahora, implementacion estandar dirigida segun edge list.
    
    for (const auto& arista : aristas_temp) {
        adj_temp[arista.first].push_back(arista.second);
        // Si fuera no dirigido: adj_temp[arista.second].push_back(arista.first);
    }

    // 2. Llenar CSR
    valores.clear(); // No usado realmente en no ponderado, pero llenaremos con 1s
    indices_columnas.clear();
    
    int current_idx = 0;
    for (int i = 0; i < numNodos; ++i) {
        punteros_fila[i] = current_idx;
        // Ordenar vecinos para busquedas mas rapidas si fuera necesario, o determinismo
        std::sort(adj_temp[i].begin(), adj_temp[i].end());
        
        for (int vecino : adj_temp[i]) {
            indices_columnas.push_back(vecino);
            valores.push_back(1);
            current_idx++;
        }
    }
    punteros_fila[numNodos] = current_idx;

    std::cout << "[C++ Core] Carga completa. Nodos: " << numNodos << " | Aristas: " << numAristas << std::endl;
    std::cout << "[C++ Core] Estructura CSR construida." << std::endl;
}

std::pair<int, int> GrafoDisperso::obtenerGrado() {
    int max_grado = -1;
    int nodo_max = -1;

    for (int i = 0; i < numNodos; ++i) {
        // Grado de salida en CSR es facil: row_ptr[i+1] - row_ptr[i]
        int grado = punteros_fila[i+1] - punteros_fila[i];
        if (grado > max_grado) {
            max_grado = grado;
            nodo_max = i;
        }
    }
    return {nodo_max, max_grado};
}

std::vector<int> GrafoDisperso::getVecinos(int nodo) {
    std::vector<int> vecinos;
    if (nodo < 0 || nodo >= numNodos) return vecinos;

    int inicio = punteros_fila[nodo];
    int fin = punteros_fila[nodo+1];

    for (int i = inicio; i < fin; ++i) {
        vecinos.push_back(indices_columnas[i]);
    }
    return vecinos;
}

std::vector<std::pair<int, int>> GrafoDisperso::BFS(int nodoInicio, int profundidadMax) {
    std::cout << "[C++ Core] Ejecutando BFS nativo desde " << nodoInicio << " prof " << profundidadMax << "..." << std::endl;
    std::vector<std::pair<int, int>> aristas_visitadas;
    
    if (nodoInicio < 0 || nodoInicio >= numNodos) return aristas_visitadas;

    std::queue<std::pair<int, int>> q; // nodo, nivel
    std::vector<bool> visitado(numNodos, false);
    
    q.push({nodoInicio, 0});
    visitado[nodoInicio] = true;

    while (!q.empty()) {
        int u = q.front().first;
        int nivel = q.front().second;
        q.pop();

        if (nivel >= profundidadMax) continue;

        int inicio = punteros_fila[u];
        int fin = punteros_fila[u+1];

        for (int i = inicio; i < fin; ++i) {
            int v = indices_columnas[i];
            
            // Agregamos la arista al resultado para visualizacion
            aristas_visitadas.push_back({u, v});

            if (!visitado[v]) {
                visitado[v] = true;
                q.push({v, nivel + 1});
            }
        }
    }
    
    std::cout << "[C++ Core] BFS terminado. Aristas encontradas: " << aristas_visitadas.size() << std::endl;
    return aristas_visitadas;
}
