# Explicit first-power separation on the new closed annulus

Actual author **six-reviewer-1**, role **independent mathematical reviewer**, 2026-10-04. This is an ordinary, unformalized refinement of the independently audited LEMMA10216/0. Its only computational inputs are the exact strict inequalities proved by the complete cover and energy-shell verification in [REVIEW.md](REVIEW.md). The proof on the new annulus does not invoke an older numerical margin.

For every degree-nine polynomial with all original zeros in the closed unit disk and every marked zero with \(5/8\le|a|\le13/20\), counting all eight critical multiplicities and interpreting a zero denominator as infinity,

\[
\sum_{j=1}^8\frac1{|a-\zeta_j|}>8+\varepsilon,
\qquad\varepsilon=2^{-22}=1/4194304.
\tag{1}
\]

Use the definitions \(r_j,F,E,u,O_a,J_a\) from the review. The exact shell maximum \(M\) in [EXPECTED.json](EXPECTED.json) and the two certificate thresholds satisfy

\[
M<1-64\varepsilon,
\quad 1-64\varepsilon>19999/20000,
\quad 1+578\varepsilon<4097/4096.
\tag{2}
\]

These are exact rational checks in the independent source. No displayed decimal approximation is an input.

## Floor-preserving clipping and channel continuity

Fix a real \(a\in[5/8,13/20]\), and set \(m=1/(1+a)\). Suppose \(r_j\ge m\) and \(F=8+\delta\) for \(0<\delta\le1\). There exists a common radial threshold \(\tau\ge0\) such that

\[
r'_j=\max(m,r_j-\tau),\qquad\sum r'_j=8.
\tag{3}
\]

Indeed, the continuous nonincreasing sum starts above eight and, at any \(\tau\ge\max_j(r_j-m)\), equals \(8m<8\). Define \(q'_j=(r'_j/r_j)q_j\). No entry is zero and all directions are retained. Then

\[
r'_j\ge1/(1+a),\quad F'=8,
\qquad\sum|q_j-q'_j|=\sum(r_j-r'_j)=\delta.
\tag{4}
\]

On the straight segment from \(q'\) to \(q\), every intermediate radius is between its two endpoint radii and the total is at most \(8+\delta\le9\). For each coordinate derivative, triangle inequality and AM–GM on the other seven factors give, for \(0\le t\le1\),

\[
\prod_{k\ne j}|a+(1-a^2)tq_k|
\le\left[a+(1-a^2)t\frac{\sum_{k\ne j}|q_k|}{7}\right]^7<2^7,
\]
\[
\prod_{k\ne j}|1-atq_k|
\le\left[1+at\frac{\sum_{k\ne j}|q_k|}{7}\right]^7<2^7,
\]

because \(a\le13/20\), \(1-a^2\le39/64\), and

\[
13/20+(39/64)(9/7)<2,
\qquad 1+(13/20)(9/7)<2.
\]

Integrate the coordinate derivatives along this segment and then over \(t\). Since \(1-a^2\le1\) and \(a\le1\), the full complex polynomial channels satisfy

\[
|J_a(q)-J_a(q')|\le2^7\delta\int_0^1t\,dt=64\delta,
\]
\[
|O_a(q)-O_a(q')|\le9\cdot2^7\delta\int_0^1t\,dt=576\delta.
\tag{5}
\]

Repeated entries, vanishing individual channel factors, and arbitrary complex phases cause no singularity: the channels and their coordinate derivatives are polynomials. The clipped tuple need not arise from any original polynomial, and no such feasibility claim is used.

## Applying all three exact margins

Take an actual original polynomial and rotate its marked root to real \(a\). A critical collision gives infinity. Otherwise \(q_j=(a-\zeta_j)^{-1}\) is finite and satisfies the full radius floor by Gauss–Lucas. The exact actual-root communication identities give

\[
|J_a(q)|\ge1,
\qquad |O_a(q)|\le\prod r_j\le(F/8)^8.
\tag{6}
\]

The audited theorem already excludes \(F\le8\). If \(F\le8+\varepsilon\), write \(\delta=F-8,\ 0<\delta\le\varepsilon\) and use \(3\). Equations \(5\) and \(6\) give

\[
|J_a(q')|\ge1-64\delta\ge1-64\varepsilon.
\tag{7}
\]

If \(E(q')\ge23/5\), the complete seventy-cell energy bound, applicable to every radius-floor tuple with \(F'=8\), gives \(|J_a(q')|\le M<1-64\varepsilon\), a contradiction. Hence \(E(q')<23/5\). The exact relation \(E'=T'+16-16u'\), with \(T'\ge0\), yields

\[
u'\ge1-E'/16>57/80>51/80,
\quad |\mu'|\le1,
\quad F'=8\ge37/5.
\]

The clipped tuple therefore satisfies the complete closed dichotomy. Its polar alternative \(|J_a(q')|<19999/20000\) contradicts \(2\) and \(7\). Thus \(|O_a(q')|>4097/4096\).

For \(0\le\delta\le1\), convexity of \(x\mapsto(1+x/8)^8\) on that interval gives

\[
(1+\delta/8)^8\le1+\delta[(9/8)^8-1]<1+2\delta,
\]

where the weak bound \(\le1+2\delta\) also covers \(delta=0\). Consequently \(5\) and \(6\) imply

\[
|O_a(q')|\le1+(2+576)\delta
\le1+578\varepsilon<4097/4096,
\]

a contradiction. This proves \(1\) on both marked endpoints and every interior modulus. Multiplicities and original closed-disk boundaries are exactly those in \(6\).

## Qualitative gap on the entire closed marked disk

Relative to the lower-domain theorem LEMMA10170/0, the complete audited actual theorem also implies the existence of some \(eta>0\) such that the first-power sum is at least \(8+\eta\) whenever the marked modulus is at most \(13/20\). This is a qualitative consequence, not a claim that \(eta=2^{-22}\) works on the lower disk.

To prove it, take the compact space of all nine ordered original zeros in the closed unit disk with a designated first root of modulus at most \(13/20\), together with eight ordered critical roots in the closed unit disk whose monic derivative polynomial equals the derivative of the original product divided by nine. Coefficient equality defines a closed condition. The actual critical-root fiber is nonempty by polynomial factorization and Gauss–Lucas. The first-power sum is lower semicontinuous with value infinity at collisions, since each extended reciprocal distance is lower semicontinuous. It attains its minimum on this compact space. Every point has value strictly greater than eight by the confirmed theorem; the minimum is therefore strictly greater than eight. There is a finite example, such as \(p(z)=z(z-1)^8\) with marked root zero, so the minimum is finite if that detail is needed.

The compactness principle is classical and the lower-radius review already uses it. Only its application to the enlarged checked domain is asserted here; historical priority is not inferred.
