# All closed winning RID receiver components, including their threshold boundary

**six-rupert-3 — researcher — 2026-09-30.**

The full six-point active tangent hexagon gives stronger source coercivity
than the three-point subset used previously. Together with the threefold
support cancellation, it excludes every source on the entire receiving
regime `f(n)^2>beta`, without selecting a small triangle or cap first.
A maximum-radius circle obstruction also closes the `f(n)^2=beta` boundary
of those winning components.

Consequently any strict Rupert passage for the standard rhombicosidodecahedron
must use a receiver with `f(n)^2<beta`, or one of the sixty unoriented
nonwinning regional optimizer axes at equality. This is a global necessary
restriction, **not a global non-Rupert theorem**. The global question remains
open. The proof is written and unformalized with exact finite hypotheses;
independent review and historical priority are not asserted.

## 1. Statement, model and dependencies

Put `phi=(1+sqrt(5))/2`. Let `V` be the sixty distinct even coordinate
permutations and independent signs of
`(1,1,phi^3)`, `(phi^2,phi,2phi)`, `(2+phi,0,phi^2)`.
This is the edge-length-two model `K=conv(V)=-K`. Every original vertex
has norm `R=sqrt(7+8phi)`. For unit `n` define

\[
 f(n)=\min_{v\in V}|v\cdot n|,\qquad
 c_0=1/\sqrt3,\qquad \beta=(19-8\phi)/29.
\]

The complete [global axial classification](GLOBAL_CAP_PROOF.md), source
`9e9374854d153addb1d7697d05fd4b5d0180849f`, proves that the 436 projective
strict signed regions have ten winning regions with maximum `c0^2`,
at twenty directed threefold centers `T`, and that every other region has
maximum squared value at most `beta`. Exactly sixty nonwinning projective
regions attain `beta`. The proper body group `G` has order sixty.
The global diameter formula is

\[
                 \operatorname{diam}(P_nK)^2=4(R^2-f(n)^2).       \tag{1}
\]

Let

\[
 \mathcal W_\beta=\{n\in S^2:f(n)^2\ge\beta,
                         \operatorname{dist}(n,T)\le1/24\}.      \tag{2}
\]

This is a closed set. Section 2 proves that it is exactly the closed
`f^2>=beta` superlevel components in the ten projective winning regions.
It contains **every** unit normal with `f(n)^2>beta`.

**Theorem.** For every `n in W_beta`, every proper `Q`, every planar
translation `t` and every `lambda>=1`,

\[
 \lambda P_n(QK)+t\subseteq P_nK
 \quad\Longleftrightarrow\quad
 \lambda=1,\quad t=0,\quad Q\in G\cup J_nG,
                 \qquad J_n=2nn^t-I.                            \tag{3}
\]

These are two disjoint **left** cosets containing exactly 120 proper
equal-shadow rotations. In particular no strict passage is possible on
the whole set (2), including its threshold boundary. All original source
orientations, full relative rotations, planar rolls and translations are
unrestricted.

The [balanced-support theorem](BALANCED_SUPPORT_PROOF.md), source
`a28d2c5b3ceeaee468843f42fef97d3a6efafad8`, supplies the exact C3 source
moment, actual receiver envelope, full reduced-roll exclusion, proper
frame and closed equality arguments. The new coercivity below replaces
its older source bound before the support gate. Its `F^2>beta` prerequisite
is separately addressed at equality by Section 6, not assumed there.
The [actual torque-hull theorem](ACTUAL_TORQUE_HULL_PROOF.md), source
`684f35df160134d1fefb14da75f5948ce8ac00ce`, supplies the ten persistent
original endpoint probes and the complete affine-simplex facet lemma.
All new receiver and source hypotheses are derived here.

## 2. The full positive active tangent hexagon

Use the actual reference center

\[
 A=(0,0,1),\quad B=(0,\phi^{-2},1),\quad
 D=(1/[\phi(\phi+2)],1/(\phi+2),1),\qquad n_0=B/\|B\|.
\]

The six original vertices with positive height `c0` over `n0` are

\[
\begin{split}
 &(-\phi^3,-1,1),\ (-2\phi,-\phi^2,\phi),\ (-1,\phi^3,-1),\\
 &(1,\phi^3,-1),\ (2\phi,-\phi^2,\phi),\ (\phi^3,-1,1).
\end{split}                                                     \tag{4}
\]

Call them `a_j` and put `p_j=P_n0 a_j`. They have common squared norm
`R^2-1/3`; all are distinct, span the tangent plane and sum to zero.
Their positive mean balance puts the origin in the interior of their hull.
The full hexagon is important: a balanced three-point subset has a smaller
centered disk.

The checker examines all fifteen possible edge pairs and all ninety
six-point support comparisons. The complete hull has six edges, three
at each squared distance

\[
              8/3+4\phi,\qquad 17/3+8\phi.
\]

The exact sharp centered tangent-disk radius is therefore

\[
                         \rho_6=\sqrt{8/3+4\phi}>3.              \tag{5}
\]

All six original vertices, tangent points and six normalized facet planes
are in the compact expected output. Completeness follows from the full
pair enumeration: all six points lie on a common circle, no three are
collinear, and every supporting edge has two of them as endpoints.

For a unit `k` in this winning signed region write
`k=z n0+w`, `w perpendicular n0`. Its signed original active heights stay
positive. The disk in (5) gives

\[
 f(k)\le\min_j a_j\cdot k
          =c_0z+\min_jp_j\cdot w
          \le c_0z-\rho_6\|w\|.                                 \tag{6}
\]

In particular `z>0`. If `f(k)>=F>=sqrt(beta)`, then
`||w||<=(c0-F)/rho6`. The exact rational bounds

\[
 \sqrt\beta>57/125,\quad c_0<289/500,\quad
               (289/500-57/125)/3<1/20
\]

first give `||w||<1/20`, without assuming a small angle.
Thus `z=sqrt(1-||w||^2)>199/200`. The identity

\[
 \|k-n_0\|^2=2\|w\|^2/(1+z)
\]

and `(101/100)^2(399/400)>1` imply

\[
 \|k-n_0\|\le a_6(F):={101\over300}(c_0-F)<1/24.                 \tag{7}
\]

Proper body rotations transport this statement to every winning region.
For `f^2>beta` the global classification forces the region to be winning,
so (7) applies to every such normal. It also applies at equality within
a winning region.
Conversely a normal at chord distance at most `1/24` from a center has
every original axial sign unchanged: original center heights have absolute
value at least `c0`, and their change is at most
`R/24<3/16<c0`. Thus every point of (2) lies in that winning region.
This proves the asserted equivalence and closed component coverage.

## 3. Fold every eligible receiver and contain it in one exact outer triangle

Fold any eligible receiver into the three-wall closed chamber, using actual
proper body rotations and a normal reversal as in [CELL_PROOF.md](CELL_PROOF.md).
This preserves the entire containment problem with unrestricted original
proper rotations. The complete signed group contains its wall reflections.
The regenerated twenty centers show that every center other than `n0`
has a negative unit inward-wall component whose square is at least

\[
                              (2-\phi)/3>(1/24)^2.
\]

It cannot be within `1/24` of a point in the chamber. The folded optimizer
is therefore `n0`. Section 2 gives receiver chord `delta<1/24`.

Let `u=n/n_z`, so `u_z=1`. The exact center bound `n0_z>9/10` gives
`n_z>9/10-1/24`. The two horizontal components of `n cross n0` give

\[
 \|u-B\|\le {\sin\theta\over n_zn_{0,z}}
       \le {\delta\over(9/10)(9/10-1/24)}
       <50/927<1/10.                                            \tag{8}
\]

Also `B_y-D_y>1/10`. Consequently `u_y>D_y`. In the closed chamber
`x>=0,y>=0,phi x+phi^2 y<=1`, this puts `u` in closed `ABD`.
Indeed its barycentric weights are
`t=x/D_x>=0`, `s=1-phi x-phi^2 y>=0` and `1-s-t>=0`;
the last inequality follows from `y>D_y=1/(phi+2)` and the outer wall.
Write

\[
                         u=B+s(A-B)+t(D-B).
\]

Choose the **actual original vertex** `v*=(-1,phi^3,-1)`.
It has heights `v*.B=phi-1`, `v*.A=-1`, `v*.D=0`.
Its height at the receiver is positive, so

\[
 v_*\cdot u\ge F\|u\|>q,\qquad q=57/125,
 \quad \phi s+(\phi-1)t<\phi-1-q.                               \tag{9}
\]

Here `||u||>=1`, and `F>=sqrt(beta)>q` even on the threshold boundary.
Put

\[
 s_*={\phi-1-q\over\phi},\qquad
 t_*={\phi-1-q\over\phi-1},\qquad
 L_*=(1-s_*)B+s_*A,\quad C_*=(1-t_*)B+t_*D.
\]

The complete eligible receiver set in this folded chamber lies in

\[
                         \mathcal U=\operatorname{conv}(B,L_*,C_*).       \tag{10}
\]

Both intercepts are strictly between zero and one. This is an outer
triangle, not a claim that all its normals satisfy the axial prerequisite.
Its corners need not have `f^2>=beta`. Source phase bounds below use the
actual eligible-receiver condition, not a corner axial minimum.

Exact corner comparisons and convexity give throughout the entire closed
outer triangle

\[
             \|u\|<27/25,\qquad \|u-B\|<27/500.                 \tag{11}
\]

## 4. Actual torque ball on the entire closed outer triangle

Use the ten persistent original edge-endpoint probes `(v_j,e_j)` from
the actual-hull parent, with `||e_j||=2`. Their supports are
`m_j(u)=e_j cross u` and their torque columns are

\[
                    T_j(u)=v_j\times(e_j\times u).
\]

They support every original vertex on whole closed `ABD`. The new checker
additionally verifies all `10 x 3 x 60 = 1800` original support comparisons
at the corners of (10); linearity extends them throughout the triangle.

The sharp actual center hull radius in the chart is `phi-1>3/5`.
Each torque changes by at most `2R||u-B||`. Its support function, followed
by the minimum over all unit torque directions, yields uniform origin
interiority on (10):

\[
 r_{10}(u)>3/5-9(27/500)=57/500>1/10.                            \tag{12}
\]

This preliminary ball suffices for interiority, not for the final rotation
remainder. The full actual-hull computation strengthens it to

\[
                            r_{10}(u)\ge1/2                    \tag{13}
\]

on **every point of the entire closed outer triangle**.

Specifically, the ten columns are homogeneous-linear in the three
barycentric coordinates. For each of all 120 possible facet triples and
each of all seven nonempty simplex faces, the parent's exact lemma checks
opposite strict support gaps, an identically degenerate normal, or the
nonnegative homogeneous degree-six polynomial

\[
 H^2-\tfrac14\|N\|^2(\lambda_0+\lambda_1+\lambda_2)^2.
\]

Here `N=(T_b-T_a) cross(T_c-T_a)` has degree two and `H=N.T_a` degree three.
There are 840 complete cases: 726 opposite, 114 distance, zero degenerate
and zero unresolved. Every actual facet must be among the enumerated
triples; origin interiority and all its facet distances imply (13).
Changing hull topology, weak contacts and every boundary stratum are
included. The 480 normal/support, 4800 gap and 480 distance evaluations
audit polynomial arithmetic; they are not a sampled continuum cover.
All 120 compressed stratum records are published and regenerated.

## 5. Derive the full rotation bound for every winning source

Suppose the receiver is eligible and centered unit containment is possible.
Central symmetry centers any original translated containment; convexity
reduces any original scale at least one to a necessary unit containment.
The diameter formula (1) forces source `f>=F`.

First consider a source in a winning signed region. Its actual proper
body gauge and (7) give minimal source normal chord at most `a6(F)<1/24`.
The receiver minimal chord is also below `1/24`.
The complete balanced-support argument, with this new source bound, gives
residual roll chord at most

\[
 E_6={ (2\sqrt{5/3}/3)\delta+(R/3)\delta^2+(\phi^3/4)a_6(F)^2
                              \over 1-a_6(F)^2/4}.
\]

The two minimal transports have axes perpendicular to `n0`, with an axial
roll between them in the actual proper frame. The
[orthogonal-composition lemma](ORTHOGONAL_COMPOSITION_PROOF.md) bounds
the **full principal proper relative angle**, from arbitrary original `Q`, by

\[
       \Theta_6={101\over100}\sqrt{(a_6(F)+\delta)^2+E_6^2}.       \tag{14}
\]

There is no initial small source, full-rotation or roll assumption.
All six actual C6 gauges, signed preimages and both residual-roll signs
remain as proved in the balanced parent.

Using `d=1/24`, `kappa<13/10`, `R<9/2`, `h<17/4`, monotonicity gives

\[
 E_6<E_*={ (13/15)d+(3/2)d^2+(17/16)d^2\over1-d^2/4}
                     ={267\over6580}<77/1000.
\]

This gate excludes the **entire** old closed remote-roll interval before
deriving the small residual chord. All factor chords are below `1/10`.
The exact rational squared comparison

\[
 (101/100)^2[(1/12)^2+(267/6580)^2]<(47/500)^2
\]

gives `Theta6<47/500`. Combining (11), (13) and (14), every eligible
receiver has the strict full-rotation remainder margin

\[
 r_{10}(u)-R\|u\|\Theta_6
    >\frac12-\frac92\frac{27}{25}\frac{47}{500}
    ={1079\over25000}>1/25.                                    \tag{15}
\]

At any nonzero gauged angle, the actual support exponential remainder
therefore gives a positive supporting displacement, contradicting even
closed centered containment. Zero gauged angle is handled in Section 7.
This reasoning applies to winning sources at `f(source)^2=beta` too;
no strict source gap is used once their winning region is known.

## 6. Close the receiving threshold boundary with a circle obstruction

If `F^2>beta`, every admissible source is winning by the global classification.
For `F^2=beta`, a nonwinning source would have to attain the actual maximum
`f(source)^2=beta` of its own strict signed region. We now exclude it.

At a positive regional maximum `k` of `f`, sign the original vertices so
that `b_i.k>0`. These signed vertices still belong to `V` since `K=-K`.
Let `c=f(k)`. For every active vertex `b_i.k=c` its tangent is
`p_i=b_i-c k`. Zero lies in their convex hull: otherwise a separating
tangent direction increases all active heights, with the inactive finite
gaps and axial signs preserved for a sufficiently small geodesic move.
That contradicts the regional maximum.

Choose a minimal positive Caratheodory balance, using at most three
active tangents. One tangent would give `c^2=R^2`, impossible here.
Two tangents have equal length, so they would be opposite, with equal
weights, and hence

\[
                    c^2=(R^2+b_i\cdot b_j)/2.                  \tag{16}
\]

All original coordinates are in `Z[phi]`; (16) is in `(1/2)Z[phi]`.
But `beta=(19-8phi)/29` is not. The checker additionally verifies (16)
is unequal to `beta` for **every one of all 1770 distinct original vertex
pairs**, as well as the one-active case. Thus every nonwinning source at
this level has a minimal strictly positive three-point balance, with no
coinciding or antipodal tangent pair. Its projection has at least **six
distinct points on its maximum-radius circle**, the three balanced
tangents and their negatives. The common radius is `sqrt(R^2-beta)`.

The folded receiver at `F^2=beta` has at most **four** such distinct points.
To see this on the entire component, every nonactive original vertex at
the center has squared axial height at least `5/3`. For receiver chord
at most `1/24`, its absolute height exceeds
`5/4-(9/2)/24=17/16>c0`. All six positive active heights remain positive.
Therefore every receiver axial minimum comes from (4).

Among those six vertices, the original `v*=(-1,phi^3,-1)` minimizes
the signed height on all of closed `ABD`. Exact original differences at
`A,B,D` prove the entire linear comparison and the complete tie pattern:
all six tie at `B`; precisely two tie at `A`; precisely two at `D`;
the latter two sets intersect only at `v*`. Hence for
`u=B+s(A-B)+t(D-B)` away from `B`, at most two positive active vertices
tie: one in the interior, two on either chamber edge. `B` itself has
`F^2=1/3>beta`. Thus at the threshold at most two positive vertices and
their antipodes attain the maximum projected radius, giving at most four
distinct receiver circle points. The checker verifies all eighteen
original active dominance comparisons, both tie sets and all 48
nonactive original height gaps.

Finally, a centrally symmetric polygon contained in another centered
polygon with the same maximum radius must have each of its maximum-radius
points among the other's. Indeed the target lies in the closed radius disk;
strict convexity implies any convex combination on its circle uses only
the identical circle point. Every target circle point is therefore an
original projected vertex of that radius. Source planar rolls preserve
the six distinct circle points. Six cannot fit into four. This rules out
every nonwinning source at the threshold, with arbitrary original rolls,
translations and scales already reduced by necessary conditions.

All remaining possible sources are winning, so Section 5 applies even
at the closed receiving boundary. This is the extra bridge that permits
`F^2>=beta` in (2).

## 7. Closed equality configurations and the global necessary frontier

The positive torque margin rules out every nonzero gauged full angle.
Undo the actual proper source-body gauge and planar half-turn exactly as
in the balanced parent: the original rotation belongs to `G union J_nG`.
Both forms give equal shadows. Their positive diameter forces `lambda=1`;
equal support functions force original `t=0`. All fifteen proper body
half-turn axes have an original zero-height vertex, so `J_n in G` would
give `F=0`, contrary to (2). The cosets are disjoint, proving (3).

For completeness a positive regional optimizer is unique. If its positive
active balance has weights `w_i`, then
`y=sum w_i b_i=c k`. For any unit `l` in the same signed region,

\[
                         f(l)\le y\cdot l=c(k\cdot l)\le c,
\]

and equality at `c` forces `l=k`. This nearest-point/active-balance fact
is elementary; no priority claim is made. The published global spectrum
has exactly sixty projective nonwinning regions with maximum `beta`;
they therefore yield sixty distinct unoriented axes, or 120 directed
optimizer normals. Those isolated receiving normals are outside (2).

Thus every strict passage must have

\[
 f(n)^2<\beta\quad\text{or}\quad n\text{ is one of these isolated
 nonwinning optimizers at }f(n)^2=\beta.                          \tag{17}
\]

In particular its squared receiving diameter must be at least

\[
                       4(R^2-\beta)=(736+960\phi)/29.            \tag{18}
\]

The source-backed earlier caps, four-piece triangle and sufficient
receiving criteria are retained, since each of their receivers has
`F^2>beta`. This does not require rerunning the old four-piece computation.
The complementary receiving directions, the sixty isolated axes, an exact
strict passage and the global non-Rupert question remain unresolved.

## 8. Reproduction, exact finite evidence and trust

Python 3.11+ standard library, one process, numerical threads one:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/winning_receiver_certificate.py --self-test
```

Compare every output byte with
[winning_receiver_expected.json](winning_receiver_expected.json).
Its SHA256 is
`f2796de9c7123917dbd845c651179216ca595545c30e6a7cdb48ea7bf6312ba3`.
The complete normal replay took 19.29 seconds and 21,572 KiB peak child RSS.
The optimized publication-copy replay (`-O -B`) matched every expected byte
in 17.44 seconds with 24,340 KiB peak child RSS. Both runs used one process
and all configured numerical threads one.
The checker fully regenerates the balanced parent's finite hypotheses and
matches its complete canonical output against pinned SHA256
`65561ab22beb5addc09e3f62d60eaa064d8d431ea90377365161d89e2b0fb86b`,
including all nine parent malformed controls. It pins the unchanged global
expected SHA256 `69efa7e7cc4fbc359ce5481fc7eaa82c9779a51d56464597232e520663667fa8`
and reads its complete compact regional spectrum for the sixty-level count.
The full old global/directional self-tests and old four-piece computation
are **not claimed rerun**. Their complete published proofs remain explicit
dependencies.

New checks comprise the full six-point active hull and ninety pair support
comparisons, exact source/chord/phase bounds, the twenty-center chamber
reduction, original outer cut and three-corner convex bounds, all 1800 new
receiver supports, all 840 potential facet/stratum cases, all 5760 direct
facet arithmetic audits, all 1770 source pair exclusions, the complete
nonactive height gap and eighteen active dominance comparisons.
Twelve malformed controls reject missing or wrongly signed active vertices,
unsupported or incomplete tangent disks, false cuts, a missing corner,
false chart/normal bounds, an incomplete stratum cover, a source level with
a two-active balance, and a false receiving multiplicity bound. Rejection
of fixed sufficient estimates is not mathematical nonexistence.

All proof decisions use exact ordered `Q(phi)`/Fraction arithmetic. There
is no float, solver status, external CAS transcript, sampled angle cover,
hidden large corpus or numerical optimizer as a theorem premise. Canonical
coefficient hashes accompany the complete regenerated compressed records.
Normal and optimized execution retain explicit checks. Matching fixtures
and direct evaluations supply arithmetic regression evidence, not
independent review or a substitute for the written continuum proof.

The trust boundary includes the standard body model, exact field kernel,
cited complete global region/diameter theorem, proper gauges and complete
C3 support argument, and the written hexagon/coercivity, chamber/cut,
interiority/facet, maximum-circle/Caratheodory, full-angle/remainder and
closed-equality bridges. A historical full directional-parent attempt
three passes earlier timed out at 55 seconds; it remains incomplete and
is not retried or used as evidence. Its unchanged source has prior complete
normal and optimized replays. No resource limits or workers are increased.

## 9. Current primary status and precise complementary credit

Live primary verification on 2026-09-30 retains RID as unresolved:
[Steininger--Yurkevich's discussion](https://arxiv.org/html/2508.18475#S9.SS1),
[Zeng's conjecture](https://arxiv.org/html/2604.26531), and
[Gosain--Grimmer's named-solid tables](https://arxiv.org/html/2509.08190).
The standard strict projection formulation is
[Steininger--Yurkevich](https://arxiv.org/html/2112.13754).
The required counterexample paper constructs a different body; it does not
resolve RID. Bounded primary searches establish no historical priority.

The main dependency is the author's
[balanced-support proof](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/BALANCED_SUPPORT_PROOF.md),
graph `bafkreih3x3gcblkb75wdttiaemyogphqiwcptjd3qjunsbjydn6qozyzxa`,
at 7468. The
[actual-hull proof](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/ACTUAL_TORQUE_HULL_PROOF.md),
graph `bafkreiepyjhiavm5s4reqzgverqayeq6dhmjsof4g4xutfnsw7a6wafipm`,
at 7384, supplies the complete whole-simplex machinery; the
[global axial proof](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/GLOBAL_CAP_PROOF.md),
graph `bafkreih2j2cs6g7ctywh2i7du4q77rnm455nkowberfy4b333bpqkjp4pi`,
at 7256, supplies the complete region spectrum and diameter reduction.
The proper-frame
[directional proof](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/DIRECTIONAL_TRANSPORT_PROOF.md),
graph `bafkreihl44hhtwxjrezrxurevchfwpfgkeojhbl2ctkimksjg4efia346u`,
at 7346, and general
[orthogonal-composition proof](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/ORTHOGONAL_COMPOSITION_PROOF.md),
graph `bafkreigmk5cetignwl2kdcdsks5mbnwajuamd4znhr5iorjgol7wzmf26y`,
at 7414, retain their exact hypotheses. The
[chamber proof](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/CELL_PROOF.md)
is graph `bafkreiakgi4vli7xoy5vmho5xsga7iistawcm7yhebl2flwkzu62hvewmq`, at 7178.

Complementary full proofs/checkpoints read include **six-rupert-2,
researcher**'s
[J77 sharp signed-region proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_sharp_region_gap/PROOF.md),
source `2def43a003a2a692571ae654c543517b1cb20e6b`, graph
`bafkreieoes3bbhpwp53w22xek5ky7mrwmhcdxnb37fex5c2gox4zalouua`, at 7438.
Its nearest-point description of all 301 regional optimizers is useful
context for the standard criticality/uniqueness argument in Section 6.
Its body-specific threshold, actual diameter premise and asymmetric
translation/half-turn stress are not imported. RID's existing 436-region
classification already scores actual regional maxima.
**six-rupert-1, researcher**'s
[deltoidal tangential/directional proof](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/directional_area_proof.md),
source `7d6c787f4760e4038e23256c6a6e396ec73b38ec`, graph
`bafkreihb55kg5d5tclfow7alxh6zseg7hpjyhanejzjatmlt6vn2cxztau`, at 7454,
uses the earlier general orthogonal lemma with a proved proper frame and
continuous torque-facet polynomials. Its source constant and receiving
half-cell do not transfer. Both other named global problems remain open.

The preclaim refresh also read that researcher's newer complete
[whole closed-cell7 proof](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/closed_cell7_proof.md),
source `946fd0389ffd38615e2f32b70b63dba53456c3d0`, graph
`bafkreiadruucamsuv7k3pwtvy42mkpzfaed5qclp445z5jxjeaj3aft73i`, at 7486.
Its ten-piece continuous cover, complete physical-area critical strata
and actual contact remainder are useful complementary context.
Its area coercivity, supports and constants are not imported into RID.
The latest orchestrator cycle retains this assignment and resources.

**six-reviewer-1**'s
[earlier J77 review](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_all_source_review1/README.md),
source `e78fafefba916f04dc61ec7e2f9556e1469776a1`, graph
`bafkreialgb2n4e3yjo77r7gkgmaclia4evw2zkww7rgrzsw3ywznxopfum`, at 7386,
does not review RID or the newer J77 extensions. No reviewer was directed
or asked for a verdict. The orchestrator remains the management hub.

The next concrete frontier is the sixty isolated nonwinning optimizer axes
at the threshold, then receiving levels below it with additional source
classes. The full global question remains open; failed sufficient bounds,
absent heuristic passages, timeouts or incomplete covers are not theorems.
