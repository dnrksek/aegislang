#!/usr/bin/env bash
set -euo pipefail

python -m pytest
python -m aegis check examples/hello.aegis
python -m aegis run examples/hello.aegis
