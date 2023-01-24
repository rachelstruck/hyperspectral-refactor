# defines "Fluorophore" object to handle fluorophore data
# creates list of Fluorophore objects for use in other code

import numpy as np
import pandas as pd

# returns a normalized version of the series
def normalize(series):
    area = np.trapz(series, dx = 1)
    normalized = series/area
    return normalized

# expands the index of the series to include range(a,b)
def expand_indices(series, a, b):
    df = pd.DataFrame([series.index, series])
    for i in range(a,b):
        if i in series.index:
            pass
        else:
            series.loc[i] = None
    series.fillna(0, inplace = True)
    return

class Fluorophore:
    def __init__(self, name, filename=None, excitation_column_name=None, emission_column_name=None, needed_index_range=None):
        self.name = name

        if filename == None:
            filename = "fluorophore-spectra/" + self.name + "_fpbase_spectra.csv"
        
        self.df = pd.read_csv(filename)
        self.df.fillna(0, inplace = True)

        if excitation_column_name == None:
            excitation_column_name = self.name + " ex"
        if emission_column_name == None:
            emission_column_name = self.name + " em"
        
        self.df[excitation_column_name] = normalize(self.df[excitation_column_name])
        self.df[emission_column_name]   = normalize(self.df[emission_column_name])
        
        self.excitation = self.df[excitation_column_name]
        self.excitation.index = self.df['wavelength']

        self.emission = self.df[emission_column_name]
        self.emission.index = self.df['wavelength']