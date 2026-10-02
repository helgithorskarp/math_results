# Arbitrary three-point completion of twelve fixed incumbent points

Actual author **six-tammes-2**, role **researcher**, 2026-10-02.
Exact algebraic certificate plus an ordinary convexity/cap proof.
All 1,014 active-plane predicates were actually executed. Independent
researcher review and formalization of this new result are pending.

Let tau be the unique root of
`F(t)=13t^5-t^4+6t^3+2t^2-3t-1` in
`(0.59260590292507377809642492233275,0.59260590292507377809642492233276)`.
Write `<a,b>=a^T H b`, with `H=(1-tau)Id+tau J`, in basis
`(p0,p5,p11)`. Define the fifteen reference coefficient vectors p_i,
normal n, and alternative c14 by [INPUT.json](INPUT.json).
These are credited known incumbent data, not a new construction.
The checks supply the root signs, unit identities and all packing products.
Only the twelve points with labels
`C={0,1,2,4,5,6,7,8,9,10,11,12}` are fixed hypotheses below.
Let q be the intersection of `<p8,q>=<p9,q>=<p11,q>=tau`.
Its three normals are independent; the certificate proves q is unit.

**Exact completion theorem.** A unit tau-code containing these twelve
fixed points has at most three additional points. Its unordered three-point
extensions are exactly

`{p3,a,b}`, where `a in {p13,q}` and `b in {p14,c14}`.

All four are feasible. Complete Gram equalities identify three with the
known asymmetric reference and one with the known cyclic reference, up to
O(3) and relabeling. This does not produce a new incumbent or a global bound.
The positions of the twelve fixed points are essential hypotheses; bare
twenty prescribed contacts do not impose these positions.

**Stability theorem.** If three arbitrary unit vectors have all products
against the fixed twelve and against each other at most `tau+delta`, with
`0<=delta<=1/10000000`, then, after exchanging the three labels, their
maximum Euclidean distance to one of the four displayed triples is at most
`2100000 delta`. Distances use H in coefficient coordinates.

Consequently, if twelve points of an actual fifteen-point unit code are
within eta of these fixed reference points after O(3) alignment, and its
pair parameter is at most `tau+epsilon`, where epsilon>=0 and
`eta+epsilon<=1/10000000`, the three other points obey the same conclusion
with delta=eta+epsilon. This follows by the unit-vector product error bound.
No contact support or minimum degree is imposed on the added points.

## Complete exact polytope calculation

Set b=667/250 and define

`P={x:<p_i,x><=tau for every i in C}`,
`K=P intersect {x:<n,x><=b}`.

Zero is strictly feasible. The retained vectors p0,p1,p2 are independent,
and strictly positive w0,w1,w2 satisfy
`w0 p0+w1 p1+w2 p2+p5=0`. The checker verifies the homogeneous Cramer
identities and signs. Multiplication by invertible H preserves them.
A recession direction would have nonpositive products against all four
normals; positive dependence then makes all four zero, so the direction
is zero. Thus P, K and the later avoidance polytopes are bounded, full
dimensional polytopes and convex hulls of their vertices.

Every vertex has an independent active triple of normals. The certificate
enumerates EVERY triple, without symmetry reduction. For rows M and
right side h it computes determinant D and homogeneous Cramer vector U.
If D=0, this triple cannot independently specify a vertex; another active
basis still covers any actual vertex. Otherwise the candidate is U/D.
A literal either proves a strict violated inequality with the correct D
sign, proves a strict short norm, or identifies an exact advertised unit
vector by U=Dv. Short and unit literals also check every feasibility
inequality exactly. The complete executed census is:

| target | triples | singular | infeasible | short | unit |
|:---|---:|---:|---:|---:|---:|
| K |286|5|259|19|3|
| P with p3,p13 added as constraints |364|6|334|22|2|
| P with p3,q added as constraints |364|6|334|22|2|

These are counts of active triples and checked witnesses; the proof does
not infer completeness from counts alone. The exact combination list and
typed literals in [PLAN.json](PLAN.json) give coverage. For K the short
squared norms are strictly below 99/100 and the only unit candidates are
p3,p13,q, at triples (1,4,7),(2,8,9),(8,9,11).
For each fourteen-plane target the short norms are strictly below 3/4 and
the unit candidates are p14,c14, at triples (0,3,6),(3,4,6).

All operations are over rational coefficient polynomials modulo F.
Zero remainder gives an identity at tau. Every nonzero sign is enclosed
at the exact rational root bracket; an unresolved sign aborts.
Every inverse is verified by an exact product identity. No irreducibility
premise or floating sign is needed. H is positive definite since tau<1.

Strict convexity now proves `K intersect S_H={p3,p13,q}`.
Indeed a convex combination of vertices of norm<=1 has norm<1 if it
puts positive mass on a short vertex or on two distinct unit vertices.
Each advertised unit point is feasible. The same argument gives
`P_a intersect S_H={p14,c14}` for both a=p13,q, where P_a includes
the fourteen avoidance constraints C,p3,a.

## One cap and the four completions

Exact arithmetic checks

`0<b^2<||n||^2`,
`2b^2-(1+593/1000)||n||^2>9/1000`,
`<p13,q>>97/100>tau`.

Thus any two unit points in the open cap `<n,x>>b` have product
strictly above `2b^2/||n||^2-1>593/1000`. To see this, project each
along n/||n|| and bound the two perpendicular components by
Cauchy--Schwarz. There is at most one added packing point in that cap.
Every other added point is one of p3,p13,q. The last two cannot coexist;
repeated points are forbidden by their product 1>tau. Therefore there are
at most two added points outside the cap, and at most three in all.

With three additions, exactly two are outside. They must be p3 and
one a in {p13,q}. The remaining point avoids the fourteen fixed points
C,p3,a, whose complete calculation forces p14 or c14. Conversely the
auxiliary audit verifies all 105 products for each of the four candidates.
It checks all 225 entries of each proposed Gram relabeling and reconstructs
the already known cyclic code by the credited reflection tuples. Spanning
anchors identify equal Gram matrices by O(3), rather than contact-graph
isomorphism. Hence the four labeled outcomes are the two known shapes.

## Ordinary quantitative stability bridge

The auxiliary exact checks also give squared distance>1/25 between every
two of p3,p13,q, and between p14,c14. The following mass argument uses
these gaps and the certified short-vertex bounds, not a numerical sample.

Let x be a relaxed added unit point outside the open cap, and
`y=tau x/(tau+delta)`. Then y belongs to K, since b>0. Set
`E=1-||y||^2<=4delta`; also `||x-y||<=2delta`, since tau>1/2.
In a convex vertex decomposition of y, let L be the total short mass
and alpha_i the masses on the three unit vectors. The identity

`1-||sum lambda_i v_i||^2 = sum lambda_i(1-||v_i||^2)`
`                            + sum_{i<j} lambda_i lambda_j ||v_i-v_j||^2`

gives L<=100E. Since L<=400delta<=1/2, the largest unit mass is
at least 1/6. Its cross terms against the other two unit masses, using
their squared distances>1/25, give other-unit mass<=150E. Every vertex
has norm<=1 and distance<=2 from a chosen unit vertex. Thus
`distance(x,{p3,p13,q})<=2delta+2(100+150)E<=2002delta`.

The cap still has capacity one, because tau+delta<593/1000.
Two points near the same unit choice, or near p13 and q respectively,
have product at least `97/100-4004delta>593/1000`. Among three additions
there are consequently exactly two outside the cap, within 2002delta
of p3 and one a in {p13,q}. The third point avoids all reference
points in C,p3,a with right side at most `tau+2003delta`.

For either fourteen-plane polytope, put eps=2003delta<=1/1000.
Scale the third point by tau/(tau+eps) as before. Its squared-norm loss
is at most 4eps. The short mass is at most 4E, and the product of the two
unit masses is at most 25E. Since the larger unit mass is at least 1/4,
the other is at most 100E. The resulting point distance is at most
`2eps+2(4+100)E<=834eps<1000eps`.
Hence the third point is within 2003000delta of p14 or c14; the stated
2100000delta bounds all three simultaneously. All scalar domains and
constants are checked in [audit.py](audit.py). At delta=0 this also
recovers the exact classification.

## Scope, execution and remaining frontier

[check.py](check.py) actually executed every ordinal in the complete range
[0,1014) on the final published INPUT/PLAN/field/check SHA256 pins. Every
requested predicate passed. An earlier two-slice execution was repeated only
after removing a campaign-specific path from the public wrapper; mathematical
logic was unchanged. [audit.py](audit.py) checks 1125 full-Gram
entries, 420 packing products and the stability scalar bridge;
[controls.py](controls.py) rejects 20 semantic damages and accepts two
harmless representations. Both auxiliary programs have identical normal
and optimized Python outputs. [VALIDATION.json](VALIDATION.json) records
the actual executions; hashes alone do not supply execution evidence.
The floating selector never runs in the verifier. No private forest,
coordinate table, other source module or solver is a runtime input.

This fixed-reference theorem drops one point from the earlier
[thirteen-point completion theorem](../thirteen-core-completion/PROOF.md),
and credits its cap center/method and the
[fourteen-point completion](../fourteen-point-completion/PROOF.md).
The earlier near-contact and whole-interval G22 conclusions are not
generalized or imported. All arithmetic and the ordinary proof above
are supplied here; same-author checks are not independent review.

The variable [twelve-point frame](../twelve-core-frame/PROOF.md), independently
confirmed and strengthened in [REVIEW9809](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/twelve-core-frame-audit/REVIEW.md),
is genuinely flexible. Our input fixes its incumbent specialization, with
an additional actual 6-8 contact. Neither the bare twenty-contact hypothesis
nor the [connected-map routing filter9813](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/connected-map-filters/PROOF.md)
forces this specialization. The latter provides only a necessary 11-of-52
triangle-forest profile screen in its full physical cohort.

Three-addition capacity over ALL feasible (t,z), the critical strip,
literal motif occurrence and global optimizer-cohort coverage remain open.
The new stability result is a concrete local bridge for the next interval
calculation. No global Tammes-15 bound, optimizer optimality, new construction
or historical-priority claim is made. Ordinary convexity/cap/code bridges
remain unformalized; this NEW theorem has not been independently reviewed.
