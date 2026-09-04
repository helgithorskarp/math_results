#!/usr/bin/env bash
set -euo pipefail

task_dir=$(cd "$(dirname "$0")" && pwd)
task_tmp=$(mktemp -d)
trap 'rm -rf -- "$task_tmp"' EXIT

cd "$task_dir"
python3 verify_bounds.py --result "$task_tmp/result.json"
cmp result.json "$task_tmp/result.json"
