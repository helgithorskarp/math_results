# Three-involution degree-seven obstruction for exact 7-step domination

## Exact computer-assisted theorem

Let

\[
\Gamma=\operatorname{Cay}(A,X),\qquad
X=\{\pm g_1,\pm g_2,u_1,u_2,u_3\},
\]

where (A) is a finite abelian group and (X) is a simple inverse-closed
connection set of cardinality seven. Thus the (u_i) are distinct nonzero
involutions and the two displayed inverse pairs are non-involutory and
distinct. Then (Gamma) has no exact (7)-step dominating set of cardinality
four or six.

Together with the previously verified complete degree-at-most-six and
five-involution degree-seven obstructions, this excludes every abelian Cayley
graph of degree at most seven whose degree-seven connection set contains at
least three involutions. The degree-seven type with exactly one involution,
higher degree, nonabelian Cayley graphs, non-Cayley graphs, and the value of
Hersh's (m(7)) remain open.

## Sphere and order reduction

Put

\[
\Sigma_7=\{a\in A:d_\Gamma(0,a)=7\}.
\]

If (S) is an exact (7)-step dominating set, then

\[
A=\bigsqcup_{s\in S}(s+\Sigma_7),
\qquad |A|=|S||\Sigma_7|.
\]

In an abelian geodesic word, an involution is used at most once and a
generator cannot occur together with its inverse. If exactly (j) of the
three involutions occur, the remaining coefficient pair has positive
\(\ell_1\)-norm (7-j), with at most (4(7-j)) possibilities. Therefore

\[
|\Sigma_7|
 \le \sum_{j=0}^3\binom3j4(7-j)
 =28+72+60+16=176.
\]

A four- or six-center example consequently has (|A|\le6\cdot176=1056).

## Complete marked-quotient parameterization

Let (U=\langle u_1,u_2,u_3\rangle) and

\[
K=\left\{v\in\mathbf F_2^3:\sum_i v_i u_i=0\right\}.
\]

Nonzeroness and pairwise distinctness of the (u_i) say that (K) contains
no vector of weight one or two. The only possibilities are

\[
K=0\quad\hbox{or}\quad K=\langle(1,1,1)\rangle.
\]

Write (V=\mathbf F_2^3/K\), so (|V|=8) or (4). Modulo (U\cong V), the
images of (g_1,g_2) give a finite quotient of (mathbf Z^2). Its kernel is
a full-rank lattice (L) with a unique column Hermite normal form

\[
H=\begin{pmatrix}a&x\\0&b\end{pmatrix},
\qquad a,b>0,\quad0\le x<a.
\]

For every (ell\in L), its image before quotienting by (U) lies in (U),
giving a homomorphism (phi:L\to V). Conversely, (K), (H), and the two
arbitrary values of (phi) on the HNF basis define the marked quotient

\[
A\cong
(\mathbf Z^2\oplus V)/
\langle(\ell,-\phi(\ell)):\ell\in L\rangle.
\]

These constructions are inverse. Hence this is a complete, unique marked
parameterization, not a restriction to split, Cartesian, or diagonal models.
It also gives (|A|=ab|V|). The number of index-(n) sublattices of
(mathbf Z^2) is (sigma_1(n)), so the two marked-universe counts have the
independent formulas

\[
64\sum_{n\le132}\sigma_1(n)=923584,
\qquad
16\sum_{n\le264}\sigma_1(n)=920400.
\]

## Production enumeration

The C++ program scans the full marked universe without a symmetry quotient.
It rejects exactly the models whose seven displayed connection elements are
not distinct and nonzero. It constructs the radius-seven sphere from all
images of mixed Lee/binary words: 416 words of length at most six and 176
words of length exactly seven. Every counting candidate is additionally
recomputed by graph BFS before it is emitted.

For a candidate, let (D=\Sigma_7-\Sigma_7). Two sphere translates with
shifts (s,t) are disjoint exactly when (s-t\notin D). After translating
one center to zero, a complete compatibility-clique search tests the remaining
three or five centers. Pairwise disjointness and the counting identity imply
coverage.

Two clean optimized runs produced byte-identical candidate files and the
following exact totals:

```text
kernel=0 marked_models=923584 degree_seven_models=902571 four_candidates=354 six_candidates=16312 four_tilings=0 six_tilings=0
kernel=7 marked_models=920400 degree_seven_models=907767 four_candidates=33 six_candidates=4226 four_tilings=0 six_tilings=0
radius=7
maximum_group_order=1056
marked_models=1843984
degree_seven_models=1810338
four_center_counting_candidates=387
six_center_counting_candidates=20538
four_center_tilings=0
six_center_tilings=0
```

The 20,925-line candidate file is deliberately generated under `/scratch`
rather than committed. Its SHA-256 is

```text
d964113cbb063cb071312b2be5f9bcd2caf9a26bb619b2851471b6320aa3ddc2
```

## Independent checker

The standard-library Python checker uses the divisor-sum formulas above and
independently rescans all 1,843,984 marked models for the two simplicity
counts. For every emitted candidate it then:

1. reconstructs the Cayley graph and its sphere by BFS rather than Lee-word
   aggregation;
2. checks the stated sphere size and translate-partition count; and
3. replaces the compatibility clique by memoized first-uncovered exact cover
   with arbitrary-precision Python bitsets.

Six deterministic worker processes checked all candidates and obtained

```text
radius=7
maximum_group_order=1056
kernel=0 marked_models=923584 degree_seven_models=902571 four_candidates_checked=354 six_candidates_checked=16312 four_tilings=0 six_tilings=0
kernel=7 marked_models=920400 degree_seven_models=907767 four_candidates_checked=33 six_candidates_checked=4226 four_tilings=0 six_tilings=0
candidate_descriptors=20925
```

The checker took about 26 wall-clock minutes and 51 aggregate CPU minutes on
the shared eight-CPU host. The optimized enumerator took about 124 seconds.
A full AddressSanitizer/UndefinedBehaviorSanitizer run took about 403 seconds,
reported no diagnostic, and emitted a byte-identical candidate file.

## Reproduction

All executables, candidate files, and command output belong under `/scratch`.

```bash
g++ -std=c++20 -O3 -DNDEBUG -march=native \
  -Wall -Wextra -Wpedantic \
  enumerate_degree7_three_involutions.cpp \
  -o /scratch/enumerate_degree7_three_involutions

/scratch/enumerate_degree7_three_involutions \
  /scratch/degree7-three-involution-candidates.txt

PYTHONDONTWRITEBYTECODE=1 python3 \
  check_degree7_three_involution_candidates.py \
  --jobs 6 --progress-every 1000 \
  /scratch/degree7-three-involution-candidates.txt

sha256sum /scratch/degree7-three-involution-candidates.txt
```

The sanitizer command is

```bash
g++ -std=c++20 -O1 -g \
  -fsanitize=address,undefined -fno-omit-frame-pointer \
  -Wall -Wextra -Wpedantic \
  enumerate_degree7_three_involutions.cpp \
  -o /scratch/enumerate_degree7_three_involutions_san

/scratch/enumerate_degree7_three_involutions_san \
  /scratch/degree7-three-involution-candidates-san.txt
```

Fresh runs used GCC 12.2.0 and Python 3.11.2 on Debian 12. Source SHA-256
values are

```text
enumerate_degree7_three_involutions.cpp       cc3e215785613756103424188f850af0fb0307a4cb2143a6d3c9ab5439b633f1
check_degree7_three_involution_candidates.py  efe3357e1a507e004b3162b2b0e51cf6f4c1e526269bedee08ff14e27e103b05
```

## Status, trust boundary, and literature scope

This is an exact computer-assisted theorem. The mathematical trust boundary
contains the sphere-translate reduction, the 176 shell bound, completeness of
the binary-kernel/HNF/gluing parameterization, and the equivalence of tiling
with the two exact search formulations. The computational boundary contains
the production enumeration's complete candidate selection, the two source
implementations, and their compiler/runtime. The checker independently
validates the full marked-universe and simplicity counts and every emitted
candidate; it does not independently rescan the radius-seven size of every
noncandidate model. All decisive operations use exact integers. No heuristic,
floating-point calculation, solver result, proof log, or external certificate
enters the theorem.

Targeted exact-phrase and concept searches through 2026-09-03 found the
foundational papers below and recent work using a different, non-unique
exact-distance convention, but no published classification of this marked
abelian degree-seven orbit type. The result is therefore apparently new to the
searched sources, not a historical-priority claim.

- P. Hersh, *On exact n-step domination*, Discrete Mathematics 205 (1999),
  235--239, <https://doi.org/10.1016/S0012-365X(99)00024-2>.
- L. K. Williams, *On Exact n-Step Domination*, Ars Combinatoria 58 (2001),
  13--22,
  <https://combinatorialpress.com/article/ars/Volume%20058/volume-58-paper-2.pdf>.
