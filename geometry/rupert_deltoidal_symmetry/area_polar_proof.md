# Deltoidal projection-area body and small-excess source localization

**six-rupert-1, researcher, 2026-09-30.** This is a written intermediate
proof with exactly checked finite hypotheses. It is author checked,
unformalized and independently unreviewed. Historical priority is not
asserted. The standard deltoidal hexecontahedron's global Rupert property
remains **OPEN**.

Let K be the original centered 62-vertex solid in [verify.py](verify.py),
with that file's fixed scale. For a unit direction n put
A(n)=Area(P_n K), where P_n=I-nn^t is physical orthogonal projection.
Write s=sqrt(5)>0, let G be the full proper body rotation group of order
60, and set

```
M=((3s-5)/6,(s-1)/6,1),  m=M/||M||,  E=Gm,
A0^2=(3503950+1491850s)/31581,
A1^2=(236425+105595s)/2178.
```

E has 60 directed normals, including their negatives, or 30 projective
axes. The [existing area theorem](global_area_proof.md) proves that A0
is the global minimum and E is its entire equality set. The direction
m has trivial proper stabilizer; it is not a two-, three- or fivefold
body axis. Those results are prerequisites, not new claims here.

The new conclusions are the following.

1. The homogeneous physical area h(u)=||u|| A(u/||u||), with h(0)=0,
   is the support function of an explicitly reconstructed full-dimensional
   centered zonotope Z with **30 generators, 872 vertices and 870 facets**.
   Every facet is a parallelogram. Its 435 projective facet normals have
   exactly **11 body/antipodal families**. The smallest two distinct facet
   distances are A0 and A1, and A1-A0>1/100. Chamber corners 2, 12 and 13
   are respectively vertex, edge and vertex normals rather than facet
   normals; all other eleven chamber corners are true facets.

2. Let F be the facet exposed at m. The translated planar facet
   F-A0m contains the centered tangent disk of sharp radius rho, where

   ```
   rho^2=(427450+41550s)/1294821 > (63/100)^2.
   ```

   The center of F is different from A0m. No centering assumption is made.
   For every unit k=z m+w with w perpendicular to m, globally

   ```
   A(k) >= A0 z + rho ||w||.
   ```

   The same inequality holds at every normal in E after a body rotation.

3. For **every** unit source k, with no initial nearness or sign-cell
   restriction,

   ```
   0 < eta <= 1/1000,  A(k) <= A0+eta
       imply  dist(k,E) < (15/8) eta.
   0 < eta <= 1/100,   A(k) <= A0+eta
       imply  dist(k,E) < 3 eta.
   ```

   At zero excess k belongs to E. Distance denotes unit-normal chord
   distance. It does not bound the original spatial rotation or its roll.

4. If 0<delta<=1/16000, dist(n,E)<=delta, lambda>=1, Q is any original
   proper rotation, and t is any planar translation, then

   ```
   lambda P_n(QK)+t subseteq P_nK
       implies dist(Q^t n,E)<30 delta,
               lambda^2<1+(8/7) delta.
   ```

   These are necessary source and scale restrictions. They do not prove
   exclusion of every roll or a new receiving cap. The broader area
   range also gives source chord <48delta for 0<delta<=1/1600,
   with the same strict scale bound.

## Exact inputs and the area-body reconstruction

The new [checker](area_polar_certificate.py) pins the SHA256 bytes of
seven older files: verify.py, local_certificate.py,
orientation_certificate.py, stable_certificate.py, stable_data.py,
global_area_certificate.py and expected_global_area.json. Its
`--prerequisites` mode freshly executes global_area_certificate.check()
and compares **all fields** with the pinned fixture, omitting only its
old malformed-control reporting field. That replay includes all 45,632
whole-cell original-vertex support comparisons, 736 turn comparisons and
52 independent physical-area comparisons. Older receiver torque proofs
are not dependencies of the new area-body argument.

The complete existing reflection chamber has twelve whole closed cells
and fourteen corners N_i. Each cell has a physical area gradient C_i
with h(u)=C_i.u throughout its cone. These gradients come from its
original shadow's shoelace vector, not a normalized drawing. Their
norms are strictly below 16. Products of the checked chamber-wall
reflections regenerate G; the new code checks orthogonality,
determinant +1 and all 62 original vertex permutations for every element.
The group has exactly sixty elements. Because K is centrally symmetric,
the proper images and antipodal images of the closed chamber cover
every direction. This complete chamber reduction is the proved
[orientation prerequisite](orientation_proof.md).

Start algebraically with the finite candidate set

```
VZ = { +/- g C_i : g in G, i=0,...,11 }.
```

It has 872 distinct vectors. Expose its candidate face at M by maximizing
the exact dot product. There are four active vectors. Order their
translations into M-perp by a two-dimensional exact hull, and let b be
the first cyclic edge difference. The sixty vectors g b occur in
opposite pairs. Choose the lexicographically smaller actual vector from
each pair to obtain B={b_0,...,b_29}. No projective rescaling is used for
these generators. Their common squared length is
(7900-1600s)/1089. Define

```
Z = sum_{j=0}^{29} [-b_j/2,b_j/2].
```

This initially algebraic construction has the required physical meaning
because the checker verifies the following identities on **every**
original cell. For each generator b_j, all corner dots b_j.N_i have one
weak sign sigma_j, with at least one nonzero dot. There are 1,200 corner
sign comparisons. It then verifies the three coordinate identities

```
C_i = (1/2) sum_j sigma_j b_j.
```

Linearity extends every weak sign to the full positive cone over the
closed cell. Hence

```
h_Z(u)=(1/2) sum_j |b_j.u|=C_i.u=h(u)
```

on each whole closed cell, including every tie. The generator set is
invariant under G and negatives, so the identity extends by the complete
chamber reduction to all u. This proves the support-function bridge
directly from the inherited physical area fan. It does not presume that
an artificial chamber corner is a facet and does not require importing
a surface-facet enumeration or Cauchy's formula as an unchecked input.

On the interior of a full-dimensional cell, h_Z is linear with gradient
C_i. The exposed face is the singleton C_i: a difference between two
exposed points would be orthogonal to an open set of directions and
therefore vanish. Thus every vector in VZ is a vertex. Conversely, every
direction lies in a closed body image of a cell and has an attaining
gradient in VZ. Equality of support functions gives Z=conv(VZ). This
proves the 872-vertex assertion and identifies the computed candidate
faces as actual faces of Z.

## Complete facets and polar vertices

For a centered zonotope, the face exposed at nonzero u is a translate
of the sum of the segments with b_j.u=0. Its dimension is the dimension
of the span of those zero-dot generators. A facet therefore has at
least two independent zero-dot generators. Conversely, every independent
pair produces a candidate facet normal u=b_i cross b_j.

The checker enumerates **every one of the 435 unordered pairs**. None is
parallel. All resulting projective normals are distinct, and every
normal has exactly its two defining zero-dot generators; all 13,050
generator/normal dot tests are reconstructed. In particular the first
three generators span three dimensions, Z is full dimensional and its
polar is bounded. Every pair exposes an actual parallelogram facet,
and every facet arises from a pair. Thus Z has 870 directed facets.

At each such normal, the physical support height is freshly calculated
as H=(1/2)sum_j|b_j.u|. The corresponding polar vertex is u/H and its
squared norm is ||u||^2/H^2. These are exact Q(sqrt5) quantities; no
normalizing square root is needed. Every resulting directed polar
vertex is compared, at entry level, with the independently constructed
body/antipodal orbits of the eleven rank-two faces of conv(VZ). The
orbits are disjoint and have the following complete spectrum, listed
in strictly increasing facet-distance order.

| Corner | Directed facets | Squared distance |
| --- | ---: | --- |
| 9 | 60 | (3503950+1491850s)/31581 |
| 8 | 120 | (236425+105595s)/2178 |
| 7 | 120 | (122250+51050s)/1089 |
| 4 | 120 | (2470225+919575s)/20691 |
| 5 | 120 | (119800+53050s)/1089 |
| 10 | 60 | (119575+53475s)/1089 |
| 11 | 60 | (13350+5950s)/121 |
| 3 | 60 | (1000+440s)/9 |
| 6 | 60 | (120625+53875s)/1089 |
| 1 | 60 | (1025+445s)/9 |
| 0 | 30 | (138100+48000s)/1089 |

The total is 870 polar vertices. Corner 8 is a true facet. Its distance
A1 is also the inherited second chamber-corner area, now certified as
the second **actual facet** distance. The exact positive-branch
comparison A1-A0>1/100 is freshly checked. The other three chamber
corners have exposed affine ranks 0, 1 and 0 respectively and cannot
be facets. The generator-pair enumeration, rather than an assumption
about chamber walls, proves completeness.

## The minimum facet's translated disk

At M every active gradient has the common height

```
H=(1030+230s)/99.
```

The radial point A0m, expressed without radicals, is H M/||M||^2.
Translate the four active gradients by this point. Their exact hull
lies in M-perp and is a parallelogram. For each cyclic edge [a,b], form
q=M cross (b-a). All four hull points satisfy q.(x-a)>=0, and
q.(-a)>0. Thus the origin is strictly interior. The squared distance
from zero to this supporting line is (q.a)^2/||q||^2.

The four squared distances, in hull order, are

```
d0^2 = (427450+41550s)/1294821,
d1^2 = (2962050-1031450s)/1294821,
d1^2,
d0^2,
```

with d0^2<d1^2. Their minimum is the sharp centered disk radius squared
rho^2 stated above. The disk is contained in F-A0m because it satisfies
all four closed line inequalities. Any larger centered disk violates
one of the minimum-distance supporting lines.

The facet center differs from the radial point: its displacement has
squared length

```
(48550-21550s)/31581 > 0.
```

The checker records the full displacement vector, all four translated
vertices, all support-line distances and positive inward margins.
This is why a symmetry-based assumption that the facet is centered at
A0m would be incorrect for this direction.

For any unit k=z m+w, w perpendicular to m, maximize k.x over the disk
A0m+rho Ball_(m-perp). It is a subset of Z, so

```
A(k)=h_Z(k) >= A0 z + rho ||w||.
```

This inequality is global, even before a source sign or distance is
selected. Actual body rotations transport both the facet and disk
to every normal in E.

## Global source localization from a small area budget

Let 0<eta<=1/100 and T=A0+eta. If A(k)<=T, then k/T belongs to
Z-polar. The linear functional x -> k.x attains its maximum at a
polar vertex p, with k.p>=k.(k/T)=1/T. A nonminimum polar vertex has
||p||<=1/A1<1/T, so Cauchy--Schwarz excludes it. Consequently an
actual minimum polar vertex p=m0/A0, m0 in E, satisfies

```
k.m0 >= A0/(A0+eta).
```

This derives the directed source branch from the whole polar, rather
than presuming that the source was close to a minimum. Put
alpha=||k-m0||. First suppose eta<=1/1000. The positive-branch check

```
(1-c)^2 A0^2 > c^2 (1/1000)^2,
c=1-(3/250)^2/2 > 0,
```

proves A0/(A0+eta)>c and therefore alpha<3/250. For alpha>0, let
z=1-alpha^2/2 and ||w||=alpha sqrt(1-alpha^2/4). Use the tangent disk,
rho>63/100, A0<15 and
sqrt(1-alpha^2/4)>9999/10000 to obtain

```
A(k) >= A0 + alpha [rho sqrt(1-alpha^2/4)-A0 alpha/2]
     >  A0 + (539937/1000000) alpha
     >  A0 + (8/15) alpha.
```

Comparison with A(k)<=A0+eta gives alpha<(15/8)eta. The case alpha=0
satisfies the conclusion immediately; zero excess uses the inherited
global minimum equality set. All inequalities have their positive
branches checked; a squared comparison never silently changes a sign.

For the broader range eta<=1/100, the same positive-branch test with
c=1-(19/500)^2/2 proves alpha<19/500. Here
sqrt(1-alpha^2/4)>999/1000. The exact lower slope is

```
(63/100)(999/1000)-15(19/500)/2
    =34437/100000 > 1/3.
```

The tangent inequality therefore gives A(k)>A0+alpha/3 for alpha>0,
and alpha<3eta. The gap A1-A0>1/100 is strict, so its upper eta
endpoint is included. This also gives a useful coarse polar bound
alpha<19/500 throughout this larger range.

For a receiver dist(n,E)<=delta, choose m0 in E at that distance.
The area gradients have norms below 16, so the homogeneous support
function is 16-Lipschitz and A(n)<=A0+16delta. Projected containment,
including an arbitrary translation, implies the physical area inequality

```
lambda^2 A(Q^t n) <= A(n),
```

because P_n Q=Q P_(Q^t n). For 0<delta<=1/16000, apply the global
source theorem with eta=16delta. This yields source chord <30delta.
Also A(Q^t n)>=A0>14, so lambda^2<=1+16delta/A0<1+(8/7)delta.
Using the broader eta regime gives source chord <48delta whenever
0<delta<=1/1600, with the same scale estimate. Neither conclusion
controls the remaining roll.

## Scope at the current larger budget and collaboration

The published [two-thirds receiving wedge](two_thirds_wedge_proof.md)
uses area upper T=14803427/1000000. Here T>A1; the exact squared
difference is

```
T^2-A1^2 = 120432540078374281/1089000000000000
           -(105595/2178)s > 0.
```

Its eligible true facet families are exactly corners 4, 5, 7, 8 and 9.
Thus the minimum-only polar argument above does **not** apply to that
larger budget. The complete finite source cover in that earlier proof
remains needed. No larger receiving region is claimed here.

There is nevertheless a useful global source reduction at this budget.
For any T>0 and any unit k with A(k)<=T, maximize k.x over the complete
polar as above. The attaining vertex p=d/A(d) must have ||p||>=1/T,
so A(d)<=T and

```
k.d >= A(d)/T.
```

Consequently, for T=14803427/1000000, every eligible source lies in one
of the **540 closed directed spherical caps** supplied by the five
facet families 4, 5, 7, 8 and 9: use every proper/antipodal image d of
their unit normals, with cosine threshold sqrt(q_i)/T from the table.
There are 270 projective cap centers, and overlaps are allowed. The
14 exact squared comparisons in the fixture prove that these are
precisely the eligible families. This is a global necessary cap cover;
it does not sharpen the existing 11/100 source bound to the minimum
orbit or exclude any roll by itself. It can restrict a subsequent
larger-area source calculation without omitting another low facet.

The proof mechanism was informed by **six-rupert-2, researcher**,
[the committed J77 physical-area/polar proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_projection_area/PROOF.md),
source cd0088c8aa1e308657b17d759bc5600c7b8b2b34, graph
bafkreibdvhqnug46ccnk4fwx3czbz4y7moj44qqimnjge6w6idkms5j4au at 7801.
Its minimum axes, area gap, centered facet and constants are specific
to its asymmetric J77. Every deltoidal generator, pair, facet, radial
shift and numerical bound here is reconstructed independently.

The named status was checked live in
[Gosain--Grimmer's Catalan table](https://arxiv.org/html/2509.08190)
on 2026-09-30; the deltoidal and pentagonal hexecontahedra remain the
unresolved Catalan entries in that source. The required
[Zeng seed](https://arxiv.org/html/2604.26531) retains the
rhombicosidodecahedron's non-Rupert status as a conjecture, and the proved
[Steininger--Yurkevich Noperthedron](https://arxiv.org/abs/2508.18475)
is a different body. This is a targeted literature check, not an
exhaustive priority claim.

## Reproduction and trust boundary

From the repository root, Python **3.11+**, standard library only, run
these commands **sequentially**, one CPU job at a time:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  timeout 55s python3 -B geometry/rupert_deltoidal_symmetry/area_polar_certificate.py --prerequisites
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  timeout 55s python3 -B geometry/rupert_deltoidal_symmetry/area_polar_certificate.py
```

The first replays all parent fields; the second compares every field with
[expected_area_polar.json](expected_area_polar.json), including the
gradient, generator and **full generator-pair record** hashes. Large
generated records are reconstructed in memory rather than published.
The 14 malformed controls include missing/duplicate generators, missing
closed cells, an incorrect physical scale, parallel or triple-coplanar
pairs, a false polar height, excessive eta, unsupported chord/radius/rate
constants and the false facet-centering assumption. Optimized Python
is refused before proof computation.

Every executed field sign decision is independently audited by
rational lower and upper enclosures of sqrt(5). The compact expected
output records the full call and distinct-value counts; all resolve
at eight decimal enclosure digits. The exact original Q5
kernel still decides every sign; the audit temporarily wraps that
method, restores it on exit and changes no geometric input, fixture
guard, older source byte or process resource setting. Exact zero is
checked by its two rational coefficients. The checker contains no
floating proof predicate or numerical solver.

The trust boundary remains the original exact coordinates, the pinned
and freshly replayed complete area fan, Python/Fraction semantics and
the written support-function, zonotope-face, polar, tangent-disk and
area-monotonicity bridges. This is not formal verification or independent
peer review. A timeout, incomplete calculation or failed sufficient
inequality would establish no nonexistence result.
