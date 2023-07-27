import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def adjust_emissions(df, source_type, pollutant, percent_change):
    source_map = {'Area': 1, 'Fija': 2, 'Movil': 3}
    source_index = source_map[source_type]
    
    pollutant_map = {'PM 10': 1, 'PM 2.5': 2, 'CO': 3, 'NOX': 4, 'COV': 5, 'SO2': 6, 'PM2.5 - PM10': 7}
    pollutant_column = pollutant_map[pollutant]
    
    original_emissions = df.iloc[source_index, pollutant_column]
    adjusted_emissions = original_emissions * (1 + percent_change / 100)
    
    df.iloc[source_index, pollutant_column] = adjusted_emissions
    df.iloc[4, pollutant_column] = df.iloc[1:4, pollutant_column].sum()
    
    return df

def show_graph(df, df_adjusted):
    # Get the original and adjusted emissions for each source and pollutant
    original_emissions_area = df1.iloc[1, 1:-1].values
    original_emissions_fixed = df1.iloc[2, 1:-1].values
    original_emissions_mobile = df1.iloc[3, 1:-1].values

    adjusted_emissions_area = df_adjusted.iloc[1, 1:-1].values
    adjusted_emissions_fixed = df_adjusted.iloc[2, 1:-1].values
    adjusted_emissions_mobile = df_adjusted.iloc[3, 1:-1].values

    # Get the names of the pollutants
    pollutants = df1.columns[1:-1]

    # Create the x locations for the groups
    x = np.arange(len(pollutants)) * 2

    # Create the stacked bar plots
    width = 0.8
    fig, ax = plt.subplots()

    colors = ['#006400', '#32CD32', '#90EE90']  # DarkGreen, LimeGreen, LightGreen

    rects1a = ax.bar(x, original_emissions_area, width, color=colors[0], label='Area')
    rects1f = ax.bar(x, original_emissions_fixed, width, color=colors[1], bottom=original_emissions_area, label='Fija')
    rects1m = ax.bar(x, original_emissions_mobile, width, color=colors[2], bottom=original_emissions_area+original_emissions_fixed, label='Movil')

    rects2a = ax.bar(x + 1, adjusted_emissions_area, width, color=colors[0])
    rects2f = ax.bar(x + 1, adjusted_emissions_fixed, width, color=colors[1], bottom=adjusted_emissions_area)
    rects2m = ax.bar(x + 1, adjusted_emissions_mobile, width, color=colors[2], bottom=adjusted_emissions_area+adjusted_emissions_fixed)

    # Add some text for labels, title and custom x-axis tick labels
    ax.set_ylabel('Emisiones (Toneladas)')
    ax.set_title('Emisiones por contaminante y fuente')
    ax.set_xticks(x + 0.5)
    ax.set_xticklabels(pollutants, rotation=45)
    ax.legend()

    fig.tight_layout()

    plt.show()

# Load the spreadsheet
xlsx = pd.ExcelFile('Tabulados del Inventario Nacional de Emisiones AMM.xlsx')

# Load a sheet into a DataFrame
df1 = xlsx.parse(xlsx.sheet_names[0], skiprows=1)
df_adjusted = df1.copy()

######

### Contaminantes: PM 10, PM 2.5, CO, NOX, COV, SO2, PM2.5 - PM10
### Fuentes: Area, Fija, Movil

# Adjust the 'CO' emissions from 'Movil' by -50%
df_adjusted = adjust_emissions(df_adjusted, 'Movil', 'CO', -50)

# Adjust the 'PM 10' emissions from 'Area' by -90%
df_adjusted = adjust_emissions(df_adjusted, 'Area', 'PM 10', -90)

######

show_graph(df1, df_adjusted)
