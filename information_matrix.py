import numpy as np
import pandas as pd

# reads quantum efficiency vector from data sheet
def read_qe(wavelength_range):
    q_df = pd.read_csv("quantum-efficiency-data/qe-sampled-points-interpolated.csv")
    lambda_min, lambda_max = wavelength_range
    q_temp = q_df.loc[ (lambda_min <= q_df["Wavelength"]) & (q_df["Wavelength"] < lambda_max) , "Quantum Efficiency"]
    qe = pd.Series(
        q_temp.to_list(),
        index=range(*wavelength_range)
    )
    return qe

# reformats quantum efficiency data into a vector where the value at each index i is the quantum efficiency at illumination i
def form_q_vec(illumination_df, qe):
    q_vec = qe[(illumination_df.bin_wavelength_min + illumination_df.bin_wavelength_max)//2]
    q_vec = np.array(q_vec.array)
    return q_vec

"""Computes Fisher information matrix of model, where
        A is the imaging matrix, which determines the mean number of photons that each pixel recieves
        x_vec is the vector of fluorophore concentrations
        q_vec is a series with quantum efficiencies at each illumination in A
    
    Uses the matrix formula to avoid for loops
"""
def FIM(A, x_vec, q_vec, variance):
    y_vec = A @ x_vec
    variance_vec = y_vec + variance
    inverse_variance_vec = 1/variance_vec
    diag_vec = q_vec*q_vec * inverse_variance_vec * (1 + inverse_variance_vec/2)
    F = (A.T * diag_vec) @ A
    return F
