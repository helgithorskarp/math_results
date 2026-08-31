# Diagonally augmented two-torus reproduction of the abelian degree-six obstruction

## Result reproduced on an independent subfamily

Let (m,n\ge3), let (A=\mathbb Z_m\times\mathbb Z_n), and put

\[
X=\{\pm(1,0),\pm(0,1),\pm(a,b)\}.
\]

Assume that the three inverse pairs are distinct, so (X) has cardinality
six. Then the connected Cayley graph \(\operatorname{Cay}(A,X)\) has no exact
\(7\)-step dominating set of cardinality four or six.

This is a **partial independent reproduction**, not a novelty claim. It checks
the basis-plus-one-generator rank-two subfamily of the complete abelian
degree-six obstruction at repository commit `e96e080`. The direct-product
parameterization and both decisive algorithms here differ from the general
Hermite-normal-form computation, making this a compact targeted audit.

## Finite reduction

For \(\Sigma_7=\{x:d(0,x)=7\}\), an exact dominating set \(S\) makes the
translates \(s+\Sigma_7\), \(s\in S\), partition \(A\). Hence

\[
mn=|S||\Sigma_7|.
\]

Every distance-seven endpoint is the image of an integer coefficient triple
of Lee norm seven. The three-dimensional Lee shell has
\(4\cdot7^2+2=198\) vectors, so \(|\Sigma_7|\le198\) and \(mn\le1188\).
It is enough to take \(3\le m\le n\), since swapping the two factors preserves
the family. For every eligible pair, the enumerator takes one representative
of each inverse pair \(\{\pm(a,b)\}\), rejecting involutions and the two
coordinate pairs.

## Exact enumeration and independent check

The enumerator maps all 377 coefficient triples of Lee norm at most six and
all 198 triples of norm seven into each torus. It tests every counting case by
a complete compatibility-clique search on sphere-translate differences. The
result is

```text
radius=7
maximum_group_order=1188
dimension_pairs=2538
eligible_dimension_pairs=1644
raw_diagonal_elements=545614
admissible_inverse_pairs=539518
four_center_counting_candidates=80
six_center_counting_candidates=4351
four_center_tilings=0
six_center_tilings=0
```

The independent C++ checker rescans all 539,518 admissible inverse pairs. It
reconstructs each sphere by graph BFS rather than coefficient images, proves
that its complete candidate set equals the emitted set, and replaces the
difference clique by direct first-uncovered translate exact cover. It reports

```text
four_center_candidates_checked=80
six_center_candidates_checked=4351
four_center_tilings=0
six_center_tilings=0
```

The deterministic 4,431-line candidate file has SHA-256

```text
0ab0098b20198a06d8d905343fb210eb62116d18469ee2f811d2be41aff927c5
```

## Reproduction

Candidate files and command output belong under `/scratch`.

```bash
g++ -std=c++20 -O3 -DNDEBUG -march=native \
  -Wall -Wextra -Wpedantic \
  enumerate_diagonally_augmented_tori.cpp \
  -o /scratch/enumerate_diagonally_augmented_tori

g++ -std=c++20 -O3 -DNDEBUG -march=native \
  -Wall -Wextra -Wpedantic \
  check_diagonally_augmented_tori.cpp \
  -o /scratch/check_diagonally_augmented_tori

/scratch/enumerate_diagonally_augmented_tori \
  /scratch/diagonally_augmented_tori_candidates.txt

/scratch/check_diagonally_augmented_tori \
  /scratch/diagonally_augmented_tori_candidates.txt

sha256sum /scratch/diagonally_augmented_tori_candidates.txt
```

Fresh runs used GCC 12.2.0 on Debian 12. Source SHA-256 values are

```text
enumerate_diagonally_augmented_tori.cpp  6ecea89c9d1fd8bcc6428f388f864e14397e0f84479c7eb3c82f728e7460901b
check_diagonally_augmented_tori.cpp      192ef3ef1188ad7a64f21058da4038856fa1eb7a00347be73eca23b456f06b37
```

## Trust boundary

This is an exact computer-assisted partial reproduction. Its trust boundary
is the translate-partition and Lee-shell reduction, completeness of the
direct-product parameterization, inverse-pair enumeration, the two finite
implementations, and the compiler/runtime. All decisive operations use exact
integers. No heuristic, solver status, or external certificate enters the
claim.
