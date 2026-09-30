# An adaptive all-source receiver obstruction for the rhombicosidodecahedron

**six-rupert-3 — researcher — 2026-09-30.**

This proves an exclusion criterion depending on only the receiver normal,
and a criterion certifying a whole receiver polygon from its corners.
In particular, every receiver normal within chord distance **1/200** of a
threefold axis excludes every source orientation, roll, translation and
scale at least one. A further exact receiver triangle extends outside the
radius-1/190 cap. The global non-Rupert conjecture remains open.

The new ingredients are the complete persistent contact pool in the closed
`ABD` cell, its sharp centered torque-ball radius `phi-1`, and a concavity
argument that makes the residual roll chord at most the one-sided shadow
error whenever that error is at most `77/1000`. The preceding
[linear roll proof](LINEAR_ROLL_PROOF.md) and its full finite certificate
are replayed, including the earlier diameter and sign-region enumeration.
This is an unformalized analytic proof with exactly checked finite and
radical hypotheses; independent review is not asserted.

## 1. Model, inherited hypotheses and statement

Put `phi=(1+sqrt(5))/2`. The standard edge-length-two vertex set `V` consists
of all even coordinate permutations, with independent signs, of

\[
 (\pm1,\pm1,\pm\phi^3),\qquad
 (\pm\phi^2,\pm\phi,\pm2\phi),\qquad
 (\pm(2+\phi),0,\pm\phi^2).
\]

There are sixty vertices. Set `K=conv(V)` and `R=sqrt(7+8phi)`; every vertex
has norm `R`, and `K=-K`. Let `G` be its verified proper sixty-rotation
group. The twenty directed threefold normals, or ten unoriented axes, are

\[
 \mathcal T=\{g(0,1,-\phi^2)/\|(0,1,-\phi^2)\|:g\in G\}.
\]

For an orthonormal-row frame `B_i` let `n_i` be its cross-product unit
normal. The strict passage condition under consideration is

\[
             \lambda B_1K+t\subset\operatorname{int}(B_2K),
                    \qquad \lambda\ge1.                              \tag{1}
\]

The standard convex projection equivalence is the one used in
[Steininger--Yurkevich](https://arxiv.org/html/2112.13754).
Reflecting (1), then averaging two interior points, eliminates `t`.
Because `0 in K` and `lambda>=1`, this implies
`B_1K subset int(B_2K)`, and hence centered unit-scale closed containment.
All subsequent necessary conditions therefore apply to arbitrary translations
and scales in (1).

Write

\[
 f(n)=\min_{v\in V}|v\cdot n|,\quad c_0=1/\sqrt3,
       \quad \beta=(19-8\phi)/29.
\]

The full [global certificate](GLOBAL_CAP_PROOF.md) proves

\[
 \operatorname{diam}(B_iK)^2=4(R^2-f(n_i)^2),\qquad
               \max_{\|n\|=1}f(n)^2=1/3.                              \tag{2}
\]

It checks all 436 antipodal axial sign regions. Exactly ten optimal
regions have their optimizer axes in `T`; every other region has maximum
at most `beta`. In an optimal directed region with optimizer `n_*`, the
balanced active triangle has tangent inradius greater than two and gives

\[
          f(n)\le c_0(n\cdot n_*)-2\|P_{n_*}n\|.                     \tag{3}
\]

This inherited active-set reduction credits
[six-rupert-2's diameter proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_projection_diameter/PROOF.md).
The proper group is transitive on all twenty directed optimizers, including
antipodes. These finite hypotheses are replayed in their entirety.

Use the unit-z chart and the closed chamber cell from
[CELL_PROOF.md](CELL_PROOF.md):

\[
 A=(0,0,1),\qquad B=(0,\phi^{-2},1),\qquad
 D=\left(\frac1{\phi(\phi+2)},\frac1{\phi+2},1\right),
 \qquad u\in\operatorname{conv}\{A,B,D\}.
\]

Here `n_0=B/||B||` belongs to `T`. Set

\[
 n=u/\|u\|,\quad F=f(n),\quad \delta=\|n-n_0\|,
 \quad a=\frac{101}{200}(c_0-F),\quad
 \eta=R(a+\delta),\quad
 \Theta=\frac{101}{100}(a+\delta+\eta).                               \tag{4}
\]

**Adaptive receiver theorem.** If

\[
 F^2>\beta,\qquad \eta\le77/1000,\qquad
 R\|u\|\Theta+2R\|u-B\|<\phi-1,                                   \tag{5}
\]

then no receiver frame with normal `n` admits (1), for any source frame,
roll, translation or `lambda>=1`. The same holds for normals obtained by
the verified signed chamber reduction. The conditions involve only the
receiver. The inequalities are sufficient conditions; their failure does
not establish a passage or negate another possible obstruction.

## 2. The complete persistent contact pool

The exact checker generates all 1,770 unordered vertex pairs and checks
their squared distances. The 120 nearest-neighbor pairs have squared
distance four, and every vertex has degree four. For each pair `(p,q)` it
tests both orientations `e=+(q-p)` and `e=-(q-p)`. It retains the orientation
precisely when

\[
       (e\times u)\cdot(p-v)\ge0
                   \quad(v\in V,\quad u\in\{A,B,D\}).                \tag{6}
\]

All 43,200 candidate corner gaps are compared exactly. There are eighteen
retained oriented edges, with thirty-six distinct endpoint probes `(v_j,e_j)`.
Both endpoints satisfy (6), since `e cross u` is perpendicular to `e`.
Linearity in `u` extends all these supports to the entire **closed** cell
`ABD`, including ties. The checker separately validates all 6,480 selected
endpoint/corner/vertex inequalities. No unique-support assumption is made.

Define their torque vectors

\[
              m_j(u)=e_j\times u,\qquad
              T_j(u)=v_j\times m_j(u).                              \tag{7}
\]

At `B` the thirty-six probes give eighteen distinct torque points. The
previous four-contact tetrahedron is a subset. Its strictly positive
cofactor stress, exact balance, and full rank put the origin in the
three-dimensional interior of the new hull. Every one of the 816 triples
of distinct torque points is affinely independent; all 14,688 triple/point
support comparisons are tested. Keeping the supporting planes and
normalizing them as `q dot x<=1` gives exactly fifteen distinct facets.
This is complete: every facet of a three-dimensional finite polytope
contains an affinely independent triple from its defining point set.

All these normalized facets satisfy

\[
                   \frac1{\|q\|^2}\ge2-\phi.
\]

The facet `q=(phi,0,0)` has four contacts and attains equality. Therefore
the sharp centered ball radius of the **complete torque hull at B** is

\[
        r_0=\sqrt{2-\phi}=\phi-1=1/\phi.                            \tag{8}
\]

This describes the hull of the eighteen torque points; it does not assert
that all eighteen are extreme vertices. For every probe, `||e_j||=2`, so

\[
       \|T_j(u)-T_j(B)\|\le2R\|u-B\|.                              \tag{9}
\]

For each unit direction the support value of the actual torque hull is
at least `r_0-2R||u-B||`. If this is positive, the hull contains that
centered ball. This follows from convex support functions and does not
assume that the center facets or extreme points persist away from `B`.

## 3. A stronger roll branch, without an initial small-roll hypothesis

Let `S` be the threefold shadow in orthonormal planar coordinates. The
replayed [linear roll certificate](linear_roll_certificate.py) constructs
its cyclic dodecagon, checks every original vertex on every edge, and
retains all long-edge ties. It verifies its complete planar rotation group
`C6`, realized by the axial body group `C3` and central symmetry. For both
rotation signs it provides a long-edge endpoint with unit support
`h=phi^3=1+2phi` and signed derivative of magnitude `kappa=sqrt(5/3)`.

Suppose, for a planar rotation `U`,

\[
                      US\subset S+\eta\mathbb D,
                            \qquad 0\le\eta\le77/1000.              \tag{10}
\]

Reduce `U` modulo `C6` to an angle `alpha in [-pi/6,pi/6]`; put
`t=|alpha|`, `r=2sin(t/2)`. A long-edge endpoint chosen with the proper
derivative sign has outward support displacement

\[
 g(t)=\kappa\sin t-h(1-\cos t)
       =r\left\{\kappa\sqrt{1-r^2/4}-hr/2\right\}\le\eta.           \tag{11}
\]

On `[0,pi/6]`, `g''(t)=-kappa sin t-h cos t<0`. Let
`t_0=2arcsin(1/20)`, so its chord is `1/10`. Exact rational inequalities

\[
 \kappa>12909/10000,\qquad h<42361/10000,\qquad
 \sqrt3>433/250
\]

give

\[
 g(\pi/6)>
 \frac{12909}{20000}-\frac{42361}{10000}\left(1-\frac{433}{500}\right)
                       >77/1000.                                  \tag{12}
\]

At `t_0`, `sqrt(1-r^2/4)>99/100`, and hence

\[
 g(t_0)>
 \frac{12909}{10000}\frac1{10}\frac{99}{100}
       -\frac{42361}{10000}\frac1{200}>77/1000.                     \tag{13}
\]

Concavity bounds `g` from below by its endpoint chord on the entire
interval `[t_0,pi/6]`. Thus (10)-(13) force `r<1/10`, with both endpoints
excluded. On this remaining interval the bracket in (11) is strictly
greater than

\[
            (5/4)(99/100)-(17/4)(1/20)=41/40>1.                     \tag{14}
\]

For `r>0` this proves `r<eta`; for `r=0` the weak bound is immediate.
Consequently (10) gives

\[
                  \min_{U_0\in C_6}\|U-U_0\|_{op}\le\eta.          \tag{15}
\]

No initial small-roll condition, sampled rotation interval, or nearest
circle-point assignment is used. Concavity rejects the entire remote
part of the reduced roll interval before applying (14).

## 4. Elimination of all source parameters

Assume (1) with receiver normal `n` satisfying (5). Centering and diameter
containment give `f(n_1)>=F` by (2). Since `F^2>beta`, the source belongs
to an optimal sign region. In (3), positivity forces `n_1 dot n_*>0`.
With `s=||P_n* n_1||` and `e=c_0-F`,

\[
                         2s\le e.                                  \tag{16}
\]

The exact comparisons `beta>4/25` and `c_0<3/5` imply
`0<=e<1/5`, so `s<1/10` and `n_1 dot n_*>99/100`. Therefore

\[
 \|n_1-n_*\|^2=\frac{2s^2}{1+n_1\cdot n_*}
        <\frac{200}{199}s^2<\left(\frac{101}{100}s\right)^2
\]

when `s>0`; at `s=0` the chord is zero. In all cases

\[
                         \|n_1-n_*\|\le a.                         \tag{17}
\]

An independent proper source body symmetry aligns `n_*` with `n_0` and
preserves the source shadow, even for the antipodal optimizer. Minimal
proper transports `A_1,A_2` from `n_0` to the resulting source normal and
receiver normal have operator chords at most `a` and `delta`.
With `B_0=B_2A_2` there is a planar `U in SO(2)` such that

\[
                    B_2=B_0A_2^t,\qquad B_1=UB_0A_1^t.
\]

All source vertices have norm `R`. For each `v in K`, centered containment
and the two transport errors place `UB_0v` within `R(a+delta)=eta` of
`B_0K`. This yields (10), because `B_0K` is isometric to `S`.

Choose `U_0 in C6` by (15), and realize it by an axial body symmetry `h`
and a source planar half-turn `sigma in {+1,-1}` so that
`sigma U_0 B_0 h=B_0`. The half-turn leaves the source set unchanged by
central symmetry and leaves its cross-product normal unchanged. With
`W=UU_0^{-1}`, the gauged source frame becomes

\[
        B_1'=\sigma B_1h=W B_0(A_1')^t,\qquad A_1'=h^tA_1h.
\]

Completing the frames by their cross-product normals gives a proper
relative matrix `Q`, with `B_1'=B_2Q`, of the form

\[
          Q=A_2S_0^t\operatorname{diag}(W,1)S_0(A_1')^t.            \tag{18}
\]

Its factor chords are bounded by `delta, eta, a`. Because `R>4` and
`eta<=77/1000`, their maximum is below `1/10`. For a chord `x<=1/10`,
the corresponding rotation angle is at most `(101/100)x`: differentiate
`2arcsin(x/2)` and use `(101/100)^2(1-1/400)>1`.
The sum of these three angle bounds is `Theta<1`.
The rotation-angle triangle inequality proves

\[
                           \theta(Q)\le\Theta.                     \tag{19}
\]

For completeness, multiply unit quaternions of factor angles `b,c`,
with `b+c<pi`. Their scalar part is at least
`cos(b/2)cos(c/2)-sin(b/2)sin(c/2)=cos((b+c)/2)>0`, so their product
angle is at most `b+c`. Apply this twice in (18).
Thus (19) controls the **full** relative rotation, including roll.

For a nonzero relative rotation, let `z` be its unit axis and `theta` its
angle. By (8)-(9), some actual receiver torque obeys
`z dot T_j(u)>=phi-1-2R||u-B||`. The exponential remainder
`||Q-I-theta[z]_cross||<=theta^2/2` then gives

\[
 \begin{split}
 m_j(u)\cdot(Qv_j-v_j)
 &\ge\theta\left\{\phi-1-2R\|u-B\|
              -R\|u\|\theta\right\}>0.                            \tag{20}
 \end{split}
\]

Here `||m_j||<=2||u||`, and strict positivity follows from (5) and (19).
But (6) makes `m_j` an actual outer support normal perpendicular to the
receiver normal; centered closed containment requires the displacement in
(20) to be nonpositive. This contradiction excludes every `theta>0`.
At `theta=0` the gauged shadows coincide and cannot fit strictly.
This proves the adaptive receiver theorem, with all source parameters
and the closed-cell boundaries included.

## 5. Whole receiver polygons from their corners

Let `u_1,...,u_m` be nonzero chart points in the closed `ABD` cell with the
same strict axial sign pattern as `B`. For `n_j=u_j/||u_j||`, define

\[
 F_* =\min_j f(n_j),\quad \delta_* =\max_j\|n_j-n_0\|,\quad
 L_* =\max_j\|u_j\|,\quad H_* =\max_j\|u_j-B\|.
\]

Set `a_*=(101/200)(c_0-F_*)`, `eta_*=R(a_*+delta_*)`, and
`Theta_*=(101/100)(a_*+delta_*+eta_*)`. If

\[
 F_*^2>\beta,\quad \eta_*\le77/1000,\quad
               RL_*\Theta_*+2RH_*<\phi-1,                          \tag{21}
\]

then **every** ray through `conv{u_1,...,u_m}` excludes all sources.
This is a continuum certificate for a two-parameter receiver polygon.

To prove coverage, let `u=sum_j t_j u_j`, `t_j>=0`, `sum_j t_j=1`.
The norm triangle inequality gives `||u||<=L_*` and `||u-B||<=H_*`.
For each vertex `v`, let `sigma_v` be its common axial sign at the corners.
Then

\[
 \sigma_v v\cdot u\ge F_*\sum_jt_j\|u_j\|\ge F_*\|u\|.
\]

Hence `f(u/||u||)>=F_*`. Merely taking an absolute-value minimum at
corners without the common-sign hypothesis would not justify this step.
Similarly set `c=1-delta_*^2/2>0`; positivity follows from (21), since
`delta_*<=eta_*/R<1/10`. At every corner
`n_0 dot u_j>=c||u_j||`; convex combination and the norm inequality give
`n_0 dot u>=c||u||`. Thus `||u/||u||-n_0||<=delta_*`.
All quantities in (4)-(5) have the required bounds throughout the polygon,
so (21) proves the claim, including edges and corners.

An explicit nondegenerate example is the chart triangle with corners

\[
             B,\qquad L=(0,\phi^{-2}-1/163,1),\qquad
             C=(39/40)B+(1/40)D.                                   \tag{22}
\]

The checker computes exact barycentric coordinates in `ABD`, checks all
sixty axial signs at each corner, and certifies (21). Its rational
enclosures give a torque margin greater than `1/10`. The second corner
has normal chord distance greater than `1/190` from `n_0`, so this triangle
extends beyond the cap in the next section. The complete triangle, rather
than only its vertices, is excluded by the preceding convexity argument.

## 6. A closed cap of radius 1/200

Suppose the receiver normal has distance at most `d=1/200` from `T`.
The `R`-Lipschitz property of `f` gives
`F>=c_0-Rd>1/2`, since `c_0>4/7` and `R<9/2`. Therefore
`F^2>1/4>beta`. Equations (16)-(17) give

\[
 a\le(101/200)Rd<(23/10)d,\qquad
 \eta<(9/2)(23/10+1)d=(297/20)d=297/4000<77/1000.
\]

The full frame estimate gives

\[
 \Theta<(101/100)(23/10+1+297/20)d<(37/2)d=37/400.                    \tag{23}
\]

Reduce the receiver normal to the closed symmetry chamber by a proper body
symmetry and, when needed, a common planar reflection of both frames.
Proper symmetries conjugate `Q`. A common reflection preserves `Q` and
containment: the proper frame completions are multiplied on the left by
the same `diag(O,det O)`. Thus its full angle is preserved.
The inherited exact chamber enumeration shows that every other signed
orbit center violates a unit inward wall by more than `1/100`. Since
`d<1/100`, the reduced cap is centered at `B/||B||`.

The inherited inequalities `||B||<5/4` and `n_z>79/100` imply
`||u-B||<3d` for `u=n/n_z`. The other four chamber cells have
`y<=D_y`, whereas `B_y-D_y=(7-4phi)/5>1/10`. As `3d<1/10`, the reduced
receiver belongs to the closed `ABD` cell. These statements also apply
at the original cap boundary.

The new exact bound `||B||<27/25` gives `||u||<27/25+3d<10/9`.
Thus `2R||u||<10`, while `phi-1>3/5`. Combining (9), (20) and (23),
the torque remainder has strict margin greater than

\[
 \frac35-27d-5(37/2)d
                 =\frac35-\frac{239}{2}d=\frac1{400}>0.             \tag{24}
\]

This proves the closed radius-1/200 cap theorem for all source frames,
rolls, translations and `lambda>=1`. Its radius is thirty-five times the
preceding radius `1/7000`. The adaptive polygon theorem is a further
reduction rather than a claim that these caps cover the remaining sphere.

## 7. Exact reproduction, trust and remaining frontier

From repository root, Python 3.11+ standard library:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/adaptive_receiver_certificate.py --self-test
```

Every output field must match
[adaptive_receiver_expected.json](adaptive_receiver_expected.json).
The checker first replays and compares every field of
[linear_roll_expected.json](linear_roll_expected.json), including the
entire earlier diameter/sign-region/cell proof computation. It then
regenerates the complete persistent contact pool and complete center torque
facets, checks the ten roll-branch inequalities and all cap constants, and
verifies exact root enclosures and the example triangle's corner hypotheses.

Every radical is enclosed on a fixed rational grid of denominator `10^12`.
Binary integer search finds `l,h` with `0<=l<=h` and
`l^2<=q<=h^2` by exact `Q(phi)` comparisons. This directly proves
`l<=sqrt(q)<=h`; no floating-point tolerance enters. For a normal chord,
the stable identity

\[
 s^2=\frac{\|u\|^2\|B\|^2-(u\cdot B)^2}{\|u\|^2\|B\|^2},\quad
 \delta^2=\frac{2s^2}{1+\sqrt{1-s^2}}
\]

is used on the explicitly verified positive-dot branch. All endpoint
substitutions are monotone. The finite scalar comparisons use the resulting
rational upper and lower bounds, rather than rounded displayed decimals.

Ten new malformed controls reject a missing probe, reversed probe,
missing or reversed facet, unsupported roll threshold, unsupported cap
constant, negative radical argument, false radical enclosure, incomplete
receiver triangle, and a triangle failing the sufficient bound. Twelve
inherited malformed controls are replayed. Rejection of a stronger constant
or a different triangle means that this particular certificate fails;
it is not a proof of mathematical failure for that domain.

The trust boundary is the inspected exact integer/Fraction and `Q(phi)`
kernel, the standard vertex model, exhaustive finite generators, exact
radical sign comparisons, and the displayed convexity, coercivity, roll
concavity, frame-gauge, quaternion and exponential-remainder arguments.
The continuous analytic reasoning is not formalized in a proof assistant.
No solver, sampled-angle cover, floating search or external corpus is a
proof input.

Primary context: the projection equivalence and diameter obstruction in
[Steininger--Yurkevich](https://arxiv.org/html/2112.13754), the unresolved
[RID discussion](https://arxiv.org/html/2508.18475#S9.SS1), and the
[retained conjecture in Zeng](https://arxiv.org/html/2604.26531).
Bounded current primary-literature and graph checks do not support a
historical priority assertion.

Complementary published work read in this pass includes
[six-rupert-2's five-axis J77 limiting reduction](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_critical_axes/PROOF.md),
source `00ba486565df55ee9373f6e5da4668aefb7b71c8`, graph
`bafkreihlmsmzuw4pyogtn6sigsrdx2ugyvk5bsqmsyxjbgybyj4hnl7cea`, and
[six-rupert-1's proper closed deltoidal contact family](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/contact_family_proof.md),
source `c50ea79908001ec3653259ab0e72619b1495095d`, graph
`bafkreigjpweaoaxvwxvovhxejcija7pvmj6b5tmo7qemlybewwkm5h2obm`.
The major-claim refresh additionally supplied and prompted a full reading of
[six-rupert-1's mirror-branch exclusion](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/mirror_branch_proof.md),
source `4b853c13767c3b638c6fa9f81a00bf1c8e8fc791`, graph
`bafkreiab36zckg7tqwnv4f54has6hlbyyrcxqu2oybdnpvdxhm7engt35q`.
Its exact fixed-vertex endpoint identities force an axial drift rate and
close the deltoidal mirror-normal branch, leaving fifteen twofold axes.
They keep limiting, closed and strict quantifiers separate. They concern
different solids; no conclusion is transferred to RID through duality.

The precise next frontier is to extend (21), or a stronger receiver
criterion, over a specified larger part of the complementary normal domain.
Using the complete contact pool at actual receiver normals may improve the
ball bound (9), and other axial regions require a different coercivity or
structural argument. The receiver criterion reduces a certified patch from
five passage parameters to two receiver parameters, but leaves the global
non-Rupert conjecture unresolved.
