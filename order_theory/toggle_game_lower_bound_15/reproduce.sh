#!/usr/bin/env bash
set -euo pipefail

scratch_root=${1:-/scratch/toggle_game_lower_bound_15}
source_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
catalog_dir="$scratch_root/catalogs"
build_dir="$scratch_root/build"
base_url=https://rds.westernsydney.edu.au/Schools/SCEM/VGebhardt-UnlabelledLattices-20180926

mkdir -p "$catalog_dir" "$build_dir"

curl -fL --retry 3 "$base_url/unlabelled.sha256" \
  -o "$catalog_dir/unlabelled.sha256"

for order in 02 03 04 05; do
  curl -fL --retry 3 "$base_url/unlabelled-${order}.cats" \
    -o "$catalog_dir/unlabelled-${order}.cats"
done

for order in 06 07 08 09 10 11 12 13 14; do
  curl -fL --retry 3 "$base_url/unlabelled-${order}.cats.xz" \
    -o "$catalog_dir/unlabelled-${order}.cats.xz"
  xz -dc "$catalog_dir/unlabelled-${order}.cats.xz" \
    > "$catalog_dir/unlabelled-${order}.cats"
done

(
  cd "$catalog_dir"
  sha256sum --ignore-missing -c unlabelled.sha256
)

g++ -std=c++20 -O3 -DNDEBUG -Wall -Wextra -Wpedantic \
  -Wconversion -Wshadow "$source_dir/catalog_search.cpp" \
  -o "$build_dir/catalog_search"

: > "$scratch_root/results.txt"
for order in $(seq 2 14); do
  printf -v padded '%02d' "$order"
  "$build_dir/catalog_search" "$order" \
    "$catalog_dir/unlabelled-${padded}.cats" cats \
    | tee -a "$scratch_root/results.txt"
done
