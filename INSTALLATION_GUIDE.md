# Installation Guide: PyRosetta-Free AF2 Binder Design

This guide provides step-by-step instructions for setting up the migrated binder design pipeline that works with or without PyRosetta.

## 🎯 Installation Options

### Option 1: Minimal Installation (PDB files only)
- **No PyRosetta required**
- Works with PDB file inputs
- Simpler installation process
- Recommended for most users

### Option 2: Full Installation (PDB + Silent files)
- Includes PyRosetta for silent file support
- Backwards compatible with existing workflows
- More complex installation due to PyRosetta licensing

---

## 📋 Prerequisites

### System Requirements
- **OS**: Linux or macOS (Windows not officially supported)
- **GPU**: NVIDIA GPU with CUDA support (recommended)
- **RAM**: 16GB+ recommended
- **Storage**: 10GB+ for model weights

### Software Requirements
- [Conda](https://docs.conda.io/en/latest/miniconda.html) or [Mamba](https://mamba.readthedocs.io/)
- Git

---

## 🚀 Option 1: Minimal Installation (Recommended)

### Quick Setup (Automated)
```bash
git clone https://github.com/nrbennet/dl_binder_design.git
cd dl_binder_design
chmod +x quick_setup.sh
./quick_setup.sh
```

### Manual Setup
#### Step 1: Clone Repository
```bash
git clone https://github.com/nrbennet/dl_binder_design.git
cd dl_binder_design
```

#### Step 2: Create Conda Environment

Choose the appropriate environment based on your system:

#### Option A: CUDA 12 (Recommended for modern GPUs)
```bash
conda env create -f include/af2_binder_minimal.yml
conda activate af2_binder_minimal
```

#### Option B: CUDA 11 (For older GPUs)
```bash
conda env create -f include/af2_binder_minimal_cuda11.yml
conda activate af2_binder_minimal_cuda11
```

#### Option C: CPU Only (No GPU)
```bash
conda env create -f include/af2_binder_minimal_cpu.yml
conda activate af2_binder_minimal_cpu
```

**Note**: CPU-only mode will be significantly slower for AF2 predictions.

### Step 3: Download AlphaFold2 Model Weights
```bash
cd af2_initial_guess
mkdir -p model_weights/params
cd model_weights/params

# Download AF2 model weights (required)
wget https://storage.googleapis.com/alphafold/alphafold_params_2022-12-06.tar
tar --extract --verbose --file=alphafold_params_2022-12-06.tar

# Keep only the PTM model (saves space)
mv params_model_1_ptm.npz ./
rm -f params_model_*.npz  # Remove other models if desired
mv params_model_1_ptm.npz params_model_1_ptm.npz
```

### Step 4: Install ProteinMPNN (if using sequence design)
```bash
cd ../../mpnn_fr
git clone https://github.com/dauparas/ProteinMPNN.git
```

### Step 5: Test Installation
```bash
cd ..
python test_migration.py
```

**Expected output:**
```
✅ BioPython import successful
✅ SimpleStructure class working
✅ AF2 predict script functional
```

---

## 🔧 Option 2: Full Installation (PDB + Silent Files)

### Step 1: Setup PyRosetta Access
**Important**: PyRosetta requires an academic license (free for academics).

1. **Get PyRosetta License**: Visit [PyRosetta Downloads](https://graylab.jhu.edu/pyrosetta/downloads/documentation/PyRosetta_Install_Tutorial.pdf)
2. **Register** for academic license
3. **Note your USERNAME and PASSWORD** for conda channel access

### Step 2: Configure Conda for PyRosetta
```bash
# Add PyRosetta channel to conda config
echo "channels:" > ~/.condarc
echo "  - https://USERNAME:PASSWORD@conda.graylab.jhu.edu" >> ~/.condarc
echo "  - conda-forge" >> ~/.condarc
echo "  - pytorch" >> ~/.condarc
echo "  - nvidia" >> ~/.condarc
echo "  - defaults" >> ~/.condarc

# Replace USERNAME and PASSWORD with your PyRosetta credentials
```

### Step 3: Create Full Environment
```bash
# Clone repository
git clone https://github.com/nrbennet/dl_binder_design.git
cd dl_binder_design

# Create environment with PyRosetta
conda env create -f include/af2_binder_full.yml
conda activate af2_binder_full
```

### Step 4: Download Model Weights and ProteinMPNN
```bash
# Follow steps 3-4 from Option 1
# (Download AF2 weights and install ProteinMPNN)
```

### Step 5: Test Full Installation
```bash
python test_migration.py
python include/importtests/af2_importtest.py
python include/importtests/proteinmpnn_importtest.py
```

---

## 📦 Conda Environment Files

### Environment Options

#### Minimal Environment - CUDA 12 (`include/af2_binder_minimal.yml`)
```yaml
name: af2_binder_minimal
channels:
  - conda-forge
  - pytorch
  - nvidia
  - defaults
dependencies:
  - python=3.9
  - numpy, scipy, matplotlib, pandas
  - biopython
  - pytorch, torchvision, torchaudio
  - pytorch-cuda=12.1
  - tensorflow
  - pip, wget, git
  - pip:
    - jax[cuda12_pip]==0.4.20
    - jaxlib, dm-haiku, dm-tree
    - ml-collections, ml_dtypes, chex
    - immutabledict, absl-py, tree
    - tqdm, requests
```

#### CUDA 11 Environment (`include/af2_binder_minimal_cuda11.yml`)
- Same as above but with `pytorch-cuda=11.8` and `jax[cuda11_pip]`

#### CPU-Only Environment (`include/af2_binder_minimal_cpu.yml`)  
- Same as above but with `pytorch-cpu`, `tensorflow-cpu`, and `jax[cpu]`

### Full Environment (`include/af2_binder_full.yml`)
```yaml
name: af2_binder_full
channels:
  - https://USERNAME:PASSWORD@conda.graylab.jhu.edu
  - conda-forge
  - pytorch
  - nvidia
  - defaults
dependencies:
  - python=3.9
  - numpy
  - scipy
  - matplotlib
  - biopython
  - pyrosetta
  - pytorch
  - torchvision 
  - torchaudio
  - pytorch-cuda=12.1
  - pip
  - pip:
    - jax[cuda12_pip]
    - dm-haiku
    - chex
    - ml-collections
    - immutabledict
    - absl-py
```

---

## 🧪 Testing Your Installation

### Quick Test
```bash
# Test BioPython functionality
python examples/example_af2_biopython.py

# Test AF2 prediction (requires test data)
python af2_initial_guess/predict.py -pdbdir examples/inputs/pdbs -outpdbdir test_output
```

### Comprehensive Test
```bash
# Run full test suite
python test_migration.py

# Expected results:
# ✅ BioPython Import: PASS
# ✅ SimpleStructure Class: PASS  
# ✅ AF2 Predict Help: PASS
# ✅ ProteinMPNN Help: PASS
# ✅ PDB Directory Support: PASS
```

---

## 🚀 Usage Examples

### PDB File Input (No PyRosetta needed)
```bash
# AF2 prediction from PDB directory
python af2_initial_guess/predict.py \
  -pdbdir /path/to/pdbs/ \
  -outpdbdir af2_predictions \
  -recycle 3

# ProteinMPNN design from PDB directory  
python mpnn_fr/dl_interface_design.py \
  -pdbdir /path/to/pdbs/ \
  -outpdbdir designed_sequences \
  -seqs_per_struct 4
```

### Silent File Input (PyRosetta required)
```bash
# AF2 prediction from silent file
python af2_initial_guess/predict.py \
  -silent input.silent \
  -outsilent af2_predictions.silent

# ProteinMPNN design from silent file
python mpnn_fr/dl_interface_design.py \
  -silent input.silent \
  -outsilent designed_sequences.silent
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. "No module named 'Bio'"
```bash
# Solution: Install BioPython
conda install biopython
# or
pip install biopython
```

#### 2. "No GPU found" or JAX CUDA issues
```bash
# Check CUDA installation
nvidia-smi

# Reinstall JAX with correct CUDA version
pip uninstall jax jaxlib
pip install jax[cuda12_pip]  # For CUDA 12
# or
pip install jax[cuda11_pip]  # For CUDA 11
```

#### 3. "PyRosetta not available" (for silent files)
```bash
# Check conda channel configuration
conda config --show channels

# Should include: https://USERNAME:PASSWORD@conda.graylab.jhu.edu
# If not, reconfigure with your PyRosetta credentials
```

#### 4. AF2 model weights not found
```bash
# Check weights directory
ls af2_initial_guess/model_weights/params/

# Should contain: params_model_1_ptm.npz
# If missing, re-download weights (see Step 3 above)
```

#### 5. Out of GPU memory
```bash
# Reduce batch size or use CPU
export CUDA_VISIBLE_DEVICES=""  # Force CPU usage

# Or reduce structure size/complexity
```

### Performance Optimization

#### GPU Memory Management
```bash
# For large structures, process one at a time
python af2_initial_guess/predict.py -pdbdir pdbs/ -debug
```

#### CPU Fallback
```bash
# If GPU issues, force CPU usage
export JAX_PLATFORM_NAME=cpu
python af2_initial_guess/predict.py -pdbdir pdbs/
```

---

## 📊 Installation Verification Checklist

- [ ] Conda environment created successfully
- [ ] BioPython imports without errors
- [ ] JAX detects GPU (if available)
- [ ] AF2 model weights downloaded and accessible
- [ ] ProteinMPNN repository cloned
- [ ] Test scripts run without errors
- [ ] Example predictions complete successfully

---

## 🆘 Getting Help

### Check Installation Status
```bash
# Run diagnostic script
python test_migration.py

# Check conda environment
conda list

# Check GPU availability
python -c "import jax; print(jax.devices())"
```

### Common Commands
```bash
# Reinstall environment from scratch
conda env remove -n af2_binder_minimal
conda env create -f include/af2_binder_minimal.yml

# Update packages
conda update --all

# Clear conda cache
conda clean --all
```

### Support Resources
- **GitHub Issues**: [dl_binder_design/issues](https://github.com/nrbennet/dl_binder_design/issues)
- **PyRosetta Support**: [PyRosetta Forums](https://www.pyrosetta.org/forum)
- **JAX Documentation**: [JAX Installation Guide](https://jax.readthedocs.io/en/latest/installation.html)

---

## 🎉 Success!

After completing installation, you should be able to:

1. **Process PDB files directly** without PyRosetta
2. **Run AF2 predictions** on protein structures
3. **Design sequences** with ProteinMPNN
4. **Handle both PDB and silent file formats** (with appropriate dependencies)

The system is now ready for protein binder design workflows!