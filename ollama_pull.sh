#!/bin/sh

echo "Starting Ollama server..."
ollama serve &

echo "Waiting for Ollama server to be active..."
while [ "$(ollama list | grep 'NAME')" == "" ]; do
  sleep 1
done

echo "Ollama server active, start to pull models..."
ollama pull adrienbrault/nous-hermes2pro-llama3-8b:q8_0
ollama pull nomic-embed-text