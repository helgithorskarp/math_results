# The 119-edge character617 theorem

Actual author **six-vdw-3**, role **researcher**, 2026-10-03. This is an
author-checked exact finite theorem with two distinct implementations.
The ordinary mathematical reductions are unformalized; independent-person
review of this new theorem is pending.

## Statement and graph

Let S and T be the nonzero square and nonsquare classes of F_617. For
d in {285,314,362,381,409,570}, take the endpoint support
{1+j*d : 1 <= j <= 6}, with field arithmetic. Their supports are respectively

```
192 239 286 477 524 571
12 23 34 315 326 337
108 215 322 363 470 577
55 146 291 382 436 527
195 202 403 410 604 611
336 383 430 477 524 571
```

All entries are nonsquares. Their union V has size 33, V and V^-1 are
disjoint, and D = V union V^-1 has size 66. The bipartite graph G joins
q in S to t in T exactly when t/q belongs to D. Both sides have 308
vertices, each of degree 66. For selected sets A,B, M(A,B) denotes the
number of missing cross-pairs.

**Theorem.** If |A|=10 and |B|=14, then M(A,B)>=21, or equivalently
the selected subgraph has at most **119 edges**.

**Coloring corollary.** For an AP7-free coloring of [1,N], N>=3702,
relative to one constant-phase affine quadratic character of prime 617,
a nonempty actual nonroot flip support of size 24 has character-class
balance **11/13 or 12/12**. Original root occurrences are independently
free. Additional edits may vary between integer occurrences in a residue
column. A flip column must actually change a point; a merely declared free
column is not counted. The theorem makes no assertion that either surviving
balance is feasible, gives no 25-flip lower bound, and produces no coloring
of [1,3704]. Here W(2,7) means two colors and seven terms.

## Actual-position bridge and prior results

[Lemma 9880](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/character617-flip-rigidity/PROOF.md)
proves the interval lift. For an actual changed nonroot point q and a
transformed endpoint step delta in {1,...,616}, use its forward seven-term
progression if q+6*delta<=N. Otherwise the backward endpoint progression
with positive step 617-delta begins at q+6*delta-3702>N-3702>=0.
Its residues are the same seven field points in reverse order. Thus every
nonconstant field endpoint progression used here has an actual interval
representative at the changed point. All six endpoints avoid the original
root. If all six were unchanged, the changed point and endpoints would be
monochromatic. Each demand therefore supplies another selected flip column.
The first five displayed supports are disjoint, giving five distinct
opposite-character selected outneighbors per flip. V intersect V^-1 is
empty, so no two arcs have the same underlying edge in opposite directions.

Consequently m actual nonroot flips require at least 5*m graph edges. A
24-flip 10/14 balance would require 120 edges and M<=20, contrary to the
theorem. Scalar normalization by a selected field row is used only on this
necessary ratio graph; it is not a quotient of actual interval colorings.
Since D=D^-1, exchanging character classes preserves this field graph.

[Lemma 9904](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/character617-dense-support/PROOF.md)
and independent
[review 9964](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/dense617-audit/PROOF.md)
exclude K5,9, K6,7 and K7,6. The new complete threshold-four computation
here independently checks no K5,9. Review 9964's 107-edge 10-by-12 bound
is context and supplies no numerical cut in this proof.
[Lemma 9940](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/character617-quantized-support/PROOF.md)
proves at least 24 actual nonroot flips when the support is nonempty.
Independent
[review 9976](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/quantized617-audit/REVIEW.md)
checks that new exclusion relative to the explicit 9880/9904 premises and
separately proves that a size-24 support can have only 10/14, 11/13 or
12/12 balance. Combining its three-balance cover with the new theorem
gives the coloring corollary. Earlier reviews do not certify this theorem.

## Complete least-five-row cover

Assume for contradiction M<=20. Choose A0 as five least-missing rows among
the ten selected rows and write S5 for their total missing count. If the
fifth degree is <=1, S5<=5 and at least 14-S5>=9 selected columns are common,
contrary to no K5,9. If the fifth degree is >=3, the remaining five rows
contribute at least 15; hence S5<=5, with the same contradiction. Thus the
fifth degree is exactly 2, all five prefix degrees are <=2, and every
additional selected row has degree >=2. In particular 6<=S5<=10.

Let C be the ENTIRE common neighborhood of A0 and B0=B intersect C. Then
|C|<=8 and |B0|>=14-S5>=4. Multiply by the inverse of an A0 row to anchor
one row at 1, retaining every physical label and all degree ties.
[COVER.md](COVER.md) gives the complete independently checked threshold-four
domain, exact singleton-capacity reduction and C4/C5 exclusions. They leave
620 possible prefixes and **3,400 labeled cores (A0,B0)**, with |C| in
{6,7,8} and |B0|>=5. Each core uses the whole C, rather than its selected
subset, to define the outside-column domain.

## Allocated scores and complete row-subset coefficients

For a core put k=14-|B0| and g(q)=missing degree from q into B0, for
q in S outside A0. For t in T outside the ENTIRE C, let d0(t) be its
positive missing degree into A0. Define

```
h(q) = 5*g(q) + min_{U subset T\C, |U|=k}
                         sum_{t in U} [d0(t)+5*1_(q not adjacent to t)].
```

For A'=A\A0 and U=B\C, distributing the A0-U cost across the five
added rows gives sum_{q in A'} h(q)<=5*M<=100. Independent optimizing
sets U may differ between rows. This is a necessary relaxation, not a
construction of a common U.

The producer uses Euler characters and row bitmasks. Adjacent-column costs
are <=5 and nonadjacent-column costs >=6; each row has at least
66-|C|>=58 adjacent outside columns, more than k<=9. Thus its cheapest
k columns are adjacent. The checker independently uses square sets and
Euclidean inverses, constructs all actual outside-column costs and sorts
the full physical list, without assuming the producer's shortcut.

Every one of the 303 physical added-row scores in every core is checked.
The coefficient of z^5 and x-degree <=100 in

```
product_{q in S\A0} (1+z*x^h(q))
```

counts exactly the permitted labeled five-row subsets. The producer groups
equal scores with binomial coefficients. The checker multiplies all 303
individual factors using nonnegative reduced costs h(q)-min(h) and budget
100-5*min(h). Larger reduced degrees cannot contribute a permitted five-row
monomial. The two complete computations agree in normal and optimized
Python. The counts are labeled (A0,B0,A') incidences, not distinct supports,
feasible colorings or symmetry orbits.

| Full C | B0 | All cores | Surviving cores | Five-row choices |
| --- | --- | ---: | ---: | ---: |
|6|5|480|450|543660|
|6|6|415|355|159150|
|7|5|420|350|194110|
|7|6|700|420|103770|
|7|7|180|70|1510|
|8|5|560|480|883270|
|8|6|420|290|141990|
|8|7|200|90|6110|
|8|8|25|5|20|

The total is **2,510 surviving cores and 2,033,590 row choices**. Their
canonical row-score/coefficient record digest is
`3ef4aded675b0c98bba22df7ae280b5623b2429a8906bedc26cbf2afa8d87ddd`.

## Exact relaxed column minima and contradiction

For fixed A=A0 union A' and B0, a real completion selects k distinct
columns from T\C. Its missing count is at least

```
sum_{q in A'} g(q) + sum of the k smallest d_A(t), t in T\C,
```

where d_A(t) counts all ten selected rows missing t. This is the exact
minimum after relaxing the prefix's capacity and least-row ordering
constraints. The relaxation can admit more completions, so a lower bound
above 20 remains a valid exclusion.

The producer visits all five-row subsets with score sum <=100, pruning
only by increasing remaining-score sums. Four binary bit planes compute
all ten-row outside-column deficits. The checker imports neither the
enumeration nor that counter. It reconstructs literal column-to-row
adjacency and computes each column's deficit by population count. It
checks legality, strict tuple order, uniqueness, every row score, every
physical column and the exact minimum. Equality of its row-list size with
the separately proved five-factor coefficient certifies completeness.

The full domain is partitioned into 113 disjoint batches of at most 20,000
choices, with all 3,400 cores appearing once. All **2,033,590 choices** have
been checked. No relaxed completion has missing count <=20.

| Full C | B0 | Conditional minimum |
| --- | --- | ---: |
|6|5|28|
|6|6|28|
|7|5|29|
|7|6|28|
|7|7|30|
|8|5|29|
|8|6|29|
|8|7|29|
|8|8|33|

The full histogram is
28:190;29:2700;30:19390;31:59610;32:124770;33:211090;34:301710;
35:362650;36:362940;37:290180;38:179940;39:84020;40:28450;
41:5410;42:500;43:40. The canonical summary digest is
`8a50a21c3f6527e40fcc9a475a3db25d97dde55c96bb80eed916634cc0ae1a6b`.
The empty residual digest is
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`.
These digests summarize full exact checks, rather than replacing them.

A hypothetical M<=20 subgraph has a normalized least-five prefix in the
complete cover. Its actual added rows belong to the complete allocated
domain. Its exact relaxed column minimum would exceed 20 while being at
most its actual M, a contradiction. This proves **M>=21 and E<=119**.
The computed minimum 28 is conditional on the hypothetical M<=20 cover
and allocated-score domain; it is **not** a universal M>=28 assertion.

## Validation, reproducibility and literature

The complete cold replay regenerates the cover, all coefficients and all
column minima. The two implementations compare whole records in ordinary
and optimized Python. Fourteen repaired-digest semantic damages per mode
exercise actual row and minimum records; three valid controls per mode
pass. All 9,720 complete small weighted five-row coefficient fixtures use
literal-subset oracles, and all 4,096 three-row/four-column binary matrices
check the counter. COVER.md describes the separate earlier cover controls.

Run `python3.11 reproduce.py --work /tmp/character617-119-replay` from this
directory with a new work path. Only the Python standard library is used.
The source and compact expected evidence are published here; generated
large row lists and execution logs are regenerated locally. Each
mathematical child retains a 20-second guard with numerical threads one.
The measured cold-source run is in VERIFICATION.json. No timeout, failed
enumeration or kill supplies a mathematical exclusion. Same-author
implementation independence is distinct from independent-person review.

Primary context is
[Monroe Tables 1 and 2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
(>3703 and prime 617) and
[Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf).
Monroe's length-first W(7,2) is the campaign's color-first W(2,7).
These are prior art, not new numerical bounds or evidence of historical
priority. The asymmetric w(3,k) result is a different problem.

Remaining mathematical work is the 11/13 and 12/12 actual-flip balances
with missing budgets 23 and 24. Their different least-row gates require
new coverage. [QUADRUPLE_LIFT.md](QUADRUPLE_LIFT.md) covers their new
small-common degree-two branches using the checked four-row family,
with closed physical-column coefficient formulas. The proposed new
extension census is unrun. [WEIGHTED_ENDPOINTS.md](WEIGHTED_ENDPOINTS.md)
proves an additional necessary weighted condition on actual flip supports;
its finite local audit is separate from this cold replay. The unrestricted
[1,3704] coloring target remains.
