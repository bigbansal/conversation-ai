#!/bin/bash

# Load environment variables
if [ -z "$ENV" ]; then
    echo "Environment variable ENV is not set. Defaulting to 'dev'."
    ENV=dev
fi

# Source the appropriate .env file based on the environment
source env/.env.$ENV
ollama run $MODEL_NAME

# Function to download and install Ollama based on OS
#download_ollama() {
#    OS_NAME=$1
#    if [ "$OS_NAME" == "linux" ]; then
#        wget https://ollama.com/download/ollama-linux-amd64.tgz -O ollama.tgz
#        tar -xzf ollama.tgz
        #ls -lrt
        #sudo mv Ollama /usr/local/bin/
#    elif [ "$OS_NAME" == "macos" ]; then
#        wget https://ollama.com/download/Ollama-darwin.zip -O ollama.zip
#        unzip ollama.zip
#        #ls -lrt
        #sudo mv Ollama /usr/local/bin/
#    else
#        echo "Unsupported OS: $OS_NAME"
#        exit 1
#    fi
#}

# Check if Ollama is already installed
#if command -v ollama &> /dev/null; then
#    echo "Ollama is already installed. Skipping installation."
#else
    # Download and install Ollama
#    echo "Downloading and installing Ollama for $OS_NAME..."
#    download_ollama $OS_NAME
#    echo "Ollama installation complete."
#fi

# Download and install Ollama
#echo "Downloading and installing Ollama for $OS_NAME..."
#download_ollama $OS_NAME
#echo "Ollama installation complete."

# Run Ollama serve
#echo "Starting Ollama serve..."
#ollama serve &
#sleep 5  # Wait for the server to start

# Verify installation and server
#if ollama run $MODEL_NAME --help &> /dev/null; then
#    echo "Ollama $MODEL_NAME installed and server started successfully."
#else
#    echo "Ollama $MODEL_NAME installation or server startup failed."
#    exit 1
#fi