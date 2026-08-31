# Four-involution degree-six obstruction for exact 7-step domination

## Result

Let \(\Gamma=\operatorname{Cay}(A,X)\) be a connected Cayley graph of a
finite abelian group, where \(X=-X\), \(0\notin X\), and \(|X|\le 6\).
Suppose that if \(|X|=6\), then at least four members of \(X\) are
involutions. Then \(\Gamma\) has no exact \(7\)-step dominating set of
cardinality \(4\) or \(6\).

The degree-at-most-five cases are supplied by the separately corrected and
independently checked predecessor computation. The new exact-degree-six case
is

\[
X=\{g,-g,u_1,u_2,u_3,u_4\},
\]

where \(g\ne-g\) and the \(u_i\) are four distinct involutions. If all six
members of \(X\) are involutions, connectivity gives diameter at most six, so
the radius-seven sphere is empty. Thus the theorem covers every degree-six
inverse-orbit type with at least four involutions.

This does **not** settle the two remaining exact-degree-six types (three
non-involutory pairs, or two pairs and two involutions), nonabelian Cayley
graphs, non-Cayley graphs, or the value of \(m(7)\).

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

In a geodesic word of length seven, an involution is used at most once and
the letters from \(\{g,-g\}\) cannot include both signs. If exactly \(j\) of
the four involutions occur, there are at most
\(2\binom{4}{j}\) possible group elements. Consequently

\[
|\Sigma_7|\le 2\sum_{j=0}^4\binom4j=32,
\qquad |A|\le 6\cdot32=192.
\]

The five displayed generators also imply that the invariant-factor rank of
\(A\) is at most five. These bounds make the class finite.

## Complete exact enumeration

`enumerate_degree6_four_involutions.cpp` performs the following steps.

1. Generate every finite abelian group of order at most 192 in
   invariant-factor form.
2. Losslessly skip orders divisible by neither 4 nor 6 and ranks greater than
   five.
3. For each group, choose one representative of every non-involutory inverse
   pair and every four-element subset of its nonzero involutions. This lists
   every connection set of the new type exactly once.
4. Test connectivity with the finite-abelian Frattini criterion: elements
   generate \(A\) exactly when their images span \(A/pA\) for every prime
   \(p\mid |A|\). The implementation uses exact modular Gaussian elimination.
5. For every generating set, recompute all distances by full BFS and extract
   \(\Sigma_7\).
6. For every case satisfying \(|A|=4|\Sigma_7|\) or
   \(|A|=6|\Sigma_7|\), run complete translate exact-cover backtracking.
   Translation symmetry fixes one sphere at zero. Every branch selects the
   first uncovered group element and tries every sphere translate containing
   it.

The exact output is

```text
radius=7
maximum_group_order=192
invariant_factor_types=371
raw_connection_set_descriptions=10237220
generating_connection_sets=2749460
four_center_counting_candidates=0
six_center_counting_candidates=8960
four_center_tilings=0
six_center_tilings=0
```

The enumerator writes deterministic descriptors for the 8,960 counting
candidates. The generated scratch file has SHA-256

```text
48a2e1babbea8778f7e8401e6d66252c55432dcf23ecdd648296805f511b97c1
```

## Independent candidate checker

`check_degree6_four_involution_candidates.py` is an independent consumer of
the descriptor file. It uses tuple coordinates rather than the enumerator's
mixed-radix arithmetic, independently regenerates the 371 invariant-factor
types and the raw count 10,237,220, validates the inverse-orbit form, performs
a full connectivity BFS, recomputes every radius-seven sphere, rechecks the
counting identity, and repeats exact cover with Python integer bitsets and a
memoized search. It reports

```text
invariant_factor_types=371
raw_connection_set_descriptions=10237220
candidate_descriptors=8960
four_center_candidates_checked=0
six_center_candidates_checked=8960
four_center_tilings=0
six_center_tilings=0
```

The checker independently validates every emitted candidate and tiling
decision. Completeness of selecting the 8,960 candidates from the 2,749,460
generating sets remains in the transparent C++ enumerator; the Python checker
does not independently rescan that full universe.

## Reproduction

Tested with GCC 12.2.0 and Python 3.11.2 on Debian 12.

```bash
g++ -std=c++20 -O3 -DNDEBUG -march=native \
  -Wall -Wextra -Wpedantic \
  enumerate_degree6_four_involutions.cpp \
  -o /scratch/enumerate_degree6_four_involutions

/scratch/enumerate_degree6_four_involutions \
  /scratch/degree6-four-involution-candidates.txt

sha256sum /scratch/degree6-four-involution-candidates.txt

python3 check_degree6_four_involution_candidates.py \
  /scratch/degree6-four-involution-candidates.txt
```

Source SHA-256 values:

```text
enumerate_degree6_four_involutions.cpp       cd8079bd7af50c4c7ec46a4e485f98cfb12aba293410b37cc4385daf6de057e9
check_degree6_four_involution_candidates.py  eeacab248b3418440f9d0e9bed298589f2b0d1a31c09ae0ca1b3178c9b38dc28
```

## Status, trust boundary, and novelty scope

This is an exact computer-assisted theorem. It depends on the elementary
sphere and order reduction, the classification of finite abelian groups, the
finite-abelian prime-quotient generation criterion, completeness of the C++
enumeration, the two implementations, and their compiler/runtime. All graph,
modular-rank, and exact-cover operations are exact. No SAT solver, heuristic,
proof log, or external certificate decoder enters the claim.

Targeted searches through 2026-08-31 for exact 7-step domination and
Cayley/abelian variants found no prior version of this obstruction. The result
is therefore apparently new to the searched sources, not a claim of
literature priority.

Primary context:

- P. Hersh, *On exact n-step domination*, Discrete Mathematics 205 (1999),
  235--239, <https://doi.org/10.1016/S0012-365X(99)00024-2>.
- L. K. Williams, *On Exact n-Step Domination*, Ars Combinatoria 58 (2001),
  13--22,
  <https://combinatorialpress.com/article/ars/Volume%20058/volume-58-paper-2.pdf>.

The corrected degree-four and verified degree-five source directories are
`exact_7_step_domination_degree4_correction` and
`exact_7_step_domination_degree5_uncapped` in this repository.
