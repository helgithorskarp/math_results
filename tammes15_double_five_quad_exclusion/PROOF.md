# The two ordinary fives have disjoint original triangle fans

Author: **six-tammes-1**, role: **researcher**, 2026-09-30.
Status: complete author-audited exact conditional lemma with a written
geometric reduction. Independent mathematical review and formalization
are pending.

## Statement and scope

Let fifteen distinct unit vectors have minimum geodesic separation d,
and let c=cos(d). Their **complete** contact graph gives a connected
cellular sphere decomposition into simple strictly convex triangles T
and quadrilaterals Q, each contained in an open hemisphere. On the
full interval `1/2<c<3/5`, assume exactly two vertices A,B have degree
five, each with four T faces and one Q; the other thirteen have degree
four.

**Local exclusion.** A and B cannot be opposite corners of one Q.

**Original-fan corollary.** Using the preceding
[contacting-five exclusion](../tammes15_adjacent_fives_exclusion/PROOF.md),
A,B do not contact, and their original six-point four-T fans are disjoint.
This means disjoint sets of original vertices, not disjoint normalized
copies. Their sole Qs are distinct. Twelve original points lie in the
two fans and three lie outside.

**Eight-Q corollary.** In the degree3..5, eight-Q branch with
`1/2<c<beta`, where beta is the unique root in `(119/200,3/5)` of

```text
1+4c+2c^2-4c^3-11c^4-24c^5,
```

the [three-five exclusion](../tammes15_three_five_exclusion/PROOF.md)
supplies degree pattern `(5^2,4^13)` and two ordinary fives. Both
corollaries apply. The two necessary profiles remain
`(d41,d42,d51,n3)=(4,0,0,0),(2,1,0,0)`, with thirteen fours and two
fives. The separated-four lists are now `{1,3}` and **`{2,4}`**:
the second profile's formerly allowed `s=0` is excluded by the endpoint
incidence argument in Section4a. The eleven inherited H types are
unchanged; these s restrictions need not delete a whole H type.

This is a reduction, not a realized packing or a complete enumeration.
The disjoint-fan branch, the entire eight-Q exclusion, larger faces and
coverage of global optimizers remain open. No improved global numerical
bound or Tammes-15 optimality is asserted.

## 1. The complete original-fan overlap split

Write

```text
alpha=acos(c/(1+c)); x=2*pi-4*alpha;
rho(u)=2*atan(1/(c*tan(u/2))); y=rho(x).
```

The inherited [ordinary-five geometry](../tammes15_eight_quad_reduction/FIVE_BOUNDARY.md)
and [corner-capacity proof](../tammes15_eight_quad_reduction/FIVE_CORNER_CAPACITY.md)
give throughout `(1/2,3/5)`, with ordinary fives explicit,
`alpha<qangle<2alpha`, `alpha<2*pi/5`, and `y>pi-alpha`.
At each F its sole Q has angle x, and the two adjacent Q corners
have angle y. A degree-four vertex has at most two Ts: three Ts and
one Q sum strictly below5alpha<2pi, while four Ts sum below2pi.

By the contacting-five exclusion, A,B are noncontacting. Let C(A),C(B)
be the sets consisting of each F and its five contact neighbors, with
four consecutive T faces. A,B are outside each other's fan. A point in
their intersection is a common contact neighbor. Two distinct unit
points have at most two common contact neighbors: their contact planes
meet in a line with at most two sphere intersections. Antipodal points
have none for c>0.

A shared point cannot be internal in either T link. An internal point
has two Ts in that fan and at least one different T in the other fan;
none of these Ts can coincide since A,B do not contact. This contradicts
the two-T ceiling. Thus every shared point is an endpoint in both links,
with one T from each fan, and is adjacent to each F in its sole Q.

If there were just one shared endpoint S, the sole Qs would be distinct:
if they were the same face, noncontacting A,B would be opposite, and
both other Q corners would be shared endpoints. In two distinct sole
Qs, S has two y corners and two T corners, giving
`2y+2alpha>2pi`, impossible. Exactly one shared point is excluded.

If there are two shared endpoints S,T, the sphere/contact-plane
intersection for S,T has the two distinct common neighbors A,B. In
A's sole Q, its other opposite corner is a different common neighbor
of S,T, so it must be B. Thus the full overlap split is: disjoint
original fans, or the double-five Q examined next. No external-ear
condition, assumed triangle connectedness or arbitrary fan disjointness
is inserted.

## 2. One structural patch, both metric seed branches

Suppose A=0,B=1 are opposite in their common Q `(0,2,1,3)`.
The original fans share exactly2,3 and have no other common neighbor.
Their links can be named

```text
A: 2,4,5,6,3; B: 3,7,8,9,2.
T faces: 024,045,056,063,137,178,189,192.
```

Every non-F point here is a degree four with two Ts already. The ten
original labels are distinct. This covers the structural patch up to
renaming and reflection; the two metric third-point choices below are
both checked, rather than choosing one from an orientation sample.

Use an equilateral basis `a0=e1,a2=e2,a4=e3` and

```text
H=(1-c)I+cJ; <u,v>=u^T H v; r=2*c/(1+c).
```

H has positive eigenvalues1-c,1-c,1+2c, so the coefficient space is
isometric to Euclidean R3. At a contact edge a,b with an old triangular
third point o, the two unit common neighbors are o and `r(a+b)-o`.
Two distinct adjacent triangular faces select the latter by original
injectivity. Hence

```text
a5=r(a0+a4)-a2;
a6=r(a0+a5)-a4;
a3=r(a0+a6)-a5.
```

For a Q with old opposite corner f and adjacent corners a,b, its other
opposite is

```text
Qopp(f;a,b)=2*c/(1+<a,b>)*(a+b)-f.                 (1)
```

The two contact planes and sphere have at most two intersections. A
simple Q selects the one different from f. Its denominator is positive:
Cauchy--Schwarz applied to a+b and the unit common neighbor f gives
`1+<a,b>>=2*c^2>0`. The checker additionally certifies every explicit
divisor sign before division. Thus `a1=Qopp(a0;a2,a3)`.

To seed B's first triangle, for any unit contact pair a,b let u be the
ordinary coefficient cross product `a cross b`. The two unit equilateral
third points are

```text
v_+-=c/(1+c)*(a+b)
      +-( (1+2c)*u-c*sum(u)*(1,1,1) )/(1+c).      (2)
```

For completeness, `w=H^-1 u` is H-orthogonal to a,b and
`<w,w>=(1-c^2)/det(H)`. The squared normal height above
`c/(1+c)*(a+b)` is `(1-c)*(1+2c)/(1+c)`. The positive multiplier of w
is `(1-c)*(1+2c)/(1+c)`, yielding (2). Both heights are nonzero, and
these are exactly the two intersections. No algebraic radical or
exceptional determinant parameter is omitted.

For each sign in (2) on `(a1,a3)`, set that result to a7 and form

```text
a8=r(a1+a7)-a3;
a9=r(a1+a8)-a7;
a2'=r(a1+a9)-a8.
```

The negative seed has `1-<a2',a2>>0` throughout `(1/2,3/5)`, so the
required endpoint equality fails everywhere. The positive seed has
`a2'=a2` coefficientwise. All unit/contact identities and poles are
checked. Its ten-point core has45pairs: eighteen identically contacts
and twenty-seven strictly noncontacting throughout the interval. This
also verifies original distinctness. The accepted seed is unique up
to the common ambient isometry.

## 3. Saturated stars force five more Q opposites

At2, the known two Ts and common Q form the contact-link path
`4,0,1,9`. These four distinct neighbors exhaust its degree four.
The remaining sector has endpoints4,9, which are strictly noncontacting,
so it is Q. At3 the path is `6,0,1,7`. Thus the next Qs are

```text
(2,4,10,9); (3,6,11,7),
a10=Qopp(a2;a4,a9); a11=Qopp(a3;a6,a7).
```

The twelve-position audit has66pairs: twenty-two identically contacts
and forty-four strict noncontacts. All twelve positions are unit,
distinct and free of coordinate poles over the full interval, so the
two opposites cannot be overlooked aliases of earlier original points.

Three more degree-four stars now have known link paths

| Vertex | Known link path | Missing-sector endpoints | Forced Q |
|---|---|---|---|
| 4 | 10,2,0,5 | 5,10 | (4,5,12,10) |
| 9 | 8,1,2,10 | 8,10 | (9,8,13,10) |
| 6 | 5,0,3,11 | 5,11 | (6,5,14,11) |

Each missing-sector endpoint pair is strictly noncontacting by the
twelve-point audit. These are Qs, not Ts. Their original opposite
corners have the forced positions

```text
a12=Qopp(a4;a5,a10);
a13=Qopp(a9;a8,a10);
a14=Qopp(a6;a5,a11).
```

Each of these assertions follows independently from the same twelve
original points and known faces. We **retain all possible original
aliases** of these new formal labels, including aliases among them.
We neither count fifteen distinct points nor assume one remaining point
outside a fifteen-point core. A fourth optional Q completion is not
needed. All fifteen formal positions have unit norm and no poles.

## 4. A forced alias leads to a closed-strip packing contradiction

Define packing gaps `gij=c-<ai,aj>`. The exact checker first proves

```text
g12,14<0 throughout (1/2,3/5).                    (3)
```

If12 and14 represented distinct original points, (3) would contradict
minimum separation. Thus any actual packing must have `a12=a14`.
Let

```text
P(c)=1+2c-5c^2-8c^3+6c^4+4c^5.
```

The **second coefficient** of `a12-a14` is exactly

```text
-2*c*P(c)/D(c),
D(c)=1+3c-3c^2-11c^3+4c^4+12c^5+2c^6.
```

D has a strict nonzero sign on the full interval, checked separately.
Consequently the necessary alias implies P(c)=0. No converse about
aliases is needed.

The degree-five Bernstein coefficients of P on `[1/2,11/20]` are

```text
1/4, 81/400, 617/4000, 4217/40000, 2811/50000, 5481/800000,
```

all positive. Its coefficients on `[14/25,3/5]` are

```text
-415679/9765625, -160397/1953125, -95079/781250,
-5037/31250, -3132/15625, -748/3125,
```

all negative. Therefore every possible P-root in `(1/2,3/5)` lies
in the smaller open strip `(11/20,14/25)`. This argument does not
require root uniqueness or a numerical root approximation.

But `1-<a12,a13>>0` throughout `(1/2,3/5)`, so12 and13 are always
distinct original points. On the **closed** strip `[11/20,14/25]`,
the numerator of their packing gap is strictly negative by Bernstein
coefficients, and its denominator is strictly positive on the full
interval. Thus

```text
g12,13<0 on [11/20,14/25].                       (4)
```

The checker records the exact numerator/denominator polynomials and
Bernstein ranges in [EXPECTED.json](EXPECTED.json). Any alias parameter
forced by (3) lies in (4), contradicting separation of the distinct
original points12,13. This excludes the double-five Q, including
possible aliases and strip endpoints. Section1 then proves the original
fans are disjoint.

## 4a. The free-triangle budget removes s=0 from the second profile

The two disjoint fans contain six internal ordinary fours R, each with
two consecutive Ts, and four endpoints, each with one known T. Let k
of these endpoints be ordinary fours with a second T (the promoted
ears). The other4-k endpoints are deficit-one fours D. Every promoted
endpoint is **separated**: its known T has edges to F and the neighboring
internal R. The edge to F has the known sole Q on its other side; the
internal R already has its maximum two Ts. An extra T cannot share
either edge of the endpoint's known T, so the two Ts are separated.

Degree sum gives31edges, and Euler gives18faces. Solving
`T+Q=18`, `3T+4Q=62` gives exactly10Ts and8Qs. The eight fan Ts are
all distinct, leaving two free Ts. They cannot involve either F or
the six internal Rs, which already exhaust their T sectors. A promoted
endpoint belongs to exactly one free T; each outside R belongs to both;
each outside D to exactly one; an outside U (zero-T four) to neither.
The two free Ts therefore share exactly the outside Rs. Three such Rs
would force the same convex T face twice, two mean a shared edge and
consecutive Ts at those Rs, one means a shared vertex and a separated
R, and zero mean disjoint Ts.

Put p=d42 in the two remaining eight-Q/beta profiles. There are
`4-2p` Ds, `9+p` Rs, and p Us. All Us are outside because every fan
point has a T. On the three outside original points the counts are

```text
outside D=k-2p; outside U=p; outside R=3-k+p.
```

The exact finite count audit gives:

| p | promoted endpoints k | outside (D,R,U) | free-T intersection | s |
|---|---:|---|---|---:|
| 0 | 1 | (1,2,0) | edge | 1 |
| 0 | 2 | (2,1,0) | vertex | 3 |
| 0 | 3 | (3,0,0) | empty | 3 |
| 1 | 2 | (0,2,1) | edge | 2 |
| 1 | 3 | (1,1,1) | vertex | 4 |
| 1 | 4 | (2,0,1) | empty | 4 |

These are necessary counts, not realizable triangle placements or a
complete edge/face enumeration. In particular the second profile has
at least two promoted endpoints and hence cannot have s=0. No symmetry
or triangle-connectedness premise enters this deduction.

## 5. Reproducibility, dependencies and limitations

[check.py](check.py) verifies both seed branches, all45/66 core pairs,
five complete saturated-star paths, all unit and denominator identities,
the alias polynomial factor, its outside-strip signs, full-interval
critical distinctness, the closed-strip forbidden gap and the six
necessary free-triangle count rows. Ten altered
certificates are rejected, including a wrong seed, an omitted Q, a
reused original core label, a claim that the alias pair is uniformly
distinct, and a strip that misses a possible root. All conditions use
explicit exceptions rather than Python assertions, so `python3 -O`
keeps them active.

For p on `[l,h]`, its exact Bernstein expansion has weights
`binom(n,k)*t^k*(1-t)^(n-k)`. Nonnegative coefficients with at least
one positive give strict positivity for `0<t<1`; nonnegative
coefficients and positive endpoint coefficients also cover the closed
interval. Negation gives the negative case. All interval endpoints and
coefficients are rational. Rational-function denominators and actual
construction divisors are checked independently, so cancellation does
not silently remove a singular geometric case.

The two small arithmetic modules are adapted from six-tammes-2's
[overlap kernel](../tammes15_bridge_overlap_reduction/README.md),
source `34d5a62d025ea9ade24e17c9ba848d297469063f`, graph
`bafkreifmazqrp77dkqbsh5f6wcme2ufxphjwkkjmoczsvdwwjepdl2zliy`
(h7488), via the preceding adjacent-five source. Shared kernels are
not an independent arithmetic audit. Original-point face interpretation,
the original-fan cover and inherited geometric statements remain written
mathematical bridges; this is not a proof-assistant formalization.

Exact graph/source prerequisites:

- Adjacent-five exclusion: source `21d7c373cfa2234494841a11642b53baf0380b7b`,
  graph `bafkreiekk7nnksnqfuav2yd2bezeildzxvcpp25ymk75ho4s7nqhumwvhi` (h7631).
- Degree pattern and no threes: source `d1f289db096e04d307604aa243d757574ffb998d`,
  graph `bafkreifqqkykpc6zwd6xmvvuq4yl7ik6qktmksr6ozase3fqm3hbt6k4fm` (h7562).
- Ordinary-five boundary: source `14b0fcbf082e2e9b5eff01e2ea2facd5405b9b07`,
  graph `bafkreih2mh527yek4vsnnmqgdlfjicxvludvrsoxgyvlb645soj5fjnb6m` (h7340).
- Corner capacities: source `9f43d6fdac0c7b0e0333c527c739cb0c24c68afb`,
  graph `bafkreiasa2n2mywlaokeron7wkpsj4z2ows4asfkm5fbnf6gphzbgmtvba` (h7444).
- Initial rhombus/profile reduction: source `2f9b8b2c7125c339a7a350437bc32b8aa40ac7db`,
  graph `bafkreiekf4d4rllqsf42fr5j5l36lb226ev4jsedqjvmyg6aqokjsrolzm` (h7232).

The old rhombus review
`bafkreiflxdrel4fv4opchhucsisp7ylw2lsfgtrv4q7tya3o5vjh4ld53a`
(h7182) concerns that precursor, not this new exclusion. Complementary
six-tammes-2 research excludes a specified decagon core on a closed
parameter strip; see its [proof](../tammes15_decagon_type0_cap_exclusion/PROOF.md),
source `dee2ed4ef0de70e9caf483bd8cf77d1d3c38278a`, graph
`bafkreiezfjdjqcwjeyc3g4uoi3t22ztq5kxcibqajzspplh5i3naq66gje`
(h7613). It is context, not a premise or review of this branch. No
teammate motif or external-ear occurrence is assumed.

Primary status was refreshed live on2026-09-30. The
[Cohn table](https://cohn.mit.edu/spherical-codes/) has an unstarred
N15entry with cosine0.59260590292507377809642492233276 and polynomial
`13c^5-c^4+6c^3+2c^2-3c-1`; the
[current coordinate table](https://spherical-codes.org/data/3/15)
is unchanged (890bytes, SHA256
`1b77ee43d73613885d3fdcfb03dc8fad2e40302ff9c9ff639559cc9b326fb805`).
[Musin--Tarasov arXiv1410.2536](https://arxiv.org/abs/1410.2536) solves
N14, not N15. These sources do not establish this campaign's conditional
branch exclusion; bounded searches are not an exhaustive priority check.

The next frontier is the relative placement of two disjoint original
six-point fans and the three outside points, including original aliases
of sole-Q opposites. No unrestricted optimizer coverage or improved
global separation bound follows merely from the present reduction.
