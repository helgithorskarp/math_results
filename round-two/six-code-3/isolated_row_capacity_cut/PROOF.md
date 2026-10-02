# Isolated-row capacity cut and odd boundary blocks at71

Actual author **six-code-3, researcher**, 2026-10-02, pass13.
Author-checked conditional theorem, exact finite checks complete,
ordinary bridges unformalized, independently unreviewed. Historical
priority and sharpness are unclaimed; unrestricted69--71 stays open.

Let F have71 distinct five-subsets of18 points with pairwise
intersection at most2. Write r_p and lambda_pq for point and pair
replication. Import the universal point cap20/no-low-low saturated-star
leave theorem [8323](../../../constant_weight_upper71_review1/REVIEW.md),
generic23-star coverage [8933](../../six-reviewer-5/twenty-star-classification-audit/REVIEW.md)
conditional on8323, and the exact three-point local bound
[9249](../unit_second_u_four_interfaces/PROOF.md). These are explicit
mathematical dependencies. Independent
[9293](../../six-reviewer-4/three-point-star-audit/REVIEW.md) confirms
the imported three-point theorem with a complete combined proof from
8933/8323, replacing the earlier numerical9209/9176/9141 branches.
That review does not audit this new capacity cut or its boundary transfer.

Let S={p:r_p=20}, H its complement, m=|H| and n=18-m.
Total point replication355 implies sum(20-r_p)=5 and1<=m<=5.
Define P=sum_{a<b in H}lambda_ab and T as the number of covered
triples wholly in H. For distinct points let delta_pq=5-lambda_pq.
Pair multiplicity is at most5, since the three-point tails of words
through a fixed pair are disjoint on16 remaining points.

**Theorem, for1<=m<=4.** With the quantities below,

    K <= E+Q,
    2E+Q >= W+2X,
    4P >= C_m + 2T + 2X + 4tau + Q,
    (C_1,C_2,C_3,C_4)=(9,12,35,76).

**Boundary refinement.** If m3, then **P>=10**; if m4, then
**P>=20**. Thus both possible three-unsaturated profiles
(17,19,19,20^15) and(18,18,19,20^15) meet the sameP10 restriction.
The four-unsaturated profile(18,19,19,19,20^14) meetsP20.
There is no assumed unit S-S deficit pattern, fixed hub pair,
covered/uncovered hub triple, tau0, marked fourth point, whole-code
symmetry or actual row-inventory realization. X,T,tau and Q become
zero in some boundary arguments as proved consequences only.

## Row definitions and exact finite domain

Shortening at s in S gives twenty quadruples on17 link points,
with pairwise intersection at most1. Link replication is lambda_sp.
The nonnegative deficits sum5. Let H_s be the deficient link points,
h_s=|H_s|, e_s=5-h_s, and k_s=|H_s intersect H|. A row is unit
exactly when e_s=0, equivalently every pair multiplicity is4 or5.
Let q_s count leave edges within H_s having a hub endpoint.
Let g1_s count saturated link points with deficit1.
Let sigma_s sum(delta_sp-1) over deficient saturated link points.

Call a row eligible when some actual U in H intersect H_s is isolated
in the leave induced on H_s. Isolation concerns only deficient
neighbors; ordinary low leave neighbors remain permitted.

At a unit eligible row put psi_s=g1_s. At a nonunit ineligible row
put psi_s=-g1_s. At all other rows put psi_s=0.

The exact local certificate is

    psi_s >= 3*(k_s-e_s-q_s).                  (R)

[produce.py](produce.py) validates all23 actual quadruple objects,
replications, unique pairs and leaves from credited
[fixtures.json](fixtures.json). For every high subset J representing
the deficient hubs it derives eligibility, k,e,q,g1,sigma and psi.
No automorphism quotient or maximal group assumption is used.
There are426 actual high-subset records, of which **418 have|J|<=4**.
Every one of those418 satisfies(R), with minimum margin0.

Coverage is explicit: at most5 link points are high. For an actual
m-hub placement only J=H intersect H_s affects these statistics.
The other m-|J| hubs are low. At least12 low points are available;
each such low placement yields exactly the same row statistics.
Every high subset of size at mostm is enumerated. Actual point labels
and complete row records, not just populations, are compared with
the separate point-mask reconstruction in [verify.py](verify.py).
It imports no producer, boundary enumerator, solver or earlier program.
Supplied fixture groups are credited input fields but are unused here.

Eight actual unit-star marks with all five high points designated hubs
have k5,e0,q4,g1=psi0 and margin-3. They are deliberately retained
as exact scope controls. Thus(R) is not extended to m5. These are
actual marked20-stars, not counterexamples realizing a global71 code.

## Why the row demand fits only in noneligible nonunit capacity

The imported9249 says any distinct x,y,U with r_x=r_y20,xy4,
unit second row y and an isolated deficient U at x force upper67.
It has no named fourth mark and no lambda_yU5 requirement.
Its generic inputs retain exact scope. Independent9293 supplies the
complete combined local proof without older numerical branch premises;
this runner does not replay either author's earlier finite carriers.

Take a unit eligible x and a deficient saturated neighbor y. Its
pair deficit is1. If y is unit,9249 at(x,y,U_x) contradicts71.
If y is nonunit eligible, reverse the centers and apply9249 at
(y,x,U_y), again contradicting71. Both U marks are actual hubs,
hence distinct from the saturated centers. Therefore every deficient
saturated neighbor of a unit eligible row is nonunit AND ineligible.

The pair deficit is1 at both ends. Count these simple undirected
edges from their unit-eligible endpoints. At a nonunit ineligible
endpoint their number is at most its g1_s. Thus

    sum_s psi_s <=0.                         (D)

Combining(D) with all actual(R) rows gives K<=E+Q, where
K=sum k_s,E=sum e_s,Q=sum q_s. Counting only singleton unit
eligible rows against ALL nonunit rows would discard the reverse
orientation and be weaker. Eligible nonunit rows cannot offer
capacity to a unit eligible neighbor.

## Weighted deficits and homogeneous triples

Let X=sum_{a<b in S,delta_ab>0}(delta_ab-1).
The weighted S-H deficit is

    W=sum_{s in S,a in H}delta_sa
     =20+10m-5m^2+2P.

Indeed the hub replication sum is R_H=20m-5. Total incident
deficit at hubs is85m-4R_H; subtract the twice-counted H-H
deficit10*C(m,2)-2P. At a saturated row,
e_s=sum_positive(delta-1); globally

    E=W-K+2X.

Hence K<=E+Q is precisely2E+Q>=W+2X. No S-S excess has
been silently set to zero.

Every low link point in a20-star has exactly one leave neighbor,
which is high by8323. Its16 leave edges therefore include h_s-1
high-high edges. Their total is4n-E.

Let G be the simple S-S positive-deficit support, and let tau
count uncovered S-triples whose three pairs are all in G. Every
uncovered S-triple is a path or triangle in G: a triple with fewer
than two deficit pairs would give a forbidden low-low leave at
one saturated center. Its high-high center count is1 or3.
Consequently, if A0 counts all uncovered S-triples,

    4n-E = A0+2tau+Q.

A word with j hubs owns C(5-j,3) saturated triples, and

    C(5-j,3)=10-6j+3*C(j,2)-C(j,3), 0<=j<=5.

All triples have at most one owner. Therefore

    A0=C(n,3)-710+6R_H-3P+T,
    E+Q+2tau=B_m+3P-T,
    B_m=4(18-m)-C(18-m,3)-120m+740.

This elementary homogeneous-triple identity retains the method credit
of [8368](../../../constant_weight_18_6_5_equality_structure/DEFICIT_CUT_71.md);
it is fully derived here. Substituting it into2E+Q>=W+2X gives

    4P >= C_m+2T+2X+4tau+Q,
    C_m=(20+10m-5m^2)-2B_m.

| m | n | B_m | C_m | Initial consequence |
|---|---|---|---|---|
|1|17|8|9|Impossible since P0.|
|2|16|4|12|P>=3 before boundary parity.|
|3|15|-15|35|P>=9 before boundary parity.|
|4|14|-48|76|P>=19 before boundary parity.|

The one-/two-hub observations are calibration, not claimed new.

## Exact boundary categories and the ordinary odd handshake

Put margin_s=psi_s-3*(k_s-e_s-q_s)>=0. From(D),

    sum margin_s <=3*(E+Q-K).                (M)

This bound is used together with the literal local categories; an
aggregate population or missing category is not treated as coverage.
[boundaries.py](boundaries.py) recursively enumerates every necessary
category composition. The separate checker iterates count vectors and
compares every actual category/template, without importing that program.
The three targets(m,P)=(2,3),(3,9),(4,19) have four complete branches.
They are necessary statistics, not actual packings or isomorphism classes.

For m3,P9, the exact inequality forces T=X=tau0 and Q<=1.
If Q0 then E12,K11. Bound(M) permits total margin at most3.
The complete q0/sigma0 catalog contains a missing-link-point row with
h1,e4,k1,psi0 and margin9; it is excluded HERE by(M), not discarded
from the catalog. Every remaining q0/sigma0 category with margin<=3
has k>=e, contradicting K11<E12. The exact category inventory is empty.

If Q1 then E11,K12 and total margin0. The complete remaining categories
are shown below, with their uniquely forced populations:

| e | k | q | Eligible | h | g1 | Population |
|---|---|---|---|---|---|---|
|0|0|0|no|5|5|3|
|0|1|1|no|5|4|1|
|1|1|0|yes|4|3|11|
|1|1|1|no|4|3|0|

Thus all11 nonunit rows are eligible2111 rows whose heavy entry is
at their sole deficient hub. Each has exactly three deficient
saturated neighbors, all with pair deficit1. None of those neighbors
can be unit, by9249 with that row as first center. All three therefore
lie among the same11 nonunit rows. The induced simple graph would
be3-regular with degree sum33, impossible by the handshake lemma.
Hence P9 is impossible and m3 impliesP>=10.

For m4,P19, equality forces T=X=tau=Q0,E9,K9 and all margins0.
The unique necessary category composition is five unit rows with k0
and nine eligible2111 rows with k1,q0. These nine have all three
saturated deficit neighbors inside their own block. Degree sum27
is odd, giving the same contradiction. Hence m4 impliesP>=20.

The m2,P3 calibration similarly leaves thirteen eligible2111 rows,
degree sum39, and is contradictory. No novelty is assigned to this
already closed two-hub frontier. No shared-isolated-hub completion
lemma, whole remaining-inventory census or graph realization is used
in the new m3/m4 boundary proof.

## Verification, provenance and remaining scope

[expected.json](expected.json), scalar [certificate.json](certificate.json)
and literal input were frozen before both complete cold replays.
Normal and optimized modes have byte-identical whole mathematical
RESULT files and all eight mathematical-source hashes unchanged.
The full426-record SHA256 is
19205841cee4584466bac048f114d0d5f0db096b6861e45f34c94b9180087b16;
the four boundary records have SHA256
dd7d8f21ddc92ac2e5acb3708adc4824429aa77b4842e078e5c4dcdfd70de552.

[controls.py](controls.py) rejects23 semantic damages/gaps, including
wrong eligibility/capacity/charge, an account-consistent wrong psi,
deleting the actual e4 mark, deleting the five-hub scope failures,
offering eligible mixed capacity, widening to five hubs, missing
fixtures/products and fabricated even boundary blocks/handshakes.
Three actual point bijections transport all23 stars and all426
marked row objects:69 relabeled stars and1278 actual marked rows.
These are same-author separate implementations, not independent review.
Exact costs are in [VALIDATION.json](VALIDATION.json); commands and
scope are in [README.md](README.md) and [DEPENDENCIES.json](DEPENDENCIES.json).

One serial CPU-intensive job, all numerical threads1, unchanged1CPU2GiB.
Guards10s/subprocess,100000 category states and10s/category branch;
no guard hit or resource change. Incomplete computation proves no absence.
The finite checks establish complete row and necessary-category inventories;
ordinary shortening/projection/incidence/identity/parity arguments bridge
them to the theorem and remain unformalized. The imported local theorem
9249 is independently confirmed by9293; the new row coefficient and
boundary parity remain independently unreviewed. Neither the original
nor the independent local finite carrier is replayed here.

The incidence-cut direction was independently raised in six-code-1's
private draft at chat1555 (2026-10-02): a weaker3E+2Q cut and P8/P18
thresholds, plus a separate five-hub statement. That unpublished draft
is method credit, not a theorem premise. This source's distinguishing
mechanism excludes ELIGIBLE nonunit capacity, checks the exact23-star
coefficient and closes the new boundaries by odd degree sums. The private
count bridge1549 is not substituted for public9249.

Earlier [9180](../../six-code-1/three_unsaturated_pair_total/PROOF.md),
source6089c57659f6be672b466aaf77ddf25e0467a685, establishedP>=7
for profile17/19/19. The presentP10 result strengthens that scope and
also covers the other three-hub profile. Its prior numerical proof is
not imported. No novelty is assigned to previously closed one-/two-hub
profiles or to the inherited local67 certificate.

The current primary [Brouwer table](https://aeb.win.tue.nl/codes/Andw.html)
retains69--72; [Aw--Chee--Ling2003 Theorem1/AppendixA](https://ymchee66.github.io/home/PDF/6cwc.pdf)
supplies the prior69 construction. The [literal69](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69)
was freshly checked:69 distinct weight5 words,2346 pairs,690 unique
owned triples, distances6:1264/8:637/10:445, source SHA256
cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d.
Baseline reproduction is validation, not research novelty. No historical
priority, m5 extension, whole three-/four-hub exclusion or unrestricted
upper70 is claimed. The new precise frontiers include m3,P>=10 and
m4,P>=20 with all original global compatibility requirements retained.
