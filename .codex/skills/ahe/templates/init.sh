#!/usr/bin/env bash
set -euo pipefail

echo "AHE workspace initialization"
echo "Detected or default environment: Python"
echo

if [ -f "pyproject.toml" ]; then
  echo "Detected pyproject.toml"
fi

if [ -f "requirements.txt" ]; then
  echo "Detected requirements.txt"
  echo "Recommended install command:"
  echo "  pip install -r requirements.txt"
fi

if [ -f "uv.lock" ]; then
  echo "Detected uv.lock"
  echo "Recommended install command:"
  echo "  uv sync"
fi

if [ -f "poetry.lock" ]; then
  echo "Detected poetry.lock"
  echo "Recommended install command:"
  echo "  poetry install"
fi

if [ -f "environment.yml" ]; then
  echo "Detected environment.yml"
  echo "Recommended install command:"
  echo "  conda env update -f environment.yml"
fi

if [ -f "conda.yaml" ]; then
  echo "Detected conda.yaml"
  echo "Recommended install command:"
  echo "  conda env update -f conda.yaml"
fi

echo
echo "Recommended verification commands:"
echo "  pytest tests/ -x"
echo "  mypy src/ --strict"
echo "  ruff check src/"

if [ -f "Makefile" ]; then
  echo "  make check"
fi
