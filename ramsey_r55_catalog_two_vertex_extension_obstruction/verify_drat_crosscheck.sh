#!/bin/sh
set -eu

if test "$#" -ne 1; then
  echo "usage: $0 /path/to/drat-trim" >&2
  exit 2
fi

artifact_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT HUP INT TERM

xz -dc "$artifact_dir/r55_41_deletions_unique.g6.xz" > "$tmp_dir/cores.g6"
"${CXX:-c++}" -std=c++17 -O3 -Wall -Wextra -Wpedantic \
  "$artifact_dir/gen_two_extension.cpp" -o "$tmp_dir/gen_two_extension"
"$tmp_dir/gen_two_extension" "$tmp_dir/cores.g6" 3451 "$tmp_dir/core3451.cnf"

actual_cnf=$(sha256sum "$tmp_dir/core3451.cnf" | awk '{print $1}')
test "$actual_cnf" = a344f2440cbb24bd5af24c4411ddf9eef16d00422e14796a90efff1a9640c5c3
actual_proof=$(sha256sum "$artifact_dir/core3451.drat.xz" | awk '{print $1}')
test "$actual_proof" = 0f93733a4391b879db6158391d3e412b87b53e45942502b05f8d7c3cb7875c01

xz -dc "$artifact_dir/core3451.drat.xz" > "$tmp_dir/core3451.drat"
actual_raw_proof=$(sha256sum "$tmp_dir/core3451.drat" | awk '{print $1}')
test "$actual_raw_proof" = c0b1778e7aed4ecf248c4836365b46982931e9c37274316b936875c8a50e1d6d
"$1" "$tmp_dir/core3451.cnf" "$tmp_dir/core3451.drat" -i \
  > "$tmp_dir/drat-output.txt"
grep -q '^s VERIFIED' "$tmp_dir/drat-output.txt"
cat "$tmp_dir/drat-output.txt"
