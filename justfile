venv:
    python -m venv .venv

i:
    chmod +x .venv/bin/activate
    .venv/bin/activate
    .venv/bin/pip install -U pip pyyaml requests
    .venv/bin/python3 scripts/depcollect.py

pull-all:
    git submodule update
    git submodule foreach --recursive git pull origin main