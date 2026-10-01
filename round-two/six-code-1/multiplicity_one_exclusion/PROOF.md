# Two unsaturated points at 71 words share at least two words

Actual author: **six-code-1, researcher**, 2026-10-01.

**Theorem, with the explicit published premises below.** Let F consist
of 71 distinct five-subsets of an eighteen-point set, with distinct
members intersecting in at most two points. If exactly two points u,v
have replication below 20, then their pair multiplicity satisfies

    lambda_uv >= 2.

The new step excludes lambda_uv=1. The already published absent-pair
theorem excludes lambda_uv=0. This strengthens the known restriction
in the remaining profile (17,18,20^16); the alternative two-point
profile (16,19,20^16) was excluded by earlier work. No hypothesis on
other pair multiplicities or code automorphisms is made.

This is a counting proof using previously published exact local
lemmas. The written proof is unformalized and independently unreviewed;
the imported shared-hub pair lemmas also retain their unreviewed status.
The global campaign interval remains 69--71. Attainment of 70 or 71
and the other replication profiles are not decided here. Historical
priority is unassessed.

## Definitions and exact premises

Write r_x for point replication, lambda_xy for pair multiplicity, and
delta_xy=5-lambda_xy. Words through a pair have disjoint three-point
tails, so lambda_xy<=5. Shortening at a point gives a quadruple pair
packing on seventeen points. The established point cap 20 implies
sum_x(20-r_x)=5. With exactly two unsaturated points their replication
profiles are therefore (16,19,20^16) or (17,18,20^16).

Let S be the sixteen saturated points, each with replication 20.
At a saturated center x its positive-deficit neighbors are called
high; the other link points have replication five and are called low.
An edge of its leave means that the corresponding triple with x is
uncovered by F. The reviewed
[universal twenty-star theorem8323](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_upper71_review1/REVIEW.md)
says that a saturated link has no low-low leave edge, and has exactly
h_x-1 high-high leave edges, where h_x counts its high points.
Every positive deficit row at a saturated point has total weight five.

Partition S into A (deficient only to u), B (only to v), T (to both),
and Z (to neither). Put z=|Z| and

    X=sum_(unordered xy in S) max(delta_xy-1,0).

Set m=lambda_uv. The m common words have disjoint three-point tails.
Let C be their union and c=|T intersect C|. The published
[incidence theorem8497](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/TWO_UNSATURATED_INCIDENCES.md)
gives

    |C|=3m,   Z subset C,   2X+z+c<=m,
    R=m-z+c-2X.                                           (1)

Here R is exactly the number of saturated high-high incidences in
uncovered triples containing one of u,v, plus twice the number of
wholly saturated uncovered deficit triangles. In the first summand,
an incidence is indexed by its saturated center x, its hub i in {u,v},
and its other saturated point a: the triple xia is uncovered and
delta_xi,delta_xa are positive. A triple can contribute at both of its
saturated centers; these are different incidences. All summands are
nonnegative. Each point of T intersect C contributes at least two
one-hub incidences centered at that point. The published proof of
this last fact explicitly imports the marked-unit-star classification.

The three shared-isolated-hub lemmas
[mixed/mixed8356](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/COMMON_MIXED.md),
[unit/unit8397](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/COMMON_UNIT.md), and
[mixed/unit8438](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/COMMON_MIXED_UNIT.md)
forbid a multiplicity-four pair of saturated centers whose common
deficient hub is isolated in both high leaves. The endpoint rows must
respectively be mixed (2,1,1,1), with the common hub its unique
deficit-two point, or unit (1,1,1,1,1). These lemmas assume no total
code size or replication of the shared hub. The input classifications
and complete relative-star carriers are credited in their published
proofs; their completeness is an imported premise here.

## Multiplicity one and its covered triples

Assume m=1. There is a unique common word

    K={u,v} union C,   |C|=3.

In particular, for every two distinct a,t in C the triples uat and vat
are covered. Equation(1) gives X=0, z+c<=1, and

    R=1-z+c.                                              (2)

Thus every positive S-S deficit is one. We consider c=1 and c=0;
these are all possible values of c.

## A covered point deficient to both hubs is impossible

Suppose c=1, and let t be the unique point in T intersect C.
Then z=0 and R=2. The two-incidence lower bound at t exhausts R:
there are exactly two one-hub incidences centered at t and none at
any other saturated center, and no wholly saturated deficit triangle.

Choose one of these incidences, given by an uncovered triple ita,
with i in {u,v}, a in S, delta_it>0, and delta_ta=1.
If delta_ia>0, the same triple gives another one-hub high-high
incidence at the different saturated center a, contradicting the
exhausted budget. Therefore delta_ia=0, so lambda_ia=5.

At center a the link point i consequently has leave degree
16-3*5=1. Its sole leave partner is t. Let j be the other hub.
As j differs from t, the triple aij=auv is covered. Uniqueness of
the uv word forces a in C. But then ita is a subset of K and is
covered, contradicting the incidence we chose. This excludes c=1.

## Good and bad single-hub centers

Now c=0, so z is zero or one, and R=1-z.
Let H be the number of one-hub high-high incidences centered in
A union B. It is a subset of the incidences counted by R, so

    H <= R.                                               (3)

Call a center in A union B good if it contributes no such incidence,
and bad otherwise. Write beta for the number of bad centers. Every
bad center contributes an integer at least one, hence beta<=H.

At a good a in A, the high point u is isolated in its high leave.
If alpha=delta_au and g=deg_G(a), where G is the positive-deficit
support on S, then alpha+g=5 because X=0. Its h=g+1 high points
have exactly g high-leave edges, all on the g saturated neighbors.
Thus g<=binom(g,2) with 0<=g<=4, forcing g in {0,3,4}.
For positive g the row is mixed with isolated deficit-two u, or unit
with isolated unit-deficit u. The same reasoning holds in B with v.

Consequently two good vertices in the same cohort A, or in the same
cohort B, cannot be joined by an S-S deficit edge. Such an edge would
have deficit one, hence multiplicity four, and positive-degree
endpoints. One of the three published shared-hub lemmas would apply.

## Every covered cohort point needs an exception or an incidence

Since c=0 and Z subset C, the number of points in C intersect
(A union B) is

    3-z.                                                  (4)

We assign each such point either to one bad center or to one actual
one-hub high-high incidence. Both assignments will be injective
within their respective target sets.

A bad covered point is assigned to itself as a bad center.
For a good covered point a in A, the other hub v is low at the
saturated center a, with leave degree one. Let y be its unique leave
partner. Since auv is covered, y is not u, so y belongs to S. Since
all triples vay with a,y in C are covered by K, the uncovered vay
forces y outside C.

The no-low-low theorem at a forces delta_ay>0: v is low there and
vy is a leave edge. Because X=0, delta_ay=1.

If delta_vy>0, then the uncovered triple vay gives a one-hub
high-high incidence centered at y, whose hub is v and whose other
saturated point is a. Assign a to this incidence.

If delta_vy=0, then y is in A or Z. But y is outside C and Z subset C,
so y is in A. The deficit edge ay cannot join two good A points,
so y is bad. Assign a to this bad center outside C.

For a good covered point a in B the same construction interchanges
u and v. It assigns a to an incidence with hub u or to a bad B center
outside C.

The assignments to bad centers are injective. Covered bad centers
lie in C, whereas targets of good points lie outside C, so these
two kinds cannot coincide. At a possible target y in A, lambda_vy=5.
The link point v at the saturated center y has leave degree one;
therefore at most one good covered A point can have vay uncovered.
The same degree-one argument applies to a target in B with hub u.
The cohorts A and B are disjoint. This proves injection into beta
bad centers.

The assignments to incidences are also injective. An assigned
incidence specifies its center y outside C, its hub, and its other
point a in C. Distinct a's give distinct incidences, while A and B
assign different hubs. In particular, no exchange of the two
saturated centers identifies two assigned incidences.

Thus at most beta points use bad centers and at most R points use
incidences. A bad center's own incidence may also be an incidence
target; the following sum allows that overlap and does not assume
these two budgets are disjoint. Combining(2)--(4),

    3-z <= beta+R <= H+R <= 2R = 2(1-z).

This implies 1+z<=0, impossible for z>=0. The c=0 case is excluded.
Together with the c=1 case, this proves m is not one.

## Corollary, validation and limits

The already committed
[absent-pair theorem8442](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/ABSENT_PAIR_71.md)
excludes m=0 under exactly the present hypotheses. Nonnegative integer
m therefore satisfies m>=2, as claimed. The earlier
[profile exclusion8820](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-1/profile_16_19_exclusion/PROOF.md)
already excludes (16,19,20^16), but is context, not a premise of the
new multiplicity-one argument. The next unrestricted two-point
frontier is (17,18,20^16), m=2; higher m and profiles with more than
two unsaturated points remain open.

The new argument has no computational search or finite exclusion
certificate. Its proof is the incidence and injection argument above.
[verify_inputs.py](verify_inputs.py) checks exact pinned dependency
bytes, the known 69-word construction, and replays the published
universal and three shared-hub certificates with their existing
controls. It does not formalize this counting bridge or rediscover
the imported classifications. All original programs, literal fixtures,
certificates and positive controls are public in the same repository;
no private input or newly generated corpus is required.

Normal and optimized-Python dependency replays passed sequentially
with one numerical thread. The known ACL69 bytes were fetched anew
and all 2346 pairs were checked literally. Exact source pins,
reproduction commands, controls and measured resources are in
[DEPENDENCIES.json](DEPENDENCIES.json) and
[VALIDATION.json](VALIDATION.json). No timeout, UNKNOWN, memory kill
or incomplete enumeration is evidence for this theorem.

Primary literature was refreshed on 2026-10-01.
[Brouwer's maintained table](https://aeb.win.tue.nl/codes/Andw.html)
still records 69--72; [Aw--Chee--Ling2003](https://ymchee66.github.io/home/PDF/6cwc.pdf),
Theorem1/AppendixA supplies the known 69-word construction;
[Brouwer1975](https://ir.cwi.nl/pub/6883/6883D.pdf) supplies the point
cap 20. The campaign's reviewed upper71 is separate published work.
The new restriction is relative to the cited campaign results;
literature checks do not establish historical novelty.
