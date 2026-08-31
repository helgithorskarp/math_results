# Abelian degree-five obstruction for exact 7-step domination

## Result

Let \(\Gamma=\operatorname{Cay}(A,X)\) be a connected Cayley graph of a
finite abelian group, where \(X=-X\), \(0\notin X\), and \(|X|\le5\). Then
\(\Gamma\) has no exact 7-step dominating set of cardinality 4 or 6.

This strictly extends the corrected degree-four obstruction. It does not
determine \(m(7)\): non-Cayley graphs, nonabelian Cayley graphs, and abelian
Cayley graphs of degree at least six remain possible.

## Reduction to the new degree-five cases

For the radius-7 sphere \(\Sigma_7\) about zero, an exact dominating set
\(S\) makes the translates \(\{s+\Sigma_7:s\in S\}\) partition \(A\). Thus

\[
|A|=|S||\Sigma_7|.
\]

An inverse-closed connection set of cardinality exactly five has one of three
forms.

1. Two non-involutory pairs and one involution. A geodesic of length 7 uses
   the involution zero or one time, giving
   \(|\Sigma_7|\le28+24=52\). Hence \(|A|\le6\cdot52=312\).
2. One non-involutory pair and three involutions. Each involution appears at
   most once in a geodesic, giving
   \(|\Sigma_7|\le2(1+3+3+1)=16\). Hence \(|A|\le96\).
3. Five involutions. A connected graph of this form has diameter at most 5,
   so \(\Sigma_7\) is empty.

The separately corrected degree-four computation covers \(|X|\le4\). The
program in this directory therefore enumerates only the genuinely new first
two forms.

## Complete enumeration

`enumerate_degree5_new_cases.cpp` generates every finite abelian group in
invariant-factor form through the relevant sharp order bound and every
cardinality-five inverse-closed connection set of the two nontrivial forms.
It uses a full, uncapped BFS to determine connectivity and all distances.
Group orders divisible by neither 4 nor 6 and invariant-factor ranks too large
for the listed generators are skipped by necessary conditions only.

Every counting candidate is tested by complete translate exact-cover
backtracking. Translation symmetry fixes one center at zero; each branch
takes the first uncovered group element and tries every sphere translate that
contains it. The exact summary is

```text
radius=7
maximum_group_order=312
invariant_factor_types=619
connection_sets_examined=3822979
connected_connection_sets=1681610
four_center_counting_candidates=702
six_center_counting_candidates=25304
four_center_tilings=0
six_center_tilings=0
```

These are the corrected counts. A radius-capped connectivity test would
incorrectly discard connected groups of eccentricity greater than 7 and
produce much smaller, incomplete totals.

The enumerator also writes one deterministic descriptor for each of the
26,006 counting candidates. The generated scratch file has SHA-256

```text
fc6793936a58390acfd60c4107296c6fd3d30eaecfd92e71d4ae788b35557503
```

`check_degree5_candidates.py` is an independent consumer of those
descriptors. It uses a different direct-product representation, recomputes
full connectivity and every radius-7 sphere, validates that each connection
set has cardinality five and satisfies the counting identity, and independently
runs a bit-set translate exact-cover search. It reports

```text
four_center_candidates_checked=702
six_center_candidates_checked=25304
four_center_tilings=0
six_center_tilings=0
```

The Python checker independently validates every candidate and every tiling
decision; completeness of candidate generation remains in the transparent
C++ invariant-factor and connection-set enumeration.

## Reproduce

Tested with GCC 12.2.0 and Python 3.11.2 on Debian 12.

```bash
g++ -std=c++20 -O2 -Wall -Wextra -Wpedantic \
  enumerate_degree5_new_cases.cpp \
  -o /scratch/enumerate_degree5_new_cases

/scratch/enumerate_degree5_new_cases \
  /scratch/degree5-new-candidates.txt

wc -l /scratch/degree5-new-candidates.txt
sha256sum /scratch/degree5-new-candidates.txt

python3 check_degree5_candidates.py \
  /scratch/degree5-new-candidates.txt
```

Source SHA-256 values:

```text
enumerate_degree5_new_cases.cpp  23f686ac65d1d12d5deb490cca4ab2b54c9b2351707774edcc800d547216ba97
check_degree5_candidates.py       6ba12fb3a22ac4c616fd3c5cdf581f44adc6d204ba6a0afc5bedb8a44dd9cc5f
```

## Status and trust boundary

This is an exact computational theorem, apparently new to the searched
sources rather than a claim of literature priority. The trust boundary is the
elementary sphere-size reduction, the corrected degree-four predecessor, the
invariant-factor and connection-set enumeration, the two implementations,
and their compiler/runtime. All calculations use exact integer or set
operations. No heuristic, SAT result, proof log, or external certificate
decoder enters the claim.

Primary context:

- P. Hersh, *On exact n-step domination*, Discrete Mathematics 205 (1999),
  235--239, DOI `10.1016/S0012-365X(99)00024-2`.
- L. K. Williams, *On Exact n-Step Domination*, Ars Combinatoria 58 (2001),
  13--22,
  <https://combinatorialpress.com/article/ars/Volume%20058/volume-58-paper-2.pdf>.

