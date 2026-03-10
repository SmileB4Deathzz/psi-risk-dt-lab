import numpy as np
import pandas as pd

def calc_delta_h(current_entropy, baseline_mean):
    """
    Calculates the ΔH as the absolute difference between the current entropy and the baseline mean entropy.
    """
    return np.abs(current_entropy - baseline_mean)

def detect_drift_threshold(delta_h, threshold):
    """
    Returns True if the ΔH exceeds the specified threshold, indicating a potential drift.
    """
    return delta_h > threshold

def get_rolling_entropy(data, window_size, step, entropy_func):
    """
    Simulates stream processing: calculates entropy in blocks.
    """
    results = []
    for i in range(0, len(data) - window_size, step):
        window = data[i : i + window_size]
        h_t = entropy_func(window)
        results.append(h_t)
    return np.array(results)