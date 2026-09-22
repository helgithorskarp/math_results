#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
diff -u EXPECTED_OUTPUT.json <(python3 verify.py)
python3 -m unittest -v test_verify.py
sha256sum -c MANIFEST.sha256
