# Exact mixed-gadget overlap exclusion

## Result

Let `A` be the archived 159-point `v159e646` square-root-seven
nonmonochromatic-triple gadget and let `B` be the archived 214-point
`v214e977` distance-three nonmonochromatic-pair gadget of Jaan Parts. For every
Euclidean isometry `g` satisfying

```text
|A intersection g(B)| >= 20,
```

the strict unit-distance graph on `A union g(B)` is 4-colorable.

The exact stratum contains 13,184 placements. Their strict graphs have
250--353 vertices and 1,207--1,756 edges. `colorings.txt.xz` contains an
explicit four-coloring for every graph, and `verify.sh` reconstructs every
unit edge in exact arithmetic and checks the certificates without a SAT
solver.

Since even the disjoint union has only 373 vertices, any non-4-colorable member
would have improved the 509-vertex record. This result closes the stated
high-overlap mixed family, but not placements with fewer than 20 overlaps or
compositions with additional gadgets.

## Exact completeness argument

Any placement with at least two overlaps maps a directed segment of `B` to an
equal-length directed segment of `A`. Such a correspondence determines one
orientation-preserving or orientation-reversing isometry. The enumerator
checks every equal-length directed-segment pair, canonicalizes the resulting
orientation, and obtains every supported translation from exact point
differences. Filtering that complete enumeration at overlap 20 therefore
omits no isometry in the theorem.

The census has 1,906 rotations, 1,906 reflections, and 2,557,868 placements
with at least two overlaps; exactly 13,184 have at least 20. Arithmetic is in
`Q(sqrt(3),sqrt(5),sqrt(11))`, encoded in the integer bit-subset basis
documented by the preceding homogeneous artifact.

## Verification

Requirements are a C++20 compiler, `xz`, and `sha256sum`. The check is
single-core.

```bash
cd hadwiger_nelson_nonmono159_214_overlap20
./verify.sh
```

Expected output is in `expected_verify.txt`.

## Full rebuild

The exact enumeration and graph emitters are shared with
`../hadwiger_nelson_nonmono159_overlap10`. Rebuilding the SAT-produced
colorings additionally requires Python 3.11+ and the requirements from that
directory. The intermediate graph stream is about 158 MB and is not committed.

```bash
python3 -m venv .venv
.venv/bin/pip install -r ../hadwiger_nelson_nonmono159_overlap10/requirements.txt
g++ -std=c++20 -O3 ../hadwiger_nelson_nonmono159_overlap10/enumerate_overlaps.cpp -o enumerate_overlaps
g++ -std=c++20 -O3 ../hadwiger_nelson_nonmono159_overlap10/emit_graphs.cpp -o emit_graphs
./enumerate_overlaps points159.tsv points214.tsv --emit-at-least 20 > overlap_transforms.rebuilt.txt
xz -dc overlap_transforms.txt.xz | cmp - overlap_transforms.rebuilt.txt
./emit_graphs points159.tsv points214.tsv overlap_transforms.rebuilt.txt > graphs.rebuilt.txt
.venv/bin/python ../hadwiger_nelson_nonmono159_overlap10/check_graph_stream.py \
  graphs.rebuilt.txt --jobs 4 > colorings.rebuilt.txt
xz -dc colorings.txt.xz | cmp - colorings.rebuilt.txt
```

## Context

- J. Parts, [Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane](https://arxiv.org/abs/2010.12665).
- J. K. Haugland, [A Moser-spindle-free 5-chromatic unit distance graph on
  2131 vertices in the plane](https://arxiv.org/abs/2608.04542), confirming
  the 509-vertex benchmark in 2026.

`SOURCE.md` records coordinate provenance. No minimality claim is made for
either archived gadget.
