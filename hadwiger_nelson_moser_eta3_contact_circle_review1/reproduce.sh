#!/bin/sh
set -eu
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo=$(CDPATH= cd -- "$here/.." && pwd)
target="$repo/hadwiger_nelson_moser_eta3_contact_circle"
prior="$repo/hadwiger_nelson_independent_moser_sum_collisions_review1/independent_audit.py"
work=$(mktemp -d /tmp/hn-eta3-review.XXXXXX)
trap 'rm -rf "$work"' EXIT HUP INT TERM

g++ -std=c++17 -O3 -shared -fPIC "$here/geometry_check.cpp" -o "$work/geometry.so"
python3 "$here/independent_check.py" \
  --certificate "$target/certificate.json" \
  --expected "$target/expected.json" \
  --prior-audit "$prior" \
  --library "$work/geometry.so" > "$work/actual.json"
cmp "$here/EXPECTED.json" "$work/actual.json"

g++ -std=c++17 -O1 -g -fno-omit-frame-pointer -fsanitize=undefined \
  -shared -fPIC "$here/geometry_check.cpp" -o "$work/geometry-ubsan.so"
python3 -O "$here/independent_check.py" \
  --certificate "$target/certificate.json" \
  --expected "$target/expected.json" \
  --prior-audit "$prior" \
  --library "$work/geometry-ubsan.so" > "$work/actual-ubsan.json"
cmp "$here/EXPECTED.json" "$work/actual-ubsan.json"
sha256sum -c "$here/SHA256SUMS"
echo PASS
