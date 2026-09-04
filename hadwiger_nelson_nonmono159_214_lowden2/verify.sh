#!/usr/bin/env bash
set -eu

artifact_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec python3 "$artifact_dir/reproduce.py" "$@"
