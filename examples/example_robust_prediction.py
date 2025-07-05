#!/usr/bin/env python3
"""
Example demonstrating robust AF2 prediction with edge case handling
This script shows how the enhanced pipeline handles problematic PDB files
"""

import sys
import os
from pathlib import Path
import tempfile

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'af2_initial_guess'))

def create_test_pdb_with_issues(filename: str) -> str:
    """Create a test PDB with common edge case issues"""
    
    pdb_content = """HEADER    COMPLEX                                 01-JAN-21   TEST
TITLE     TEST COMPLEX WITH NUMBERING ISSUES
REMARK 350 BOTH CHAINS START FROM RESIDUE 1 (PROBLEMATIC)
ATOM      1  N   ALA A   1      20.154  16.000  10.000  1.00 20.00           N  
ATOM      2  CA  ALA A   1      21.000  16.500  10.500  1.00 20.00           C  
ATOM      3  C   ALA A   1      22.000  17.000  11.000  1.00 20.00           C  
ATOM      4  O   ALA A   1      23.000  17.500  11.500  1.00 20.00           O  
ATOM      5  CB  ALA A   1      20.500  16.200  9.800   1.00 20.00           C  
ATOM      6  N   VAL A   2      22.200  17.100  12.000  1.00 20.00           N  
ATOM      7  CA  VAL A   2      23.200  17.600  12.500  1.00 20.00           C  
ATOM      8  C   VAL A   2      24.200  18.100  13.000  1.00 20.00           C  
ATOM      9  O   VAL A   2      25.200  18.600  13.500  1.00 20.00           O  
ATOM     10  CB  VAL A   2      22.800  17.300  11.800  1.00 20.00           C  
HETATM   11  O   HOH A 100      30.000  30.000  30.000  1.00 30.00           O  
HETATM   12  O   HOH A 101      31.000  31.000  31.000  1.00 30.00           O  
TER      13      VAL A   2
ATOM     14  N   GLY B   1      10.154  16.000  10.000  1.00 20.00           N  
ATOM     15  CA  GLY B   1      11.000  16.500  10.500  1.00 20.00           C  
ATOM     16  C   GLY B   1      12.000  17.000  11.000  1.00 20.00           C  
ATOM     17  O   GLY B   1      13.000  17.500  11.500  1.00 20.00           O  
ATOM     18  N   LEU B   2      12.200  17.100  12.000  1.00 20.00           N  
ATOM     19  CA  LEU B   2      13.200  17.600  12.500  1.00 20.00           C  
ATOM     20  C   LEU B   2      14.200  18.100  13.000  1.00 20.00           C  
ATOM     21  O   LEU B   2      15.200  18.600  13.500  1.00 20.00           O  
ATOM     22  CB  LEU B   2      12.800  17.300  11.800  1.00 20.00           C  
TER      23      LEU B   2
END
"""
    
    with open(filename, 'w') as f:
        f.write(pdb_content)
    
    return filename

def demonstrate_edge_case_handling():
    """Demonstrate how the robust pipeline handles edge cases"""
    
    print("🧪 Demonstrating Robust AF2 Prediction Edge Case Handling")
    print("=" * 60)
    
    # Create test PDB with issues
    with tempfile.NamedTemporaryFile(mode='w', suffix='.pdb', delete=False) as tmp:
        test_pdb = create_test_pdb_with_issues(tmp.name)
    
    try:
        from robust_structure_handler import prepare_structure_for_af2, RobustStructureHandler
        from simple_structure import SimpleStructure
        
        print(f"📁 Created test PDB: {test_pdb}")
        print("   Issues: Both chains start from residue 1, contains water molecules")
        
        # Load with basic SimpleStructure (old way)
        print("\n🔍 Testing Basic SimpleStructure Loading...")
        try:
            basic_structure = SimpleStructure(test_pdb)
            chains = basic_structure.split_by_chain()
            print(f"✅ Basic loading successful")
            print(f"   Chains: {len(chains)}")
            print(f"   Total residues: {basic_structure.size()}")
            
            # Check for residue numbering issues
            handler = RobustStructureHandler()
            validation = handler.validate_structure(basic_structure)
            
            if not validation['valid']:
                print("❌ Validation issues found:")
                for error in validation['errors']:
                    print(f"   Error: {error}")
            
            if validation['warnings']:
                print("⚠️  Validation warnings:")
                for warning in validation['warnings']:
                    print(f"   Warning: {warning}")
                    
        except Exception as e:
            print(f"❌ Basic loading failed: {e}")
        
        # Load with robust handler (new way)
        print("\n🛡️  Testing Robust Structure Preparation...")
        try:
            robust_structure = prepare_structure_for_af2(
                pdb_file=test_pdb,
                auto_clean=True,
                auto_renumber=True
            )
            
            print("✅ Robust preparation successful!")
            
            # Validate the prepared structure
            validation_after = handler.validate_structure(robust_structure)
            if validation_after['valid']:
                print("✅ Structure is now valid for AF2 prediction")
                
                for i, chain_info in enumerate(validation_after['chain_info']):
                    chain_type = "Binder" if i == 0 else "Target"
                    print(f"   {chain_type} chain: {chain_info['length']} residues "
                          f"(residues {min(chain_info['residue_numbers'])}-{max(chain_info['residue_numbers'])})")
            else:
                print("❌ Structure still has issues after preparation")
                
        except Exception as e:
            print(f"❌ Robust preparation failed: {e}")
        
        # Demonstrate different options
        print("\n🔧 Testing Different Preparation Options...")
        
        # Option 1: Conservative (minimal processing)
        print("\n   Option 1: Conservative Processing")
        try:
            conservative = prepare_structure_for_af2(
                pdb_file=test_pdb,
                auto_clean=False,  # Don't remove waters
                auto_renumber=False  # Don't renumber
            )
            print("   ✅ Conservative processing works (issues may remain)")
        except Exception as e:
            print(f"   ❌ Conservative processing failed: {e}")
        
        # Option 2: Aggressive cleaning
        print("\n   Option 2: Aggressive Cleaning")
        try:
            aggressive = handler.clean_structure(
                SimpleStructure(test_pdb),
                remove_waters=True,
                remove_hetero=True,
                keep_only_ca=False
            )
            print("   ✅ Aggressive cleaning successful")
            print(f"   Residues after cleaning: {aggressive.size()}")
        except Exception as e:
            print(f"   ❌ Aggressive cleaning failed: {e}")
        
        # Option 3: Chain specification
        print("\n   Option 3: Manual Chain Specification")
        try:
            manual = prepare_structure_for_af2(
                pdb_file=test_pdb,
                binder_chain='A',  # Specify A as binder
                target_chain='B',  # Specify B as target
                auto_clean=True,
                auto_renumber=True
            )
            print("   ✅ Manual chain specification successful")
        except Exception as e:
            print(f"   ❌ Manual chain specification failed: {e}")
        
        print("\n🎯 Summary:")
        print("   • Robust handler automatically fixes common PDB issues")
        print("   • Residue numbering is corrected for AF2 compatibility")
        print("   • Waters and hetero atoms are removed")
        print("   • Chain order is handled automatically")
        print("   • Fallback options available for edge cases")
        
        print("\n🚀 Command Line Usage:")
        print("   # Automatic processing (recommended)")
        print(f"   python af2_initial_guess/predict.py -pdbdir {Path(test_pdb).parent}")
        print("")
        print("   # With manual chain specification")
        print(f"   python af2_initial_guess/predict.py -pdbdir {Path(test_pdb).parent} -binder_chain A -target_chain B")
        print("")
        print("   # Conservative processing")
        print(f"   python af2_initial_guess/predict.py -pdbdir {Path(test_pdb).parent} -auto_clean=False -auto_renumber=False")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure BioPython is installed: pip install biopython")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        # Clean up
        if os.path.exists(test_pdb):
            os.unlink(test_pdb)

if __name__ == "__main__":
    demonstrate_edge_case_handling()