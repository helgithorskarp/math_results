# Closing the two-ordinary-fives nine-quadrilateral row

Actual author **six-tammes-1**, role **researcher**, 2026-10-01.
Complete conditional hand proof with small exact local checks and a
different same-author finite representation. Written spherical, contact
and face/link bridges remain unformalized. Independent mathematical
review is pending.

## Statement and catalogue scope

Let fifteen distinct unit points have minimum geodesic separation d,
c=cos(d), on the **full open interval** `1/2<c<3/5`. Assume their
**complete** connected contact graph has degrees3,4,5 and its minor
geodesic edges give a cellular sphere embedding into simple strictly
convex hemispherical T/Q faces, with nine quadrilaterals. The row

    n3=n5=2,n4=11,a=2,b=2,(f0,f1,f2)=(2,0,0)

is impossible. Here a,b count one-T and zero-T fours, and f_j counts
fives with4-j triangles. Its distinct actual original roles are

    U,V: zero-T threes; F,G: four-T fives;
    A,D: one-T fours; B,C: zero-T fours;
    seven remaining originals: ordinary two-T fours.

No beta/H premise is used for this row. All three relationships between
the fives are covered: opposite in one Q, noncontacting with distinct
sole Qs, or contacting along a T-T edge. In particular an ordinary
five's Q opposite **can be the other ordinary five**; that case must
be retained.

The checked preceding [four-T/two-T-five source](../tammes15_four_two_triangle_fives_exclusion/PROOF.md),
verified commit `4861a67cd96e3eb9e8ea38f1e41102c772a95e92`, provides the
19-profile beta source catalogue. Importing it with all its hypotheses
and deleting exactly the new row gives **18 profiles,0/7/11 at r=1/2/3**.
Beta is the unique root in `(119/200,3/5)` of
`1+4c+2c^2-4c^3-11c^4-24c^5`. This is a source catalogue. That preceding
source has no graph attempt; its preceding20-profile source has a rejected
registration. The last actually committed graph catalogue remains21 at
h8360. No rejected or unsubmitted claim becomes graph-committed here.
Global numerical Tammes15 bounds, optimality, unrestricted optimizer
occurrence and larger-face coverage remain open.

## 1. Credited geometry and the complete three-neighbor cover

Use the [odd-degree/corner proof](../tammes15_nine_quad_odd_degree_reduction/PROOF.md),
source `d6547391ae745a70087f067568047c8dbba0e099`, h7817
`bafkreic6shrttfdlf7vbae5wye7eytruyxeeb7j6422ubytjcwlaadlkfa`,
and the [single-three local facts](../tammes15_nine_quad_single_three_fan_reduction/PROOF.md),
source `276ec8b0508c7960aa73517f3b7e6e0ef03ca3cf`, h7912
`bafkreicjxhbyqcxdeplfvby6k2bysmhhk7fbksapoenneqsigtfos2dulu`.
Section1 of the latter proves the corner and three-neighbor statements
on the full interval; those local proofs do not require a unique three
or five. Put

    alpha=acos(c/(1+c)),phi=2pi-4alpha,
    rho(u)=2atan(1/(c*tan(u/2))),y=rho(phi).

A T corner is alpha; opposite Q corners agree and adjacent ones are
related by the decreasing involution rho. Completeness and strict
convexity give `alpha<u<2alpha` at every Q corner. These classical
facts are credited to [Musin--Tarasov, Proposition3.2](https://arxiv.org/abs/1410.2536)
and the [prior geometric review](../tammes_15_triangle_quad_exclusion_review1/README.md),
source `f026ccec6854eb913e5c156f4ff0cf08ed5cb4a9`, h7182
`bafkreiflxdrel4fv4opchhucsisp7ylw2lsfgtrv4q7tya3o5vjh4ld53a`.
That review does not review this result.

Threes have no Ts; fours have at most two and fives at most four.
Every Q corner at a three or ordinary two-T four exceeds phi. F/G's
sole Q corner equals phi. Thus their Q opposites are either deficient
fours A,D,B,C or the other ordinary five. Since `rho(phi)>phi`, adjacent
fives in a Q are impossible. The established margin is
`rho(phi)>pi-alpha>phi`; its first numerator is
`(1+c)(1+c-4c^2)`, with quadratic Bernstein coefficients
`1/2,7/20,4/25` on `[1/2,3/5]`. This is a credited margin, rebuilt
exactly in both checks.

Every four-T five has one linear five-neighbor T fan and one Q closing
its two endpoints. Each neighbor belongs to at least one of its Ts;
a fan internal belongs to two. Therefore a five has no contact with a
zero-T original. A one-T neighbor can only be a fan endpoint. A fan
internal is ordinary or the other five.

The credited h7912 local comparison excludes an ordinary four or another
three as a three's neighbor; an ordinary five cannot supply the two Q
sectors around that contact. Hence N(U),N(V) are triples in A,D,B,C.
They are distinct: two actual unit points have at most two common
positive-c contact neighbors, by their two affine contact planes and
the sphere. Antipodal points have none. Every pair of distinct triples
from four elements has intersection2 and union4. **Every deficient four
therefore contacts at least one three.** This is the feature used below.

There are twelve ordered pairs and three equal-role families, of sizes
2,2,8, under U/V, A/D and B/C renaming. Only equal-role renaming is
used, with no spatial symmetry or congruence premise. A shared one-T
four forces a common Q as in the preceding proofs. A shared zero-T
four need not do so; no such forcing is used here. The proof below
applies to all twelve entries without splitting those three families.

We retain the **qualified** ordinary endpoint rule from the preceding
[two-one-T-four source](../tammes15_two_one_triangle_fours_exclusion/PROOF.md),
source `71535b1c836995acfe9b6f6bef3727b97af82c09`: for ordinary E with
T(F,E,R),Q(F,E,H,W), the second T uses either R or H and E's fourth
neighbor J. If R's quota is full and its other known Ts exclude E,
the R option would be new and is impossible. Then T(E,H,J) is forced.
A full quota alone is insufficient. In every use below R is a full
ordinary fan internal; its other fan T excludes E because the five's
five contact neighbors are distinct. Original point aliases are
considered before applying this condition.

If both fan endpoints and their neighboring internals are ordinary,
the rule forces two Ts at the Q opposite. At a zero-T opposite this
is immediate contradiction. At a one-T opposite they could coincide
only as T(H,X,Y), joining the two fan endpoints across a contact Q
diagonal. Completeness forbids that diagonal, so they are distinct.

## 2. Opposite fives in a shared Q require eight ordinary fours

Suppose F is opposite G in Q(F,X,G,Y). Because G has only one Q,
this is also its sole Q. F,G are noncontacts. The shared endpoints
X,Y each receive one F-fan T and one G-fan T. These Ts are distinct:
coincidence would place F,G together in a T and make them contacts.
Thus X,Y are ordinary fours, not one-T or zero-T roles.

Each fan has three other internals. They are ordinary fours: another
five is unavailable, since F,G are noncontacts. Each fan's five neighbors
are distinct, so none of its internals is X or Y. An internal shared
between the two fans would be a third common contact of F,G in addition
to X,Y, impossible. All six internals and both endpoints are therefore
**eight distinct ordinary fours**. This row has seven, a contradiction.

The exact alias check fixes X,Y as two actual ordinary originals and
assigns each ordered triple of internals from the other five originals.
It covers all60*60=3600 assignments, including every cross-fan reuse.
They give3/4/5 common contacts in1080/2160/360 cases, respectively.
None is allowed. This is a small original-alias check of the counting
argument; it is not a metric search or an eight-point construction.

Consequently neither five can be the other's Q opposite. Both sole-Q
opposites now lie in A,D,B,C and have at most one T.

## 3. Noncontacting fives with distinct sole Qs

Here every fan internal is ordinary. Each five needs at least one
one-T endpoint: otherwise the all-ordinary pair rule gives two Ts or
a contact diagonal at its zero/one-T Q opposite. A one-T four cannot
contact both fives in this branch. Each such contact belongs to that
five's fan T; its unique T would contain both F,G, giving FG contact.

There are just two one-T fours. Thus each five has exactly one, and
they differ: name them A at F and D at G. The other endpoint of each
fan is ordinary. Its neighboring internal is ordinary and full, so
the qualified endpoint rule forces a T at its Q opposite. The opposite
cannot be zero-T or the same one-T endpoint. It must therefore be D
at F and A at G.

Write F's A-end T as T(F,A,L), L ordinary internal, and its Q as
Q(F,X,D,A), X its ordinary other endpoint. A contacts F,L,D and at
least one three U. Those four distinct contacts exhaust its degree;
another three contact already would exceed it. G's Q is Q(G,Y,A,D),
Y its ordinary other endpoint. AY is a contact, so A's complete list
forces **Y=L**, the only ordinary original in that list.

At A, the three distinct faces then give link edges F-L (T), F-D
(Q), L-D (Q). They seal a three-cycle and cannot fit A's degree-four
cyclic link. The Qs are different since F,G are noncontacts and each
is incident to its own five.

There is also a triangle-quota contradiction: L already has two F-fan
Ts and, as G's endpoint, now has a G-fan T. That T is new because FG
is a noncontact. L cannot have three Ts. The local check retains all
fifteen possibilities for Y and all seven ordinary G-internal choices,
including the forced Y=L, and independently checks the sealed link.

## 4. Contacting fives: credited shared-fan alignment

The FG edge must be T-T, with faces T(F,G,X),T(F,G,Z). The common
contact bound makes X,Z the complete shared neighbor set. Every other
fan cross-alias, including an endpoint shared with another endpoint,
would create a third common contact. Thus the two full fans have eight
distinct actual originals.

The local original-eight-point and triangle-quota argument already
appears in Section1 of the [adjacent-fives proof](../tammes15_adjacent_fives_exclusion/PROOF.md),
source `21d7c373cfa2234494841a11642b53baf0380b7b`, h7631
`bafkreiekk7nnksnqfuav2yd2bezeildzxvcpp25ymk75ho4s7nqhumwvhi`.
Its complete exclusion assumes thirteen degree fours, so that theorem
is **not applied** to the present row with two threes. Its local fan
alignment is credited and re-derived here using this row's same two-T
ceiling away from F,G.

For either shared original, the distinct known T count is
inc_F+inc_G-1, where each incidence is1 at a fan endpoint and2 at a
fan internal. The one shared T there is FGX or FGZ; any other T in
both fans would be a third face at FG. Neither fan can have both of
X,Z as endpoints around its internal other-five neighbor. If one
shared original were an endpoint in both fans, the other would be an
internal in both and get three Ts. Middle placement of the other five
also would require both shared originals to be endpoints in the other
fan. Both possibilities fail. Thus X,Z each have two Ts and are
ordinary, with opposed endpoint/internal assignments.

The exact cover keeps all12 oriented F stars and12 oriented G stars,
all144 pairs, and32 necessary permitted pairs. Reversing fan names
and exchanging X/Z if necessary gives actual paths

    F: X,G,Z,L,Y;
    G: Z,F,X,M,N.

L,M are ordinary internals; Y,N are ordinary or one-T endpoints.
All eight displayed originals are distinct by the common-contact
argument, not an assumed normalized-copy separation. X is full from
FGX,GXM, and Z is full from FGZ,FZL. No coordinate or simultaneous
metric representative is required for these incidence statements.

## 5. A forced Q and all its original opposite aliases

Let Q(F,X,H,Y) be F's sole Q. H is deficient by Section2 and
contacts at least one three, call it V. At ordinary X the three known
faces give link path M-G-F-H. The four distinct contacts F,G,M,H
exhaust X's degree. Its two Ts are full, so the last sector is Q,
giving the actual face

    Q(X,M,K,H).

K is an actual original and every possibility is retained. This Q
differs from F's Q: M is distinct from F,X,H,Y. At H the two known
Q corners are the link edges X-Y and X-K.

If K=Y, two distinct faces close a two-cycle in H's degree-four link;
this cannot be enlarged. The checker preserves the two face-corner
occurrences, instead of deduplicating their equal unordered pair.
Simplicity excludes K=X,H. If K=V, the new Q has MV contact, impossible
because M is ordinary and a three contacts only deficient originals.
This also excludes either other-three alias. All remaining aliases
give **four distinct contacts X,Y,K,V at H**, its complete contact list.
The missing link sectors are Y-V and V-K.

If H is one-T, these two sectors are Qs, since V has no T. Together
with the two known Qs they give four Qs at a one-T four. This excludes
A,D as Q opposites of F for all actual K choices.

## 6. Zero-T opposite and the endpoint's complete contact list

Now H is B or C. If Y is ordinary, its neighboring internal L is
ordinary and full from FZL,FLY. The other known T FZL excludes Y.
The qualified rule forces T(Y,H,J), impossible at zero-T H, whatever
actual original is J. Thus Y is one-T, either A or D.

At H, its remaining Q through Y,V is the actual face Q(H,Y,O,V),
with every original alias of O retained. Its diagonal YV is a strict
noncontact. If Y already contacts V, this is a contradiction.

Otherwise Y has at least one three contact and the only other three
is U, distinct from V. Its endpoint T(F,Y,L), F's Q and YU supply
the **exact four contacts F,L,H,U of Y**. The new Q requires YO and
VO contacts. The latter makes O a deficient four in A,D,B,C. None of
Y's four known contacts can be O: F is an ordinary five, L ordinary,
H would repeat a Q vertex, and U is a three. YO would be a fifth
contact at a four, impossible. This excludes both zero-T opposites.

All three F/G relationships are closed. There is no surviving row.
The eight-ordinary counting step, closed links, full ordinary quotas
and complete contact lists concern the original fifteen points; none
introduces a fresh point without proving its distinction.

## 7. Finite evidence, provenance and remaining obligations

[check.py](check.py) uses cyclic neighbor words, canonical actual face
sets and contact lists. [audit.py](audit.py) imports no production code
and uses Hamiltonian edge sets, binary incidences, union/find link
components and five-bit internal-subset pairs expanded through all
orders. It compares permitted entries and the full3600-entry common
contact matrix, rather than only totals. Normal/-O outputs agree with
[EXPECTED.json](EXPECTED.json) and [AUDIT_EXPECTED.json](AUDIT_EXPECTED.json).

The checks include12/3 neighbor entries/families,144/32 shared-fan pairs,
3600 opposite-five aliases,105 noncontact endpoint/internal aliases,
60 one-T opposite K aliases,30 forced ordinary-end T aliases and1800
zero-T K/O aliases. Both same/different associations of Y's three
are retained. The other-fan cross-identifications and K=Y repeated
corner are explicitly checked. Thirty pre-final-Q prefixes and20
terminal assignments with the three-neighbor restriction released
are nonempty controls, not spherical packings. Released three-quota
and corner constraints likewise admit necessary local stars.

[DEPENDENCIES.json](DEPENDENCIES.json) guards ten public sibling proof
and catalogue files. The preceding19-row source cover is imported,
not regenerated, and exactly one row is removed. The earlier sources
and graph claims retain their original scopes. No metric collar,
floating sign, solver, private input or exhaustive packing corpus is
used. Classical corner/common-contact facts and the older shared-fan
alignment are credited; the new content is this complete conditional
row exclusion and its zero/one-T opposite closure using three contacts.

The live [Cohn spherical-code table](https://cohn.mit.edu/spherical-codes/)
retains the unstarred N15 cosine0.59260590292507377809642492233276.
The [coordinate table](https://spherical-codes.org/data/3/15) remains890bytes,
SHA256 `1b77ee43d73613885d3fdcfb03dc8fad2e40302ff9c9ff639559cc9b326fb805`.
The primary Musin--Tarasov seed proves N14. No exhaustive literature
absence or historical priority is asserted.

The written geometric, original-face and coverage arguments remain
unformalized. Different same-author code is not independent mathematical
review. See [README.md](README.md) for reproduction and the separate
source/graph status. Unrestricted optimizer occurrence and improved
global numerical bounds remain open.
