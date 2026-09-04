#!/bin/sh
set -eu

if test "$#" -ne 1; then
  echo "usage: $0 NEW_WORK_DIRECTORY" >&2
  exit 2
fi

artifact_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
root_dir="$artifact_dir/.."
work_dir=$1
if test -e "$work_dir"; then
  echo "work directory already exists: $work_dir" >&2
  exit 2
fi
mkdir -p "$work_dir"

target="$root_dir/hadwiger_nelson_parts509_two_overlap_library_census"
points="$root_dir/hadwiger_nelson_parts509_completion_census_degree9/points.tsv"
libraries="$root_dir/hadwiger_nelson_parts509_two_overlap_cross_census/colour_libraries.txt"
seeds="$target/residual_seeds.tsv"

"${CXX:-c++}" -std=c++20 -O3 -Wall -Wextra -pedantic \
  "$target/census_all.cpp" -o "$work_dir/primary_census"
"${CXX:-c++}" -std=c++20 -O3 -Wall -Wextra -pedantic \
  "$artifact_dir/reverse_match_census.cpp" -o "$work_dir/reverse_match_census"

"$work_dir/primary_census" "$points" "$libraries" \
  "$work_dir/primary_residual.jsonl" > "$work_dir/primary_census.jsonl"
PYTHONDONTWRITEBYTECODE=1 python3 "$target/verify.py" \
  "$work_dir/primary_census.jsonl" "$work_dir/primary_residual.jsonl" \
  > "$work_dir/target_verify.txt"
diff -u "$target/expected_verify.txt" "$work_dir/target_verify.txt"

PYTHONDONTWRITEBYTECODE=1 python3 "$target/check_residual.py" \
  "$work_dir/primary_residual.jsonl" > "$work_dir/target_residual_check.txt"
diff -u "$target/expected_residual_check.txt" "$work_dir/target_residual_check.txt"

"${CXX:-c++}" -std=c++20 -O3 -Wall -Wextra -pedantic \
  "$target/test_matcher.cpp" -o "$work_dir/test_matcher"
"$work_dir/test_matcher" > "$work_dir/target_matcher.txt"
diff -u "$target/expected_matcher.txt" "$work_dir/target_matcher.txt"

"$work_dir/reverse_match_census" "$points" "$libraries" \
  "$work_dir/reverse_residual.jsonl" > "$work_dir/reverse_census.jsonl"

PYTHONDONTWRITEBYTECODE=1 python3 "$artifact_dir/audit_transcripts.py" \
  "$work_dir/primary_census.jsonl" "$work_dir/primary_residual.jsonl" \
  "$work_dir/reverse_census.jsonl" "$work_dir/reverse_residual.jsonl" "$seeds" \
  > "$work_dir/reviewer_audits.txt"
PYTHONDONTWRITEBYTECODE=1 python3 "$artifact_dir/audit_orientations.py" \
  "$points" "$seeds" >> "$work_dir/reviewer_audits.txt"
diff -u "$artifact_dir/EXPECTED_OUTPUT.txt" "$work_dir/reviewer_audits.txt"
cat "$work_dir/reviewer_audits.txt"

sha256sum "$work_dir/primary_census.jsonl" "$work_dir/primary_residual.jsonl" \
  "$work_dir/reverse_census.jsonl" "$work_dir/reverse_residual.jsonl"
