import numpy as np
import pandas as pd
import os

os.makedirs('data', exist_ok=True)

N_SAMPLES = 5000
STEPS = np.linspace(0, 100, N_SAMPLES)

print("Generazione dei dataset simulati...")

def gen_baseline():
    """Generates a stable sinusoidal signal (e.g., a vibration sensor at steady state)."""

    signal = np.sin(2 * np.pi * 0.5 * STEPS)
    noise = np.random.normal(0, 0.2, N_SAMPLES)
    
    return signal + noise

def gen_drift():
    """Generates a signal that undergoes a drift (anomaly/fault) at the midpoint of the time."""
    # First half: normal signal
    signal_normal = np.sin(2 * np.pi * 0.5 * STEPS[:2500])
    noise_normal = np.random.normal(0, 0.2, 2500)
    
    # Second half: anomalous signal with increased noise
    signal_anomalous = np.sin(2 * np.pi * 0.5 * STEPS[2500:])
    noise_anomalous = np.random.normal(0, 1.5, 2500)
    
    half_1 = signal_normal + noise_normal
    half_2 = signal_anomalous + noise_anomalous
    
    return np.concatenate([half_1, half_2])

df_baseline = pd.DataFrame({
    'timestamp': pd.date_range(start='2024-01-01', periods=N_SAMPLES, freq='s'),
    'sensor_value': gen_baseline()
})

df_drift = pd.DataFrame({
    'timestamp': pd.date_range(start='2024-01-01', periods=N_SAMPLES, freq='s'),
    'sensor_value': gen_drift()
})

df_baseline.to_csv('data/baseline_dataset.csv', index=False)
df_drift.to_csv('data/drift_dataset.csv', index=False)

print("Dataset generati in data/baseline_dataset.csv e data/drift_dataset.csv")
