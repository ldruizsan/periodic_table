import tkinter as tk
#from mendeleev.fetch import fetch_table
from get_element import elements
import pandas as pd
class PeriodicTable:
    def __init__(self, root):
        self.root = root
        self.root.title("Periodic Table")
        self.element_data = elements
        self.create_table()

    def create_table(self):
         # Element data (symbol, row, column)
        element_positions = {
            "H": (0, 0), "He": (0, 17),  # Period 1
            "Li": (1, 0), "Be": (1, 1), "B": (1, 12), "C": (1, 13), "N": (1, 14), "O": (1, 15), "F": (1, 16), "Ne": (1, 17),  # Period 2
            "Na": (2, 0), "Mg": (2, 1),"Al": (2,12), "Si": (2,13), "P": (2,14), "S": (2,15), "Cl": (2,16), "Ar": (2,17),
            "K": (3, 0), "Ca": (3, 1), "Sc": (3, 2), "Ti": (3, 3), "V": (3, 4), "Cr": (3, 5),"Mn": (3,6), "Fe": (3,7), "Co": (3,8), "Ni": (3,9), "Cu": (3,10), "Zn": (3,11), "Ga": (3,12), "Ge": (3,13), "As": (3,14), "Se": (3,15), "Br": (3,16), "Kr": (3,17),
            "Rb": (4, 0), "Sr": (4, 1), "Y": (4, 2), "Zr": (4, 3), "Nb": (4, 4), "Mo": (4, 5), "Tc": (4, 6),"Ru": (4, 7), "Rh": (4, 8), "Pd": (4, 9), "Ag": (4, 10),"Cd": (4, 11),"In": (4, 12),"Sn": (4, 13),"Sb": (4, 14),"Te": (4, 15),"I": (4, 16),"Xe": (4, 17),
            "Cs": (5, 0), "Ba": (5, 1), "Hf": (5, 3), "Ta": (5, 4), "W": (5, 5), "Re": (5, 6), "Os": (5, 7), "Ir": (5, 8), "Pt": (5, 9), "Au": (5, 10), "Hg": (5, 11), "Tl": (5, 12), "Pb": (5, 13), "Bi": (5, 14), "Po": (5, 15), "At": (5, 16), "Rn": (5, 17),
            "Fr": (6, 0), "Ra": (6, 1), "Rf": (6, 3), "Db": (6, 4), "Sg": (6, 5), "Bh": (6, 6), "Hs": (6, 7), "Mt": (6, 8), "Ds": (6, 9), "Rg": (6, 10), "Cn": (6, 11), "Nh": (6, 12), "Fl": (6, 13), "Mc": (6, 14), "Lv": (6, 15), "Ts": (6, 16), "Og": (6, 17),
            "La": (8, 2), "Ce": (8, 3), "Pr": (8, 4),"Nd": (8, 5), "Pm": (8, 6), "Sm": (8, 7), "Eu": (8, 8), "Gd": (8,9), "Tb":(8,10), "Dy": (8,11), "Ho": (8,12), "Er": (8,13), "Tm": (8,14), "Yb": (8,15), "Lu": (8,16),
            "Ac": (9, 2), "Th": (9, 3),  "Pa": (9, 4), "U": (9, 5), "Np": (9, 6), "Pu": (9, 7), "Am": (9, 8), "Cm": (9, 9),"Bk": (9, 10),"Cf": (9, 11), "Es": (9, 12), "Fm": (9, 13), "Md": (9, 14), "No": (9, 15), "Lr": (9, 16),
        }

        # Create buttons for each element
        for symbol, (row,col) in element_positions.items():
            btn = tk.Button(self.root, text=symbol, width=5, height=2, command=lambda s=symbol: self.element_click(s))
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            
            # Configure row and column weights for proper resizing (IMPORTANT!)
        for i in range(9):  # Adjust to the number of rows you need
            self.root.grid_rowconfigure(i, weight=1)  # Make rows expandable
        for i in range(18):  # Adjust to the number of columns
            self.root.grid_columnconfigure(i, weight=1) # Make columns expandable
            # Bind click event (for future functionality)
            #btn.bind('<Button-1>', lambda e, s=symbol: self.element_click(s))
    
    def element_click(self, symbol):
        # Placeholder for click functionality
        print(f"Clicked on {symbol}")

def main():
    root = tk.Tk()
    app = PeriodicTable(root)
    root.mainloop()

if __name__ == "__main__":
    main()

