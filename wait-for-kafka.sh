#!/bin/bash
set -e

host="$1"
shift
cmd="$@"

echo "Waiting for Kafka at $host:9092..."
until nc -z "$host" 9092; do
  echo "Kafka not ready yet. Sleeping 2 seconds..."
  sleep 2
done

echo "Kafka is up! Starting service..."
exec $cmd