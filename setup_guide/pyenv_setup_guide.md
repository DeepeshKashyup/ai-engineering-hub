# Pyenv Setup Guide

This guide provides a step-by-step process to set up `pyenv` for managing Python versions and virtual environments in Windows.

**Note:** `pyenv` is designed for Unix-like environments and does not natively support Windows outside of WSL. If you want to avoid using WSL, you can use [`pyenv-win`](https://github.com/pyenv-win/pyenv-win), a Windows-compatible fork of pyenv. `pyenv-win` allows you to manage Python versions directly on Windows without WSL.

## Pre-requisites
- Ensure you have Git installed on your system.
- Install Windows Subsystem for Linux (WSL) and set up a Linux distribution (e.g., Ubuntu) from the Microsoft Store.
- Install `pyenv` dependencies in WSL:
  ```bash
  sudo apt update
  sudo apt install -y build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
  libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev \
  liblzma-dev python3-openssl git
  ```

## Step 1: Install pyenv-win
- Open a PowerShell terminal as Administrator.
- Run the following command to download `pyenv-win`:
  ```powershell
    New-Item -ItemType Directory -Path "$env:USERPROFILE\.pyenv" -Force

  ```powershell
  Invoke-WebRequest -Uri "https://github.com/pyenv-win/pyenv-win/archive/refs/heads/master.zip" -OutFile "$env:USERPROFILE\.pyenv\pyenv-win.zip"
  ```
- Extract the downloaded zip file to the `C:\` drive:
  ```powershell
  Expand-Archive -Path "$env:USERPROFILE\.pyenv\pyenv-win.zip" -DestinationPath "C:\pyenv-win"
  ```
- Add `pyenv` to your system `PATH`:
  ```powershell
  [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\pyenv-win\pyenv-win-master\bin;C:\pyenv-win\pyenv-win-master\shims", [EnvironmentVariableTarget]::User)
  ```
- Restart your PowerShell terminal.
## Step 2: Verify Installation
- Run the following command to verify that `pyenv` is installed correctly:
  ```bash
  pyenv --version
  ```

## Usage
### Managing Python Versions
1. List all available Python versions:
   ```powershell
   pyenv install --list
   ```

2. Install a specific Python version:
   ```powershell
   pyenv install 3.11.5
   ```

3. Set global Python version (system-wide default):
   ```powershell
   pyenv global 3.11.5
   ```

4. Set local Python version (per-project):
   ```powershell
   # Navigate to your project directory
   cd your-project-directory
   pyenv local 3.11.5
   ```

5. View installed versions:
   ```powershell
   pyenv versions
   ```

### Project Setup
1. Create a new project:
   ```powershell
   # Create and navigate to project directory
   mkdir my-project
   cd my-project
   
   # Set project-specific Python version
   pyenv local 3.11.5
   
   # Verify Python version
   python --version
   ```

2. Create a virtual environment (Choose one option):
   
   **Option A: Standard venv**
   ```powershell
   # Create and activate virtual environment
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

   **Option B: Using uv (Faster Alternative)**
   ```powershell
   # Install uv using pipx
   python -m pip install --user pipx
   python -m pipx ensurepath
   # Close and reopen terminal after running ensurepath
   python -m pipx install uv
   
   # If you're in a virtual environment, you can also install uv directly:
   python -m pip install uv
   
   # Create virtual environment with uv
   uv venv
   uv venv
   .\.venv\Scripts\activate
   ```

3. Managing Dependencies with uv:
   ```powershell
   # Install packages (much faster than pip)
   uv pip install numpy pandas

   # Install from requirements.txt
   uv pip install -r requirements.txt

   # Generate requirements.txt
   uv pip freeze > requirements.txt

   # Install development dependencies
   uv pip install -r requirements-dev.txt
   ```

4. Using pyproject.toml (Modern Approach):
   ```toml
   # pyproject.toml
   [project]
   name = "my-project"
   version = "0.1.0"
   dependencies = [
       "numpy>=1.24.0",
       "pandas>=2.0.0"
   ]

   [project.optional-dependencies]
   dev = [
       "pytest>=7.0.0",
       "black>=23.0.0"
   ]
   ```
   ```powershell
   # Install using pyproject.toml with uv
   uv pip install -e ".[dev]"
   ```

## Best Practices
1. **Version Control**:
   - Always include `.python-version` file (created by `pyenv local`) in version control
   - Add `.venv` directory to `.gitignore`

2. **Project Organization**:
   - Use one Python version per project
   - Create a virtual environment for each project
   - Document dependencies in `requirements.txt` or `pyproject.toml`

3. **Virtual Environments**:
   - Always use virtual environments for project isolation
   - Never install packages globally
   - Use `pip freeze > requirements.txt` to capture dependencies

4. **Version Selection**:
   - Use `pyenv local` for projects instead of `pyenv global`
   - Choose Python versions based on project requirements and dependencies
   - Consider long-term support (LTS) versions for production projects

5. **Security**:
   - Keep Python versions updated for security patches
   - Regularly update packages in virtual environments
   - Review security advisories for installed packages

6. **Performance**:
   - Remove unused Python versions with `pyenv uninstall`
   - Clean up unused virtual environments
   - Consider using `pyenv which python` to verify active Python path