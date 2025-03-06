#!/bin/bash

source /home/benjamin/git/leica-disto-reader/venv/bin/activate

python /home/benjamin/git/leica-disto-reader/disto_discover.py "$@"

deactivate