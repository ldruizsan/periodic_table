from flask import Flask, render_template, jsonify, url_for
import pandas as pd
import numpy as np
from get_element import elements_df as elements
from mendeleev.fetch import fetch_table

app = Flask(__name__)

# Fetch series and merge with elements to provide `series_name`
series = pd.DataFrame(fetch_table("series"))
# Ensure `atomic_number` is a normal column (was the index in `elements`)
if 'atomic_number' not in elements.columns:
    elements = elements.reset_index()
merged_df = pd.merge(elements, series, left_on='series_id', right_on='id', how='left')
if '_annotation' in merged_df.columns:
    merged_df.drop(columns=["_annotation"], inplace=True)
merged_df.rename(columns={"id_x": "series_id", "name_x": "name", "name_y": "series_name"}, inplace=True)

# Hard-coded element positions (copied from your GUI version)
element_positions = {
    "H": (0, 0), "He": (0, 17),
    "Li": (1, 0), "Be": (1, 1), "B": (1, 12), "C": (1, 13), "N": (1, 14), "O": (1, 15), "F": (1, 16), "Ne": (1, 17),
    "Na": (2, 0), "Mg": (2, 1),"Al": (2,12), "Si": (2,13), "P": (2,14), "S": (2,15), "Cl": (2,16), "Ar": (2,17),
    "K": (3, 0), "Ca": (3, 1), "Sc": (3, 2), "Ti": (3, 3), "V": (3, 4), "Cr": (3, 5),"Mn": (3,6), "Fe": (3,7), "Co": (3,8), "Ni": (3,9), "Cu": (3,10), "Zn": (3,11), "Ga": (3,12), "Ge": (3,13), "As": (3,14), "Se": (3,15), "Br": (3,16), "Kr": (3,17),
    "Rb": (4, 0), "Sr": (4, 1), "Y": (4, 2), "Zr": (4, 3), "Nb": (4, 4), "Mo": (4, 5), "Tc": (4, 6),"Ru": (4, 7), "Rh": (4, 8), "Pd": (4, 9), "Ag": (4, 10),"Cd": (4, 11),"In": (4, 12),"Sn": (4, 13),"Sb": (4, 14),"Te": (4, 15),"I": (4, 16),"Xe": (4, 17),
    "Cs": (5, 0), "Ba": (5, 1), "Hf": (5, 3), "Ta": (5, 4), "W": (5, 5), "Re": (5, 6), "Os": (5, 7), "Ir": (5, 8), "Pt": (5, 9), "Au": (5, 10), "Hg": (5, 11), "Tl": (5, 12), "Pb": (5, 13), "Bi": (5, 14), "Po": (5, 15), "At": (5, 16), "Rn": (5, 17),
    "Fr": (6, 0), "Ra": (6, 1), "Rf": (6, 3), "Db": (6, 4), "Sg": (6, 5), "Bh": (6, 6), "Hs": (6, 7), "Mt": (6, 8), "Ds": (6, 9), "Rg": (6, 10), "Cn": (6, 11), "Nh": (6, 12), "Fl": (6, 13), "Mc": (6, 14), "Lv": (6, 15), "Ts": (6, 16), "Og": (6, 17),
    "La": (8, 2), "Ce": (8, 3), "Pr": (8, 4),"Nd": (8, 5), "Pm": (8, 6), "Sm": (8, 7), "Eu": (8, 8), "Gd": (8,9), "Tb":(8,10), "Dy": (8,11), "Ho": (8,12), "Er": (8,13), "Tm": (8,14), "Yb": (8,15), "Lu": (8,16),
    "Ac": (9, 2), "Th": (9, 3),  "Pa": (9, 4), "U": (9, 5), "Np": (9, 6), "Pu": (9, 7), "Am": (9, 8), "Cm": (9, 9),"Bk": (9, 10),"Cf": (9, 11), "Es": (9, 12), "Fm": (9, 13), "Md": (9, 14), "No": (9, 15), "Lr": (9, 16),
}

# build reverse mapping for template rendering
symbols_by_pos = {pos: sym for sym, pos in element_positions.items()}


def get_element_category(symbol):
    """Categorize element into 10 main families."""
    try:
        # Known metalloids (At classified as metalloid)
        metalloids = {'B', 'Si', 'Ge', 'As', 'Sb', 'Te', 'At'}
        # Known nonmetals
        nonmetals = {'H', 'C', 'N', 'O', 'P', 'S', 'Se'}
        # Post-transition metals (include Po)
        post_transition = {'Al', 'Ga', 'In', 'Tl', 'Sn', 'Pb', 'Bi', 'Po'}
        # Synthetic elements with uncertain properties (classify as nonmetals)
        synthetic_nonmetals = {'Ts', 'Og'}
        
        row = merged_df[merged_df['symbol'] == symbol].iloc[0]
        group = float(row.get('group_id', 0)) if row.get('group_id') != 'No data available' else 0
        period = float(row.get('period', 0)) if row.get('period') != 'No data available' else 0
        block = row.get('block', '')
        
        # Family 4: Lanthanides (includes La)
        if symbol == 'La' or (period == 6 and block == 'f'):
            return 'lanthanide'
        
        # Family 5: Actinides (includes Ac)
        if symbol == 'Ac' or (period == 7 and block == 'f'):
            return 'actinide'
        
        # Family 3: Transition Metals (block d)
        if block == 'd':
            return 'transition-metal'
        
        # Family 1: Alkali Metals
        if group == 1 and period > 1:
            return 'alkali-metal'
        
        # Family 2: Alkaline Earth Metals
        if group == 2 and period > 1:
            return 'alkaline-earth'
        
        # Family 9: Metalloids (check before halogens so At is classified correctly)
        if symbol in metalloids:
            return 'metalloid'

        # Family 10: Post-transition Metals
        if symbol in post_transition:
            return 'post-transition-metal'

        # Family 6: Halogens (exclude Ts)
        if group == 17 and symbol != 'Ts':
            return 'halogen'

        # Family 7: Noble Gases (exclude Og)
        if group == 18 and symbol != 'Og':
            return 'noble-gas'
        
        # Family 8: Nonmetals (includes synthetic elements)
        if symbol in nonmetals or symbol in synthetic_nonmetals:
            return 'nonmetal'
        
        # Default fallback to nonmetal
        return 'nonmetal'
    except:
        return 'nonmetal'


@app.route('/')
def index():
    # Pass basic grid dimensions and symbol mapping to the template
    # Traditional A/B group labels (old notation) for 18 columns
    group_labels = [
        "IA", "IIA", "IIIB", "IVB", "VB", "VIB", "VIIB", "VIII",
        "VIII", "VIII", "IB", "IIB", "IIIA", "IVA", "VA", "VIA",
        "VIIA", "VIIIA"
    ]
    # Build category mapping for all symbols
    symbol_categories = {sym: get_element_category(sym) for sym in symbols_by_pos.values()}

    # Build metadata for tiles: atomic number, name, atomic weight
    symbol_meta = {}
    for sym in symbols_by_pos.values():
        try:
            row = merged_df[merged_df['symbol'] == sym].iloc[0]
            # prefer explicit atomic_number column if available
            atomic_number = ''
            if 'atomic_number' in row.index and pd.notna(row['atomic_number']):
                try:
                    atomic_number = int(row['atomic_number'])
                except Exception:
                    atomic_number = str(row['atomic_number'])
            atomic_weight = row.get('atomic_weight', 'No data')
            name = row.get('name', '')
            # Convert nan to empty/string and format numeric atomic weights to 3 decimals
            if pd.isna(atomic_weight):
                atomic_weight = 'No data'
            else:
                try:
                    awf = float(atomic_weight)
                    atomic_weight = f"{awf:.3f}"
                except Exception:
                    atomic_weight = str(atomic_weight)
            symbol_meta[sym] = {
                'atomic_number': atomic_number,
                'name': str(name),
                'atomic_weight': str(atomic_weight)
            }
        except Exception:
            symbol_meta[sym] = {
                'atomic_number': '',
                'name': '',
                'atomic_weight': ''
            }

    # Extract electronegativity values for heatmap
    en_values = {}
    en_min, en_max = float('inf'), float('-inf')
    for sym in symbols_by_pos.values():
        try:
            row = merged_df[merged_df['symbol'] == sym].iloc[0]
            en = row.get('en_pauling', None)
            if pd.notna(en):
                en_val = float(en)
                en_values[sym] = en_val
                en_min = min(en_min, en_val)
                en_max = max(en_max, en_val)
        except:
            pass
    
    # Normalize electronegativity to 0-1 and generate heatmap colors (red=high, blue=low)
    heatmap_colors = {}
    if en_min != float('inf') and en_max != en_min:
        for sym, en_val in en_values.items():
            normalized = (en_val - en_min) / (en_max - en_min)
            # Red (high EN) to Blue (low EN): interpolate RGB
            # Red: (255, 0, 0), Blue: (0, 0, 255)
            r = int(255 * normalized)
            g = 0
            b = int(255 * (1 - normalized))
            heatmap_colors[sym] = f'rgb({r}, {g}, {b})'

    # Round EN min/max for display
    en_min_rounded = round(en_min, 2) if en_min != float('inf') else 0
    en_max_rounded = round(en_max, 2) if en_max != float('-inf') else 0

    return render_template('index.html', rows=range(10), cols=range(18), symbols_by_pos=symbols_by_pos, 
                          group_labels=group_labels, symbol_categories=symbol_categories,
                          symbol_meta=symbol_meta, heatmap_colors=heatmap_colors,
                          en_min=en_min_rounded, en_max=en_max_rounded,
                          # Legend placement: centered at VIIB (column 6, 0-based), rows 0-2
                          legend_row_start=0, legend_row_span=3,
                          legend_col_start=6, legend_col_span=6)


@app.route('/api/element/<symbol>')
def element_api(symbol):
    try:
        row = merged_df[merged_df['symbol'] == symbol].iloc[0]
        atomic_number = merged_df[merged_df['symbol'] == symbol].index[0]
        def _serialize(v):
            # Handle pandas missing
            if pd.isna(v):
                return None
            # numpy scalar types -> native python types
            if isinstance(v, (np.integer,)):
                return int(v)
            if isinstance(v, (np.floating,)):
                return float(v)
            if isinstance(v, (np.bool_,)):
                return bool(v)
            # pandas Timestamp or other types -> string
            if isinstance(v, (pd.Timestamp,)):
                return str(v)
            # Already JSON-serializable types
            if isinstance(v, (str, int, float, bool, list, dict)):
                return v
            # Fallback to string
            return str(v)

        data = {
            'name': _serialize(row.get('name', 'No data available')),
            'symbol': _serialize(row.get('symbol', symbol)),
            'atomic_number': int(atomic_number),
            'atomic_weight': _serialize(row.get('atomic_weight', 'No data available')),
            'period': _serialize(row.get('period', 'No data available')),
            'group': _serialize(row.get('group_id', 'No data available')),
            'block': _serialize(row.get('block', 'No data available')),
            'electronic_configuration': _serialize(row.get('electronic_configuration', 'No data available')),
            'en_pauling': _serialize(row.get('en_pauling', 'No data available')),
            'density': _serialize(row.get('density', 'No data available')),
            'atomic_radius': _serialize(row.get('atomic_radius', 'No data available')),
            'description': _serialize(row.get('description', 'No data available')),
            'series_name': _serialize(row.get('series_name', 'No data available'))
        }
        # Ensure API returns atomic weight formatted to 3 decimal places when available
        aw = data.get('atomic_weight')
        if aw is not None:
            try:
                awf = float(aw)
                data['atomic_weight'] = f"{awf:.3f}"
            except Exception:
                data['atomic_weight'] = str(aw)
        return jsonify(success=True, data=data)
    except IndexError:
        return jsonify(success=False, error=f"Element '{symbol}' not found"), 404
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500


if __name__ == '__main__':
    app.run(debug=True)
