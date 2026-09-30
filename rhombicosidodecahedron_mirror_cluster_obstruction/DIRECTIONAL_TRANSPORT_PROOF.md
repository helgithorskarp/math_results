# Axial-height transport and larger all-source RID receiver regions

**six-rupert-3 — researcher — 2026-09-30.**

This sharpens the [adaptive receiver criterion](ADAPTIVE_RECEIVER_PROOF.md)
by bounding normal-transport errors at actual supporting vertices. The
result excludes every source orientation whenever the receiver satisfies
a two-parameter criterion, and certifies whole receiver polygons from
their corners. It includes every receiver previously certified by the
adaptive criterion. Concrete consequences are the **closed chord caps
of radius 1/100** about all ten unoriented threefold axes, and a larger
closed receiver triangle containing the previous one, with **163/30 times
its unit-z chart area**. The global non-Rupert conjecture remains open.

All source normals, planar rolls and translations are unrestricted; scale
at least one is allowed. The argument is an unformalized analytic proof
with exactly checked finite and radical hypotheses. Independent review
or proof-assistant verification is not asserted.

## 1. Model, inherited facts and receiver criterion

Put `phi=(1+sqrt(5))/2`. Let `V` be all even coordinate permutations,
with independent signs, of

\[
 (\pm1,\pm1,\pm\phi^3),\qquad
 (\pm\phi^2,\pm\phi,\pm2\phi),\qquad
 (\pm(2+\phi),0,\pm\phi^2).
\]

Set `K=conv(V)`, `R=sqrt(7+8phi)`, `c0=1/sqrt(3)` and
`beta=(19-8phi)/29`. There are sixty vertices of norm `R`; `K=-K`.
An orthonormal-row projection frame `B_i` has cross-product normal `n_i`.
The standard strict passage condition is

\[
       \lambda B_1K+t\subset\operatorname{int}(B_2K),\qquad\lambda\ge1.
                                                                    \tag{1}
\]

For the convex projection equivalence see
[Steininger--Yurkevich](https://arxiv.org/html/2112.13754).
Central symmetry and convex averaging remove `t` while preserving strict
containment. Scaling down preserves it because `0` is an interior point.
Thus (1) implies centered, unit-scale closed containment. We use only
necessary conditions for that containment until excluding strict equality.

The complete [global diameter certificate](GLOBAL_CAP_PROOF.md), replayed
by the present checker through its dependencies, proves

\[
 f(n)=\min_{v\in V}|v\cdot n|,\quad
 \operatorname{diam}(BK)^2=4(R^2-f(n)^2),\quad
                  \max_{\|n\|=1}f(n)^2=1/3.                         \tag{2}
\]

Of all 436 antipodal axial sign regions, only ten attain the maximum;
every other region has maximum at most `beta`. The twenty directed
optimizers form a single orbit under the exactly verified sixty proper
body rotations. For an optimal region with optimizer `n_*`, its balanced
active tangent triangle has inradius greater than two, giving

\[
       f(n)\le c_0(n\cdot n_*)-2\|P_{n_*}n\|.                       \tag{3}
\]

The general equal-radius active-set reduction is credited to
[six-rupert-2's diameter proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_projection_diameter/PROOF.md).

Use the closed chamber cell and chart from [CELL_PROOF.md](CELL_PROOF.md):

\[
 A=(0,0,1),\quad B=(0,\phi^{-2},1),\quad
 D=\left(\frac1{\phi(\phi+2)},\frac1{\phi+2},1\right),\quad
                    u\in\operatorname{conv}\{A,B,D\}.
\]

Write `n0=B/||B||`, `n=u/||u||`, and define

\[
 \begin{split}
 F&=f(n),&\delta&=\|n-n_0\|,&a&=\frac{101}{200}(c_0-F),\\
 \kappa&=\sqrt{5/3},&
 E&=c_0a+\kappa\delta+\frac R2(a^2+\delta^2),&
 \Theta&=\frac{101}{100}(a+\delta+E).
 \end{split}                                                       \tag{4}
\]

**Directional receiver theorem.** If

\[
 F^2>\beta,\qquad E\le77/1000,\qquad
          R\|u\|\Theta+2R\|u-B\|<\phi-1,                           \tag{5}
\]

then no receiver frame with normal `n` admits (1), for any source frame.
The verified signed chamber symmetries transport this conclusion.
The bound `E` controls selected long-edge supports. It is not asserted
to bound the Hausdorff distance of complete shadows.

## 2. Minimal normal transport uses axial height

Let `A` be the minimal proper rotation taking a unit normal `n0` to
`n=cos(theta)n0+sin(theta)t`, with `t` unit and perpendicular to `n0`,
and `0<=theta<pi`. Put `b=n0 cross t` and
`v=zeta n0+chi t+omega b`. Its inverse acts by

\[
 P_{n_0}(A^t-I)v
      =\{(\cos\theta-1)\chi-\sin\theta\,\zeta\}t.
\]

For the normal chord `x=||n-n0||=2sin(theta/2)`, one has
`sin(theta)<=x` and `1-cos(theta)=x^2/2`. If `||v||<=R`, any
orthonormal-row frame `B0` with normal `n0` therefore satisfies

\[
       \|B_0(A^t-I)v\|\le |v\cdot n_0|x+\frac R2x^2.               \tag{6}
\]

At `theta=0` this holds directly. Unlike the coarser bound `Rx`, the
first-order coefficient is the vertex's actual axial height.

## 3. Finite long-edge gaps and source corner preimages

The [linear roll certificate](LINEAR_ROLL_PROOF.md) verifies the complete
center shadow `S=B0K`. It is a cyclic dodecagon with six long and six short
edges, twelve distinct original corner preimages, and full planar rotation
group `C6`. Every corner has squared radius `20/3+8phi`. The long edges
have unit support `h=phi^3=1+2phi` and tangential endpoint derivative
of magnitude `kappa`. Both signs are available. All sixty original
vertices, including hidden supporting ties, are checked on every edge.

The new checker regenerates that hull rather than importing an unverified
edge list. It initially works at the directed optimizer
`d=(0,1,-phi^2)`. An inherited verified proper body rotation transports
all the following facts to `n0`, and to every other directed optimizer.

For each long-edge unit normal `ell` and each original vertex `v`, set

\[
       G_v=h-\ell\cdot B_0v\ge0,\qquad H_v=|v\cdot n_0|.
\]

All 360 long-edge/original-vertex height and gap checks establish:

* Each long edge has four original ties. Their maximum squared axial
  height is exactly `5/3`.
* In each of the 216 pairs with `H_v>kappa`, the gap is positive and

\[
 \frac{G_v}{H_v-\kappa}\ge
   \frac{618033988749}{1154700538381}>\frac12.                       \tag{7}
\]

The displayed rational lower bound comes from exact outward radical
enclosures, not rounded decimal arithmetic. Hence, for `0<=delta<=1/2`,
every vertex satisfies `G_v>=(H_v-kappa)delta`; when `H_v<=kappa`,
the assertion follows already from `G_v>=0`. If `A2` is minimal normal
transport from `n0` to `n` and `B2=B0 A2^t`, equation (6) now gives

\[
          h_{B_2K}(\ell)\le h+\kappa\delta+\frac R2\delta^2.        \tag{8}
\]

This estimate applies to all original vertices, not just the center ties.
The positive gaps absorb the larger heights of vertices that could become
supporting under transport.

All twelve corner preimages have squared axial height **1/3**. The center
projection has sixty distinct projected vertices, so these preimages
are unique. Their permutations under `C6` are verified explicitly.
For clarity, the checker constructs the three proper axial body rotations
over `Q(phi)` by Rodrigues' formula. Since `||d||^2=3phi^2`, the two
nonidentity matrices are

\[
 g_\pm=-\frac12 I+\frac32\frac{dd^t}{\|d\|^2}
                   \ \pm\frac{\phi-1}{2}[d]_\times.                \tag{9}
\]

It checks orthogonality, determinant one, `g d=d`, order dividing three,
and all original vertex images. Multiplying their plane actions by a
source planar half-turn `sigma=+1` or `-1` gives exactly six distinct
rotations, the full `C6`. Every signed plane action is checked on all
sixty projected points and all twelve corner preimages. In three
dimensions `sigma=-1` may be improper; only `g` is used as a proper
body gauge. The extra sign is a planar half-turn allowed because `K=-K`.

## 4. From actual containment to the reduced roll

Assume (1). Centering and (2) imply `f(n1)>=F`. If `F^2>beta`, the
source belongs to an optimal sign region. Equation (3) and positivity
imply `n1 dot n_*>0`. Put `s=||P_n* n1||` and `e=c0-F`. Then
`2s<=e`. Since `beta>4/25` and `c0<3/5`, `e<1/5`, `s<1/10`, and
`n1 dot n_*>99/100`. The exact identity

\[
 \|n_1-n_*\|^2=\frac{2s^2}{1+n_1\cdot n_*}
        \le(101s/100)^2
\]

with the zero case included gives `||n1-n_*||<=a` as in the preceding
adaptive proof. A proper independent source body symmetry takes the
optimizer to `n0`, including when it was antipodal.

Choose minimal transports `A1,A2` from `n0` to the resulting source and
receiver normals, with chords at most `a,delta`. With `B0=B2 A2`, there
is a planar `U in SO(2)` such that

\[
                       B_1=UB_0A_1^t,\qquad B_2=B_0A_2^t.           \tag{10}
\]

Reduce `U` modulo `C6`: choose `U0` with `W=U U0^{-1}` having angle
`alpha in [-pi/6,pi/6]`. Choose a long-edge endpoint `p` and unit
normal `ell` with tangential derivative of the sign of `alpha`.
Let `v` be the original preimage of `U0^{-1}p`. Section 3 verifies that
it exists and has axial height `c0`. Equation (6) proves

\[
             \|B_1v-Wp\|\le c_0a+\frac R2a^2.                     \tag{11}
\]

If (5) holds, `kappa>1` and `E>=kappa delta` force `delta<77/1000<1/2`,
so (8) applies. Actual centered containment implies
`ell dot B1v<=h_B2K(ell)`. Combining it with (8) and (11), and putting
`t=|alpha|`, gives the necessary inequality

\[
             g(t)=\kappa\sin t-h(1-\cos t)\le E.                   \tag{12}
\]

This establishes the bridge for every original source orientation and
every roll. It uses one actual corner preimage and selected receiver
supports, without asserting `US subset S+E disk`.

The earlier [concavity argument](ADAPTIVE_RECEIVER_PROOF.md) depends
only on (12) and `E<=77/1000`, so it applies here. In detail,
`g''(t)=-kappa sin(t)-h cos(t)<0` on `[0,pi/6]`. For the angle `t0`
whose chord is `1/10`, exact inequalities
`kappa>12909/10000`, `h<42361/10000`, `sqrt(3)>433/250`
show `g(t0)>77/1000` and `g(pi/6)>77/1000`. Concavity excludes the
entire closed interval `[t0,pi/6]`. For `r=2sin(t/2)<1/10`,

\[
 \frac{g(t)}r=\kappa\sqrt{1-r^2/4}-hr/2
            >(5/4)(99/100)-(17/4)(1/20)=41/40>1
\]

when `r>0`. Thus the residual roll chord is at most `E`, with zero
included. The same ten exact roll comparisons are replayed explicitly.

## 5. Proper frame gauge and the torque contradiction

For the chosen `U0`, Section 3 gives a proper axial body rotation `g`
and `sigma in {+1,-1}` with `U0 B0=sigma B0 g`. Set `h=g^t`, so
`sigma U0 B0 h=B0`. Replace the source frame by `B1'=sigma B1 h`;
its source set is unchanged. Its normal is `h^t n1`, and the source
half-turn preserves the cross-product normal. With `A1'=h^t A1 h`,

\[
                B_1'=W B_0(A_1')^t.
\]

Complete `B0` to a proper three-dimensional row frame `S0`. The full
proper relative matrix `Q`, characterized by `B1'=B2 Q`, is

\[
           Q=A_2 S_0^t\operatorname{diag}(W,1)S_0(A_1')^t.          \tag{13}
\]

Its three factor chords are bounded by `delta,E,a`. For every receiver
in (5), `F>2/5` and `c0<7/12` imply
`a<(101/200)(7/12-2/5)=1111/12000<1/10`. Also `delta<E` unless zero,
and `E<=77/1000<1/10`. For any factor chord `x<=1/10`, its angle
is at most `(101/100)x`, by differentiating `2arcsin(x/2)` and checking
`(101/100)^2(1-1/400)>1`. Their angle sum is at most `Theta<1`.
The proper rotation-angle triangle inequality, or the unit-quaternion
argument in the adaptive proof, therefore gives `theta(Q)<=Theta`.

The complete thirty-six persistent endpoint probes `(vj,ej)` from the
adaptive proof are valid throughout closed `ABD`. Their support normals
`mj=ej cross u` are perpendicular to `u`; every `||ej||=2`.
At `B`, the full torque hull `conv{vj cross(ej cross B)}` contains the
sharp centered ball of radius `phi-1`. All 816 triples and fifteen facets
are replayed. Since every torque moves by at most `2R||u-B||`, support
functions show that the actual receiver torque hull contains a centered
ball of radius at least `phi-1-2R||u-B||` whenever this is positive.
This does not assume persistence of the center facet topology.

If `Q` has positive angle `theta` and unit axis `z`, one actual torque
has `z dot (vj cross mj)>=phi-1-2R||u-B||`. The exponential remainder
`||Q-I-theta[z]_cross||<=theta^2/2`, valid by integrating orthogonal
rotations twice, now gives

\[
 m_j\cdot(Qv_j-v_j)
 \ge\theta\{\phi-1-2R\|u-B\|-R\|u\|\theta\}>0.                   \tag{14}
\]

The last inequality is (5). Since `mj` is an actual receiver support
normal, closed containment requires the same displacement to be
nonpositive. This is a contradiction. If `Q=I`, the two gauged shadows
coincide and cannot fit strictly. The directional receiver theorem follows.

It contains the entire preceding adaptive criterion. Indeed, there
`eta=R(a+delta)<=77/1000`, and `R>4` implies `a,delta<1/50`.
Using `c0<3/5`, `kappa<13/10`, `R<9/2`, one obtains

\[
 c_0+(R/2)a<3/5+9/200<R,\qquad
 \kappa+(R/2)\delta<13/10+9/200<R.
\]

Multiplying by `a,delta` and adding gives `E<=eta`, including the zero
case. Consequently `Theta` is no larger than the preceding bound and
every receiver certified there satisfies (5).

## 6. Whole polygons and a larger exact triangle

Take chart corners `uj` in closed `ABD`, sharing all sixty strict axial
signs with `B`. Let

\[
 F_* =\min_j f(u_j/\|u_j\|),\quad
 \delta_* =\max_j\|u_j/\|u_j\|-n_0\|,\quad
 L_* =\max_j\|u_j\|,\quad H_* =\max_j\|u_j-B\|.
\]

Define `a*,E*,Theta*` by (4), using `F*,delta*`. If

\[
 F_*^2>\beta,\quad E_*\le77/1000,\quad
                  RL_*\Theta_*+2RH_*<\phi-1,                        \tag{15}
\]

then all rays through the **entire closed** convex polygon of these
corners exclude every source. For `u=sum tj uj`, the norm inequalities
give `||u||<=L*` and `||u-B||<=H*`. For each vertex's common sign
`sigma_v`, linearity gives
`sigma_v v dot u>=F* sum tj||uj||>=F*||u||`, so `f(u/||u||)>=F*`.
Similarly the positive coefficient `c=1-delta*^2/2` satisfies
`n0 dot uj>=c||uj||`; convex combination gives
`n0 dot u>=c||u||`, and hence the chord bound `delta*`.
The error polynomial is increasing in nonnegative `a,delta`, so all
three inequalities (5) hold throughout the polygon. This is a continuum
argument; testing just the corner values would not suffice without it.

Use the nondegenerate triangle

\[
 B,\qquad L_{60}=(0,\phi^{-2}-1/60,1),\qquad
                   C_{20}=(19/20)B+(1/20)D.                         \tag{16}
\]

The checker verifies its exact barycentric coordinates in `ABD`, all
sixty common axial signs and all radical inequalities in (15). The
enclosed strict torque margin exceeds **1/20**. The corner `L60` has
normal chord greater than **1/70**, so this triangle extends beyond the
new radius-1/100 cap.

Writing the previous corners as `L163,C40`, one has

\[
       L_{163}=B+\frac{60}{163}(L_{60}-B),\qquad
       C_{40}=B+\frac12(C_{20}-B).
\]

Both lie inside the new triangle, so the entire previous triangle is
contained. The cross-product area identity gives ratio `163/30` for
their areas in the unit-z affine chart. No spherical-area ratio is claimed.

## 7. All-source closed receiver caps of radius 1/100

Suppose a receiver normal is within chord distance `d=1/100` of one
of the twenty directed threefold optimizers. The `R`-Lipschitz property
of `f` gives `F>=c0-Rd>1/2`, so `F^2>1/4>beta`. Equations (3)-(4) give
`a<23d/10`. Substituting `c0<3/5`, `kappa<13/10` and `R<9/2`,

\[
 E<\frac{67}{25}d+\frac{5661}{400}d^2
     =\frac{112861}{4000000}<\frac{77}{1000},                        \tag{17}
\]

and therefore

\[
 \Theta<\frac{101}{100}\left(\frac{33}{10}d+
                      \frac{112861}{4000000}\right)
       =\frac{24730961}{400000000}<\frac{63}{10}d.                  \tag{18}
\]

Fold the receiver into the closed symmetry chamber using proper body
rotations and, when needed, a common planar reflection of both frames,
as in the adaptive proof. This preserves containment and full relative
angle. Every other signed orbit center violates a unit inward chamber
wall by **strictly more than** `1/100`. Thus even at `d=1/100`, the
folded cap must be centered at `n0=B/||B||`.

The strict inherited estimate `n0_z>4/5` gives `n_z>79/100` on this
closed cap. With `||B||<5/4`, the chart identity
`u-B=((n-n0)-B(n_z-n0_z))/n_z` gives `||u-B||<3d`.
Every other chamber cell has `y<=D_y`, and `B_y-D_y>1/10>3d`,
so the receiver lies in closed `ABD`.
These strict wall and z margins are retained at the cap boundary;
replacing them by weak bounds and then requiring `d<1/100` would lose it.

The bound `||B||<27/25` gives `||u||<27/25+3d<10/9`, hence
`R||u||<5`. Since `phi-1>3/5`, equations (17)-(18) imply

\[
 \phi-1-2R\|u-B\|-R\|u\|\Theta
          >\frac35-27d-5\left(\frac{63}{10}d\right)
          =\frac3{200}>0.                                        \tag{19}
\]

This verifies (5) on all closed receiver caps. Both directed centers of
each axis are included, as are all source orientations and every roll,
translation and scale `lambda>=1` from (1). The radius doubles the
preceding `1/200`; the general transport mechanism and polygon criterion
are the contribution beyond the numerical constant.

## 8. Exact checking, dependencies and open frontier

From repository root, Python 3.11+ standard library:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/directional_transport_certificate.py --self-test
```

Every output field must match
[directional_transport_expected.json](directional_transport_expected.json).
The entire preceding adaptive output is replayed and compared, including
its complete diameter/sign-region, chamber, edge, contact and torque-hull
dependencies. The new checker regenerates the complete center polygon;
checks all 360 long-edge height/gaps, 216 excess-height comparisons and
twelve unique corner preimages; verifies the three proper body matrices
and six signed planar actions; and checks all criterion, cap, radical,
triangle-containment and chart-area bounds.

Radicals are enclosed on a fixed rational grid of denominator `10^12`.
The inherited exact `Q(phi)` sign kernel checks `lo^2<=q<=hi^2` with
`0<=lo<=hi`. Thus the root enclosures are rigorous, including all monotone
substitutions in (7), (15) and (19). Eleven new malformed controls reject
missing vertices or edges, a reversed support normal, an unsupported
height-gap range, missing or incorrect corner preimages, missing or
improper gauge matrices, an unsupported cap constant, an incomplete
triangle, and a triangle failing this sufficient criterion. Twenty-two
inherited malformed controls are replayed. Certificate rejection does
not prove that the rejected parameter range is mathematically impossible.

The trust boundary comprises exact integer/Fraction and `Q(phi)`
arithmetic, the stated standard vertex model, exhaustive finite
generators, and the displayed transport, convexity, coercivity, roll
concavity, proper frame-gauge and exponential-remainder arguments.
The continuous proof is not formalized. No floating-point search,
sampled parameter cover, solver verdict or external proof corpus is an
input. The global remaining normal domain is not covered.

The direct proof dependencies are the preceding adaptive source
`53e57de0ba3c38d4ee789e7bbd5fbb031347a267`, graph
`bafkreicsflhs33t2yft342slfzk46vnr55unjj3uf6pnmsaxmtgum6rvz4`, the
linear-roll source `472864df5e2b773cad681b680e6901b01f4c8a6a`, graph
`bafkreih2r7gsrai6kr32c2vapf5v5debgmkr2ri3n2uysvdtmfgxp3mbtm`, the
global source `9e9374854d153addb1d7697d05fd4b5d0180849f`, graph
`bafkreih2j2cs6g7ctywh2i7du4q77rnm455nkowberfy4b333bpqkjp4pi`, and
cell source `fa77703cccae7cf90a5e5ca519bded273de776f3`, graph
`bafkreiakgi4vli7xoy5vmho5xsga7iistawcm7yhebl2flwkzu62hvewmq`.

Primary status was refreshed in this pass against
[Steininger--Yurkevich's RID discussion](https://arxiv.org/html/2508.18475#S9.SS1)
and [Zeng's retained RID conjecture](https://arxiv.org/html/2604.26531).
The global question remains unresolved; bounded literature searches do
not establish historical priority.

Complementary full published proofs and checkpoints read include
[six-rupert-1's uniform local deltoidal exclusion](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/twofold_area_proof.md),
source `58ec651cdd077243b556287369b6f56132735f6d`, graph
`bafkreifnp5u7bnnjoxqysdxep55lhl6ohvvro6jmagbdw4wacpdae2eryy`, and
[six-rupert-2's uniform local J77 exclusion](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_uniform_local_exclusion/PROOF.md),
source `d23b45ee6e2d2704087e42b6a4faef698c53b14d`, graph
`bafkreiar5zgul6vfndfhkjkvg5cpkuewkkipybatfsbeo6iqojlbeqtbci`.
Their global passage questions also remain open. They sharpen the shared
contact and limiting-branch methodology, but concern distinct bodies;
no conclusion is transferred to RID through duality or local similarity.

The next substantive frontier is an exact receiver cover extending (15)
toward the rest of `ABD`, preferably replacing the global perturbation
loss `2R||u-B||` by an actual-receiver torque-ball bound that tolerates
changes of facet topology. Other axial regions require a separate
coercivity or structural argument. Failure of (5) or (15) is no evidence
of a passage and no proof of non-Rupertness for the complementary region.
