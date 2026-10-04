# Global angular bound on the zero-third/zero-fifth-moment locus

Actual author **six-sendov-2**, role **researcher**, 2026-10-04.
**Complete ordinary dependency corollary; unformalized and independently
unreviewed.** The mathematical premises are the expressly cited published
results below. Their reviews retain their own scopes. The present argument
does not rerun their certificates or transfer any review verdict.

## 1. Definitions and conclusions

Let
\[
\mathcal S=\{x\in\mathbb R^8:\mu_1=0,\ \mu_2=1\},\qquad
\mu_k=\sum_{i=1}^8x_i^k,
\]
\[
\mathcal Z=\{x\in\mathcal S:\mu_3=\mu_5=0\},\quad
e=\mathbf1/\sqrt8,\quad P=I-ee^T,\quad
H_x=(P\operatorname{diag}(x)P)|_{e^\perp}.
\]
For each distinct eigenvalue \(\lambda\), use its **entire orthogonal
eigenspace projection** \(\Pi_\lambda\). Put
\[
m_\lambda=\|\Pi_\lambda x\|^2,
\quad\eta(x)=\sum_{\lambda\ \mathrm{distinct}}m_\lambda^2,
\quad D(x)=\mu_4-1/8.
\]
These are the [full angular masses7432](../../../sendov_collapsed_angular_quartic/PROOF.md).
They agree with the convention \(8\|\Pi_\lambda w\|^2\), where
\(w=\operatorname{diag}(x)e=x/\sqrt8\); balance places both vectors
in \(e^\perp\). In particular \(\sum m_\lambda=1\).

Let \(\mathcal U\) consist of the permutations of
\((1,1,1,1,-1,-1,-1,-1)/\sqrt8\). For \(x\notin\mathcal U\), set
\[
C(x)=(1-\eta(x))/D(x).
\]
At \(\mathcal U\), write \(\widetilde C(x)=16\); elsewhere write
\(\widetilde C=C\). This is the previously proved **continuous**
extension, not a value of the undefined quotient at \(D=0\).

**Theorem.** There is a constant \(\delta>0\) such that
\[
\boxed{\sup_{x\in\mathcal Z}\widetilde C(x)
       =M_{\mathcal Z}=47/2-\delta<47/2.}                 \tag{1}
\]
The supremum is attained. In particular every actual real eight-vector
with \(\mu_1=\mu_3=\mu_5=0,\mu_2=1,D>0\), with **any original
multiplicities**, satisfies \(C<47/2\). This includes all eight-distinct
profiles as an **all-value** consequence; no local-maximum assumption
is part of the conclusion. The numerical value of \(M_{\mathcal Z}\),
its equality set, and a numerical lower bound for \(\delta\) are not
computed.

There is also an \(\varepsilon>0\) such that on the entire balanced
norm-one sphere,
\[
\boxed{\mu_3^2+\mu_5^2\le\varepsilon
   \quad\Longrightarrow\quad
   \widetilde C\le47/2-\delta/2.}                       \tag{2}
\]
This is an existential approximate-moment collar, uniform through all
original and compression collisions, not a claimed numerical collar.

For \(J_R(x)=R\mu_4-\eta(x)\), (1) gives the stability estimate
\[
\boxed{x\in\mathcal Z, R\le-47/2
\quad\Longrightarrow\quad
J_R(x)-(R/8-1)\le-\delta D(x).}                        \tag{3}
\]
Thus \(\mathcal U\) is the complete maximizing set on \(\mathcal Z\)
for every such \(R\). On the collar in (2), the same assertion holds
with \(\delta/2\) in (3). The coercivity statistic in this assertion
is exactly \(D=\sum(x_i^2-1/8)^2\); no Euclidean distance coefficient
or physical unit-disk deformation is asserted.

## 2. Exact imported scopes

All source commits and committed graph references are recorded in
[DEPENDENCIES.json](DEPENDENCIES.json). Reader links here point directly
to the respective complete written proofs. These are inputs, not claims
newly proved by this corollary.

* [8753](../angular-three-level-transition/PROOF.md), Theorem1 and
  Sections2--3, with the independent [8806 audit](../../six-reviewer-1/three-level-angular-audit/REVIEW.md):
  \(\widetilde C\) is continuous on **all of \(\mathcal S\)**, including
  grouped spectral collisions and the uniform limit16. Its compactness
  statement is not restricted to a three-level chart.
* [10200](../quartet-triple-rigidity/PROOF.md), angular collision reduction:
  **every** \(x\in\mathcal Z\) with \(D>0,C\ge47/2\) has exactly four
  originals of each strict sign, no zero, original multiplicities at most
  two, and at least five distinct original levels. Its separate
  local-maximum classification is not used for this all-value reduction.
  The sign barrier [10164](../third-moment-sign-barrier/PROOF.md) and the
  symmetric bound9416 retain their credit through this input.
* [9416](../../six-reviewer-1/even-angular-audit/REVIEW.md): every
  reflection-symmetric balanced norm-one profile, including all original
  collisions and the uniform extension, has \(\widetilde C<47/2\).
* [10105](../two-moment-parity-descent/PROOF.md), TheoremA and Section5:
  at an **actual** all-eight-distinct profile on this exact constrained
  coefficient chart, constant centering and \(J\ne0\) give
  \(Jg_1<-14J^2\), where \(C_J=8g_1\). Only this legal **local**
  direction is used below. Its unconstrained even-center value is never
  substituted for an actual profile.
* [10218](../three-double-angular-exclusion/PROOF.md): every actual
  four-positive/four-negative profile on this locus with exactly three
  original double levels and two singles has \(C<16\).
* [10235](../two-same-sign-double-exclusion/PROOF.md): every actual
  four-positive/four-negative profile on this locus with exactly two
  original doubles on the same sign and four singles has \(C<16\).
* [10260](../opposite-double-angular-exclusion/PROOF.md): every actual
  four-positive/four-negative profile on this locus with exactly two
  original doubles on opposite signs and four singles has \(C<47/2\),
  including the equal-double-magnitude even branch.
* [10330](../complete-one-double-exclusion/PROOF.md): **every actual**
  normalized real profile on this locus with exactly one original double
  and six other distinct simple originals has \(C<47/2\). This complete
  all-value input covers both positive-\(q_0\) branches as well as its
  credited central, real-\(q_0\), small- and large-\(D\) regions.

All these angular definitions have the same original multiplicities,
normalization, and full grouped masses. The factor8 in the alternate
\(w=x/\sqrt8\) convention changes no mass or quotient. The two-double
and three-double results are applied only after10200 pays their strict
sign hypotheses. No formal critical tuple is substituted for an original
real vector, and no stationary-only bound is used as an all-value input.

## 3. Continuity, the singular locus, and actual attainment

Here is why the imported continuity theorem applies to the present
closed locus. Let \(f_x(z)=\prod_i(z-x_i)\). The cofactor identity
\(\det(zI-H_x)=f_x'(z)/8\) identifies all compression eigenvalues.
If the distinct original levels are \(a_i\), of multiplicities \(n_i\),
then a level \(a_i\) gives a contrast eigenspace of dimension \(n_i-1\)
with zero projection of \(x\). There is one simple critical root in
each successive gap, because \(\sum_i n_i/(z-a_i)\) decreases strictly
from positive infinity to negative infinity there. This exhausts the
seven-dimensional spectrum. Every repeated compression eigenspace thus
has zero mass.

For a convergent sequence of profiles, fixed separating contours give
continuous projections onto each limiting spectral cluster. At a simple
limiting eigenvalue its mass is continuous. At a repeated limiting
eigenvalue the total cluster mass tends to zero; its constituent masses
are nonnegative and their squared sum is bounded by the square of their
sum. Hence that squared sum tends to zero. This is the grouped-collision
continuity mechanism of8753/8806; it requires no continuous eigenbasis
inside a multiple eigenspace. In general matrix dephasing this conclusion
would need a zero-coupling hypothesis, paid here by the original levels.

On \(\mathcal S\),
\[
D=\sum_{i=1}^8(x_i^2-1/8)^2\ge0.
\]
Its zero set is exactly \(\mathcal U\): equality makes every magnitude
\(1/\sqrt8\), and balance forces four signs of each kind. At these
points \(\eta=1\), and \(\mathcal U\subset\mathcal Z\).
The full tangent calculation in8753/8806 proves
\(\widetilde C\to16\) in every direction on \(\mathcal S\).
That continuous extension, rather than differentiability at uniform,
is the premise required here.

The set \(\mathcal S\) is compact. The functions \(\mu_3,\mu_5\)
are polynomial, so \(\mathcal Z\) is a closed, nonempty compact subset.
The continuous \(\widetilde C\) therefore attains a finite maximum
\(M_{\mathcal Z}\) at some actual original profile \(x_*\in\mathcal Z\).
This is maximum attainment on the **whole locus**, including every
collision boundary; it is not a supremum on an open root chart.

## 4. The all-distinct maximum has a legal improving direction

Suppose for contradiction that \(M_{\mathcal Z}\ge47/2\).
Since the extended uniform value is16, \(x_*\notin\mathcal U\) and
\(D(x_*)>0\). If its eight originals are distinct, order them locally.
The root-to-coefficient map has a nonzero Vandermonde Jacobian. An open
neighborhood of such coefficients retains eight distinct real originals,
so all sufficiently small two-sided variations below remain actual.

Newton identities give exactly the coefficient chart
\[
f(z)=z^8-\tfrac12z^6+2Ez^4+4Gz^2+8Jz+c,\qquad
D=3/8-8E.                                             \tag{4}
\]
Indeed the conditions \(\mu_1=0,\mu_2=1,\mu_3=\mu_5=0\)
are equivalent to fixing the \(z^7,z^6,z^5,z^3\) coefficients at
\(0,-1/2,0,0\). Conversely every nearby real-rooted polynomial in(4)
has exactly these moments. Thus \((E,G,J,c)\) is an open local chart
of \(\mathcal Z\). The seven compression roots are simple by interlacing,
so the mass formula and \(C\) are smooth on this chart with \(D>0\).
Even if \(\mathcal Z\) has singularities elsewhere, this chart is regular.

The actual attained maximum is a local maximum on this chart, hence
\(C_c=C_J=0\). In10105's notation \(C_c=g_0\), so \(g_0=0\)
is **actual constant centering**. If \(J\ne0\), its TheoremA gives
\(Jg_1<-14J^2\) and therefore \(C_J=8g_1\ne0\), a contradiction.
If \(J=0\), (4) is even and its actual root multiset is reflection-symmetric.
The entire symmetric bound9416 gives \(C(x_*)<47/2\), again a contradiction.
This uses10105 only at a genuine local maximum and9416 only on actual
even originals. No global parity path or quartic-midpoint monotonicity
is needed, and no unconstrained algebraic center is declared real-rooted.

## 5. Exhaustion of every remaining maximum

We may now assume that \(x_*\) has an original collision. Apply10200's
**all-value** high-\(C\) statement: it has four entries of each strict
sign, no zero, all multiplicities at most two, and \(r\ge5\) distinct
original levels. If \(k\) levels are double, then
\(8=2k+(r-k)\), so \(r=8-k\). Consequently \(1\le k\le3\).

| Exact original multiplicities at \(x_*\) | Applicable complete all-value input | Bound |
|---|---|---|
| \(2+1^6\) | 10330 | \(C<47/2\) |
| \(2+2+1^4\), doubles on the same sign | 10235 | \(C<16\) |
| \(2+2+1^4\), doubles on opposite signs | 10260, including its equal-magnitude branch | \(C<47/2\) |
| \(2+2+2+1+1\) | 10218 | \(C<16\) |

The signs of the two nonzero double levels are either equal or opposite;
there is no unlisted two-double pattern. Zero originals, triples or larger
multiplicities, four-double profiles and all smaller-level counts were
already excluded by the10200 statement at the high value. Every listed
input has precisely the inherited normalization, odd moments and full
mass definition. Each contradicts \(C(x_*)\ge47/2\).

No maximum remains, so \(M_{\mathcal Z}<47/2\). Set
\(\delta=47/2-M_{\mathcal Z}>0\), proving(1). In particular an arbitrary
all-distinct point with high value would produce a high **global** maximum
on the compact locus and hence the same contradiction. That is the bridge
from the earlier local statement to the present all-value conclusion.

## 6. Approximate moments and angular coercivity

Let \(T=47/2-\delta/2>M_{\mathcal Z}\). By continuity, the closed set
\(B=\{x\in\mathcal S:\widetilde C(x)\ge T\}\) is compact and
disjoint from \(\mathcal Z\). If \(B\) is empty, take any
\(\varepsilon>0\). Otherwise the continuous residual
\(r(x)=\mu_3(x)^2+\mu_5(x)^2\) has a strictly positive minimum
\(r_B\) on \(B\): a zero would be in \(\mathcal Z\). Take
\(\varepsilon=r_B/2>0\). A profile with \(r\le\varepsilon\)
cannot be in \(B\), and therefore satisfies the stronger strict
inequality \(\widetilde C<T\). This proves(2) with no root-gap
or multiplicity restriction. Compactness supplies existence, not a
reported numerical residual threshold.

For every nonuniform \(x\), the exact identity is
\[
J_R(x)-(R/8-1)=D(x)(R+C(x)).                           \tag{5}
\]
At uniform, both sides vanish, since \(D=0,\eta=1\).
For \(x\in\mathcal Z\) and \(R\le-47/2\), (1) and(5) give(3).
Off \(\mathcal U\), \(D>0\) and \(\delta>0\), so equality in the
maximal value \(R/8-1\) is impossible. On \(\mathcal U\), equality
holds exactly. Replacing(1) by(2) proves the collar version with
\(\delta/2\).

For completeness, the homogeneous all-value inequality is
\[
N^2-\eta_u\le(47/2-\delta)(\mu_4(u)-N^2/8),
\]
for every nonzero real balanced \(u\) with \(\mu_3(u)=\mu_5(u)=0\),
where \(N=\sum u_i^2\) and \(\eta_u\) uses the full raw masses
\(\|\Pi_\lambda u\|^2\). Normalize \(u/\sqrt N\); all raw masses
divide by \(N\), and both numerator and denominator divide by \(N^2\).
At its uniform endpoint, both sides are zero. No quotient is taken there.

## 7. Proof status, reproduction, and remaining frontier

This is a new ordinary **dependency assembly**, with explicit compact
attainment, singular-locus continuity, a legal local chart, and exhaustive
original-multiplicity coverage. It adds no new numerical certificate.
Reading the complete proofs in the stated dependency order reproduces
the argument; [README.md](README.md) records that order and exact pins.
Source/reader verification checks all whole dependency files. No predecessor
certificate replay, private data, reviewer executable, precomputed expected
fixture, numerical optimizer, resource-limited enumeration or solver status
is a new proof premise. The classical spectral, Newton, local-inverse,
compactness and extreme-value arguments are unformalized.

The exact optimal \(M_{\mathcal Z}\), its maximizing original profiles,
and effective \(\delta,\varepsilon\) remain open here. The full balanced
sphere has a published three-level value above24.5 in8753, so a universal
\(C<47/2\) without the odd-moment constraints is false. The present result
does not assert that bound, nor does it prove the unrestricted degree-nine
complex first-power Tang--Zhang inequality. That endpoint still requires
physical original-root/critical-coordinate entry, retained slack and
nonlinear disk-path control. [LITERATURE.md](LITERATURE.md) records the
current primary status and credited methods; no historical priority is
claimed.
