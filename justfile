i:
    python3 scripts/depcollect.py

pull-all:
    git submodule update
    git submodule foreach --recursive git pull origin main