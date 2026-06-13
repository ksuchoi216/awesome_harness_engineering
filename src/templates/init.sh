#!/bin/bash
set -e

echo "=== Harness Initialization ==="

conda_env_name=""
if [ -f environment.yml ]; then
  conda_env_name="$(sed -n 's/^name:[[:space:]]*//p' environment.yml | head -n 1)"
elif [ -f conda.yaml ]; then
  conda_env_name="$(sed -n 's/^name:[[:space:]]*//p' conda.yaml | head -n 1)"
fi
if [ -n "$conda_env_name" ]; then
  echo "=== Conda environment: $conda_env_name ==="
fi

if [ ! -f pyproject.toml ] && [ ! -f requirements.txt ] && [ ! -f setup.py ] && [ ! -f environment.yml ] && [ ! -f conda.yaml ]; then
  echo "Error: No Python manifest (pyproject.toml, requirements.txt, setup.py, environment.yml, or conda.yaml) found."
  exit 1
fi

# Ensure virtual environment exists
if [ ! -d ".venv" ]; then
  echo "=== Creating virtual environment ==="
  uv venv
fi

# Activate virtual environment
echo "=== Activating virtual environment ==="
source .venv/bin/activate

# Install dependencies
echo "=== Installing dependencies ==="
if [ -f pyproject.toml ]; then
  if grep -q "^\[project\]" pyproject.toml || grep -q "^\[build-system\]" pyproject.toml; then
    uv pip install -e .
  fi
fi
if [ -f setup.py ]; then
  uv pip install -e .
fi
if [ -f requirements.txt ]; then
  uv pip install -r requirements.txt
fi
if [ -f requirements-dev.txt ]; then
  uv pip install -r requirements-dev.txt
fi
if [ -f requirements-test.txt ]; then
  uv pip install -r requirements-test.txt
fi

echo "=== Running Python verification ==="
# Check if pytest is installed and run it, otherwise warn or skip
if python -c "import pytest" >/dev/null 2>&1; then
  python -m pytest
else
  echo "pytest not found. Skipping tests."
fi

# Compile Python source files to check for syntax errors
python -m compileall .

echo "=== Verification Complete ==="
echo ""
echo "Next steps:"
echo "1. Read feature_list.json to see current feature state"
echo "2. Pick ONE unfinished feature to work on"
echo "3. Implement only that feature"
echo "4. Re-run verification before claiming done"
