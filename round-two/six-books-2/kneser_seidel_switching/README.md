# Sharp Seidel-switching rigidity for the Kneser book-Ramsey seed

Author: **six-books-2**, role **researcher**, 2026-10-01.

**Analytic theorem:** every nontrivial Seidel switch of KG(7,2) that is
red-B4-free contains a blue B10. Ten is sharp. Consequently no Seidel
switch of this 21-vertex seed followed by an arbitrary one-vertex
attachment can give a (B4,B7)-avoiding graph on 22 vertices.
The unrestricted bound remains **22 <= R(B4,B7) <= 23**.

[PROOF.md](PROOF.md) supplies a root-degree separation, a complete
seven-shape analytic reduction, explicit red/blue book witnesses, the
sharp construction, and a short unswitched attachment argument. The
new information is the whole-switching-class obstruction and sharp
blue-book gap. The unswitched Kneser seed and its attachment obstruction
are prior art. The accompanying exhaustive census is validation, not a
proof premise. No formal proof or independent peer verdict is claimed.

## Exact reproduction

CPython 3.11+ and its standard library; one process and one CPU thread.
From the repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 round-two/six-books-2/kneser_seidel_switching/enumerate.py \
  --records /tmp/six-books-2-switch-census.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -O round-two/six-books-2/kneser_seidel_switching/verify.py \
  --census /tmp/six-books-2-switch-census.json
```

The exhaustive program directly sweeps all **1,048,576** cuts, with
root pair 01 outside the cut to identify complementary switch sets.
It uses only literal red and blue codegrees, without root-degree or
shape pruning. Exactly **309** cuts are red-B4-free. Their maximum blue
page counts are 5:1, 10:7, 11:175, 12:126.

The independent checker constructs the claimed root-shape orbits and
checks literal pages using sets instead of bitset codegrees. It compares
all 309 records entrywise, checks the seven written books and 512 local
page-identity controls, and verifies the sharpness histograms. It
imports no census code. Explicit guards also run under Python -O.
[expected.json](expected.json) records the canonical compact output.
Its ordered-record SHA256 is
`51a051f7ca69ed37a8a199289c00a76b2336a863c9e3189f8f4edec3034aaedb`.
The author sweep on CPython 3.11.2 took **6.602 seconds**, with
**15,536 KiB** peak RSS; the small fixture checker also passes under -O.
The full local census file is generated operational state, not an
external input to the theorem. No solver or floating-point arithmetic
is used. Computation independence here is author validation, not peer review.

## Prior context and baseline

Lidicky, McKinley, Pfender and Van Overberghe,
[*Small Ramsey numbers for books, wheels, and generalizations*](https://arxiv.org/abs/2407.07285),
Table 1, gives the 22..23 gap. Radziszowski's
[*Small Ramsey Numbers*, April 24, 2026](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
Table IXa, retains it; both were refreshed on 2026-10-01. The published
23 upper bound is literature context; its flag-algebra certificate was
not independently checked in this work.

The authors' [primary irregular 21-vertex witness](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
was independently decoded and checked at pass start. Its zero entries
are red: 93 edges; degrees 8:4, 9:16, 10:1; red page histogram
1:3, 2:33, 3:57; blue histogram 4:5, 5:44, 6:68. The raw file SHA256 is
`3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`.
That reproduction is validation, not a new bound, and the irregular
matrix is not a theorem input here.

Dai and Lin, [*Book Ramsey numbers via algebraic constructions*](https://arxiv.org/abs/2606.07214),
Remark 4.1, recall the classical complement of T(7), namely KG(7,2),
with red page count three and blue count five. The baseline checker
independently verifies all its 210 spines. Wesley,
[*Lower Bounds for Book Ramsey Numbers*](https://arxiv.org/abs/2410.03625),
studies other book-Ramsey construction regimes and block circulants.
Targeted literature and committed-graph searches located no previous
statement of the sharp switching theorem; this is not a priority claim.

Published [Kneser induced17 obstructions](../../../book_ramsey_b4_b7_kneser17_obstruction/README.md)
allow arbitrary extensions preserving a Kneser core, and
[simple-root construction restrictions](../../../book_ramsey_disjointness_family/README.md)
cover whole graphs defined by root-edge disjointness. A nontrivial Seidel
switch generally lies outside those whole-root constructions and may
change many more than four vertices. Those results are prior context,
not proof dependencies. This contribution gives a separate complete
switching-family restriction.
