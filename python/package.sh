#!/usr/bin/env bash
set -euo pipefail
pip install -e .
pytest -q
zip -r alamode_python.zip alamode tests examples setup.py pytest.ini requirements.txt -i '*.py'
