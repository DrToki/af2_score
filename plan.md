# Simplified PyRosetta → AF2 Migration Guide

## Critical Reality Check

**The original plan is over-engineered**. Here's what actually needs to happen:

### Core Problem
- Remove PyRosetta dependency
- Keep AF2 initial guess working
- Don't break existing workflows

### Simple Solution
- Replace PyRosetta structure handling with standard Python libraries
- Keep everything else exactly the same

## Phase 1: Structure I/O Replacement (Week 1)

### Step 1.1: Replace PyRosetta Structure Parsing

**Current Problem**: PyRosetta used for PDB reading/writing
**Simple Solution**: Use BioPython

```python
# OLD (PyRosetta)
from pyrosetta import *
pose = pose_from_pdb(pdb_file)

# NEW (BioPython)
from Bio.PDB import PDBParser, PDBIO
parser = PDBParser()
structure = parser.get_structure('protein', pdb_file)
```

**File to modify**: `af2_initial_guess/predict.py`

### Step 1.2: Create Simple Structure Class

```python
# File: af2_initial_guess/simple_structure.py
from Bio.PDB import PDBParser, PDBIO
import numpy as np

class SimpleStructure:
    def __init__(self, pdb_file):
        parser = PDBParser()
        self.structure = parser.get_structure('protein', pdb_file)
        self.atoms = self._extract_atoms()
    
    def _extract_atoms(self):
        atoms = []
        for atom in self.structure.get_atoms():
            atoms.append(atom.get_coord())
        return np.array(atoms)
    
    def save(self, filename):
        io = PDBIO()
        io.set_structure(self.structure)
        io.save(filename)
```

**That's it. No complex parsers, no translation layers.**

## Phase 2: Silent File Handling (Week 2)

### Step 2.1: Keep Silent Files Optional

**Don't remove silent files** - they're used by other tools. Make them optional:

```python
# File: af2_initial_guess/predict.py
def main():
    if args.silent:
        # Use existing silent file code (keep as-is)
        structures = load_from_silent(args.silent)
    else:
        # Use new PDB directory input
        structures = load_from_pdb_dir(args.pdb_dir)
```

### Step 2.2: Add PDB Directory Support

```python
def load_from_pdb_dir(pdb_dir):
    """Load structures from PDB directory"""
    structures = []
    for pdb_file in Path(pdb_dir).glob('*.pdb'):
        structure = SimpleStructure(pdb_file)
        structures.append(structure)
    return structures
```

**No complex conversion, no performance analysis. Just add the option.**

## Phase 3: Remove PyRosetta Imports (Week 3)

### Step 3.1: Find and Replace PyRosetta Imports

**Simple search and replace**:

```bash
# Find all PyRosetta imports
grep -r "from pyrosetta" .
grep -r "import pyrosetta" .
grep -r "from rosetta" .

# Replace with BioPython equivalents
```

### Step 3.2: Update Main Scripts

**File**: `af2_initial_guess/predict.py`

```python
# Remove these lines:
# from pyrosetta import *
# from rosetta import *

# Add these lines:
from Bio.PDB import PDBParser, PDBIO
from .simple_structure import SimpleStructure
```

**File**: `mpnn_fr/dl_interface_design.py`

```python
# Remove PyRosetta FastRelax calls
# Replace with simple structure validation:

def validate_structure(structure):
    """Simple structure validation without PyRosetta"""
    # Basic clash detection
    # Basic geometry checks
    # Return True/False
    return True  # For now, just accept all structures
```

## Phase 4: Testing (Week 4)

### Step 4.1: Simple Before/After Test

```python
# File: test_migration.py
import subprocess
import sys

def test_old_vs_new():
    # Run old version
    old_result = subprocess.run([
        sys.executable, 'af2_initial_guess/predict.py',
        '--silent', 'test_data/test.silent'
    ], capture_output=True)
    
    # Run new version
    new_result = subprocess.run([
        sys.executable, 'af2_initial_guess/predict.py',
        '--pdb_dir', 'test_data/pdbs/'
    ], capture_output=True)
    
    # Compare outputs
    print("Old version output:", old_result.stdout)
    print("New version output:", new_result.stdout)
    print("Both successful:", old_result.returncode == 0 and new_result.returncode == 0)

if __name__ == "__main__":
    test_old_vs_new()
```

### Step 4.2: User Acceptance Test

```bash
# Test with real data
python af2_initial_guess/predict.py --pdb_dir /path/to/real/pdbs/
```

**If it works, you're done. If not, fix the specific error.**

## What NOT to Do

### ❌ Don't Create These Over-Engineered Components:
- "Scoring translation layers"
- "Performance benchmarking frameworks"
- "Backwards compatibility layers"
- "Migration monitoring systems"
- "Gradual rollout managers"

### ❌ Don't Worry About:
- Exact performance matching
- Score correlation analysis
- Memory usage optimization
- Complex validation frameworks

## What TO Do

### ✅ Keep It Simple:
1. Replace PyRosetta with BioPython
2. Add PDB directory input option
3. Keep silent files working
4. Test with real data
5. Deploy when it works

## Implementation Priority

### Week 1: Core Replacement
- Replace PyRosetta structure I/O
- Keep AF2 prediction unchanged

### Week 2: Input Options
- Add PDB directory input
- Keep silent file support

### Week 3: Cleanup
- Remove PyRosetta imports
- Fix any remaining issues

### Week 4: Testing
- Test with real data
- Fix bugs as they appear

## Success Criteria

**Simple metrics:**
1. ✅ Code runs without PyRosetta installed
2. ✅ AF2 predictions work the same
3. ✅ Users can provide PDB files or directories
4. ✅ No crashes on real data

