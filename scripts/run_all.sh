#!/bin/bash

# Creazione cartelle per i risultati
mkdir -p ../results/logs
mkdir -p ../results/figures

# Build & Start Container
echo "--Build e avvio dei container Docker..."
docker compose -f ../docker/docker-compose.yml up -d --build

# Wait for Kafka to be ready
echo "--Waiting for Kafka..."

until [ "$(docker inspect -f '{{.State.Health.Status}}' kafka_broker)" = "healthy" ]; do
  echo "Kafka not ready yet..."
  sleep 3
done

echo "Kafka ready!"

# Generazione dei Dataset
echo "--Generazione dei dataset (Baseline e Drift)..."
docker exec python_lab python scripts/generate_dataset.py

# Esecuzione Esperimento 1 - Entropia
echo "--Esecuzione Esperimento 1: Calcolo Baseline Entropica..."
docker exec python_lab papermill \
    notebooks/experiment_1_entropy.ipynb \
    results/logs/out_experiment_1_entropy.ipynb \
    --log-output

# Esecuzione Esperimento 2 - Drift Detection
echo "--Esecuzione Esperimento 2: Drift Detection e Segnale di Rischio..."
docker exec python_lab papermill \
    notebooks/experiment_2_drift.ipynb \
    results/logs/out_experiment_2_drift.ipynb \
    --log-output

echo "Pipeline completata con successo!"
echo "I grafici sono stati salvati in: results/figures/"
