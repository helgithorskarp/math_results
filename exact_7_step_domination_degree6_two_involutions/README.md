# Involutory degree-six obstruction for exact 7-step domination

## Result

Let \(\Gamma=\operatorname{Cay}(A,X)\) be a connected Cayley graph of a
finite abelian group, where \(X=-X\), \(0\notin X\), and \(|X|\le 6\).
Suppose that if \(|X|=6\), then \(X\) contains an involution. Then
\(\Gamma\) has no exact \(7\)-step dominating set of cardinality \(4\) or
\(6\).

The degree-at-most-five cases and the exact-degree-six cases with four or six
involutions are supplied by predecessor computations. The new case is

\[
X=\{g,-g,h,-h,u,v\},
\]

where \(g\ne-g\), \(h\ne-h\), the two inverse pairs are distinct, and
\(u,v\) are distinct involutions. Since a six-element inverse-closed set has
an even number of involutions, the combined theorem covers every degree-six
type containing any involution.

This leaves only the exact-degree-six type
\(X=\{\pm g,\pm h,\pm k\}\), with three non-involutory inverse pairs. It
does not settle nonabelian Cayley graphs, non-Cayley graphs, or the value of
\(m(7)\).

## Finite reduction

Write

\[
\Sigma_7=\{a\in A:d(0,a)=7\}.
\]

If \(S\) is an exact \(7\)-step dominating set, the translates
\(\{s+\Sigma_7:s\in S\}\) partition \(A\). Hence

\[
|A|=|S|\,|\Sigma_7|.
\]

In an abelian geodesic word, an involution cannot occur twice and a generator
cannot occur together with its inverse. If a length-seven geodesic uses
exactly \(j\) of \(u,v\), its remaining coefficient pair has
\(\ell_1\)-norm \(7-j\). The number of integer pairs of positive
\(\ell_1\)-norm \(r\) is \(4r\). Therefore

\[
|\Sigma_7|
 \le 4\cdot7+2(4\cdot6)+4\cdot5
 =96,
\qquad
|A|\le 6\cdot96=576.
\]

The four displayed generators also imply that the invariant-factor rank of
\(A\) is at most four. These bounds make the class finite.

## Complete exact enumeration

`enumerate_degree6_two_involutions.cpp` performs the following steps.

1. Generate every finite abelian group through order \(576\) in
   invariant-factor form.
2. Apply only the necessary order-divisibility and rank filters.
3. Choose every two-element subset of non-involutory inverse-pair
   representatives and every two-element subset of nonzero involutions. This
   lists each connection set of the new type exactly once.
4. Test generation with the finite-abelian Frattini criterion. At every odd
   prime, the involutions vanish in \(A/pA\), so \(g,h\) must span. At
   \(p=2\), the images of \(g,h,u,v\) must span. The code evaluates these
   conditions by exact modular arithmetic.
5. After generation is established independently, run a radius-limited BFS
   to extract exactly \(\Sigma_7\). Connectivity is **not** inferred from
   this capped search; this separation avoids the defect found in the
   original degree-four computation.
6. For every case satisfying \(|A|=4|\Sigma_7|\) or
   \(|A|=6|\Sigma_7|\), run complete translate exact-cover backtracking.
   Translation symmetry fixes one sphere at zero, and each branch uses the
   first uncovered element.

The exact output is

```text
radius=7
maximum_group_order=576
invariant_factor_types=1193
raw_connection_set_descriptions=144757815
generating_connection_sets=45774807
four_center_counting_candidates=2304
six_center_counting_candidates=691422
four_center_tilings=0
six_center_tilings=0
```

The enumerator writes 693,726 deterministic candidate descriptors. The
generated scratch file has SHA-256

```text
25c904686673d4ad164edd43d7840558cbb215e7940617985f29189cd7a433ce
```

## Independent candidate checker

`check_degree6_two_involution_candidates.cpp` is an independent consumer of
the descriptor file. It separately regenerates the 1,193 invariant-factor
types and raw count 144,757,815, validates canonical inverse-pair and
involution descriptions, and rejects duplicate or noncontiguous descriptors.
For every emitted candidate it performs a **full** connectivity BFS and
recomputes the radius-seven sphere and counting identity.

Its tiling algorithm is deliberately different. If \(D=\Sigma_7-\Sigma_7\),
then two translates with shift difference \(a\) are disjoint exactly when
\(a\notin D\). After fixing one shift at zero, a \(k\)-translate tiling is
therefore equivalent to a \((k-1)\)-clique in the allowed-difference graph on
\(A\setminus D\): the counting identity \(|A|=k|\Sigma_7|\) turns pairwise
disjointness into coverage. The checker uses exact fixed-size bitsets for this
clique search and does not reuse the enumerator's exact-cover recursion.

It reports

```text
invariant_factor_types=1193
raw_connection_set_descriptions=144757815
candidate_descriptors=693726
four_center_candidates_checked=2304
six_center_candidates_checked=691422
four_center_tilings=0
six_center_tilings=0
```

The checker independently validates every emitted candidate and tiling
decision. Completeness of selecting the 693,726 candidates from the
45,774,807 generating connection sets remains in the transparent C++
enumerator; the independent checker does not rescan the full raw
universe.

`check_degree6_two_involution_candidates.py` supplies a third,
standard-library implementation using tuple coordinates, full BFS, and Python
integer-bitset exact cover. Its factor blocks can run in parallel. It is
included for further reproduction, but the complete verification reported
above is the faster difference-graph checker; no claim in this document
depends on completing the supplementary Python run.

## Reproduction

Tested with GCC 12.2.0 and Python 3.11.2 on Debian 12. Generated descriptors
and command output belong under `/scratch` and are not repository artifacts.

```bash
g++ -std=c++20 -O3 -DNDEBUG -march=native \
  -Wall -Wextra -Wpedantic \
  enumerate_degree6_two_involutions.cpp \
  -o /scratch/enumerate_degree6_two_involutions

g++ -std=c++20 -O3 -DNDEBUG -march=native \
  -Wall -Wextra -Wpedantic \
  check_degree6_two_involution_candidates.cpp \
  -o /scratch/check_degree6_two_involution_candidates

/scratch/enumerate_degree6_two_involutions \
  /scratch/degree6-two-involution-candidates.txt

wc -l /scratch/degree6-two-involution-candidates.txt
sha256sum /scratch/degree6-two-involution-candidates.txt

/scratch/check_degree6_two_involution_candidates \
  /scratch/degree6-two-involution-candidates.txt
```

Source SHA-256 values:

```text
enumerate_degree6_two_involutions.cpp  65f3166d43412ac723e4269ec6b9bdba795580077400870ad29c1534e1a8e300
check_degree6_two_involution_candidates.cpp  9cca3f23409d9d0eeb9aa97684dc4cfe3fc3fd4082dc48428f770b72b34d2f08
check_degree6_two_involution_candidates.py  29ef331e750937b3b6c5ec3529898a7e058b64a13d7bccfce349ebfc89bedabc
```

## Status, trust boundary, and novelty scope

This is an exact computer-assisted theorem. It depends on the elementary
sphere and order reduction, finite-abelian classification and generation
criterion, completeness of the C++ enumeration, the two implementations,
and their compiler/runtime. All graph, modular-rank, exact-cover, and
difference-clique operations are exact. No SAT solver, heuristic result, proof
log, or external certificate decoder enters the claim.

Targeted searches through 2026-08-31 for exact 7-step domination and
Cayley/abelian variants found no prior version of this obstruction. The
result is therefore apparently new to the searched sources, not a claim of
literature priority.

Primary context:

- P. Hersh, *On exact n-step domination*, Discrete Mathematics 205 (1999),
  235--239, <https://doi.org/10.1016/S0012-365X(99)00024-2>.
- L. K. Williams, *On Exact n-Step Domination*, Ars Combinatoria 58 (2001),
  13--22,
  <https://combinatorialpress.com/article/ars/Volume%20058/volume-58-paper-2.pdf>.

The corrected degree-four, verified degree-five, and four-involution
degree-six source directories are adjacent directories in this repository.
