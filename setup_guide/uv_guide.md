# Using UV Package Manager

UV is an extremely fast package installer and resolver for Python, written in Rust. This guide explains how to use UV effectively in your Python projects.

## Quick Start Guide

### Scenario 1: Starting a New Project
```powershell
# 1. Create and navigate to project directory
mkdir my_new_project
cd my_new_project

# 2. Create virtual environment
uv venv

# 3. Activate virtual environment
.\.venv\Scripts\activate

# 4. Install essential development packages
uv pip install pytest black isort mypy

# 5. Create initial requirements files
echo "pytest>=7.0.0
black
isort
mypy" > requirements-dev.in

uv pip compile requirements-dev.in -o requirements-dev.txt
```

### Scenario 2: Setting Up Django Project
```powershell
# 1. Create and activate virtual environment
uv venv
.\.venv\Scripts\activate

# 2. Install Django and create project
uv pip install "django>=4.2"
django-admin startproject mysite .

# 3. Install common Django packages
uv pip install "djangorestframework" "django-environ" "psycopg2-binary"

# 4. Create requirements files
echo "django>=4.2
djangorestframework
django-environ
psycopg2-binary" > requirements.in

echo "# Development dependencies
-r requirements.in
pytest-django
django-debug-toolbar
coverage" > requirements-dev.in

# 5. Compile requirements
uv pip compile requirements.in -o requirements.txt
uv pip compile requirements-dev.in -o requirements-dev.txt
```

### Scenario 3: Data Science Setup
```powershell
# 1. Create and activate environment
uv venv
.\.venv\Scripts\activate

# 2. Install data science packages
uv pip install "pandas[all]" numpy matplotlib scikit-learn jupyter

# 3. Create requirements with specific versions
echo "pandas[all]
numpy>=1.24.0
matplotlib
scikit-learn
jupyter" > requirements.in

uv pip compile requirements.in --upgrade -o requirements.txt
```

### Scenario 4: Migrating from pip
```powershell
# 1. Export current dependencies
pip freeze > old-requirements.txt

# 2. Create new virtual environment
uv venv
.\.venv\Scripts\activate

# 3. Install from old requirements
uv pip install -r old-requirements.txt

# 4. Generate clean requirements
uv pip freeze > requirements.txt
```

### Scenario 5: CI/CD Pipeline Setup
```powershell
# 1. Fast, clean installation
uv pip install --clear-cache --no-deps -r requirements.txt

# 2. Install test dependencies
uv pip install --no-deps -r requirements-test.txt

# 3. Verify dependencies
uv pip check

# 4. Run tests
pytest

## Installation

There are two ways to install UV:

### 1. Using pipx (Recommended for global installation)
```powershell
# Install pipx if you haven't already
python -m pip install --user pipx
python -m pipx ensurepath
# Close and reopen terminal after running ensurepath

# Install UV
python -m pipx install uv
```

### 2. Inside a Virtual Environment
```powershell
# Activate your virtual environment first
.\.venv\Scripts\activate

# Install UV
python -m pip install uv
```

## Basic Usage

### Creating and Managing Virtual Environments
```powershell
# Create a new virtual environment
uv venv

# Create with specific Python version
uv venv --python 3.11

# Activate the virtual environment
.\.venv\Scripts\activate
```

### Installing Packages
```powershell
# Install a single package
uv pip install requests

# Install from requirements.txt
uv pip install -r requirements.txt

# Install with extra features
uv pip install "pandas[excel]"

# Install in development mode
uv pip install -e .

# Install multiple packages
uv pip install pytest black isort mypy
```

### Managing Dependencies
```powershell
# Generate requirements.txt
uv pip freeze > requirements.txt

# Compile dependencies with their exact versions
uv pip compile requirements.in -o requirements.txt

# Update all packages to their latest versions
uv pip install --upgrade-all

# Show outdated packages
uv pip list --outdated
```

### Development Workflow
```powershell
# Create a requirements.in file for primary dependencies
echo "
django>=4.0
python-dotenv
pytest
black" > requirements.in

# Compile with development dependencies
uv pip compile requirements.in --upgrade -o requirements.txt

# Install compiled requirements
uv pip install -r requirements.txt
```

## Best Practices

### 1. Project Structure
```
my_project/
├── .venv/                    # Virtual environment (excluded from git)
├── src/                      # Source code
├── tests/                    # Test files
├── requirements.in           # Primary dependencies
├── requirements.txt          # Compiled dependencies (generated)
├── requirements-dev.in       # Development dependencies
└── requirements-dev.txt      # Compiled dev dependencies (generated)
```

### 2. Dependency Management
- Use `requirements.in` for primary dependencies
- Keep separate files for production and development dependencies
- Always pin versions in compiled requirements.txt
- Regularly update dependencies with `uv pip compile --upgrade`

### 3. Virtual Environment Best Practices
- Create one virtual environment per project
- Name it `.venv` (standard practice)
- Add to `.gitignore`
- Always activate before working on project

### 4. Performance Tips
- Use UV's cache to speed up installations
- Prefer installing multiple packages in one command
- Use `uv pip compile` for deterministic builds
- Consider using `--no-deps` when you know dependencies are already installed

### 5. CI/CD Integration
```powershell
# Fast CI installations
uv pip install --no-deps -r requirements.txt

# Verify dependencies
uv pip check

# Clean installations
uv pip install --clear-cache -r requirements.txt
```

## Advanced Usage

### Working with Multiple Python Versions
```powershell
# Create venv with specific Python version
uv venv --python 3.11

# Install packages for specific Python version
uv pip install --python 3.11 -r requirements.txt
```

### Cache Management
```powershell
# Clear UV's cache
uv cache clear

# Show cache info
uv cache info
```

### Security Features
```powershell
# Install with hash verification
uv pip install --require-hashes -r requirements.txt

# Generate requirements with hashes
uv pip compile --generate-hashes requirements.in
```

## Benefits of UV

1. **Speed**: UV is significantly faster than pip for installing packages
2. **Reliability**: Better dependency resolution
3. **Caching**: Efficient local package caching
4. **Reproducibility**: Precise dependency tracking
5. **Security**: Built-in hash verification
6. **Performance**: Parallel downloads and installations

## Troubleshooting

If UV is not found after installation:
1. Make sure you've restarted your terminal after installation
2. Check if the installation directory is in your PATH:
   - For pipx installations: `%USERPROFILE%\.local\bin`
   - For venv installations: `.venv\Scripts`
3. You can always use the full path to UV:
   - In virtual environment: `.\.venv\Scripts\uv.exe`
   - Global pipx installation: `%USERPROFILE%\.local\bin\uv.exe`

### Common Issues and Solutions

1. **PATH Issues**
   ```powershell
   # Add UV to PATH temporarily
   $env:PATH += ";$env:USERPROFILE\.local\bin"
   ```

2. **Permission Issues**
   - Run terminal as administrator
   - Check file permissions in installation directory

3. **Dependency Conflicts**
   ```powershell
   # Resolve with --strict mode
   uv pip install --strict package_name
   ```

4. **Cache Problems**
   ```powershell
   # Clear cache and reinstall
   uv cache clear
   uv pip install --clear-cache -r requirements.txt
   ```

## Migration and Compatibility

### Moving from pip to UV
1. **Gradual Migration**
   ```powershell
   # Export current environment
   pip freeze > old-requirements.txt
   
   # Clean up requirements (remove platform-specific packages)
   # Edit old-requirements.txt manually
   
   # Create new environment with UV
   uv venv
   .\.venv\Scripts\activate
   uv pip install -r old-requirements.txt
   ```

2. **Working with Poetry Projects**
   ```powershell
   # Convert poetry.lock to requirements.txt
   poetry export -f requirements.txt --output requirements.txt
   
   # Install with UV
   uv pip install -r requirements.txt
   ```

3. **Working with Conda Projects**
   ```powershell
   # Export conda environment
   conda list --export > conda-requirements.txt
   
   # Create filtered pip requirements
   conda list --explicit | grep -v '#' > requirements.txt
   
   # Install with UV
   uv venv
   .\.venv\Scripts\activate
   uv pip install -r requirements.txt
   ```

### Common Tools Integration

1. **VSCode Integration**
   - Set Python interpreter to UV virtual environment
   - Use UV for package installation in terminal

2. **Git Integration**
   ```powershell
   # Add to .gitignore
   echo ".venv/
   __pycache__/
   *.pyc
   .pytest_cache/" > .gitignore
   ```

3. **Pre-commit Hooks**
   ```powershell
   # Install pre-commit
   uv pip install pre-commit
   
   # Create config
   echo "repos:
   - repo: https://github.com/pre-commit/pre-commit-hooks
     rev: v4.4.0
     hooks:
       - id: trailing-whitespace
       - id: end-of-file-fixer
       - id: check-yaml
       - id: check-added-large-files" > .pre-commit-config.yaml
   ```

4. **Tox Integration**
   ```powershell
   # Install tox
   uv pip install tox
   
   # Create tox.ini
   echo "[tox]
   envlist = py39,py310,py311
   isolated_build = True
   
   [testenv]
   deps = -r requirements-test.txt
   commands = pytest {posargs:tests}" > tox.ini
   ```
