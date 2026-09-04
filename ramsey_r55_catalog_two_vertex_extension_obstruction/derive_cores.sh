#!/bin/sh
set -eu

if test "$#" -ne 2; then
  echo "usage: $0 /path/to/delptg /path/to/shortg" >&2
  exit 2
fi

artifact_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT HUP INT TERM

"$1" -q -l "$artifact_dir/r55_42some.g6" "$tmp_dir/all.g6"
"$2" -q "$tmp_dir/all.g6" "$tmp_dir/unique.g6"

test "$(wc -l < "$tmp_dir/all.g6")" -eq 13776
test "$(wc -l < "$tmp_dir/unique.g6")" -eq 9757
echo '31925078d3c58a6e9b9b8eb1fde82bfca07e10439dbe80647c44c849575bee4e  all.g6' | \
  (cd "$tmp_dir" && sha256sum -c -)
echo '225c00c0fc26d1b372e598790fb3954a442c0bee5fd68b59a5be76bbb7761f5b  unique.g6' | \
  (cd "$tmp_dir" && sha256sum -c -)

xz -dc "$artifact_dir/r55_41_deletions_unique.g6.xz" > "$tmp_dir/shipped.g6"
cmp "$tmp_dir/unique.g6" "$tmp_dir/shipped.g6"
echo "VERIFIED deletions=13776 isomorphism_classes=9757"
