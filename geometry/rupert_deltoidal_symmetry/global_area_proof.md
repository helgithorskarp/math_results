# Global shadow areas and all-source receiver caps for the deltoidal hexecontahedron

Author: **six-rupert-1**, role **researcher**, 2026-09-30.

Let `K=conv(V)` be the centered standard 62-vertex deltoidal
hexecontahedron from [verify.py](verify.py), let `s=sqrt(5)` and
`phi=(1+s)/2`, and let `P_n` denote orthogonal projection onto the plane
perpendicular to a unit normal `n`. Set

```
A(n)=Area(P_n K),
M=((3s-5)/6,(s-1)/6,1), m=M/||M||,
B=(0,phi^-2,1),
qmin=(3503950+1491850s)/31581,
qmax=(350+150s)/3,
rho=1/20000000.
```

The matrix `J_n=2nn^T-I` is the proper half-turn about the receiver
normal. Write `G` for the proper body rotation group, verified below to
have sixty elements.

**Global area theorem.** Over every unit direction,

```
min A(n)=sqrt(qmin), attained exactly on G.m,
max A(n)=sqrt(qmax), attained exactly on G.(B/||B||).
```

The minimum has **sixty directed normals, or thirty unoriented axes**.
Its representatives are not twofold, threefold or fivefold rotation axes:
the proper stabilizer of `m` is trivial. The maximum has twenty directed
normals, the ten threefold axes. Fivefold directions are not area
minimizers, although their areas are smaller than the twofold and
threefold views examined in the first symmetry certificate.

**All-source receiver theorem, including closed classification.** For
every unit `m0 in G.m`, every unit receiver normal with
`||n-m0||<=rho`, every `Q in SO(3)`, every scale `lambda>=1`, and every
planar translation `t`,

```
lambda P_n(QK)+t subseteq P_n(K)
  if and only if lambda=1, t=0, Q in G union J_n G.       (1)
```

There are exactly **120 relative rotations** in the displayed union,
two left cosets of `G`. They give equal shadows. Consequently these
thirty closed receiver caps exclude **every strict passage**, for
arbitrary source direction, full rotation, roll, translation and scale
at least one. No source-angle restriction is assumed. The small angle
used later is derived after transformations preserving the projected
inner body.

**Universal scale bound.** Any closed projected containment, with any
receiver and source, satisfies

```
lambda^4 <= qmax/qmin < (507/500)^4.                     (2)
```

The first inequality is strict for strict containment. This supplies a
global upper bound below `1.014` for passage scale. It supplies neither
a strict passage nor a global non-Rupert proof. Receivers outside the
stated caps remain a nonlocal frontier. The earlier
[uniform strict small-angle gap](twofold_area_proof.md) remains valid.

## 1. Complete area formula on the chamber cover

The three body wall reflections have normals

```
(1,0,0), (0,1,0), (-phi,-phi^2,1).                       (3)
```

They permute all 62 vertices, as rechecked exactly. Their finite group
folds every nonzero direction into
`x,y>=0, z>=phi*x+phi^2*y`. One proof chooses an orbit point maximizing
`z`, makes its first two coordinates nonnegative, and observes that
violating the last wall would allow its reflection to increase `z`.
Rescale to `z=1`; the resulting closed chamber is

```
conv{(0,0,1),(1/phi,0,1),(0,phi^-2,1)}.
```

The [chamber generator](orientation_certificate.py) splits it along
thirty unoriented planes into twelve whole closed convex polygons and
fourteen distinct corners. Each exact clipping split preserves area and
the two half-plane pieces cover their parent, so no direction is omitted.
This is the prior [chamber construction](orientation_proof.md).

[global_area_certificate.py](global_area_certificate.py) regenerates the
entire silhouette of each cell at its interior mean. It checks every
edge against **all 62 original vertices at every cell corner**, giving
**45,632** support comparisons, and checks all **736** adjacent turn
values. Each edge offset and turn is nonnegative at every corner and
positive at some corner. By linearity it is positive over the cell
interior. The chosen cyclic polygon is the complete convex hull there;
all its vertices are projected body vertices and its supporting edges
contain every original projected vertex. Hidden edge preimages are
included in the comparisons.

For its cyclic three-dimensional vertex list `(v_j)`, put

```
C=(1/2) sum(v_j cross v_(j+1)).
```

The physical area at `n=u/||u||` is

```
A(n)=C.u/||u||.                                         (4)
```

Projection commutes with this normal component of the cross products.
Continuity of projection and convex polygon area extends (4) to every
cell boundary, including collinear or collapsed edges. Independently of
the cell area vector, the checker constructs the projected hull in
orthogonal coordinate functionals `e1,e2=u cross e1`. Coordinate
shoelace squared, divided by `||e1||^2 ||e2||^2`, matches (4) at every
cell center and every corner incidence. It keeps all projection ties.
No orthonormal square-root rounding is needed.

The generated cell hulls, area vectors and all fourteen squared corner
areas are in [expected_global_area.json](expected_global_area.json).
Every corner numerator `C.u` is positive. Formula (4), rather than a
sampling of directions, is the continuum input to the bounds below.

## 2. Exact global extrema, equality cases and area coercivity

If a cell corner `u_j` has area at least `a`, then
`C.u_j>=a||u_j||`. For `u=sum t_j u_j`, `t_j>=0`, `sum t_j=1`,

```
C.u >= a sum t_j||u_j|| >= a||u||.                       (5)
```

Thus a lower bound at all corners bounds the whole closed cell. If two
distinct corners have positive weights, the norm triangle inequality is
strict: their unit-z vectors are nonparallel. Since `a>0`, equality in
(5) can occur only at a single corner whose area equals the bound.

The checker compares every squared physical corner area over `Q(s)`.
There is exactly one minimal chamber corner: **node 9**, equal to `M`.
Its squared area is `qmin`. The second smallest distinct squared corner
area, at node 8, is

```
qsecond=(236425+105595s)/2178.
```

Every other corner has greater area, so (5) and its equality case prove
the minimum and classify all minimizers in this chamber. Body symmetry
gives exactly the orbit of `M`, checked in Section 3.

For an upper bound, (4) and Cauchy--Schwarz give `A(n)<=||C||`.
The largest squared cell-vector norm is exactly `qmax`; only cell 0
attains it. Its vector ray is `B`, and `B` belongs to the cell and has
squared physical area `qmax`. Equality in Cauchy--Schwarz forces that
ray. This proves and classifies the maximum, with symmetry supplying
the other threefold axes.

Write `a0=sqrt(qmin)` and `Delta=sqrt(qsecond)-a0`. The exact checker
proves `Delta>1/100` on the correct positive branch, using

```
qsecond-qmin-1/10000 > 0,
(qsecond-qmin-1/10000)^2 > qmin/2500.                    (6)
```

All normalized points of the chamber are within chord `2/5` of `m`.
The three chamber corners satisfy positive-dot cap tests with cosine
greater than `23/25`; positive cone combinations and the norm inequality
extend this to the whole chamber. Exactly cells **4,7,9** contain `M`.
Every normalized corner in those cells is within chord `1/5` of `m`,
proved by positive-dot tests with cosine greater than `49/50`.
The checker squares only after checking that each dot is positive.

For such an incident cell write `u=sum t_j u_j` and set

```
alpha_j=t_j||u_j||/sum t_k||u_k||,
v=sum alpha_j(u_j/||u_j||), n=v/||v||,
beta=sum alpha_j over corners different from M.
```

The area bound gives `A(n)>=a0+Delta*beta`. Moreover,

```
||n-m|| <= 2||v-m|| <= (2/5)beta.                       (7)
```

The first inequality uses `|1-||v|||<=||v-m||` and `||m||=1`.
For nonincident cells (5) gives `A(n)>=a0+Delta`, while the whole
chamber bound gives `||n-m||<=2/5`. Fold arbitrary normals into the
chamber; orthogonal symmetries preserve area and the minimizer orbit.
Both cases give the global quantitative estimate

```
dist(n,G.m) <= (2/(5Delta))*(A(n)-a0)
             <= 40*(A(n)-a0).                          (8)
```

At a minimizer both sides vanish. For positive area excess the final
inequality is strict. This is a proved rate, not a presumed perturbation
ansatz.

The homogeneous function `H(u)=||u||A(u/||u||)`, `H(0)=0`, is continuous
and piecewise linear on the finite symmetry images of the cell cones.
Each slope is an orthogonal image of a checked `C`, of norm less than
`16`. Restricting it to any line segment, including segments on fan
boundaries, proves global `16`-Lipschitz continuity. In particular

```
A(n)-a0 <= 16||n-m0||   for every unit m0 in G.m.        (9)
```

Finally, area of a scaled source is `lambda^2 A(source)` and translation
does not change it. The global extrema immediately give (2).

## 3. The complete proper group and the minimum shadow

Let `R0,R1,R2` be the reflections in (3). The checker closes the two
proper generators `R0 R1` and `R1 R2`, finding exactly sixty matrices.
It checks their inverse membership and all **3,720** body-vertex images.
Their `M` orbit has sixty directed vectors, includes `-M`, and has
thirty projective axes. The wall-reflection projective orbit matches it
exactly. This proves the stated full minimizer set without assuming
that the proper group is transitive on arbitrary directions.

The `B` orbit has twenty directed normals, including its antipode.
These are the threefold axes; the product of its two adjacent wall
reflections is an order-three axial rotation. The stabilizer of `M`
among the sixty proper matrices has order one.

The minimum shadow has sixteen extreme vertices with unique preimages.
Among **all 62 original projected vertices**, exactly indices **4,57**
attain its maximum squared radius

```
R0_shadow^2=(155+65s)/58>4.
```

They are antipodal. Every other original projection has squared radius
at most `5`. A planar rotation preserving this shadow must send either
maximum-radius point to itself or its antipode; it is therefore the
identity or half-turn. Both preserve the shadow by central symmetry.
Its planar rotation group is exactly **C2**.

The proper receiver half-turn `J_m` does not permute the body vertices.
All 62 supplied points are actual three-dimensional extreme vertices:
each is strictly exposed by its own radial normal, with all **3,782**
comparisons checked. Thus `J_m K!=K`.

This also proves that the sixty-matrix group is the **full** proper body
group. If a proper `R` preserves `K`, it takes area-minimizing normals
to area-minimizing normals. Choose a member `h` of the sixty-matrix
group with `h m=R^T m`; then `Rh` fixes `m` and preserves the
minimum shadow. Its C2 rotation group forces `Rh=I` or `J_m`. The latter
cannot preserve `K`, so `R` is in the verified sixty-matrix group.

At the exact minimizing receiver, closed containment with scale at least
one forces equal minimum areas and `lambda=1`. After removing translation
by central symmetry, the source shadow is contained and has equal area,
so it is the same convex body. Align its minimizing normal by a right
body symmetry. The remaining rotation fixes `m` and is in the shadow's
C2 group. Thus `Q in G union J_m G`. The original translation must be
zero: a nonzero translation of a compact convex body cannot lie in itself,
as its support function in the translation direction increases.

Conversely, `gK=K` and `P_n J_n=-P_n` imply

```
P_n(gK)=P_n(K), P_n(J_n gK)=-P_n(K)=P_n(K).              (10)
```

These are explicit closed equal-shadow constructions for every receiver.
The next sections prove that they exhaust all closed containments on a
specified positive receiver neighborhood, allowing all original angles.

## 4. Source-normal elimination and control of arbitrary roll

Reflect a closed containment in the origin and take convex midpoints.
Since `K=-K`, this removes any planar translation. A centered scaled
containment with `lambda>=1` implies centered unit-scale containment,
because `0 in K` and `K` is convex. These reductions preserve all necessary
conditions used below. In particular, area gives

```
A(Q^T n)<=A(n).
```

Let `delta=||n-m||<=rho`. Applying (8)--(9) gives

```
dist(Q^T n,G.m)<=640delta.                              (11)
```

Choose a minimizing normal `m1` attaining that finite-set distance and
`h in G` with `h m=m1`. Replacing `Q` by `Qh` preserves `QK`. Its source
normal `n1=h^T Q^T n` is within `a=640delta` of `m`.

Take an oriented orthonormal-row receiver frame `B2` with cross-product
normal `n`; its source frame is `B1=B2 Qh`. Let `R2,R1` be shortest proper
rotations taking `m` to `n,n1`, respectively. Their operator chords are
at most `delta,a`. With `B0=B2 R2`, both `B0` and `B1 R1` have oriented
normal `m`, so some `U in SO(2)` satisfies

```
B2=B0 R2^T, B1=U B0 R1^T.
```

Set `S=B0K`, an isometric copy of the minimum shadow. The full body's
radius is less than `5/2`, checked from all vertices. For every `v in K`,
`U B0v=B1 R1v` is within `Rbody*a` of `B1v in B2K`, and `B2K` is within
`Rbody*delta` of `S`. Thus the actual containment implies

```
US subseteq S+eta Disk, eta<=1603delta.                  (12)
```

Only this one-sided inclusion is needed. It retains the whole source
rotation; no initial small-roll hypothesis is imposed.

Reduce `U` modulo the shadow's C2 group to angle `alpha in [-pi/2,pi/2]`.
This does not change `US`, since `S=-S`. Let `p,-p` be its two maximum
radius points and `R0_shadow=||p||`; put `r_other=sqrt(5)`. Every other
original projection has norm at most `r_other`. The support function of
`S` in the unit direction of `Up` is therefore at most

```
max(R0_shadow*cos(alpha), r_other).
```

But (12) and the source point `Up` give

```
R0_shadow <= max(R0_shadow*cos(alpha),r_other)+eta.       (13)
```

The exact positive-branch square comparison proves
`R0_shadow-r_other>1/1000`. Since `eta<=1603rho<1/1000`, the second
branch cannot reach the left side. Consequently

```
1-cos(alpha)<=eta/R0_shadow,
||U-I||_op^2=2(1-cos(alpha))<=2eta/R0_shadow<=eta.        (14)
```

Here `R0_shadow>2`; if `eta>0` the last comparison is strict. It rejects
the whole remote part of the reduced roll range, rather than searching
or sampling rolls. At `eta=0` it forces `U=I` modulo C2.

The planar half-turn can be realized by a **proper** left multiplication
`J_n` of the source rotation, because

```
P_n(J_n Qh K)=-P_n(Qh K)=P_n(Qh K).                    (15)
```

Choose `sigma in {0,1}` to make the reduced roll and put
`Q'=J_n^sigma Qh`. Equation (15) preserves the entire projected source
body, even at arbitrary translation and scale.

Completing the oriented frames by their normals shows that `Q'` is a
product of three proper rotations: a receiver transport with chord
`<=delta`, a planar lift with chord `<=sqrt(1603delta)`, and an inverse
source transport with chord `<=640delta`. For chords at most one,
`2arcsin(c/2)<=2c`. The rotation-angle triangle inequality therefore gives
the **full** principal angle, including roll,

```
theta(Q')<=2(641delta+sqrt(1603delta))<9/500.             (16)
```

For example, the angle triangle inequality follows by multiplying unit
quaternions: a product of factor angles `b,c` with `b+c<pi` has scalar
part at least `cos((b+c)/2)>0`, hence angle at most `b+c`. The present
bounds keep the sum below `pi`. The last inequality in (16), uniformly
throughout the cap, is checked by the purely rational tests

```
9/1000-641rho>0,
1603rho < (9/1000-641rho)^2.                            (17)
```

The original `Q` can have any full angle. Only the exactly equivalent
projected-source presentation `Q'` has the derived bound.

## 5. Four stable supports exclude every nonzero gauged angle

The prior [stable data](stable_data.py) give four weak supports and four
strict exposing chords at chamber node 9. We use their explicit choices,
checking all required properties again rather than importing a prior
neighborhood size. In the fixed vertex indexing they are

```
contacts (a,b,j): (57,59,59),(58,45,58),(45,34,34),(20,4,20),
exposing (c,d):   (57,55),   (55,45),   (45,36),   (36,4).
```

For `epsilon=1/1000` define

```
E_i=V_b-V_a+epsilon*(V_d-V_c),
m_i(u)=E_i cross u, T_i(u)=V_j cross m_i(u).             (18)
```

At `u=M`, all four probes strictly support `K` at their stated `V_j`.
All **244** comparisons with the other body vertices are positive, with
minimum

```
gap0=(-11+5s)/3600>0.                                  (19)
```

The checker verifies `||E_i||<5`. It constructs four strictly positive
signed determinant cofactors of the torques, checks their exact balance
`sum L_i T_i(M)=0`, and checks all four squared facet distances from the
origin are greater than `81/2500`. Thus their full-dimensional torque
tetrahedron contains the centered ball of radius **9/50**. No differently
rescaled rows or weights enter this identity.

Write the receiver ray `u=n/n_z`. Since `||M||<11/10`, `m_z>10/11`;
`n_z>10/11-rho>4/5`. It follows directly that

```
||u-M|| <= (1/n_z+1/(n_z*m_z))*delta
          < (21/8)delta <3delta,
||u|| <11/10+3rho <6/5.                               (20)
```

The body radius is less than `5/2`, so every strict support gap in (19)
changes by less than `75delta`. Hence the probes still support at the
same actual vertices, throughout the entire receiver cap and across all
chamber boundaries. Their exposure margin satisfies

```
gap0-75rho>1/25000.                                    (21)
```

Each torque changes by less than `38delta`. Convex support functions
therefore show that the actual torque hull contains the centered ball
of radius `9/50-38rho`. This argument does not assume that its center
facets or extreme points persist.

If `Q'` has unit axis `a` and nonzero full angle `theta<=9/500`, some
actual torque satisfies `a.T_i(u)>=9/50-38rho`. The rotation exponential
remainder has operator norm at most `theta^2/2`. Also
`Rbody*||m_i(u)||<(5/2)*5*(6/5)=15`. Consequently

```
m_i(u).(Q'V_j-V_j)
 >=theta*(9/50-38rho-(15/2)*theta)
 >theta/25>0.                                         (22)
```

The last step uses the exact rational margin

```
9/50-38rho-(15/2)*(9/500)>1/25.                        (23)
```

Since `m_i(u)` is perpendicular to the receiver normal and actually
supports its shadow at `V_j`, (22) contradicts even centered unit-scale
**closed** containment. Thus the gauged rotation must be identity.

## 6. Closed classification, distinct rotations and symmetry transport

From `Q'=J_n^sigma Qh=I` we obtain
`Q=J_n^sigma h^-1`, so the original source rotation belongs to the two
left cosets in (1). Equation (10) now gives equality of the source and
receiver shadows. The original area inequality implies `lambda=1`,
since the receiver area is positive. With scale one the original
containment becomes `P_nK+t subseteq P_nK`. Applying its support function
in the direction `t` forces `t=0`. This recovers the original translation
and scale after their temporary removal. Conversely, all choices in (1)
give the equal shadows in (10), proving the equivalence with all boundary
cases included.

To count distinct rotations throughout the cap, the checker compares
`J_m` to every one of the sixty proper body matrices and finds

```
min_(g in G) ||J_m-g||_F^2=(106-36s)/29>8rho^2.          (24)
```

For unit normals,

```
||J_n-J_m||_F^2=8(1-(n.m)^2)<=8||n-m||^2.              (25)
```

Therefore `J_n` cannot belong to `G` anywhere in the stated cap. Two
left cosets of a subgroup are either equal or disjoint; these two are
disjoint, and each has sixty elements. There are exactly 120 rotations
in the classification.

For a general minimizing normal `m0=g0 m`, conjugate the entire
containment by the proper body rotation `g0^-1`. It preserves the body,
scale, area, chord distance and principal angle. It maps the receiver
half-turn by `g0^-1 J_n g0=J_(g0^-1 n)` and preserves `G` by conjugation.
Every estimate and the classification transport to that cap. The
sixty directed orbit points include their antipodes, giving thirty
unoriented receiver axes. Strict containment is impossible at identity
or at any of the remaining classified equal-shadow rotations. This
proves the all-source receiver theorem.

## 7. Reproduction, provenance and remaining frontier

From the repository root, with standard Python 3.11 or later:

```sh
python3 -B geometry/rupert_deltoidal_symmetry/global_area_certificate.py
python3 -B geometry/rupert_deltoidal_symmetry/global_area_certificate.py --self-test
```

The normal replay regenerates and checks the complete finite hypotheses.
The self-test additionally rejects five deliberately malformed controls:
an incomplete cell cover, a reversed hull, a missing hull corner, a
false fivefold minimum, and an unsupported receiver cap `1/1000000`.
Rejection of the larger cap only records that these estimates fail to
certify it. Its mathematical validity remains a separate question.
The expected self-test JSON is
[expected_global_area.json](expected_global_area.json), with SHA256

```
22196b0e3e6449841ac3686cc518aa51d354d41e743ff7599c77f1b6ff39dd32
```

The self-test passed in approximately 29 seconds on Python 3.11.2,
using one process and about 17 MiB peak child RSS. All finite proof
decisions use exact ordered `Q(sqrt(5))` or rational arithmetic.
Optimized Python is explicitly refused because it disables assertions.
No solver, floating-point decision, third-party package, CAS transcript,
external input file or omitted large corpus is a proof input. The
fixture comparison is a regression check; the mathematical result rests
on the checked finite hypotheses and the continuous arguments above.

The trust boundary includes the standard model in
[verify.py](verify.py), its exact field kernel, the complete clipping
cover and hull generator in
[orientation_certificate.py](orientation_certificate.py), and the
explicit four contacts from [stable_data.py](stable_data.py). The new
checker rechecks body symmetry, radial extremality, whole-cell supports,
area comparisons, group closure, projection radii, exposures, torque
cofactors, facet distances and every quantitative cap inequality.
The underlying written chamber and support arguments are in
[orientation_proof.md](orientation_proof.md) and
[stable_proof.md](stable_proof.md). The proof is complete and
unformalized; independent review is not claimed.

The source-normal elimination followed by roll control is methodologically
informed by **six-rupert-3**, researcher, whose
[adaptive RID receiver proof](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/ADAPTIVE_RECEIVER_PROOF.md)
was read alongside its durable checkpoint. That proof's equal-radius
diameter invariant and body-specific constants are not used here. The
related local-to-uniform distinction is made explicit in
**six-rupert-2**, researcher's
[J77 uniform proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_uniform_local_exclusion/PROOF.md).
These complementary results concern other named solids. The present
area vectors, minimum orbit, coercivity, C2 roll reduction, strict torque
probes and all numerical bounds are verified for this Catalan body.
The earlier [uniform strict small-angle result](twofold_area_proof.md)
is complementary and is not assumed in the all-source cap proof.

A fresh pre-publication read also found six-rupert-3's
[axial-height transport refinement](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/DIRECTIONAL_TRANSPORT_PROOF.md)
and six-rupert-2's
[all-source J77 diameter caps](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_all_source_diameter_caps/PROOF.md).
The former offers a useful sharper transport estimate for the next
receiver-domain extension; the latter handles an asymmetric shadow with
a separate half-turn obstruction. The present proof uses its own
central symmetry and coarser whole-body transport bound (12).

The primary status and definitions were checked live on 2026-09-30:

- [Gosain--Grimmer, Tables 3 and 4](https://arxiv.org/html/2509.08190)
  retain the deltoidal and pentagonal hexecontahedra as unresolved Catalan
  cases. The listed numerical search value is not an exact certificate.
- [Scott, local and reverse Rupert definitions](https://arxiv.org/html/2208.12912)
  distinguishes the relevant local notions.
- [Steininger--Yurkevich, projection formulation](https://arxiv.org/abs/2112.13754)
  supplies the standard geometric passage equivalences. Here passage
  exclusion uses strict projected containment of the congruent source;
  scale at least one is included in the stronger displayed statements.
- The mandated [Nopert seed](https://arxiv.org/abs/2508.18475) and
  [stellated-tetrahedron seed](https://arxiv.org/html/2604.26531) supply
  current context. The latter retains the rhombicosidodecahedron
  conjecture and does not resolve this Catalan solid.
- Coordinates agree with
  [McCooey's standard deltoidal model](https://dmccooey.com/polyhedra/DeltoidalHexecontahedron.txt).

Bounded primary searches did not locate this specific area-and-cap
classification. No historical priority assertion follows from that
search. The global Rupert property remains unresolved. The concrete
next frontier is to enlarge certified all-source receiver regions with
sharper area-sublevel and roll estimates, or construct and exactly check
a strict passage in the remaining domain. Any candidate must be checked
against the complete receiver hull and all 62 source vertices.
