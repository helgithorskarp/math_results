#!/bin/sh
set -eu
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python3 "$HERE/verify.py" --check-expected
python3 -m unittest discover -s "$HERE" -p 'test_*.py' -v
(cd "$HERE" && sha256sum -c SHA256SUMS)
