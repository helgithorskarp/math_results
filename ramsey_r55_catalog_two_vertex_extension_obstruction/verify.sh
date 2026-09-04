#!/bin/sh
set -eu

artifact_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT HUP INT TERM

xz -dc "$artifact_dir/r55_41_deletions_unique.g6.xz" > "$tmp_dir/cores.g6"
actual=$(sha256sum "$tmp_dir/cores.g6" | awk '{print $1}')
expected=225c00c0fc26d1b372e598790fb3954a442c0bee5fd68b59a5be76bbb7761f5b
test "$actual" = "$expected"

"${CXX:-c++}" -std=c++17 -O3 -Wall -Wextra -Wpedantic \
  "$artifact_dir/verify_extension_models.cpp" -o "$tmp_dir/verify_extension_models"
"$tmp_dir/verify_extension_models" "$tmp_dir/cores.g6" \
  "$artifact_dir/extension_models.txt" > "$tmp_dir/output.txt"
cmp "$tmp_dir/output.txt" "$artifact_dir/EXPECTED_OUTPUT.txt"
cat "$tmp_dir/output.txt"
