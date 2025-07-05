#!/bin/bash

# Download AF2 model weights script
# This script automates the download and setup of AlphaFold2 model weights

set -e  # Exit on any error

echo "🧬 AlphaFold2 Model Weights Download Script"
echo "=========================================="

# Check if we're in the right directory
if [ ! -d "af2_initial_guess" ]; then
    echo "❌ Error: af2_initial_guess directory not found"
    echo "Please run this script from the dl_binder_design root directory"
    exit 1
fi

# Create weights directory
echo "📁 Creating model weights directory..."
mkdir -p af2_initial_guess/model_weights/params
cd af2_initial_guess/model_weights/params

# Check if weights already exist
if [ -f "params_model_1_ptm.npz" ]; then
    echo "✅ AF2 model weights already exist. Skipping download."
    echo "   Location: $(pwd)/params_model_1_ptm.npz"
    echo "   Size: $(du -h params_model_1_ptm.npz | cut -f1)"
    exit 0
fi

# Download weights
echo "⬇️  Downloading AF2 model weights (this may take several minutes)..."
echo "   Source: https://storage.googleapis.com/alphafold/alphafold_params_2022-12-06.tar"

if command -v wget &> /dev/null; then
    wget https://storage.googleapis.com/alphafold/alphafold_params_2022-12-06.tar
elif command -v curl &> /dev/null; then
    curl -O https://storage.googleapis.com/alphafold/alphafold_params_2022-12-06.tar
else
    echo "❌ Error: Neither wget nor curl found. Please install one of them."
    exit 1
fi

# Verify download
if [ ! -f "alphafold_params_2022-12-06.tar" ]; then
    echo "❌ Error: Download failed"
    exit 1
fi

echo "✅ Download complete"
echo "   Size: $(du -h alphafold_params_2022-12-06.tar | cut -f1)"

# Extract weights
echo "📦 Extracting model weights..."
tar --extract --verbose --file=alphafold_params_2022-12-06.tar

# Check extraction
if [ ! -f "params_model_1_ptm.npz" ]; then
    echo "❌ Error: Expected file params_model_1_ptm.npz not found after extraction"
    echo "Available files:"
    ls -la
    exit 1
fi

echo "✅ Extraction complete"

# Clean up - remove other models and tar file to save space
echo "🧹 Cleaning up (removing unused model files)..."
rm -f params_model_2_ptm.npz params_model_3_ptm.npz params_model_4_ptm.npz params_model_5_ptm.npz
rm -f alphafold_params_2022-12-06.tar

echo "✅ Cleanup complete"

# Final verification
echo "🔍 Final verification..."
if [ -f "params_model_1_ptm.npz" ]; then
    echo "✅ AF2 model weights successfully installed"
    echo "   Location: $(pwd)/params_model_1_ptm.npz"
    echo "   Size: $(du -h params_model_1_ptm.npz | cut -f1)"
    
    # Test if Python can read the file
    cd ../../..
    python -c "
import numpy as np
try:
    weights = np.load('af2_initial_guess/model_weights/params/params_model_1_ptm.npz')
    print(f'✅ Weights file is valid (contains {len(weights.files)} parameter arrays)')
except Exception as e:
    print(f'❌ Error reading weights file: {e}')
    exit(1)
"
    
    echo "🎉 AF2 model weights are ready for use!"
else
    echo "❌ Error: Installation verification failed"
    exit 1
fi