#!/usr/bin/env bash
set -eu

artifact_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
work_dir=$(mktemp -d)
cleanup() {
    rm -r -- "$work_dir"
}
trap cleanup EXIT HUP INT TERM

cd "$artifact_dir"
sha256sum -c SHA256SUMS
xz -dc overlap_transforms.txt.xz > "$work_dir/overlap_transforms.txt"
xz -dc colorings.txt.xz > "$work_dir/colorings.txt"
g++ -std=c++20 -O3 verify_colorings.cpp -o "$work_dir/verify_colorings"
"$work_dir/verify_colorings" points159.tsv points214.tsv \
    "$work_dir/overlap_transforms.txt" "$work_dir/colorings.txt" \
    > "$work_dir/actual_verify.txt"
cmp expected_verify.txt "$work_dir/actual_verify.txt"
cat "$work_dir/actual_verify.txt"
