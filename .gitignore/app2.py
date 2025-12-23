from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel, QVBoxLayout
from get_element import elements_df as elements
import pandas as pd
import sys
from mendeleev.fetch import fetch_table

#print(elements.columns)

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

series = fetch_table("series")
series = pd.DataFrame(series)
print(series.head())

merged_df = pd.merge(elements, series, left_on='series_id', right_on='id', how='left')
merged_df.drop(columns=["_annotation"], inplace=True)
merged_df.rename(columns={"id_x": "series_id","name_x":"name","name_y":"series_name"}, inplace=True)
print(merged_df[['series_id','name','symbol','series_name']].head(10))
print(merged_df.columns)

class PeriodicTable(QWidget):
    def __init__(self):
        """Initializes the Periodic Table GUI."""
        # Initialize the base QWidget class
        super().__init__()
        self.element_data = merged_df
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Periodic Table")
        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()
        grid_layout.setSpacing(2)  # Set spacing between buttons

        # Create buttons for each element
        self.buttons = {} # Optional: store buttons if needed later
        for symbol, (row, col) in element_positions.items():
            button = QPushButton(symbol)
            button.setFixedSize(45, 45) # Adjust size for a compact look
            # Use a lambda with a default argument to capture the correct symbol
            # The 'checked' parameter is passed by the signal, but we don't need it
            button.clicked.connect(lambda checked, s=symbol: self.show_element_info(s))
            grid_layout.addWidget(button, row, col)
            self.buttons[symbol] = button

        # --- Info Display Area ---
        self.info_label = QLabel("Click an element to see its details.")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.info_label.setWordWrap(True) # Important for longer descriptions
        self.info_label.setMinimumHeight(150) # Ensure space for info

        # --- Assemble Layout ---
        main_layout.addLayout(grid_layout) # Add the grid to the main layout
        main_layout.addWidget(self.info_label) # Add the info label below the grid

        self.setLayout(main_layout)

        # --- Window Properties ---
        self.setGeometry(100, 100, 950, 650) # x, y, width, height


    def show_element_info(self, symbol):
        """Fetches and displays element information when a button is clicked."""
        try:
            # Find the element row using boolean indexing on the 'symbol' column
            element_series = self.element_data[self.element_data['symbol'] == symbol].iloc[0]

            # The index of elements_df is the atomic number
            atomic_number = self.element_data[self.element_data['symbol'] == symbol].index[0]

            # --- Format the display text ---
            # Using f-string for cleaner formatting
            info_text = f"""<b>Name:</b> {element_series['name']} ({element_series['symbol']})
                        <b>Atomic Number:</b> {atomic_number}
                        <b>Atomic Weight:</b> {element_series['atomic_weight']}
                        <b>Period:</b> {element_series['period']} | <b>Group:</b> {element_series['group_id']} | <b>Block:</b> {element_series['block']}
                        <b>Electronic Config:</b> {element_series['electronic_configuration']}
                        <b>Electronegativity (Pauling):</b> {element_series['en_pauling']}
                        <b>Density:</b> {element_series['density']}
                        <b>Atomic Radius:</b> {element_series['atomic_radius']}
                        <b>Description:</b> {element_series['description']}
                        <b>Series:</b> {element_series['series_name']}
                        """ # Added more fields and basic HTML for bolding

            self.info_label.setText(info_text)

        except IndexError:
            # Handle case where the symbol might be in element_positions but not in elements_df
            self.info_label.setText(f"Data for element '{symbol}' not found in the database.")
        except Exception as e:
            # Catch other potential errors (e.g., KeyError if a column is missing)
            self.info_label.setText(f"An error occurred retrieving data for {symbol}:\n{e}")
            print(f"Error processing symbol {symbol}: {e}") # Log error to console

# --- Main Execution ---
def main():
    app = QApplication(sys.argv) # Create the application instance
    ex = PeriodicTable()      # Create the main window
    ex.show()                    # Show the window
    sys.exit(app.exec())         # Start the event loop

if __name__ == '__main__':
    main()