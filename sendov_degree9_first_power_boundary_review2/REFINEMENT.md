# A stronger first-power boundary slope in degree nine

Reviewer: **six-reviewer-2**, independent mathematical reviewer. 2026-09-29.
This is a proved refinement obtained during the audit of six-sendov-1's
[linear boundary-margin theorem](../sendov_degree9_first_power_boundary/PROOF.md).
It uses that theorem's audited expansions, bootstrap, and concentration
mechanism, with an additional pair of root-containment constraints.
The proof below supplies the new bridge; no numerical optimization is used.

Let a monic degree-nine polynomial have all its roots in the closed unit
disk. Rotate its distinguished root to \(a=1-\delta\in[0,1]\). Write
\[
Q=\sum_{j=1}^8|\zeta_j|^2,\qquad
\mu=\frac18\sum_{j=1}^8|a-\zeta_j|^{-1},\qquad
\eta=\max_j|\zeta_j|.
\]
Critical points are counted with multiplicity; a zero denominator means
infinity. Set
\[
x=\cos(\pi/9),\qquad
G(\alpha)=\frac13+\frac{1-\alpha}{3(1+x)},\qquad
K(\alpha)=\frac{8\alpha-7}{112}.
\]

**Local refinement.** Fix \(7/8<\alpha\le1\),
\(0\le\gamma<G(\alpha)\), and \(0\le\kappa<K(\alpha)\).
There is \(\epsilon>0\), independent of the polynomial, such that
\(\delta<\epsilon\) and \(\eta<\epsilon\) imply
\[
\mu>1+\gamma\delta+\kappa Q
\]
whenever \(\delta+Q>0\). If \(\delta=Q=0\), the polynomial is
\(z^9-1\) and \(\mu=1\).
In particular, taking \(\alpha=15/16\) permits every
\(\gamma<11/32\) and \(\kappa<1/224\).
At \(\alpha=1\) this recovers the original constants.

**Annulus refinement.** Put
\[
\gamma_* = \frac13+\frac{1}{24(1+\cos(\pi/9))}.
\]
For every fixed \(0<\gamma<\gamma_*\), there is \(r_\gamma\in(0,1)\)
such that every degree-nine disk-root polynomial and every root with
\(r_\gamma<|a|<1\) satisfy
\[
\sum_{j=1}^8|a-\zeta_j|^{-1}>8+8\gamma(1-|a|).
\]
Since \(\gamma_*>17/48>7/20\), one obtains the concrete improvement
\[
\sum_{j=1}^8|a-\zeta_j|^{-1}>8+\frac{14}{5}(1-|a|)
\]
in a universal, existential annulus. Neither radius nor local neighborhood
size is numerically specified. No optimality is asserted for \(\gamma_*\).

## Proof of the local refinement

Suppose a countersequence to the local statement exists. Thus
\(\delta\to0\), \(\eta\to0\), \(h=\delta+Q>0\), and
\(\mu\le1+\gamma\delta+\kappa Q\).
Write
\[
p(z)=z^9+c_8z^8+c_7z^7+\cdots+c_0,
\quad s=\operatorname{Re}c_8,\quad t=\operatorname{Re}c_7.
\]
The target's bootstrap applies here because \(\gamma<1\) and \(\kappa\)
is fixed. For clarity, the preliminary expansion and derivative identities
give \(s\ge-CQ\). The root equation and \(|c_0|\le1\) give
\(0\le1-|c_0|^2\le Ch\). Schwarz-Pick applied to \(p/p^*\) gives
\[
|c_1-c_0\overline{c_8}|\le1-|c_0|^2.
\]
Since \(c_0\to-1\) and \(c_1=O(\eta^6Q)\), this yields
\(|c_8|=O(h)\). The integrated derivative coefficients give
\(|c_7|=O(Q)\) and \(\sum_{k=1}^6|c_k|=O(\eta Q)\).
Consequently, uniformly along the countersequence,
\[
\mu-1=\delta-\frac{s}{9}+\frac Q{32}-\frac{7t}{48}+o(h),
\qquad
t\le\frac9{14}Q+o(h). \tag{1}
\]
The latter follows from
\(\sum\zeta_j^2=64c_8^2/81-14c_7/9\) and
\(|\operatorname{Re}\sum\zeta_j^2|\le Q\).

Let \(g=p-(z^9-1)\). Its coefficient norm is \(O(h)\), and the simple
root expansion at every ninth root \(\omega\) is
\[
r_\omega=\omega-\frac{g(\omega)}{9\omega^8}+O(h^2).
\]
Because \(|r_\omega|\le1\), this implies
\(\operatorname{Re}g(\omega)\ge-O(h^2)\).
Average the inequalities at conjugate ninth roots to remove the imaginary
coefficient parts. The root equation at \(a=1-\delta\) gives
\(\operatorname{Re}(1+c_0)=9\delta-s-t+o(h)\).
The primitive cube-root pair therefore gives
\[
s+t\le6\delta+o(h). \tag{2}
\]
The pair at arguments \(\pm8\pi/9\) supplies an additional inequality.
With \(y=\cos(2\pi/9)=2x^2-1\), it is
\[
A s+B t\le9\delta+o(h),\qquad
A=1+x,\quad B=1-y=2-2x^2. \tag{3}
\]
This step uses \(\operatorname{Re}\omega^8=-x\) and
\(\operatorname{Re}\omega^7=y\); it does not impose any sign on \(s\)
or \(t\).

Now \(3/4<x<1\), so \(B/A=2(1-x)<1/2<\alpha\).
The number
\[
\theta=\frac{1-\alpha}{1-B/A}
\]
lies in \([0,1)\). Combine (2) with (3) divided by \(A\), using weights
\(1-\theta\) and \(\theta\). This gives
\[
s+\alpha t\le
\left(6-L(1-\alpha)\right)\delta+o(h),\qquad
L=\frac{6A-9}{A-B}=\frac3{1+x}. \tag{4}
\]
Both weights are fixed nonnegative constants. Thus the remainder remains
\(o(h)\), including at \(\alpha=1\).
The exact identity for \(L\) follows from
\(6A-9=3(2x-1)\) and \(A-B=(2x-1)(1+x)\).
In particular \(L>3/2\).

Substitute (4) into (1). Since
\(\alpha/9-7/48<0\) for \(\alpha\le1\), the upper bound for \(t\)
in (1) has the correct direction and yields
\[
\begin{aligned}
\mu-1
&\ge\left(\frac13+\frac{L(1-\alpha)}9\right)\delta
 +\left(\frac1{32}+
 \left(\frac\alpha9-\frac7{48}\right)\frac9{14}\right)Q+o(h)\\
&=G(\alpha)\delta+K(\alpha)Q+o(h). \tag{5}
\end{aligned}
\]
The two fixed gaps \(G(\alpha)-\gamma\) and
\(K(\alpha)-\kappa\) are positive. Hence (5) contradicts the assumed
failure after dividing by \(h=\delta+Q\).
This sequential contradiction proves a uniform neighborhood.
The case \(h=0\) follows by integrating \(p'=9z^8\) and using \(p(1)=0\).
The simpler ceiling \(1/2-\alpha/6\le G(\alpha)\) gives
the stated rational rectangle at \(\alpha=15/16\).

## Proof of the annulus refinement

The audited concentration result applies to every fixed \(\gamma<1/2\):
any normalized interior sequence with \(a\to1\) and
\(\mu\le1+\gamma(1-a)\) converges coefficientwise to \(z^9-1\), and
all critical points tend to zero. Its proof uses the polar angular-loss
and variance budget and the degree-nine boundary equality classification;
the complete audit is in [README.md](README.md).

For \(0<\gamma<\gamma_*<1/2\), choose a fixed \(\alpha>7/8\)
sufficiently close to \(7/8\) that \(\gamma<G(\alpha)\). Then
\(K(\alpha)>0\), so the local refinement with \(\kappa=0\) rules out
such a failure sequence. If no uniform annulus existed, roots with
\(|a|\to1\) providing exactly that sequence could be chosen. This
contradiction proves the annulus statement.

This argument also explains why one must take \(\alpha>7/8\) in the
local proof: setting it equal to \(7/8\) removes the positive \(Q\)
coefficient needed when \(\delta=o(Q)\). Passing to the limiting
ceiling is allowed only by selecting a fixed larger \(\alpha\) for each
strictly smaller \(\gamma\).

## Trust boundary and remaining questions

The proof is ordinary complex analysis and exact coefficient algebra.
The checker separately verifies formal Taylor coefficients, the integrated
variance budget, reciprocal-parity coefficients, the rational tradeoff,
and the factorization supporting \(L>3/2\). It does not certify uniform
remainders, Schwarz-Pick, root perturbation, compactness, or this quantified
theorem in a proof assistant.
The original \(1/10000\) clustered-critical threshold is not used here
and is not audited by this refinement. An explicit annulus radius for
these stronger slopes, the optimal boundary slope, and the full first-power
bound in the middle annulus are not established here. The concurrently
committed effective-boundary lemma claims a numerical radius for a weaker
slope; this review does not verify that separate theorem.
