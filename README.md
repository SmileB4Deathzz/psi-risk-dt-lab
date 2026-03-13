# PSI Risk Digital Twin Lab

A minimalistic digital twin lab for risk signal and drift detection using entropy metrics and Kafka streaming.

## Structure
- `src/` — Core Python modules for digital twin, entropy, drift, and risk signal
- `scripts/` — Utility scripts for dataset generation and orchestration
- `data/` — Baseline and drift datasets
- `notebooks/` — Experiments and analysis
- `docker/` — Docker Compose and Dockerfile for environment setup
- `results/` — Output logs and figures

## Quick Start
1. Build and start containers:
   ```bash
   ./scripts/run_all.sh
   ```
2. Run experiments in Jupyter notebooks or via the pipeline.

## Requirements
- Docker
- Python 3.8+
- Kafka

## Main Features
- Sliding window analysis of sensor data
- Entropy-based drift and risk detection
- Kafka streaming integration

