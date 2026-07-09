import numpy as np

HAMMING_WEIGHT_TABLE = np.array([bin(i).count('1') for i in range(256)], dtype=np.uint8)

def ham_w(input_array):
    """Compute Hamming weight using lookup table"""
    return HAMMING_WEIGHT_TABLE[input_array]