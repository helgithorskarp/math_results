# A uniform strict small-angle obstruction for the deltoidal hexecontahedron

Author: **six-rupert-1**, role **researcher**, 2026-09-30.

Let `K=conv(V)` be the standard deltoidal hexecontahedron in the exact
62-vertex model of [verify.py](verify.py). Write `P_n` for orthogonal
projection onto `n`-perpendicular, and `angle(Q)` for the full principal
angle of a proper three-dimensional rotation. Put `A=(0,0,1)`,
`s=sqrt(5)` and `phi=(1+s)/2`.

**Explicit twofold-cap theorem.** For every unit representative `n0` of
the body's 15 unoriented twofold axes, every unit receiver normal `n`
with `||n-n0||<=1/200`, every `Q in SO(3)` with
`0<=angle(Q)<=1/200` radians, every planar translation `t`, and every
scale `lambda>=1`,

```
lambda P_n(QK)+t is not strictly inside P_n(K).
```

Both receiver and inner directions vary. The inner normal in body
coordinates is `Q^-1 n`. The source orientation is restricted by the
stated full relative-angle bound, including its roll.

**Uniform small-angle corollary.** There exists a single `gamma>0` such
that the same strict exclusion holds for **every** unit receiver normal
and every proper rotation with `0<=angle(Q)<=gamma`, allowing arbitrary
translation and `lambda>=1`.

The explicit caps close the 15-axis frontier left by
[mirror_branch_proof.md](mirror_branch_proof.md). That result and the
[earlier stable cover](stable_proof.md) imply the uniform corollary by
compactness. A numerical value of the global `gamma` is **not computed**.
This work gives neither a global non-Rupert theorem nor a strict passage.
Rotations bounded away from identity remain unresolved. The named solid's
global Rupert status is still open in the primary literature checked.

The theorem concerns **strict** containment. There are nonidentity
closed equalities with angles tending to zero near `A`: the body reflection
`M_A=diag(1,1,-1)` and the receiver-plane reflection `M_n` give
`P_n(M_n M_A K)=P_n(K)`. The proper closed contact family near the other
exceptional orbit likewise remains valid.

## 1. Twelve stable singleton supports, despite three radii

Let `P(x,y,z)=(x,y)` and let `B1,B2:R^3 -> R^2` have orthonormal rows.
We first prove that

```
||B1-P||_op, ||B2-P||_op <= eta=1/100                  (1)
```

excludes a strict translated unit-scale containment `B1K+t` inside
`B2K`. The normals are the oriented cross products of the rows.

At the exact projection `A`, there are twelve extreme vertices, each
with a unique three-dimensional preimage and with height zero. Their
coordinates are, with independent signs,

```
(+/-s,0,0), (0,+/-s,0),
(+/-Lx,+/-Ly,0), Lx=(5+3s)/6, Ly=(5+s)/6,
(+/-lx,+/-ly,0), lx=(15+s)/22, ly=(25+9s)/22.
```

The useful exact ratios are

```
Lx/Ly=phi, ly/lx=phi^2.                               (2)
```

For each of these twelve vertices `v`, every other vertex `w` satisfies

```
(Pv).P(v-w) >= m=(135-35s)/242 > 0.                   (3)
```

These are **732 exact comparisons** against the full 62-vertex body,
including all hidden vertices. Thus the radial probe `Pv` uniquely
supports the projection at `v`. The twelve selected vertices have three
different radii; no common-radius hypothesis is imposed. The whole body
has maximum squared radius

```
R^2=(25+10s)/9.
```

For `v` selected, put `p=Pv` and `a=B1v`. The receiver support comparison
differs from (3) by at most

```
|a.B2(v-w)-p.P(v-w)| <= 4 R^2 eta+2 R^2 eta^2
                       =67/600+(67/1500)s < m.       (4)
```

Indeed `||a-p||<=R eta`, `||P(v-w)||<=2R`,
`||(B2-P)(v-w)||<=2R eta` and `||a||<=R(1+eta)` give this bound directly.
Consequently the receiver support in direction `a` is uniquely attained
at `B2v`. The same is true for the opposite probe and vertex `-v`.

If strict translated containment existed, these opposite inequalities
would give

```
||a||^2+a.t < a.B2v,
||a||^2-a.t < a.B2v.
```

Here `a!=0`, since `v` is equatorial and (1) has `eta<1`. Adding and
using Cauchy--Schwarz proves

```
||B1v|| < ||B2v||                                   (5)
```

for all twelve selected vertices. This is the antipodal singleton
argument used in **six-rupert-2**'s
[J77 proof, Section 4](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_critical_axes/PROOF.md#4-antipodal-projected-classes-remove-translation-locally),
building on **six-rupert-3**'s
[RID class analysis](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/LOCAL_PROOF.md).
Here all twelve classes are singletons, their actual unequal radii are
retained, and the contradiction uses the body's projection area.

Let the frame normals be `(xi,yi,zi)`, `i=1,2`. Their last coordinates
are positive: diagonal entries of the frame's first two columns exceed
`1-eta`, off-diagonal entries have absolute value at most `eta`, so their
determinant is at least `1-2eta>0`. Also `Bi ni=0` implies

```
sqrt(xi^2+yi^2)=||P ni||=||(P-Bi)ni||<=eta.
```

Thus `|xi|,|yi|<=eta` and `zi=sqrt(1-xi^2-yi^2)>1/2`. Since the frames
have orthonormal rows, `||Bi v||^2=||v||^2-(ni.v)^2`. Put

```
x=|x1|, y=|y1|, X=|x2|, Y=|y2|.
```

The axial vertices in (5) imply

```
x>X>=0, y>Y>=0.                                      (6)
```

The two signed mixed-coordinate families give

```
|phi*x-y| > |phi*X-Y|,
|x-phi^2*y| > |X-phi^2*Y|.                            (7)
```

This also holds if either actual normal changes component signs. To see
it, for a selected family `(r,+/-q,0)`, (5) for both signs yields

```
r^2(x^2-X^2)+q^2(y^2-Y^2) > 2 r q |x1*y1-x2*y2|
                         >= 2 r q (x*y-X*Y).
```

Hence `(r*x-q*y)^2>(r*X-q*Y)^2`, and (2) gives (7).
Taking absolute components here does not assume that the two frames can
be independently folded by a shared geometric gauge.

## 2. Exact projection area near the twofold direction

For positive last component, write the direction chart as
`u=(u_x,u_y,1)`. The exact chamber partition from
[orientation_certificate.py](orientation_certificate.py) has just two
cells incident to `A`: **cells 1 and 5**. Each interior silhouette has
sixteen vertices, including four hidden vertices that tie on four edges
of the twelve-vertex silhouette at `A`.

[twofold_area_certificate.py](twofold_area_certificate.py) reconstructs
both hulls. On all corners of each **whole closed polygon**, it checks
every edge against all 62 vertices, with **6,944 comparisons**, and
checks all **112** turn values. Each edge offset and turn is nonnegative
at all corners and positive at some corner. It follows that the hull is
complete and strictly convex over each cell interior. Its area formula
extends to every cell boundary by continuity. No hidden edge preimage
is omitted from the support comparisons.

For the cyclic hull `(vj)`, put `C=(1/2) sum(vj cross v_(j+1))`.
Its physical projection area in unit direction `n=u/||u||` is `n.C`.
The two exact coefficients are

```
cell1: C=(0,c*Cx,C0),
cell5: C=(Cx,0,C0),
C0=(160+150s)/33, Cx=(5+15s)/33, c=(5-s)/2=3-phi.      (8)
```

The checker proves that the entire small triangle

```
u_x,u_y>=0, u_x+u_y<=1/10
```

is covered by these cells, including its boundaries. It clips the
triangle along `u_x-c*u_y=0` and tests each resulting corner against
the full respective polygon. Cell 1 is the `u_x<=c*u_y` side; cell 5
is the other side. The body is invariant under separate reflections
of its coordinate signs. Thus for every unit normal `(x0,y0,z0)` with
`z0>0` and `(|x0|+|y0|)/z0<=1/10`, the projection area is exactly

```
Area(P_n K)=C0*z0+Cx*max(|x0|,c*|y0|).                (9)
```

The normals from (1) satisfy this domain condition: each coordinate has
absolute value at most `eta`, `zi>1/2`, and `4eta<=1/10`.

## 3. A four-case scalar comparison

Assume (6)--(7). Set

```
dx=x-X>0, dy=y-Y>0,
M1=max(x,c*y), M2=max(X,c*Y), D=M1-M2>0.
```

We prove the complete increment bound

```
dx+dy < 3D.                                          (10)
```

There are four choices of the dominant components in the two maxima.
All boundary ties can be assigned to either valid case.

**Both maxima use x.** Since `x>=c*y` and `phi>1/c`,
`phi*x-y>0`. The first inequality in (7) implies
`phi*dx-dy>0`. Here `D=dx`, so
`dx+dy<(1+phi)D=phi^2 D<3D`.

**Both maxima use c*y.** Since `c*y>=x` and `phi^2>c`,
`phi^2*y-x>0`. The second inequality in (7) gives
`phi^2*dy-dx>0`. Now `D=c*dy`, and
`dx+dy<(phi^2+1)D/c=phi^2 D<3D`.

**The first uses x, the second c*Y.** If `phi^2*y>=x`, the second
inequality in (7) again gives `dx<phi^2*dy`; if its left side were zero,
the strict inequality itself would be impossible. Also
`D=x-c*Y>=c*dy`, giving `dx+dy<phi^2 D`.
Otherwise `y<q*x`, where `q=1/phi^2`. Then

```
D=x-c*Y >= x-c*y > (1-c*q)*x,
dx+dy <= x+y < (1+q)*x < 3D,
```

using the exact positive denominator and comparison
`1-c*q>0`, `3(1-c*q)>1+q`.

**The first uses c*y, the second X.** If `y<=phi*x`, the first
inequality in (7) gives `dy<phi*dx`. Since `D=c*y-X>=dx`,
`dx+dy<phi^2 D`. Otherwise `x<y/phi`, so

```
D=c*y-X >= c*y-x > (c-1/phi)*y,
dx+dy <= x+y < (1+1/phi)*y < 3D,
```

using `c-1/phi>0`, `3(c-1/phi)>1+1/phi`.

The exact checker replays all field constants used in these cases,
including `(phi^2+1)/c=phi^2` and `phi^2<3`. This argument covers
arbitrary real normal coordinates; it is not a sampled-direction claim.

## 4. Area contradicts strict containment

For the two normals from Section 1, (6) implies `z1<z2`. Since all four
absolute components are at most `eta` and `z1+z2>1`,

```
z2-z1 = [(x+X)*dx+(y+Y)*dy]/(z1+z2)
       < 2eta*(dx+dy) < 6eta*D.                      (11)
```

Using (9), the difference between inner and receiver areas is

```
Area(B1K)-Area(B2K)=Cx*D-C0*(z2-z1)
                  > (Cx-6eta*C0)*D > 0,             (12)
Cx-6eta*C0=(-23+30s)/165>0.
```

But containment requires the inner area to be at most the receiver area.
Thus the hypothesized strict containment under (1) is impossible.
Strictness was used in the singleton support comparisons, not in a
numerical area tolerance. Closed equality is not excluded.

Scale `lambda>=1` causes no difficulty. The body is centrally symmetric
with the origin in its interior. A strict scaled translated containment
can be centered by reflecting and taking convex midpoints; dividing
the centered copy by `lambda` gives strict unit-scale containment.
Alternatively the opposite support calculation directly yields
`lambda*||B1v||<||B2v||`, which implies (5). The unit-scale obstruction
therefore excludes all such scales and translations.

## 5. Explicit receiver caps and the uniform angle conclusion

Suppose `||n-A||<=1/200`. Choose the shortest proper rotation `S`
taking `n` to `A`. Its operator chord is exactly `||n-A||`. The frame
`B2=P S` therefore satisfies

```
||B2-P||<=1/200.
```

For `angle(Q)<=1/200`, take `B1=B2 Q`. Since
`||Q-I||=2 sin(angle(Q)/2)<=angle(Q)`,

```
||B1-P||<=||B2-P||+||Q-I||<=1/100.
```

The frame theorem applies and proves the explicit cap at `A`. It includes
zero relative angle, when equality of the bodies already precludes strict
unit-scale containment. Body symmetries transport the cap to all fifteen
unoriented axes and both unit signs; orthogonal conjugation preserves
the full proper-rotation angle and projection containment. The verified
15-axis orbit is from [stable_certificate.py](stable_certificate.py).

The preceding [stable theorem](stable_proof.md) supplies joint receiver
and angle neighborhoods excluding even closed containments with nonzero
relative angles outside its
45-axis set. [mirror_branch_proof.md](mirror_branch_proof.md) supplies
strict-exclusion neighborhoods at the other thirty axes. The new caps
cover the remaining fifteen. Every unit normal now has a receiver
neighborhood with a positive strict angle bound. Use open sub-neighborhoods
and choose a finite subcover of the compact unit sphere. The minimum of
their positive bounds is a single `gamma>0`. Zero angle is handled by
equality, and scale reduces as above. This proves the uniform corollary.

No numerical lower bound for this global `gamma` follows merely from the
explicit `1/200` twofold caps: the E-orbit bounds in the earlier proof are
existential. A future quantitative global claim must bound those caps
and the complementary cover rather than quote `1/200` as a global angle.

## 6. Reproduction, provenance and remaining problem

From repository root, standard Python 3.11 or later:

```sh
python3 -B geometry/rupert_deltoidal_symmetry/twofold_area_certificate.py --self-test
```

Expected output: [expected_twofold_area.json](expected_twofold_area.json).
The checker regenerates the vertices, twelve radial supports, both complete
sixteen-vertex hulls, whole-cell supports and turns, small-triangle cover,
area constants, and every scalar field inequality. Three malformed
controls reject frame radius `1/50`, reversed hull orientation and an
omitted hull corner. Only small source and expected output are needed;
there is no external input or omitted large corpus.

Trust includes the exact standard body model, the inspected ordered
`Q(sqrt(5))`/Fraction kernel, finite hull and support checks, and the
written frame-support perturbation, four-case scalar comparison, projection
area, symmetry and compactness arguments. No solver, floating-point search,
CAS transcript or analytic-path assumption is a proof input. The proof
is unformalized and has not been independently reviewed.

The class method is credited above to the public J77/RID work. The
unequal-radius singleton selections, exact area formula and scalar
increment comparison are computed and proved for this named Catalan
solid; no status or theorem is transferred through duality. Own
dependencies are the exact model/chamber, the stable cover and the
E-orbit exclusion. Previous results remain valid with their original
strict or closed quantifiers.

Current primary context is
[Gosain–Grimmer, Tables 3–4](https://arxiv.org/html/2509.08190),
[Scott's definitions](https://arxiv.org/html/2208.12912),
[Steininger–Yurkevich's projection criteria](https://arxiv.org/abs/2112.13754),
the supplied [Nopert seed](https://arxiv.org/abs/2508.18475), and the
[stellated-tetrahedron seed](https://arxiv.org/html/2604.26531).
The standard coordinates are from
[McCooey](https://dmccooey.com/polyhedra/DeltoidalHexecontahedron.txt).
Bounded live literature checks still leave the global deltoidal question
unresolved and support no historical priority claim.

The highest-value remaining frontier is now **nonlocal relative rotations**.
Useful next steps include an explicit quantitative global angle gap and
an invariant or certified receiver-region reduction for source orientations
away from body symmetries. A strict construction must retain the full
three-dimensional relative rotation, complete correct receiver hull and
all 62 inner vertices. Lack of a numerical witness is not nonexistence.
