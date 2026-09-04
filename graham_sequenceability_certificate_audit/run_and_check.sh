#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
python3 verify.py
python3 search_false_positive.py \
  --n 6 --mode none --strategy bfs --max-nodes 10000 --primes 2
python3 audit_archived_source.py
