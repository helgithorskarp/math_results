#!/bin/sh
set -eu

if test "$#" -ne 2; then
  echo "usage: $0 /path/to/delptg /path/to/shortg" >&2
  exit 2
fi

artifact_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT HUP INT TERM

"$1" -q -l -n2 "$artifact_dir/r55_42some.g6" "$tmp_dir/all.g6"
"$2" -q "$tmp_dir/all.g6" "$tmp_dir/unique.g6"
test "$(wc -l < "$tmp_dir/all.g6")" -eq 282408
test "$(wc -l < "$tmp_dir/unique.g6")" -eq 173114
test "$(sha256sum "$tmp_dir/all.g6" | awk '{print $1}')" = 12a48d3fbfca4060aeabb7798c82cafc054b26100a9f263d311176fbf54991f8
test "$(sha256sum "$tmp_dir/unique.g6" | awk '{print $1}')" = 45bbbea5ccdbad7aeccb04698bb194845f731c53685a5e01d04cef2bfd20a237

"${CXX:-c++}" -std=c++17 -O3 -Wall -Wextra -Wpedantic \
  "$artifact_dir/search_three_extension.cpp" -o "$tmp_dir/search_three_extension"

for id in 0 1 2 3 4 5 6 7; do
  (
    start=$((id * 173114 / 8))
    end=$(((id + 1) * 173114 / 8))
    count=$((end - start))
    rc=0
    "$tmp_dir/search_three_extension" "$tmp_dir/unique.g6" "$start" "$count" \
      > "$tmp_dir/$id.out" 2> "$tmp_dir/$id.progress" || rc=$?
    test "$rc" -eq 20
    : > "$tmp_dir/$id.ok"
  ) &
done
wait
test "$(find "$tmp_dir" -name '*.ok' -type f | wc -l)" -eq 8

cat "$tmp_dir/0.out" "$tmp_dir/1.out" "$tmp_dir/2.out" "$tmp_dir/3.out" \
  "$tmp_dir/4.out" "$tmp_dir/5.out" "$tmp_dir/6.out" "$tmp_dir/7.out" \
  > "$tmp_dir/ranges.txt"
cmp "$tmp_dir/ranges.txt" "$artifact_dir/EXPECTED_RANGES.txt"
python3 "$artifact_dir/summarize_frontier.py" "$tmp_dir/0.progress" \
  "$tmp_dir/1.progress" "$tmp_dir/2.progress" "$tmp_dir/3.progress" \
  "$tmp_dir/4.progress" "$tmp_dir/5.progress" "$tmp_dir/6.progress" \
  "$tmp_dir/7.progress" > "$tmp_dir/frontier.tsv"
cmp "$tmp_dir/frontier.tsv" "$artifact_dir/FINAL_OBSTRUCTIONS.tsv"
cat "$tmp_dir/ranges.txt"
cat "$tmp_dir/frontier.tsv"
