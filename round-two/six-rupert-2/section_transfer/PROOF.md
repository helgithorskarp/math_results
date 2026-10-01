# Central sections of the J74 half-difference body and enlarged receiving exclusions

**six-rupert-2, researcher; 2026-10-01.** Complete author-checked written
intermediate proof with exact finite certificates. The continuous bridges
remain unformalized. No independent review of this extension or historical
priority is asserted. The global Rupert property of J74 remains open.

## 1. Bodies, units and conclusions

Let `s=sqrt(5)>0`, `phi=(1+s)/2`. Let `K` be the **original unit-edge
metabigyrate rhombicosidodecahedron J74** in [model.py](../model.py), and
let `B` be the unit-edge standard rhombicosidodecahedron in the same axes.
Set

\[
 S=(K-K)/2,\quad P_n=I-nn^t,\quad
 A(n)=\operatorname{Area}(P_nK),\quad
 A_D(n)=\operatorname{Area}(P_nS),\quad a_0=(13+7s)/2.
\]

All normals in area and distance formulas are unit. Distances are Euclidean
unit-normal chords. The [original geometry](../PROOF.md) gives `A(n)>=a0`,
with equality exactly on `E_pm={+/-m_i:0<=i<=5}`, where

\[
 m_0=e_x,\quad m_1=e_y,\quad
 (m_2,m_3,m_4,m_5)=
 \left(\frac{(1,\epsilon\phi,\delta\phi^2)}{2\phi}\right)_{
 (\epsilon,\delta)=(-1,-1),(-1,1),(1,-1),(1,1)}.
\]

The same source proves the physical shadow equality `P_nK=P_nB` on the
entire closed cone

\[
 C=\{n\ne0: |n_x|,|n_z|\le\rho|n_y|\},\qquad \rho=(s-1)/8.
 \tag{1}
\]

Put `a1=51/8+143s/40` and `ax=127/20+18s/5`.

**Theorem.**

1. For all six minimum axes, the complete half-difference shadow is an
   actual central section:
   \[
   P_{m_i}S=S\cap m_i^\perp.
   \tag{2}
   \]
   Their respective areas are `ax,a0,a1,a1,a1,a1`. Consequently, for every
   unit `k` and each directed choice of those axes,
   \[
   A_D(k)\ge A_D(m_i)|k\cdot m_i|.
   \tag{3}
   \]
2. For `0<eta<=1/25`, `A(n)<=a0+eta` implies
   `dist(n,E_pm)<eta/3`. The half-difference area has minimum exactly
   `a0`, attained **only** at `+/-e_y`. Moreover,
   \[
   A_D(n)\le a_0+\eta,quad 0<\eta\le1/25
   \quad\Longrightarrow\quad
   \operatorname{dist}(n,\{e_y,-e_y\})<\eta/3.
   \tag{4}
   \]
3. Suppose `n in C` and `A(n)<=a0+1/25`. Every original **closed** fit
   \[
   \lambda P_n(QK)+t\subset P_nK,
   \quad Q\in SO(3),\quad\lambda\ge1,\quad t\in n^\perp
   \tag{5}
   \]
   has source normal `k=Q^t n` in `C`. At positive receiving excess
   `eta=A(n)-a0`, this normal is within `<eta/3` of `+/-e_y`; at zero
   excess it equals one of those normals. The same `Q,lambda,t` gives
   the identical physical RID fit. For each fixed `lambda,t`, existence
   of a proper source for J74 and for RID is equivalent, for closed and
   strict fits. Reverse transfer may change `Q` by a proper RID body
   symmetry, while retaining the projected source polygon, scale and
   translation. These statements also apply whenever
   `A_D(n)<=a0+1/25`, without an initial hypothesis `n in C`.
4. The transfer band includes closed receiving-normal caps of radius
   **8/875** about `+/-e_y`. Every strict fit (5) is excluded on the
   closed caps of radius **1/270**, with arbitrary source, full roll,
   translation and scale at least one. Every strict J74 fit satisfies
   the **global** necessary inequality
   \[
   A_D(n)>a_0+1/90.
   \tag{6}
   \]
   For receivers in `C`, it also satisfies `A(n)>a0+1/90`. An original
   area gap outside `C` is not claimed.

The cap radius `8/875` is a transfer radius. Touching closed fits, including
self-fit at a minimum axis, are allowed. The smaller radius `1/270` excludes
**strict interior containment**, the standard projected passage criterion.

The proof uses the published [RID quadratic cap theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_quadratic_twofold_caps/PROOF.md)
of six-rupert-3, graph
`bafkreidiwye4mcfzaickzc4zmrbldyce44awk4f4ndnnlxpxgowilgvpsi`,
height 8613, source commit `dc752d2b996ffc77ff2a24e6c05c3bbaa426f6ad`.
It excludes arbitrary sources at receiver chord at most `1/270` about
every RID twofold axis and gives the unit-edge necessary receiving-area
gap `1/90`. Its body has **edge two**, equals exactly `2B`, and has area
minimum `4a0`; scaling down divides area by four and translation by two,
while preserving normal chords and proper motions. This identification
is rechecked by the pinned parent verifier. These RID results are inputs,
not new RID claims.

## 2. A finite construction of complete central sections

The compact [certificate](expected.json) lists each central-section corner
as original vertex-index pairs. A one-pair entry `(i,j)` denotes

\[
 p=(v_i-v_j)/2\in S.
\]

A two-pair entry `(i,j),(k,l)` denotes the convex midpoint

\[
 p=(v_i-v_j+v_k-v_l)/4\in S.
 \tag{7}
\]

The checker requires the two constituent half-differences to have exactly
opposite nonzero heights along the relevant `m`. In every entry it checks
`m dot p=0`. Thus all constructed points lie in the **actual central
section**, without projecting a nonplanar point and pretending it belongs
to `S`.

There are 94 section corners: 50 direct half-differences and 44 exact
midpoints. The x section has 18 corners, 6 direct and 12 midpoint lifts;
the y section has 12, all direct; each mixed section has 16, comprising
8 direct and 8 midpoint lifts. Let `H` be the convex hull of the listed
planar points in one record. Distinctness, nonzero consecutive edges and
strict inward signs at every other listed corner establish a complete
convex cyclic boundary. For an edge `p->q`, put

\[
 d=m\times(q-p)\in m^\perp.
\]

Instead of trusting a generated projected hull, the checker evaluates
`d dot v_i` at **all 60 original vertices**, and requires

\[
 \frac{\min_i d\cdot v_i-\max_j d\cdot v_j}{2}=d\cdot p.
 \tag{8}
\]

The left side is the minimum of `d dot x` on `S`. As `d` is planar,
it is also its minimum on `P_mS`. Hence every projected half-difference
lies on the inward side of every boundary edge of `H`. The intersection
of these halfplanes is `H`, so `P_mS subset H`. Conversely the actual
membership just established gives `H subset S intersect m-perp subset P_mS`.
This proves (2), including the entire projection, not a sample of its
extreme points.

Summing `cross(p,q)/2` around these polygons gives a vector exactly equal
to their physical area times the **unit** normal. This proves the area
table above. The checker also verifies central symmetry of each polygon.
Across the six sections, it uses 5640 original support evaluations and
1304 strict corner/edge gates. Four malformed certificate controls reject
a discarded half-lift, a reversed half-difference, an incorrect cyclic
order, and a cropped corner.

For the continuous bound (3), orthogonal projection of any planar set
from `m-perp` to `k-perp` multiplies area by `|k dot m|`: choose their
intersection direction as one orthonormal coordinate, with contraction
factor `|k dot m|` in the other. The perpendicular case has zero projected
area. Since the polygon (2) is contained in `S`, its image is contained
in `P_kS`. This proves (3) at **every** unit `k`, not only near `m`.
In particular, for chord `alpha=||k-m||` with `alpha<2`,

\[
 A_D(k)\ge A_D(m)(1-\alpha^2/2)
 \quad\text{when }k\cdot m\ge0.
 \tag{9}
\]

The loss near these axes is quadratic. This replaces the earlier
linear Hausdorff-area estimate and is the reason the transfer band grows.

## 3. A larger global original-area budget

The parent [receiving-cap proof](../RECEIVING_CAPS.md), with its freshly
replayed exact hypotheses, gives the complete area zonotope
`Z=sum_F[-b_F/2,b_F/2]`, where `b_F` are the physical area vectors of all
62 supporting original faces. Its support function is `A`. The complete
613 projective facet-normal spectrum has minimum `a0` at exactly the six
axes above and next squared level

\[
 a_1^2=(16727+7293s)/160.
 \tag{10}
\]

Equation (10) also equals the square of the mixed central-section area
constructed here; the exact equality is checked. Every maximum-norm
vertex of `Z`'s polar is `m/a0` for `m in E_pm`; every other vertex has
norm at most `1/a1`.

Suppose `A(n)<=T=a0+eta` with `0<eta<=1/25`. Homogeneity puts `n/T`
in `Z`'s polar. A polar vertex maximizing `n dot x` has value at least
`1/T`. The scalar checks show `a1>a0+1/25`, so this vertex must be
`m/a0` for some `m in E_pm`. Consequently,

\[
 n\cdot m\ge a_0/T,\qquad
 \alpha^2:=\|n-m\|^2\le\frac{2\eta}{a_0+\eta}
 <\frac{2\eta}{14}\le\frac1{175}<\left(\frac2{25}\right)^2.
 \tag{11}
\]

At each such axis, the generators orthogonal to `m` form a tangent
zonotope containing a centered disk of radius `r_m`, and the signed sum
of the remaining generators is exactly `a0 m`. The pinned parent checker
reconstructs these facts independently at every axis. Their squared
disk radii are

\[
 r_{m_0}^2=277/40+619s/200,
 \qquad r_{m_i}^2=13/2+29s/10\quad(1\le i\le5).
\]

All radii exceed `18/5`, and `14<a0<29/2`. Absolute values dominate the
fixed signed sum globally, so writing `n=z m+w` gives

\[
 A(n)\ge a_0z+r_m\|w\|.
 \tag{12}
\]

For unit normals, `z=1-alpha^2/2` and
`||w||=alpha sqrt(1-alpha^2/4)`. From (11), the square-root factor is
greater than `999/1000`. For positive `alpha`, (12) gives

\[
 A(n)-a_0>
 \alpha\left(\frac{18}{5}\frac{999}{1000}
                 -\frac{29/2}{25}\right)>3\alpha.
 \tag{13}
\]

This proves the original-area localization in conclusion 2. The
`alpha=0` case satisfies the strict `<eta/3` conclusion because `eta>0`.
At zero excess the prior exact equality classification applies. No
initial proximity or source-nearness assumption is used.

## 4. Global localization of the half-difference area

For a planar convex polygon `H`, the classical **Brunn-Minkowski**
inequality with bodies `H,-H` and weights `1/2,1/2` gives

\[
 \sqrt{\operatorname{Area}((H-H)/2)}
 \ge\tfrac12\sqrt{\operatorname{Area}(H)}
     +\tfrac12\sqrt{\operatorname{Area}(-H)}.
\]

Taking `H=P_nK` proves `A_D(n)>=A(n)` for every unit normal.
This standard input is [Gardner, equation (2) and Theorem 4.1](https://sites.stat.washington.edu/jaw/COURSES/520s/523/HO.523.20/Gardner.BullAMS.02.pdf),
*Bull. Amer. Math. Soc.* 39 (2002), 355-405,
DOI `10.1090/S0273-0979-02-00941-2`. No equality characterization of that
inequality is needed here, and no novelty is claimed for symmetrization.

If `A_D(n)=a0`, then `A(n)=a0`, so `n in E_pm`. The section table
eliminates x and the four mixed axes because `ax>=a1>a0`; the y area
is exactly `a0`. Thus `+/-e_y` are precisely the half-difference minima.

More generally, `A_D(n)<=a0+eta`, `0<eta<=1/25`, implies the original-area
budget and hence puts `n` within `<eta/3<=1/75` of some `m in E_pm`.
If `m` is any non-y axis, (9) and the exact scalar check give

\[
 A_D(n)\ge a_1(1-\alpha^2/2)
 \ge a_1(1-1/11250)>a_0+1/25,
 \tag{14}
\]

contradicting the assumed budget. This includes `alpha=0`. Therefore
the nearby directed axis is `+/-e_y`, proving (4).

Every unit normal within chord `1/20` of either y axis belongs to `C`:
each transverse component is at most `1/20`, `|n_y|>=799/800`, and
`rho>3/20`. Thus the whole global sublevel in (4) is in `C`.

## 5. Arbitrary-source transfer on the larger band

Apply the operation `D(H)=(H-H)/2` to the actual original containment (5).
Linear maps, positive scaling and this operation commute; translation
cancels. Thus for **every** receiving direction,

\[
 \lambda P_n(QS)\subset P_nS,\qquad
 \lambda^2 A_D(k)\le A_D(n),\quad k=Q^t n.
 \tag{15}
\]

If initially `n in C`, its receiving shadow equals `P_nB` and is
centered symmetric because `B=-B`. Consequently `P_nS=P_nK=P_nB`, and
`A_D(n)=A(n)`. For `A(n)<=a0+1/25`, (15) and (4) force every source
normal into the y cone with the stated `<eta/3` bound. At zero excess
the half-difference equality classification forces `k=+/-e_y` exactly.
If instead `A_D(n)<=a0+1/25` is given globally, (4) first places the
receiver in `C`, reducing to the same argument. No symmetry assumption
on `K` itself is made.

For such a source, proper motion and shadow equality give

\[
 P_n(QK)=Q P_kK=Q P_kB=P_n(QB).
 \tag{16}
\]

The receiving polygons also coincide. Thus the actual source placement,
translation and scale transfer, and strictness is preserved.

For reverse **existence** transfer across the whole new band, the RID
linear budget `eta<=1/60` is insufficient and is not extrapolated.
Instead use its published [complete polar spectrum and proper body group](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_brightness_twofold_caps/PROOF.md),
graph `bafkreigejf2bp43sgs6vx5eaomipinr2ifhyvsgucjf6gsnedxlembvi6u`,
height 8555. In unit-edge normalization the next squared area level is

\[
 b_1^2=(425+190s)/4>(a_0+1/25)^2.
\]

The same polar argument as (11) therefore puts every RID source with
area at most `a0+1/25` within chord `<2/25` of one of its thirty directed
minimum normals; zero excess gives an exact minimum normal. The proper
RID group acts transitively on these normals and includes `e_y` in the
orbit. For a fit with motion `Q`, choose a proper body symmetry `G` taking
`e_y` to that nearby normal. The new motion `QG` preserves the projected
RID source body, and its source normal `G^t k` is within `2/25` of `e_y`.
The exact inequality

\[
 2/25<\rho(1-2/625)
\]

places that normal in `C`: its transverse components are at most `2/25`,
and its y component is at least `1-(2/25)^2/2=1-2/625`. Now (16) with
`QG` replaces the RID source by the original J74 source. This preserves
the same `lambda,t`, including strictness. Conclusion 3 follows.

## 6. Transfer caps, exclusion caps and the global area gap

The parent verifier checks stable nonzero generator signs for original
normals within chord `1/20` of `+/-e_y`. The tangent zonotope there has
64 signed endpoint sums and maximum norm squared `10+4s<(35/8)^2`.
Its support therefore gives the local upper bound

\[
 A(n)\le a_0+(35/8)\alpha,
 \quad \alpha=\operatorname{dist}(n,\{e_y,-e_y\})\le1/20.
 \tag{17}
\]

The excess is strictly below this linear upper term for positive chord.
Since `(35/8)(8/875)=1/25` and `8/875<1/20`, conclusion 3 applies to
the whole closed radius-`8/875` cap. This is sixteen times the previous
transfer radius `1/1750`, and the new area band `1/25` is sixteen times
the previous `1/400`.

The committed RID radius `1/270` lies wholly inside this transfer cap.
The forward transfer would turn any strict J74 fit there into a strict
RID fit, contrary to that input theorem. This proves the claimed
all-source J74 exclusion and enlarges the former `1/30000` exclusion
radius by `1000/9`. Closed touching fits are not excluded.

If a strict J74 fit has `n in C` and `A(n)<=a0+1/90`, it lies in the
transfer band and contradicts the published RID unit-edge receiving-area
gap `1/90`. Hence the original-area statement holds in `C`. Finally,
if an arbitrary strict J74 fit had `A_D(n)<=a0+1/90`, then (4), since
`1/90<1/25`, would force its receiver into `C`. There `A_D(n)=A(n)`,
and the same contradiction applies. This proves the global inequality
(6), without claiming the corresponding global original-area statement.

## 7. Reproduction and proof boundaries

From the repository root, use Python 3.11+ and its standard library:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  timeout 55s python3 -B round-two/six-rupert-2/section_transfer/check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  timeout 55s python3 -O -B round-two/six-rupert-2/section_transfer/check.py
```

Run these separately. Explicit guards remain active under `-O`. The
checker first verifies every parent-source SHA256 in [DEPENDENCIES.json](DEPENDENCIES.json),
then freshly replays the parent compact record: original facets,
support signs, all 613 area candidates, tangent disks and sums, old
half-difference areas, common-cone gates and the RID coordinate scale.
It then checks the **supplied** 94 actual section lifts by the separate
support audit (8), not by its optional hull-based generator. `--emit`
instead finds the lifts and then checks them. All calculations use exact
`Fraction` arithmetic in the ordered real field `Q(sqrt(5))`.

The output records the full section witnesses, exact areas, all counts,
quantitative hypotheses and four rejected malformed controls. Comparison
with `expected.json` checks every field. The fields naming continuous
theorem conclusions are records of this written proof; finite evaluation
of those strings alone is not a quantified proof. The classical
Brunn-Minkowski input and both cited RID written theorems remain explicit
external mathematical dependencies. The larger RID checker was separately
replayed locally and matched its pinned evidence; this is an author input
replay, not independent review. Use that input's README for reproduction.

No floating-point passage search, solver verdict, numerical library,
private ledger, private checkpoint, large omitted corpus or external
dataset is required. The trust boundary consists of Python/Fraction
semantics, checker correctness, the original-solid identification, exact
finite coverage, and the unformalized geometric and cited RID bridges.
A timeout or incomplete computation does not establish nonexistence.

Primary status sources refreshed on 2026-10-01 are
[Fredriksson](https://arxiv.org/html/2210.00601),
[Gosain--Grimmer, Table 4](https://arxiv.org/html/2509.08190),
[Zeng](https://arxiv.org/html/2604.26531) and
[Steininger--Yurkevich](https://arxiv.org/html/2508.18475#S9.SS1).
The located unresolved Johnson list remains J72, J73, J74, J75 and J77;
RID remains a non-Rupert conjecture, while Noperthedron is a different
proved example. These bounded literature checks do not establish
historical priority. The general Cauchy/polar method is prior work;
the new finite construction and specializations are for J74's
half-difference central sections, sublevel geometry and wider exact
arbitrary-source transfer. Receivers outside these restrictions remain
an unresolved construction or obstruction frontier.
