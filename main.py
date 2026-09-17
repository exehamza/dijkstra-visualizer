import tkinter as tk
from tkinter import simpledialog, messagebox
import heapq
import time
import threading
import random

class DijkstraVisualizer:
    # Constants
    NODE_RADIUS = 20
    NODE_FONT = ("Arial", 10, "bold")
    WEIGHT_FONT = ("Arial", 14, "bold")
    LINE_WIDTH = 3
    ANIMATION_DELAY = 0.4
    PATH_DELAY = 0.2

    # Colors
    COLOR_DEFAULT = "#4CAF50"    # Vibrant Green
    COLOR_START = "#00bcd4"      # Cyan
    COLOR_END = "#FF5722"        # Deep Orange
    COLOR_VISITING = "#FFEB3B"   # Bright Yellow
    COLOR_PERMANENT = "#B0BEC5"   # Light Gray for finalized node
    COLOR_PATH = "#E91E63"       # Pink/Magenta (Used for Shortest Path)
    COLOR_BACKGROUND = "#f0f0f0" # Light Gray Background
    COLOR_EDGE = "#757575"       # Default line color

    def __init__(self, root):
        self.root = root
        self.root.title("Dijkstra Algorithm Visualizer")
        self.canvas = tk.Canvas(root, width=1280, height=720, bg=self.COLOR_BACKGROUND)
        self.canvas.pack(fill="both", expand=True)

        self.nodes = []
        self.edges = []
        self.start_node = None
        self.end_node = None
        self.running = False
        self.dist = {}

        self.btn_frame = tk.Frame(root, bg='white')
        self.btn_frame.pack(pady=10)
        
        # Buttons
        tk.Button(self.btn_frame, text="Set Start", command=self.set_start, bg='#E0F7FA', fg='black').grid(row=0, column=0, padx=5, ipadx=10, ipady=5)
        tk.Button(self.btn_frame, text="Set End", command=self.set_end, bg='#FFCCBC', fg='black').grid(row=0, column=1, padx=5, ipadx=10, ipady=5)
        tk.Button(self.btn_frame, text="Run", command=self.run_dijkstra_thread, bg='#8BC34A', fg='white', font=("Arial", 10, "bold")).grid(row=0, column=2, padx=15, ipadx=20, ipady=5)
        tk.Button(self.btn_frame, text="Reset", command=self.reset, bg='#BDBDBD', fg='black').grid(row=0, column=3, padx=5, ipadx=10, ipady=5)

        self.canvas.bind("<Button-1>", self.add_node)
        self.canvas.bind("<Button-3>", self.connect_nodes)

    def add_node(self, event):
        if self.running: return
        x, y = event.x, event.y
        node_id = len(self.nodes)
        node = {"x": x, "y": y, "id": node_id}
        self.nodes.append(node)
        
        self.canvas.create_oval(x-self.NODE_RADIUS, y-self.NODE_RADIUS, x+self.NODE_RADIUS, y+self.NODE_RADIUS, 
                                fill=self.COLOR_DEFAULT, outline="#388E3C", width=2, tags=f"node{node_id}")
        self.canvas.create_text(x, y, text=str(node_id), fill="white", font=self.NODE_FONT, tags=f"text{node_id}")

    def connect_nodes(self, event):
        if self.running: return
        if len(self.nodes) < 2: return
        
        x, y = event.x, event.y
        nearest = self.get_nearest_node(x, y)

        if not hasattr(self, 'temp_node'):
            self.temp_node = nearest
            self.canvas.itemconfig(f"node{nearest['id']}", fill="gray")
        else:
            if self.temp_node["id"] == nearest["id"]: 
                self.canvas.itemconfig(f"node{self.temp_node['id']}", fill=self.COLOR_DEFAULT)
                del self.temp_node
                return

            #weight = simpledialog.askinteger("Edge Weight", "Enter weight (must be positive):", minvalue=1)
            weight = random.randint(1,50)

            if weight is not None:
                # Store the edges
                self.edges.append((self.temp_node["id"], nearest["id"], weight))
                self.edges.append((nearest["id"], self.temp_node["id"], weight))
                
                # Draw the line
                u_id, v_id = min(self.temp_node['id'], nearest['id']), max(self.temp_node['id'], nearest['id'])
                line_tag = f"line_{u_id}_{v_id}"
                
                # Prevent edge duplicates
                if not self.canvas.find_withtag(line_tag):
                    self.canvas.create_line(self.temp_node["x"], self.temp_node["y"], nearest["x"], nearest["y"], 
                                            fill=self.COLOR_EDGE, width=self.LINE_WIDTH, tags=line_tag, dash=(4, 2))
                    
                    midx = (self.temp_node["x"] + nearest["x"]) / 2
                    midy = (self.temp_node["y"] + nearest["y"]) / 2
                    
                    # Add background and weight text
                    self.canvas.create_rectangle(midx - 15, midy - 10, midx + 15, midy + 10, fill="white", tags=f"weight_bg_{line_tag}", outline="")
                    self.canvas.create_text(midx, midy, text=str(weight), fill="#212121", font=self.WEIGHT_FONT, tags=f"weight_{line_tag}")
                    
                    # Re-stack nodes on top of lines/weights
                    for node_id in [self.temp_node['id'], nearest['id']]:
                        self.canvas.tag_raise(f"node{node_id}")
                        self.canvas.tag_raise(f"text{node_id}")
                else:
                    pass

            # Reset temporary node colors
            self._reset_node_color(self.temp_node['id'])
            self._reset_node_color(nearest['id'])
            del self.temp_node

    def _reset_node_color(self, node_id):
        color = self.COLOR_START if node_id == self.start_node else \
                (self.COLOR_END if node_id == self.end_node else self.COLOR_DEFAULT)
        self.canvas.itemconfig(f"node{node_id}", fill=color, outline="#388E3C")

    def set_start(self):
        self._set_special_node("Start Node", self.start_node, self.COLOR_START, 'start_node')

    def set_end(self):
        self._set_special_node("End Node", self.end_node, self.COLOR_END, 'end_node')

    def _set_special_node(self, title, current_id, color, attr_name):
        if self.running: return
        node_id = simpledialog.askinteger(title, f"Enter {title.lower()} ID (0 to {len(self.nodes) - 1}):")
        if node_id is not None and 0 <= node_id < len(self.nodes):
            
            # Reset previous node color
            if current_id is not None:
                 self.canvas.itemconfig(f"node{current_id}", fill=self.COLOR_DEFAULT, outline="#388E3C")
                 
            # Set new node and color
            setattr(self, attr_name, node_id)
            self.canvas.itemconfig(f"node{node_id}", fill=color, outline="#388E3C")

    def get_nearest_node(self, x, y):
        return min(self.nodes, key=lambda n: (n["x"]-x)**2 + (n["y"]-y)**2)

    def run_dijkstra_thread(self):
        self.reset_colors()
        threading.Thread(target=self.run_dijkstra).start()

    def reset_colors(self):
        # Reset all nodes and lines to default/initial
        for node in self.nodes:
            self._reset_node_color(node['id']) # Use the helper function to respect start/end

        # Reset all lines to default color and width
        for u, v, w in self.edges:
            line_tag = f"line_{min(u, v)}_{max(u, v)}"
            if u < v: # Only target one of the two edge entries
                 self.canvas.itemconfig(line_tag, fill=self.COLOR_EDGE, width=self.LINE_WIDTH)
                 
        self.root.update()

    def run_dijkstra(self):
        if self.start_node is None or self.end_node is None:
            messagebox.showerror("Error", "Please set both start and end nodes first.")
            return

        self.running = True
        self.reset_colors()
        
        # Standard Dijkstra setup
        graph = {node["id"]: [] for node in self.nodes}
        for u, v, w in self.edges:
            graph[u].append((v, w))

        self.dist = {n["id"]: float("inf") for n in self.nodes} 
        prev = {n["id"]: None for n in self.nodes}
        self.dist[self.start_node] = 0
        pq = [(0, self.start_node)]
        
        self.canvas.itemconfig(f"node{self.start_node}", fill=self.COLOR_START, outline="#00838F") # Darker outline for start
        self.root.update()

        while pq and self.running:
            d, u = heapq.heappop(pq)
            
            # Use self.dist for comparison
            if d > self.dist[u]: continue 

            if u != self.start_node and u != self.end_node:
                self.canvas.itemconfig(f"node{u}", fill=self.COLOR_VISITING, outline="#FBC02D")
            self.root.update()
            time.sleep(self.ANIMATION_DELAY)

            if u == self.end_node:
                break # Path found

            for v, w in graph[u]:
                # Use self.dist for relaxation
                if self.dist[u] + w < self.dist[v]:
                    self.dist[v] = self.dist[u] + w
                    prev[v] = u
                    heapq.heappush(pq, (self.dist[v], v))
                    
                    line_tag = f"line_{min(u, v)}_{max(u, v)}"
                    self.canvas.itemconfig(line_tag, fill=self.COLOR_VISITING, width=self.LINE_WIDTH + 1)
                    
                    if v != self.start_node and v != self.end_node:
                        self.canvas.itemconfig(f"node{v}", fill="#B3E5FC", outline="#0288D1")

                    self.root.update()
                    time.sleep(self.ANIMATION_DELAY / 2)
                    
                    # Revert edge and neighbor color
                    self.canvas.itemconfig(line_tag, fill=self.COLOR_EDGE, width=self.LINE_WIDTH)
                    if v != self.start_node and v != self.end_node:
                        self.canvas.itemconfig(f"node{v}", fill=self.COLOR_DEFAULT, outline="#388E3C")


            if u != self.start_node and u != self.end_node:
                 self.canvas.itemconfig(f"node{u}", fill=self.COLOR_PERMANENT, outline="#78909C") 
            self.root.update()
            
        self.highlight_path(prev)
        self.running = False

    def highlight_path(self, prev):
        u = self.end_node
        path = []
        while u is not None:
            path.append(u)
            u = prev[u]
        path.reverse()

        if path[0] != self.start_node:
            messagebox.showinfo("Result", "No path found from start to end node.")
            return

        total_weight = self.dist[self.end_node] 
        messagebox.showinfo("Result", f"Shortest Path Found with Total Weight: {total_weight}")

        # Highlight the path sequentially
        for i in range(len(path)-1):
            n1, n2 = path[i], path[i+1]
            
            # Highlight Node 1
            if n1 != self.start_node and n1 != self.end_node:
                self.canvas.itemconfig(f"node{n1}", fill=self.COLOR_PATH, outline="#C2185B")
            
            # Highlight Edge
            u_id, v_id = min(n1, n2), max(n1, n2)
            line_tag = f"line_{u_id}_{v_id}"
            self.canvas.itemconfig(line_tag, fill=self.COLOR_PATH, width=self.LINE_WIDTH + 2, dash="") # Solid line for path
            
            self.root.update()
            time.sleep(self.PATH_DELAY)
            
        # Highlight End Node
        self.canvas.itemconfig(f"node{self.end_node}", fill=self.COLOR_PATH, outline="#C2185B")
        self.root.update()

    def reset(self):
        if self.running: 
            messagebox.showwarning("Warning", "Algorithm is currently running. Please wait.")
            return
        
        self.canvas.delete("all")
        self.nodes = []
        self.edges = []
        self.start_node = None
        self.end_node = None
        self.dist = {} # Reset dist as well

if __name__ == "__main__":
    root = tk.Tk()
    app = DijkstraVisualizer(root)
    root.mainloop()