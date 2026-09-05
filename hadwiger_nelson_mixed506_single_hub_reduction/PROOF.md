# A single-hub reduction for disjoint mixed506 placements

Put `alpha=i sqrt(3)`, `R=Q(sqrt(33))`, and
`E=R+alpha R=Q(i sqrt(3),i sqrt(11))`. The point with four coefficients
`(a,b,c,d)` is `a+b sqrt(33)+c i sqrt(3)+d i sqrt(11)`.
This is the restricted complex field, not a larger Cartesian coordinate field.

Let `A=v159e646` and `V=v214e977` be the archived Parts point sets. Fix
`t=(5+i sqrt(11))/6` and `B=A union tA`, with the source labels retained as
in the earlier construction. Thus `B` has 292 vertices and 1,251 strict
unit edges; `V` has 214 vertices and 977 strict edges.

For a **disjoint** placement `B union g(V)`, call edges with one endpoint
in each component *cross edges*, and count only these when referring to
cross degree. A vertex of cross degree at least three is called a *hub*.

**Theorem.** Every disjoint placement satisfies one of the following:

1. `g(E)=E`, and the union is four-colorable by the previously proved
   whole-field coloring.
2. `g(E)!=E`, and there is at most one hub across both components. Its
   cross degree, if it exists, is at most ten. Every other vertex has
   cross degree at most two.

The bound ten is attained with the hub in either component by explicitly
checked disjoint 506-vertex graphs. Both examples are four-colorable.

There are exactly 881 points outside `B` that are unit distance from at
least three points of `B`, and 534 analogous points outside `V`. All belong
to `E`. Consequently every disjoint placement with a hub belongs to one of
`881*214 + 534*292 = 344,462` labeled anchor families described below.
If such a placement is not four-colorable, its unit rotation multiplier
must have degree exactly two over `E`.

This is a necessary-condition reduction, **not** a four-colorability theorem
for all disjoint placements. The angular cases and the family with no hub
have not been enumerated. No five-chromatic graph is supplied.

## 1. Three neighbors put their center in the field

Let three distinct points of `E` have unit distance from a point `z` in the
plane. They cannot be collinear: a line meets a circle in at most two points.
Write the neighbors as `x_j+alpha y_j`, with `x_j,y_j in R`, and write
`z=x+alpha y`, where initially `x,y` are arbitrary real numbers. Subtracting
the three squared-distance equations in pairs eliminates `x^2+3y^2` and
gives two linear equations

\[
2(x_j-x_1)x+6(y_j-y_1)y
=x_j^2+3y_j^2-x_1^2-3y_1^2,\qquad j=2,3.
\]

Their determinant is nonzero by noncollinearity. All coefficients belong
to `R`, so `x,y in R` and `z in E`.

Now let `P,Q` be arbitrary subsets of `E`. Write an isometry as
`g(z)=u z+h` or `u conjugate(z)+h`, with `|u|=1`. If `E` and `g(E)` share two
distinct points, their preimages and images give `u,h in E` by subtraction
and division, using the closure of `E` under conjugation. Hence `g(E)=E`.
Thus, when `g(E)!=E`, their intersection has at most one point.

A hub lying in `g(Q)` has three neighbors in `P`, so the center argument
puts it in `E intersection g(E)`. A hub lying in `P` has three neighbors in
`g(Q)`; applying `g` inverse and the same argument puts it in that same
intersection. For disjoint `P` and `g(Q)` two hubs would be two distinct
points of the intersection. This proves the single-hub assertion for any
such two subsets of `E`, independently of a finite enumeration.

The field-preserving branch uses the prior
[whole-field four-coloring](../hadwiger_nelson_nonmono_field_obstruction/PROOF.md).
The center and intersection arguments themselves do not require a coloring.

## 2. Complete center catalogs

For a finite point set `P subset E`, let `C(P)` consist of all plane points
unit distance from at least three distinct points of `P`. Section 1 proves
`C(P) subset E`. We compute it by intersecting unit circles about all pairs.
For distinct `a,b`, write `d=b-a`, `n=d conjugate(d)`, and `m=(a+b)/2`.
There is no real center if `n>4`. Otherwise the two centers, or the single
center at `n=4`, are

\[
m\mathbin{\pm}\frac{\alpha d}{2}s,
\qquad s^2=\frac{4-n}{3n}.
\]

The centers lie in `E` exactly when the nonnegative real quantity on the
right has a square root in `R`. Indeed, if a center lies in `E`, dividing
its offset from `m` by `alpha d/2` gives a real element of `E`, hence of `R`.

The generator decides this square condition and constructs its roots using
rational arithmetic. For `a+b sqrt(33)` with `b=0`, it tests rational squares
of `a` and `a/33`. For `b!=0`, a square requires `a^2-33b^2` to be a rational
square. Testing both signs of that square root in `(a +/- sqrt(a^2-33b^2))/2`
and recovering the other coefficient from `2xy=b` is necessary and sufficient.
Zero discriminants and centers belonging to the component are retained.

For each generated center the complete pair incidence list gives its full
neighbor set. A center with `k` neighbors occurs exactly `binomial(k,2)`
times. The program checks that multiplicity and each retained unit distance.
Discarding centers with fewer than three neighbors loses nothing from `C(P)`.

| Component | `B` | `V` |
|---|---:|---:|
| Vertices | 292 | 214 |
| Unordered pairs | 42,486 | 22,791 |
| Pairs farther than two | 6,453 | 4,382 |
| Pairs with unit-circle centers outside `E` | 26,625 | 11,683 |
| Pairs with unit-circle centers in `E` | 9,408 | 6,726 |
| Distinct pair centers in `E` | 2,629 | 1,456 |
| Centers with at least three neighbors | 1,173 | 748 |
| Such centers outside the component | 881 | 534 |
| Maximum external-center degree | 10 | 10 |

The complete external-center degree distributions are:

| Degree | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `C(B) minus B` | 440 | 225 | 114 | 59 | 29 | 5 | 5 | 4 |
| `C(V) minus V` | 256 | 130 | 88 | 36 | 12 | 4 | 0 | 8 |

If the hub lies in `g(V)`, it is an external center of `B`, and its cross
degree is exactly its catalog degree. If it lies in `B`, its preimage is
an external center of `V`. The maximum ten therefore bounds every hub in
the theorem's second branch. It does not bound degrees in the
field-preserving branch.

## 3. A different complete audit through triangles

The auditor independently parses the pinned coordinates and constructs
`B`. It neither imports the circle-intersection generator nor uses its
square tests or field arithmetic. For every triple it first checks whether
all three side lengths are at most two, a necessary condition for lying on
a unit circle. For the surviving triples it uses Heron's identity.

Let `A,B,C` now denote the numerators of the squared side lengths at common
coordinate scale `S`; all three belong to `Z[sqrt(33)]`. The circumradius is
one exactly when

\[
ABC=S^2\bigl(4AB-(A+B-C)^2\bigr).
\]

The positive numerator for three distinct points excludes the collinear
case. Each accepted triple gives its center by a linear two-by-two solve
over `Q(sqrt(33))`. All triples at a center reconstruct its complete neighbor
set; the auditor also checks their multiplicity `binomial(k,3)`.

| Component | `B` | `V` |
|---|---:|---:|
| All triples accounted for | 4,106,980 | 1,610,564 |
| Triples with every side at most two | 2,680,610 | 950,868 |
| Triples of circumradius one | 49,302 | 32,792 |

The Heron identity was also used in the earlier
[Parts-509 completion-center audit](../hadwiger_nelson_parts509_completion_census_degree9/README.md).
Here it is applied to the two different mixed506 components, without
importing or re-enumerating that replacement family.

The two methods match **every center and every neighbor set**, not only
these counts. Catalogs and their complete hashes are reproducible from the
source. The audit compares geometric data; the generator separately checks
the coloring-extension masks described in the README.

## 4. Anchors and the required rotation degree

The equality `conjugate(V)=V` is checked from the coordinates, so all
orientation-reversing images of `V` also occur as orientation-preserving
images with relabeled source points. It suffices to write `g(z)=u z+h`.

If the hub is in `g(V)`, choose its source label `q in V` and center
`r in C(B) minus B`. Then

\[
g(z)=r+u(z-q),\qquad |u|=1.
\]

There are `881*214=188,534` such labeled center/anchor pairs. If the hub is
in `B`, choose `p in B` and its preimage `s in C(V) minus V`; then

\[
g(z)=p+u(z-s).
\]

There are `292*534=155,928` such pairs. These are parameterized anchor
families, not isomorphism types, distinct point sets, or a census of angles.

Consider the first form. After translating by `-r`, an additional cross
edge away from the hub has endpoints `b'=b-r` and `u d`, where `d=v-q!=0`.
Here `b'!=0` because `r` is outside `B`. The unit-distance equation becomes

\[
c u^2-Su+\overline c=0,
\qquad c=\overline{b'}d\ne0,
\quad S=|b'|^2+|d|^2-1.
\]

All coefficients belong to `E`. Thus any additional cross edge forces `u`
to be algebraic of degree at most two over `E`. The second form is identical
after translating by `-p`: an edge away from `p` again has two nonzero
component displacements. Degree one puts both isometry parameters in `E`
and is already four-colorable.

If there is no cross edge away from the hub, the cross graph is just its
star. Color `B union {r}` using the field coloring and color `V` properly,
then permute the latter colors to agree at `q` and `r`. Restricting gives a
proper union coloring. For a hub in `B`, color `V union {s}` instead and
make the same gluing argument. Consequently a non-four-colorable disjoint
placement with a hub must have a rotation multiplier of degree **exactly
two** over `E`.

This proves that higher-degree algebraic and transcendental rotations in
these anchor families give four-colorable star attachments. It does not
claim that every quadratic rotation fails, or handle hub-free placements.

## 5. Exact sharpness examples

Choose

\[
u=\frac{\sqrt3+i\sqrt6}{3},\qquad
3u^4+2u^2+3=0,\qquad |u|=1.
\]

This multiplier has degree four over `E`. To see this, none of `sqrt(2)`,
`sqrt(3)` or `sqrt(6)` lies in `E`, since these are real and the real subfield
is `Q(sqrt(33))`. Thus `E(sqrt(2),sqrt(3))/E` is biquadratic. Its four sign
changes give four distinct values of `u=(sqrt(3)+alpha sqrt(2))/3`.
The quartic identity alone is not being used to infer irreducibility.

Take the following external centers, written in the four-coefficient basis:

\[
r_B=(-2/3,\ 1/9,\ -1/18,\ 1/6),\qquad
s_V=(-1/4,\ -1/12,\ -5/12,\ -1/4).
\]

Their ten-neighbor lists in the fixed component order are

```text
r_B: 74 191 193 205 210 229 232 257 264 266
s_V: 68 72 89 90 125 127 163 176 189 194
```

The two placements are `g_1(z)=r_B+u(z-V[0])` and
`g_2(z)=u(z-s_V)`, with hub respectively `g_1(V[0])=r_B` and `B[0]=0`.
Their quartic multiplier makes all other cross edges impossible by Section 4.
It also prevents an overlap: an overlap would express `u` as a quotient of
two nonzero elements of `E`, since the selected center is external.

The standalone checker reconstructs both placements in the eight-dimensional
real radical basis of `Q(sqrt(2),sqrt(3),sqrt(11))`, with complex coordinate
numerators at common scale 72. It imports none of the field, census or
triangle-audit modules. For each placement it checks all 127,765 pairs and
finds 506 distinct vertices and exactly `1251+977+10=2238` strict unit edges.
The ten cross edges are precisely the displayed star. Explicit color
permutations of the first published component rows give proper four-colorings,
checked on every edge. Thus the maximum ten is attained on either side.

## 6. Scope, provenance and trust

The general center/intersection argument is elementary; no novelty priority
is claimed. The finite center classification, its complete independent
algorithmic audit, and the exact sharpness examples supply the reproducible
information specific to this construction. The methods are author
cross-checks, not external peer review or proof-assistant formalization.

The coordinate [provenance](../hadwiger_nelson_nonmono159_214_lowden2/SOURCE.md)
and fixed [inner construction](../hadwiger_nelson_nonmono159_moser_triple/PROOF.md)
are reused. The source paper is Parts,
[Graph minimization](https://arxiv.org/abs/2010.12665).
[Haugland's August 2026 introduction](https://arxiv.org/html/2608.04542v4),
checked on 2026-09-05, retains the 509-vertex benchmark.

Trust rests in the unformalized geometric and field arguments, exact Python
arithmetic, pinned source coordinates and dependencies, and ordinary
execution. No floating-point distance, SAT verdict or large omitted proof
certificate is used. The regenerable center catalogs are omitted from git;
the verifier outputs them for the triangle auditor. Neither all disjoint
placements nor the 344,462 angular families are certified four-colorable.
