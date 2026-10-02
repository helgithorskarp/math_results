# Five unsaturated points at 71 words force hub-pair total at least 35

Actual author **six-code-1**, role **researcher**, 2026-10-02.
Author-checked conditional lemma; exact finite checks complete, ordinary
mathematical bridges unformalized, independent review pending. The shared
signing identity does not establish distinct authorship or independence.

Let F be a family of 71 distinct five-subsets of an eighteen-point set,
with every two members intersecting in at most two points. Write r_p for
point replication and lambda_pq for pair replication. Put
S={p:r_p=20}, H its complement, m=|H|, and
P=sum_{a<b in H}lambda_ab. The following three mathematical premises
are explicit dependencies:

* [8323](../../../constant_weight_upper71_review1/REVIEW.md): the point cap
  20, the universal prohibition of low-low leave edges in twenty-block
  quadruple stars, and the independently proved unrestricted upper bound 71.
* [8933](../../six-reviewer-5/twenty-star-classification-audit/REVIEW.md):
  conditional on8323, the 23 literal fixtures represent every twenty-block
  quadruple pair packing on seventeen points.
* [9249](../../six-code-3/unit_second_u_four_interfaces/PROOF.md): for
  distinct x,y,U, if r_x=r_y=20, lambda_xy=4, the second row y is unit,
  and U is a deficient link point isolated in the high-induced leave at x,
  then |F|<=67. Independent
  [9293](../../six-reviewer-4/three-point-star-audit/REVIEW.md) confirms this
  local theorem directly from8933/8323, including its stated structural
  conclusions. No additional fourth mark or lambda_yU=5 is required.

**Theorem.** Under those premises, if m=5, then **P>=35**.
The point profile is necessarily (19^5,20^13). This sharpens the previous
[P>=34](../selection_deficit_cut/PROOF.md), graph9299. Independent
[9355](../../six-reviewer-5/selection-capacity-audit/REVIEW.md) now confirms
that prior result, proves a stronger catalog-free capacity inequality, and
proves T=1,X=tau=0 at its P34 boundary using the explicit upper71 append
step. Its verdict expressly excludes this new P35 argument. The present
proof rederives its needed count and append step rather than importing the
new9355 numerical inequality. It excludes the
minimal P34 boundary, not the entire five-hub profile. No construction,
unrestricted upper70, sharpness or historical priority is asserted.

A useful intermediate result extends the capacity inequality of
[9313](../../six-code-3/isolated_row_capacity_cut/PROOF.md) to all 1<=m<=5,
with an explicit correction for its eight actual five-hub scope failures.
The earlier P10/P20 boundary results for m3/m4 retain their own proofs.

## Corrected row capacity, including the exceptional markings

Pair tails are disjoint triples on sixteen points, so lambda_pq<=5.
Define delta_pq=5-lambda_pq. Total point replication is355 and the
point cap gives sum_p(20-r_p)=5, hence1<=m<=5.

At a saturated center s, shortening gives twenty quadruples on seventeen
link points, with every pair owned at most once. Its deficit row sums5.
Let D_s be its positive-deficit link points, h_s=|D_s|, e_s=5-h_s,
and k_s=|D_s intersect H|. A row is unit precisely when e_s=0: its
positive deficits are all1, so all pair multiplicities are4 or5.

The leave consists of uncovered link pairs. It has16 edges. A point
with deficit d has leave degree1+3d; a low point has degree1, and8323
places its unique leave neighbor in D_s. Exactly h_s-1 leave edges
therefore have both endpoints in D_s. Let q_s count those edges with
at least one endpoint in H.

Call s eligible if some actual U in D_s intersect H is isolated in
the leave induced on D_s. This permits low leave neighbors of U.
Let g1_s count deficient saturated link points whose deficit is1,
and sigma_s=sum_{p in D_s intersect S}(delta_sp-1). Define

    psi_s = g1_s     for a unit eligible row,
            -g1_s   for a nonunit ineligible row,
            0       otherwise.

Let I_s=1 exactly when s is unit and all five of its deficient link
points lie in H; otherwise I_s=0. The corrected local inequality is

    psi_s >= 3*(k_s-e_s-q_s-I_s).                 (R5)

This is checked on **every 426 actual marked row** by [verify.py](verify.py).
The credited [fixtures.json](fixtures.json) is copied unchanged from the
published9313 input, itself credited to the complete generic8720 census.
Its SHA256 is
`c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7`.

The checker builds a column of actual block indices for each of the17
points. Their pairwise intersections give the unique pair owners and the
entire leave. It reconstructs each replication, deficit, high-induced
edge, isolated point and statistic from these physical columns, then
checks every subset of the high points as the set of deficient hubs.
The other m-k hubs are low and do not change these statistics; at least12
low points are available and m-k<=5. No whole-code symmetry, prescribed
hub pair, automorphism quotient or supplied group order is assumed.
The supplied fixture groups are ignored.

There are418 original rows with k<=4, and eight further unit rows with
k5,e0,q4,g1=psi0. Their original margin is-3 and their corrected margin
is0. All426 corrected margins are nonnegative. The eight exceptions
are retained rather than deleted. Their existence is local marked-star
evidence, not realization of a71-word code. A separate cold replay of
all four stages of the published9313 source in normal/optimized Python
also passed. Every original row coordinate from this new reconstruction
agrees entry by entry with that replay, not merely by population.

Generic completeness is imported from8933. This new checker does not
reprove that classification or rerun the earlier local9249 carrier.

## Incidence transfer and exact global coefficients

At a unit eligible x, any deficient saturated neighbor y has lambda_xy=4.
If y is unit,9249 applies at(x,y,U_x), contradicting71. If y is nonunit
eligible,9249 applies with the centers reversed at(y,x,U_y), again
contradicting71. Both U marks are actual hubs, distinct from the saturated
centers. Thus every such neighbor is nonunit and ineligible. The edge
has deficit1 at both endpoints. Counting these simple edges gives

    sum_{s in S}psi_s <=0.                       (D)

Let K=sum k_s, E=sum e_s, Q=sum q_s, N5=sum I_s, and
X=sum_{a<b in S,delta_ab>0}(delta_ab-1). Let W=sum_{s in S,a in H}delta_sa.
The hub replication sum is20m-5, so direct incident-deficit counting gives

    W=20+10m-5m^2+2P,       E=W-K+2X.

Summing(R5) and using(D) yields

    K<=E+Q+N5,       2E+Q+N5>=W+2X.              (C5)

Every I_s=1 row has all its four high-high leave edges charged to q_s,
so Q>=4N5. For m<=4, N5=0, recovering precisely the capacity inequality
of9313; no five-hub failure is hidden in that earlier scope.

For completeness, rederive the homogeneous count credited to
[8368](../../../constant_weight_18_6_5_equality_structure/DEFICIT_CUT_71.md).
Let G be the simple positive-deficit graph on S; let tau count uncovered
S-triples whose three pairs all lie in G. An uncovered S-triple must
induce a path or triangle in G: with fewer than two deficit edges, one
center would have a forbidden low-low leave. Its high-high center count
is respectively1 or3. If A0 is the total number of uncovered S-triples,
the high-high leave edges at all saturated centers therefore give

    4(18-m)-E=A0+2tau+Q.

Let T be the number of covered triples contained in H. Every triple has
at most one owner. A word with j hubs owns
C(5-j,3)=10-6j+3C(j,2)-C(j,3) saturated triples. Thus, for n=18-m,

    A0=C(n,3)-710+6(20m-5)-3P+T,
    E+Q+2tau=B_m+3P-T,
    B_m=4(18-m)-C(18-m,3)-120m+740.

Substitution into(C5) yields the corrected inequality

    4P>=C_m+2T+2X+4tau+Q-N5,
    (C_1,C_2,C_3,C_4,C_5)=(9,12,35,76,133).       (P5)

The word polynomial and every integer coefficient are checked exactly.
No S-S excess, uncovered-triple count or eligibility hypothesis has been
silently set to zero.

## The five-hub extension obstruction and the P34 boundary

Now m=5, so each hub has replication19 and n13. If T=0, every existing
word meets the actual five-set H in at most two points. H is then a
new word, since a word equal to H would own ten hub triples. Appending
H produces a72-word packing, contradicting the separately imported
unrestricted upper71 clause of8323. Hence **T>=1**. This uses upper71;
it does not reprove it or presume the desired upper70.

Since Q>=4N5, inequality(P5) gives4P>=135, hence P>=34. Suppose P=34.
Its remaining slack is

    2T+2X+4tau+Q-N5<=3,        Q>=4N5.

As T>=1 and Q-N5>=3N5, this forces

    N5=X=tau=0,       T=1,       Q=0 or 1.

The homogeneous identity and support identity now give

    E=7-Q,       W=13,       K=6+Q.

Put mu_s=psi_s-3*(k_s-e_s-q_s-I_s)>=0. From(D),

    sum mu_s<=3*(E+Q+N5-K).

The total margin budget is3 for Q=0 and0 for Q=1. Since X=0, every
saturated row has sigma_s=0. [EXPECTED.json](EXPECTED.json) contains
every necessary category and every count vector for these two branches.
Recursive count-vector enumeration and a separate sparse generating-
function coefficient calculation agree on every pattern. These are
necessary row statistics, not actual packings or global isomorphism classes.

For Q=0 the complete categories within margin budget3 are:

| e | k | q | Eligible | h | g1 | psi | Margin |
|---:|---:|---:|---|---:|---:|---:|---:|
|0|0|0|no|5|5|0|0|
|0|1|0|yes|5|4|4|1|
|1|1|0|yes|4|3|0|0|

Each has k>=e, contradicting K=6<E=7. The actual h1/e4/k1 missing-link
point row has margin9 and is excluded by this proved budget, not removed
from the 426-row catalog. The exact necessary inventory is empty.

For Q=1 every row has margin0. Its complete categories and the uniquely
forced populations are:

| e | k | q | Eligible | h | g1 | psi | Population |
|---:|---:|---:|---|---:|---:|---:|---:|
|0|0|0|no|5|5|0|6|
|0|1|1|no|5|4|0|1|
|1|1|0|yes|4|3|0|6|
|1|1|1|no|4|3|-3|0|

Indeed E=6 fixes six nonunit rows, all with k=1; K=7 then requires the
additional unit k=1 row, which exhausts Q=1. All six nonunit rows are
eligible2111 rows with their deficit2 at their sole deficient hub.
The other three positive entries are saturated points of deficit1.

## A nonempty closed cubic block must have at least ten points

Let C be those **six** nonunit saturated centers. At x in C, let U be
its deficient hub and let a,b,c be its three saturated deficient neighbors.
Since q_x=0, U is isolated in the high-induced leave. With h_x=4 there
are exactly three high-high leave edges, all among a,b,c. Thus all three
of their pairs are leave edges: every neighbor wedge at x is an actual
uncovered saturated triple.

None of a,b,c can be unit, by9249 with x as first center and the unit
point as second center. The forced category inventory has no other
nonunit rows, so all three neighbors belong to C. The induced G[C] is
therefore a **simple cubic graph**. Closure is a proved consequence of
the physical local theorem, not a graph assumption about an invented row
inventory.

It has no triangle. A triangle x,y,z would make xyz uncovered by the
neighbor wedge at x; all its pairs are in G, so it would count toward
tau, contrary to tau=0.

It has no four-cycle. Suppose x-y-z-w-x is a cycle with four distinct
vertices in C. Triangle-freeness excludes the diagonal yw from G.
Thus lambda_yw=5 and w is low in y's shortened star. The neighbor wedges
at x and z give the **two distinct** uncovered triples xyw and zyw.
In the star at y, the low point w would consequently have both x and z
as leave neighbors. Its exact leave degree is1, a contradiction.

Finally choose a vertex of the nonempty cubic graph. Its three neighbors
are distinct. Each has two further neighbors. The absence of triangles
puts these six points outside the first layer and the root; the absence
of four-cycles makes all six distinct. Therefore its vertex set has at
least1+3+6=10 points, contradicting |C|=6. The nonempty qualification is
essential; an empty closed block would supply no root. Here nonemptiness
is forced separately by the six-row count.

This ordinary argument also proves the general conditional closed-block
lemma: any **nonempty closed** set of saturated rows of type e1/k1/q0,
with zero saturated excess and tau=0, has at least ten points. It does
not assert that such a closed set must exist away from the present boundary.
Compatible private girth arguments in six-code-3's chat1661/1664 are
credited, including the correction to retain nonemptiness; those messages
are research input, not an independent mathematical review.

Both P34 branches are impossible. Combined with P>=34 this proves P>=35.

## Exact checks, primary context and remaining trust boundary

The new reconstruction's original426-record SHA256 is
`19205841cee4584466bac048f114d0d5f0db096b6861e45f34c94b9180087b16`;
its full corrected426-record SHA256 is
`4832875a52850041bc33b5fc8d99ab96de0a35019b0b2dad68830701cb0d5034`.
Hashes authenticate full records but do not replace the classification
or the written transfer. The checker also literally tests every one of
the5005 nine-edge sets on six labeled vertices:70 are cubic,10 of those
are triangle-free, and none has girth at least five. This is a check of
the small abstract obstruction; the physical packing-to-graph bridge is
the ordinary proof above. A literal Petersen graph on ten vertices is
a positive sharp control for the abstract bound, not a71-code construction.

Twenty-two damaged-input, deleted-exception, false-scope and nonempty
controls reject. Three actual point permutations transport all23 stars
and all 426 marked rows,1278 transported rows in total. Each full transported
record and boundary pattern is compared after inverse point transport.
Checks use explicit exceptions, so they remain active under Python -O.
Normal and optimized whole frozen mathematical outputs agree; exact
versions, costs and source hashes are in [VALIDATION.json](VALIDATION.json).
Commands are in [README.md](README.md); [DEPENDENCIES.json](DEPENDENCIES.json)
records scope, verified source commits and graph references.

The [maintained primary table](https://aeb.win.tue.nl/codes/Andw.html),
refreshed live2026-10-02, still lists69..72. The separately reviewed
campaign upper71 is distinct prior work. [Aw--Chee--Ling2003](https://ymchee66.github.io/home/PDF/6cwc.pdf),
Theorem1/AppendixA, supplies the established69-word construction. Its
[primary literal certificate](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69)
is copied unchanged as [BASELINE69.txt](BASELINE69.txt), SHA256
`cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d`.
The checker reproduces all 2346 word pairs,690 unique triple owners and
distances6:1264/8:637/10:445. This is baseline validation, not new research.
The established point cap retains [Brouwer1975](https://ir.cwi.nl/pub/6883/6883D.pdf)
credit even though8323 supplies a separate proof.

The new claim relies on the explicit imported mathematical premises,
literal fixture decoding, CPython3.11 standard-library exact integers,
and unformalized shortening, capacity, homogeneous-count, extension and
girth bridges. Author execution of peer code is reproducibility evidence,
not independent review of this new lemma. No solver, floating-point
bound, heuristic failure, timeout, incomplete enumeration or resource
kill supplies an exclusion. One serial mathematical job, all native
threads1, unchanged1CPU2GiB; fixed10-second/100000-state category guards
and a10-second cold subprocess guard are sufficient and are never raised.
Large row dumps and operational state regenerate in scratch and are not
published. The unrestricted69..71 interval remains unresolved.
