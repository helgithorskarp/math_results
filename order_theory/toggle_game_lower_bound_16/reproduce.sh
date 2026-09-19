#!/usr/bin/env bash
set -euo pipefail

work_root=${1:-/scratch/toggle_game_lower_bound_16}
workers=${TOGGLE_WORKERS:-4}
source_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
base_url=https://rds.westernsydney.edu.au/Schools/CDMS/VGebhardt-UnlabelledLattices-20180926

case "$workers" in
  ''|*[!0-9]*) echo "TOGGLE_WORKERS must be a positive integer" >&2; exit 2 ;;
esac
if ((workers < 1 || workers > 999)); then
  echo "TOGGLE_WORKERS must lie in 1..999" >&2
  exit 2
fi

catalog_dir="$work_root/catalog"
build_dir="$work_root/build"
mkdir -p "$work_root" "$catalog_dir" "$build_dir"
run_dir=$(mktemp -d "$work_root/run.XXXXXX")

curl -fL --retry 5 --retry-delay 2 "$base_url/unlabelled.sha256" \
  -o "$catalog_dir/unlabelled.sha256"
curl -fL --retry 5 --retry-delay 2 "$base_url/unlabelled-15.cats.xz" \
  -o "$catalog_dir/unlabelled-15.cats.xz"
(
  cd "$catalog_dir"
  sha256sum --ignore-missing -c unlabelled.sha256
)
xz -t "$catalog_dir/unlabelled-15.cats.xz"

set -o pipefail
xz -dc "$catalog_dir/unlabelled-15.cats.xz" |
  split -d -a 3 -n "r/$workers" --additional-suffix=.cats - "$run_dir/part-"

g++ -std=c++20 -O3 -DNDEBUG -Wall -Wextra -Wpedantic \
  -Wconversion -Wshadow "$source_dir/catalog_search.cpp" \
  -o "$build_dir/catalog_search"

start_epoch=$(date +%s)
pids=()
for part in "$run_dir"/part-*.cats; do
  name=$(basename "$part" .cats)
  "$build_dir/catalog_search" 15 "$part" cats \
    > "$run_dir/$name.out" 2> "$run_dir/$name.err" &
  pids+=("$!")
done
status=0
for pid in "${pids[@]}"; do
  if ! wait "$pid"; then status=1; fi
done
end_epoch=$(date +%s)
if ((status != 0)); then
  echo "at least one slice failed; inspect $run_dir" >&2
  exit 1
fi

summary=$(awk '
  {
    for (i = 1; i <= NF; ++i) {
      split($i, a, "=")
      if (a[1] == "total") total += a[2]
      if (a[1] == "winnable") wins += a[2]
      if (a[1] == "max_states_before_goal" && a[2] > max) max = a[2]
    }
  }
  END {
    printf "PASS order=15 total=%.0f winnable=%.0f max_states_before_goal=%.0f", total, wins, max
  }
' "$run_dir"/part-*.out)

expected='PASS order=15 total=152233518 winnable=152233518 max_states_before_goal=16383'
if [[ "$summary" != "$expected" ]]; then
  echo "unexpected aggregate: $summary" >&2
  exit 1
fi
printf '%s\n' "$summary"
printf 'workers=%d search_wall_seconds=%d run_dir=%s\n' \
  "$workers" "$((end_epoch - start_epoch))" "$run_dir"
