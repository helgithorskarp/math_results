#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
mkdir -p "$here/build"

cxx=${CXX:-g++}
flags="-O3 -std=c++20 -Wall -Wextra -pedantic"
$cxx $flags "$here/enumerate_rank829.cpp" -o "$here/build/enumerate_rank829"
$cxx $flags "$here/verify_rank829.cpp" -o "$here/build/verify_rank829"

set +e
"$here/build/enumerate_rank829" > "$here/ACTUAL_OUTPUT.txt"
producer_status=$?
set -e
if [ "$producer_status" -ne 20 ]; then
  echo "producer returned $producer_status, expected 20" >&2
  exit 1
fi
"$here/build/verify_rank829" >> "$here/ACTUAL_OUTPUT.txt"
diff -u "$here/EXPECTED_OUTPUT.txt" "$here/ACTUAL_OUTPUT.txt"
echo REPRODUCED_VERIFIED_RANK829_PARITY_CELL_FAMILY
