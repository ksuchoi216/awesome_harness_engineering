#!/bin/bash
docker run --rm -v $(pwd):/app -w /app python:3.11-slim bash -c "
  pip install pytest pytest-mock faker requests-mock
  pytest tests/test_ahe_antigravity_ship.py -x -v
"
