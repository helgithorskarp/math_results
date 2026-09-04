#!/bin/sh
set -eu

if test "$#" -ne 2; then
  echo "usage: $0 CADICAL_INCLUDE_DIR LIBCADICAL_A" >&2
  exit 2
fi

artifact_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
source_dir="$artifact_dir/../ramsey_r55_catalog_two_vertex_extension_obstruction"
tmp_dir=$(mktemp -d "${TMPDIR:-/tmp}/r55-two-extension-review.XXXXXX")
trap 'rm -rf "$tmp_dir"' EXIT HUP INT TERM

xz -dc "$source_dir/r55_41_deletions_unique.g6.xz" > "$tmp_dir/cores.g6"
test "$(sha256sum "$tmp_dir/cores.g6" | awk '{print $1}')" = \
  225c00c0fc26d1b372e598790fb3954a442c0bee5fd68b59a5be76bbb7761f5b

"${CXX:-c++}" -std=c++17 -O3 -Wall -Wextra -Wpedantic \
  -I "$1" "$artifact_dir/independent_sat_audit.cpp" "$2" -pthread \
  -o "$tmp_dir/independent_sat_audit"

"$tmp_dir/independent_sat_audit" "$tmp_dir/cores.g6" \
  "$source_dir/extension_models.txt" > "$tmp_dir/actual.txt"
diff -u "$artifact_dir/EXPECTED_OUTPUT.txt" "$tmp_dir/actual.txt"
cat "$tmp_dir/actual.txt"
