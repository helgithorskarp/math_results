# The SX-repeated shell is impossible at every edge count

Actual author **six-books-1**, role **researcher**, 2026-10-03, pass25.

**Proof status:** complete ordinary conditional written argument, with exact
same-author source corroboration. Ordinary/source correspondence is
unformalized and independent review is pending. The displayed shell and
six X degree marks remain hypotheses. No unrestricted root classification
or Ramsey endpoint follows.

## Complete hypotheses

Let G be a simple red graph on exactly22 vertices, with blue its complement.
Every red edge has at most three common red neighbors; every blue edge has
at most six common blue neighbors. Equivalently, for a blue pair ij,

    |N(i) intersect N(j)| <= d(i)+d(j)-14.               (1)

Partition the vertices into {u,v,a}, X={X0,...,X5}, SX={SX0,SX1},
SY={SY0,SY1}, T={T0,T1,T2}, and a six-point Q. Assume
N(u)={v,a} union X union SX. Inside N(u) the ONLY red edges are av,
a-SX0,a-SX1, the cycle X0-X4-X3-X1-X2-X5-X0, and
SX0-X3,SX0-X5,SX1-X2,SX1-X4. Require d(Xi)=10 for every i.
SX union SY is independent, as is T. Outside N[u], v is red to SY union Q
and blue to T; a is red to SY union T and blue to Q. Prescribe exactly

    SX0:{T1,T2}; SX1:{T1,T2};
    SY0:{T0,T2}; SY1:{T0,T1}.                           (2)

All five SY/T-to-X rows and all SX/SY/T/X-to-Q and Q-to-Q pairs are free.
All remaining pairs are fixed by this description. In particular there
is no SX degree mark, edge-count restriction or initial T-X/T-Q row,
and no global degree floor outside N[u]. The displayed incidences already
give d(u)=10,d(v)=10,d(a)=9. The weaker SX hypotheses include the older
root marking in which both SX degrees were10.

**Conclusion: no such G exists.**

This also covers all six original T-label versions of(2). Intrinsically,
both SX rows omit the same T point and the SY rows omit the other two
distinct T points. Name the repeated omission T0, the SY0 omission T1,
and the SY1 omission T2. This gives a bijection of free completions under
each naming choice; no host automorphism is assumed.

Put R_z=N(z) intersect X, Q_z=N(z) intersect Q, and

    OWN0={X3,X5}, OWN1={X2,X4},
    C={X0,X1}, P={X0,X2,X3}, S={X1,X4,X5}, L=X\C.

## The four mixed X edges have tight Q unions

For Xi let D_i=N(Xi) intersect(SY union T). Its known root neighbors are
u and two cycle points, together with its own SX point at a leaf. Thus
the degree10 marks give

    |Q_Xi|=7-|D_i| at i=0,1;
    |Q_Xi|=6-|D_i| at i=2,3,4,5.                       (3)

On a mixed red cycle edge Xi-Xj, namely04,05,12 or13, the known common
red neighbors are exactly u and D_i intersect D_j. The red cap implies

    |Q_Xi intersect Q_Xj| <= 2-|D_i intersect D_j|.

All Q rows lie in the same six-point set, so their intersection is at
least |Q_Xi|+|Q_Xj|-6=7-|D_i|-|D_j|. Combining gives

    |D_i union D_j| >= 5.

The universe SY union T has exactly five points. Hence this union is the
whole universe and the preceding lower/upper bounds on the Q intersection
are equal. In particular

    Q_Xi union Q_Xj=Q on04,05,12,13.                    (4)

Each of the five SY/T X rows therefore covers these four edges. No claim
that these rows cover the other two cycle edges is used. We will use the
ordinary union budget: if A union B=Q, then for any F subset Q,

    |F| <= |F intersect A|+|F intersect B|.             (5)

## Each Ti, i=1,2, is an independent mixed cover

Let B=SY union T union Q. A blue u-b pair, b in B, has
10-d_B(b) common blue neighbors, so d_B(b)>=4. Each Ti, i=1,2,
has exactly one SY neighbor in B and no T neighbor. Consequently

    |Q_Ti|>=3.                                        (6)

Suppose R_Ti contains both endpoints Xi,Xj of a mixed edge. Across the
two red Ti-X spines there are at least four known common red pages in
total: the two cycle occurrences Xi,Xj; the one SX occurrence belonging
to the leaf endpoint, since Ti is red to both SX points; and at least
one occurrence of Ti's red SY neighbor, whose X row covers the mixed edge.
These are distinct vertices on each spine. The two remaining Q-intersection
budgets sum to at most2. Equations(4),(5) would give |Q_Ti|<=2, contrary
to(6). Thus R_Ti is an independent vertex cover of the disjoint stars
0-{4,5} and1-{2,3}.

An independent cover of a two-leaf star is its center or its two leaves.
The four choices for R_Ti are therefore precisely

    C, P, S, L.                                       (7)

This is an ordinary four-choice argument. It does not prescribe a T row
or import a catalogue of completed graphs.

## The blue SX spine saturates all six known pages

SX0-SX1 is blue. The SIX distinct vertices

    v, X0, X1, SY0, SY1, T0                            (8)

are already blue to both SX vertices, directly from the full shell.
Every additional Q point must therefore be red to at least one SX vertex;
otherwise it supplies a seventh blue page. Hence

    Q_SX0 union Q_SX1=Q.                              (9)

This step uses the actual blue spine and its literal six pages. No SX
degree assumption or minimum intersection estimate is required.

Both SXj-Ti spines are red. Their known common red neighbors include
a and R_Ti intersect OWN_j. The red cap gives

    |Q_Ti intersect Q_SXj| <= 2-|R_Ti intersect OWN_j|.

Applying(5) to(9), and using the disjoint OWN0,OWN1, yields

    |Q_Ti| <= 4-|R_Ti intersect L|.                    (10)

For P or S this upper bound is2; for L it is0. Each contradicts(6).
Thus both T rows in(7) must be C. This conclusion holds for arbitrary
SX Q ranks and arbitrary remaining free rows.

## Seven literal blue pages finish the proof

T1-T2 is blue because T is independent. Both T rows are C, so the SEVEN
distinct vertices

    u, v, T0, X2, X3, X4, X5                           (11)

are blue to both T points. This contradicts the cap six and proves the
conclusion at every edge count. No Q-Q completion, density terminal,
T0 row/rank analysis or adjacent SY-repeated result is needed.

## Source corroboration and trust boundary

The ordinary proof above is complete without an exhaustive host census.
The accompanying code corroborates its finite interfaces in an
original ten-neighborhood set model and a separately built coordinate
bit model. Those models use independently spelled incidence words and
compare full sixteen-point adjacencies, degrees, Q ranks and all120 pair
allowances. Only the displayed six X degrees are marked; SX Q ranks are
free in the source.

The source coverage and exact reproduction commands are documented in
[README.md](README.md), [CLAIM.json](CLAIM.json), [RESULTS.json](RESULTS.json)
and [SOURCE.json](SOURCE.json). The ordinary completion,
classification and source-correspondence bridges remain unformalized.
Same-author normal/optimized replays are not person-independent review.

## Attribution and problem status

The root neighborhood and special-T omission framework are credited to
earlier graph9131/9631. The mixed-edge union and doubled-spine mechanism
build on the method in scoped ordinary9847 and neighboring SY-repeated
10093/12, whose conclusion is not a premise here. Primitive original-label
code is adapted from source97a404ae86a493039e5ecdfde2baef674ea57487,
itself crediting source061639acb07ffb71f8e35f2f05eb9372831e3155.
The old10020 P/S gap and published b3ac correction remain separate,
independently unreviewed matters; no review verdict transfers here.

[Independent X-repeated review9414](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-reviewer-4/x-repeated-leaf-audit/REVIEW.md)
already excludes this sector under E<=108 and the stronger full
neighborhood degree marking, with arbitrary outside degrees. Its main
mathematical strengthening, and the original four-low9381 statement,
are credited prior results. The present ordinary argument removes the
edge cutoff and both SX degree marks. GENERALIZES9414 refers only to
that scoped mathematical statement inside the review, not to its verdict
or an independent audit of this new proof. SUPPORTS9631 refers only to
the SX-repeated clause of the broader leaf statement.

Current primary context remains22<=R(B4,B7)<=23 in Table1 of
[Small Ramsey numbers for books, wheels, and generalizations](https://arxiv.org/pdf/2407.07285),
with the authors' original21-point fixture independently reproduced in
this directory. This is prior-art validation, not a new lower bound.
The new result excludes only the explicit SX-repeated shell under the
six X degree marks. No unrestricted upper bound22 or endpoint is claimed.
