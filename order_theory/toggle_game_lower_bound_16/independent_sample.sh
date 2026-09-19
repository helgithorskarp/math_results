#!/usr/bin/env bash
set -euo pipefail

work_root=${1:-/scratch/toggle_game_lower_bound_16}
source_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
catalog="$work_root/catalog/unlabelled-15.cats.xz"
sample="$work_root/order15-independent-sample.cats"

if [[ ! -f "$catalog" ]]; then
  echo "run reproduce.sh first; missing $catalog" >&2
  exit 2
fi

set -o pipefail
xz -dc "$catalog" | LC_ALL=C awk '
  NR <= 6000 ||
  (NR >= 76110001 && NR <= 76116000) ||
  NR >= 152227519
' > "$sample"

lines=$(wc -l < "$sample")
if [[ "$lines" != 18000 ]]; then
  echo "unexpected sample size: $lines" >&2
  exit 1
fi
actual_hash=$(sha256sum "$sample" | awk '{print $1}')
expected_hash=1841dfc6506adffcd5d386ac3612562deb7b4723c4db7fb5061f1b629930511c
if [[ "$actual_hash" != "$expected_hash" ]]; then
  echo "unexpected sample hash: $actual_hash" >&2
  exit 1
fi

PYTHONDONTWRITEBYTECODE=1 python3 "$source_dir/verify_small.py" 15 "$sample"
