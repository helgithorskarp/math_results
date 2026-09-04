#!/usr/bin/env bash
set -euo pipefail

review_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$review_dir/.." && pwd)
python_bin=${PYTHON:-python3}
workers=${WORKERS:-6}
checkpoint_dir=${CHECKPOINT_DIR:-${TMPDIR:-/tmp}/parts509-quad-review1-checkpoints}

cd "$repo_root/hadwiger_nelson_parts509_triple_closure"
"$python_bin" two_neighbour_points.py
"$python_bin" nonk_exact.py q2k_extra.json nonk_exact.json --workers "$workers"

mkdir -p "$checkpoint_dir"
cd "$repo_root/hadwiger_nelson_parts509_quad_closure"
"$python_bin" independent_check.py certificate.json.gz 0 16 21 220 347 415 --samples 20000
"$python_bin" verify4.py certificate.json.gz --workers "$workers" --checkpoint "$checkpoint_dir"
