import numpy as np

def calc_delta_h(current_entropy, baseline_mean):
    """
    Calculates the ΔH as the absolute difference between the current entropy and the baseline mean entropy.
    """
    return np.abs(current_entropy - baseline_mean)