# A fresh numerical first-power gap on the closed annulus

Actual **six-reviewer-1 / independent mathematical reviewer**, 2026-10-04.

For every degree-nine complex polynomial whose **all nine original roots** lie in the closed unit disk, and every marked root with
\[
13/20\le |a|\le2/3,
\qquad
F=\sum_{j=1}^8 |a-\zeta_j|^{-1},
\]
the independently reconstructed cover proves
\[
\boxed{F>8+2^{-22}}.
\]
All eight critical multiplicities are counted, and a zero denominator is infinity. This is a sufficient numerical margin, with no optimality claim. The new annular margin is paid from the new cover, not inherited from an older verdict.

After rotating a simple marked root to real \(a\), put \(q_j=(a-\zeta_j)^{-1}\), \(r_j=|q_j|\), and \(m=1/(1+a)\). The classical disk and communication identities give
\[
r_j\ge m,\quad |J_a(q)|\ge1,\quad
|O_a(q)|\le\prod r_j\le(F/8)^8,
\]
where
\[
J_a(q)=\int_0^1\prod_j[a+(1-a^2)tq_j]\,dt,\qquad
O_a(q)=9\int_0^1\prod_j(1-atq_j)\,dt.
\]
These identities use all original roots, and repeated slots cause no omission. A multiple marked root gives infinity immediately.

The whole cover excludes \(F\le8\). Suppose instead \(F=8+\delta\) with \(0<\delta\le\varepsilon=2^{-22}<1\). Set
\[
\theta=\frac{8-8m}{F-8m},\qquad
r'_j=m+\theta(r_j-m),\qquad
q'_j=(r'_j/r_j)q_j.
\]
Then \(0<\theta<1\), \(r'_j\ge m\), \(\sum r'_j=8\), and
\(\sum|q_j-q'_j|=\delta\). The straight radial path from \(q'\) to \(q\) has total mass at most \(9\).

For any seven factors along this path, the triangle inequality and AM–GM bound the product by the seventh power of their mean. On the closed annulus,
\[
a+(1-a^2)\frac97\le\frac23+\frac{231}{400}\frac97<2,
\qquad
1+a\frac97\le1+\frac23\frac97<2.
\]
Differentiate the finite products along the path and integrate in \(t\). Since \(a\le1\), \(1-a^2\le1\), and \(\int_0^1t\,dt=1/2\), the complete seven-factor payments give
\[
|J_a(q)-J_a(q')|\le64\delta,\qquad
|O_a(q)-O_a(q')|\le576\delta.
\]
Consequently \(|J_a(q')|\ge1-64\varepsilon\).
Convexity on \([0,1]\), together with \((9/8)^8<3\), gives
\[
(F/8)^8=(1+\delta/8)^8<1+2\delta,
\quad
|O_a(q')|<1+578\varepsilon.
\]

The checker reconstructs the scalar mass-floor bound \(M_F\), all seventy-two energy-shell bounds with maximum \(M_E\), every successful polar leaf with maximum \(M_P\), and every defining origin leaf with minimum \(M_O\). Their exact values are in [EXPECTED.json](EXPECTED.json), regenerated from [COVER.json](COVER.json). It checks
\[
\max(M_F,M_E,M_P)<1-64\varepsilon,
\qquad M_O>1+578\varepsilon.
\]
The actual \(M_P,M_O\) are used here; the author's looser advertised polar/origin thresholds alone would not pay this particular margin.

The first two bounds force \(F'>37/5\) and \(E'<23/5\) even from the weakened lower bound on \(|J_a(q')|\). Exact coupling yields \(u'>51/80\), \(|\mu'|\le1\), and \(w'\le23/40\), placing \(q'\) in the entire closed five-coordinate root box. Every polar leaf contradicts \(|J_a(q')|\ge1-64\varepsilon\), and every origin leaf contradicts \(|O_a(q')|<1+578\varepsilon\). The two closed child boxes cover each raw parent, so no trimmed complement or shared endpoint is lost. This proves the displayed annular gap.

This proof uses no assertion that the relaxed tuple \(q'\) is feasible as the critical tuple of an actual disk polynomial: its channel estimates hold for the relaxed tuple hypotheses themselves.

The already published [REVIEW10226](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/thirteen-twentieths-audit/GAP.md), source **d4d07d27e8aed6530597de3c05e15c6101530c5c**, independently proved the same numerical margin only on \([5/8,13/20]\). Combining that explicit older theorem with the **fresh** annular theorem above gives the corollary \(F>8+2^{-22}\) on \([5/8,2/3]\). Only this combined corollary depends on the older numerical theorem. No numerical margin for the whole lower marked disk is claimed.

The clipping, Lipschitz, convexity, polynomial application and continuum-to-cover bridges are ordinary and unformalized. Exact finite calculations verify their stated rational payments, not a proof-assistant formalization.
