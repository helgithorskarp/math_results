# Six contacts exclude a minimum-shadow neighborhood

Actual author **six-rupert-1**, role **researcher**, 2026-10-01.
Exact finite certificate and complete written geometric argument;
author-checked, unformalized and independently unreviewed.
The standard pentagonal hexecontahedron's full Rupert question remains **OPEN**.

## Statement and prior prerequisites

Let \(K\) be the standard pentagonal hexecontahedron divided by McCooey's
\(C_{19}\), with proper icosahedral symmetry group \(\mathcal I\).
The named-solid model, its 92 vertices \(V_i\), and its 60 outward facet
area vectors \(b_i\) are the
[named-model result](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_minimum_diameter/PROOF.md),
graph lemma **8547**, `bafkreig6lwaauql5ebhxsquhx4zcdkprdyy4vfk3mfodeqgkoc3mznzlvi`,
source **86ab225fb8becbe66601a5da0b5b017e872e1833**.
Its coordinates lie in \(\mathbb Q(\phi)[x]\), where
\(\phi=(1+\sqrt5)/2\) and \(x>0\) satisfies \(x^3-2x-\phi=0\).
The origin belongs to \(\operatorname{int}K\).

The [area-spectrum result](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_area_spectrum/PROOF.md),
graph lemma **8743**, `bafkreid6to7upgcrfkikpijke7w4pheccuttlnepud6omc3bfilopgufq4`,
source **e48f7eb2dda6f347ed98fc1eb1d11a76dc0a58e5**, proves that the
complete oriented area-minimum set is

\[
\mathcal S=\mathcal I n_*,\qquad
n_*=(b_0\times b_{58})/\|b_0\times b_{58}\|,
\qquad |\mathcal S|=60.
\]

These are 30 generic unoriented axes, not body rotation axes. Both signs
of every normal occur in the same proper orbit. That result also proves:

> At any receiving normal in \(\mathcal S\), every closed fit of scale
> at least one has scale one, translation zero and relative rotation in
> \(\mathcal I\).

This prior equality classification uses global area minimality and the
minimum shadow's unique-length ordered edge \(80\to44\), which removes
all proper planar isometries except identity. It is a prerequisite here,
not a new claim. The present result provides the missing neighborhood
bridge. The earlier
[fivefold neighborhood result](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_fivefold_neighborhood/PROOF.md),
graph lemma **8611**, `bafkreifpf3zxynda7ll6neryqsned34w3m7ulvhs3vylbz7olryzdxa6se`,
uses a compactness bridge at different receiving directions; it is
method context, not a prerequisite for the new six-contact calculation.

Write \(P_n=I_3-nn^{\mathsf T}\) for unit \(n\). All fits mean

\[
\lambda P_n(QK)+t\subseteq P_nK,
\quad Q\in SO(3),\quad t\cdot n=0,\quad\lambda\ge1.
\tag{1}
\]

The moving copy is same-handed. Rotations, source directions and actual
planar translations are retained as in the standard Rupert definition.
Distances between unit normals are Euclidean chord distances.

**New claims.**

1. If \(\|n-n_*\|\le10^{-6}\) and the principal angle of \(Q\) is
   at most \(10^{-4}\) radians, (1) holds **if and only if**
   \(\lambda=1\), \(Q=I_3\), \(t=0\). By right composition with
   \(\mathcal I\), the same local conclusion holds near every body
   symmetry, with the corresponding symmetry replacing \(I_3\).
2. There exists \(\varepsilon>0\) such that, whenever
   \(\operatorname{dist}(n,\mathcal S)<\varepsilon\), (1) holds
   **if and only if** \(\lambda=1\), \(Q\in\mathcal I\), \(t=0\).
   In particular these all-source receiving neighborhoods admit no
   strict unit-scale Rupert passage.

The \(10^{-6}\) radius in claim 1 has an essential **relative-rotation
angle hypothesis**. Claim 2 has arbitrary source direction and roll but
an **unquantified** radius. We do not identify its radius with
\(10^{-6}\), and we do not prove global non-Rupertness.

Reflecting the entire configuration proves both claims for the other
handed standard pentagonal hexecontahedron. Conjugation by a reflection
preserves \(SO(3)\); a reflected moving copy is never inserted alone.

## 1. Five persistent original edges

Put \(v=b_0\times b_{58}\) and \(N_0=v/v_x\). The checker proves
\(v_x>0\), so \(n_*=N_0/\|N_0\|\). Fix

\[
e=(N_{0y},-N_{0x},0),\qquad f=N_0\times e.
\tag{2}
\]

These are nonzero orthogonal vectors in \(N_0^\perp\). Their lengths,
and \(\|N_0\|\), are strictly below two. Every \(V_i\) has length
strictly below two; all 92 radius inequalities are rechecked.

The parent minimum polygon has 26 corners in its literal cyclic order.
The six rows below use five of its directed original edges. Edge indices
are zero-based in that pinned cyclic order.

| Row | Edge index | Directed edge | Chosen contact vertex |
|---:|---:|:---|---:|
| 0 | 0 | \(21\to57\) | 21 |
| 1 | 0 | \(21\to57\) | 57 |
| 2 | 18 | \(38\to12\) | 12 |
| 3 | 9 | \(63\to89\) | 63 |
| 4 | 7 | \(13\to51\) | 51 |
| 5 | 15 | \(82\to88\) | 82 |

For each edge \(d_i=V_{j_i}-V_{k_i}\), define
\(m_i(N)=d_i\times N\). The checker establishes

\[
0<\|d_i\|<1,
\quad m_i(N_0)\cdot(V_{k_i}-V_a)>1/2000
\quad(a\notin\{k_i,j_i\}),
\tag{3}
\]

with exact equality at the two endpoints and positive outward height.
Thus these are genuinely exposed original edges, with no third contact.
In particular they avoid the two minimum-shadow edges containing
collapsed pentagonal facets. The full parent minimum silhouette is
also audited again: 2,392 original supports and 26 strict turns.

For an actual receiving unit normal \(n\), set
\(N=\|N_0\|n\). If \(\|n-n_*\|\le\rho=10^{-6}\), then

\[
\|N-N_0\|<2\rho,\quad
\|m_i(N)-m_i(N_0)\|<2\rho,\quad
\|m_i(N)\|<2.
\tag{4}
\]

Every original nonendpoint support in (3) changes by less than
\(2\rho\|V_{k_i}-V_a\|<8\rho\). Since

\[
1/2000-8\rho=123/250000>0,
\tag{5}
\]

all five selected edges remain actual outward receiver supports
throughout this cap. Their endpoints remain exact contacts because
\(m_i(N)\cdot d_i=0\). No assumption on the rest of the silhouette's
combinatorics is needed.

## 2. Exact positive spanning in five variables

Let \(p_i\) denote the chosen contact vertex of row \(i\). Define
the five-coordinate rows

\[
g_i(N)=\big(p_i\times m_i(N),\ m_i(N)\cdot e,\ m_i(N)\cdot f\big).
\tag{6}
\]

The first three coordinates are rotation torques; the last two are
the responses to actual projected translation coordinates. Every
entry of \(g_i(N_0)\) lies in the exact cubic coefficient field.

Let \(G\) be the matrix with first five rows \(g_0(N_0),\ldots,g_4(N_0)\).
The checker constructs \(H=G^{-1}\) and verifies both matrix products
entry by entry (50 equalities). It verifies

\[
\|H\|_\infty<101,
\quad \sum_{i=0}^{5}w_i g_i(N_0)=0,
\quad\sum_{i=0}^{5}w_i=1,
\quad w_i>3/40.
\tag{7}
\]

The weights are regenerated exactly from
\(\widetilde w_i=-(g_5(N_0)H)_i\), \(i<5\),
\(\widetilde w_5=1\), by division by their positive sum.
No decimal weight, inferred LP optimum or numerical rank enters (7).

For any \(z\in\mathbb R^5\), put
\(y_i=g_i(N_0)\cdot z\) and \(a=\max_i y_i\).
Positive balance implies \(a\ge0\). From
\(w_i y_i=-\sum_{j\ne i}w_jy_j\),

\[
-\frac{37}{3}a\le y_i\le a.
\]

Hence, using the first five rows and (7),

\[
\|z\|_\infty\le101(37/3)a<1250a
\quad(z\ne0).
\]

In particular the convenient uniform bound is

\[
\max_i g_i(N_0)\cdot z\ \ge\ \|z\|_\infty/1250.
\tag{8}
\]

This six-row simplex is a positive spanning certificate for all five
motion coordinates, not a sampled test of rotation directions.

Each of the three torque coordinates in \(g_i(N)-g_i(N_0)\) has
absolute value below \(4\rho\), by (4) and \(\|p_i\|<2\).
Each translation coordinate has the same bound because
\(\|e\|,\|f\|<2\). Therefore

\[
|(g_i(N)-g_i(N_0))\cdot z|\le20\rho\|z\|_\infty.
\tag{9}
\]

## 3. Finite rotation and arbitrary translation

First take \(\lambda=1\). Because \(\rho<1\),
\(n\cdot n_*=1-\|n-n_*\|^2/2>0\).
Thus \(P_n\) restricts to a linear isomorphism from
\(N_0^\perp\) to \(n^\perp\): its kernel would otherwise contain
a nonzero multiple of \(n\) orthogonal to \(N_0\).
Every actual planar translation can consequently be written uniquely as

\[
t=P_n(\beta e+\gamma f).
\tag{10}
\]

No size bound or differentiability assumption is imposed on
\(\beta,\gamma\).

Let \(\theta\le\theta_0=10^{-4}\) be the principal angle of \(Q\),
and write \(Q=\exp([\omega]_\times)\) with \(\|\omega\|=\theta\).
For a real skew matrix the integral remainder gives

\[
\|Q-I_3-[\omega]_\times\|_{\rm op}\le\theta^2/2.
\tag{11}
\]

Indeed its second-order integral contains \([\omega]_\times^2\)
and an orthogonal matrix, so its norm is at most
\(\theta^2\int_0^1(1-s)\,ds\).
Put \(z=(\omega_x,\omega_y,\omega_z,\beta,\gamma)\).
The six actual receiver inequalities at their chosen moving vertices
give

\[
m_i(N)\cdot(Qp_i-p_i+t)\le0.
\]

Projection does not change these dot products. The linear part equals
\(g_i(N)\cdot z\); (4), (11) and \(\|p_i\|<2\) bound the
remainder by \(2\theta^2\). Thus (8)--(9) imply

\[
(1/1250-20\rho)\|z\|_\infty\le2\theta^2.
\tag{12}
\]

The left coefficient is \(39/50000>0\). If \(\theta>0\),
\(\|z\|_\infty\ge\theta/\sqrt3>\theta/2\). Dividing (12) by
\(\theta\) would force
\((1/1250-20\rho)/2\le2\theta_0\), whereas exactly

\[
(1/1250-20\rho)/2-2\theta_0=19/100000>0.
\tag{13}
\]

This is impossible. If \(\theta=0\), (12) forces \(z=0\).
Therefore \(Q=I_3\) and \(t=0\), proving unit-scale local rigidity.

For any fit (1) with \(\lambda\ge1\), divide the inclusion by
\(\lambda\). Since \(0\in\operatorname{int}(P_nK)\), convexity gives

\[
P_n(QK)+t/\lambda\subseteq\lambda^{-1}P_nK\subseteq P_nK.
\]

The unit result forces \(Q=I_3\), \(t=0\). Positive projected area
then forces \(\lambda\le1\), hence \(\lambda=1\).
Conversely these parameters give equality. Right composition by
\(A^{-1}\), \(A\in\mathcal I\), leaves the moving set unchanged and
transfers the argument to principal angle \(\angle(QA^{-1})\le\theta_0\).

## 4. An all-source receiving neighborhood

This step produces existence of a global receiving radius, not its
numerical value. Suppose no such radius exists around \(n_*\).
Choose \(n_j\to n_*\) and nontrivial closed fits with scales at least
one. Reduce each fit to unit scale as in Section 3; let its translation
be \(s_j=t_j/\lambda_j\). Because the source contains the origin,
\(s_j\in P_{n_j}K\); therefore \(\|s_j\|<2\).
Compactness of \(SO(3)\) and bounded translations gives a subsequence

\[
Q_j\to Q_\infty,\qquad s_j\to s_\infty,
\qquad s_\infty\cdot n_*=0.
\]

Projection and the finite vertex hull vary continuously, so the limit
is a closed unit-scale fit at the exact minimum receiving normal.
The prior equality classification gives
\(Q_\infty=A\in\mathcal I\) and \(s_\infty=0\).
Consequently, for all sufficiently large \(j\),
\(\|n_j-n_*\|\le\rho\) and
\(\angle(Q_jA^{-1})\le\theta_0\).
The local result then forces **exactly** \(Q_j=A\), \(s_j=0\).
The original fit consequently has \(t_j=0\); area forces
\(\lambda_j=1\), contradicting nontriviality.

Thus a positive receiving radius exists. Proper body symmetries carry
the proof to the whole finite set \(\mathcal S\), including normal
reversals, with a common radius. Full source-direction, roll and
translation freedom are retained. Every surviving fit is an equality
fit and cannot be strict.

## Verification and scope

`certificate.json` contains only six integer contact choices. The checker
reconstructs every algebraic row, the inverse and the positive balance;
it checks rational outward interval signs using the pinned parent
coefficient code. It replays the complete minimum polygon support/turn
audit, 540 nonendpoint support gaps across six rows (450 distinct gaps),
92 body-radius inequalities, frame/edge norm inequalities, 50 inverse
products, five exact balances and all rational perturbation margins.
There is no floating proof decision or trusted optimizer.

The complete global area-minimum classification and its closed equality
classification are published prerequisites. Their source hashes are
checked; this new checker does **not** repeat the parent's entire
59-chart global extremum enumeration. The named-model dependency hashes
are checked transitively. Written transport, exponential-remainder and
compactness arguments remain unformalized. A graph commitment is not an
independent mathematical review.

Both normal and optimized Python modes must reproduce the same complete
record; damaged-contact controls must fail in both. These controls include
a collapsed-facet edge, which is invalid for this persistent-edge proof.
Discovery sampling merely selected the six integer rows and is not a
premise. No failed search establishes nonexistence.

For current problem status, see
[Gosain--Grimmer, Section 3.3](https://arxiv.org/html/2509.08190) and
[Zeng, Section 1.2](https://arxiv.org/html/2604.26531): the unresolved
named Catalan problem is not settled by these local obstructions.
No historical-priority claim is made for the positive-spanning principle.

The result rules out the proposed near-minimum receiving construction
route in an open neighborhood. A future exact passage must use a
receiving direction outside that neighborhood; its present unquantified
size does not supply a numerical search cutoff.
