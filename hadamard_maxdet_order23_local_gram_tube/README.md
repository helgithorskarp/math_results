# A local Gram classification tube around the order-23 record

## Result

Let `R0` be the published order-23 sign matrix in `record23.txt`, let

```text
G0 = R0 R0^T,
L  = |det(R0)| = 2779447296000000,
```

and measure the distance between symmetric matrices by the number of
different entries strictly above the diagonal.  The off-diagonal entries of
`G0` consist of 208 copies of `-1` and 45 copies of `3`.

This artifact proves the following finite local classification.

> **Lemma.** Let `M` be symmetric of order 23 with diagonal entries 23.
>
> 1. If every off-diagonal entry of `M` is congruent to 3 modulo 4 and has
>    absolute value below 23, and `M` differs from `G0` in at most two
>    off-diagonal positions, then `det(M)` cannot be a square at least `L^2`
>    unless `M=G0`.
> 2. If every off-diagonal entry belongs to `{-1,3}` and `M` differs from
>    `G0` in at most four positions, then `det(M)` cannot be a square at
>    least `L^2` unless `M` is permutation-congruent to `G0`.  More
>    precisely, the equality cases are `G0` and twelve labeled copies at
>    distance four.

The twelve nontrivial equality cases have a simple description.  In each of
the three four-vertex blocks

```text
{3,4 | 5,6}, {7,8 | 9,10}, {11,12 | 13,14},
```

swap one vertex on the left with one on the right.  There are
`3*2*2=12` choices.  Simultaneously permuting the corresponding rows and
columns of `G0` changes exactly four entries, so every such matrix is the
Gram matrix of a row permutation of `R0`.

The computation is stronger than a positive-definite candidate search: it
tests all matrices in the stated discrete neighborhoods, whether or not they
are positive definite.  A parity-normalized Gram matrix of a nonsingular
order-23 sign matrix satisfies the entry conditions in part 1, so the lemma
excludes every record-beating sign decomposition in these neighborhoods and
classifies graph-valued record equality through distance four.

The artifact also determines the complete row-permutation symmetry of `G0`:

```text
Aut(G0) = (C2^6 semidirect S3) x (S4 wreath C2),
|Aut(G0)| = 442368.
```

Under this group, the 372 distance-four square survivors form exactly six
orbits, of sizes `12, 24, 24, 24, 96, 192`.  The 12 record-equality cases
form one orbit.  The two 24-element orbits immediately below the record have
the same determinant but are not related by an automorphism of `G0`.

This does **not** determine the maximal determinant in order 23.  Candidate
Gram matrices farther from `G0`, including other graph-Gram matrices and
matrices containing larger inner products, remain untreated.

## Exact census

The four nonoverlapping searches cover 172,552,831 edited matrices:

| neighborhood | matrices | square-determinant survivors | largest square root |
|---|---:|---:|---:|
| exactly one arbitrary legal edit | 2,530 | 0 | — |
| exactly two arbitrary legal edits | 3,187,800 | 756 | 2,743,271,424,000,000 |
| exactly three `-1`/`3` toggles | 2,667,126 | 24 | 2,740,715,520,000,000 |
| exactly four `-1`/`3` toggles | 166,695,375 | 372 | 2,779,447,296,000,000 |

All 1,152 survivors are evaluated by direct exact integer determinants.
Their complete determinant/multiplicity census is in `certificate.json`.
At distance four, twelve have square root exactly `L`; the independent
checker reconstructs the twelve row/column transpositions above.  Every
other survivor is strictly below `L`, with largest root
`2,760,297,676,800,000`, about 0.689% below the record.

As a retained directional control, the enumerator also checks the 148,995
ways to delete four existing `3`-edges.  This overlaps the radius-four
search and has no modular survivors.

## Exact symmetry quotient

An edit set is a subset of the 253 unordered off-diagonal positions.
Burnside's lemma applied to the induced action of `Aut(G0)` gives the
following exact orbit counts:

| number of toggles | labeled edit sets | symmetry classes |
|---:|---:|---:|
| 0 | 1 | 1 |
| 1 | 253 | 16 |
| 2 | 31,878 | 380 |
| 3 | 2,667,126 | 8,887 |
| 4 | 166,695,375 | 197,931 |
| 5 | 8,301,429,675 | 4,132,509 |
| 6 | 343,125,759,900 | 81,094,402 |

The machine-readable certificate continues the exact Burnside count through
12 toggles.  In particular, a radius-five graph-valued search needs at most
4,132,509 determinant tests once one representative of each orbit is
generated, rather than 8.3 billion labeled tests.  This artifact proves the
orbit count; it does not yet implement the canonical representative
generator or make a radius-five determinant claim.

## Reproduction

Only Python 3.10 or later and a C++20 compiler are required.

```bash
g++ -std=c++20 -O3 -Wall -Wextra -Wconversion -Wshadow -pedantic \
  enumerate.cpp -o enumerate
./enumerate record23.txt > result.json
python3 verify.py result.json
python3 symmetry.py result.json
```

The terminal output ends with

```text
modular local Gram classification verified
exact local Gram classification certificate verified
exact Gram-graph symmetry and orbit certificate verified
```

`enumerate.cpp` performs 172,701,826 evaluations, including the overlapping
four-deletion control, and assigns every nonsquare a quadratic-nonresidue
witness among 48 explicitly checked primes.  It emits the 1,152 cases that
survive those tests.  `verify.py` independently rebuilds
`G0`, checks `det(G0)=L^2` by fraction-free Bareiss elimination, recomputes
the scaled inverse, validates the survivor encodings, and evaluates every
survivor determinant directly with Python integers.  It derives the twelve
distance-four equality edit sets from explicit vertex transpositions and
requires exact agreement with the emitted equality cases.

On the research host, GCC 12.2.0 completed the documented strict `-O3` build
in 734.6 seconds on one core; the Python checker took 3.1 seconds.  An
allocation-heavy baseline produced byte-identical JSON in 770.8 seconds.
The symmetry checker takes under one second after `result.json` exists.  It
independently constructs the two automorphism factors, verifies their
generator closures, computes their induced cycle types and Burnside
coefficients with exact integers, and traverses the six survivor orbits.

## Known frontier and sources

Orrick, Solomon, Dowdeswell, and Smith published the matrix and determinant
record in [*New lower bounds for the maximal determinant
problem*](https://arxiv.org/abs/math/0304410).  Exhaustive candidate-Gram
generation and decomposition are the standard route to exact odd-order
results; the relevant definitions and algorithms are given by
[Orrick](https://arxiv.org/abs/math/0401179) and by
[Brent--Orrick--Osborn--Zimmermann](https://arxiv.org/abs/1112.4160).

At least 14 inequivalent order-23 matrices attaining the same record were
already known by 2005; see Orrick's
[*On the enumeration of some D-optimal
designs*](https://arxiv.org/abs/math/0511141).  This artifact is anchored to
the particular published matrix `R0`.  It does not assert that the Gram
neighborhoods of the other record designs are equivalent to this one.

The present result is a local certificate around the order-23 record.  No
claim is made that the local neighborhood had previously been studied, or
that this replaces global candidate-Gram enumeration.

## Trust boundary

The proof trusts the matrix determinant lemma, elementary finite-field
arithmetic, and the fact that an integer square is a quadratic residue or
zero modulo every prime.  All listed primes are checked by trial division at
runtime.  Products modulo primes are bounded below `10^18`, and the raw
scaled-update entries are below `2*10^9`, so signed 64-bit arithmetic is
safe.  The C++ enumerator is the exhaustive coverage component; the Python
program is an independent exact checker for its compact survivor list and
for the permutation description of every record-equality survivor.
The symmetry extension additionally trusts Burnside's lemma and the
elementary component-based proof of the displayed automorphism group.  Its
Python checker performs only exact permutation and integer arithmetic.  The
radius-five number is an orbit count, not a completed determinant search.
