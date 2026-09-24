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
> 4. At distance seven there are exactly 2,943 automorphism orbits with
>    square determinant.  Exactly 26 have square root greater than `L`, none
>    has square root equal to `L`, and all 26 record-beating matrices are
>    positive definite but sign-indecomposable.  Consequently the conclusion
>    of part 3 holds with distance seven in place of distance six.
> 5. If every off-diagonal entry satisfies the arbitrary legal-entry
>    conditions in part 1 and `M` differs from `G0` in at most four positions,
>    then a positive-definite `M` with square determinant at least `L^2` is
>    permutation-congruent to `G0` and has determinant exactly `L^2`.  At
>    exactly four positions the complete normalized cover has only one square
>    determinant above `L^2`, and that matrix is not positive definite.

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
classifies graph-valued sign-Gram record equality through distance seven.  The
distinction between square candidate Grams and actual sign Grams is essential
at distances six and seven.

At distance seven the largest square determinant root is
`2838233088000000`; the largest root below the record is
`2777874432000000`.  Exhaustive normalized-column searches eliminate the 26
record-beating candidates: eleven admit no column satisfying
`v^T G^-1 v=1`, fourteen force a row-pair product inconsistent with the
candidate Gram, and the remaining candidate has 424 admissible columns but
forces

```text
1 + v_11*v_13 + v_11*v_14 + v_13*v_14 = 0
```

for every one (row subscripts are zero-based).  Summing over 23 columns would
give zero, whereas its three relevant Gram entries are all 3 and require
`23+3+3+3=32`.

The artifact also determines the complete row-permutation symmetry of `G0`:

```text
Aut(G0) = (C2^6 semidirect S3) x (S4 wreath C2),
|Aut(G0)| = 442368.
```

Under this group, the 372 distance-four square survivors form exactly six
orbits, of sizes `12, 24, 24, 24, 96, 192`.  The 12 record-equality cases
form one orbit.  The two 24-element orbits immediately below the record have
the same determinant but are not related by an automorphism of `G0`.

The artifact now also supplies `record23_class2.txt`, a second exact record
matrix `R1`.  It differs from `R0` in 12 entries and has

```text
|det(R1)| = L.
```

Nevertheless, `R1` is not Hadamard-equivalent to `R0`: their exhaustive
absolute 4-by-4 minor distributions, listed for determinant magnitudes
`0,8,16`, are

```text
R0: 45245701, 31659704, 1505620
R1: 45247429, 31657400, 1506196.
```

Signed row and column permutations are bijections on minors of each size, so
this discrepancy is an exact inequivalence certificate.  Explicit signed
permutations in both checkers map `R1 R1^T` and `R1^T R1` to the corresponding
Grams of `R0`.  Thus the local Gram classification above applies, after the
displayed normalization, to two distinct H-classes.

The second class is found without randomized search.  For each core index
`c=0,1,2`, independently choose one of the three four-vertex blocks, one of
its two twin pairs for two flips in row `c`, and one twin pair for two flips
in column `c`.  These `12^3=1728` structured 12-flip matrices have exactly
770 absolute determinant values.  Exactly two labeled choices attain `L`,
and none exceeds it; `R1` is one of the two.  The C++ program exhausts this
family and the complete 4-minor distributions.  An independent Python
checker instead separates the H-classes by a canonical four-row
column-pattern profile: the signature `(2,3,3,2,3,3,3,4)` occurs 2,508 times
for `R0` and 2,460 times for `R1`.

The full decomposition census is now exact.  Normalize every sign column by
making its first entry positive and disregard column order.  There are
exactly 552,960 normalized unordered sign matrices `R` satisfying

```text
R R^T = G0.
```

They form exactly **14 Hadamard-equivalence classes**.  Under `Aut(G0)`, six
classes have orbit size 18,432 and stabilizer order 24; eight have orbit size
55,296 and stabilizer order 8.  Thus

```text
6*18432 + 8*55296 = 552960.
```

The published `R0` and the independently certified `R1` are classes 14 and
13 in the canonical list.  All fourteen class representatives are recorded
as explicit normalized-column masks in
`gram_decomposition_certificate.json`.

The key reduction is exact orthogonality.  Exhausting the `2^22` normalized
sign vectors leaves 1,382 vectors `v` with `v^T G0^-1 v=1`.  Join two when
`v^T G0^-1 w=0`; the resulting graph has 338,582 edges.  A decomposition of
`G0` is then exactly a 23-clique.  Exact colored branch-and-bound enumerates
all 552,960 such cliques, and the 13 generators of `Aut(G0)` partition them
into the fourteen classes above.  A separate Python implementation rebuilds
the graph with arbitrary-precision integers, independently repeats the
9,804,083-node clique census, reconstructs every representative matrix, and
traverses all fourteen orbits.

There is a second, structurally different census.  The 1,382 candidate
columns form four `Aut(G0)`-orbits of sizes `6,512,432,432`.  Their equitable
compatibility quotient is

```text
  2 512 216 216
  6 131 216 216
  3 256  73 108
  3 256 108  73
```

and the four induced graphs have clique numbers `3,8,6,6`.  Since these
sum to 23, every decomposition must attain all four bounds.  The six-point
graph is two disjoint triangles.  The 512-point graph has exactly 276,480
maximum 8-cliques.  For either triangle, every such 8-clique has exactly six
common neighbors in each 432-point orbit; both six-sets are cliques and are
cross-complete.  Hence the remaining twelve columns are forced and

```text
2*276480 = 552960.
```

The 276,480 middle cliques form ten automorphism orbits.  In six orbits the
two triangle extensions merge under the stabilizer, while in four they
split, giving `6+2*4=14` full decomposition classes.  The independent
checker counts middle cliques by anchoring one vertex: its neighborhood has
4,320 seven-cliques and no eight-clique, so transitivity gives
`512*4320/8=276480`.  It then expands ten explicit orbit representatives and
checks only their two forced completions.  This avoids the original
9,804,083-node full-clique recursion.

The transpose action on these classes is also exact.  Every representative's
column Gram is signed-permutation-congruent to `G0`, so transposition closes
on the same fourteen classes.  In the certificate's canonical numbering it
has four two-cycles

```text
(1,11), (2,12), (3,7), (4,8)
```

and fixes classes `5,6,9,10,13,14`.  Thus exactly six of the fourteen
classes are self-dual under transposition.  This conclusion does not depend
on an isomorphism black box: `transpose_duality_certificate.json` gives, for
each class `i`, explicit signed row and column permutations carrying
`R_i^T` to the stated canonical representative `R_j`.  The independent
checker reconstructs the fourteen matrices from their masks and verifies
all fourteen entrywise equalities.

This does **not** determine the maximal determinant in order 23.  Graph-valued
candidate Gram matrices at distance eight or farther from `G0`, arbitrary
legal-entry matrices at distance five or farther, and other possible Gram
classes remain untreated.  In particular, the result classifies every sign
decomposition of the published Gram center, not every order-23 sign matrix
whose determinant equals or exceeds the record.

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

The arbitrary-entry cover now extends to exactly four positions.  Its labeled
domain has `binom(253,4)*10^4 = 1,666,953,750,000` matrices.  The 197,931
underlying edit-set orbits, independently predicted by Burnside's lemma, give
a complete 1,979,310,000-evaluation cover after all 10,000 transported value
assignments are tested for each representative.  The 48-prime sieve leaves
990,410 encodings; exact low-rank determinants show that every survivor is a
square.  Of these, 990,408 lie below the record, one equals it, and one has
root `2,791,505,920,000,000 > L`.  The latter matrix is not positive definite:
its order-14 leading principal minor is exactly `-43,620,761,600,000`.  The
equality encoding belongs to the already certified 12-element
row-permutation orbit.  Thus no order-23 sign Gram in the full arbitrary
legal-entry radius-four neighborhood beats the record.  The compact shard
manifest records the exact JSON hash, five partition counts, 48-prime witness
distribution, survivor count, and survivor digest for each of the 32 omitted
bulk shard files.

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
| 7 | 12,107,437,527,900 | 1,503,560,419 |

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

`radius7.cpp` adds 79 connected seven-edge shapes and handles the exceptional
`6+1` partition without materializing either colored catalogue.  It first
quotients color-multiplicity vectors by the outer `S3 x C2`, then quotients
assignments by the stabilizer of that vector and the graph automorphism group.
An exact radius-six regression reproduces all 4,361,518 connected classes.
Thirty-two deterministic, disjoint shards give 75,778,019 connected classes,
158,015,168 classes of type `6+1`, and 1,269,767,232 classes from the remaining
partitions.  Their sum is the independent radius-seven Burnside coefficient.

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
g++ -std=c++20 -O3 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -Werror \
  radius4_arbitrary.cpp -o radius4_arbitrary
mkdir -p /tmp/radius4-arbitrary-parts
seq 0 31 | xargs -P 8 -I SHARD sh -c \
  './radius4_arbitrary SHARD 32 record23.txt \
   > /tmp/radius4-arbitrary-parts/part_SHARD.json \
   2> /tmp/radius4-arbitrary-parts/part_SHARD.log'
python3 merge_radius4_arbitrary.py -o radius4_arbitrary_result.json \
  /tmp/radius4-arbitrary-parts/part_*.json
python3 make_radius4_arbitrary_manifest.py \
  -o radius4_arbitrary_shard_manifest_result.json \
  radius4_arbitrary_result.json /tmp/radius4-arbitrary-parts/part_*.json
cmp radius4_arbitrary_shard_manifest_result.json \
  radius4_arbitrary_shard_manifest.json
python3 verify_radius4_arbitrary.py radius4_arbitrary_result.json \
  radius4_arbitrary_shard_manifest_result.json
g++ -std=c++20 -O3 -Wall -Wextra -Wconversion -Wshadow -pedantic \
  radius6.cpp -o radius6
./radius6 record23.txt > radius6_result.json
python3 verify_radius6.py radius6_result.json
python3 candidate_obstructions.py
python3 candidate_orbit_obstructions.py > candidate_orbit_result.json
python3 verify_candidate_orbit_obstructions.py candidate_orbit_result.json
g++ -std=c++20 -O3 -Wall -Wextra -Wpedantic -Werror \
  radius7.cpp -o radius7
mkdir -p /tmp/radius7-parts
seq 0 31 | xargs -P 8 -I SHARD sh -c \
  './radius7 SHARD 32 record23.txt > /tmp/radius7-parts/part_SHARD.json \
   2> /tmp/radius7-parts/part_SHARD.log'
python3 merge_radius7.py -o radius7_result.json \
  /tmp/radius7-parts/part_*.json
python3 radius7_candidate_obstructions.py \
  radius7_result.json radius7_candidate_result.json 8
python3 verify_radius7.py \
  radius7_result.json radius7_candidate_result.json 8
g++ -std=c++20 -O3 -Wall -Wextra -Wconversion -Wshadow -pedantic \
  multicenter.cpp -o multicenter
./multicenter record23.txt record23_class2.txt
python3 verify_multicenter.py
g++ -std=c++20 -O3 -Wall -Wextra -Wconversion -Wshadow -pedantic \
  gram_decompositions.cpp -o gram_decompositions
./gram_decompositions record23.txt record23_class2.txt \
  > gram_decomposition_result.json
python3 verify_gram_decompositions.py gram_decomposition_result.json
python3 factor_gram_decompositions.py gram_decomposition_certificate.json \
  > gram_factorization_result.json
python3 verify_gram_factorization.py gram_decomposition_certificate.json \
  gram_factorization_result.json
python3 transpose_duality.py gram_decomposition_certificate.json \
  > transpose_duality_result.json
python3 verify_transpose_duality.py gram_decomposition_certificate.json \
  transpose_duality_result.json
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
exact arbitrary radius-four covering certificate verified
radius-six canonical orbit enumeration and modular sieve verified
exact radius-six symmetry-quotient certificate verified
both record-beating radius-six Gram candidates are indecomposable
symmetry-compressed sign-column certificate verified
radius seven: 1,503,560,419 symmetry classes and 2,943 exact square Gram orbits
all 26 record-beating square Gram orbits are indecomposable
exact radius-seven symmetry-quotient certificate verified
second H-class and signed Gram-center equivalence verified
the two record matrices are Hadamard-inequivalent
552960 exact 23-cliques independently enumerated
14 decomposition orbits cover every clique
candidate compatibility graph factors into clique numbers 3+8+6+6
six merged and four split middle orbits give exactly fourteen classes
fourteen explicit signed transpose equivalences verified
self-dual classes: 5, 6, 9, 10, 13, 14
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

The arbitrary radius-four cover was run as 32 deterministic hash-balanced
shards with eight workers in about 21 minutes of wall time.  It evaluated
1,979,310,000 transported assignments and retained 990,410 modular survivors.
The streaming Python merger classified every survivor by exact integer
low-rank determinants in about two minutes, checked positive definiteness by
fraction-free Sylvester elimination, and emitted the compact certificate
`radius4_arbitrary_certificate.json`.  Its SHA-256 is recorded in
`SHA256SUMS`; the canonical survivor-encoding SHA-256 is
`1bc15ff2431fb08ec0ad7faedefe8eff124e88f735a00e9a33f2e7e7cef803de`.
`radius4_arbitrary_shard_manifest.json` supplies 32 compact restart and
reproduction checkpoints; regenerating it from the omitted shard files is
byte-identical, with SHA-256
`620a30c9b8cb199de869f135e9667ba945d8607e845a2eac047c4de2acc50954`.

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

The radius-seven census was run as 32 deterministic shards with eight workers
in about 42 minutes of wall time.  The strict C++20 build and a sparse
end-to-end address/undefined-behavior sanitizer shard completed without a
diagnostic.  Merging requires exact shard coverage, unique survivors, closed
sieve accounting, and agreement with the independent Burnside coefficient.
The obstruction producer and verifier each repeat 26 exhaustive `2^22`
normalized-column traversals, using eight workers.  Their exact hashes are
listed in `SHA256SUMS`.

The multicenter C++ census takes about three seconds on one core; the
independent Python checker takes about five seconds.  They use different
H-invariants (complete 4-minor distribution versus canonical four-row
pattern profile), while both verify the exact determinants, the structured
switch family, and explicit signed Gram congruences.

The complete Gram-decomposition C++ census takes about nine seconds on one
core and emits byte-identical JSON.  The independent pure-Python checker
takes about 75 seconds, including its own 1,382-vertex graph construction,
9,804,083-node clique search, exact reconstruction of all fourteen
representatives, and orbit traversals.  The deterministic
`gram_decomposition_certificate.json` SHA-256 is
`7b94f5918015a250db3619c7e1f2f37a8d31a3e2ad589afe21a99a30a445aa81`.
A complete address- and undefined-behavior-sanitizer run also emits that
same byte-identical certificate without a diagnostic.

The factored producer takes about 31 seconds and its independent
vertex-anchored checker about 46 seconds.  Their deterministic compact
certificate is `gram_factorization_certificate.json`, with SHA-256
`0e02a35023db47594a469c42e3e30111630ea3ef018fd9c3566ad8c679def26d`.
It contains the equitable quotient, induced clique counts, ten middle-orbit
representatives, merge/split data, and hashes of both the 276,480 middle
cliques and the forced 552,960-clique stream.

The transpose-certificate producer takes about 18 seconds, dominated by
reconstructing the normalized sign-column set and its automorphism action;
the definition-level checker takes under one second.  Repeated producer runs
emit byte-identical JSON.  The SHA-256 of
`transpose_duality_certificate.json` is
`12284e4fc6c0f06ab54615b56574b99070177772fcb620544280f97ab462fa16`.

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
designs*](https://arxiv.org/abs/math/0511141).  That is a global lower bound
obtained by gradient ascent, not an exhaustive decomposition statement for a
specified Gram in the cited text.  The advance here is a reproducible proof
that the published Gram `G0` itself has exactly fourteen H-inequivalent sign
decompositions, together with explicit representatives.  No claim is made
that every record design has Gram equivalent to `G0`.

The targeted September 2026 primary-literature refresh found no later
order-23 exact classification beyond the sources above.  This is only a
novelty check, not a proof of absence.  The present result is a local
certificate around the order-23 record.  No claim is made that the local
neighborhood had previously been studied, or that this replaces global
candidate-Gram enumeration.

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
radius-five, radius-six, radius-seven, and arbitrary radius-three and
radius-four generators
additionally trust the completeness of the colored connected-component
canonicalization proved in `PROOF.md`.  Their independently predicted
underlying edit-set class counts agree with Burnside's lemma.  Radius seven
additionally trusts the multiplicity-vector/stabilizer factorization proved
there; its complete radius-six regression and final Burnside agreement test
both levels of that quotient.  For arbitrary radii three and four,
respectively all 1,000 and 10,000 value assignments are tested over every
underlying representative; these are complete covers, not claims that
stabilizer-equivalent valued edits have been deduplicated.  The radius-four
modular survivors are evaluated through the exact determinant lemma over
Python integers, and its sole above-record square is rejected by an exact
negative leading principal minor.  No floating-point filter is used.  The
per-shard manifest binds every omitted raw JSON output by SHA-256 and preserves
all local count and witness summaries without treating the manifest as an
independent proof of canonical coverage.  The
radius-six decomposition obstruction
trusts the identity `R^T(RR^T)^{-1}R=I` and exhaustive Gray-code traversal of
the normalized sign cube; exact rational inversion is checked by multiplying
`G P=Q I`, and the published record matrix supplies a positive control.  The
compact obstruction additionally trusts only the explicit candidate
permutation subgroups and their elementary binary-color orbit classification;
the checker expands the reported solution orbits and compares them exactly to
the full Gray-code result.  The radius-seven obstructions use the same exact
scaled-inverse identity and full Gray-code domain.  Their only final steps are
zero-column contradictions, forced pair correlations, or one displayed
three-row identity; the verifier checks every admissible column directly.
The optional SAT traces are not part of the
published proof boundary.  The multicenter extension trusts exhaustive exact
enumeration of a stated 1,728-member switch family and invariance of minor
distributions under signed permutations.  Its independent checker uses the
separate elementary four-row projective-pattern invariant; no graph
isomorphism package or floating-point determinant enters the certificate.
The complete decomposition extension additionally trusts the elementary
identity `R^T G0^-1 R=I`, the equivalence between a square orthonormal column
set and a Gram decomposition, and the greedy-color upper bound used in the
exact clique recursion.  The C++ and Python implementations use different
bit-set representations and independently obtain the same graph, node, and
clique counts.  Orbit representatives are expanded again by the Python
checker; their disjoint sizes sum to the full independent clique count.
The factorized extension supplies a second coverage argument.  It trusts
four much smaller induced-graph clique bounds, vertex-transitive incidence
counting, and the forced common-neighbor construction.  Its checker uses
plain recursive anchored clique counting rather than the producer's greedy
color recursion, expands all ten reported middle-clique orbits, and checks
both representative completions entrywise in the compatibility graph.
The transpose extension depends on the exhaustive fourteen-class result,
then reduces its new content to fourteen displayed finite identities.  For
each canonical representative, the compact certificate records two
permutations and two sign vectors whose direct application carries the
transpose to another canonical representative.  The independent checker
does not import the producer and verifies every entry of every identity.
