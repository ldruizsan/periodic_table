import tkinter as tk

class PeriodicTable:
    def __init__(self, root):
        self.root = root
        self.root.title("Periodic Table")
        
        # Dictionary to store element data
        # Currently only contains symbols, but can be expanded
        self.elements = {
            'H': (0, 0), 'He': (0, 17),
            'Li': (1, 0), 'Be': (1, 1), 'B': (1, 12), 'C': (1, 13), 'N': (1, 14), 'O': (1, 15), 'F': (1, 16), 'Ne': (1, 17),
            'Na': (2, 0), 'Mg': (2, 1), 'Al': (2, 12), 'Si': (2, 13), 'P': (2, 14), 'S': (2, 15), 'Cl': (2, 16), 'Ar': (2, 17),
            'K': (3, 0), 'Ca': (3, 1),
            'Sc': (3, 2), 'Ti': (3, 3), 'V': (3, 4), 'Cr': (3, 5), 'Mn': (3, 6), 'Fe': (3, 7), 'Co': (3, 8),
            'Ni': (3, 9), 'Cu': (3, 10), 'Zn': (3, 11), 'Ga': (3, 12), 'Ge': (3, 13), 'As': (3, 14), 'Se': (3, 15), 'Br': (3, 16), 'Kr': (3, 17)
        }
        
        self.create_table()
    
    def create_table(self):
        # Create buttons for each element
        for symbol, (row, col) in self.elements.items():
            btn = tk.Button(self.root, text=symbol, width=5, height=2)
            btn.grid(row=row, column=col, padx=2, pady=2)
            
            # Bind click event (for future functionality)
            btn.bind('<Button-1>', lambda e, s=symbol: self.element_click(s))
    
    def element_click(self, symbol):
        # Placeholder for click functionality
        print(f"Clicked on {symbol}")

def main():
    root = tk.Tk()
    app = PeriodicTable(root)
    root.mainloop()

if __name__ == "__main__":
    main()