import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# TO DO: 
# Fix the colours: 1 - no data and 0 - data available
# Change title to indicator name instead of indicator code 
# Change country names on the y-axis to display full name
# Choose pretty colours 

### SPECIFY SHEET INFORMATION
sheet_featureMap = {'WDI Data': ['indicator', 'country.region', 'year'],
                    '4.2.1 (ILO - UNPL)': ['Attribute:MEASURE', 'Attribute:REF_AREA', 'Obs.Attribute:TIME_PERIOD'],
                    '4.3.1 (IMF - IR)': ['Column1.@INDICATOR', 'Column1.@REF_AREA', 'Column1.Obs.@TIME_PERIOD'],
                    '4.6.3 (ILO - INEMPL)': ['Attribute:MEASURE', 'Attribute:REF_AREA', 'Obs.Attribute:TIME_PERIOD'],
                    '4.6.4. (ILO - SP)': ['Attribute:MEASURE', 'Attribute:REF_AREA', 'Obs.Attribute:TIME_PERIOD'],
                    '4.6.5 (ILO - FLFP)': ['Attribute:MEASURE', 'Attribute:REF_AREA', 'Obs.Attribute:TIME_PERIOD']}

### Load file
file_name = "data/230619_MSME-DWH-Data.xlsx"
xls = pd.ExcelFile(file_name)

### Define heatmap function
def get_heatmaps(sheet_name, ind_col_name, country_col_name, year_col_name):

    xls = pd.ExcelFile(file_name)
    df = pd.read_excel(xls, sheet_name)

    # Get unique indicator list
    ind_list = df[ind_col_name].unique()

    for ind in ind_list:

        ############## Create dataframe ##############

        idx = df[country_col_name].unique()
        cols = range(2000, 2021)
        df_results = pd.DataFrame(np.nan, index=idx, columns=cols)

        # Retrieve data availability for one indicator
        df_test = df[df[ind_col_name] == ind]

        for index, row in df_test.iterrows():
            country = row[country_col_name]
            year = row[year_col_name] # Convert year to string to match column names

            # Replace available data with 1
            df_results.at[country, year] = 1

        # Replace missing data with 0 
        df_results.fillna(0, inplace=True)
        print(df_results)
        # Have countries on x-axis and years on y-axis (transpose df)
        #df_results = df_results.T

        ############## Heatmap ##############

        # Map the amount of values 
        value_to_int = {j:i for i,j in enumerate(pd.unique(df_results.values.ravel()))} 
        n = len(value_to_int) 

        # Create discrete colormap (n samples from a given cmap) using specified colours from palette
        #cmap = sns.color_palette("Pastel1", n) 
        custom_cmap = mcolors.ListedColormap([sns.color_palette("Dark2", n)[0], sns.color_palette("Dark2", n)[-1]])

        # Set the figure size to accommodate all rows and columns
        fig, ax = plt.subplots(figsize=(20, 50))  

        # Add title to the heatmap
        ax.set_title(ind, fontsize=20)

        sns.heatmap(df_results.replace(value_to_int), 
                    cmap=custom_cmap, 
                    ax=ax) 

        # Draw horizontal and vertical lines to separate data points
        for i in range(1, len(df_results.index)):
            ax.hlines(i, *ax.get_xlim(), colors='white', linewidth=1)
        for i in range(1, len(df_results.columns)):
            ax.vlines(i, *ax.get_ylim(), colors='white', linewidth=1)
        
        # Modify colorbar:
        colorbar = ax.collections[0].colorbar 
        r = colorbar.vmax - colorbar.vmin 
        colorbar.set_ticks([colorbar.vmin + r / n * (0.5 + i) for i in range(n)])
        colorbar.set_ticklabels(list(value_to_int.keys()))    

        # Set axis labels
        #ax.set_yticklabels(df_results.columns)
        #ax.set_xticklabels(df_results.index)

        # Reduce the font size of y-axis labels
        ax.yaxis.set_tick_params(labelsize=12)
        ax.xaxis.set_tick_params(labelsize=12)

        # Rotate the x-labels
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)  # Rotate x-axis labels by 45 degrees  

        # Save plot
        plt.savefig(f"graphics/test/{sheet_name}_{ind}.jpg", format='jpg')

        # Show plot
        #plt.show()


# Get the heatmaps 
for key, value in sheet_featureMap.items():
    sheet_input = key 
    ind_col_input = value[0] 
    country_col_input = value[1]
    year_col_input = value[2]

    get_heatmaps(sheet_input, ind_col_input, country_col_input, year_col_input)
