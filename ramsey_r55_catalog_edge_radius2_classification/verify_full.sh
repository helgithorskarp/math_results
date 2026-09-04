#!/bin/sh
set -eu

if test "$#" -ne 2; then
  echo "usage: $0 /path/to/labelg /path/to/complg" >&2
  exit 2
fi

artifact_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT HUP INT TERM

"${CXX:-c++}" -std=c++17 -O3 -Wall -Wextra -Wpedantic \
  "$artifact_dir/enumerate_two_flip_ramsey.cpp" -o "$tmp_dir/enumerate"
for id in 0 1 2 3 4 5 6 7; do
  (
    start=$((id * 328 / 8))
    end=$(((id + 1) * 328 / 8))
    count=$((end - start))
    "$tmp_dir/enumerate" "$artifact_dir/r55_42some.g6" "$start" "$count" \
      > "$tmp_dir/$id.tsv" 2> "$tmp_dir/$id.log"
    : > "$tmp_dir/$id.ok"
  ) &
done
wait
test "$(find "$tmp_dir" -name '*.ok' -type f | wc -l)" -eq 8

cat "$tmp_dir/0.tsv" "$tmp_dir/1.tsv" "$tmp_dir/2.tsv" "$tmp_dir/3.tsv" \
  "$tmp_dir/4.tsv" "$tmp_dir/5.tsv" "$tmp_dir/6.tsv" "$tmp_dir/7.tsv" \
  > "$tmp_dir/variants.tsv"
for id in 0 1 2 3 4 5 6 7; do tail -n 1 "$tmp_dir/$id.log"; done \
  > "$tmp_dir/ranges.txt"
cmp "$tmp_dir/ranges.txt" "$artifact_dir/EXPECTED_RANGES.txt"

cut -f5 "$tmp_dir/variants.tsv" > "$tmp_dir/variants.g6"
"$1" -q "$tmp_dir/variants.g6" "$tmp_dir/variants.canonical.g6"
"$1" -q "$artifact_dir/r55_42some.g6" "$tmp_dir/catalog.canonical.g6"
"$2" -q "$artifact_dir/r55_42some.g6" "$tmp_dir/complements.g6"
"$1" -q "$tmp_dir/complements.g6" "$tmp_dir/complements.canonical.g6"
python3 "$artifact_dir/classify_variants.py" "$tmp_dir/variants.tsv" \
  "$tmp_dir/variants.canonical.g6" "$tmp_dir/catalog.canonical.g6" \
  "$tmp_dir/complements.canonical.g6" > "$tmp_dir/map.tsv"
cmp "$tmp_dir/map.tsv" "$artifact_dir/EDGE_RADIUS2_MAP.tsv"
cat "$tmp_dir/ranges.txt"
tail -n 1 "$tmp_dir/map.tsv"
