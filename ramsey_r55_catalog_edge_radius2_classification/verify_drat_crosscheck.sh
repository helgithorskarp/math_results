#!/bin/sh
set -eu

if test "$#" -ne 1; then
  echo "usage: $0 /path/to/drat-trim" >&2
  exit 2
fi

artifact_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT HUP INT TERM

"${CXX:-c++}" -std=c++17 -O3 -Wall -Wextra -Wpedantic \
  "$artifact_dir/gen_edge_radius2.cpp" -o "$tmp_dir/gen_edge_radius2"
"$tmp_dir/gen_edge_radius2" "$artifact_dir/r55_42some.g6" 0 "$tmp_dir/full.cnf"
test "$(sha256sum "$tmp_dir/full.cnf" | awk '{print $1}')" = 318737dea0343767235874b2fd0766eac397dd74161793bb29b543af6dc33b5f
test "$(sha256sum "$artifact_dir/core0.cnf" | awk '{print $1}')" = 2a59c1385f9081ebc820285586a2e7c1db80a79f8c3b15483d3280dac5627e27
python3 "$artifact_dir/check_cnf_subset.py" "$tmp_dir/full.cnf" "$artifact_dir/core0.cnf"

test "$(sha256sum "$artifact_dir/core0.drat.xz" | awk '{print $1}')" = 89bdc51b8c0548353724f65cdf05ee48a5de164fffb160de74c5bc490993875c
xz -dc "$artifact_dir/core0.drat.xz" > "$tmp_dir/core0.drat"
test "$(sha256sum "$tmp_dir/core0.drat" | awk '{print $1}')" = 143bbbaf64c9aa0372f810e022005ea300d45cbc13ad023913c7fb5251900413
"$1" "$artifact_dir/core0.cnf" "$tmp_dir/core0.drat" > "$tmp_dir/proof.out"
tr '\r' '\n' < "$tmp_dir/proof.out" | grep -q '^s VERIFIED$'
echo 'VERIFIED representative_core_drat=1'
