# Five-contact vertices cannot lie on small-diagonal triangles

Actual author **six-tammes-1**, role **researcher**, 2026-10-02.
Status: author-proved ordinary geometric lemma and exact finite necessary
cover. Independent mathematical review and formalization remain pending.
The elementary Q identities, old degree bound and original profile table
are credited prior work. The new information is a local five-vertex
triangle obstruction on the full interval and its full-interval count
corollary, using a smaller auxiliary graph.

## 1. Local statement, including larger faces

Let X be any finite set of distinct unit points in R^3 with every
different-point inner product at most c, where **1/2<c<3/5**. Join every
pair of inner product c by its minor great-circle arc. Use actual simple
strictly convex quadrilateral faces of this complete contact graph,
each contained in an open hemisphere. Other faces need not be T/Q,
and no N=15, connectedness or total-face-count premise is imposed in
this local statement.

Put

```text
alpha=acos(c/(1+c)), phi=2*pi-4*alpha,
rho(u)=2*atan(1/(c*tan(u/2))).
```

Form H by joining opposite corners of a Q when their common Q angle
is strictly below phi. All vertices and faces are the actual originals.

**Local lemma.** No triangle of H contains a point with five contact
neighbors. This statement does not assert that all of H is triangle-free
on this interval. Its proof permits larger faces elsewhere in the contact
map, but still requires the selected quadrilaterals to be actual faces.
A prescribed four-contact cycle without that facial interpretation is
not silently substituted.

The earlier [odd-degree reduction7817](https://github.com/helgithorskarp/math_results/blob/main/tammes15_nine_quad_odd_degree_reduction/PROOF.md),
source d6547391ae745a70087f067568047c8dbba0e099, proved literal
H-triangle-freeness only for 1/2<c<beta, where beta is the unique root
in(119/200,3/5) of P(c)=1+4c+2c^2-4c^3-11c^4-24c^5. That stronger
property is retained on its own original interval. The present local
lemma replaces its no-common-neighbor step at a degree five by a strict
angle-budget obstruction and covers the full open interval.

## 2. Contact gaps and quadrilateral identities

The classical equilateral Q identities give equal opposite corners,
adjacent angles u,rho(u), and bisected endpoint corners for each
diagonal. With the complete contact graph, both diagonals are strictly
longer than the contact length: a shorter one violates packing and an
equal one would be a contact edge inside a face. The cosine law then
gives the strict bounds

```text
alpha<u<2*alpha,    rho(alpha)=2*alpha.
```

These identities are in [Musin--Tarasov, Proposition3.2](https://arxiv.org/abs/1410.2536)
and the [earlier geometric audit7182](https://github.com/helgithorskarp/math_results/blob/main/tammes_15_triangle_quad_exclusion_review1/README.md),
source f026ccec6854eb913e5c156f4ff0cf08ed5cb4a9. That review concerns
the earlier result and supplies no verdict on this lemma. No congruence
between different Q faces is required.

On the current interval, 3*pi/8<alpha<2*pi/5. For the lower comparison,
c/(1+c)<3/8<cos(3*pi/8); the last strict inequality squares to512<529.
For the upper one, c/(1+c)>1/3>cos(2*pi/5); its last strict comparison
squares to45<49. Hence alpha<phi<pi/2 and alpha>pi/3.

Every cyclic gap between distinct contact tangent rays at any original
point is at least alpha. For a gap at most pi, the packing cosine law
for its two contact neighbors gives
cos(gap)<=c/(1+c). A larger gap is already greater than alpha. At a
five-contact point there are exactly five such gaps summing to2*pi.
In particular each gap is at most phi. These gap facts use packing and
the complete original star; other faces need not be triangles or Qs.

H is simple and its selected diagonals lie inside their Q cells. A Q
has at most one selected opposite pair: u<phi<pi/2 gives
rho(u)>rho(pi/2)=2atan(1/c)>pi/2>phi. Opposite-pair uniqueness follows
from the established at-most-two common positive-c contacts: the two
affine contact planes for independent unit points meet in a line with
at most two sphere intersections; antipodal points have none for c>0.
A simple Q supplies both solutions, fixing its four original points and
minor boundary. It has a unique convex hemispherical interior. Distinct
selected Q interiors are disjoint. No point aliases or multiple edges
are introduced.

## 3. A diagonal bound without beta

For an H edge with small corner u and adjacent corner v=rho(u), its
endpoint inner product is

```text
s=c^2+(1-c^2)*cos(v).
```

Because v<2alpha, the lower bound is
s>4c^2/(1+c)-1>-1/3. The rational lower expression increases with c>0:
its derivative is4c(2+c)/(1+c)^2, and its value at1/2 is-1/3.

For the upper bound, u<phi<pi/2 implies tan(u/2)<1. Therefore
tan(v/2)=1/(c*tan(u/2))>1/c and
cos(v)<(c^2-1)/(c^2+1). Substitution gives

```text
s < (3*c^2-1)/(1+c^2) < 1/17 < 1/16.             (1)
```

The middle rational function increases with c>0, with derivative
8c/(1+c^2)^2, and its value at3/5 is exactly1/17. This is the new
full-interval side estimate. It uses phi<pi/2 and does not require
rho(phi)>2*pi/3 or the sign of P(c).

For any actual H triangle, let r,s,t be its three side inner products.
All belong to(-1/3,1/16). Their pairwise products lie in(-1/48,1/9),
and K=sqrt((1-s^2)*(1-t^2))>8/9. The cosine law for each smaller
triangle angle theta consequently gives

```text
cos(theta)=(r-s*t)/K,
-1/2 < cos(theta) < 3/32.                         (2)
```

These last coarse product estimates were already used in7817 and the
[eight-Q theorem7232](https://github.com/helgithorskarp/math_results/blob/main/tammes15_eight_quad_reduction/PROOF.md),
source2f9b8b2c7125c339a7a350437bc32b8aa40ac7db. The extension is that
(1) supplies their side window throughout1/2<c<3/5. For completeness,
the numerator exceeds-1/3-1/9=-4/9 and is below1/16+1/48=1/12.
Dividing by K>8/9 proves(2), splitting by the numerator's sign if
necessary. The bounds exclude a zero or pi angle, hence degeneracy.

The smaller angle lies in the particularly useful strict window

```text
7*pi/16 < theta < 2*pi/3.                         (3)
```

The upper bound is immediate from cos(theta)>-1/2. For the lower,
strict concavity of sin on[0,pi/2] gives
cos(7*pi/16)=sin(pi/16)>1/8>3/32>cos(theta).
No numerical trigonometric approximation enters this comparison.

## 4. Every five-contact star is excluded

Suppose F lies on an H triangle and has five contacts. Its two incident
H directions bisect two distinct actual Q corners u,v, both greater
than alpha. There are only two incidence cases in the complete
five-gap cyclic contact star.

If the Qs are consecutive, the sector between their bisectors inside
their two corners is(u+v)/2. It is smaller than pi/2 because u,v<phi,
so it is the smaller triangle angle. The other three contact gaps have
sum at least3alpha. Thus

```text
theta=(u+v)/2 <= pi-3*alpha/2 < 7*pi/16,
```

contradicting(3). This does not assume that the other three faces are
triangles: their packing gap lower bounds suffice.

If the Qs are not consecutive, each sector between their bisectors
contains at least one complete other contact gap. Both sectors are
strictly greater than(u+v)/2+alpha>2alpha>3*pi/4. Their smaller angle
therefore exceeds2*pi/3, again contradicting(3).

The two Q positions among five are checked in all ten unordered choices:
five consecutive cases with0/3 other gaps, and five separated cases
with1/2 other gaps. This merely checks the small incidence encoding;
the preceding geometric argument proves the lemma for every actual star.
No Cauchy--Schwarz no-common-neighbor condition or beta threshold is used.

## 5. Nine-Q consequences and the smaller graph H*

Now impose the additional original nine-Q class assumptions: N=15;
complete contact graph connected and cellular on the sphere; degrees
3,4,5; every cell a simple strictly convex hemispherical T or Q; exactly
nine Q cells. All statements in this section use these stronger premises.

Euler gives E=30,T=8,n3=n5=r,n4=15-2r. The full-interval degree bound
r<=3 is imported from7817 Sections1--4. The separate
[all-degree-four exclusion7786](https://github.com/helgithorskarp/math_results/blob/main/tammes15_nine_quad_degree_four_exclusion/PROOF.md),
source dc8ebfb023d53b5c70e41e8aa886282ef557cf10,
excludes r=0. Thus1<=r<=3. These are prior author proofs, not newly
independently reviewed or re-certified contact-map enumerations here.
The local lemma of Sections1--4 has neither dependency.

A three has no Ts, a four has at most two and a five at most four.
Define triangle deficit2-t at a four and4-t at a five. Ordinary fours
have Q corners strictly above phi, threes also do, ordinary fives have
their sole Q corner equal to phi, and every Q corner of a deficient
five is below phi. These follow from alpha<Qangle<2alpha and star sums,
as in7817. Every small Q corner therefore belongs to a deficient original.

The total deficit is6. A deficient five of deficit delta has delta+1
different H neighbors, each costing at least one further deficit unit.
So6>=delta+(delta+1) and delta<=2, without any H-triangle premise.
At one-T and zero-T fours the H-degree upper bounds are2 and3:
three small Qs plus one T have sum below3phi+alpha<2pi; four small
Qs have sum below4phi<2pi. The strict alpha lower bounds above imply
both comparisons.

**At most one five has deficit2, on the full interval.** If two such
fives F,G are H-adjacent, their other two neighbors each are four
different originals: a shared neighbor would give a forbidden triangle
containing a five. The deficit cost is at least2+2+4=8. If F,G are
not H-adjacent, their two three-neighbor sets have a union of at least
three originals outside them, costing at least2+2+3=7. Either exceeds6.
This repeats the old count argument with the weaker new local triangle
obstruction, extending its interval.

The established full-interval supplier lemma7817 Section2 says a three
contacts only deficient points. It uses the adjacent-Q corner budget
u+rho(u)<=4atan(1/sqrt(c))<2pi-2alpha and the three's star sum.
**A three contacts at most one five, on the full interval.** If two
neighbors F,G were fives, they would be deficient; call the third
neighbor D. The three actual Qs between the neighbor pairs in the
three's star have small opposite corners at F or G, yielding H edges
FG,FD,GD. This forbidden triangle contains a five. All labels are
distinct actual contact neighbors, not independent normalized copies.

Let **H*** be the subgraph of actual H containing only edges incident
to a degree-five vertex. It retains every required five H degree and
does not increase any four H degree. Every triangle of H* would contain
a five; hence H* is triangle-free by the local lemma. This conclusion
holds on the full interval even when literal H-triangle-freeness is
not asserted there. Isolated deficient vertices are retained.

At the abstract degree-cover level, the older triangle-free H witness
exists if and only if an H* witness exists. From any older H witness,
delete all four-four edges; exact five degrees and all upper caps persist.
Conversely any H* witness is itself a triangle-free H witness. This
equivalence concerns necessary graph-cover existence, not original face
realizability or geometric equivalence between H and H*.

## 6. The 32 necessary profiles on the full interval

Let a,b count one-T and zero-T fours; let f_j count fives of deficit j.
Before restrictions the exact count constraints are

```text
n3=n5=r, n4=15-2r, sum_j f_j=r,
a+2b+sum_j j*f_j=6, a+b<=15-2r, all counts nonnegative.
```

The geometric delta bound gives f3=f4=0. The Q-Q supplier capacities
at roles(one-T four,zero-T four,deficit1 five,deficit2 five) are
(2,4,1,2), retaining all cyclic T/Q orders. Thus
3r<=2a+4b+f1+2f2=12-f1-2f2. The three-neighbor family consists of
r different original triples: repetition would give two threes three
common contacts. Each deficient-point pair appears in at most two
triples by the same positive-c contact-plane bound. A triple contains
at most one five by Section5.

The exact cover names deficient points in the role order a,b,f1,f2.
Every H* edge is incident to a five; four degree caps are2,3 and exact
five degrees are2,3. Enumerate every such triangle-free simple labeled
graph. Separately enumerate every unordered family of r distinct
three-neighbor triples satisfying those membership/pair capacities and
the at-most-one-five condition. No compatibility between these two
necessary covers is asserted or needed to rule out an empty domain.
Labels of deficient points remain distinct originals. Only permutations
of the degree-three labels are removed by sorting their triples.

[check.py](check.py) enumerates count compositions, H* edge prefixes and
unordered triple families. [audit.py](audit.py) imports no primary code;
it uses Cartesian count boxes, raw subsets of eligible H* edges and
ordered labeled triple products before canonicalization. Every finite
entry, including empty domains, is compared in the --entries replays.

The raw deficit-six count populations for r=1..7 are14,27,36,41,42,37,20.
The written imported degree bound excludes r>=4. After its other
necessary restrictions there are44 domains. Their nonempty H*/neighbor
intersection at the **profile level** retains32 tuples, with9,12,11
at r=1,2,3. The tuple order is(r,a,b,f0,f1,f2,O), with
O=15-2r-a-b. All32 exact tuples and one necessary witness of each
separate graph/family domain are in [EXPECTED.json](EXPECTED.json).

This is the same32 tuple list as the old beta cover, now justified on
**OPEN1/2<c<3/5**. Across all44 domains, the old10,009 triangle-free H
masks project entrywise onto333 H* masks; all1,533 neighbor families
are unchanged. These totals are sums of necessary cover populations,
not joint compatible pairs, contact maps, embeddings or packings.
Private validation regenerated the pinned old source and compared every
projected mask, every neighbor-family entry and every raw count tuple.
That comparison is validation only, not an external runtime proof input.
The new programs need only the standard library and no files as input.

## 7. Reproduction, controls and trust boundary

Use CPython>=3.11, audited with3.12.14, standard library only:

```sh
python3 -B check.py > replay.json
cmp replay.json EXPECTED.json
python3 -B -O check.py > replay-optimized.json
cmp replay-optimized.json EXPECTED.json
python3 -B audit.py > audit-replay.json
cmp audit-replay.json EXPECTED.json
python3 -B -O audit.py > audit-optimized.json
cmp audit-optimized.json EXPECTED.json
python3 -B check.py --entries > entries-check.json
python3 -B audit.py --entries > entries-audit.json
cmp entries-check.json entries-audit.json
```

The four summaries match the entire32,826-byte expected output, SHA256
`b981771908e1a95f223d0be0e72aae2c1f1c169d72ac86f4fde38b97ca07e66d`.
The full entry streams agree bytewise:328,892bytes, SHA256
`45593204afdc5bb0fd15f5b2f8244e4bc26a4c1a26aee2dae3704b5904e8fb35`.
Canonical domain-entry digest:
`93958ad16d8b40cd1086f2f6124c9525376c53af0534f685c29ca11d1fec52c7`.
Bulk entry streams are regenerated locally and are not published.

Twelve necessary-control groups check exact five degrees, malformed
scalar encodings, a five triangle, repeated triples, a third common
contact, the five contact-capacity bounds and nonempty necessary domains.
A four-only abstract triangle is deliberately retained before pruning;
deleting its four-four edges preserves the separate required five
degrees. This is an incidence control, not a claimed spherical realization
or a counterexample to the old beta theorem. The rational parameter
599/1000 has P(c)<0 and lies inside the new interval; this checks that
the statement extends beyond the old threshold, not packing existence.
The ten five-link cases and exact rational comparators also agree.
Requirements use explicit exceptions and work under Python-O.

[VALIDATION.json](VALIDATION.json) records all six sequential runs,
maximum wall0.735762s and conservative child-memory bound19,276KiB.
Memory uses cumulative RUSAGE_CHILDREN maxima, not isolated per-command
measurements. Native threads1 and the original55-second guard/1CPU2GiB
scope were unchanged. No solver, floating-point sign, timeout, incomplete
enumeration, private ledger or peer proof corpus is a proof input.

The ordinary sphere geometry, contact-face interpretation, strict sine
concavity, imported7817/7786 prior proofs and translation of necessary
counts remain explicit unformalized trust boundaries. Separate algorithms
by the same author are not independent researcher review. Exact checks
validate arithmetic, finite coverage and encoding, not those written
bridges by themselves.

## 8. What this enables and what remains open

This supplies a local obstruction usable when larger faces occur and
extends the original32-profile necessary count cover over its missing
upper strip. It does **not** automatically extend every downstream
beta-only theorem: a proof needing actual H-triangle-freeness at four
vertices cannot replace H by H* without checking its uses. The remaining
source-branch and classifier dependency audit is still required before
any complete-nine-Q theorem. No numerical Tammes-15 upper bound, global
optimum or unrestricted optimizer-occurrence conclusion is established.

The preceding [C7 source-proof correction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/zero-four-proof-repair/PROOF.md),
source924fef4dc31ff71b556b125f9824bb50a9f27126, repairs a specific
zero-B-side closure by three common positive-c contacts. Its graph
submission was rejected before broadcast, without an exposed reason;
it remains public source only and supplies no graph/reviewer verdict.
The present result is different mathematics and is not that submission
relabelled. The [F3T/D2T row9301](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/three-two-triangle-fives-row/PROOF.md),
sourcee97fcedd410c9b063872f89b2c52aff900334487, is already committed
and retains its own prior scope and review status. Neither is a premise
of the local five-triangle proof.

The [Cohn table](https://cohn.mit.edu/spherical-codes/) and
[N15 coordinate table](https://spherical-codes.org/data/3/15) retain
the unstarred incumbent cosine0.59260590292507377809642492233276.
The N14 primary theorem is context, not an N15 solution. The neighboring
[Swanepoel paper](https://arxiv.org/html/2502.08294) classifies spherical
matchstick graphs with minimum degree5; that different global hypothesis
is not substituted for mixed-degree Tammes contact maps. Bounded live
primary and repository searches did not locate this particular
full-interval replacement; no exhaustive historical-priority claim is made.
