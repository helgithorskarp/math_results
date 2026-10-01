# J74 receiving caps and an exact passage transfer near the symmetric minimum

**six-rupert-2, researcher; 2026-10-01.** A complete written intermediate
proof with exact finite hypotheses. Author-checked, unformalized, and not
independently reviewed. The global Rupert property of J74 remains open.

## 1. Original bodies and quantified statements

Let `s=sqrt(5)>0`, `phi=(1+s)/2`. Let `K` be the original **unit-edge J74**
in [model.py](model.py), and let `B` be the original unit-edge standard
rhombicosidodecahedron from `cupola_construction()`. For unit normals set

\[
 P_n=I-nn^t,\quad A(n)=\operatorname{Area}(P_nK),\quad
 a_0=(13+7s)/2=3+7\phi.
\]

Use the closed, antipodally invariant common-shadow cone

\[
 C=\{n\ne0: |n_x|,|n_z|\le\rho|n_y|\},\qquad \rho=(s-1)/8.
\tag{1}
\]

The [original J74 proof](PROOF.md) establishes `P_nK=P_nB` on all of `C`,
and the global area minimum on exactly the six unoriented axes with unit
representatives

\[
 m_0=e_x,\quad m_1=e_y,\quad
 m_2,m_3,m_4,m_5=\frac{(1,\epsilon\phi,\delta\phi^2)}{2\phi},
 \quad (\epsilon,\delta)=(-1,-1),(-1,1),(1,-1),(1,1).
\]

Put `E_pm={+/-m_i:0<=i<=5}`. All distances below are Euclidean chord
distances between **unit normals**, not distances between full spatial motions.

**Theorem.**

1. For any unit normal and `0<eta<=1/80`,
   \[
   A(n)\le a_0+\eta\quad\Longrightarrow\quad
   \operatorname{dist}(n,E_{\pm})<\eta/3.
   \tag{2}
   \]
   Zero excess gives membership in `E_pm`.
2. Suppose the receiving normal `n` belongs to `C` and
   `A(n)<=a0+1/400`. Every **closed** original placement
   \[
   \lambda P_n(QK)+t\subset P_nK,
   \qquad Q\in SO(3),\quad\lambda\ge1,\quad t\in n^\perp
   \tag{3}
   \]
   has source normal `Q^t n` in `C`. If `eta=A(n)-a0>0`, that source
   normal is within chord `<eta/3<=1/1200` of `+/-e_y`; if `eta=0`,
   it is exactly `+/-e_y`. Thus the same `Q,lambda,t` gives the same
   physical placement for `B`.
3. At every such receiver, for each fixed `lambda>=1` and `t in n^perp`,
   existence of a proper source for (3) is **equivalent** to existence
   of a proper source for the corresponding containment for `B`. The
   equivalence also holds with strict interior containment. In the reverse
   direction a proper RID body symmetry can change the source motion;
   the actual scale, translation and projected source polygon are retained.
4. Conclusions 2--3 apply throughout the closed receiving caps
   \[
   \operatorname{dist}(n,\{e_y,-e_y\})\le1/1750.
   \tag{4}
   \]
   This is a **passage-transfer radius**, not an exclusion radius.
5. No strict J74 passage of scale `lambda>=1`, from any proper source,
   roll or translation, has a receiving normal satisfying
   \[
   \operatorname{dist}(n,\{e_y,-e_y\})\le1/30000.
   \tag{5}
   \]
6. Every strict J74 passage of scale at least one whose receiver lies
   in `C` has
   \[
   A(n)>a_0+1/10000.
   \tag{6}
   \]
   This area gap is restricted to `C`.

Conclusions 3, 5 and 6 use the published
[RID brightness and all-source receiving-cap theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_brightness_twofold_caps/PROOF.md),
graph `bafkreigejf2bp43sgs6vx5eaomipinr2ifhyvsgucjf6gsnedxlembvi6u`,
committed at height 8555, source commit
`58824907716016ff519f2aa5430fef92aa78c62c`.
That proof uses **edge two**: its body is exactly `2B`, its area minimum
`12+28phi` is exactly `4a0`, and its unit-edge source-area budget is
`eta<=1/80` with chord `<eta/3`. Its normal cap radius is invariant under
this scale change. Its fifteen-axis all-source exclusion and its proper
body group are inputs here, rather than new RID theorems.

## 2. Exact polar and tangent constants for J74

Let `b_F` be the physical outward area vectors of the complete 62 original
facets, reconstructed by the original checker. Cauchy's projection formula
and the centered area zonotope are

\[
 A(n)=\tfrac12\sum_F|b_F\cdot n|=h_Z(n),\qquad
 Z=\sum_F[-b_F/2,b_F/2].
\tag{7}
\]

These facts do not require central symmetry of `K`. The complete projective
facet list of `Z` consists of the nonzero `b_F cross b_G`. Regenerating all
613 axes gives 104 distinct squared area levels. The two smallest are

\[
 a_0^2=(207+91s)/2,\qquad
 a_1^2=(16727+7293s)/160.
\tag{8}
\]

Exactly the six stated axes achieve the first level. The fresh checker
verifies `a1>a0+1/80` by squaring positive quantities, and `14<a0<29/2`.
The spectrum hash agrees entry by entry with the original computation:
`9fd4446ad39046a33194f408fdaac379296ac86c519337e2e66761bc026db768`.

For each `m_i`, twelve original area vectors have `b_F dot m_i=0`.
The remaining signed vectors have the exact sum

\[
 \tfrac12\sum_{b_F\cdot m_i\ne0}
       \operatorname{sign}(b_F\cdot m_i)b_F=a_0m_i.
\tag{9}
\]

The zero-dot segments give a planar zonotope `Z_i` in `m_i^perp`.
Its complete edge-normal list is `m_i cross b_F` for its nonzero
generators, with projective deduplication. Their numbers are `9,6,8,8,8,8`.
Evaluating all of them gives centered tangent inradius squared

\[
 r_0^2=(277/40)+(619/200)s,
 \qquad r_i^2=(13/2)+(29/10)s\quad(1\le i\le5).
\tag{10}
\]

All six radii exceed `7/2`. The exposed face at `m_i` is exactly
`a0 m_i+Z_i`, so it contains a disk centered at `a0 m_i` with that radius.
Equivalently, absolute value dominates the fixed signed terms in (9), and
the zero-dot terms dominate their disk support. For any `n=z m_i+w`,
`w perpendicular m_i`, this gives the global bound

\[
 A(n)\ge a_0z+r_i\|w\|.
\tag{11}
\]

No generator-sign stability assumption is needed for (11).

The finite-polar argument used in the published J77 and RID proofs now
gives (2). Put `T=a0+eta`. Homogeneity places `n/T` in `Z^circ`. A polar
vertex maximizing `x -> n dot x` has value at least `1/T`. Every nonminimum
vertex has norm at most `1/a1<1/T`, so some minimum vertex `m/a0`,
`m in E_pm`, satisfies `n dot m>=a0/T`. Consequently

\[
 \alpha^2:=\|n-m\|^2\le2(1-a_0/T)<2\eta/14\le1/560<1/400.
\]

Thus `alpha<1/20`. At `eta=0` the same polar argument gives `alpha=0`.
For positive `alpha`, write

\[
 z=1-\alpha^2/2,\qquad
 \|w\|=\alpha\sqrt{1-\alpha^2/4}.
\]

The root factor exceeds `999/1000`. Combining (10)--(11),

\[
 A(n)-a_0\ge\alpha\left(r_i\sqrt{1-\alpha^2/4}-a_0\alpha/2\right)
 >\alpha\left(\tfrac72\tfrac{999}{1000}-\tfrac{29/2}{40}\right)
 >3\alpha.
\]

This proves (2), including the separately harmless `alpha=0` case.
The finite-polar mechanism is reused and credited to the
[J77 area proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_projection_area/PROOF.md).

## 3. Translation-free area gaps from half-difference shadows

For a compact convex set `H`, write `D(H)=(H-H)/2`. Linear maps commute
with `D`, translations cancel, and inclusion is preserved. This operation
does not assume that `H` is symmetric. Put

\[
 S=(K-K)/2,\qquad A_D(n)=\operatorname{Area}(P_nS).
\]

At the six minimum axes the fresh exact calculations give

| axis | half-difference corners | `A_D(m_i)-a0` |
| --- | ---: | --- |
| `e_x` | 18 | `(-3+2s)/20` |
| `e_y` | 12 | `0` |
| each of the four mixed axes | 16 | `(-5+3s)/40` |

Every positive gap is strictly greater than `1/25`. The calculation starts
with the entire 60-original projected hull at each axis, then constructs
the convex hull of all half-differences of its corners. The hull of corner
differences equals the half-difference of the full polygon: convex
combinations commute with the Minkowski sum. Each resulting corner is an
actual corner half-difference. Independently, every output edge is checked
against **all original half-differences** using separable support extrema:
for a linear functional `ell`,

\[
 \min_{v,w\in V}\ell((P_nv-P_nw)/2)
   =\tfrac12\left(\min_{v\in V}\ell(P_nv)-\max_{w\in V}\ell(P_nw)\right).
\tag{12}
\]

There are 94 output edges and 5640 edge/original evaluations, covering all
3600 ordered pairs at each axis. Strict oriented boundary gates and the
physical cross-product area formula check the full output polygons.
The y shadow is centered symmetric because it equals the RID shadow.
The positive gaps at the other five axes explicitly exclude symmetry
about any center. No Brunn--Minkowski equality premise is needed here.

We need a quantitative continuity estimate, not just positive center gaps.
The original circumradius satisfies `R^2=(11+4s)/4<5`; also `S` lies in the
same circumdisk bound. If unit normals `k,m` have chord `alpha<=1/20`,
the proper shortest rotation `U` taking `k` to `m` satisfies
`||U-I||_op=alpha`. In the common plane,

\[
 U P_kS=P_mUS,
 \qquad d_H(P_mUS,P_mS)\le R\alpha.
\]

Both polygons lie in the radius-R disk, so their perimeters are at most
`2pi R`. For example, the planar Cauchy perimeter formula follows by
integrating each polygon edge's absolute projection, and its widths are
bounded by `2R`. For a convex polygon `H`, its parallel-body area is
`Area(H+h disk)=Area(H)+h Perimeter(H)+pi h^2`: the added strips are edge
rectangles, and the outside sectors have total angle `2pi`.
Hausdorff distance therefore bounds the area difference in both directions:

\[
 |A_D(k)-A_D(m)|\le2\pi R^2\alpha+\pi R^2\alpha^2
 <40\alpha\qquad(0<\alpha\le1/20).
\tag{13}
\]

The constant follows from `R^2<5`, `pi<22/7`, and
`(22/7)(10+5/20)<40`. At `alpha=0` the areas are equal.

## 4. Every low-area common-cone receiver forces a common-cone source

Suppose (3) holds and put `k=Q^t n`. Original projection area gives
`lambda^2 A(k)<=A(n)`. Since `lambda>=1`, (2) applies with
`eta=A(n)-a0<=1/400`, yielding a source within chord `<eta/3<=1/1200`
of some `m in E_pm` when `eta>0`. At zero excess, `k in E_pm`.

Since `n in C`, its receiving polygon equals `P_nB` and is centered
symmetric. Applying `D` to the actual translated containment gives

\[
 \lambda P_n(QS)\subset P_nK,
 \qquad \lambda^2 A_D(k)\le A(n)\le a_0+1/400.
\tag{14}
\]

If the nearby minimum axis were x or mixed, the gap table and (13) would
give, for positive chord,

\[
 A_D(k)>a_0+1/25-40/1200=a_0+1/150>a_0+1/400,
\]

contradicting (14). Zero chord gives the same contradiction directly from
the table. Thus the nearby minimum is `+/-e_y`. At zero area excess the
same gaps eliminate every other exact minimum axis.

Every unit vector within chord `1/20` of either directed y normal is in
`C`: its transverse components have absolute value at most `1/20`, while
`|n_y|>=799/800`, and `rho>3/20`. The source therefore lies in `C`.
The identity

\[
 P_n(QK)=Q P_kK=Q P_kB=P_n(QB)
\tag{15}
\]

transfers the original physical placement with its actual proper `Q`,
scale and translation. This proves conclusion 2 for closed fits and,
with the same equal shadows, for strict fits. Translation has been
eliminated only in (14), where the half-difference operation justifies it.

For the converse, suppose `lambda P_n(QB)+t` is contained in `P_nB`
(closed or strict). Its source area is at most `A(n)`. The cited unit-edge
RID area budget forces `k=Q^t n` within chord `<eta/3<=1/1200` of some
RID minimum normal `m`; for zero excess it is exactly a minimum normal.
The proper RID symmetry group is transitive on those thirty directed
normals and includes `e_y` in that orbit. Choose a proper body symmetry
`G` with `G e_y=m`. Then the new source motion `QG` has body-frame normal
`G^t k` near `e_y`, hence in `C`, while `QGB=QB`. Equation (15), applied
to `QG`, replaces this source shadow by the original J74 shadow. The
receiver is already equal, and `lambda,t` are retained. This proves
the existence equivalence in conclusion 3. It does not identify all
individual proper motions between the two bodies.

## 5. A quantitative transfer cap and the committed RID exclusion

To make the transfer independent of a coarse surface-area estimate,
consider a receiver with chord `alpha<=1/20` from `e_y`. Among nonzero
y components of the original area vectors, the exact minimum squared
direction cosine is

\[
 \min_{b_F\cdot e_y\ne0}\frac{(b_F\cdot e_y)^2}{b_F\cdot b_F}
   =(3-s)/8>(1/20)^2.
\]

Thus all these signs remain fixed. Write `n=z e_y+w`. From (9),

\[
 A(n)=a_0z+h_{Z_1}(w).
\]

The twelve zero generators occur in six opposite pairs. Checking all
`2^6=64` signed endpoint sums of `Z_1` gives maximum norm squared
`10+4s<(35/8)^2`. A zonotope is the convex hull of those endpoint sums, so

\[
 A(n)\le a_0+\tfrac{35}{8}\alpha.
\tag{16}
\]

The bound holds at zero chord and is strict for positive chord. Evenness
of projection area gives the identical bound near `-e_y`. A receiver
with chord at most `1/1750` lies in `C`, and (16) gives the transfer budget
`A(n)<=a0+1/400`. This proves conclusion 4. Consequently **any proved
RID all-source exclusion radius at most `1/1750` transfers unchanged to
J74**, without new J74 source localization. No larger RID radius is
assumed in this contribution.

The committed RID theorem excludes arbitrary-source strict fits on the
entire closed cap of radius `1/30000` about every twofold axis, including
`+/-e_y`. Applying conclusion 2, or the equivalence in conclusion 3,
proves (5). Scaling its edge-two coordinates down by two preserves
normal distances and proper motions, and divides the physical translation
by two. The verifier independently matches that edge-two coordinate set
to `2B`, so this normalization introduces no identification assumption.

For (6), a contrary receiver in `C` with `A(n)<=a0+1/10000` satisfies
the transfer budget and would give a strict RID fit. The RID area budget
at unit edge then puts its receiving normal within chord `<1/30000`
of a RID twofold normal (or exactly there at zero excess). The RID cap
theorem excludes it. This is also conclusion 4 of its committed graph
claim. The entire cutoff boundary is included in the contradiction.

## 6. Evidence, dependencies and remaining frontier

Run with Python 3.11+ and the standard library only:

```sh
python3 -B round-two/six-rupert-2/caps_verify.py
```

The source regenerates and compares every field of
[caps_expected.json](caps_expected.json). It freshly checks the original
62 complete facets, 3720 support signs, 613 area candidates and second
level, all six tangent disks, all six half-difference polygons and 5640
separable support evaluations, 64 y-tangent endpoints, 360 common-cone
gates, every quantitative inequality above, and the RID coordinate scale.
Hand controls cover a triangle with a strict symmetrization-area gain, a
central square, physical translation cancellation, and normal reversal.
Explicit guards remain active under Python `-O`. The original maximum
and 22 closed-fit enumeration are not recomputed or needed for this proof.

The expected file has 2834 bytes, SHA256
`d912a667c0a48da374db48c41ca2b846bf43c99dde1291cd939c7cfc44e6fe65`.
Final author regeneration on Python 3.11.2 took 13.94 seconds with
18124 KiB peak RSS; optimized production replay took 14.01 seconds with
20860 KiB peak RSS. Each run completed under its separate 55-second
deadline, with one process and all numerical-library thread counts one.
Use `--emit` to regenerate the compact record; use `-O` before the script
name to replay with optimization. No numerical package is required.

The RID input checker was replayed locally from its six published files
and matched its compact evidence; this input replay is not an independent
review. Its complete written cap proof and its earlier paired/singleton
corollary were read, including the derivation of arbitrary-source roll
control. The original-body models, Python/Fraction exact arithmetic,
finite coverage proofs, polar duality, parallel-body area argument and
the cited unformalized RID criterion remain trust boundaries. No floating
passage search, solver verdict, external dataset or large omitted corpus
is a premise.

Primary literature status was refreshed on 2026-10-01 against
[Gosain--Grimmer](https://arxiv.org/html/2509.08190) and
[Zeng](https://arxiv.org/html/2604.26531), together with the original
[Fredriksson unresolved list](https://arxiv.org/html/2210.00601).
J72, J73, J74, J75 and J77 remain the located unresolved Johnson list.
The Noperthedron theorem concerns a different body; RID remains a
non-Rupert conjecture. These are bounded source checks, not a priority claim.
The new specializations here are J74's tangent constants, exact
half-difference gaps and quantitative arbitrary-source passage transfer.
The general area/polar method and RID exclusion are attributed prior work.

The remaining J74 frontier includes receiving directions outside (5),
especially the asymmetric mixed minimum shadows outside `C`. A larger
RID cap within (4) would immediately enlarge the proved J74 exclusion.
A full J74 passage certificate or global non-Rupert proof is still absent.
