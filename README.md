## 🎄 Advent of Code 2025

A collection of solutions for the [Advent of Code 2025](https://adventofcode.com/2025) puzzles, implemented across four different languages to compare performance, syntax, and idiomatic patterns in a terminal-centric environment.

---

### 🚀 The Polyglot Approach

This repository explores the same mathematical logic across:
* **Python**: For rapid prototyping and native "floor division" math.
* **Go (Golang)**: For high-performance concurrency and robust I/O.
* **C++**: For maximum execution speed and low-level control.
* **JavaScript (Node.js)**: For flexible, event-driven scripting.

---

### 🛠️ Project Structure

```
.
├── Cpp/
│   ├── day-01/
│   └── day-02/
├── Go/
│   ├── day-01/
│   └── day-02/
├── JS/
│   ├── day-01/
│   └── day-02/
├── Py/
│   ├── day-01/
│   └── day-02/
└── inputs/
    ├── day-01/
    └── day-02/
```

---

### ⌨️ Development Setup (Neovim)

These solutions were crafted in a shared terminal environment of **Neovim** + **tmux** & **VSCode**.

#### 🧩 Recommended Neovim Plugins:
* **lazy.nvim**: Plugin management.
* **lspconfig**: For `gopls`, `clangd`, and `pyright` support.
* **blink.cmp**: For high-speed autocompletion.
* **LuaSnip**: Custom snippets for docstrings and math utilities.
* **Telescope**: For project-wide searching (`live_grep`).

#### 🧩 Recommended VSCode Plugins:
* **C/C++ (Microsoft)**: Provides IntelliSense and debugging. Requires **g++** on macOS (installed via Xcode Command Line Tools) or **MinGW-w64** on Windows.
* **Python (Microsoft)**: Essential for Python development; includes native support for **venv** for environment isolation.
* **Prettier**: To maintain consistent formatting across all four languages.

#### 🏃 Quick Run Commands:
* **Python**: `python3 day-xx.py` or `python3 day-xx.py < input-xx.txt`
* **Go**: `go run day-xx.go`
* **C++**: `g++ -O3 day-xx.cpp -o output && ./output`
* **Node**: `node day-xx.js`
