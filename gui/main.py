import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import time
import os
import sys

# Asegurarse de que se puede importar el modulo compilado
sys.path.append(os.getcwd())

try:
    from neuronet import PyGrafo
    print("Usando motor C++ optimizado.")
except ImportError:
    from neuronet_mock import PyGrafo
    messagebox.showwarning("Advertencia", "No se encontró la extensión C++ compilada.\nSe usará una implementación en Python (Lenta).\nPara máximo rendimiento, compile el módulo C++.")
    print("Usando motor Python (Mock).")

class NeuroNetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NeuroNet: Análisis de Grafos Masivos")
        self.root.geometry("1000x700")

        self.grafo = PyGrafo()
        self.archivo_cargado = False

        self._setup_ui()

    def _setup_ui(self):
        # Panel de Control (Izquierda)
        control_frame = tk.Frame(self.root, width=250, bg="#f0f0f0", padx=10, pady=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(control_frame, text="NeuroNet Control", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=(0, 20))

        # Cargar Datos
        tk.Button(control_frame, text="Cargar Dataset", command=self.cargar_dataset, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(fill=tk.X, pady=5)
        
        self.lbl_info = tk.Label(control_frame, text="Nodos: 0\nAristas: 0", bg="#f0f0f0", justify=tk.LEFT)
        self.lbl_info.pack(pady=10)

        # Analisis
        tk.Label(control_frame, text="Análisis", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=(20, 5))
        
        tk.Button(control_frame, text="Nodo Mayor Grado", command=self.calcular_mayor_grado, bg="#2196F3", fg="white").pack(fill=tk.X, pady=5)
        self.lbl_grado = tk.Label(control_frame, text="", bg="#f0f0f0", wraplength=230)
        self.lbl_grado.pack(pady=5)

        # Simulacion BFS
        tk.Label(control_frame, text="Simulación BFS", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=(20, 5))
        
        tk.Label(control_frame, text="Nodo Inicio:", bg="#f0f0f0").pack(anchor="w")
        self.entry_inicio = tk.Entry(control_frame)
        self.entry_inicio.pack(fill=tk.X)

        tk.Label(control_frame, text="Profundidad:", bg="#f0f0f0").pack(anchor="w")
        self.entry_prof = tk.Entry(control_frame)
        self.entry_prof.insert(0, "2")
        self.entry_prof.pack(fill=tk.X)

        tk.Button(control_frame, text="Ejecutar BFS", command=self.ejecutar_bfs, bg="#FF9800", fg="white").pack(fill=tk.X, pady=10)

        # Area de Visualizacion (Derecha)
        self.viz_frame = tk.Frame(self.root, bg="white")
        self.viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def cargar_dataset(self):
        filename = filedialog.askopenfilename(title="Seleccionar Dataset", filetypes=(("Archivos de Texto", "*.txt"), ("Todos los archivos", "*.*")))
        if filename:
            start_time = time.time()
            self.grafo.cargar_datos(filename)
            end_time = time.time()
            
            nodos = self.grafo.num_nodos
            aristas = self.grafo.num_aristas
            
            self.lbl_info.config(text=f"Nodos: {nodos}\nAristas: {aristas}\nTiempo Carga: {end_time - start_time:.4f}s")
            self.archivo_cargado = True
            messagebox.showinfo("Éxito", f"Dataset cargado correctamente.\n{nodos} nodos, {aristas} aristas.")

    def calcular_mayor_grado(self):
        if not self.archivo_cargado:
            messagebox.showwarning("Aviso", "Primero cargue un dataset.")
            return

        nodo, grado = self.grafo.obtener_grado()
        self.lbl_grado.config(text=f"Nodo: {nodo}\nGrado: {grado}")

    def ejecutar_bfs(self):
        if not self.archivo_cargado:
            messagebox.showwarning("Aviso", "Primero cargue un dataset.")
            return

        try:
            inicio = int(self.entry_inicio.get())
            prof = int(self.entry_prof.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos.")
            return

        start_time = time.time()
        aristas = self.grafo.bfs(inicio, prof)
        end_time = time.time()

        print(f"BFS encontrado: {len(aristas)} aristas en {end_time - start_time:.4f}s")

        self.dibujar_subgrafo(aristas, inicio)

    def dibujar_subgrafo(self, aristas, inicio):
        self.ax.clear()
        
        if not aristas:
            self.ax.text(0.5, 0.5, "No se encontraron conexiones o nodo aislado", ha='center')
            self.canvas.draw()
            return

        G = nx.DiGraph() # O Graph() si fuera no dirigido
        G.add_edges_from(aristas)

        pos = nx.spring_layout(G, seed=42)
        
        # Dibujar nodos
        nx.draw_networkx_nodes(G, pos, ax=self.ax, node_size=300, node_color='lightblue')
        
        # Resaltar nodo inicio
        if inicio in G:
            nx.draw_networkx_nodes(G, pos, ax=self.ax, nodelist=[inicio], node_size=500, node_color='red')

        # Dibujar aristas
        nx.draw_networkx_edges(G, pos, ax=self.ax, edge_color='gray', arrows=True)
        
        # Etiquetas
        nx.draw_networkx_labels(G, pos, ax=self.ax, font_size=8)

        self.ax.set_title(f"Subgrafo BFS desde Nodo {inicio}")
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = NeuroNetApp(root)
    root.mainloop()
