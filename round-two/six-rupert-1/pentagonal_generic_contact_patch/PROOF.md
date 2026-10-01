# Six-contact rigidity on a generic receiving patch

**six-rupert-1, researcher; 2026-10-01.** Author-checked exact finite
certificate and written continuum argument. Unformalized; no independent
review is claimed. The standard pentagonal hexecontahedron's full Rupert
property remains **OPEN**.

## 1. Exact statement and the named solid

Use the proper icosahedral group \(\mathcal I\) of order sixty, the six
icosahedral vertex-line representatives \(W\), and the twenty dodecahedral
points \(\mathcal D\) from the
[named-model proof](../pentagonal_minimum_diameter/PROOF.md), source
`86ab225fb8becbe66601a5da0b5b017e872e1833`, graph
`bafkreig6lwaauql5ebhxsquhx4zcdkprdyy4vfk3mfodeqgkoc3mznzlvi`.
Define the 92-generator hull

\[
 K_p=\operatorname{conv}\big(\mathcal I(-u,-\rho,-1)
       \ \cup\ a(\pm W)\ \cup\ \tau\mathcal D\big),
 \qquad p=(u,\rho,a,\tau)\in\mathcal B,
 \tag{1}
\]

where the **closed** rational parameter box is

| Parameter | Lower endpoint | Upper endpoint |
|---|---:|---:|
| \(u\) | 0.0919831 | 0.0919833 |
| \(\rho\) | 0.1041858 | 0.1041860 |
| \(a\) | 0.5565538 | 0.5565540 |
| \(\tau\) | 0.5828994 | 0.5828997 |

Each decimal in the table means the exact terminating rational. The cited
model identification places the standard pentagonal hexecontahedron,
normalized by its positive coordinate constant \(C_{19}\), strictly inside
this box. The checker re-isolates its positive algebraic root and verifies
that inclusion. The family statement concerns the point hulls (1); it
does not require all generators to remain vertices or all nearby hulls to
have the same facet lattice.

For a nonzero vector \(r\), write
\(\pi_r=I-rr^T/(r\cdot r)\). Put

\[
 r=(1+s,2+z,3),\qquad |s|,|z|\le\frac1{1000},
 \qquad
 R(c)=(I+[c]_\times)(I-[c]_\times)^{-1},
 \quad [c]_\times v=c\times v.
 \tag{2}
\]

**Theorem.** Let \(p\in\mathcal B\), \(g,G\in\mathcal I\), and
\(n=\pm gr/\|r\|\). Suppose \(Q\in SO(3)\) satisfies

\[
 g^{-1}Q=R(c)G,\qquad \|c\|_\infty\le\frac1{10^6}.
 \tag{3}
\]

For any \(\lambda\ge1\) and **arbitrary actual translation**
\(b\in n^\perp\), the closed containment

\[
 \lambda\pi_n(QK_p)+b\ \subseteq\ \pi_n(K_p)
 \tag{4}
\]

holds if and only if \(c=0\), \(\lambda=1\), and \(b=0\).
In this case \(Q=gG\) is a proper body symmetry and the two shadows agree.

The motion hypothesis (3) is essential. This is a two-dimensional
receiving patch, together with its proper group images and the equivalent
negative normals, with **conditional** neighborhoods of the body
symmetries. It is not an exclusion for all sources at these receivers, an
all-normal local rigidity theorem, or a non-Rupert proof. Applying a fixed
orthogonal reflection to the whole configuration gives the other handed
solid. Both copies retain the same handedness; reflecting only the moving
copy is not an allowed motion.

## 2. Six original supports; no complete-hull assumption

The [certificate](certificate.json) identifies six contacts. Indices refer
to the deterministic original-generator order constructed by the pinned
[prerequisite source](../pentagonal_minimum_diameter/verify.py), rather
than the order of a floating-point model file. A contact \((a,b,v,k)\)
means

\[
 m_i=2^k(P_b-P_a)\times r,\qquad
 v\in\{a,b\},\qquad h_i=m_i\cdot P_v.
 \tag{5}
\]

| Row | \(a\) | \(b\) | \(v\) | \(k\) |
|---|---:|---:|---:|---:|
| 0 | 38 | 19 | 38 | 1 |
| 1 | 67 | 43 | 43 | -1 |
| 2 | 46 | 78 | 46 | 0 |
| 3 | 71 | 25 | 71 | -1 |
| 4 | 25 | 36 | 36 | 1 |
| 5 | 44 | 73 | 73 | 0 |

For every \(p\in\mathcal B\) and every \(r\) in (2),
\(m_i\cdot r=0\) and \(m_i\cdot(P_b-P_a)=0\) identically by the cross
product. At the other ninety original points the checker verifies

\[
 m_i\cdot(P_v-P_j)>\frac9{1000},\qquad
 h_i>0.\tag{6}
\]

These are **540 strict support comparisons** over the entire real boxes.
Consequently each \(m_i\cdot x\le h_i\) is a genuine receiving support
halfspace, with the selected source point itself a support contact.
Completeness of a receiver cycle is unnecessary: (4) must satisfy these
six valid halfspaces. The checker also verifies
\(\|P_j\|<2\) for all originals and \(\|m_i\|^2<2\), so in particular
\(\|m_i\|<2\).

All points are linear forms in \((1,u,\rho,a,\tau)\) with coefficients
in the ordered field \(\mathbb Q(\phi)\),
\(\phi=(1+\sqrt5)/2\). Rational interval arithmetic encloses the entire
parameter box and receiving rectangle, including their boundaries.
Every endpoint calculation uses integers and fractions. The exact
cross-product identities account for the two zero endpoint gaps; no
floating contact tolerance is used.

## 3. A positive stress and five independent motion coordinates

Let \(r_0=(1,2,3)\), and fix

\[
 E=(0,3,-2),\qquad F=(-13,2,3),\qquad E\times F=13r_0.
 \tag{7}
\]

The vectors \(\pi_rE,\pi_rF\) span the actual receiving plane:
\(r\cdot r_0=14+s+2z>0\), so their projected oriented area is
nonzero. Hence every physical translation has a unique representation
\(b=\pi_r(\alpha E+\beta F)\). Since \(m_i\perp r\), its support
contribution is exactly \(m_i\cdot b=\alpha m_i\cdot E+\beta m_i\cdot F\).

Define the five-component row

\[
 f_i=\big(P_v\times m_i,\ m_i\cdot E,\ m_i\cdot F\big).
 \tag{8}
\]

Let \(A\) have columns \(f_0,\ldots,f_4\). The checker proves uniformly
that \(A\) is invertible and that there are real weights satisfying

\[
 w_i>\frac1{60},\quad \sum_{i=0}^5w_if_i=0,\quad
 W:=\sum_iw_i<\frac75,\quad
 H:=\sum_iw_ih_i>\frac35,
 \qquad \|A^{-1}\|_\infty<21.
 \tag{9}
\]

Here and below the matrix norm is the induced infinity norm. No numerical
LP equilibrium is used as a premise. To obtain (9), the checker takes
the rational midpoint \(p_0\) of \(\mathcal B\) and \(r_0\). It forms
the exact \(A_0\) over \(\mathbb Q(\phi)\), verifies both inverse products,
fixes the certificate's positive rational \(w_5^0\), and solves
\(A_0(w_0^0,\ldots,w_4^0)^T=-w_5^0f_5^0\). All six reference weights
are positive and all five reference equilibrium components are exactly
zero.

Writing \(\epsilon_A\) for the verified matrix error bound and
\(L_0\) for its reference inverse bound, the rational interval checks give

\[
 L_0<\frac{21}{2},\qquad L_0\epsilon_A<\frac14.
 \tag{10}
\]

Thus the Neumann-series criterion makes \(A\) invertible throughout the
boxes and gives \(\|A^{-1}\|_\infty<2L_0<21\). Set
\(e=\sum_iw_i^0f_i\), keep \(w_5=w_5^0\), and define the other weights by

\[
 (w_0,\ldots,w_4)^T=(w_0^0,\ldots,w_4^0)^T-A^{-1}e.
 \tag{11}
\]

This enforces the five equilibrium identities exactly. The checker bounds
the change in each of these five weights by less than \(9/125\), then
verifies all the stronger bounds in (9). This construction covers real
parameters continuously; it is not a set of sampled poses. The force
also balances in three dimensions: \(\sum_iw_im_i\) is perpendicular
to \(E,F,r\); (7) and \(r\cdot r_0>0\) force it to vanish. The first
three components of (8) balance torque.

In particular, the six rows positively span \(\mathbb R^5\). The linear
inequalities \(f_i\cdot U+\sigma h_i\le0\) with \(\sigma\ge0\)
force \(\sigma=0\) by the positive stress, then all six row values
are zero, and finally \(U=0\) by the independent five columns. This
is exact infinitesimal rigidity. The following argument closes the
possible gap between first variation and finite proper motions.

## 4. Cayley remainder, arbitrary scale, and actual translation

First take \(g=G=I\). Write \(C=[c]_\times\) and \(d=\|c\|_2^2\).
The exact proper rotation is

\[
 R(c)=I+\frac{2(C+C^2)}{1+d}.
 \tag{12}
\]

For \(\|c\|_2\le1/2\), the induced Euclidean norm satisfies

\[
 \|R(c)-I-2C\|_2
 \le\frac{2(d+d\sqrt d)}{1+d}\le3d.
 \tag{13}
\]

By the point and support-normal bounds in Section 2, write
\(\varepsilon_i=m_i\cdot(R(c)-I-2C)P_v\); then
\(|\varepsilon_i|<12d\le16d\). Put

\[
 \sigma=\lambda-1\ge0,\qquad
 U=(2\lambda c,\alpha,\beta)\in\mathbb R^5.
\]

Applying the actual containment (4) to each original contact gives

\[
 f_i\cdot U+\sigma h_i+\lambda\varepsilon_i\le0.
 \tag{14}
\]

The positive equilibrium cancels rotation and the actual translation in
the weighted sum. Therefore

\[
 (\lambda-1)H\le16\lambda Wd.
 \tag{15}
\]

Under \(\|c\|_\infty\le10^{-6}\), we have \(d\le3\cdot10^{-12}\)
and \(\|c\|_2<1/2\). The bounds (9) give \(16Wd<H/2\), so (15)
implies \(\lambda\le2\). No upper bound on scale was assumed.

Equation (14) now gives \(f_i\cdot U\le32d\). Using
\(\sum_iw_i(f_i\cdot U)=0\), \(w_i>1/60\) and \(W<7/5\), every
row value is also greater than \(-2688d\). Thus

\[
 |f_i\cdot U|\le2700d.\tag{16}
\]

For the first five rows, their value vector is \(A^TU\). Since a
five-by-five matrix satisfies
\(\|A^{-T}\|_\infty\le5\|A^{-1}\|_\infty<105\), (16) yields

\[
 2\|c\|_\infty\le\|U\|_\infty
 \le105\cdot2700d
 \le315\cdot2700\|c\|_\infty^2.
 \tag{17}
\]

If \(c\ne0\), division forces \(1\le425250\|c\|_\infty\le1701/4000<1\),
a contradiction. Hence \(c=0\). Equation (15) then forces \(\lambda=1\).
The six row inequalities and their positive zero sum force every row
value to vanish; invertibility gives \(\alpha=\beta=0\), hence the
actual translation \(b=0\). No small-translation assumption was made.

For general \(g,G\), rotate the entire configuration by \(g^{-1}\).
The receiving plane becomes \(r^\perp\), \(g^{-1}K_p=K_p\), and
\(g^{-1}QK_p=R(c)GK_p=R(c)K_p\). The preceding proof applies. The
equivalent negative normal gives the same orthogonal projection. The
converse follows from body symmetry. Orthogonal conjugation of all data
also proves the stated whole-configuration mirror version.

## 5. Provenance and use

This supplies an explicit generic receiving patch and a four-parameter
uniform contact certificate for this named family. It can remove the
specified body-motion neighborhoods from a future exhaustive domain
cover; no complete cover or global exclusion is supplied here.

Positive contact stresses, Farkas-style balancing, Neumann perturbation
bounds and Cayley control are standard mechanisms; no general-method
priority is claimed. The earlier
[minimum-receiver contact lemma](../pentagonal_minimum_contact_cap/PROOF.md),
source `6fe2877d56118527bb70138d413e5d415398708f`, graph
`bafkreic4dfjxkb4qyodxbfgoygz2xac7ib7v77rx7q2ys6easvcvbn3w3m`,
concerns a different receiving neighborhood for the single named body.
The present six supports and parameter-uniform bounds are reconstructed
here; that lemma's contacts and constants are not premises. The
[explicit all-source minimum-shadow caps](../pentagonal_effective_minimum_cap/PROOF.md),
source `42f00e8d348c548db68d8507c7f2b578d06b2e11`, graph
`bafkreibgak5dssow3qpsowgcpxtr7dqvnrxlwj52wx3ncqajqtzvvzrbci`,
retain their separate receiving hypotheses. The present statement does
not replace their all-source quantifier. The
[J74 nonlocal arc proof](../../six-rupert-2/nonlocal_arc_wrench/PROOF.md),
by six-rupert-2, source `03e077716c0a21496133189eee3ba5444cb77555`, graph
`bafkreihs43shk7p73kl327xg73lvh32elxxl5f6qg5o64mzeayyqkgoprm`,
is complementary contact/Cayley context for a different body. Its
mirror motions, data and constants do not transfer to this chiral solid.
The later [J74 two-dimensional patch](../../six-rupert-2/nonlocal_receiving_patch/PROOF.md),
source `5e1e16fecbe2514c930d8cba069a62cad1abb578`, graph
`bafkreicz5kllfqaamirgfwd55t24hfzs6ysxxnj572pfp3o4cbd34w2clq`,
also uses a five-weight repair. It is cited as methodological context;
its original-body model, constants, full receiver cycle and reference
motions are not premises for this certificate.

Current primary status was refreshed on 2026-10-01:
[Gosain--Grimmer, Section 3.3/Table 3](https://arxiv.org/html/2509.08190)
retains both pentagonal and deltoidal hexecontahedra among the unresolved
Catalan cases; its unsuccessful numerical searches are not exclusions.
[Zeng, Section 1.2](https://arxiv.org/html/2604.26531) reports eleven of
thirteen Catalan solids known Rupert and keeps the rhombicosidodecahedron
conjecture open. The universal-polyhedron conjecture is superseded by the
[Steininger--Yurkevich Noperthedron](https://arxiv.org/abs/2508.18475).
None of these facts settles this target.

The exact checker trusts Python integer/fraction arithmetic, the pinned
\(\mathbb Q(\phi)\) and rational-interval implementation, and the cited
named-model identification. The implication from its finite checks to
the continuum statement is the written argument above, which is not
proof-assistant formalized. The selection experiment is not a trusted
input, and no independent reviewer verdict is asserted.
