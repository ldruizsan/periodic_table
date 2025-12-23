from mendeleev.fetch import fetch_table
import pandas as pd

elements = pd.DataFrame(fetch_table("elements"))
elements.set_index("atomic_number",inplace=True)
#print(elements.columns)

elements_df = pd.DataFrame(data=elements, columns=["_annotation","atomic_radius","atomic_volume", "block", 
                                                   "description", "group_id","name","period","series_id","en_pauling","symbol",
                                                   "atomic_weight","electronic_configuration","is_monoisotopic",
                                                   "is_radioactive","cas","fusion_heat","evaporation_heat", 
                                                   "thermal_conductivity","density","heat_of_formation"], index=elements.index)
elements_df.fillna(value="No data available", inplace=True)

"""
elements = {}
for _, row in elements.iterrows():
# Skip if missing crucial data
    if pd.isna(row['symbol']) or pd.isna(row['period']) or pd.isna(row['group_id']):
        continue
    
# Calculate position
period = int(row['period'])
group = int(row['group_id']) if pd.notna(row['group_id']) else 0

# Adjust positions for lanthanides and actinides
if row['block'] == 'f':
    if period == 6:  # Lanthanides
        period = 8
        group = int(row['atomic_number']) - 57 + 2
    elif period == 7:  # Actinides
        period = 9
        group = int(row['atomic_number']) - 89 + 2


elements[row['symbol']] = {
    'position': (period - 1, group - 1 if group > 0 else 17),
    'category': row['block'] if pd.notna(row['block']) else 'unknown',
    'electronegativity': row['en_pauling'],
    'atomic_number': row['atomic_number'],
    'atomic_mass': row['atomic_weight'],
    'name': row['name'],
    'block': row['block'],
    'electronic_configuration': row['electronic_configuration']
}

print(elements)

for symbol, data in elements.items():
            row, col = data['position']
            category = data['category']
            print(f"Category: {category}")
"""