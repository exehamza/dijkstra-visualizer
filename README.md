# Dijkstra's Algorithm Visualizer 🗺️

An interactive pathfinding visualizer built in Python using **Tkinter** and **multithreading**. This tool demonstrates how Dijkstra's shortest-path algorithm explores a grid and finds the optimal route, all while keeping the user interface completely responsive.

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange.svg)

---

## ✨ Features

* **Interactive Grid:** Click and drag to set start points, end points, and draw obstacles/walls.
* **Real-Time Visualization:** Watch the algorithm explore nodes step-by-step to find the shortest path.
* **Non-Blocking UI (Multithreaded):** Utilizes Python's `threading` module to ensure the application window never freezes or lags while calculations are running in the background.
* **Efficient Implementation:** Powered by Python's `heapq` (priority queue) module for optimal performance.

---

## 🛠️ Technologies Used

* **Python 3.x**
* **Tkinter** (Built-in GUI framework)
* **Heapq** (Priority queue for the algorithm)
* **Threading** (Background execution for smooth animations)

---

## 🚀 How to Run Locally

Since this project relies entirely on Python's built-in libraries, you don't need to install any external packages!

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/exehamza/dijkstra-visualizer.git](https://github.com/exehamza/dijkstra-visualizer.git)
    ```

2. **Navigate to the project directory**
    ```bash
    cd your-repo-name
    ```

3. **Run the script:**
    ```bash
    python main.py
    ```

## 🎮 How to Use
- Launch the program
- Left Click to add nodes
- Add **Start Node** and **End Node**
- Click **Start** to see the simulation