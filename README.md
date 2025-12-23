# Periodic Table Application

A comprehensive and interactive Periodic Table of Elements application. This project provides both a web-based interface (using Flask) and a desktop interface (using Tkinter) to explore chemical elements, their properties, and trends.

## Features

*   **Interactive Grid:** Navigate the periodic table with a clean, responsive layout.
*   **Element Details:** Click on any element to view detailed properties, including:
    *   Atomic Number & Weight
    *   Period, Group, and Block
    *   Electron Configuration
    *   Density, Atomic Radius, and more.
*   **Electronegativity Heatmap:** Toggle a heatmap view to visualize Pauling electronegativity trends across the table (Web version).
*   **Element Families:** Color-coded categorization of element families (Alkali Metals, Noble Gases, Transition Metals, etc.).
*   **Dual Interface:**
    *   **Web App:** A modern, browser-based experience.
    *   **Desktop App:** A lightweight Tkinter-based desktop viewer.

## Tech Stack

*   **Python:** Core logic and data processing.
*   **Flask:** Web framework for the browser interface.
*   **Pandas & NumPy:** Data manipulation.
*   **Mendeleev:** Source library for chemical element data.
*   **HTML/CSS/JavaScript:** Frontend for the web application.
*   **Tkinter:** GUI for the desktop application.

## Installation

1.  Clone the repository.
2.  Install the required dependencies:
    ```bash
    pip install flask pandas numpy mendeleev
    ```

## Usage

### Web Application
Run the Flask server:
```bash
python webapp.py
```
Open your browser and navigate to `http://127.0.0.1:5000/`.

### Desktop Application
Run the Tkinter app:
```bash
python app.py
```
