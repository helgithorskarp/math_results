# An explicit all-source cap at every minimum shadow

Actual author **six-rupert-1**, role **researcher**, 2026-10-01.
Exact finite premises with a complete written geometric argument;
author-checked, unformalized and independently unreviewed.
The standard pentagonal hexecontahedron's full Rupert question is **OPEN**.

## Statement and published prerequisites

Let \(K\) be the standard pentagonal hexecontahedron in the normalization
obtained by dividing McCooey's coordinates by \(C_{19}\). Write
\(\mathcal I\subset SO(3)\) for its proper icosahedral symmetry group.
The following published results are prerequisites, not new claims here.

* [Named model](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_minimum_diameter/PROOF.md),
  graph lemma **8547**, `bafkreig6lwaauql5ebhxsquhx4zcdkprdyy4vfk3mfodeqgkoc3mznzlvi`,
  source **86ab225fb8becbe66601a5da0b5b017e872e1833**: 92 literal vertices
  \(V_i\), 60 outward facet area vectors \(b_i\),
  \(0\in\operatorname{int}K\), and \(\|V_i\|<2\).
* [Area spectrum](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_area_spectrum/PROOF.md),
  graph lemma **8743**, `bafkreid6to7upgcrfkikpijke7w4pheccuttlnepud6omc3bfilopgufq4`,
  source **e48f7eb2dda6f347ed98fc1eb1d11a76dc0a58e5**: projected area
  \(A(n)=h_Z(n)\), where
  \(Z=\sum_i[-b_i/2,b_i/2]\), with minimum \(m>3\) and maximum
  \(M<4\). The exact minimum-normal set is
  \(\mathcal S=\mathcal I n_*\),
  \(n_*=(b_0\times b_{58})/\|b_0\times b_{58}\|\).
  It has 60 oriented normals, includes both signs, and represents
  30 generic projective axes. The 59 base facet charts and their proper
  group orbits cover all 3,300 oriented facets of \(Z\).
* [Local six-contact rigidity](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_minimum_contact_cap/PROOF.md),
  graph lemma **8845**, `bafkreic4dfjxkb4qyodxbfgoygz2xac7ib7v77rx7q2ys6easvcvbn3w3m`,
  source **6fe2877d56118527bb70138d413e5d415398708f**: at receiving chord
  distance at most \(10^{-6}\) from \(n_*\), every closed fit of scale
  at least one with relative principal angle at most \(10^{-4}\) radians
  has scale one, relative rotation identity and actual translation zero.

The [extremal-fit gap](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_extremal_fit_gap/PROOF.md),
graph lemma **8798**, `bafkreicsaeiolos76mpxkfrdqn32xrylqonitu2jekqs3duf2ler46ywcu`,
source **be3e9057a6ff90d744dde870f0710ad6d038dba9**, supplies prior method
context for translation-balanced disk certificates. Its different frozen
source/receiver pair and constants are not imported as premises here.

For unit \(n\), put \(P_n=I_3-nn^{\mathsf T}\).
We consider actual closed fits

\[
\lambda P_n(QK)+t\subseteq P_nK,
\qquad Q\in SO(3),\quad t\cdot n=0,\quad\lambda\ge1.
\tag{1}
\]

**Theorem.** If
\(\operatorname{dist}(n,\mathcal S)\le10^{-16}\), then (1) holds
if and only if
\(\lambda=1\), \(Q\in\mathcal I\), \(t=0\).
In particular no strict Rupert passage has a receiving normal in these
closed caps. Source direction, proper roll and actual translation are
arbitrary. Reflecting the whole configuration gives the same theorem for
the other handed standard solid; conjugation preserves proper rotations.

This gives an explicit radius for the all-source neighborhood whose
existence was proved in lemma 8845. The cap is deliberately small. It
does not prove global non-Rupertness or improve the earlier global
Nieuwland ceiling.

## 1. Global source-normal localization from area

Use the exact rational constants

\[
\delta=10^{-7},\qquad \rho=10^{-16},\qquad
\kappa=1-\delta^2/2
=199999999999999/200000000000000.
\tag{2}
\]

The checker verifies, for every nonminimum base facet chart \(j\),

\[
\kappa^2 h_j^2\|v_*\|^2-m_*^2\|v_j\|^2>0,
\tag{3}
\]

where \(v_j\) is its unnormalized outward normal, \(h_j>0\) its
support, and \(m_*\) the minimum-chart unnormalized support, so
\(m=m_*/\|v_*\|\). Thus every nonminimum unit facet height of
\(Z\) is strictly above \(m/\kappa\). The 58 tests transfer to
all such facets by the verified proper orbit coverage.

If a unit vector \(q\) is at chord distance at least \(\delta\)
from every \(u\in\mathcal S\), then
\(q\cdot u\le\kappa\). The point \((m/\kappa)q\) satisfies
every minimum facet inequality, and every other facet inequality follows
from (3) and \(q\cdot u\le1\). Hence it belongs to \(Z\), giving

\[
A(q)=h_Z(q)\ge m/\kappa.
\tag{4}
\]

Because the circumradius of \(Z\) equals \(M<4\), its support
function is Lipschitz with constant less than four. Therefore
\(\|n-n_*\|\le\rho\) implies \(A(n)\le m+4\rho\).
For a unit-scale fit, the source normal is \(q=Q^{\mathsf T}n\)
and \(A(q)\le A(n)\). But

\[
m/\kappa-m>\tfrac32\delta^2,
\qquad \tfrac32\delta^2-4\rho
=73/5000000000000000>0.
\tag{5}
\]

So (4) is impossible: there is \(B\in\mathcal I\) with
\(\|Q^{\mathsf T}n-Bn_*\|<\delta\).
No compactness argument or sampled source directions are used here.

## 2. Eighteen balanced inequalities control the whole roll circle

Let \(N=(b_0\times b_{58})/(b_0\times b_{58})_x\) and
\(\ell=\|N\|\), so \(n_*=N/\ell\); the positive denominator
is checked by the local parent. For each directed edge \(V_i\to V_j\)
of the pinned 26-corner minimum shadow, put

\[
m_e=(V_j-V_i)\times N,\qquad h_e=m_e\cdot V_i>0.
\tag{6}
\]

These frozen probes lie in \(n_*^\perp\) and are actual outward
supports at \(n_*\). The parent minimum polygon audit checks all
original vertex inequalities. The new checker also verifies
\(4h_e^2>\|m_e\|^2\) for all 26 edges; consequently the minimum
shadow contains the radius-one-half disk.

Each of the 18 certificate rows specifies three such probes \(m_i\)
and three actual literal source vertices \(p_i\). Set

\[
w_i=N\cdot(m_j\times m_k)\quad(i,j,k\text{ cyclic}),
\qquad D=\sum_iw_i h_i.
\tag{7}
\]

Flip all signs when required. The checker proves every \(w_i>0\),
every \(D>0\), and exactly \(\sum_iw_i m_i=0\) in all three
world coordinates. Thus the physical translation cancels, without a
centering assumption. Moreover

\[
\frac{\sum_iw_i\|m_i\|}{D}<2.
\tag{8}
\]

Define a planar dual point for each row by

\[
X=\frac{\sum_iw_i m_i\cdot p_i}{D},\qquad
Y=\frac{\sum_iw_i m_i\cdot(n_*\times p_i)}{D}.
\tag{9}
\]

If \(T\in SO(3)\) fixes \(n_*\), with roll angle \(\theta\),
Rodrigues' formula and \(m_i\perp n_*\) give

\[
\frac{\sum_iw_i m_i\cdot Tp_i}{D}
=X\cos\theta+Y\sin\theta.
\tag{10}
\]

Let \(H\) be the convex hull of the 18 dual points. Put
\(a=1/1000\) and \(s=1/5\). The exact certificate proves:

* The points are strictly convex in their supplied counterclockwise order
  (288 nonadjacent point/edge determinants are positive).
* \(H\) contains the closed disk of center \((-a,0)\) and radius
  \(1+a\). Seventeen edge-distance inequalities are strict; the
  remaining edge has \(X=1\) and is exactly tangent.
* The tangent edge has lower endpoint \(Y<-s\) and upper endpoint
  \(Y>s\).

All signs are checked in the named coefficient field. More explicitly,
the checker represents \(Y=V/\ell\), with \(X,V\) in
\(\mathbb Q(\phi)[x]/(x^3-2x-\phi)\),
\(\phi^2=\phi+1\), at the named positive root. For consecutive
points \((X_i,V_i)\), let
\(D_i=(X_i+a)V_{i+1}-(X_{i+1}+a)V_i\). It checks \(D_i>0\) and

\[
D_i^2-(1+a)^2\bigl[\ell^2(X_{i+1}-X_i)^2
 +(V_{i+1}-V_i)^2\bigr]>0
\tag{11}
\]

except at the single exact right tangency. There it checks
\(X_i=X_{i+1}=1\), the endpoint signs and
\(V_i^2,V_{i+1}^2>s^2\ell^2\). Squaring loses no sign because
the center is strictly on the inner side of every edge.

For \(u=(\cos\theta,\sin\theta)\), put
\(d=\|u-(1,0)\|\). The disk and tangent segment imply

\[
h_H(u)\ge1+(a/2)d^2,
\qquad h_H(u)\ge\cos\theta+s|\sin\theta|.
\tag{12}
\]

Take \(\zeta=1/25000\). If \(\zeta\le d\le s/2\), then
\(|\sin\theta|=d\sqrt{1-d^2/4}\ge d/2\) and
\(h_H(u)\ge1+sd/4\ge1+s\zeta/4\).
If \(d\ge s/2\), the disk gives
\(h_H(u)\ge1+as^2/8\). Thus over the entire roll circle,

\[
d\ge\zeta\quad\Longrightarrow\quad
h_H(u)\ge1+\gamma,
\qquad \gamma=\min(s\zeta/4,as^2/8)=1/500000.
\tag{13}
\]

This is a continuous inequality for every proper roll. No angle mesh,
floating optimum or exhaustive enumeration of all possible dual rows is
needed: the 18 proved rows suffice.

## 3. Transfer an arbitrary fit to a nearly frozen roll

Consider a unit-scale fit with \(\|n-n_*\|\le\rho\). By Section 1
choose \(B\in\mathcal I\) and put \(R=QB\), leaving the moving
set unchanged. Then

\[
\|Rn_*-n\|<\delta,
\qquad \|Rn_*-n_*\|<\delta+\rho<2\delta.
\tag{14}
\]

Let \(L\) be the shortest proper rotation taking \(Rn_*\) to
\(n_*\). Its operator distance from identity is the chord distance
between these unit vectors, so \(\|L-I_3\|_{\rm op}<2\delta\).
The proper rotation \(T=LR\) fixes \(n_*\).

We use the frozen probes (6) only as necessary tests of the actual fit;
we do not assume that the entire actual silhouette keeps its edge list.
For any such \(m\), and any actual source vertex \(p\), the fit gives

\[
m\cdot P_nRp+m\cdot t\le h_K(P_nm).
\tag{15}
\]

Since \(m\perp n_*\),
\(\|P_nm-m\|=|m\cdot n|\le\rho\|m\|\).
The body radius is below two, so
\(h_K(P_nm)\le h_K(m)+2\rho\|m\|\) and
\(m\cdot Rp\le m\cdot P_nRp+2\rho\|m\|\).
Replacing \(R\) by \(T=LR\) adds less than
\(4\delta\|m\|\). Combining these estimates yields

\[
m\cdot Tp+m\cdot t
\le h_K(m)+(4\delta+4\rho)\|m\|
<h_K(m)+8\delta\|m\|.
\tag{16}
\]

For each balanced row, multiply (16) by its positive weights and sum.
The actual translation term cancels exactly. Equations (8)--(10) give

\[
X\cos\theta+Y\sin\theta<1+16\delta,
\qquad h_H(u)<1+16\delta.
\tag{17}
\]

But \(\gamma-16\delta=1/2500000>0\). Equations (13) and (17)
therefore imply \(d<\zeta\). For a proper rotation fixing \(n_*\),
\(\|T-I_3\|_{\rm op}=d\), and hence

\[
\|R-I_3\|_{\rm op}<2\delta+\zeta<1.
\tag{18}
\]

If a proper rotation has operator chord \(c\le1\), its principal
angle is \(2\arcsin(c/2)\le2c\). Thus (18) gives

\[
\angle(R)<4\delta+2\zeta<10^{-4},\qquad
10^{-4}-4\delta-2\zeta=49/2500000>0.
\tag{19}
\]

The receiving chord is also below the local parent's \(10^{-6}\).
Its six-contact theorem applies to the actual receiving normal and
actual translation, forcing \(R=I_3\) and \(t=0\).
Consequently \(Q=B^{-1}\in\mathcal I\).

## 4. Scale, the full minimum orbit and handedness

For (1) with arbitrary \(\lambda\ge1\), convexity and \(0\in K\)
give

\[
P_n(QK)+t/\lambda\subseteq\lambda^{-1}P_nK\subseteq P_nK.
\tag{20}
\]

Apply the unit-scale proof to (20): \(Q\in\mathcal I\) and
\(t/\lambda=0\). The original inclusion is then
\(\lambda P_nK\subseteq P_nK\). Positive projected area forces
\(\lambda\le1\), so \(\lambda=1\). Conversely the stated
equality parameters plainly give a fit.

If \(n\) is close to another \(A n_*\), \(A\in\mathcal I\),
rotate the whole fit by \(A^{-1}\). This preserves chord distance,
physical translation and proper rotations, and reduces it to the proved
cap at \(n_*\). The verified orbit contains both normal signs. Finally,
reflecting the whole configuration conjugates \(SO(3)\) to itself and
transfers the result to the other handed form. The moving copy is always
same-handed with the receiving solid.

## Verification, trust and remaining frontier

`certificate.json` contains 18 triples of integer edge/source choices
and five rational constants. The checker regenerates all dual coordinates,
positive weights, denominators and 54 exact balance coordinates; checks
288 convexity determinants, 17 strict disk inequalities, the exact tangent
edge and its span; and verifies all 26 radius-one-half support inequalities,
58 nonminimum facet-localization inequalities and rational margins.
It also regenerates and compares all 30 fields of the global-extremum
audit and the complete local six-contact expected record. Dependency
hashes guard the area and local code, and the named coefficient/model
code transitively. It does not rerun the named-model publication's entire
original facet/model verifier; that published identification remains a
prerequisite.

Normal and optimized Python must reproduce identical complete records,
including rejection of five damaged controls. Signs use rational outward
enclosures at the isolated named root; no floating decision is trusted.
Written support-function, area-localization, full-circle, proper-rotation
and projection-transport arguments remain unformalized. A graph commitment
is not an independent mathematical review.

The current named-solid status is documented in
[Gosain--Grimmer, Section 3.3](https://arxiv.org/html/2509.08190) and
[Zeng, Section 1.2](https://arxiv.org/html/2604.26531). These caps settle
only a receiving-direction subset. A future exact passage must occur
outside it; the rest of the receiving sphere remains an unresolved
construction/obstruction frontier. No failed or finite floating search
proves nonexistence, and no historical-priority claim is made for the
balanced-support principle.
