import numpy as np
import antropy as ant
import EntropyHub as eh
from scipy.stats import entropy as scipy_entropy

def calc_shannon(data):
    data = (data - np.mean(data)) / np.std(data) #normalize data

    bins = int(np.sqrt(len(data)))
    counts, _ = np.histogram(data, bins=bins)

    probs = counts / counts.sum()
    probs = probs[probs > 0]

    return scipy_entropy(probs)

def calc_sample_entropy(data):
    """
    Calculates the Sample Entropy of the data.
    """
    return ant.sample_entropy(data)

def calc_permutation_entropy(data, order=3, delay=1):
    """
    Calcola la Permutation Entropy
    """
    return ant.perm_entropy(data, order=order, delay=delay, normalize=True)

def compute_all_metrics(data):
    """
    Returns a dictionary with all the computed entropy metrics for the given data.
    """
    metrics = {
        'shannon': calc_shannon(data),
        'sample_en': calc_sample_entropy(data),
        'perm_en': calc_permutation_entropy(data)
    }
    return metrics
