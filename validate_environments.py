#!/usr/bin/env python3
"""
Validate conda environment files for AF2 binder design
Checks that all required packages are included and versions are compatible
"""

import yaml
import sys
from pathlib import Path

def validate_environment_file(env_file_path: Path) -> dict:
    """Validate a conda environment file"""
    
    print(f"🔍 Validating: {env_file_path.name}")
    
    if not env_file_path.exists():
        return {"valid": False, "error": f"File not found: {env_file_path}"}
    
    try:
        with open(env_file_path) as f:
            env_data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return {"valid": False, "error": f"YAML parsing error: {e}"}
    
    # Required packages for AF2 pipeline
    required_conda_packages = {
        "python", "numpy", "scipy", "biopython", "pip"
    }
    
    required_pip_packages = {
        "jax", "dm-haiku", "ml-collections", "absl-py"
    }
    
    # Check structure
    if "name" not in env_data:
        return {"valid": False, "error": "Missing environment name"}
    
    if "dependencies" not in env_data:
        return {"valid": False, "error": "Missing dependencies section"}
    
    # Extract conda packages
    conda_packages = set()
    pip_packages = set()
    
    for dep in env_data["dependencies"]:
        if isinstance(dep, str):
            # Conda package
            pkg_name = dep.split("=")[0].split(">=")[0].split("<=")[0]
            conda_packages.add(pkg_name)
        elif isinstance(dep, dict) and "pip" in dep:
            # Pip packages
            for pip_dep in dep["pip"]:
                if isinstance(pip_dep, str) and not pip_dep.startswith("-"):
                    pkg_name = pip_dep.split("==")[0].split(">=")[0].split("<=")[0].split("[")[0]
                    pip_packages.add(pkg_name)
    
    # Validate required packages
    missing_conda = required_conda_packages - conda_packages
    missing_pip = required_pip_packages - pip_packages
    
    warnings = []
    errors = []
    
    if missing_conda:
        errors.append(f"Missing conda packages: {missing_conda}")
    
    if missing_pip:
        errors.append(f"Missing pip packages: {missing_pip}")
    
    # Check for TensorFlow (required by AF2)
    has_tensorflow = any("tensorflow" in pkg for pkg in conda_packages)
    if not has_tensorflow:
        errors.append("TensorFlow not found (required by AlphaFold2)")
    
    # Check for PyTorch (useful for ProteinMPNN)
    has_pytorch = any("pytorch" in pkg for pkg in conda_packages)
    if not has_pytorch:
        warnings.append("PyTorch not found (recommended for ProteinMPNN)")
    
    # Check JAX version compatibility
    jax_packages = [pkg for pkg in pip_packages if "jax" in pkg.lower()]
    if jax_packages:
        # Check if CUDA version is specified appropriately for environment type
        if "cuda12" in str(env_data).lower() and not any("cuda12" in str(dep) for dep in env_data["dependencies"] if isinstance(dep, dict)):
            warnings.append("Environment suggests CUDA 12 but JAX CUDA 12 not explicitly specified")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "conda_packages": sorted(conda_packages),
        "pip_packages": sorted(pip_packages),
        "env_name": env_data["name"]
    }

def main():
    """Validate all environment files"""
    
    print("🧪 AF2 Binder Design Environment Validation")
    print("=" * 50)
    
    include_dir = Path("include")
    
    if not include_dir.exists():
        print("❌ Include directory not found. Run from repository root.")
        return 1
    
    # Environment files to check
    env_files = [
        "af2_binder_minimal.yml",
        "af2_binder_minimal_cuda11.yml", 
        "af2_binder_minimal_cpu.yml",
        "af2_binder_full.yml"
    ]
    
    all_valid = True
    
    for env_file in env_files:
        env_path = include_dir / env_file
        result = validate_environment_file(env_path)
        
        if result["valid"]:
            print(f"✅ {env_file}")
            print(f"   Environment: {result['env_name']}")
            print(f"   Conda packages: {len(result['conda_packages'])}")
            print(f"   Pip packages: {len(result['pip_packages'])}")
            
            if result["warnings"]:
                print(f"   ⚠️  Warnings:")
                for warning in result["warnings"]:
                    print(f"      - {warning}")
        else:
            print(f"❌ {env_file}")
            if "error" in result:
                print(f"   Error: {result['error']}")
            if "errors" in result:
                for error in result["errors"]:
                    print(f"   Error: {error}")
            all_valid = False
        
        print()
    
    # Summary
    if all_valid:
        print("🎉 All environment files are valid!")
        print("\nRecommended installation order:")
        print("1. af2_binder_minimal.yml (CUDA 12, most users)")
        print("2. af2_binder_minimal_cuda11.yml (older GPUs)")
        print("3. af2_binder_minimal_cpu.yml (no GPU)")
        print("4. af2_binder_full.yml (with PyRosetta)")
        return 0
    else:
        print("❌ Some environment files have issues. Please fix before proceeding.")
        return 1

if __name__ == "__main__":
    exit(main())