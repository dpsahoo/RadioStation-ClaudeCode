#!/usr/bin/env python3
"""
Radio Sahoo Docker Configuration Validator
Validates Docker configuration files for common issues.
"""

import os
import sys
from pathlib import Path

def validate_dockerfile():
    """Validate Dockerfile exists and has required elements."""
    dockerfile_path = Path("Dockerfile")
    if not dockerfile_path.exists():
        return False, "Dockerfile not found"
    
    content = dockerfile_path.read_text()
    required_elements = [
        "FROM python:",
        "WORKDIR /app",
        "COPY requirements.txt",
        "RUN pip install",
        "EXPOSE 5000",
        "ENTRYPOINT"
    ]
    
    missing = [elem for elem in required_elements if elem not in content]
    if missing:
        return False, f"Missing elements in Dockerfile: {missing}"
    
    return True, "Dockerfile validation passed"

def validate_docker_compose():
    """Validate docker-compose.yml configuration."""
    compose_path = Path("docker-compose.yml")
    if not compose_path.exists():
        return False, "docker-compose.yml not found"
    
    content = compose_path.read_text()
    
    # Check required sections
    required_elements = [
        "services:",
        "radio-sahoo:",
        "build:",
        "ports:",
        "- \"5000:5000\"",
        "environment:",
        "volumes:"
    ]
    
    missing = [elem for elem in required_elements if elem not in content]
    if missing:
        return False, f"Missing elements in docker-compose.yml: {missing}"
    
    return True, "docker-compose.yml validation passed"

def validate_prod_compose():
    """Validate docker-compose.prod.yml configuration."""
    prod_path = Path("docker-compose.prod.yml")
    if not prod_path.exists():
        return False, "docker-compose.prod.yml not found"
    
    content = prod_path.read_text()
    
    # Check production-specific configurations
    required_elements = [
        "FLASK_ENV=production",
        "security_opt:",
        "read_only: true",
        "deploy:",
        "resources:"
    ]
    
    missing = [elem for elem in required_elements if elem not in content]
    if missing:
        return False, f"Missing production elements: {missing}"
    
    return True, "docker-compose.prod.yml validation passed"

def validate_dockerignore():
    """Validate .dockerignore file."""
    dockerignore_path = Path(".dockerignore")
    if not dockerignore_path.exists():
        return False, ".dockerignore not found"
    
    content = dockerignore_path.read_text()
    important_ignores = [".git", "__pycache__", "*.pyc", ".env", "node_modules"]
    
    missing = [ignore for ignore in important_ignores if ignore not in content]
    if missing:
        return False, f"Important ignores missing: {missing}"
    
    return True, ".dockerignore validation passed"

def validate_env_example():
    """Validate .env.example file."""
    env_path = Path(".env.example")
    if not env_path.exists():
        return False, ".env.example not found"
    
    content = env_path.read_text()
    required_vars = ["SECRET_KEY", "DATABASE_PATH", "STREAM_URL", "FLASK_ENV"]
    
    missing = [var for var in required_vars if var not in content]
    if missing:
        return False, f"Missing environment variables: {missing}"
    
    return True, ".env.example validation passed"

def main():
    """Run all validations."""
    print("🐳 Radio Sahoo Docker Configuration Validator")
    print("=" * 50)
    
    validators = [
        ("Dockerfile", validate_dockerfile),
        ("docker-compose.yml", validate_docker_compose), 
        ("docker-compose.prod.yml", validate_prod_compose),
        (".dockerignore", validate_dockerignore),
        (".env.example", validate_env_example)
    ]
    
    all_passed = True
    
    for name, validator in validators:
        try:
            passed, message = validator()
            status = "✅" if passed else "❌"
            print(f"{status} {name}: {message}")
            if not passed:
                all_passed = False
        except Exception as e:
            print(f"❌ {name}: Validation error - {e}")
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("🎉 All Docker configuration files are valid!")
        print("\n📋 Next steps:")
        print("   1. Install Docker and Docker Compose")
        print("   2. Copy .env.example to .env and configure")
        print("   3. Run: docker-compose up --build")
        return 0
    else:
        print("❌ Some configuration files have issues. Please fix them before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())