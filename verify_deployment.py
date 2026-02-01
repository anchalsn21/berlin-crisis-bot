#!/usr/bin/env python3
"""
Pre-deployment verification script for Render
Checks if everything is configured correctly before deploying
"""

import os
import sys
from pathlib import Path

def print_status(check_name, passed, message=""):
    """Print colored status message"""
    if passed:
        print(f"✅ {check_name}")
    else:
        print(f"❌ {check_name}")
        if message:
            print(f"   → {message}")
    return passed

def check_file_exists(filepath, description):
    """Check if a file exists"""
    exists = Path(filepath).exists()
    return print_status(
        description,
        exists,
        f"Missing: {filepath}" if not exists else ""
    )

def check_docker_file(dockerfile_path, required_strings):
    """Check if Dockerfile contains required configurations"""
    if not Path(dockerfile_path).exists():
        return print_status(f"Check {dockerfile_path}", False, "File not found")
    
    content = Path(dockerfile_path).read_text()
    all_found = True
    missing = []
    
    for required in required_strings:
        if required not in content:
            all_found = False
            missing.append(required)
    
    return print_status(
        f"Check {dockerfile_path} configuration",
        all_found,
        f"Missing: {', '.join(missing)}" if missing else ""
    )

def check_model_exists():
    """Check if trained model exists"""
    model_dir = Path("rasa-backend/models")
    if not model_dir.exists():
        return print_status("Model directory exists", False, "models/ directory not found")
    
    model_files = list(model_dir.glob("*.tar.gz"))
    return print_status(
        "Trained model exists",
        len(model_files) > 0,
        "No .tar.gz model found in models/ directory. Run 'rasa train' first." if len(model_files) == 0 else ""
    )

def check_render_yaml():
    """Check render.yaml configuration"""
    render_file = Path("render.yaml")
    if not render_file.exists():
        return print_status("render.yaml exists", False, "render.yaml not found")
    
    content = render_file.read_text()
    checks = {
        "runtime: docker": "runtime: docker",
        "dockerContext": "dockerContext:",
        "rasa-actions service": "name: rasa-actions",
        "rasa-server service": "name: rasa-server",
    }
    
    all_passed = True
    for check_name, check_string in checks.items():
        if check_string not in content:
            print_status(f"render.yaml contains {check_name}", False)
            all_passed = False
        else:
            print_status(f"render.yaml contains {check_name}", True)
    
    return all_passed

def main():
    print("🔍 Pre-deployment Verification for Render\n")
    print("=" * 60)
    
    # Change to project root
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    all_checks_passed = True
    
    print("\n📁 File Structure Checks:")
    all_checks_passed &= check_file_exists("rasa-backend/Dockerfile.rasa", "Dockerfile.rasa exists")
    all_checks_passed &= check_file_exists("rasa-backend/Dockerfile.actions", "Dockerfile.actions exists")
    all_checks_passed &= check_file_exists("rasa-backend/requirements.txt", "requirements.txt exists")
    all_checks_passed &= check_file_exists("rasa-backend/domain.yml", "domain.yml exists")
    all_checks_passed &= check_file_exists("rasa-backend/config.yml", "config.yml exists")
    all_checks_passed &= check_file_exists("rasa-backend/endpoints.yml", "endpoints.yml exists")
    all_checks_passed &= check_file_exists("render.yaml", "render.yaml exists")
    
    print("\n🤖 Model Checks:")
    all_checks_passed &= check_model_exists()
    
    print("\n🐳 Dockerfile Configuration:")
    all_checks_passed &= check_docker_file(
        "rasa-backend/Dockerfile.rasa",
        ["FROM python:3.8", "COPY . .", "rasa run"]
    )
    all_checks_passed &= check_docker_file(
        "rasa-backend/Dockerfile.actions",
        ["FROM python:3.8", "COPY . .", "rasa run actions"]
    )
    
    print("\n⚙️  Render Configuration:")
    all_checks_passed &= check_render_yaml()
    
    print("\n" + "=" * 60)
    
    if all_checks_passed:
        print("\n✅ All checks passed! Ready to deploy to Render.")
        print("\n📚 Next steps:")
        print("   1. Commit and push your changes to GitHub")
        print("   2. Follow the steps in RENDER_DEPLOYMENT.md")
        print("   3. Create web services in Render dashboard")
        print("\n💡 Tip: Check RENDER_TROUBLESHOOTING.md if you encounter issues")
        return 0
    else:
        print("\n❌ Some checks failed. Please fix the issues above before deploying.")
        print("\n📚 For help, check:")
        print("   - RENDER_DEPLOYMENT.md for deployment instructions")
        print("   - RENDER_TROUBLESHOOTING.md for common issues")
        return 1

if __name__ == "__main__":
    sys.exit(main())
