# Five-involution degree-seven obstruction for exact 7-step domination

## Result

Let \(\Gamma=\operatorname{Cay}(A,X)\) be a connected Cayley graph of a
finite abelian group, with \(X=-X\), \(0\notin X\), and \(|X|\le7\).
Suppose that if \(|X|=7\), then at least five members of \(X\) are
involutions. Then \(\Gamma\) has no exact \(7\)-step dominating set of
cardinality four or six.

The degree-at-most-six cases are supplied by the complete abelian
degree-six obstruction at repository commit `e96e080`. The new
exact-degree-seven orbit types are

\[
X=\{\pm g,u_1,u_2,u_3,u_4,u_5\}
\]

with five distinct involutions, and the elementary case of seven
involutions. This does not settle the degree-seven types with one or three
involutions, higher degree, nonabelian Cayley graphs, non-Cayley graphs, or
the value of \(m(7)\).

## Sharp finite reduction for five involutions

Put \(\Sigma_7=\{a:d(0,a)=7\}\). If \(S\) is an exact \(7\)-step
dominating set, its sphere translates partition \(A\), so

\[
|A|=|S||\Sigma_7|.
\]

In an abelian geodesic word, each involution is used at most once and the
letters \(g\) and \(-g\) cannot both occur. If exactly \(j\) involutions
occur, where \(0\le j\le5\), the remaining \(7-j\ge2\) letters have two
possible signs. Consequently

\[
|\Sigma_7|\le2\sum_{j=0}^5\binom5j=64,
\qquad |A|\le6\cdot64=384.
\]

## Complete binary-kernel parameterization

Let \(n=\operatorname{ord}(g)\), \(H=\langle u_1,\ldots,u_5\rangle\), and
define

\[
K=\left\{x\in\mathbf F_2^5:
\sum_{i=1}^5x_i u_i=0\right\}.
\]

The five involutions are nonzero and pairwise distinct exactly when

\[
e_i\notin K,
\qquad e_i+e_j\notin K\quad(i\ne j).
\]

Because \(H\) has exponent two, the intersection
\(\langle g\rangle\cap H\) has order one or two.

- In the split case it is trivial and
  \(A\cong C_n\oplus(\mathbf F_2^5/K)\).
- In the nonsplit case, \(n\) is even and there is a nonzero class
  \(v+K\) such that \((n/2)g=\sum v_i u_i\). Then

  \[
  A\cong
  \bigl(C_n\oplus(\mathbf F_2^5/K)\bigr)
  \big/\langle(n/2,v+K)\rangle.
  \]

Conversely every displayed model has the required marked generating set.
Thus the parameterization is exact, not merely a necessary-condition
relaxation. There are 374 binary subspaces of \(\mathbf F_2^5\), and exactly
32 satisfy the two distinctness conditions. Taking one representative of
each nonzero coset \(v+K\), the order/divisibility bound leaves

```text
split_models=1052
nonsplit_models=10796
```

The models are label-redundant under permutations of the five involutions,
which is harmless for completeness.

## Exact enumeration

The C++ enumerator constructs each finite group from its binary quotient and
possible cyclic-binary intersection, verifies that the displayed connection
set is simple of degree seven, computes the entire distance function by BFS,
and tests every counting case by a complete compatibility-clique search on
sphere-translate differences. It obtains

```text
radius=7
maximum_group_order=384
binary_subspaces=374
valid_relation_kernels=32
split_models=1052
nonsplit_models=10796
four_center_counting_candidates=0
six_center_counting_candidates=61
four_center_tilings=0
six_center_tilings=0
```

All 61 candidates are nonsplit, have \(n=24\), fall into five orbits under
permuting the involution labels, and have only two cyclic-fiber profiles.

## Independent full rescan

The Python checker independently generates every binary subspace using
canonical reduced row bases rather than closure of subspaces. It reconstructs
the same 32 valid kernels and all 11,848 finite models, recomputes every
sphere by BFS, and proves that its complete counting-candidate set equals the
emitted 61-line file. It replaces the difference-clique decision by memoized
first-uncovered translate exact cover with Python integer bitsets. It reports

```text
binary_subspaces=374
valid_relation_kernels=32
split_models=1052
nonsplit_models=10796
candidate_descriptors=61
candidate_permutation_orbits=5
candidate_cyclic_fiber_profiles=2
four_center_candidates_checked=0
six_center_candidates_checked=61
four_center_tilings=0
six_center_tilings=0
```

The deterministic candidate file has SHA-256

```text
6deeea42f7bcf277c6ab81f952ddfce5678a2731766ed0fd22ff5d9bbe925481
```

## Seven involutions

If all seven connection elements are involutions, a length-seven geodesic
must use every one exactly once, so \(|\Sigma_7|\le1\). A four- or six-center
tiling would force \(|A|\le6\), whereas a simple connection set containing
seven distinct nonzero elements forces \(|A|\ge8\). Hence this orbit type is
excluded without computation.

## Reproduction

Candidate files, bytecode, and command output belong under `/scratch`.

```bash
g++ -std=c++20 -O3 -DNDEBUG -march=native \
  -Wall -Wextra -Wpedantic \
  enumerate_degree7_five_involutions.cpp \
  -o /scratch/enumerate_degree7_five_involutions

/scratch/enumerate_degree7_five_involutions \
  /scratch/degree7-five-involution-candidates.txt

python3 check_degree7_five_involution_candidates.py \
  /scratch/degree7-five-involution-candidates.txt

sha256sum /scratch/degree7-five-involution-candidates.txt
```

Fresh complete runs used GCC 12.2.0 and Python 3.11.2 on Debian 12. Source
SHA-256 values are

```text
enumerate_degree7_five_involutions.cpp        9cb56f191094ff369e2ec65e5734966bda0acf7dab394895e022c3b669a98bc4
check_degree7_five_involution_candidates.py   470e0cbc471b9155f109c925e6df2e827a4d3250d5c6393904ea7c36208f2aaf
```

## Status, trust boundary, and novelty scope

This is an exact computer-assisted theorem. Its trust boundary is the
translate-partition and shell bound, completeness of the binary-kernel and
cyclic-intersection classification, the two exhaustive implementations, and
their compiler/runtime. The checker independently rescans the full finite
model universe and every candidate. All decisive operations use exact
integers; no heuristic, solver result, proof log, or external certificate is
used.

Targeted searches through 2026-08-31 found the foundational exact-step papers
and recent work using a different non-unique exact-distance convention, but
no prior degree-seven abelian obstruction of this form. The result is
therefore apparently new to the searched sources, not a priority claim.

- P. Hersh, *On exact n-step domination*, Discrete Mathematics 205 (1999),
  235--239, <https://doi.org/10.1016/S0012-365X(99)00024-2>.
- L. K. Williams, *On Exact n-Step Domination*, Ars Combinatoria 58 (2001),
  13--22,
  <https://combinatorialpress.com/article/ars/Volume%20058/volume-58-paper-2.pdf>.
- S. Das, S. Das, and A. Sadhukhan, *Exact-Distance Domination in Grid
  Graphs*, arXiv:2607.29648 (2026), <https://arxiv.org/abs/2607.29648>.
