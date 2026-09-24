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
>    absolute value below 23, and `M` differs from `G0` in at most three
>    off-diagonal positions, then `det(M)` cannot be a square at least `L^2`
>    unless `M=G0`.
> 2. If every off-diagonal entry belongs to `{-1,3}` and `M` differs from
>    `G0` in at most five positions, then `det(M)` cannot be a square at
>    least `L^2` unless `M` is permutation-congruent to `G0`.  More
>    precisely, the equality cases are `G0` and twelve labeled copies at
>    distance four.
> 3. At distance six, exactly two automorphism orbits have square determinant
>    greater than `L^2`, with square roots `2823605452800000` and
>    `2783182848000000`.  Both matrices are positive definite, but neither is
>    the row Gram matrix of a 23-by-23 sign matrix.  Consequently, if
>    `M=R R^T` for a sign matrix `R`, `M` is graph-valued, and its distance
>    from `G0` is at most six, then `|det(R)| <= L`; equality occurs only in
>    the cases described in part 2.

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
classifies graph-valued sign-Gram record equality through distance six.  The
distinction between square candidate Grams and actual sign Grams is essential
at distance six.

The artifact also determines the complete row-permutation symmetry of `G0`:

```text
Aut(G0) = (C2^6 semidirect S3) x (S4 wreath C2),
|Aut(G0)| = 442368.
```

Under this group, the 372 distance-four square survivors form exactly six
orbits, of sizes `12, 24, 24, 24, 96, 192`.  The 12 record-equality cases
form one orbit.  The two 24-element orbits immediately below the record have
the same determinant but are not related by an automorphism of `G0`.

This does **not** determine the maximal determinant in order 23.  Graph-valued
candidate Gram matrices at distance seven or farther from `G0`, arbitrary
legal-entry matrices at distance four or farther, and neighborhoods of other
record designs remain untreated.

## Exact census

The six nonoverlapping searches cover 351,599,742,406 labeled edited matrices:

| neighborhood | matrices | square-determinant survivors | largest square root |
|---|---:|---:|---:|
| exactly one arbitrary legal edit | 2,530 | 0 | — |
| exactly two arbitrary legal edits | 3,187,800 | 756 | 2,743,271,424,000,000 |
| exactly three `-1`/`3` toggles | 2,667,126 | 24 | 2,740,715,520,000,000 |
| exactly four `-1`/`3` toggles | 166,695,375 | 372 | 2,779,447,296,000,000 |
| exactly five `-1`/`3` toggles | 8,301,429,675 | 14,784 | 2,743,153,459,200,000 |
| exactly six `-1`/`3` toggles | 343,125,759,900 | 420,647 | 2,823,605,452,800,000 |

The 1,152 survivors in the first four rows are evaluated by direct exact
integer determinants.  Their complete determinant/multiplicity census is in
`certificate.json`.
At distance four, twelve have square root exactly `L`; the independent
checker reconstructs the twelve row/column transpositions above.  Every
other survivor is strictly below `L`, with largest root
`2,760,297,676,800,000`, about 0.689% below the record.

A broader, overlapping search permits all ten alternative legal values at
each of exactly three positions.  Its labeled domain has
`binom(253,3)*10^3 = 2,667,126,000` matrices.  The 2,667,126 underlying edit
sets form 8,887 automorphism orbits; testing all 1,000 transported value
assignments for one representative of each orbit gives a complete
8,887,000-evaluation cover.  The modular sieve leaves 4,825 encodings, and
direct exact determinants show that all are squares with 880 distinct roots.
The largest root is only `2,740,715,520,000,000 < L`.  This search overlaps
the three-toggle row above, so it is not included in the disjoint total.

As a retained directional control, the enumerator also checks the 148,995
ways to delete four existing `3`-edges.  This overlaps the radius-four
search and has no modular survivors.

The radius-five row is proved by testing one representative of every
automorphism orbit.  Exactly 27 of the 4,132,509 representatives have square
determinant.  Their orbit sizes sum to 14,784, their determinants are all
distinct, and their largest square root is
`2,743,153,459,200,000`, about 1.306% below `L`.  The complete exact list is
in `radius5_certificate.json`.

At distance six, the 343,125,759,900 labeled edit sets form 81,094,402
automorphism classes.  The modular sieve leaves 359 classes; direct exact
determinants show that all 359 are squares, representing 420,647 labeled
matrices and 298 distinct determinant values.  Exactly two classes exceed
the record, with orbit sizes 96 and 48.  The next largest square root is
`2,771,425,689,600,000 < L`.

The two apparent improvements are genuine positive-definite square Gram
candidates, not numerical artifacts.  They fail a stronger necessary column
condition.  If `G=R R^T` with invertible sign matrix `R`, every sign column
`v` of `R` obeys `v^T G^{-1}v=1`.  After normalizing `v_0=1`, exhaustive
exact enumeration of all `2^22` sign vectors finds no admissible column for
the larger candidate.  The smaller candidate has 48 admissible columns, but
all have `v_0v_1=1`; any 23-column decomposition would therefore give
`G_01=23`, whereas this candidate has `G_01=3`.  Thus neither decomposes.

The same obstruction now has a compact symmetry quotient.  Explicit
row-permutation subgroups of orders 4,608 and 9,216 reduce the first complete
normalized sign cube to 138,240 canonical vectors and the second forbidden
`v_0v_1=-1` half-cube to 51,840.  Exact orbit multiplicities recover all
`2^22` and `2^21` labeled vectors.  The unrestricted second quotient has two
admissible orbits, of sizes 32 and 16, whose expansion is exactly the original
48-column list.  This independently structured certificate replaces the
four-million-vector trace as the smallest published proof layer.

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

The machine-readable symmetry certificate continues the exact Burnside count
through 12 toggles.  `radius5.cpp` independently generates the 4,132,509
radius-five representatives by colored connected-component decomposition and
tests all of them.  Its counts for every radius from zero through five agree
with the Burnside calculation.

`radius6.cpp` extends the same constructive quotient without storing the
much larger six-edge connected catalogue.  It streams the 30 connected
six-edge shapes and reuses the stored catalogue only for disconnected edit
graphs.  Its 81,094,402 generated representatives agree exactly with the
independent radius-six Burnside coefficient.

## Reproduction

Only Python 3.10 or later and a C++20 compiler are required.

```bash
g++ -std=c++20 -O3 -Wall -Wextra -Wconversion -Wshadow -pedantic \
  enumerate.cpp -o enumerate
./enumerate record23.txt > result.json
python3 verify.py result.json
python3 symmetry.py result.json
g++ -std=c++20 -O3 -Wall -Wextra -Wconversion -Wshadow -pedantic \
  radius5.cpp -o radius5
./radius5 record23.txt > radius5_result.json
python3 verify_radius5.py radius5_result.json
g++ -std=c++20 -O3 -Wall -Wextra -Wconversion -Wshadow -pedantic \
  radius3_arbitrary.cpp -o radius3_arbitrary
./radius3_arbitrary record23.txt > radius3_arbitrary_result.json
python3 verify_radius3_arbitrary.py radius3_arbitrary_result.json
g++ -std=c++20 -O3 -Wall -Wextra -Wconversion -Wshadow -pedantic \
  radius6.cpp -o radius6
./radius6 record23.txt > radius6_result.json
python3 verify_radius6.py radius6_result.json
python3 candidate_obstructions.py
python3 candidate_orbit_obstructions.py > candidate_orbit_result.json
python3 verify_candidate_orbit_obstructions.py candidate_orbit_result.json
```

The terminal output ends with

```text
modular local Gram classification verified
exact local Gram classification certificate verified
exact Gram-graph symmetry and orbit certificate verified
radius-five canonical orbit enumeration and modular sieve verified
exact radius-five symmetry-quotient certificate verified
arbitrary radius-three covering quotient and modular sieve verified
exact arbitrary radius-three covering certificate verified
radius-six canonical orbit enumeration and modular sieve verified
exact radius-six symmetry-quotient certificate verified
both record-beating radius-six Gram candidates are indecomposable
symmetry-compressed sign-column certificate verified
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
The radius-five C++ generator and sieve take about 25 seconds on one core and
use about 259 MiB peak resident memory.
The Python checker independently evaluates all 27 surviving determinants by
Bareiss elimination and traverses their 13-generator orbits in under one
second.  A full `-fsanitize=address,undefined` run produced byte-identical
JSON without a diagnostic.  The deterministic `radius5_result.json` SHA-256
is `ac9e23d4fe04fda81012cd736c77c610956858635a45912a65497a8a21457efc`.

The arbitrary radius-three C++ cover takes about 26 seconds on one core and
uses about 10 MiB peak resident memory.  Two complete optimized runs produced
byte-identical JSON, and the independent Python checker evaluates all 4,825
survivors exactly in about four seconds.  The deterministic
`radius3_arbitrary_result.json` SHA-256 is
`a5302735167229496e3bc4d294bc5821ed5132922e53b576a9b4a8632bac98af`.
A complete `-fsanitize=address,undefined` run also produced byte-identical
JSON without a diagnostic.

The radius-six C++ run takes about 9 minutes 44 seconds on one core and peaks
at 289,908 KiB resident memory.  The independent Python checker takes about
14 seconds, including exact Bareiss
determinants and traversal of all 359 survivor orbits.  The column-obstruction
checker takes about 20 seconds.  The deterministic `radius6_result.json`
SHA-256 is `8145a2fdf28d61be0abb24813385c9b4f28f358668875be5f40ef9bc2c8e46e2`.
The symmetry-compressed column generator takes about 15 seconds and its
definition-level checker, including the independent full Gray-code control,
takes about 19 seconds.  The deterministic
`candidate_orbit_certificate.json` SHA-256 is
`8b8a282bdcaacaea67f9c354fc40e2637a61ddb510864aa3e7b3d4e199c5a764`.

An optional SAT experiment can be regenerated with
`python3 candidate_sat_certificates.py /tmp/order23-sat`.  At official-source
commits `c60730422e758ef1cebe7aeddf2dda31c996bf04` (CaDiCaL 3.0.1) and
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` (`drat-trim`), the two target
CNFs were independently proved and checked UNSAT.  Their raw binary traces
were 35 MiB and 33 MiB, and extracted core proofs were larger, so no SAT trace
is committed.  `PROOF.md` records the exact CNF hashes and experiment scope.

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
radius-five, radius-six, and arbitrary radius-three generators additionally
trust the completeness of the colored connected-component canonicalization
proved in `PROOF.md`.  Their independently predicted underlying edit-set
class counts agree with Burnside's lemma.  For arbitrary radius three, all
1,000 value assignments are tested over every underlying representative;
this is a complete cover, not a claim that stabilizer-equivalent valued edits
have been deduplicated.  All arithmetic is exact; no positivity assumption or
floating-point filter is used.  The radius-six decomposition obstruction
trusts the identity `R^T(RR^T)^{-1}R=I` and exhaustive Gray-code traversal of
the normalized sign cube; exact rational inversion is checked by multiplying
`G P=Q I`, and the published record matrix supplies a positive control.  The
compact obstruction additionally trusts only the explicit candidate
permutation subgroups and their elementary binary-color orbit classification;
the checker expands the reported solution orbits and compares them exactly to
the full Gray-code result.  The optional SAT traces are not part of the
published proof boundary.
