#!/bin/sh
set -eu

if test "$#" -ne 1; then
  echo "usage: $0 /path/to/drat-trim" >&2
  exit 2
fi

artifact_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT HUP INT TERM

tail -n +2 "$artifact_dir/FRONTIER_HASHES.tsv" |
while IFS="	" read -r local_index original_index models clauses cnf_sha raw_sha xz_sha; do
  python3 "$artifact_dir/gen_three_extension.py" "$artifact_dir/frontier7.g6" \
    "$local_index" "$tmp_dir/$local_index.cnf" > "$tmp_dir/$local_index.gen"
  test "$(sha256sum "$tmp_dir/$local_index.cnf" | awk '{print $1}')" = "$cnf_sha"
  test "$(sha256sum "$artifact_dir/drat/$local_index.drat.xz" | awk '{print $1}')" = "$xz_sha"
  xz -dc "$artifact_dir/drat/$local_index.drat.xz" > "$tmp_dir/$local_index.drat"
  test "$(sha256sum "$tmp_dir/$local_index.drat" | awk '{print $1}')" = "$raw_sha"
  "$1" "$tmp_dir/$local_index.cnf" "$tmp_dir/$local_index.drat" -i \
    > "$tmp_dir/$local_index.verify"
  tr '\r' '\n' < "$tmp_dir/$local_index.verify" | grep -q '^s VERIFIED$'
  echo "VERIFIED local_index=$local_index original_core_index=$original_index models=$models clauses=$clauses"
done

echo "VERIFIED direct_drat_cases=7"
