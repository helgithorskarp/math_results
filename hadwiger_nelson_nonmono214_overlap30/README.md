# Exact two-copy overlap exclusion for the 214-vertex nonmono-pair gadget

## Result

Let `V` be the archived 214-point `v214e977` distance-three
nonmonochromatic-pair gadget of Jaan Parts. For every Euclidean isometry `g`
with

```text
|V intersection g(V)| >= 30,
```

the strict unit-distance graph on `V union g(V)` is 4-colorable.

The complete exact stratum has 8,932 placements. Its graphs have 214--398
vertices and 977--2,058 strict unit edges. Explicit four-colorings are stored
in `colorings.txt.xz`; `verify.sh` reconstructs all exact unit edges and checks
every certificate without invoking a SAT solver.

Two copies have at most 428 vertices, so any non-4-colorable member would beat
the 509-vertex record. The result closes only the overlap-at-least-30 family;
lower-overlap placements and larger or mixed compositions remain open.

## Completeness and exactness

Every placement with at least two overlaps maps a nonzero directed segment of
the second copy to an equal-length directed segment of the first. Enumerating
all such segment pairs gives every orientation-preserving and
orientation-reversing isometry supporting two overlaps. Exact point-difference
multiplicities then give all translations, so the threshold-30 filter loses no
placement in the theorem.

The full census contains 2,234 rotations, 2,234 reflections, and 3,992,708
placements with at least two overlaps; 8,932 have at least 30. Arithmetic is
performed in `Q(sqrt(3),sqrt(5),sqrt(11))` with integer coefficient arrays and
explicit denominators.

## Verification

Requirements are a C++20 compiler, `xz`, and `sha256sum`. The check is
single-core.

```bash
cd hadwiger_nelson_nonmono214_overlap30
./verify.sh
```

Expected output is in `expected_verify.txt`.

## Full rebuild

The exact enumerator, graph emitter, SAT witness generator, and Python
requirements are shared with `../hadwiger_nelson_nonmono159_overlap10`.
The intermediate graph stream is about 128 MB and is not committed.

```bash
python3 -m venv .venv
.venv/bin/pip install -r ../hadwiger_nelson_nonmono159_overlap10/requirements.txt
g++ -std=c++20 -O3 ../hadwiger_nelson_nonmono159_overlap10/enumerate_overlaps.cpp -o enumerate_overlaps
g++ -std=c++20 -O3 ../hadwiger_nelson_nonmono159_overlap10/emit_graphs.cpp -o emit_graphs
./enumerate_overlaps points.tsv points.tsv --emit-at-least 30 > overlap_transforms.rebuilt.txt
xz -dc overlap_transforms.txt.xz | cmp - overlap_transforms.rebuilt.txt
./emit_graphs points.tsv points.tsv overlap_transforms.rebuilt.txt > graphs.rebuilt.txt
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

`SOURCE.md` records the archived coordinate provenance. No minimality claim is
made for the gadget.
