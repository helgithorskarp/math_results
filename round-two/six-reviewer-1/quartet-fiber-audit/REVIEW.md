# Independent positive-quartet and feasible-fiber audit

Actual **six-reviewer-1**, role **independent mathematical reviewer**, 2026-10-04.
Target: LEMMA10200/index0, **Positive-quartet rigidity, original-triple
angular exclusion and a feasible quartic midpoint**,
artifact **bafkreigfwlmump2onl4wf2aaov36devapvkcjkb3ub3gsfgl5tbgirrlg4**.
Author identified explicitly in its signed body: six-sendov-2/researcher.
Target source: **500529f784055cdce54206a44aea0867c4bd0687**.

**Verdict: CONFIRMS the stated quartet rigidity, complete positive-root
fiber, actual midpoint and high-value collision restriction, relative to
the explicitly retained angular inputs below.** The proof is ordinary and
unformalized. Independent exact arithmetic supports its finite bridges;
it does not formalize the compactness, IFT or universal root-count argument.
No verdict on the whole10105 or10136 leaf is transferred or asserted.

**Proved refinement:** in the normalized angular domain with
\(\mu_1=\mu_3=0\) and \(C\ge47/2\), the direction quadratic satisfies
\[
 q(z)\ge\frac{84113}{1118600}>0\qquad(z\in\mathbb R).
\]
This quantitative direction statement does not require \(\mu_5=0\).
The quartet-rigidity and odd-moment-preserving midpoint statements still do.
This review also records the ordered simple-root velocity signs on the
feasible fiber. Neither assertion proves angular monotonicity, an optimal
angular value, a disk-polynomial deformation or the complex first-power
endpoint.

## Scope and retained premises

Write \(\mu_j=\sum_{i=1}^8u_i^j\). For real balanced originals with
\(\mu_2=1\), use the7432 full orthogonal-compression convention:
\(e=(1,\ldots,1)/\sqrt8\), \(P=I-ee^T\),
\(H=(P\operatorname{diag}(u)P)|_{e^\perp}\), and
\(w=\operatorname{diag}(u)e\). For each *whole* eigenspace set
\(\rho_\lambda=8\|\Pi_\lambda w\|^2\),
\(\eta_{\rm ang}=\sum_\lambda\rho_\lambda^2\),
\(D=\mu_4-1/8>0\), \(C=(1-\eta_{\rm ang})/D\).
All masses, including repeated eigenspaces and zero masses, use this
convention; \(\sum\rho_\lambda=1\) and
\(\eta_{\rm ang}\ge1/7\).

The sign-sector premise is10164's strict \(C<144/7\) when \(\mu_3=0\)
and either strict sign has at most three originals. Its entire target was
previously confirmed in this reviewer's10186, which also proved404/23.
The stronger404/23 value is credited context, not needed here.
The reflection-symmetric premise is this reviewer's9416 ordinary
strengthening \(C<47/2\), including all original and critical collisions.
These two results and the full7432 definitions are retained explicit inputs.
They are not newly reviewed by replaying this leaf.

The final local-maximum restriction credits10105's relevant constrained
parity argument. Section4 independently reconstructs only the simple
Schur nonvanishing part needed at high value. It neither audits all of
10105's quantitative constants nor imports its unconstrained even center
as an actual profile.10136 is a downstream collision chart, not a proof
premise for quartet rigidity.8851 supplies credited support-face
methodology;8753 supplies earlier angular continuity context. Classical
linear algebra, interlacing, Newton, IFT and Sturm theory are retained.

## 1. Quartet rigidity, with every support boundary paid

Fix \(S>0\) and \(S^3/16<K<S^3\). The nonnegative four-coordinate
set with first sum \(S\) and third sum \(K\) is compact. It is nonempty:
\(((S-y)/3,(S-y)/3,(S-y)/3,y)\) has third sum
\(G(y)=(S-y)^3/9+y^3\), which increases strictly from \(S^3/16\)
to \(S^3\) for \(S/4<y<S\). The same function decreases strictly
from \(S^3/9\) to \(S^3/16\) for \(0<y<S/4\).

At an extremum of the fifth sum on a positive support having at least
two distinct levels, the first/third constraint Jacobian has rank two.
Every tangent has an actual smooth feasible curve by IFT. The multiplier
equation
\[
 5x^4-3\lambda x^2-\mu=0
\]
has at most two positive roots. At levels \(a<b\), its exact factor is
\(5(x^2-a^2)(x^2-b^2)\), with
\(\lambda=5(a^2+b^2)/3,\ \mu=-5a^2b^2\).
The constrained Hessian is negative at \(a\) and positive at \(b\),
with values \(10a(a^2-b^2)\) and \(10b(b^2-a^2)\).
Splitting two equal entries by \((1,-1)\) is a feasible tangent.
Thus an interior minimum must be three-large/one-small, and an interior
maximum three-small/one-large. The two-level branches have unique parameters
by the preceding strict monotonicity.

For \(K<S^3/9\), every zero boundary is impossible by Jensen on at most
three positive entries. Hence the three-large/one-small branch is the
unique global fifth minimum there.

For the global fifth maximum, a boundary with two distinct positive
levels admits a zero opening while adjusting one entry at each level:
the adjustment determinant is \(3(b^2-a^2)>0\). The objective derivative
is \(-\mu=5a^2b^2>0\). More than two positive levels already violates
the multiplier equation. A one-positive support would give \(K=S^3\),
excluded here.

The dependent constraint rows at two or three equal positive entries
cannot be discarded. For \(k=2,3\), open one zero to \(cx\) and replace
two equal \(c\)'s by \(c(a+\delta),c(a-\delta)\), the other \(k-2\)
by \(ca\), where
\[
 a=1-x/k,\qquad \delta^2=(k-ka^3-x^3)/(6a),\qquad0<x\le1/4.
\]
First and third sums remain \(kc,kc^3\). The fifth sum divided by \(c^5\)
is \(F_k=ka^5+20a^3\delta^2+10a\delta^4+x^5\).
All six numerator/denominator pairs for
\(\delta^2/x,\ a^2-\delta^2,\ (F_k-k)/x\) have strictly positive
complete Bernstein vectors on \([0,1/4]\). Both independent engines
reconstruct the full rational identities and all twelve vectors.
This proves actual positive openings with \(F_k>k\), including all
remaining zero boundaries. Also \(F_k'(0)=5\).
Therefore the global fifth maximum is the unique three-small/one-large
branch for the entire stated range of \(K\).

For \((t,t,t,s)\), \(t,s>0\), the identities
\[
16K-S^3=3(s-t)^2(5s+7t),\quad
S^3-K=3t(8t^2+9ts+3s^2),
\]
\[
S^3-9K=s(27t^2+9ts-8s^2)
\]
put \(s>t\) on the unique maximum branch and \(0<s<t\) on the
unique minimum branch with \(K<S^3/9\). Matching the fifth sum forces
that same quartet, up to permutation. If \(s=t\), Jensen equality
forces all entries equal. Comparison quartets may be nonnegative;
the proof actually excludes their boundary alternatives.

Consequently a four-positive/four-negative vector with
\(\mu_1=\mu_3=\mu_5=0\) and an original triple or quadruple is
reflection-symmetric. The fifth hypothesis is essential. The exposed
positive quartets \((1,1,1,1/2)\) and
\((a,a,a,b)\), \(a=(47-3\sqrt{57})/32\),
\(b=(-29+9\sqrt{57})/32\), match first and third sums but differ at
the fifth by
\((14592015-1946835\sqrt{57})/262144<0\).
Exact reduction modulo \(v^2-57\) checks all three differences.
The rational enclosure \(15/2<\sqrt{57}<38/5\) proves both positivity
and the strict sign; no approximate radical is used.

## 2. The entire positive-root fiber and actual midpoint

Given positive-quartet first/third/fifth sums \(S,K,L\), let
\[
 T=(K-S^3)/3,\quad U=(S^5+5S^2T-L)/(5S),\quad
 R=-T^2-S^2U,\quad q(z)=z^2-Sz-T/S.
\]
Newton identities give the complete coefficient pencil
\[
 g_A=z^4-Sz^3+Az^2-(SA+T)z+U-TA/S
     =q(z)(z^2+A+T/S)-R/S^2 .
\]
The independently expanded six-pair Orlando product is
\[
 R=SAe_3-e_3^2-S^2e_4=\prod_{i<j}(a_i+a_j)>0.
\]
All divisions here require \(S>0\). This product identity and the pencil
are classical algebraic structure; no historical priority is asserted.

Suppose \(K<S^3/4\). Then
\(\operatorname{disc}q=(4K-S^3)/(3S)<0\), so \(q>0\) on the whole
real line. A triple/quadruple fiber is a singleton by Section1; so is
the Jensen boundary \(K=S^3/16\). In every other nonempty fiber put
\[
\Psi(z)=R/(S^2q(z))-z^2-T/S,\qquad
H_0(z)=zq(z)^2/(S-2z).
\]
The positive zeros of \(\Psi'\) lie in \((0,S/2)\) and satisfy
\(H_0=R/(2S^2)>0\). Its derivative numerator is \(qN\), where
\[
N=-8z^3+9Sz^2-3S^2z-T,\quad
N'=-3(4z-S)(2z-S).
\]
The values at \(0,S/4,S/2\) are respectively
\(-T>0,(S^3-16K)/48<0,(S^3-4K)/12>0\).
Thus \(H_0\) has exactly three monotone branches.
Any positive horizontal level meets at most three of them; a level through
a turning point meets at most two distinct branches.

A feasible quartet without a triple forces three distinct zeros of
\(\Psi'\): Rolle for four simple roots; a zero at every double and one
in each intervening distinct-root gap otherwise. This includes both
positions of a single double and the two-double case. Hence exactly
three simple critical points \(0<\alpha<\beta<\gamma<S/2\) exist.
Their types are maximum/minimum/maximum and derivative signs \(+,-,+,-\).
Outside this interval \(\Psi\) increases strictly on the negative
half-line and decreases strictly beyond \(S/2\).

It follows, with both necessity and sufficiency, that the complete
positive-real-root parameter set is
\[
 I=\{A:\ A>\Psi(0),\
 \Psi(\beta)\le A\le\min(\Psi(\alpha),\Psi(\gamma))\}.
\]
The four monotone positive intervals each supply one root, with multiplicity
counted at the limiting critical levels. The lower endpoint merges the
middle two; the upper merges one or both external pairs. Simplicity of the
critical points excludes triple roots here. \(A=\Psi(0)\) has a zero
original and is excluded; \(A<\Psi(0)\) has a negative original.
Degree four precludes an uncounted complex or extra real branch.
Thus this is one interval, with a possible open zero boundary.
In the nonsingleton case it has positive length and every relative interior
member has four simple positive roots.

For matching sign quartets with total squared norm one, set
\(\bar A=S^2/2-1/4\), \(A_\pm=\bar A\pm d\).
Two distinct feasible parameters have a strict interior midpoint.
All \(\bar A\pm td\), \(0\le t\le1\), stay in \(I\).
For \(d\ne0\), every \(t<1\) has four simple positive and four simple
negative originals; opposite signs cannot collide. The midpoint is actual
and symmetric. First, third and fifth odd moments remain zero and the
norm remains one throughout. A uniform midpoint would require an all-equal
positive quartet and hence a singleton fiber, contradicting \(d\ne0\);
therefore \(D>0\) also persists.

The complete original octic is
\[
 f(z)=(g_{\bar A}(z)+dq(z))(g_{\bar A}(-z)-dq(-z))
 =z^8-z^6/2+2Ez^4+4Gz^2+8Jz+c_0 .
\]
In particular \(J=dR/(4S)\), and all nine coefficients, including all
zeros, are checked. \(E,G,c_0\) move with \(d^2\).
This path is not the fixed-\((E,G)\) direction in10105.
There is no comparison of angular values along this feasible path in the
target or this review.

## 3. Competitive collisions and the new quantitative direction margin

The retained sign bound forces every \(C\ge47/2\) profile to have four
originals of each strict sign, with no zeros. Section1 makes every triple
symmetric, contrary to the retained symmetric bound. Thus multiplicities
are at most two. Four distinct original levels would all be doubled:
the positive pairs \((a,a,b,b)\) and negative pairs
\((-c,-c,-d,-d)\) have \(a+b=c+d>0\); equality of cubic sums then
gives \(ab=cd\). They too are symmetric. Hence at least five distinct
originals remain. All critical roots are simple: a simple derivative root
at each original double and one in each original-level gap, because
\(\sum m_i/(z-u_i)\) decreases strictly. The count is exactly seven.
Selecting one original double therefore permits the stated10136 chart;
its other original collisions still constrain legal variations.

Here is a quantitative strengthening of the direction step. It uses
\(\mu_3=0\), not \(\mu_5=0\). Write the common positive-quartet first
and third sums as \(S,K\), and their second sums as \(N_\pm>0\), with
\(N_++N_-=1\). Cauchy gives
\[
 SK\ge\max(N_+^2,N_-^2)\ge1/4,\qquad
 X:=\mu_4\ge K^2(1/N_++1/N_-)\ge4K^2 .
\]
Also \(\eta_{\rm ang}\ge1/7\) and \(C\ge47/2\), so
\[
 D\le12/329,\quad X\le425/2632,\quad
 S^2\ge1/(16K^2)\ge1/(4X)\ge658/425,\quad S^2\le2 .
\]
Since \(S\ge1/(4K)\),
\[
 \frac{4K}{S^3}\le256K^4\le16X^2\le(425/658)^2<1.
\]
Completing the square now proves uniformly
\[
 q(z)=(z-S/2)^2+\frac{S^3-4K}{12S}
 \ge\frac{84113}{1731856}S^2
 \ge\boxed{\frac{84113}{1118600}} .
\]
The complete rational scalar record is GAP.json. The constants are
sufficient bounds, not optimal values or a spectral-root separation
certificate. In particular positivity has a uniform margin in this
competitive angular domain.

## 4. The exact scope of the constrained local-maximum input

For eight distinct real originals, the constrained coefficient chart is
\((E,G,J,c_0)\). Real-rootedness is locally open; Newton gives exactly
the stated first/second/third/fifth constraints. No global change of the
centered primitive is licensed.

For the actual seven distinct criticals of
\(h=f'/8=z^7-3z^5/8+Ez^3+Gz+J\), the7432 resolvent gives actual
masses and the first six coupling moments
\[
 \nu=(1,0,3/8-8E,0,9/64-4E-24G,-56J).
\]
At fixed \(E,G,J\), changing \(c_0\) traces the entire one-dimensional
affine solution set for these moments. A local maximum must be its
Euclidean least-norm center. The six-by-six Gram matrix of critical
monomials is positive definite. In parity order it is
\[
 M=\begin{pmatrix}A&JU\\JU^T&B\end{pmatrix},\
 \nu=(u,Jv),\
 U=\begin{pmatrix}0&0&0\\0&0&-7\\0&-7&-27/8\end{pmatrix},\
 v=(0,0,-56).
\]
All even blocks are independent of \(J\); the independent engines derive
all traces through ten and all nine coupling entries.
Put \(y=A^{-1}u,w=v-U^Ty,Q=U^TA^{-1}U\),
\(\Sigma=B-J^2Q\succ0\). Schur elimination yields
\[
 R_6=u^TA^{-1}u+J^2w^T\Sigma^{-1}w,\qquad
 \partial_{J^2}R_6=w^T\Sigma^{-1}B\Sigma^{-1}w>0.
\]
For strictness, \(w=0\) would give \(y=(-5/7,8,0)\).
Its second normal equation forces \(E=25/448\), hence
\(D=-1/14\), impossible. At an actual center the chain rule therefore
gives \(J\,\partial_J C<0\) for \(J\ne0\).
Changing \(J\) slightly toward zero is a legal improvement in the open
actual chart. If \(J=0\), the actual profile is symmetric and already
has \(C<47/2\). Thus no high-value all-distinct local maximum remains.
Combining with at least five distinct originals leaves exactly one, two
or three original doubles:
\(2+1^6,\ 2+2+1^4,\ 2+2+2+1+1\).
These are necessary patterns, not existence or sufficiency claims.

This reproduces the relevant10105 mechanism with attribution. It does
not verify its whole quantitative gradient or integrated penalty theorem,
and it never replaces an actual profile by its possibly nonreal
unconstrained even center.

## Strengthening and improvement opportunities

**Established here:** the absolute direction margin84113/1118600,
including the relaxed \(\mu_5\) hypothesis for that statement alone.
On any nonsingular fiber interior with ordered roots
\(r_1<r_2<r_3<r_4\), IFT also gives
\[
 r_i'(A)=-q(r_i)/g_A'(r_i),\qquad
 (\operatorname{sign}r_i')=(+,-,+,-).
\]
The independent root-derivative products retain every factor.
This supplies ordered analytic root tracking on compact interior
subintervals. The octic Newton recurrence also gives exactly
\(\mu_4(d)=\mu_4(0)+4d^2\).
These refinements concern actual root flow and the denominator, not
monotonicity of the quotient \(C\).

The consequential unresolved task is to control the *full angular numerator*
while the even coefficients vary along this actual fiber, including
one/two/three-double endpoints. A fixed-even-coefficient penalty cannot
be inserted without paying those changes. Formalizing the support-face
IFT and all four root-count branches would remove the ordinary-proof
trust boundaries. Effective disk containment is a separate obligation.

The literature audit also located the exact four-versus-four
first/third/fifth Diophantine system in a1991 Choudhry citation.
Its full original text was not obtained, so no matching positivity,
rigidity or midpoint theorem is asserted. That narrow historical comparison
is worth completing before any priority claim. The target correctly makes
none.

## Independence, evidence and publication readiness

Written formulas, theorem numbers and prior9416/10186 proofs were exposed:
**NOT BLIND**. The two new arithmetic engines were written in this
workspace without importing or copying the target programs. Dense QQ
SymPy1.14.0 derivation and fresh standard-library Fraction coefficient,
Newton and Euclidean-Sturm reconstruction agree. Both use exact arithmetic;
there is no numerical root finding, solver or finite sample standing in
for a universal theorem.

Four primary files were sealed before intentional inspection of the target's
new native programs or expected record. The supplementary scalar files
were separately sealed before that inspection; the first four bytes were
unchanged. PRIMARY_SEAL.json and GAP_SEAL.json record exact dates and hashes.
The late comparison imports only the owned sealed portable checker and
reads author data, with explicit variable renamings. It compares36 complete
shared polynomial fields/all154 native nonzero entries. Native source
replays are subsequent corroboration, not the primary proof.

The independent full record has75 identities,21 complete polynomials,
12 complete Bernstein vectors and8 whole Sturm chains. Six normal,
optimized and cold-source positives agree, with6 method and20 typed
fixture rejections. The eight root controls include an excluded zero
endpoint, its actual positive interior neighbor, both sides of a
two-double endpoint and both sides of a triple singleton. Such controls
verify arithmetic and challenge omitted cases; the universal conclusions
are proved in Sections1–4.

The ordinary result is publication-ready within these explicit premises
and trust boundaries. The uniform gap is a campaign refinement, with no
claim of historical priority or optimality. LITERATURE.md separates
classical moment recovery/Newton/Orlando structure from the scoped Sendov
application and the still-open first-power endpoint. Source publication
and a committed review do not by themselves establish the mathematics.
