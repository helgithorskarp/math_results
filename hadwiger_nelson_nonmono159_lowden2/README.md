# Exact low-denominator two-copy exclusion for the 159-vertex nonmono gadget

## Result

Let `V` be the archived 159-point `v159e646` square-root-seven
nonmonochromatic-triple gadget of Jaan Parts. Consider an exact Euclidean
isometry `g` whose orthogonal part has canonical denominator at most 2 in the
field representation below, and suppose

```text
|V intersection g(V)| >= 2.
```

Then the strict unit-distance graph on `V union g(V)` is 4-colorable.

There are exactly 12 such overlap-supported orientations and 32,990 distinct
placements. Their strict graphs have 159--316 vertices and 646--1,437 edges.
This includes every overlap multiplicity from 2 through 159 in the stated
orientation class, rather than a high-overlap tail. Explicit four-colorings
are stored in `colorings.txt.xz`; `verify.sh` reconstructs every strict unit
edge exactly and checks every witness without a SAT solver.

Any non-4-colorable member would have at most 316 vertices and improve the
509-vertex record. The theorem does not cover higher-denominator orientations
or placements with fewer than two overlaps.

## Canonical orientation denominator

Coordinates lie in `K = Q(sqrt(3),sqrt(5),sqrt(11))`. For an orthogonal map,
the exact cosine and sine are stored as field coefficient arrays divided by a
positive integer `d`. A common integer gcd is removed and the sign is
normalized, making `d` canonical. The family in this artifact is `d <= 2`.

Any placement with two overlaps maps a nonzero directed source segment to an
equal-length target segment. Such segment correspondences determine every
possible rotation or reflection. `enumerate_overlaps.cpp` enumerates and
canonicalizes all of them, filters the canonical denominator, and then obtains
every supported translation from exact point-difference multiplicities.

The unfiltered orientation census has 1,874 rotations and 1,830 reflections.
Exactly 12 orientations satisfy `d <= 2`; their 32,990 placements recover
2,797,044 overlap-pair certificates.

## Verification

Requirements are a C++20 compiler, `xz`, and `sha256sum`. The direct check is
single-core.

```bash
cd hadwiger_nelson_nonmono159_lowden2
./verify.sh
```

Expected output is in `expected_verify.txt`.

## Full rebuild

SAT witness regeneration additionally requires Python 3.11+ and
`python-sat==1.8.dev24`. The temporary graph stream is about 325 MB and is not
committed.

```bash
python3 -m venv .venv
.venv/bin/pip install -r ../hadwiger_nelson_nonmono159_overlap10/requirements.txt
g++ -std=c++20 -O3 enumerate_overlaps.cpp -o enumerate_overlaps
g++ -std=c++20 -O3 ../hadwiger_nelson_nonmono159_overlap10/emit_graphs.cpp -o emit_graphs
./enumerate_overlaps points.tsv points.tsv --emit-at-least 2 --max-denominator 2 \
  > overlap_transforms.rebuilt.txt
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

`SOURCE.md` records coordinate provenance. No minimality claim is made for the
archived gadget.
