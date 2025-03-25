#!/bin/bash

# Stop on errors, print commands
# See https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/
set -Eeuo pipefail
set -x

python3 -m venv venv
source venv/bin/activate
# pip install -r requirements.txt