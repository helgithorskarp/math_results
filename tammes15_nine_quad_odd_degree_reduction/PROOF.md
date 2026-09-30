# At most three degree threes in the nine-quadrilateral Tammes-15 branch

Author: **six-tammes-1**, role: **researcher**, 2026-09-30.
Status: complete author-audited conditional hand proof, with exact arithmetic
and a separate full-entry audit of the small necessary finite covers.
Independent mathematical review and formalization are pending.

## Statement and scope

Let fifteen distinct points on the unit sphere have minimum geodesic
separation d and c=cos(d). Assume their **complete** contact graph is
connected, has degrees 3,4,5, and gives a cellular sphere decomposition
into simple strictly convex geodesic triangles T and quadrilaterals Q,
each contained in an open hemisphere. Assume exactly nine Q faces.

**Degree bound.** On the full open interval `1/2<c<3/5`,

```text
n3=n5<=3, n4=15-2*n3, E=30, T=8.
```

Every degree-three point contacts only vertices of positive triangle
deficit. Here the deficits at degrees 4 and 5 are `2-t` and `4-t`,
where t is the number of incident T faces. Every deficient five has
deficit at most two. The degree bound and these statements do not use
the earlier all-degree-four exclusion.

**Remaining odd-degree corollary.** The [all-degree-four exclusion](../tammes15_nine_quad_degree_four_exclusion/PROOF.md),
source `dc8ebfb023d53b5c70e41e8aa886282ef557cf10`, graph h7786
`bafkreicb2v2lhtmsardhszso4mjifb3rizdabt5g6iar2cqgdsxoeolpl4`,
therefore leaves precisely the degree ranges `1<=n3=n5<=3` on this full
interval. This is a dependency of the lower bound 1, not of the new upper
bound 3. It remains author-audited and independently unreviewed here.

**Stronger necessary structure on the beta interval.** Let beta be the
unique root in `(119/200,3/5)` of

```text
P(c)=1+4c+2c^2-4c^3-11c^4-24c^5.
```

On `1/2<c<beta`, the small-corner opposite graph H is triangle-free
regardless of the number of T/Q faces or points. For the nine-Q branch,
at most one five has deficit two, and a degree-three point contacts
at most one degree five. There are **32 necessary count profiles**:
9 with r=1,12 with r=2,11 with r=3, where r=n3=n5. Section 6 defines
the finite cover exactly.

A retained count profile is not an embedding, an exact candidate or a
realizable packing. The original face-incidence and metric problems
remain open. This result does not prove that all global optimizers have
these T/Q/degree hypotheses, exclude larger polygonal faces, improve a
global numerical separation bound, or settle Tammes-15 optimality.

## 1. Corner identities and two strict inequalities

Put

```text
alpha=acos(c/(1+c)); A=2*pi-2*alpha; phi=2*pi-4*alpha;
rho(u)=2*atan(1/(c*tan(u/2))); b0=2*atan(1/sqrt(c)); y=rho(phi).
```

A T corner is alpha. Opposite Q corners are equal, adjacent corners
are related by the decreasing involution rho, and diagonals bisect their
endpoint corners. Completeness makes both Q diagonals strictly longer
than d, so every Q corner satisfies

```text
alpha < u < 2*alpha.                                  (1)
```

These classical identities appear in [Musin--Tarasov, Proposition 3.2](https://arxiv.org/abs/1410.2536)
and the [earlier geometric audit](../tammes_15_triangle_quad_exclusion_review1/README.md),
source `f026ccec6854eb913e5c156f4ff0cf08ed5cb4a9`, graph h7182
`bafkreiflxdrel4fv4opchhucsisp7ylw2lsfgtrv4q7tya3o5vjh4ld53a`.
That review does not review this result.

On the full local interval, `3*pi/8<alpha<2*pi/5` and `alpha>pi/3`.
The upper bound follows from `c/(1+c)>1/3>cos(2*pi/5)`; the lower bound
from `c/(1+c)<3/8<cos(3*pi/8)`. The latter last comparison squares to
`sqrt(2)<23/16`, or `512<529`. Consequently a three has no Ts, a four
has at most two Ts, and a five has at most four Ts, by angle sums and
(1). In particular `alpha<phi<pi/2`.

For positive half-angle tangents with product `1/c>1`, their arctangent
sum is maximal when they agree. Thus

```text
u+rho(u) <= 2*b0 < A.                                 (2)
```

For the strict comparison, `cos(b0)=(c-1)/(c+1)` is greater than
`cos(pi-alpha)=-c/(c+1)` since c>1/2. All these angles are in `(0,pi)`.

There is also the uniform strict bound

```text
y > pi-alpha.                                        (3)
```

Indeed with `h=sqrt(1+2*c)` and `D=1+2*c-c^2`,
`tan(phi/2)=2*c*h/D`, `tan(y/2)=D/(2*c^2*h)`, and
`tan((pi-alpha)/2)=h`. Clearing only positive factors, (3) is

```text
D-2*c^2*(1+2*c)=(1+c)*(1+c-4*c^2)>0.
```

The last factor is at least its value `4/25` at c=3/5, since its
derivative is `1-8*c<0`. The checker additionally verifies its exact
positive Bernstein coefficients on the closed `[1/2,3/5]` interval.
This certifies the comparison, not a closed-endpoint graph theorem.

An ordinary four has two Q corners summing to A; each is strictly
above phi because the other is below 2alpha. A degree three also has
all Q corners strictly above phi. Every Q corner at a five is at most
phi, since its other four corners are at least alpha. Equality requires
those four faces to be Ts. A deficient five therefore has every Q corner
strictly below phi. Opposite-angle equality rules out a Q opposite
three/five pair on the full interval.

Two distinct unit points have at most two common contact neighbors:
their two dot-product planes intersect in a line meeting the sphere
in at most two points. The points are independent except at antipodality;
antipodal points have no common neighbor since c>0. This argument also
makes Q opposite pairs unique: an existing simple Q supplies both contact
solutions, fixing its four vertices and minor boundary arcs, and only
one convex hemispherical cell can use that boundary. An opposite Q pair
cannot contact since its complete contact diagonal would split the face.
These facts use original points throughout.

## 2. A degree-three point can contact only a deficient point

Let U be degree three and V a contact neighbor. The two faces at edge
UV are Qs. Name their corners u,v at U, and w the third Q corner at U.
By (1) and the star sum,

```text
u+v=2*pi-w>A.
```

Their corners at V are rho(u),rho(v), so (2) gives

```text
rho(u)+rho(v) <= 4*b0-u-v < 4*b0-A < A.               (4)
```

If V were another three, its remaining corner would be greater than
`2*pi-A=2*alpha`, contradicting (1). If V were an ordinary four,
its two Q corners would have to sum to A, also contradicting (4).
An ordinary five has only one Q and cannot have the two Q faces at UV.
Thus U's three distinct neighbors are all deficient fours or fives.
In particular degree-three vertices are pairwise noncontacting.

This argument is independent of N,q,beta and the deficit-six count.
It uses the full local interval and avoids assuming ordinary fives in
the new odd-degree branch.

## 3. Deficit six and the contact-capacity inequality

Euler and incidence for N=15,q=9 give `E=30,F=17,T=8` and
`n3=n5=r,n4=15-2*r`. As threes have no Ts, the maximum T-corner
budget has exactly six units of deficit:

```text
sum_D deficit = 2*n4+4*n5-3*T = 6.                   (5)
```

For a deficient five with deficit delta, all its delta+1 Q corners
are below phi. Each opposite corner is at a distinct other deficient
point, by opposite-angle equality, the strict ordinary/three bounds,
and uniqueness. These points each cost at least one deficit unit.
Hence `6>=delta+(delta+1)`, and delta<=2. This does not need the
triangle-free assertion below.

Let a,b count deficient fours of deficits 1,2, and f1,f2 count fives
of deficits 1,2. Then

```text
a+2*b+f1+2*f2=6.                                     (6)
```

A contact edge incident to a degree-three point is Q-Q. At a one-T four,
at most two edges avoid the T. At a zero-T four there are at most four.
At a deficit-one five with three Ts, at least four distinct edges bound
its Ts, leaving at most one Q-Q edge; at a deficit-two five with two Ts,
at least three distinct edges bound its Ts, leaving at most two.
These bounds retain every cyclic star order. Separated T blocks use
more edges and can only reduce the available Q-Q contacts.

Count the 3r contacts of threes, all supplied by deficient points by
Section 2. Therefore

```text
3*r <= 2*a+4*b+f1+2*f2 = 12-f1-2*f2.                 (7)
```

This first gives r<=4. If r=4, equality forces f1=f2=0 and saturates
all Q-Q edges at every deficient four with contacts to degree threes.

## 4. The equality r=4 is impossible

Suppose r=4. All four fives F are ordinary. There are seven fours,
a+2b=6 deficient ones, and `1+b` ordinary fours R, with b=0,1,2,3.
Every Q at a deficient four touches at least one Q-Q edge there: its
star is T,Q,Q,Q or Q,Q,Q,Q. Saturation in (7) makes that edge lead
to a degree three. Hence **every Q at a deficient four contains a three**.

No Q can contain both an ordinary five F and a three U. They cannot
be adjacent by Section 2, and cannot be opposite since their corners
are phi and strictly greater than phi. A Q at F consequently contains
neither a deficient four nor a three; all its corners are Fs or Rs.
Its opposite corner cannot be R because every R corner exceeds phi,
so it is another F. Adjacent F corners are impossible since rho(phi)=y
is greater than phi. Thus each F-containing Q has two opposite Fs
and two adjacent Rs, whose angles are y.

The four ordinary Fs contribute four Q corners, hence exactly two such
Qs. An R can supply at most one y corner: two of them and its two
triangular corners would have total greater than `2*(pi-alpha)+2*alpha`
by (3). The two Qs therefore require four **distinct original** Rs.
The necessary count `nR=1+b` forces b=3,a=0. The remaining three
fours are zero-T and, by saturation, each contacts all four degree-three
points. Two of these fours would have four distinct common contact
neighbors, contradicting the at-most-two fact of Section 1.

Thus r=4 is excluded and `r<=3` on `(1/2,3/5)`. Combining with h7786
excludes r=0 and gives the stated range 1,2,3. No H-triangle hypothesis
was used in this degree-bound proof.

## 5. The small-corner graph is triangle-free without a deficit-four premise

For `1/2<c<beta`, the identities in Section 1 also give `y>2*pi/3`.
Indeed this is equivalent to `D^2>12*c^4*(1+2*c)`, whose difference
is P(c). Its derivative is strictly negative on `[1/2,3/5]`; exact
Bernstein signs and the endpoint signs at119/200 and3/5 isolate beta
and certify P>0 below it. This repeats a threshold computation in h7182;
that threshold is prior work, not new here.

Join two opposite Q corners by the minor internal diagonal if their
common angle is **strictly below phi**. These edges form a simple
embedded graph H on deficient points, with no contact edges. Only one
opposite pair in a Q can be small, since its adjacent corners exceed
y>phi. Distinct Q diagonals cannot cross because the cells have disjoint
interiors. No particular total deficit or face count is assumed in this
paragraph or the following triangle argument.

For an H edge, its adjacent Q angle v satisfies `y<v<2*alpha`, so the
inner product s of its endpoints is

```text
s=c^2+(1-c^2)*cos(v),
-1/3 < 4*c^2/(1+c)-1 < s < (3*c^2-1)/2 < 1/25 < 1/16.   (8)
```

The lower rational function is strictly increasing for c>0 and equals
-1/3 at1/2; its positive numerator relative to-1/3 is also checked.
For a putative H triangle with side cosines r,s,t, every smaller
spherical angle theta satisfies

```text
cos(theta)=(r-s*t)/sqrt((1-s^2)*(1-t^2)),
-1/2 < cos(theta) < 3/32.                              (9)
```

Indeed pairwise products lie between-1/48 and1/9, and the positive
denominator exceeds8/9. This excludes degeneracy and makes each smaller
angle strictly less than2pi/3. Such a triangle has no common contact
neighbor Z: (8) gives

```text
||P+Q+R||^2 < 9*c^2, while Z dot(P+Q+R)=3*c,
```

contradicting Cauchy--Schwarz.

Now inspect the two H diagonals at any triangle vertex. They bisect
two distinct small Q corners u,v. If those Qs are consecutive in its
face star, their shared boundary neighbor contacts all three H vertices,
which was just excluded. If they are not consecutive, each of the two
angular sectors between their bisectors contains at least one entire
other face corner, of angle at least alpha. Both sectors are therefore
strictly greater than `(u+v)/2+alpha>2*alpha>2*pi/3`.
Their smaller angle contradicts (9). This proves triangle-freeness
without the older deficit-four argument's exclusion of three deficit-two
vertices. It generalizes the [earlier eight-Q H theorem](../tammes15_eight_quad_reduction/PROOF.md),
source `2f9b8b2c7125c339a7a350437bc32b8aa40ac7db`, graph h7232
`bafkreiekf4d4rllqsf42fr5j5l36lb226ev4jsedqjvmyg6aqokjsrolzm`.

At a deficient five H has degree delta+1. At a deficient four its H
degree is at most2 for deficit1 and at most3 for deficit2: three small
Q corners and one T would have sum below `3*phi+alpha<2*pi`, and
four small Qs would have sum below `4*phi<2*pi`. The first comparison
uses `alpha>3*pi/8>4*pi/11`. Isolated deficient fours are allowed.

There cannot be two deficit-two fives. If they are joined in H, their two
other H neighbors each are four distinct points, since a shared neighbor
would form a triangle; this would cost at least `2+2+4=8` deficit units.
If they are not joined in H, their union of neighbors has at least three
points outside them, costing at least `2+2+3=7`. Both contradict (5).

A three U contacts at most one five. If two of its three contact neighbors
were fives F,G, both would be deficient by Section 2. The third neighbor
is another deficient point D. The three Qs in U's star, between each
pair of its neighbors, have small corners at those fives. Their opposite
corner pairs therefore give H edges FG,FD,GD, forming a forbidden triangle.
The use of the three original neighbor labels preserves all Q-opposite
aliases; it does not substitute independently normalized metric copies.

## 6. Exact necessary count and neighbor covers

Write f_j for the number of fives with deficit j, j=0..4. Before the
new restrictions the complete necessary bookkeeping is

```text
n3=n5=r, n4=15-2*r; sum_j f_j=r;
a+2*b+sum_j j*f_j=6; a+b<=15-2*r; all counts nonnegative.
```

For every r=1..7 the checker generates all these integer count tuples,
not a contact-map population. Sections 3,4 rule out r>=4 and f3,f4>0.
Equation (7) removes more count rows. For each remaining tuple:

* Name deficient points in fixed role blocks: a one-T fours, b zero-T
  fours, f1 deficit-one fives and f2 deficit-two fives.
* Enumerate every simple triangle-free H edge mask on these **at most
  six** points. Degree caps at the fours are2,3; required degrees at the
  fives are exactly2,3. No spatial embedding, symmetry or connectedness
  of H is assumed. This is a necessary graph cover.
* Enumerate the unordered family of r distinct contact-neighbor triples
  of the original degree threes. Triple membership capacities at these
  role blocks are2,4,1,2; a triple contains at most one five. A pair of
  deficient points occurs in at most two triples, since it has at most
  two common contact neighbors. Two triples cannot be equal, since two
  original degree threes would then have three common contact neighbors.
  Canonical ordering only removes permutations of the degree-three labels.

A tuple with no H or no neighbor family is impossible. The finite cover
leaves9,12,11 tuples at r=1,2,3, **32 in total**. For r=1 these correspond
to four ordinary-five rows, three deficit-one-five rows and two deficit-
two-five rows. At r=2 the all-ordinary row a=0,b=3 has only three
possible deficient neighbors and is excluded by repeated neighbor triples.
At r=3 four analogous capacity/common-neighbor rows are excluded.

[check.py](check.py) generates all surviving masks and families and records
their counts, complete-entry SHA256 hashes and one witness each. The
retained H and neighbor families are separately necessary covers, not
assertions of compatible original faces or coordinates. Embeddings,
other Q opposites, ordinary-point incidence and metric equations remain
uncovered. The upper/lower degree theorems rely on the written proof and
h7786, not on interpreting a finite output as a packing exclusion.

[audit.py](audit.py), by the same author, independently loops over all raw
count boxes, every binary H edge subset, and every ordered labeled
neighbor-triple tuple. It compares all masks and all canonicalized neighbor
families entry by entry, including empty populations, with the production
cover. It supplies different enumeration algorithms, not an independent
mathematical reviewer or a proof-assistant theorem.

## 7. Reproduction and current context

CPython>=3.11, standard library only; audited with3.11.2. All calculations
in the proof checker are exact integers and fractions. From this directory:

```sh
python3 -B check.py > replay.json
cmp replay.json EXPECTED.json
python3 -B -O check.py > replay-optimized.json
cmp replay-optimized.json EXPECTED.json
python3 -B audit.py > audit-replay.json
cmp audit-replay.json AUDIT_EXPECTED.json
sha256sum -c SHA256SUMS
```

The production checker additionally enumerates every cyclic T/Q word in
the seven relevant degree/triangle roles and verifies the Q-Q capacities
and the deficient-four equality-case property.

Six negative controls reject a triangle H, missing required five H edges,
repeated degree-three neighbor triples, three common contacts of a deficient
pair, a second three contact at a deficit-one five, and two five contacts
at one three. Two positive controls accept basic necessary instances.
All requirements use explicit exceptions and work under Python-O.

The geometry, contact/face correspondence, star capacities and the r=4
quadrilateral-incidence argument remain written and unformalized. The
checker certifies the specified arithmetic and finite necessary covers;
it does not establish the unformalized bridges independently. No solver,
CAS, floating sign, external dataset or private search corpus is a proof
input. This package does not copy the preceding rational-function kernel.

The [current code table](https://cohn.mit.edu/spherical-codes/) and [N15 coordinates](https://spherical-codes.org/data/3/15),
refreshed on2026-09-30, still give the unstarred cosine
0.59260590292507377809642492233276 and known quintic
`13*c^5-c^4+6*c^3+2*c^2-3*c-1`. The890-byte coordinate table's SHA256
is `1b77ee43d73613885d3fdcfb03dc8fad2e40302ff9c9ff639559cc9b326fb805`.
The [N14 theorem](https://arxiv.org/abs/1410.2536) does not settle N15.
Bounded live primary/graph/source searches found no identical degree-
three restriction; no exhaustive priority claim is made.

Complementary research by **six-tammes-2**, role: researcher, excludes
the fourth prescribed decagon on its full strict-improvement domain:
[proof](../tammes15_decagon_chart_exclusion/PROOF.md), source
`04bf5ec7dfb2d56e939c23b9f56c3a13ab4db87e`, graph h7763
`bafkreicmbexlcgyvks7h7dahhl6qknlcfbzvlyrfjtcotjrllq4xbsv6uq`.
That theorem does not assert occurrence of its coordinate motif in our
remaining count profiles. The [independent eight-Q review](../tammes15_eight_quad_review4/REVIEW.md),
by six-reviewer-4, h7767, source
`7f8d065bd778621d2a519e2f581cd6c74e3a42d7`, independently confirms the
preceding local q8 theorem and its metric margin; it does not review the
new q9 proof. No reviewer target or verdict was requested or directed.

The next task is a complete original-face incidence cover in the32 rows,
starting with the r=1 seven-point Q star. Every degree-three neighbor is
now a known deficient role, and every five-contact branch has a constrained
H star. Ordinary fives, omitted Q opposites and original aliases must still
be retained. Larger faces and unrestricted optimizer coverage are separate
unresolved dependencies.
