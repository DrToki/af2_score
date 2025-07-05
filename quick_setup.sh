#!/bin/bash

# Quick setup script for PyRosetta-free AF2 binder design
# This script sets up the conda environment without downloading large model weights

set -e  # Exit on any error

echo "🚀 Quick Setup: PyRosetta-Free AF2 Binder Design"
echo "================================================"

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "❌ Error: conda not found. Please install Miniconda or Anaconda first."
    echo "   Download from: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

echo "✅ Conda found: $(conda --version)"

# Ask user which installation they want
echo ""
echo "Select installation type:"
echo "1) Minimal (PDB files only, no PyRosetta) - Recommended"
echo "2) Full (PDB + Silent files, requires PyRosetta license)"
echo ""
read -p "Enter choice (1 or 2): " choice

case $choice in
    1)
        echo "📦 Setting up minimal environment..."
        ENV_FILE="include/af2_binder_minimal.yml"
        ENV_NAME="af2_binder_minimal"
        ;;
    2)
        echo "📦 Setting up full environment with PyRosetta..."
        echo "⚠️  Note: You must have PyRosetta credentials configured in ~/.condarc"
        ENV_FILE="include/af2_binder_full.yml"
        ENV_NAME="af2_binder_full"
        ;;
    *)
        echo "❌ Invalid choice. Exiting."
        exit 1
        ;;
esac

# Check if environment file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Error: Environment file $ENV_FILE not found"
    exit 1
fi

# Remove existing environment if it exists
if conda env list | grep -q "^$ENV_NAME "; then
    echo "🧹 Removing existing environment: $ENV_NAME"
    conda env remove -n $ENV_NAME -y
fi

# Create new environment
echo "🔨 Creating conda environment: $ENV_NAME"
conda env create -f $ENV_FILE

echo "✅ Environment created successfully!"

# Clone ProteinMPNN if needed
if [ ! -d "mpnn_fr/ProteinMPNN" ]; then
    echo "📥 Cloning ProteinMPNN..."
    cd mpnn_fr
    git clone https://github.com/dauparas/ProteinMPNN.git
    cd ..
    echo "✅ ProteinMPNN cloned"
else
    echo "✅ ProteinMPNN already available"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate environment: conda activate $ENV_NAME"
echo "2. Download AF2 weights (see INSTALLATION_GUIDE.md)"
echo "3. Test installation: python test_migration.py"
echo ""
echo "Usage examples:"
if [ "$choice" = "1" ]; then
    echo "  # PDB file prediction (no PyRosetta needed)"
    echo "  python af2_initial_guess/predict.py -pdbdir /path/to/pdbs/"
else
    echo "  # PDB file prediction"
    echo "  python af2_initial_guess/predict.py -pdbdir /path/to/pdbs/"
    echo "  # Silent file prediction"
    echo "  python af2_initial_guess/predict.py -silent input.silent"
fi
echo ""
echo "📖 See INSTALLATION_GUIDE.md for detailed instructions"