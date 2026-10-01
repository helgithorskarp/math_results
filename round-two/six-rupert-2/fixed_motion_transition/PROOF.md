# An exact J74 source-support transition and its rigid closed-fit branch

**six-rupert-2, researcher; 2026-10-01.** Author-checked exact finite
hypotheses and a complete written geometric proof. Unformalized and
independently unreviewed. The global Rupert property of original J74
remains **OPEN**.

Let `K=conv(V)` be the original unit-edge metabigyrate
rhombicosidodecahedron J74 in [model.py](../model.py). All sixty originals,
both asymmetric cupola replacements, proper motions and actual physical
translations are retained. The body is not assumed centrally symmetric.
Its constructive named-solid identification and complete finite geometry
are the [original proof](../PROOF.md), source
`25fc9695745b6832d068d18544452b7852b5847f`, graph
`bafkreig4wvsmlau4koaib63i3cefofih67cczseu3hgdv2r6r54ga572aq`.
That geometry was independently audited in graph
`bafkreidtzhezgggv5hfqyjbmdtbrfuntr7ua6vx3ild6tv4tqdblfqt3ua`.
Every original has norm `R`, with `R^2=(11+4sqrt5)/4<5` and `R<9/4`.

## 1. The receiving patch and four additional proper motion families

Write `phi=(1+sqrt5)/2` and use the entire closed receiving rectangle
from the [two-dimensional patch proof](../nonlocal_receiving_patch/PROOF.md):

\[
\begin{split}
m&=(1,-\phi,-\phi^2)/(2\phi),\\
d&=((-5+3\sqrt5)/8,(11-3\sqrt5)/8,-1/4),\\
e&=m\times d,\qquad u(t,s)=m+td+se,\\
D&=\{(t,s):3/5\le t\le7/10,\ |s|\le\varepsilon=1/50000\}.
\end{split}                                                        \tag{1}
\]

These are raw parameters; `u` is not a unit normal. Put
`P_u=I-uu^T/(u.u)` and `M_u=I-2uu^T/(u.u)`. Let
`G=diag(-1,-1,1)`, `Hx=diag(-1,1,1)`, `Hy=diag(1,-1,1)`.
They are actual full-body symmetries, checked on all sixty originals.
Define the **fixed proper motion**

\[
Q_0=M_mH_y=
\begin{pmatrix}
(1+\sqrt5)/4 &(1-\sqrt5)/4 &1/2\\
(-1+\sqrt5)/4 &-1/2 &-(1+\sqrt5)/4\\
1/2 &(1+\sqrt5)/4 &(1-\sqrt5)/4
\end{pmatrix}.                                                     \tag{2}
\]

This is the original minimum-fit catalogue motion14. Its matrix,
orthogonality, determinant `+1` and identity `Q0=M_m Hy` are checked
directly, without trusting a catalogue label or a private search. It is
not a full-body symmetry. The new centers are

\[
\mathcal R(u)=\{Q_0,Q_0G,M_uQ_0H_x,M_uQ_0H_y\}.                   \tag{3}
\]

All are proper spatial motions. The two reflected companions are proper
because each reflection is composed with an improper actual body symmetry.
No improperly placed full source body is used.
These are motion matrices: each pair related by right multiplication
by `G` positions the same full source body. No count of inequivalent
passages is asserted.

Set

\[
a=(\sqrt5-1)/2,\quad b=(\sqrt5-3)/4,\qquad
f(t,s)=a-t+bs.                                                     \tag{4}
\]

**Theorem.** For any `(t,s) in D`, `S in R(u)`, `Q in SO(3)`,
`lambda>=1` and arbitrary actual `B in u-perp`, suppose

\[
QS^T=(I+[c]_\times)(I-[c]_\times)^{-1},
                         \quad\|c\|\le1/14400.                    \tag{5}
\]

Then

\[
\lambda P_u(QK)+B\subseteq P_uK
\quad\Longleftrightarrow\quad
Q=S,\ \lambda=1,\ B=0,\ f(t,s)\ge0.                              \tag{6}
\]

At the centers the feasible shadows are exactly equal. On the other
side of the sloped line `f=0`, the entire conditional motion neighborhood
in(5) has no closed fit of scale at least one. All boundaries and unbounded
`lambda>=1` are included. These are additional conditional source-motion
neighborhoods, not an all-source receiving classification.

**Continuous-branch consequence.** Let a continuous path of closed fits
of scale at least one stay in `D`. If it starts at one family in(3), then
it stays at that same family, with scale one and zero physical translation,
throughout its connected time interval. It cannot cross `f=0` into `f<0`
or turn into a strict passage while staying in this receiving patch.
Section5 proves this path statement without assuming differentiability.

Every center in(3) is at operator distance **greater than1/2** from each
of the prior patch centers `I,G,M_u Hx,M_u Hy`; Section6 verifies this
uniformly. Consequently the new source neighborhoods in(5) are disjoint
from the four old neighborhoods at the same receiver. The receiving
patch itself is unchanged and remains separated by projective normal
chord greater than1/3 from all six minimum axes, as proved by the parent.

## 2. Complete original contacts, including the infeasible side

The parent patch, source `5e1e16fecbe2514c930d8cba069a62cad1abb578`, graph
`bafkreicz5kllfqaamirgfwd55t24hfzs6ysxxnj572pfp3o4cbd34w2clq`,
proves that the complete original receiving boundary throughout `D` is

```
17,32,44,8,28,10,46,54,26,23,35,51,15,31,13,49,57,21
```

For each oriented edge `v_i->v_j` put

\[
a_{ij}(u)=(v_j-v_i)\times u,\qquad h_{ij}(u)=a_{ij}(u)\cdot v_i>0.
                                                                    \tag{7}
\]

The parent checks all60 original receiving inequalities at all four box
corners, strictly off the two incident originals. Affinity in `(t,s)`
therefore gives the full original polygon throughout `D`. It also proves
`u_z<0`, `||u||<9/8`, and that the physical edge lengths in(7) are one.
The current checker replays the **complete** pinned parent finite record,
all its positive-stress and inverse gates, and its damaged controls.

In cycle order, the following are the literal original preimages under
`Q0` of every receiving corner:

```
55,47,11,10,8,28,36,16,20,40,48,12,13,15,31,43,59,27
```

The checker verifies all eighteen spatial equalities `Q0 v_k=v_i` on
the original model. These equalities are independent of the receiving
parameters. Thus every endpoint contact in(7) has an original source
preimage **even where Q0K itself protrudes**. For `Q0G`, use `G v_k`.
For `M_u Q0 Hj`, use `Hj v_k`; its spatial image is `M_u v_i`.
The full-body symmetries prove these remain original vertices. In every
case the image `p'` has norm `R` and satisfies `a_ij.p'=h_ij>0`.
An assumed closed fit must satisfy these contact inequalities regardless
of the behavior of other source vertices.

## 3. Exact nonlinear rigidity at all four new centers

The parent proves uniform positive normalized weights on all36 endpoint
contacts, each greater than `1/60`, with full spatial force and torque
balance. Its five-row inverse bound is12. As established in its
Sections3--4, the rows

\[
A_i(u)=(p_i\times a_i(u),(a_i(u))_x,(a_i(u))_y),\qquad p_i=v_i
\ \hbox{or }v_j,
\]

satisfy, for every real `Z in R5`,

\[
L=\max_i A_i(u)Z\ge0,\qquad \|Z\|_2\le2160L.                     \tag{8}
\]

These are the actual endpoint rows, not rows from a centrally symmetric
replacement. The positive weights are repaired off the parent arc by
five exact corrections, and uniform existence and positivity are proved
by a Neumann inverse bound. Four exact stress evaluations only check
that repair formula; sampling is not its continuum justification.

For an arbitrary physical `B perpendicular u`, write
`B=(tau_x,tau_y,-w.tau)`, `w=(u_x/u_z,u_y/u_z)`, and `T=I2+ww^T`.
Then `a_i.B=(a_i)_xy.T tau` and `||B||<=||T tau||`.
Consequently(8) retains both unrestricted physical translation variables.

Let `C=QS^T` as in(5) and `v=2 lambda c/(1+||c||^2)`. The exact Cayley
identity and the actual original contact inequalities give

\[
(\lambda-1)h_i+a_i\cdot(v\times p'_i+B)+E_i\le0,\qquad
E_i=a_i\cdot\{c\times(v\times p'_i)\}.                             \tag{9}
\]

For the fixed centers `p'_i=p_i`; use `Z=(v,T tau)` in(8).
For the reflected centers `p'_i=M_u p_i`, and
`p'_i cross a_i=-M_u(p_i cross a_i)` because `M_u a_i=a_i` and
`det M_u=-1`. Use `Z=(-M_u v,T tau)`. This preserves Euclidean norm,
so the same balanced spanning bound applies.

The physical estimates `||a_i||<9/8` and `||p'_i||=R<9/4` yield

\[
|E_i|\le(81/32)\|c\|\|v\|.                                       \tag{10}
\]

Since `lambda>=1` and every `h_i>0`, dropping the first nonnegative term
in(9), then using(8)--(10), gives

\[
\|Z\|\le2160(81/32)(1/14400)\|Z\|
                  =(243/640)\|Z\|.                               \tag{11}
\]

Hence `Z=0`, which forces `c=0`, `B=0`, and `Q=S`. The remaining
positive-support inequality in(9) forces `lambda=1`. This conclusion
does not presuppose that the center is feasible. It includes arbitrary
scale at least one; no upper bound on scale or translation was imposed.

## 4. The complete fixed-pose feasible quadrilateral

For every edge in the complete cycle and every original source vertex
`v_k`, the unit-scale zero-translation support gap is the affine form

\[
g_{ij,k}(t,s)=((v_j-v_i)\times(m+td+se))\cdot(v_i-Q_0v_k).
                                                                    \tag{12}
\]

There are exactly `18*60=1080` forms; none of the asymmetric originals
is omitted. The actual source39 against receiving edge17--32 gives

\[
g_{17,32,39}(t,s)=(-1+\sqrt5)/4-t/2+(-3+\sqrt5)s/8=f(t,s)/2.
                                                                    \tag{13}
\]

Thus `f>=0` is necessary. Its intersection with `D` is exactly the
quadrilateral with vertices, in order,

\[
(3/5,-\varepsilon),\quad(a-b\varepsilon,-\varepsilon),\quad
(a+b\varepsilon,\varepsilon),\quad(3/5,\varepsilon).                \tag{14}
\]

The checker verifies `3/5<a+b s<7/10` at both `s=+-epsilon`, and tests
**all1080 actual original forms at all four vertices** in(14). All are
nonnegative. Affinity and convexity imply all1080 are nonnegative
everywhere in this quadrilateral, so the full source fits. This is an
exact finite certificate of the complete region; the discovery clipping
program is not a checker dependency.

Exactly36 forms vanish identically, the two literal preimage endpoint
constraints per edge. All other forms except(13) are strictly positive
at all four vertices. Formula(13) vanishes at the two right vertices
and is positive at the two left ones. The full sign accounting is4320
comparisons:4174 positive and146 zero. Thus no additional hidden support
event truncates(14). Original39 gives the single nonbox frontier.

Because every receiver corner has a literal source image,
`P_uK subseteq P_u(Q0K)` holds everywhere in `D`. On(14) the reverse
containment also holds, so these feasible shadows are **equal**.
Furthermore `GK=HxK=HyK=K` and `P_u M_u=P_u`. Therefore every center
in(3) has the same projected source shadow as `Q0` and has exactly the
same feasibility region. Combining this with Section3 proves(6).
In particular the transition does not hide a strict unit passage.

## 5. Continuous closed-fit paths cannot leave this branch in the patch

Let `r` range over a connected real time interval, with continuous
`t(r),s(r),Q(r),lambda(r),B(r)` giving closed fits in `D`, `Q(r) in SO(3)`,
`lambda(r)>=1`, `B(r) perpendicular u(r)`. Choose one of the continuous
center formulas `S(r)` in(3). Suppose at some time `r0` the path has
`Q(r0)=S(r0)`, `lambda(r0)=1`, `B(r0)=0`.

Let `E` be the set of times with all three equalities. It is nonempty
and relatively closed by continuity. It is relatively open as well:
at any `r in E`, the relative motion `Q(r')S(r')^T` tends to identity
as `r'` tends to `r`. The inverse Cayley chart is continuous near
identity, so(5) holds in a time neighborhood. Theorem(6) forces the
three equalities at every such time. Connectedness gives the entire
time interval `E`. Equation(6) also forces `f(t(r),s(r))>=0` throughout.

This proves the stated branch consequence, including paths along the
event line or box boundary. It uses only continuity. Paths leaving the
receiving patch, or other disconnected source motions, remain outside
this conclusion.

## 6. These source neighborhoods are additional, with uniform separation

For proper matrices `A,B`, the exact rotation-axis identity gives

\[
\|A-B\|_{\rm op}^2=3-\operatorname{tr}(AB^T).                      \tag{15}
\]

For old fixed centers `I,G`, the checker directly verifies
`11/4-tr(Q0 S^T)>0`. For each moving old center `S=M_u Hj`, put
`D_j=Q0 Hj`; then

\[
(11/4-\operatorname{tr}(Q_0S^T))\|u\|^2
=(11/4-\operatorname{tr}D_j)\|u\|^2+2u^TD_ju.                     \tag{16}
\]

This is a quadratic polynomial in the real rectangle parameters.
Under `t=3/5+x/10`, `s=-epsilon+2epsilon*y`, `x,y in[0,1]`, the
checker expands it exactly and verifies all nine degree-(2,2) tensor
Bernstein coefficients strictly positive. The tensor Bernstein basis
is nonnegative and sums to one, so(16) is uniformly positive. Formula(15)
therefore proves `||Q0-S||op>1/2` for all four old centers.

Right multiplication by `G` and the map `A -> M_u A Hy` preserve
operator distance and permute the old center set. They take `Q0` to
all four formulas in(3), so every new center has the same strict
separation from the old set. A relative Cayley vector of norm at most
`kappa=1/14400` gives `||Q-S||op<=2kappa`. Since `4kappa<1/2`, no new
and old conditional neighborhood at the same receiver can overlap.
This certifies additional source coverage, not a change of constants
in the prior receiving theorem.

The four new matrices are also distinct from one another. Fixed centers
differ by `G`, and so do the two reflected centers. Coincidence of a fixed
and reflected center would require `u` parallel to either sign of `Q0 e_x`
or `Q0 e_y`. The checker verifies that all four receiving box corners
have octant `(+,-,-)`, hence so does the entire patch by affinity. The
two source columns have octants `(+,+,+)` and `(-,-,+)`, respectively;
neither it nor its opposite agrees with the receiving octant. This
rules out those parallelisms.

## 7. Reproduction, dependencies, literature and remaining frontier

From the repository root, Python3.11+ standard library only:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-rupert-2/fixed_motion_transition/check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B -O round-two/six-rupert-2/fixed_motion_transition/check.py
```

Both compare the **entire** compact expected record. All mathematical
guards use explicit exceptions and survive optimization. Eight damaged
controls break properness, an original preimage, a full-body companion,
the event's original source witness, its transverse coefficient, the
feasible polygon, the nonlinear absorption radius, or the old-center
separation. Each must reject. `DEPENDENCIES.json` pins seven direct
inputs including the complete parent proof; the complete patch record
transitively replays the [parent arc](../nonlocal_arc_wrench/PROOF.md),
source `03e077716c0a21496133189eee3ba5444cb77555`, graph
`bafkreihs43shk7p73kl327xg73lvh32elxxl5f6qg5o64mzeayyqkgoprm`.
The parent's larger `1/6000` source radius at `s=0` is unchanged.

The six-axis [quantitative result](../quantitative_minimum_caps/PROOF.md),
graph `bafkreiedis2ptxh7hqn5gnz7czo2klknnnhboluo3dz7ufcddgvzi2hote`,
and its [independent quantitative audit](../../six-reviewer-4/quantitative-cap-audit/REVIEW.md),
graph `bafkreiaq2w4cqofuwbkqhi66lkff2p6lxgaepdxsvapsw6jypjmmqez5lm`,
remain credited context; their all-source localizers are not an all-source
premise at this nonlocal receiving patch. The complementary
[RID Cauchy-transition proof](../../six-rupert-3/rid_cauchy_transition_cones/PROOF.md),
source `49504817cd4e23b52419dbb91ca6970ec3554dd1`, graph
`bafkreiga3tnen3tjbmd36lgpveyfxcta6zyvnecje7gt2rxogdf7s7ebki`,
was read in full. It uses different-body central symmetry, area/width
localization and opposite radial pairs; none supplies a J74 premise here.
Its published scope and independent unreviewed status are retained.
The later [independent RID wedge audit](../../six-reviewer-4/rid-wedge-audit/REVIEW.md),
graph `bafkreibpjecrwhcfm5hijqhqd3ippbddthuikhyqytrserhf5vojukzvfm`,
confirms the older wedge8995 premise and sharpens its area domination.
It explicitly gives no verdict on the new region in9037; none transfers
to this J74 theorem. Its complete committed body was read before publication.

Primary literature reopened live2026-10-01: [Gosain--Grimmer, Table4](https://arxiv.org/html/2509.08190)
still has no passage for J72,J73,J74,J75,J77; [Zeng, Section1.2](https://arxiv.org/html/2604.26531)
reports87 of92 Johnson solids Rupert and states the RID non-Rupert
conjecture as open. [Steininger--Yurkevich](https://arxiv.org/abs/2508.18475)
proves a different constructed body non-Rupert. No global resolution
or method-priority claim is asserted. Positive stresses, Cayley closure,
exact affine support certificates and connectedness are prior methods.
The increment is the four additional J74 source families, their complete
two-parameter support transition, and the continuous branch obstruction.

Trust boundary: exact ordered Fraction/Q(sqrt5) arithmetic, the original
named-body construction and the written continuum geometry. Source
publication and shared signing identity do not prove correctness or
independent review. No floating search, missing passage, timeout or
incomplete enumeration supplies a nonexistence premise.

The original receiving complement and disconnected source motions remain
unresolved. A concrete next construction frontier is a changed receiving
horizon with new original contacts, or source motions outside the eight
conditional neighborhoods now credited on this patch. Merely perturbing
this fixed catalogue branch across(13) cannot provide a passage within `D`.
