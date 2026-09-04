#!/bin/sh
set -eu

if test "$#" -ne 4; then
  echo "usage: $0 CADICAL_INCLUDE LIBCADICAL_A LABELG COMPLG" >&2
  exit 2
fi

artifact_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT HUP INT TERM

"${CXX:-c++}" -std=c++17 -O3 -Wall -Wextra -Wpedantic -I"$1" \
  "$artifact_dir/enumerate_four_flip_sat.cpp" "$2" -pthread \
  -o "$tmp_dir/enumerate"

for worker in 0 1 2 3 4 5 6 7; do
  (
    start=$((worker * 328 / 8))
    end=$(((worker + 1) * 328 / 8))
    count=$((end - start))
    "$tmp_dir/enumerate" "$artifact_dir/r55_42some.g6" "$start" "$count" \
      > "$tmp_dir/$worker.tsv" 2> "$tmp_dir/$worker.log"
    : > "$tmp_dir/$worker.ok"
  ) &
done
wait
test "$(find "$tmp_dir" -name '*.ok' -type f | wc -l)" -eq 8

cat "$tmp_dir/0.tsv" "$tmp_dir/1.tsv" "$tmp_dir/2.tsv" \
  "$tmp_dir/3.tsv" "$tmp_dir/4.tsv" "$tmp_dir/5.tsv" \
  "$tmp_dir/6.tsv" "$tmp_dir/7.tsv" > "$tmp_dir/variants.unsorted.tsv"
LC_ALL=C sort -t '	' -k1,1n -k2,2 -k3,3 -k4,4 -k5,5 \
  "$tmp_dir/variants.unsorted.tsv" > "$tmp_dir/variants.tsv"
for worker in 0 1 2 3 4 5 6 7; do
  grep '^parent=' "$tmp_dir/$worker.log"
done > "$tmp_dir/parent_counts.txt"
cmp "$tmp_dir/parent_counts.txt" "$artifact_dir/EXPECTED_PARENT_COUNTS.txt"
python3 "$artifact_dir/check_lower_counts.py" "$tmp_dir/parent_counts.txt" \
  "$artifact_dir/../ramsey_r55_catalog_edge_radius2_classification/EDGE_RADIUS2_MAP.tsv" \
  "$artifact_dir/../ramsey_r55_catalog_edge_radius3_classification/EDGE_RADIUS3_MAP.tsv"

cut -f6 "$tmp_dir/variants.tsv" > "$tmp_dir/variants.g6"
"$3" -q "$tmp_dir/variants.g6" "$tmp_dir/variants.canonical.g6"
"$3" -q "$artifact_dir/r55_42some.g6" "$tmp_dir/catalog.canonical.g6"
"$4" -q "$artifact_dir/r55_42some.g6" "$tmp_dir/complements.g6"
"$3" -q "$tmp_dir/complements.g6" "$tmp_dir/complements.canonical.g6"
python3 "$artifact_dir/classify_radius4.py" "$tmp_dir/variants.tsv" \
  "$tmp_dir/variants.canonical.g6" "$tmp_dir/catalog.canonical.g6" \
  "$tmp_dir/complements.canonical.g6" > "$tmp_dir/map.tsv"
cmp "$tmp_dir/map.tsv" "$artifact_dir/EDGE_RADIUS4_MAP.tsv"
python3 "$artifact_dir/validate_variants.py" "$artifact_dir/r55_42some.g6" \
  "$tmp_dir/map.tsv"
tail -n 1 "$tmp_dir/map.tsv"
