# Excluding the three-T/two-T five-vertex row

Actual author **six-tammes-1**, role **researcher**, 2026-10-02.
Complete exact computer-assisted author proof. Independent mathematical
review and proof-assistant formalization of this new row remain pending.

## 1. Statement and scope

Let fifteen distinct unit points have all pair products at most c, where
**1/2<c<3/5**. Their **complete** contact graph joins exactly pairs of
product c. Assume its minor geodesic embedding is connected and cellular
on the sphere, with degrees3/4/5, simple strictly convex hemispherical
triangular and quadrilateral faces, and exactly nine Q faces. The following
profile is impossible:

* Two degree threes U,V, each with no T corner.
* Two degree fives F,D, with respectively three and two T corners.
* Three one-T degree fours A,B,C and eight two-T degree fours.

There is no zero-T four. In the existing catalogue notation this is
`(r,a,b,f0,f1,f2,O)=(2,3,0,0,1,1,8)`. The degree sum and Euler identity
give30 edges, eight T faces and nine Q faces.

The main lemma has no beta or optimizer irreducibility premise. It does
not establish endpoint cases, a numerical global Tammes-15 bound, an
unrestricted optimizer occurrence bridge, or exclusions of larger faces,
other embeddings or lower degrees.

[Three-five reduction8975](../three-five-branch/PROOF.md), source
`71f757b0cd0eafe8bf76fb0fa725ab2c43db3198`, and
[two-ordinary-five exclusion9025](../two-ordinary-five-branch/PROOF.md), source
`4634cb9daf85bf0c54aafe76f6141b03dabc1341`, provide credited local facts
and qualified catalogues. [F4T/D2T row9263](../four-two-triangle-fives-row/PROOF.md),
source `6bf3f5ade5f952ec7d0cddceaa52b7d48335c4e9`, provides credited
predicate/audit code and the preceding literal catalogue deletion.
Its F QQ cap0 and one-T-only Q-opposite rule are replaced here.

## 2. Corner geometry and supplier necessities

Put `alpha=acos(c/(1+c))`, `phi=2pi-4alpha`, and
`rho(u)=2atan(1/(c tan(u/2)))`. We credit the equilateral spherical
triangle/rhombus identities to
[Musin--Tarasov1312.5450, Proposition4.1](https://arxiv.org/abs/1312.5450)
and [their N14 paper1410.2536](https://arxiv.org/abs/1410.2536).
The following necessities are derived in8975/9025 from local7817/7912:

1. A T corner is alpha. Opposite Q corners are equal, while adjacent
   corners are u,rho(u), with `alpha<u<2alpha` because both Q diagonals
   are strict noncontacts. On our interval `3pi/8<alpha<2pi/5`, hence
   `alpha<phi<pi/2`.
2. Q corners at a three or two-T four are greater than phi. A three
   contacts only a one-T four or a five, and every incident edge is QQ.
   Here QQ means a Q on both sides of the edge.
3. Two distinct originals have at most two common positive-c contacts:
   their two independent contact planes intersect the sphere in at most
   two points. In the dependent antipodal case there is no common contact.

F's two Q corners sum to `2pi-3alpha`; each is below phi since the other
exceeds alpha. D's three Q corners sum to `2pi-2alpha`; each is below
phi since the other two have sum greater than2alpha. Therefore a Q
opposite either five may be a one-T four **or the other five**. The latter
possibility is retained throughout the noncontact cover. It is excluded
only if FD is already a contact, because Q diagonals are strict noncontacts.

On our interval `rho(phi)>pi-alpha`, following from the positive factor
`(1+c)(1+c-4c^2)`. For a QQ edge at either five, its two corners are
below phi, so the two corners at the other endpoint exceed pi-alpha.
A four or five would have at least two further corners at least alpha
and exceed2pi. Thus every QQ edge at a five leads to a three.

F has QQ cap1. Its Qs are adjacent exactly when it supplies one three;
otherwise they are separated. If F supplies a three, both of its Qs
contain that three as an adjacent boundary neighbor.
D has QQ cap2. Its two Ts separated give one QQ edge and one three
supplier; its Ts adjacent give two QQ edges and both suppliers U,V.
In the latter case every D Q contains at least one of U,V as an adjacent
boundary neighbor. This guard is **not** imposed in the one-three case:
the isolated D Q there is allowed to avoid the three.

The remaining QQ caps are3 at a three,2 at a one-T four and1 at a two-T
four. Known QQ edges count at both endpoints.

An FD contact cannot be a Q side. Its two corners would be below
phi<pi/2, contradicting `cot(u/2)cot(v/2)=c<1`. Thus FD is TT, consuming
D's entire two-T quota and giving D both three suppliers. The two TT
thirds are distinct and each is a common FD contact. If F also supplied
any three, that original would be a third common FD contact; it differs
from the TT thirds because its T quota is zero. This is impossible.
Therefore **F supplies no three when FD contacts**, and F's Qs are separated.

## 3. The terminal QQ obstruction

We use the prior adjacent-corner budget, credited to8975/9025 and
[review9043](../../six-reviewer-3/three-five-audit/REVIEW.md), source
`cbcba14f1a1b573739e5c2c2f0c2ec73e59e1f2c`. The following elementary
consequence is included with its proof; no priority claim is made for it.

For any adjacent Q corners u,v and0<c<1,

`u+v <= M(c) = 4atan(1/sqrt(c))`.

Indeed let t=tan(u/2),s=tan(v/2), so ts=1/c>1. Then

`(u+v)/2 = pi-atan((t+s)/(1/c-1))`.

AM-GM gives t+s>=2/sqrt(c), with the maximum corner sum attained at
t=s=1/sqrt(c), yielding the stated bound.
Let `S(c)=2pi-2alpha`. For c>1/2,

`cos(M/2)-cos(pi-alpha) = (2c-1)/(1+c) > 0`.

Both M/2 and pi-alpha lie in(0,pi), where cosine decreases strictly.
Thus **M<S**. This also supplies the three-contact restriction of
Section2: its two Q corners at an edge sum to more than S, leaving a
sum less than S at the other end, which excludes another three or a
two-T four.

Now suppose a QQ edge ab joins two degree fours each having exactly two
T corners. The two Q corners at a sum to S, and the two at b sum to S.
Each of its two Q faces has adjacent a,b corners of sum at most M.
Adding both inequalities gives `2S<=2M`, contrary to M<S.

**A QQ edge between two two-T fours is impossible for c>1/2.**
This is a geometric obstruction. A closed incidence map can satisfy all
the earlier combinatorial necessities while still containing this edge.
The final checker deliberately retains those maps and verifies this
obstruction at every such terminal.

## 4. Necessary finite incidence predicate

Every contact three-cycle is an actual T face. For its vertices a,b,d,
a further original p in its closed minor triangle has
`p=lambda_a a+lambda_b b+lambda_d d` with nonnegative coefficients of sum L.
Unit norm gives L>=1. Consequently
`p.(a+b+d)=(1+2c)L>=1+2c>3c`, contradicting packing. The noncrossing
cellular embedding therefore makes the empty minor triangle a face.
No analogous rule is imposed on arbitrary longer contact cycles.

The predicate enforces simple distinct face boundaries, noncontact Q
diagonals, degree capacities, automatic contact-triangle extraction,
T/Q quotas, common-contact and QQ caps, the allowed Q opposites of Section2,
five QQ neighbors, and the F/D Q supplier guards with their precise cases.
It does **not** reject ordinary-ordinary QQ edges at this stage.

Known corners at each vertex must form part of one cycle on its distinct
neighbors. Repeated corners, link degree above2 and a proper closed
subcycle are impossible. A complete neighbor set makes every other
original a noncontact. All compatible cyclic orders are retained and
checked against known corners and T quotas: consecutive contacts give T
sectors, noncontacts give Q sectors, unknown pairs retain both possibilities.

If only one neighbor is missing and known corners form a spanning path,
the new neighbor must join both path ends. Each remaining T requires
unused T quota at its end original, including an already named original.
Too little end capacity excludes the patch. If both endpoints of an
edge have complete neighbor sets and one known face, their compatible
cycles list every possible other face. Reject only if every such face
fails the same necessities. These tests are not sufficient conditions
for a sphere packing.

## 5. Complete supplier cover and original aliases

U,V each have three suppliers among A,B,C,F,D. They cannot share F,
whose QQ cap is1. D must occur in their union. Their triples intersect.
A shared one-T four or D has two consecutive QQ edges to U,V; the
intervening Q gives another common supplier. Thus the common-contact
bound forces intersection exactly two.

Of all100 ordered pairs of triples,30 satisfy these necessities. Every
admitted assignment is mapped by permuting the three actual one-T
labels and exchanging U,V to one of four families:

|family|N(U)|N(V)|ordered assignments|forced Q|
|---:|---|---|---:|---|
|0|A,B,C|A,B,D|6|Q(A,U,B,V)|
|1|A,B,F|A,B,D|6|Q(A,U,B,V)|
|2|A,B,D|A,C,D|6|Q(D,U,A,V)|
|3|A,B,D|A,F,D|12|Q(D,U,A,V)|

The original-role-map SHA256 is
`38f7cb0a388f7ddfee1e558e74dffba6f7ba3df517da23a119f9fc380c7c0607`.
F,D are not exchanged because their T quotas differ. These are label
renamings, not metric symmetry assumptions.

Labels0..6 are F,D,U,V,A,B,C, and7..14 are the eight ordinary fours.
Distinct fixed ordinary roles take the first unused ordinary labels.
Other distinct endpoint slots range over each one-T name or a distinct
unused ordinary label assigned in first-occurrence order. Four slots
have73 words and two slots13. Later unknown Q opposites range over all
fifteen actual originals; every compatible coincidence is retained.
No role is assumed new merely because it is introduced later.

## 6. Noncontacting fives

If F supplies no three, its Qs are separated. Its Ts consist of a
length-two path and an isolated T. Up to direction, its neighbor cycle
is `(a,I,b,c,d)` with Ts
`T(F,a,I), T(F,I,b), T(F,c,d)` and Qs
`Q(F,b,h,c), Q(F,d,k,a)`.
The internal I receives two Ts and is ordinary; fix it as7. The four
distinct endpoints use all73 words starting unused ordinary labels at8.
Both h,k range over A,B,C,D, including the other five D and all endpoint
aliases. Supplier families0,2 give `2*73*4^2=2336` initial patches;
four pass the necessary predicate.

If F supplies one three t, its Qs are adjacent and its Ts form the path
`e,I,R,p`. Its cycle is `(e,I,R,p,t)`, with Qs
`Q(F,p,h,t), Q(F,t,k,e)`. I,R receive two Ts and are distinct ordinary
originals, fixed as7,8. All13 endpoint words start unused ordinary
labels at9. Families1,3 give `2*13*4^2=416` initial patches; six pass.
Again the other-five Q opposite D is retained.

Each three has its complete supplier neighbor set. Every neighbor pair
a,b at v is consecutive and must have a Q face. For every missing
corner try all fifteen X in Q(v,a,X,b). Evaluate all missing corners,
choose one with the fewest passing X assignments, breaking ties by
`(v,a,b)`, and continue every passing child. An actual map supplies a
passing child at each choice. Each step adds a three corner, so depth
is at most six.

The separated-Q case has104 such states and2130 Q-opposite tests,
leaving36 full-three-star partial patches. The adjacent-Q case has106
states and480 tests, leaving80. Those116 patches still require the
remaining-face cover of Section8; full stars alone are not an exclusion.

## 7. Contacting fives

By Section2, F supplies no three and D supplies both; hence only family2
can occur. The F cycle is `(a,D,b,c,d)`, with Ts
`T(F,a,D), T(F,D,b), T(F,c,d)` and Qs
`Q(F,b,h,c), Q(F,d,k,a)`.
The D cycle is `(a,F,b,t,w)` for either order `(t,w)=(U,V)` or(V,U).
Its Qs are `Q(D,b,l,t), Q(D,t,A,w), Q(D,w,m,a)`.
The two FD triangles are already shared with F; they are not counted twice.

All four a,b,c,d are distinct one-T or ordinary fours: every one receives
a T, so none is a three. Use all73 words starting ordinary labels at7.
All h,k,l,m range over A,B,C. The other five is excluded from these
opposites precisely because FD is a contact and would become a Q diagonal.
Both orders of the three suppliers are retained. There are
`73*2*3^4=11826` initial patches. **All reject** the necessary predicate.
No contact terminal is omitted by an unproved symmetry choice.

## 8. Complete remaining-face cover and terminal certificates

At an edge uv with one known face, enumerate every possible other
boundary neighbor w at u and x at v. With complete neighbor sets, use
all compatible cycles of Section4. Otherwise overcover by allowing every
actual original except the center, uv neighbor and known face's other
neighbor, subject only to degree capacity for a new contact.
If w=x, add T(u,v,w); otherwise add Q(u,v,x,w). Canonicalize candidates
and remove already known faces.

The actual second face is retained: distinct incident faces have distinct
corners at both edge endpoints. Choose the open edge with fewest raw
candidates, breaking ties by `(u,v)`, and continue all passing children.
Each child adds a new face; an actual target has17, so its path terminates.

From the36 separated-Q full stars, closure visits120 states and480 face
tests. There are24 leaves with an impossible second face, and **twelve
closed incidence terminals**. From the80 adjacent-Q full stars, closure
visits728 states and3904 face tests; all288 leaves have an impossible
second face. No closed terminal remains in that case.

Each closed terminal is checked for15 connected originals, the exact
degree and T/Q corner profiles,30 two-sided edges and8T/9Q faces.
All twelve have a QQ edge between two ordinary two-T fours. Its endpoints
and SHA256 of the entire canonical17-face list are recorded in
[EXPECTED.json](EXPECTED.json). All twelve are therefore geometrically
excluded by Section3. An unexpected closed profile or a terminal without
that obstruction causes failure, never a false exclusion verdict.
No terminal is asserted to be a sphere packing.

The full original-label cover, the local necessities, exhaustive completion
and explicit terminal obstruction prove the stated row exclusion.

## 9. Reproducibility and trust boundary

[patch.py](patch.py) implements the necessary set predicate.
[check.py](check.py) regenerates every case and terminal certificate with
no solver, metric sample, floating signs or external runtime data.
[audit.py](audit.py) imports none of the primary code. It uses edge and
neighbor masks, contact triangles from common neighbors, directed face
boundaries, recursive cycle masks, supplier mask triples, endpoint words
from selected one-T positions and T-sector-pattern fan construction.
Its separate terminal check uses pair masks and full role counts.

The written geometry, case specification and deterministic record order
are shared. This is a separate **same-author** audit, not independent
researcher review or proof-assistant formalization.
The implementations agree on all **21572 admission decisions**, branch
choices and twelve terminal obstruction witnesses. Full record SHA256:
`8c4923f7794d1326711436db91c1fa72de6e6ff63da4e33b6241871e592327dd`.
Admitted/selected SHA256:
`236fc4f2f872fae275085d0fa5eaefac823c21860acdaeaa98b15c0c5ed9046e`.

[controls.py](controls.py) checks18 partial positive/damaged fixtures,
including a retained other-five Q opposite, F/D one-/two-three guards,
QQ-to-ordinary rejection, quota/link/diagonal failures and a missing-T
capacity release. It preserves a literal closed incidence map through
both necessary predicates, then finds its ordinary QQ obstruction;
deletion of a T or Q makes the full terminal profile check fail.
Positive incidences are not claimed as sphere packings.

All six normal/optimized check/audit/control commands complete and match
their entire expected files. [VALIDATION.json](VALIDATION.json) records
CPython3.12.14/stdlib, native threads1, one CPU child, original55-second
per-command guard and1CPU/2GiB scope, timings, memory and output hashes.
Main output4990 bytes SHA256:
`e8096b4aab523a7302ee68ccb3907edf55cb2bc2c1a7b67db7ef3945500e33f7`.
Controls1991 bytes SHA256:
`e74258641e03c84fb3c94f08fc82b6d3ff849fb0b214c717ccaacb38e8cecfa8`.
Bulk traces and private pilots are omitted and regenerate from source.
The written geometric necessity and completeness arguments, CPython
encoding and digest comparison remain explicit trust boundaries.

## 10. Prior catalogues, reviews and unresolved global frontier

The optional literal deletion after9125/9185/9233/9263 takes the committed
qualified basis from three to two rows and the later **source-only** basis
from one to zero. [DEPENDENCIES.json](DEPENDENCIES.json) retains every
original hypothesis, including beta where present. Those catalogue
derivations are imported, not regenerated. Necessary count rows do not
assert realizations. An empty source-only list is not promoted here to
an independently audited classifier or an unrestricted optimizer theorem.

[Review9043](../../six-reviewer-3/three-five-audit/REVIEW.md) reviews8975;
[review9119](../../six-reviewer-3/two-fives-audit/REVIEW.md), source
`3cd270405739c719b1add3891475c99b5586ef39`, reviews9025. Their endpoint
or wider-interval findings do not transfer to this new row.
The peer's [G22 strip9193](../../six-tammes-2/twenty-two-contact-strip/PROOF.md),
source `20cf3a8d2a8a222058bf3f8c15e50f62490d80da`, concerns a prescribed
22-contact, nine-triangle motif and supplies no premise or optimizer
occurrence bridge for this eight-T contact-map class.

The [live Cohn table](https://cohn.mit.edu/spherical-codes/) and
[fifteen-point coordinates](https://spherical-codes.org/data/3/15) were
refreshed2026-10-02. The row remains unstarred with incumbent cosine
`0.59260590292507377809642492233276`. The
[MIT data-set reader](https://hdl.handle.net/1721.1/142661) is credited.
Musin--Tarasov1410.2536 solvesN14. The located
[2026 deterministic optimization paper](https://doi.org/10.1016/j.dam.2026.05.015)
reports Tammes through13 with numerical tolerance, not exactN15.
Bounded live primary search located no overlapping finite certificate;
it is not an exhaustive priority claim.

The next global step still needs explicit treatment of larger faces,
other contact structures and an optimizer occurrence argument. The
remaining committed count rows and the source-only classifier hypotheses
also require precise comparison before any complete-branch conclusion.
