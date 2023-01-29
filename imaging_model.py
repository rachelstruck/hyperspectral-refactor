# functions for computing entries of imaging matrix (matrix A) and the matrix itself
# organizes data for illumination i into the rows of a dataframe
# depends on Fluorophore object in data_objects.py, even though data_objects is not imported

import numpy as np
import pandas as pd

""" Return a DataFrame where row i contains data to calculate matrix entry A_ij
"""
def form_illumination_df(
        illumination_data,        # dataframe with columns:
                                     # "wavelength" for wavelength of illumination
                                     # "k" for the value (photon flux)*(volume of voxel)
        bin_wavelength_range,     # pair with first and last detected wavelengths
        bin_width                 # width of each bin
    ):
    illumination_df = pd.DataFrame(
        {
            "illumination_wavelength" : [],
            "bin_wavelength_min"      : [],
            "bin_wavelength_max"      : [],
            "k"                       : []
        }
    )
    bins_list = range(*bin_wavelength_range, bin_width)
    counter = 0
    for illumination_index in illumination_data.index:
        illumination_wavelength = illumination_data.wavelength[illumination_index]
        k                       = illumination_data.k[illumination_index]
        for bin_wavelength_min in bins_list:
            bin_wavelength_max = bin_wavelength_min + bin_width

            illumination_df.loc[counter] = {
                "illumination_wavelength" : illumination_wavelength,
                "bin_wavelength_min"      : bin_wavelength_min,
                "bin_wavelength_max"      : bin_wavelength_max,
                "k"                       : k
            }
            counter += 1
    
    return illumination_df

def calc_emission_area(fluorophore, lambda_min, lambda_max):
    area = np.trapz(fluorophore.spectra.emission.loc[lambda_min:lambda_max-1])
    return area

def calc_A_entry(illumination_df_row, fluorophore):
    k = illumination_df_row.k
    b = fluorophore.brightness
    excitation = fluorophore.spectra.excitation[illumination_df_row.illumination_wavelength]
    emission = calc_emission_area(
        fluorophore,
        illumination_df_row.bin_wavelength_min,
        illumination_df_row.bin_wavelength_max
    )

    return k*b*excitation*emission

def form_A(illumination_df, fluorophore_list):
    n = len(illumination_df.index)
    m = len(fluorophore_list)
    A = np.zeros((n,m))
    for i in range(n):
        for j in range(m):
            A[i,j] = calc_A_entry(illumination_df.loc[i], fluorophore_list[j])
    
    return A
