# Exact two-copy overlap exclusion for the 159-vertex nonmono-triple gadget

## Result

Let `V` be the 159-point set in `points.tsv`, the archived `v159e646`
nonmonochromatic-triple gadget of Jaan Parts. For every Euclidean isometry `g`
such that

```text
|V intersection g(V)| >= 10,
```

the strict unit-distance graph on `V union g(V)` is 4-colorable.

The census is exact. It contains 30,013 isometric placements. Their strict
graphs have 159--308 vertices and 646--1,420 edges. An explicit four-coloring
for every graph is stored in `colorings.txt.xz`; `verify.sh` reconstructs all
strict unit edges in exact arithmetic and checks every witness.

This is useful negative evidence for the Hadwiger--Nelson record search: no
two-copy high-overlap composition of this complementary gadget family can
improve the 509-vertex Parts graph. It does not cover placements with fewer
than ten overlaps, three or more copies, or mixed gadget families.

## Why the enumeration is complete

Any placement with at least two overlapping points supplies two distinct
source points and two distinct target points at the same distance. Those two
directed segments determine exactly one orientation-preserving or
orientation-reversing Euclidean isometry. `enumerate_overlaps.cpp` enumerates
all equal-length directed-segment pairs, canonicalizes the resulting exact
orientations, and then counts every translation by a difference map. Thus
filtering the resulting placements at multiplicity ten loses no isometry in
the stated family.

All coordinates and transformations lie in
`Q(sqrt(3),sqrt(5),sqrt(11))`. A field element is stored as eight integer
coefficients in the bit-subset basis

```text
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165).
```

The point scale is 12. Transformation denominators are carried explicitly;
equality and squared-distance-one tests use integer arithmetic only.

## Verify the certificates

Requirements are a C++20 compiler, `xz`, and `sha256sum`. The direct check is
single-core and takes about five minutes on the research host.

```bash
cd hadwiger_nelson_nonmono159_overlap10
./verify.sh
```

Expected output is in `expected_verify.txt`. The verifier does not invoke a
SAT solver: the checked four-colorings are independently useful certificates.

## Rebuild the census and witnesses

The following additionally requires Python 3.11+ and `python-sat==1.8.dev24`.
The emitted graph stream is about 289 MB and is intentionally not committed.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
g++ -std=c++20 -O3 enumerate_overlaps.cpp -o enumerate_overlaps
g++ -std=c++20 -O3 emit_graphs.cpp -o emit_graphs
./enumerate_overlaps points.tsv points.tsv --emit-at-least 10 > overlap_transforms.rebuilt.txt
xz -dc overlap_transforms.txt.xz | cmp - overlap_transforms.rebuilt.txt
./emit_graphs points.tsv points.tsv overlap_transforms.rebuilt.txt > graphs.rebuilt.txt
.venv/bin/python check_graph_stream.py graphs.rebuilt.txt --jobs 4 > colorings.rebuilt.txt
xz -dc colorings.txt.xz | cmp - colorings.rebuilt.txt
```

The exact enumerator reuses the audited field/orientation implementation in
`../hadwiger_nelson_parts509_affine_overlap_scan/enumerate_overlaps.cpp`; the
wrapper generalizes it from the Parts `L`/`S` split to two arbitrary point
sets.

## Context and provenance

Parts' paper gives the 509-vertex, 2,442-edge record graph and describes the
nonmonochromatic gadget program:

- J. Parts, [Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane](https://arxiv.org/abs/2010.12665).
- J.-P. Haugland, [A new upper bound for the order of a 5-chromatic
  unit-distance graph](https://arxiv.org/abs/2608.04542), which still identifies
  509 as the record in 2026.

`SOURCE.md` records the archived coordinate source and hashes. The newer Parts
table reports a 157-vertex refinement of the square-root-seven gadget; this
artifact deliberately studies the publicly archived 159-vertex instance and
makes no minimality claim for it.
