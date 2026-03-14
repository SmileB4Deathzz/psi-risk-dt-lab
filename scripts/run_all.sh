#!/bin/bash

# Creazione cartelle per i risultati
mkdir -p ../results/logs
mkdir -p ../results/figures

# Build & Start Container
echo "--Build e avvio dei container Docker..."

# Pull images first so they're available before 'up' runs
echo "--Pulling Docker images (first boot may take a while)..."
docker compose -f ../docker/docker-compose.yml pull

docker compose -f ../docker/docker-compose.yml up -d --build

# Wait for Kafka to be ready (with timeout)
echo "--Waiting for Kafka..."

MAX_WAIT=120   # seconds
ELAPSED=0

until [ "$(docker inspect -f '{{.State.Health.Status}}' kafka_broker 2>/dev/null)" = "healthy" ]; do
  if [ "$ELAPSED" -ge "$MAX_WAIT" ]; then
    echo "ERROR: Kafka did not become healthy within ${MAX_WAIT}s. Check logs:"
    echo "  docker logs kafka_broker"
    exit 1
  fi
  echo "Kafka not ready yet... (${ELAPSED}s)"
  sleep 3
  ELAPSED=$((ELAPSED + 3))
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
