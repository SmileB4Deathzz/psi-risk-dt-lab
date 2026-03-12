#!/bin/bash

# Creazione cartelle per i risultati
mkdir -p ../results/logs
mkdir -p ../results/figures

# Build & Start Container
echo "--Build e avvio dei container Docker..."
docker compose -f ../docker/docker-compose.yml up -d --build

# Wait for Kafka to be ready
echo "--Attesa che Kafka sia pronto..."
KAFKA_READY=false
RETRIES=0
MAX_RETRIES=60

while [ "$KAFKA_READY" = false ] && [ $RETRIES -lt $MAX_RETRIES ]; do
  if docker exec kafka_broker /usr/bin/kafka-broker-api-versions --bootstrap-server localhost:9092 > /dev/null 2>&1; then
    KAFKA_READY=true
    echo "✅ Kafka è pronto!"
  else
    RETRIES=$((RETRIES + 1))
    echo "⏳ Tentativo $RETRIES/$MAX_RETRIES - Kafka non è ancora pronto, attesa 1 secondo..."
    sleep 1
  fi
done

if [ "$KAFKA_READY" = false ]; then
  echo "❌ Kafka non è stato avviato in tempo. Uscita."
  exit 1
fi

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
