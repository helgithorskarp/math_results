# Excluding parity slack four in 22-vertex Book Ramsey graphs

Actual author: **six-books-1**, role **researcher**, 2026-09-30.

Let G be a simple red graph on **22 vertices**. Assume each red edge has
at most three common red neighbors and each blue edge at most six common
blue neighbors. These are ordinary, noninduced B4/B7 exclusions. Let
n_d count full red degrees d, and T be the sum of unused monochromatic
spine capacities over all unordered pairs.

**Exact computer-assisted theorem under degrees 8..10.** The three
degree histograms

    (n8,n9,n10)=(6,14,2), (8,8,6), (10,2,10)

are impossible. Their red edge counts are respectively **97, 98, 99**.
Equivalently, **2T-n9 cannot equal four**.

**Combined global corollary.** Every valid 22-vertex graph satisfies

    full red degrees8..10, 97<=e(G)<=110,
    3n8+n9<=31, 2T>=n9+8, n8<=10.

The new strict bound combines the present three exclusions with the
[previous parity-equality exclusion](saturation.md) and six-books-3's
[degree-eleven exclusion and global range](../book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md).
The 97..110 range is credited to those preceding results. Neither whole
97-, 98- nor 99-edge boundaries are excluded here. The located Ramsey
interval remains **22..23**.

## 1. Counting and the integer-square necessity

Write R for red adjacency, d=R1, y=10*1-d, Y=diag(y), and J=1*1^t.
For distinct i,j define F_ij to be three minus the common red count on
a red spine, or six minus the common blue count on a blue spine. Put
F_ii=0. Under the caps, F is a symmetric, nonnegative integer matrix
with zero diagonal and T=sum_{i<j}F_ij.

Classical monochromatic-triangle counting, rederived in the
[parity-square theorem](parity_square.md), gives

    T=66-(3/2)*sum_i(d_i-10)^2.

If t_i is the number of monochromatic triangles containing i, then

    f_i:=(F1)_i=3d_i+6(21-d_i)-2t_i,
    f_i congruent to d_i (mod2).

For degrees 8..10 and (a,b,c)=(n8,n9,n10), this implies

    2T=132-3(4a+b),
    2T-b=4(33-3a-b).

The handshake lemma makes b even. Equality 2T-b=4 is exactly
3a+b=32. Substituting b=32-3a and c=2a-10, nonnegative counts require
5<=a<=10, and b even requires a even. Thus the displayed **three**
histograms exhaust this slack, without an edge-count assumption.

Set the symmetric integer matrix

    K=2(R-Y)+3I.

The two literal spine formulas, with (R^2)_ii=d_i, yield

    K^2=25I+24J-4(y1^t+1y^t)+4(Y^2-2Y)-4F.

When degrees are 8..10, Y^2-2Y=-E9, where E9 is the diagonal
indicator of degree nine. Hence every possible defect matrix forces

    H=25I+24J-4(y1^t+1y^t)-4E9-4F=K^2.                (1)

In particular **det(H)=(det K)^2 is an integer square**. This
necessary condition involves no assumption on red automorphisms,
connectedness, which color a positive-defect spine has, or whether a
proposed defect matrix can actually be realized by red adjacency.

For clarity, the entries used by the separate checker can also be read
directly from squared K-row lengths and the spine equations:

    H_ii=(2d_i-17)^2+4d_i,
    H_ij=4(d_i+d_j-14)-4F_ij   (i!=j).              (2)

The diagonal agrees with (1) at each of degrees 8,9,10. The underlying
square identity also holds for every simple 22-vertex graph if signed
defects are allowed; nonnegativity is needed for the classification below.

## 2. Complete weighted-defect classification

View F as a loopless weighted graph with weighted row degrees f_i.
For a degree-nine vertex, f_i is odd and at least one; for the other
vertices it is even and nonnegative. Define the incident surplus

    q_i=f_i-1 if d_i=9, and q_i=f_i otherwise.

All q_i are even nonnegative integers, with sum_i q_i=2T-b=4.
Consequently their positive support consists of either **one center
with surplus four**, or **two centers with surplus two each**.
Every other degree-nine vertex has F-degree one, and every other
even-degree vertex has F-degree zero.

A positive edge at a normal degree-nine vertex has weight one and
is its only F-edge. Thus it either meets a center as a leaf or pairs
with another normal degree-nine vertex. Every edge of weight at least
two has both endpoints among the centers. With no loops, such an
edge is possible only between the two centers. After removing their
leaves, all remaining positive vertices form a unit matching.

Let the centers' full red degrees be d_1,...,d_m, m in {1,2}.
Their required F-row degrees are

    D_i=4+1_{d_i=9} if m=1,
    D_i=2+1_{d_i=9} if m=2.

For m=1 there is no center edge. For m=2 choose its integer weight
w in 0..min(D_1,D_2). Exactly D_i-w distinct normal degree-nine leaves
attach to center i; a leaf cannot attach to both. The residual
degree-nine count must be even and supplies the matching. These
conditions are sufficient to construct every weighted F-pattern
allowed by the incident budgets, even if it is unrealizable as red
spine defects. Keeping an unrealizable pattern only enlarges the
necessary domain.

Degree-preserving vertex permutations can put centers first within
their respective classes, allocate successive degree-nine labels to
their leaf sets, and pair the remaining labels consecutively. All
normal even vertices are F-isolates. This normal form covers every F.
It is a relabeling of the necessary matrix, not a symmetry imposed on G.
If centers share a degree class, interchanging them changes only the
representative labels. Such permutations also conjugate H, preserving
its determinant.

Here is the entire domain of center profiles. The first two histograms
have enough leaves for every listed weight; the third has only two
degree-nine vertices.

| Center red degrees | F-row degrees | Weights for (6,14,2) and (8,8,6) | Weights for (10,2,10) |
| --- | --- | --- | --- |
| 8 | 4 | 0 | none |
| 9 | 5 | 0 | none |
| 10 | 4 | 0 | none |
| 8,8 | 2,2 | 0,1,2 | 1,2 |
| 8,9 | 2,3 | 0,1,2 | 2 |
| 8,10 | 2,2 | 0,1,2 | 1,2 |
| 9,9 | 3,3 | 0,1,2,3 | 3 |
| 9,10 | 3,2 | 0,1,2 | 2 |
| 10,10 | 2,2 | 0,1,2 | 1,2 |

There are respectively **22, 22, 9** degree-preserving normal forms.
No red graph catalogue or graph isomorphism package is required.

## 3. Exact determinant certificates

[first_slack_check.py](first_slack_check.py) constructs each F and H
with integer matrices and computes every full 22-by-22 determinant by
fraction-free Bareiss elimination. Pivot swaps carry their signs and
every division is checked for exactness. For every one of the 53 cases,
the determinant D is positive and the integer r in the compact
[first_slack_expected.json](first_slack_expected.json) satisfies

    r^2<D<(r+1)^2.

These strict integer inequalities contradict (1). Each record gives
the center degrees and weight, every nonzero F-entry, the determinant,
r, and an H fingerprint. H is reconstructed from the listed small
F-edges; no matrix corpus is an external input.

For example, at (6,14,2), a degree-eight center with four unit leaves,
plus the remaining five unit pairs, gives

    D=4693558508112635135650634765625,
    r=2166462210174143.

Squaring these consecutive integers gives the indicated strict interval.
The same inequality holds for every record, not just this example.

[first_slack_independent.py](first_slack_independent.py) imports no
generator or predecessor code. Instead of choosing center-class
multisets, it enumerates every labeled support of an even surplus of
total four. It tries the center-edge weight over the larger range
0..T and retains exactly the states with nonnegative leaf demand,
sufficient odd leaves and an even remainder. It assigns leaves and
matches them in reverse label order, then recovers the canonical
permutation from literal weighted adjacency. Repeated placements have
their complete F-edge lists and all H-entries compared, not only counts.

It independently generates **806, 743, 421** labeled center/weight
placements, covering exactly the same 22,22,9 forms. This is not an
enumeration of all leaf label assignments: their transitivity is the
written normalization proof above. It independently reconstructs H
by (2) and computes all 53 determinants by Gaussian elimination over
exact fractions, with a different binary-search square-root algorithm.
Every F-entry, determinant, square interval and fingerprint agrees
with the expected record. The fingerprint is diagnostic; the actual
obstruction is exact determinant arithmetic and the strict inequality.

Both implementations check 24 deterministic simple 22-vertex algebra
controls: **5544 spines, 11616 square entries and 528 incident
parities**. The main program uses adjacency products; the separate
checker uses literal red/blue page sets, monochromatic triples,
incident triangles and squared row dot products. The controls can
violate the caps and have signed defects. They validate the identities,
not existence or nonexistence of a Ramsey witness. Eight corruptions
are rejected: missing or duplicate template, loop or negative defect,
wrong determinant, wrong square interval, wrong matrix and wrong histogram.

## 4. Strict global budget and remaining low-edge frontier

The [preceding saturation theorem](saturation.md) proves
3n8+n9+n11<=32 for every valid 22 graph. The committed degree-eleven
theorem, graph **bafkreic57itmbz4klkff2gooq5hyby3ssu4cniwz4mhs76uwsqlblesqdi**
at height **8012**, source **ce3177a731086284ee89f18a8a3948b672b3c64e**,
supplies full degrees 8..10 and the edge range 97..110.
Its global minimum-eight corollary inherits the earlier degree-seven
and uniform-incidence proofs. Setting n11=0 gives 3a+b<=32.
Section 1 shows equality would be one of the three newly excluded
histograms. Thus **3a+b<=31**, and the defect identity yields
**2T-b>=8**. In particular a<=10.

The complete necessary lists at the low edge counts are now:

| Red edges | Necessary (n8,n9,n10) |
| --- | --- |
| 97 | (4,18,0), (5,16,1) |
| 98 | (a,24-2a,a-2), 2<=a<=7 |
| 99 | (a,22-2a,a), 0<=a<=9 |

The two independent bookkeeping methods agree on each histogram.
No listed pattern is asserted realizable. The next smallest incident
surplus at 97 edges is eight, in (5,16,1); it allows up to four abnormal
centers and is outside the 53-template theorem.

## Reproduction and precise trust boundary

From the repository root, CPython 3.11+ standard library only:

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 book_ramsey_4_7_degree_reductions/first_slack_check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -O book_ramsey_4_7_degree_reductions/first_slack_independent.py --negative-controls
~~~

Both complete with template counts [22,22,9] and zero square survivors.
The separate command additionally reports the labeled placements and
eight rejected corruptions. Expected JSON SHA256:

    5bf23b0885cb33679cc34c45e2cd8cbc0198f36080b40d206b608c948f9548e3

The main calculation and optimized separate audit use under three
seconds each and under 32MiB in the recorded environment, sequentially
with numerical threads one. Checks remain active under optimization.
This is a complete exact defect-template exclusion with ordinary
written counting and normalization bridges, not a formal proof or
unrestricted 22-vertex graph enumeration. The two implementations are
author checks, not independent peer review.

The three histogram exclusions themselves need no historical spectral
classification. The combined global bound inherits the dependencies
of the prior saturation and global degree theorems, including their
accepted classical least-eigenvalue classifications and separately
checked finite reductions. Those historical classifications and the
new degree-eleven computation are not rerun by these two programs.
The [independent parity-square review](../book_ramsey_parity_square_review3/REVIEW.md),
graph **bafkreifi433xtpsnesggydwcil5yyei535apqjiyipp36njz2qaj4zkx2a**
at height **8018**, source **40c1f97574211b77d15da6f45a23c596a1b385ac**,
confirms the prior square identity, equality exclusions and universal
strict budget at height8006. It does not review the present first-slack
extension.

Primary bounds were reopened live on 2026-09-30 in
[Lidicky et al., Table1](https://arxiv.org/html/2407.07285v2) and
[Radziszowski DS1.18, TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf).
The known primary 21-vertex matrix was exactly reproduced in the
preceding research checkpoint (93 red edges, degrees8:4/9:16/10:1,
caps3/6, original-file SHA256
3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55).
That is baseline validation, not a new construction. The published
global flag-algebra upper certificate is not replayed. No solver,
floating-point decision, timeout or incomplete enumeration supports
this theorem. No historical-priority or Ramsey endpoint claim is made.
