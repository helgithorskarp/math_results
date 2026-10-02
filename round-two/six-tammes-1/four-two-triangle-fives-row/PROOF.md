# Excluding the four-T/two-T five-vertex row

Actual author **six-tammes-1**, role **researcher**, 2026-10-02.
Complete exact computer-assisted author proof. Independent mathematical
review and proof-assistant formalization are pending.

## 1. Statement

Let fifteen distinct unit points have all pair products at most c, with
**1/2<c<3/5**. Their **complete** contact graph joins exactly pairs of
product c. Assume its minor geodesic embedding is connected and cellular
on the sphere, with degrees3/4/5 and simple strictly convex hemispherical
triangular and quadrilateral faces, exactly nine Q faces. The following
profile is impossible:

* Two degree threes U,V, each with no T corner.
* Two degree fives F,D, with respectively four and two T corners.
* Four one-T degree fours A,B,C,E and seven two-T degree fours.

There is no zero-T four. In the existing catalogue notation this is
`(r,a,b,f0,f1,f2,O)=(2,4,0,1,0,1,7)`. The degree sum and Euler identity
give30 edges, eight T faces and nine Q faces.

No beta threshold or optimizer irreducibility is a premise of the main
lemma. It gives no unrestricted optimizer-occurrence bridge, larger-face
or low-degree exclusion, endpoint statement, or global numerical bound
for Tammes-15.

The [three-five reduction8975](../three-five-branch/PROOF.md), source
`71f757b0cd0eafe8bf76fb0fa725ab2c43db3198`, and
[two-ordinary-five exclusion9025](../two-ordinary-five-branch/PROOF.md), source
`4634cb9daf85bf0c54aafe76f6141b03dabc1341`, leave this literal row in
their qualified catalogues. [The preceding two-three-T-five row9233](../two-three-triangle-fives-row/PROOF.md),
source `0c1f6bef2f2ee82e9c37de3f0c9b181d5a1cad4c`, supplies credited
predicate/audit code and a different row exclusion. Its QQcap1 and
other-five-opposite rule are replaced here, not reused as premises.

## 2. Geometry and the new two-T-five supplier rule

Put `alpha=acos(c/(1+c))`, `phi=2pi-4alpha`, and
`rho(u)=2atan(1/(c tan(u/2)))`. We credit the spherical triangle/rhombus
identities to [Musin--Tarasov1312.5450, Proposition4.1](https://arxiv.org/abs/1312.5450)
and [their N14 paper1410.2536](https://arxiv.org/abs/1410.2536).
The following open-interval necessities are derived in8975/9025 from
the earlier7817/7912 geometric reductions:

1. A T corner is alpha. Opposite Q corners are equal; adjacent corners
   are u,rho(u), with `alpha<u<2alpha` because both diagonals are strict
   noncontacts. Also `3pi/8<alpha<2pi/5`, and `alpha<phi<pi/2`.
2. A three has no T; a four has at most two Ts; a five has at most four.
   A Q corner at a three or two-T four is greater than phi. A three
   contacts only a one-T four or a five, and every incident edge is QQ.
   Indeed `u+rho(u)<=4atan(1/sqrt(c))<2pi-2alpha`, while the two Q
   corners at a three sum to more than `2pi-2alpha`. Applying the
   adjacent-corner sum bound excludes another three or a two-T four
   at its other endpoint.
3. Two distinct originals have at most two common positive-c contacts:
   intersect their two contact planes with the sphere. The antipodal
   dependent case has no common contact.

QQ means a Q on both sides. F's sole Q corner is phi, and F has no QQ
edge. D's three Q corners sum to `2pi-2alpha`; each is **less** than
phi because its two other Q corners have sum greater than2alpha. Thus a Q opposite
either five must be one of A,B,C,E. The other five, both threes and
all two-T fours have incompatible opposite angles.

For any QQ edge at D, both its corners there are below phi. The two
corners at the other endpoint exceed `y=rho(phi)>pi-alpha`, the latter
inequality following from `(1+c)(1+c-4c^2)>0`. A four or five has at
least two other corners of size at least alpha and would exceed2pi.
Thus every D QQ edge leads to a three. In a five-cycle with two T and
three Q sectors, separated Ts give one QQ edge, and adjacent Ts give
two. Therefore D must supply at least one of U,V. It supplies exactly
one when its Ts are separated and both when they are adjacent. In the
two-three case **every Q face at D contains at least one of U,V as an
adjacent boundary neighbor**. This last guard is not used in the
one-three case: the isolated Q there can avoid the three.

The QQ caps are3 at each three,2 at a one-T four,1 at a two-T four,
0 at F, and **2 at D**. Known QQ edges count at both endpoints.

An FD contact cannot be a Q side. Its corners would be at most
phi<pi/2, contrary to `cot(u/2)cot(v/2)=c<1`. It therefore has T
on both sides. Those two Ts consume D's entire T quota, so D's Ts
are adjacent at its F neighbor and D supplies both threes.

## 3. Necessary incidence tests

Every contact triangle is an actual T face. If its vertices are a,b,d
and a further original p is in its closed minor triangle, write
`p=lambda_a a+lambda_b b+lambda_d d` with nonnegative coefficients
of sum L. Unit norm implies L>=1; then
`p.(a+b+d)=(1+2c)L>=1+2c>3c`, contradicting packing. No other original
lies inside or on the boundary. The noncrossing cellular embedding
makes it a face. Arbitrary longer contact cycles are not forced faces.

The checker enforces distinct face vertices, strict noncontact Q
diagonals, degree capacities, automatic contact-triangle extraction,
T and Q quotas, common-contact and QQ caps, the Q-opposite rule, and
the two-three D-Q guard of Section2. At each vertex known corners
are edges of a single cycle on its distinct neighbors. Repeated
corners, link degree above2 and a proper closed subcycle are impossible.

A complete known neighbor set makes all other originals noncontacts.
All compatible cyclic orders are tested against known corners and
T quotas: consecutive contacts give T sectors, known noncontacts give Q
sectors. If only one neighbor is missing and known corners span a path,
the missing original must connect both path ends. Each new T requires
unused T quota at its corresponding end original, even if that original
was already named. Too little end capacity excludes the patch.

If both endpoints of an edge have complete neighbor sets and one known
face, their compatible cycles list every possible other face. Try each
possibility with the same necessary tests. Reject only if all fail.
None of these checks is asserted sufficient for a sphere packing.

## 4. Complete supplier and original-label cover

U,V each have three suppliers among A,B,C,E,D; F is not a supplier.
If a one-T four supplies both, these are its two QQ edges; the intervening
Q forces a second common supplier. If D supplies both, its two QQ
edges are consecutive in its three-Q run; their intervening Q similarly
forces a second common supplier. The common-contact bound gives exactly
two in either case. Two triples in a five-element universe intersect,
so every admissible supplier pair has intersection size exactly two.
D must occur in their union, by Section2.

All100 ordered pairs of triples are checked. Exactly48 satisfy these
necessities. Permuting the four actual one-T labels and exchanging U,V
maps every admitted assignment to one of two families:

| family | N(U) | N(V) | ordered assignments | forced Q |
|---:|---|---|---:|---|
|0|A,B,C|A,B,D|24|Q(A,U,B,V)|
|1|A,B,D|A,C,D|24|Q(D,U,A,V)|

All original-role maps are regenerated and hashed. F,D are not
interchanged because their T quotas differ. These are label renamings,
not metric symmetry assumptions.

Ordinary vertices have labels8..14. Fixed distinct ordinary roles are
assigned the first unused ordinary labels. Other distinct endpoint slots
range over each one-T name or a distinct unused ordinary label, assigning
ordinary names in first-occurrence order. Two slots have21 words.
This covers all assignments up to renaming unused ordinary originals.
Later unknown Q opposites range over all fifteen actual labels, preserving
every coincidence compatible with the necessities. No unknown role is
assumed new or excluded solely because it appeared earlier.

## 5. Noncontacting F,D

F's four Ts form a path `e,I,R,S,p` on its five neighbors, with
Q(F,e,h,p). The three internal originals I,R,S receive two distinct
Ts, hence are ordinary fours; fix them as8,9,10. Each endpoint is a
distinct one-T or unused ordinary four, so use the21 words of Section4.
The opposite h is one of the four one-T names. Both supplier families
and all opposite aliases are retained: `2*21*4=168` initial patches,
of which27 pass the necessary tests.

The suppliers already determine each three's full neighbor set. Every
neighbor pair is consecutive and its face is Q. For any missing pair
a,b at v in{U,V}, try all fifteen X in Q(v,a,X,b). Evaluate every
missing sector, choose one with fewest passing assignments, breaking
ties by `(v,a,b)`, then continue all passing children. An actual map
would supply a passing child at every choice. Each step adds a new
three corner, so there are at most six steps.

There are180 recursive states and5295 opposite tests. Family0 cannot
complete: it has no full-three-star patch. Family1 leaves36 partial
patches with both three-stars complete. The code fails loudly if a
family0 full completion appears; it does not silently omit that case.

In each of the36 family1 patches, all three D Qs are known and D's
four neighbors are U,V plus two distinct endpoints a,b. D's two Ts
must form the path a-i-b, where i receives both Ts and is ordinary.
Try every actual ordinary label8..14 in T(D,a,i), T(D,i,b), including
already named originals. All `36*7=252` possibilities reject.
Thus the noncontacting case is excluded.

## 6. Contacting F,D and remaining faces

FD is TT and consumes D's two Ts, so only supplier family1 remains.
In F's four-T path D occupies one of the three internal positions.
The other two internals receive two Ts and are ordinary; fix their
labels8,9 in path order. The21 endpoint words are still complete.
If a,b are the neighbors on either side of D in that path, D's cycle
is `(a,F,b,t,w)` for either order `(t,w)=(U,V)` or `(V,U)`. Its Qs are

`Q(D,b,k,t), Q(D,t,A,w), Q(D,w,l,a)`.

The middle Q is the forced common-supplier face. F's Q is
Q(F,e,h,p). All h,k,l range over A,B,C,E, including all endpoint
aliases. Hence there are `3*2*21*4^3=8064` initial patches; six pass.
The complete three-star rule of Section5 gives62 states,480 opposite
tests and36 full-three-star partial patches.

Complete the remaining faces across an edge uv with exactly one known
face. At u,v find every possible other boundary neighbor w,x. With a
complete neighbor set, use all compatible cycles of Section3. Otherwise
overcover by allowing every actual original except the center, uv neighbor
and known face's other neighbor, subject only to degree capacity for a
new contact. When w=x add T(u,v,w); otherwise add Q(u,v,x,w).
Canonicalize these candidates and remove already known faces.

The actual second face is included: distinct incident faces have distinct
corners at each edge endpoint. Choose the open edge with fewest raw
candidates, tie-breaking by `(u,v)`, and continue every passing one.
Each child adds a new face; an actual target map has17 faces, so it
would terminate after finitely many steps. A state with no open edge
triggers failure, never exclusion; no such state occurred.

From the36 contact patches there are84 recursive states and492 face
tests;48 children pass and all36 final leaves have an edge with no
possible other face. There is no completed map. Together with Section5
and the exhaustive original-label cover, this proves the stated row
exclusion.

## 7. Reproducibility and trust boundary

[patch.py](patch.py) implements the necessary set predicate;
[check.py](check.py) regenerates the full cover without metric samples,
floating signs, a solver or external runtime data. [audit.py](audit.py)
imports none of the primary code. It uses edge/neighbor masks,
contact-triangle extraction by common neighbors, directed face boundaries
and recursive neighbor-cycle masks. Supplier triples are generated by
vertex masks, endpoint words by selected one-T positions, and complete
fans by T-sector patterns. The written geometry, case specification
and deterministic record order are shared. This is a separate
**same-author** audit, not independent researcher review or a formal proof.

Both implementations agree on every one of the14751 tested admission
bits and all selected corners/edges, with full entry digest
`03d62e0baaa7ace1509adff2c155dda2fa0933f62087f49ed19f3b8432f62f4a`
and admitted/selected digest
`312d83be3c62b1fb6a750441f07573e09e66e585a1b14b6f9e3c4de77697b3a8`.
[EXPECTED.json](EXPECTED.json) is the full compact output.
[controls.py](controls.py) checks15 positive/damaged partial fixtures,
including D's retained two-three role, the isolated Q allowed only in
the one-three case, and the excluded other-five opposite. It also checks
a missing-star capacity release, a positive contact-fan prefix, all
seven ordinary internals at an admitted D parent, and mask self-pair
rejection. Positive incidences are not asserted sphere packings.

All six normal/optimized check/audit/control runs match their complete
expected bytes. [VALIDATION.json](VALIDATION.json) records CPython3.12.14,
standard library only, native threads1, one CPU child at a time, the
unchanged55s per-command guard and1CPU/2GiB scope, timings, memory and
output hashes. Bulk traces are regenerated and omitted. The written
geometry-to-cover reduction, CPython implementation and cryptographic
comparison remain explicit trust boundaries; no formalization or
independent new-row verdict is claimed.

## 8. Prior results and the remaining frontier

The optional literal catalogue deletion after9125/9185/9233 takes the
committed qualified basis from four to three rows and the later
**source-only** basis from two to one. [DEPENDENCIES.json](DEPENDENCIES.json)
retains all original hypotheses, including any beta assumption. Those
catalogue derivations are imported, not regenerated; count rows do not
assert realizations. The later remaining row is `(2,3,0,0,1,1,8)`.
No unrestricted or complete-nine-Q conclusion follows from that count alone.

[Review9119](../../six-reviewer-3/two-fives-audit/REVIEW.md), source
`3cd270405739c719b1add3891475c99b5586ef39`, reviews9025 only. Its
interval and endpoint extensions do not transfer here. The peer's
[G22 strip9193](../../six-tammes-2/twenty-two-contact-strip/PROOF.md), source
`20cf3a8d2a8a222058bf3f8c15e50f62490d80da`, is a prescribed22-contact,
nine-triangle motif. It supplies neither an occurrence bridge nor a
premise for this eight-T map class.

The [Cohn data set](https://hdl.handle.net/1721.1/142661), its
[live table](https://cohn.mit.edu/spherical-codes/) and
[fifteen-point coordinates](https://spherical-codes.org/data/3/15) were
checked2026-10-02. The row remains unstarred with incumbent cosine
`0.59260590292507377809642492233276`. Musin--Tarasov1410.2536 solvesN14.
The located [2026 deterministic global-optimization paper](https://doi.org/10.1016/j.dam.2026.05.015)
reports Tammes computations through13 points with numerical tolerance,
not an exactN15 solution. The bounded primary search did not locate an
overlapping finite certificate and is not an exhaustive priority claim.
