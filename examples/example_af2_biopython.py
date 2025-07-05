#!/usr/bin/env python3
"""
Example usage of AF2 pipeline with BioPython (no PyRosetta)
This demonstrates the new SimpleStructure-based workflow
"""

import sys
import os
from pathlib import Path

# Add AF2 modules to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'af2_initial_guess'))

def main():
    """Example of using AF2 prediction with PDB files instead of silent files"""
    
    print("🧬 AF2 Prediction with BioPython Example")
    print("=" * 50)
    
    # Test data directory
    pdb_dir = Path(__file__).parent / "inputs" / "pdbs"
    
    if not pdb_dir.exists():
        print(f"❌ Test data directory not found: {pdb_dir}")
        print("Please ensure examples/inputs/pdbs/ exists with test PDB files")
        return 1
    
    pdb_files = list(pdb_dir.glob("*.pdb"))
    if not pdb_files:
        print(f"❌ No PDB files found in: {pdb_dir}")
        return 1
    
    print(f"📁 Found {len(pdb_files)} PDB files in {pdb_dir}")
    
    # Test SimpleStructure loading
    try:
        from simple_structure import SimpleStructure
        print("✅ SimpleStructure imported successfully")
        
        # Load a test structure
        test_pdb = pdb_files[0]
        print(f"🧪 Testing with: {test_pdb.name}")
        
        structure = SimpleStructure(str(test_pdb))
        print(f"✅ Structure loaded successfully")
        print(f"   Sequence: {structure.sequence()[:50]}...")
        print(f"   Residues: {structure.size()}")
        print(f"   Atoms: {len(structure.atoms)}")
        
        # Test AF2 atom extraction
        positions, masks = structure.get_atoms_for_af2()
        print(f"✅ AF2 atoms extracted")
        print(f"   Positions shape: {positions.shape}")
        print(f"   Masks shape: {masks.shape}")
        
        # Test chain splitting
        chains = structure.split_by_chain()
        print(f"✅ Chain analysis complete")
        print(f"   Number of chains: {len(chains)}")
        for i, chain in enumerate(chains):
            print(f"   Chain {i+1}: {chain.size()} residues")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install BioPython: pip install biopython")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    print("\n🚀 Running AF2 prediction with PDB directory...")
    print("Command that would be used:")
    print(f"python af2_initial_guess/predict.py -pdbdir {pdb_dir} -outpdbdir outputs_biopython")
    
    print("\n✅ Example completed successfully!")
    print("\nNext steps:")
    print("1. Install BioPython if not already installed: pip install biopython")
    print("2. Run AF2 prediction with PDB directory instead of silent files")
    print("3. The pipeline now works without PyRosetta for PDB inputs")
    
    return 0

if __name__ == "__main__":
    exit(main())