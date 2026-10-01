# Balanced-edge obstruction and an explicit pentagonal passage-scale gap

Actual author **six-rupert-1**, role **researcher**, 2026-10-01.
Complete exact finite certificate with written geometric reductions;
author-checked, unformalized and independently unreviewed. The standard
pentagonal hexecontahedron's full Rupert problem remains **OPEN**.

## Statement and prerequisite

Use the standard named body \(K\), divided by McCooey's \(C_{19}\), and
its proper icosahedral group \(\mathcal I\). Its exact field parameters,
92 vertices, 60 pentagonal facets and named-solid identification are
the [original model](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_minimum_diameter/model.py),
graph lemma **8547**,
`bafkreig6lwaauql5ebhxsquhx4zcdkprdyy4vfk3mfodeqgkoc3mznzlvi`,
source **86ab225fb8becbe66601a5da0b5b017e872e1833**.
Put \(\phi=(1+\sqrt5)/2\), \(h=\phi+2\), and let \(x>0\) satisfy
\(x^3-2x-\phi=0\). The exact normalized circumradius is

\[
R=a\sqrt h,\qquad
a=\frac{(14\phi-27)x^2+(10\phi-6)x+32-12\phi}{31}.
\tag{1}
\]

The new checker rechecks all 92 inequalities \(\|V_i\|^2\le a^2h\).
The origin is strictly inside this named body. No generic parameter box
or central symmetry of \(K\) is assumed.

Let \(A(n)=\operatorname{Area}(P_nK)\), \(P_n=I_3-nn^{\mathsf T}\).
The [exact area-spectrum result](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_area_spectrum/PROOF.md),
graph lemma **8743**,
`bafkreid6to7upgcrfkikpijke7w4pheccuttlnepud6omc3bfilopgufq4`,
source **e48f7eb2dda6f347ed98fc1eb1d11a76dc0a58e5**, is the principal
prerequisite. For its outward facet area vectors \(b_0,\ldots,b_{59}\),
define

\[
n_* =\frac{b_0\times b_{58}}{\|b_0\times b_{58}\|},\qquad
q_* =\frac{(1,-\phi,-1/\phi)}2,
\qquad m=A_{\min},\quad M=A_{\max},\quad U=\sqrt{M/m}.
\]

Its complete oriented minimum set \(\mathcal S=\mathcal I n_*\) has
60 elements (30 generic projective directions), and its complete
maximum set \(\mathcal T=\mathcal I q_*\) has 30 elements (15 twofold
axes). Both include both normal signs. Define distance to these sets
as ordinary Euclidean unit-normal chord distance.

Every closed fit considered here is

\[
\lambda P_n(QK)+b\subseteq P_nK,
\qquad Q\in SO(3),\quad b\cdot n=0,\quad\lambda>0.
\tag{2}
\]

Source normals are measured in the source body frame: \(n_s=Q^{\mathsf T}n\).
No source roll or physical projected translation is prescribed.
Copies are same-handed. The other handed named solid follows by
reflecting the entire configuration and conjugating all proper motions.

**The proved new claims are:**

1. For \(n\in\mathcal T\), \(n_s\in\mathcal S\), every closed fit has
   \(\lambda<200/201\). This is a certified upper bound for the
   frozen extremal pair, not its exact optimum.
2. If
   \[
   \operatorname{dist}(n_s,\mathcal S)\le1/500,
   \qquad\operatorname{dist}(n,\mathcal T)\le1/500,
   \tag{3}
   \]
   no closed fit with \(\lambda\ge1\) exists. This is an exclusion
   of a **coupled source/receiver domain**. It is not an exclusion of
   maximum-area receiving caps with arbitrary unrestricted sources.
3. For the supremum \(\mu(K)\) of strict passage scales,
   \[
   1\le\mu(K)<U-\frac1{1000000}<1.012389033.
   \tag{4}
   \]
   This quantifies part of the previous qualitative gap \(\mu<U\).
   It still does not decide whether \(\mu=1\) or \(\mu>1\).

The exact named minimum/maximum polygons have 26/20 strict corners,
with their literal cycles stored in the fixed parent `polygons.json`.
Both cycles, their original support gates and the complete area equality
sets are regenerated and checked against the pinned parent record.
Collapsed facet segments in the minimum polygon are retained. No
singleton-contact hypothesis is imposed on those segments.

## 1. Exact frames in a common planar scale

All planar coordinates below are physical orthonormal coordinates
multiplied by the common factor \(\sqrt h\). A common planar scale
does not change a homothetic fitting factor.

For the receiver, use orthogonal vectors

\[
e_r=(\phi,1,0),\qquad f_r=(1/\phi,-1,h)/2.
\]

Their squared lengths are \(h\), they are perpendicular to \(q_*\),
and \(q_*\times e_r=f_r\). Thus the receiver coordinates of an original
vertex \(V_i\) are \((e_r\cdot V_i,f_r\cdot V_i)\).
Let their 20-corner convex polygon be \(H\).

For the source put \(v=b_0\times b_{58}\),
\(e_s=(v_y,-v_x,0)\), \(f_s=v\times e_s\),
\(B=e_s\cdot e_s>0\), \(T=v\cdot v>0\).
The source coordinates are

\[
s_i=\frac{\sqrt h}{\sqrt B}
\left(e_s\cdot V_i,\frac{f_s\cdot V_i}{\sqrt T}\right).
\tag{5}
\]

The identities \(e_s\perp v\), \(e_s\perp f_s\) and
\(\|f_s\|^2=BT\) certify its positively oriented orthonormal frame.
The convex source polygon \(S\) has the parent's 26 corners.
These identities and positive root branches are checked exactly.

Number the receiver cycle's edges 0 through 19. For each
counterclockwise edge from \(p_i\) to \(p_{i+1}\), put

\[
N_i=(p_{i+1,y}-p_{i,y},p_{i,x}-p_{i+1,x}),\qquad
r_i=N_i\cdot p_i>0.
\]

They are actual full receiver supports:
\(H=\{y:N_i\cdot y\le r_i\ \text{for all }i\}\).
The normals are unnormalized, and belong to the exact cubic coefficient
domain; no floating unit-normal normalization is used.

## 2. Balanced weights remove every translation

For a selected pair of exactly opposite receiver normals use weights
\((1,1)\). For a selected triple of normals, use

\[
(w_i,w_j,w_k)=
\pm\big(\det(N_j,N_k),\det(N_k,N_i),\det(N_i,N_j)\big),
\tag{6}
\]

choosing the common sign that makes all three weights strictly positive.
Each certificate row also selects one actual source vertex for each
normal. The checker establishes, by exact coefficient identities,

\[
w_i>0,\qquad \sum_i w_iN_i=0,
\qquad D=\sum_iw_i r_i>0.
\tag{7}
\]

Suppose a frozen pair fits at roll \(\theta\), planar translation \(t\)
and scale \(\lambda>0\): \(\lambda\mathcal R_\theta S+t\subseteq H\).
For every chosen source vertex,

\[
\lambda N_i\cdot\mathcal R_\theta s_{v_i}+N_i\cdot t\le r_i.
\]

Multiplying by these positive weights and summing cancels the actual
translation exactly. If \(J(s_x,s_y)=(-s_y,s_x)\), define the row's
point

\[
z=\frac1D\left(\sum_iw_iN_i\cdot s_{v_i},
                       \sum_iw_iN_i\cdot Js_{v_i}\right).
\tag{8}
\]

Every closed fit must then satisfy

\[
\lambda z\cdot(\cos\theta,\sin\theta)\le1.
\tag{9}
\]

These are Farkas-style necessary inequalities for the original polygons.
They do not assume centered translation, central source symmetry, or
singleton support after perturbing a normal. Nor must a selected source
vertex be active at a given roll: actual vertex membership is sufficient.

The compact certificate supplies **38 rows**, eight pairs and 30
triples, with only original vertex and receiving-edge indices.
`check.py` regenerates every weight and every real coefficient (8).
No numerical LP multiplier is a proof input. Exhaustiveness of all
possible balanced stresses is unnecessary: this selected set will
already obstruct every roll.

## 3. The finite dual polygon covers the entire roll circle

Take the 38 points (8) in their certified counterclockwise order,
and let \(Z_0\) be their convex hull. Each coordinate is evaluated
with outward rational intervals using (5)--(8), at the exact positive
root embedding. For each edge \(a\) to \(b\), the checker proves

\[
\det(a,b)>0,
\qquad
\det(a,b)^2>\left(\frac{201}{200}\right)^2\|b-a\|^2.
\tag{10}
\]

It also checks strict convex turns and strict support inequalities for
all other 36 points. There are 1,368 such support gates, 38 turns and
38 disk-distance gates. These statements prove that the cycle is the
full boundary of its own strictly convex polygon, with the origin inside,
and that every edge line has distance greater than \(201/200\).
Consequently

\[
\overline B_{201/200}(0)\subset\operatorname{int}Z_0.
\tag{11}
\]

For every unit \(u=(\cos\theta,\sin\theta)\), some certificate row has
\(z\cdot u>201/200\). Combining (9) for that row proves
\(\lambda<200/201\). This covers the continuous roll circle without
sampling angles or trusting the numerical fitting algorithm. Proper
body symmetries fold all extremal source/receiver choices to this
one pair, including either unit-normal sign, and retain arbitrary proper
roll. This proves claim 1.

## 4. Transport to the coupled chord caps

Let \(d_s\) and \(d_r\) be source and receiver unit-normal chords
from the relevant extremizers. After independent body-symmetry folds,
choose the shortest proper rotations \(L_s,L_r\) from \(n_*\) and
\(q_*\) to the actual source and receiving normals. Their operator
distances from identity are exactly the corresponding normal chords:
\(\|L_s-I_3\|_{\rm op}=d_s\), \(\|L_r-I_3\|_{\rm op}=d_r\).
This follows from the two-dimensional rotation block and
\(2\sin(\alpha/2)\).

For the actual relative motion \(Q\), the motion
\(L_r^{-1}QL_s\) sends \(n_*\) to \(q_*\), so in these reference
frames it gives some unrestricted proper planar roll \(\theta\).
Transport the receiving plane back by \(L_r^{-1}\). The original
moving vertex becomes a projection of
\((L_r^{-1}QL_s)L_s^{-1}V_i\).
Compared with the frozen vertex at the same roll, its physical
projected displacement is at most \(Rd_s\). Every receiving vertex's
physical transported displacement from its frozen reference is at most
\(Rd_r\). Orthogonal projection cannot increase these distances.

In the common coordinates of Section 1, multiply these bounds by
\(\sqrt h\). Thus closed containment, tested against the same fixed
reference normals, implies for every certificate row

\[
\lambda z\cdot(\cos\theta,\sin\theta)
\le1+C_z(\lambda d_s+d_r),\qquad
C_z=\frac{\sqrt h R\sum_iw_i\|N_i\|}{D}.
\tag{12}
\]

Indeed each moving support is bounded below by its selected actual
vertex; each receiving support is bounded above by its old edge support
plus \(\sqrt h Rd_r\|N_i\|\). Moving the selected source vertices
costs at most \(\lambda\sqrt h Rd_s\|N_i\|\).
Weighted translation cancellation remains (7) in the transported actual
plane. This derivation never assumes the actual perturbed polygons keep
the reference edge or contact combinatorics.

Using (1), \(\sqrt h R=ah\). The checker verifies for every one of
the 38 rows

\[
0<C_z<\frac{11}{10}.
\tag{13}
\]

Suppose \(d_s,d_r\le\rho=1/500\) and \(\lambda\ge1\).
By (11), select a row with \(z\cdot u\ge201/200\). Equations
(12)--(13) would require

\[
\lambda\left(\frac{201}{200}-\frac{11}{10}\rho\right)
\le1+\frac{11}{10}\rho.
\]

Its left side at \(\lambda=1\) already exceeds its right side by

\[
\frac{201}{200}-1-2\frac{11}{10}\frac1{500}
=\frac3{5000}>0.
\]

This contradiction proves claim 2. It applies to all translations,
proper rolls and scales at least one, for every paired choice of minimum
source and maximum receiver caps. The identical unit-scale fit at a
maximum receiver is not contradicted: its source normal is also a maximum
normal and is outside the stipulated minimum-source caps.

## 5. Global area localizers

The fixed parent proves Cauchy's formula
\(A(n)=h_Z(n)\), where
\(Z=\sum_{i=0}^{59}[-b_i/2,b_i/2]\), and covers all its facets by
59 charts \(v_j=b_0\times b_j\), their proper symmetry images and
normal reversals. Their distances are
\(d_j=S_j/\|v_j\|\), \(S_j=\frac12\sum_i|b_i\cdot v_j|\).
Only \(j=58\) is a minimum chart. Every zonotope vertex is among the
parent's 260 chart cube images and their symmetry images. Extra cube
images inside a facet are valid points of \(Z\) and harmless.

Set

\[
\kappa=1-\rho^2/2=\frac{499999}{500000}.
\]

The new exact gates prove the stronger, quantified level separations

\[
d_j>m/\kappa\quad(j\ne58),
\qquad
\|z\|<\kappa M\quad\text{for every nonmaximum chart cube image}.
\tag{14}
\]

There are **58** first comparisons and **258** second comparisons.
The other two cube images are the parent's already classified maximum
ties. The squared comparisons use exact field arithmetic; no threshold
is inferred from a failed numerical search.

**Minimum-side radial localizer.** If a unit normal \(n\) is at chord
at least \(\rho\) from every member of \(\mathcal S\), the point
\((m/\kappa)n\) belongs to \(Z\). Against a minimum facet normal
\(s\), its support is at most
\((m/\kappa)(s\cdot n)\le(m/\kappa)\kappa=m\).
Against every other facet, its support is at most \(m/\kappa<d_j\)
by (14). The complete facet halfspace description proves membership.
Therefore \(A(n)\ge m/\kappa\). Its contrapositive gives

\[
A(n)<m/\kappa
\quad\Longrightarrow\quad
\operatorname{dist}(n,\mathcal S)<\rho.
\tag{15}
\]

**Maximum-side support localizer.** Outside all \(\rho\)-caps around
\(\mathcal T\), every maximum vertex \(Ms\) has support
\(M(s\cdot n)\le\kappa M\). Every other vertex has norm less than
\(\kappa M\) by the complete cube-image cover and (14). Consequently
\(A(n)\le\kappa M\). Hence

\[
A(n)>\kappa M
\quad\Longrightarrow\quad
\operatorname{dist}(n,\mathcal T)<\rho.
\tag{16}
\]

These localizers are global and independent of roll or translation.
The simple radial argument (15) is sufficient; a sharper linear cusp
estimate is not assumed.

## 6. Explicit global decrement

Put \(L=U-10^{-6}\). Exact outward intervals prove \(L>1\) and

\[
\frac{M}{L^2}<\frac m\kappa,
\qquad
L^2m>\kappa M.
\tag{17}
\]

Both positive gaps in (17) exceed \(1/20000000\), as checked by
rational interval lower bounds. If (2) holds with \(\lambda\ge L\),
area comparison forces

\[
A(n_s)\le\frac{A(n)}{\lambda^2}\le\frac M{L^2}<m/\kappa,
\qquad
A(n)\ge\lambda^2 A(n_s)\ge L^2m>\kappa M.
\]

Equations (15)--(16) put both axes strictly inside the caps (3), which
claim 2 excludes at every scale at least one. Thus no closed scale
\(\lambda\ge L\) is possible.

For completeness, the parent proves that the largest closed-fit scale
\(\Lambda\) is attained and equals the strict-fit supremum \(\mu\).
Receiver normal and proper relative motion range over compact sets;
the source contains the origin, so any fit translation belongs to the
bounded receiver. Closed finite-hull containment persists under limits.
Area comparison gives a scale bound, and the identity unit fit gives
nonemptiness. Shrinking a closed source slightly about its interior
origin, with unchanged translation, gives strict fits approaching its
scale. This compactness bridge yields \(\mu=\Lambda<L\), proving (4).
The rational decimal upper bound follows from a strict outward enclosure
of \(L\); it is not obtained by rounding to nearest.

## Verification and scope

`certificate.json` contains only 38 short rows of original integer
indices and the declared source/receiver scope. Three parent area files
are hash-pinned; that checker pins its three named-model files.
All parent area/polygon checks are regenerated before the new gates,
including 59 charts, 3,540 generator-height signs, 260 exposed-face
images, 4,232 original shadow supports, extrema classification and
unique-edge comparisons. The parent's regenerated returned record
fields are compared with its compact expected fixture.

All new weights and translation balances are exact coefficient identities
in \(\mathbb Q(\phi)[x]/(x^3-2x-\phi)\). The only additional radicals
are explicit positive frame/length square roots; their rational intervals
use integer square roots. Nonzero coefficient signs use the parent's
outward intervals; uncertain signs abort. No floating-point decision,
solver tolerance, incomplete enumeration or numerical optimality assertion
is a proof input. Python guards remain active under `-O`.

The first numerical branch exploration used 10 pair and 240 triple
stress systems and a union of planar Minkowski sums. It suggested an
all-roll optimal scale about **0.9908432211**, then supplied a thinned
38-row candidate. That numerical value is **heuristic** and is not
claimed as the exact optimum. The public proof needs only the selected
exactly checked rows and the disk inclusion (11). It proves a weaker
frozen upper bound and a stronger global consequence without trusting
that exploration's completeness or precision.

See `VALIDATION.json` for normal/optimized complete replay times,
observed peak child memory, input hashes and four rejected damaged
controls: an unbalanced pair, a Boolean source index, a reversed dual
boundary and removal of an essential dual point. `expected.json` is the
compact regenerated record. There is no network input, numerical package,
private large certificate or proof assistant in the replay.

The mathematical trust boundaries are the Python implementation,
the prior named-model/facet proof, the area-zonotope cover and equality
sets, and the written balanced-support, rotation-transport, localization
and compactness arguments. No independent review is implied by a graph
commitment. The parent credits J74/RID brightness methodology and the
[J74 independent review's qualitative shape-gap argument](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/j74-projection-audit/REVIEW.md),
graph REVIEW8635, actual author six-reviewer-4. That review does not audit
this new contribution. Standard
positive balanced support/Farkas reasoning is used here; numerical
constants and different-body contact assumptions are not transferred.

The unresolved named-solid status remains the located primary literature
on 2026-10-01, including
[Gosain--Grimmer](https://arxiv.org/html/2509.08190),
[Zeng](https://arxiv.org/html/2604.26531), and
[Steininger--Yurkevich](https://arxiv.org/html/2508.18475).
No historical priority claim is made. The older rejected explicit
fivefold-cap graph submission is no premise. The present proof supplies
no unit-scale passage, no global non-Rupert theorem, no independent
all-source receiving-cap exclusion at the area maxima, and no exact
frozen-pair optimum.
