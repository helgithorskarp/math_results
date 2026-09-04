# Exact cross-edge census for two-overlap Parts placements

## Result

Let `L` be the 374-point large gadget of the Parts 509 construction, and let
`S+` be its 135-point small gadget with a second origin point adjoined.  The
two gadgets have 510 labels before identifications.  The sibling exact affine
enumeration proves that 2,373,802 Euclidean placements

```text
L union (T(S+) + t)
```

have exactly two cross-gadget coincidences.  This artifact classifies all of
them by their additional cross-unit edges:

| property | exact placement count |
|---|---:|
| exactly two overlaps | 2,373,802 |
| at least one cross-unit label pair | 2,373,802 |
| at least one genuinely new cross edge | 2,194,728 |
| no genuinely new cross edge | **179,074** |

The published two-overlap gluing lemma says that a placement with exactly two
overlaps and no genuinely new cross edge is four-colourable.  Consequently
all 179,074 placements in the last row are four-colourable, and any
five-chromatic exactly-two-overlap placement in this fixed-gadget family must
belong to the remaining set of 2,194,728.

The rotation-preserving and reflection-reversing halves each contain exactly
1,186,901 two-overlap placements, of which 1,097,364 have a genuinely new
cross edge.  The equality is an independently checked aggregate symmetry.

This is a finite structural reduction, **not a new five-chromatic graph and
not an improvement of the 509-vertex record**.  It does not close the
2,194,728 genuinely cross-coupled cases or placements with three or more
overlaps.

## Cross-difference characterization

Fix one of the 2,840 orthogonal orientations `T` forced by a matching nonzero
segment of `L` and `S+`.  Form the labelled cross-difference multiset

```text
D_T = {p - Tq : p in L, q in S+}.
```

A translation `t` has exactly two overlaps precisely when `t` has
multiplicity two in `D_T`.  A cross label pair `(p,q)` is a unit pair in the
placement at `t` precisely when

```text
|(p - Tq) - t| = 1.
```

Thus cross-edge detection becomes an exact unit-neighbour query inside the
finite point set underlying `D_T`.

Some cross label pairs do not add an edge to the strict union graph.  If
`q` is one of the two overlapped `S+` labels, its image is already an `L`
point, and the cross pair duplicates an internal `L` edge exactly when those
two `L` labels are adjacent.  Dually, if `p` is overlapped, the cross pair can
duplicate an internal `S+` edge.  With exactly two overlaps these are the
only ways a cross label pair can fail to be a genuinely new strict edge.  The
census tests both conditions against the exactly reconstructed internal
graphs.

## Complete exact enumeration

All arithmetic is in
`K = Q(sqrt(3),sqrt(5),sqrt(11))`, represented in its eight-element radical
basis with signed integers.  The program independently reproduces the prior
checksums:

```text
distinct directed L vectors       11,650
distinct directed S+ vectors       1,666
orientations                       2,840
all placements with >=2 overlaps 2,992,078
determining overlap pairs        17,658,256
internal L / S+ edges          1,860 / 564
```

For speed, the program places cross differences in square buckets of side
`1/4`.  This index is certified rather than heuristic.  Each radical is
bounded between consecutive rationals with denominator `10^12`; the bounds
are checked by exact integer squaring.  For every coordinate encountered,
the exact value lies less than `1/1000` above its computed lower bound.  Only
68 bucket offsets can therefore contain a unit neighbour.  An exact interval
square test removes impossible candidates, and all 18,848,971 survivors are
tested by exact multiplication in `K`.  No floating-point operation is used.

The full per-orientation output is committed as `expected_census.txt` with
SHA-256
`ddb2b0f7f878e56ce985c8b4493bdd6850fc548d9568cb3f62460364da99bfe4`.

## Reproduction

From this directory:

```bash
g++ -std=c++20 -O3 -DNDEBUG -Wall -Wextra -pedantic \
  census.cpp -o census
./census \
  ../hadwiger_nelson_parts509_completion_census_degree9/points.tsv \
  > census_output.txt
diff -u expected_census.txt census_output.txt
python3 verify.py > verify_output.txt
diff -u expected_verify.txt verify_output.txt
```

The exact C++ census is single-threaded and took about 12 minutes on the
shared research host.  The Python verifier uses only the standard library.

## Trust boundary

- `census.cpp` exactly reconstructs the orientations, all cross differences,
  internal edges, interval filters, and final unit tests.  Hash collisions
  cannot affect the result because full field elements are compared.
- `verify.py` pins every source, checks the complete transcript digest and
  all per-orientation/global sums, verifies the radical bounds and signed
  128-bit safety inequality, and reruns the solver-free sibling certificate
  supplying the pair-flexibility input used by the gluing lemma.
- The transcript checker does not independently reimplement the full C++
  census.  The proof is a reproducible finite exact computation in ordinary
  C++ and Python, not a proof-assistant formalization.
- The conclusion is confined to this fixed Parts `L`/`S+` placement family.

## Files

- `census.cpp` — complete exact orientation, translation, and cross-edge
  census.
- `expected_census.txt` — all 2,840 per-orientation counts and global
  checksums.
- `verify.py` — solver-free source, transcript, arithmetic, and dependency
  verifier.
- `expected_verify.txt` — expected compact verifier output.
